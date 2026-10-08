# The base image Linewright publishes: linewright, git and the agent runtime.
# Build your own image FROM it with your project's toolchain added, so the
# agents can build and test your code (docs/specs/product.md, "Operation").

FROM rust:1-bookworm AS build
WORKDIR /src
COPY . .
# Installs the toolchain rust-toolchain.toml pins.
RUN rustup toolchain install && cargo build --release --locked

FROM node:22-bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates tini \
    && rm -rf /var/lib/apt/lists/*
RUN npm install --global @anthropic-ai/claude-code
COPY --from=build /src/target/release/linewright /usr/local/bin/linewright
# Agents run without permission prompts; the container is the isolation, and
# they run as an ordinary user inside it.
RUN useradd --create-home linewright
USER linewright
WORKDIR /home/linewright
# tini runs as PID 1: it passes signals on to linewright and reaps the
# processes left behind when an agent session is killed
# (<https://github.com/krallin/tini>).
ENTRYPOINT ["tini", "--", "linewright"]
CMD ["serve"]
