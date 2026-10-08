//! The tracking issue of a spec change (`docs/spec.md`, "Tickets"): its
//! title and body, which the manager writes and the reconcile step reads back
//! to find the spec change a tracking issue belongs to.

use crate::domain::{Issue, Login, Number};

const TITLE_PREFIX: &str = "Spec change: ";

pub fn title(pr_title: &str) -> String {
    format!("{TITLE_PREFIX}{pr_title}")
}

pub fn body(pr: Number, tickets: &[(Number, String)]) -> String {
    let list: String = tickets
        .iter()
        .map(|(number, title)| format!("- {number} {title}\n"))
        .collect();
    format!("Tickets for the spec change in {pr}.\n\n{list}")
}

/// The spec change the issue tracks, if it is a tracking issue.
pub fn spec_change_of(issue: &Issue, machine_user: &Login) -> Option<Number> {
    if &issue.author != machine_user || !issue.title.starts_with(TITLE_PREFIX) {
        return None;
    }
    let first = issue.body.lines().next()?;
    let rest = first.strip_prefix("Tickets for the spec change in #")?;
    let digits: String = rest.chars().take_while(char::is_ascii_digit).collect();
    digits.parse().ok().map(Number)
}
