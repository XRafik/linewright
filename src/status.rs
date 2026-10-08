//! `linewright status`: the work in flight, derived from a snapshot the way
//! the reconcile step derives it.

use crate::domain::{CheckState, PullState, Snapshot, Timestamp, label};
use crate::reconcile::{Policy, pending_spec_changes};
use crate::tracking;

pub fn report(snapshot: &Snapshot, now: Timestamp, policy: &Policy) -> Vec<String> {
    let machine = &policy.machine_user;
    let mut lines = vec![];
    for pr in pending_spec_changes(snapshot, now, policy) {
        lines.push(format!(
            "{} {}: spec change waiting for tickets",
            pr.number, pr.title
        ));
    }
    for issue in snapshot.issues.iter().filter(|i| i.open) {
        let state = if tracking::spec_change_of(issue, machine).is_some() {
            let closed = issue.sub_issues.iter().filter(|t| !t.open).count();
            format!(
                "tracking issue, {closed}/{} tickets closed",
                issue.sub_issues.len()
            )
        } else if issue.has_label(label::NEEDS_TRIAGE) {
            "waiting for triage".into()
        } else if issue.has_label(label::NEEDS_INFO) {
            "waiting on the reporter".into()
        } else if issue.has_label(label::READY_FOR_HUMAN) {
            "with the maintainer".into()
        } else if issue.has_label(label::READY_FOR_AGENT) {
            let pr = snapshot
                .pulls
                .iter()
                .find(|p| p.is_open() && &p.author == machine && p.closes.contains(&issue.number));
            let blockers: Vec<String> = issue
                .blocked_by
                .iter()
                .filter(|b| b.open)
                .map(|b| b.number.to_string())
                .collect();
            match pr {
                Some(pr) => {
                    let ci = if pr.checks.is_empty() {
                        "no checks"
                    } else if pr.checks.iter().any(|c| c.state == CheckState::Failed) {
                        "CI failing"
                    } else if pr.checks.iter().any(|c| c.state == CheckState::Pending) {
                        "CI running"
                    } else {
                        "CI green"
                    };
                    let stage = match pr.state {
                        PullState::Open { draft: true } => "draft",
                        _ => "ready for review",
                    };
                    format!("in review: {} ({stage}, {ci})", pr.number)
                }
                None if !blockers.is_empty() => format!("blocked by {}", blockers.join(", ")),
                None if issue.is_assigned(machine) => "claimed: being implemented".into(),
                None => "ready to claim".into(),
            }
        } else {
            continue;
        };
        lines.push(format!("{} {}: {state}", issue.number, issue.title));
    }
    lines
}
