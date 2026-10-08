//! The marker line that opens every Linewright comment (`docs/specs/product.md`,
//! "Visibility"), so people and the manager can tell its comments from
//! others.

use std::fmt;

use crate::domain::{Comment, Login};

/// The stage of the pipeline a comment reports on.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Stage {
    Triage,
    Tickets,
    Implementation,
    Ci,
    Review,
    Rework,
    Update,
}

impl Stage {
    const ALL: [Stage; 7] = [
        Stage::Triage,
        Stage::Tickets,
        Stage::Implementation,
        Stage::Ci,
        Stage::Review,
        Stage::Rework,
        Stage::Update,
    ];

    fn name(self) -> &'static str {
        match self {
            Stage::Triage => "triage",
            Stage::Tickets => "tickets",
            Stage::Implementation => "implementation",
            Stage::Ci => "CI",
            Stage::Review => "review",
            Stage::Rework => "rework",
            Stage::Update => "update",
        }
    }
}

impl fmt::Display for Stage {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.name())
    }
}

/// A comment body opening with the stage's marker line.
pub fn marked(stage: Stage, body: &str) -> String {
    format!("> *Linewright, {stage}*\n\n{}", body.trim())
}

/// The stage of a comment the machine user wrote with a marker line, if it
/// is one.
pub fn stage_of(comment: &Comment, machine_user: &Login) -> Option<Stage> {
    if &comment.author != machine_user {
        return None;
    }
    let first = comment.body.lines().next()?.trim();
    Stage::ALL
        .into_iter()
        .find(|stage| first == format!("> *Linewright, {stage}*"))
}
