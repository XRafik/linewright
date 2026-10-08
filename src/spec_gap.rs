//! A spec gap that did not block its ticket (`docs/spec.md`, "Implementation"):
//! an issue whose body the manager writes and reads back, so later sessions
//! on the ticket see the gaps already filed and don't file them again.

use crate::domain::{Issue, Login, Number, Snapshot};

fn footer(ticket: Number) -> String {
    format!("Found while working on {ticket}.")
}

pub fn body(gap: &str, ticket: Number) -> String {
    format!("{}\n\n{}", gap.trim(), footer(ticket))
}

/// The open spec gaps filed while working on the ticket.
pub fn filed_for<'a>(
    snapshot: &'a Snapshot,
    ticket: Number,
    machine_user: &Login,
) -> Vec<&'a Issue> {
    let footer = footer(ticket);
    snapshot
        .issues
        .iter()
        .filter(|i| i.open && &i.author == machine_user && i.body.trim_end().ends_with(&footer))
        .collect()
}
