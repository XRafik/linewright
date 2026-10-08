# The base image Linewright publishes: linewright, git and the agent runtime.
# Build your own image FROM it with your project's toolchain added, so the
# agents can build and test your code (docs/spec.md, "Operation").

FROM rust:1-bookworm AS build
WORKDIR /src
COPY . .
RUN cargo build --release --locked

FROM node:22-bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN npm install --global @anthropic-ai/claude-code
COPY --from=build /src/target/release/linewright /usr/local/bin/linewright
# Agents run without permission prompts; the container is the isolation, and
# they run as an ordinary user inside it.
RUN useradd --create-home linewright
USER linewright
WORKDIR /home/linewright
ENTRYPOINT ["linewright"]
CMD ["serve"]
