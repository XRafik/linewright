# Checks

Run these before every commit, and fix what they report. CI runs the same
checks and fails on any warning.

- `cargo fmt`
- `CARGO_BUILD_WARNINGS=deny cargo clippy --all-targets --locked`
- `CARGO_BUILD_WARNINGS=deny cargo test --locked`
- `CARGO_BUILD_WARNINGS=deny cargo doc --no-deps --locked`
