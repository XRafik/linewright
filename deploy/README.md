# Running Linewright on itself

`compose.yaml` runs Linewright on this repository in Docker, locked down:
agents reach the network only through
[Smokescreen](https://github.com/stripe/smokescreen), a proxy that refuses
private addresses, so they get the public internet but not the host, the LAN,
or other containers. Tools that ignore `https_proxy`, or use SSH, cannot
connect.

Run the commands here from `deploy/`; to run it on another machine, point
Docker at it with a
[context](https://docs.docker.com/engine/manage-resources/contexts/), and the
image is built there.

1. Copy `.env.example` to `.env` and fill it in: `GH_TOKEN`, the token of
   the factory's GitHub user, and either `ANTHROPIC_API_KEY` or a
   `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`.

2. Optionally, set what this host needs in `compose.override.yaml`, such as
   a directory of the host's for the work directory, in place of a volume,
   owned by the agents' user, and limits. If Docker runs on another machine,
   name its context in `CLAUDE.local.md` at the repository's root, so coding
   agents deploy and watch it there too.

   ```yaml
   x-user: &user
     args: {LINEWRIGHT_UID: "1500", LINEWRIGHT_GID: "1500"}
   services:
     runtime: {build: *user}
     base: {build: *user}
     linewright:
       volumes: ["/srv/linewright:/data"]
       mem_limit: 8g
       environment: {LINEWRIGHT_MAX_WORKERS: 2}
   ```

3. Build and start it, and follow its log:

   ```sh
   docker compose up -d --build
   docker compose logs -f
   ```

## Deploying and watching it

With Docker on another machine, pass its context to each command:
`docker --context NAME compose ...`.

- Deploy another version: check it out, such as by pulling `main`, and rerun
  step 3. The image is built from the working tree, uncommitted changes
  included.
- The server's log, a JSON line for each decision and action:
  `docker compose logs -f linewright`.
- The work in flight: `docker compose exec linewright linewright status`.
- What each agent session did: its record, under
  `/data/OWNER/NAME/sessions/` in the container. There is a directory for
  each issue (`issue-N`), spec PR (`pr-N`) and workflow (`workflow-NAME`),
  and in it one for each session, named by its start time (UTC) and kind:
  - `brief.md`: what the session was asked, and `followup-N.md` after it;
  - `output.jsonl`: its output, written as it runs;
  - `result.json`, `trace.jsonl` (the full transcript) and `stderr.log`,
    written when it ends.

  For example, the latest session for issue 3:

  ```sh
  docker compose exec linewright bash -c \
    'ls -td /data/tibbe/linewright/sessions/issue-3/* | head -1'
  ```

- What the proxy refused: `docker compose logs proxy | grep '"allow":false'`.
