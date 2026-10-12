# syntax=docker/dockerfile:1

FROM runtime
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev curl \
    && rm -rf /var/lib/apt/lists/*
ENV RUSTUP_HOME=/usr/local/rustup CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH
RUN install -d -o linewright -g "$(id -g linewright)" \
    "$RUSTUP_HOME" "$CARGO_HOME" "$CARGO_HOME/registry" /data
USER linewright
RUN install -d -m 700 /home/linewright/.claude
COPY rust-toolchain.toml /tmp/toolchain/
ARG RUSTUP_VERSION=1.29.1
RUN curl --proto '=https' --tlsv1.2 -sSf -o /tmp/rustup-init.sh https://sh.rustup.rs \
    && RUSTUP_VERSION=$RUSTUP_VERSION sh /tmp/rustup-init.sh -y --no-modify-path \
        --profile minimal --default-toolchain none \
    && rm /tmp/rustup-init.sh \
    && cd /tmp/toolchain && rustup toolchain install
COPY linewright.toml ./
COPY --link --from=base /usr/local/bin/linewright /usr/local/bin/linewright
