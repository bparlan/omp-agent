# VPS Migration Report — OMP Agent → Coolify Docker

## 1. Host / Container Path Model

| Layer | Path | Role |
|-------|------|------|
| VPS host | `/home/<user>/devcode` | Base directory for all projects |
| Container mount | `/devcode` | OMP workspace root inside container |
| OMP root | `/devcode` | Treated as project root for relative paths and artifact resolution |

### Directory Layout

```
[ VPS Host ]
/home/<user>/devcode/          ──►  [ Container ]
  ├── aef-agent/                      ├── /devcode/aef-agent/
  ├── project-1/                      ├── /devcode/project-1/
  └── project-2/                      ├── /devcode/project-2/
```

**Recommendation:** Use relative paths when prompting OMP inside the container. For absolute references, set `WORKSPACE_ROOT=/devcode` and reference paths as `${WORKSPACE_ROOT}/...`.

---

## 2. Required Environment Variables

| Variable | Purpose | Required | Source / Default |
|----------|---------|----------|------------------|
| `OPENAI_API_KEY` | FreeLLMAPI OpenAI-compatible provider auth | Yes | Injected via Coolify env |
| `ANTHROPIC_API_KEY` | Anthropic-compatible proxy auth | Yes | Injected via Coolify env |
| `PROJECT_ROOT` | Canonical project root for artifact resolution | Conditional | `/devcode` |
| `ARTIFACT_REGISTRY_PATH` | Canonical artifact registry location | Conditional | `/devcode/milestones` |
| `PYTHONPATH` | Test/runtime module resolution | Yes for tests | `/devcode` |
| `PATH` | Binary discovery for `bin/*` tools | Yes | `/devcode/bin:/home/omp/.local/bin:${PATH}` |
| `TERM` | Terminal capability for tmux/CLI | Yes | `xterm-256color` |
| `HOME` | User home for `.aef-env` lookups | Yes | `/home/omp` |
| `WORKSPACE_ROOT` | Absolute workspace root for scripts | Yes | `/devcode` |
| `NODE_VERSION` | mise-managed Node.js version hint | No | `22` from `mise.toml` |
| `PAGER` | Pager behavior | No | `less -R` recommended |

**Security note:** No `.env` file is committed in this repo. Inject all secrets through Coolify environment variables. Do not bake secrets into the Docker image.

---

## 3. Docker Volumes and State Paths

### Volume Mappings

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `/home/<user>/devcode` | `/devcode` | Workspace root containing all projects |
| `./.omp` | `/devcode/.omp` | OMP config and graph metadata |
| `./.aef-env` | `/home/omp/.aef-env` | Workspace environment isolation |
| `./sessions` | `/devcode/sessions` | Active session state |
| `./cache` | `/devcode/cache` | Runtime cache |
| `./blobs` | `/devcode/blobs` | OMP state/media |
| `./terminal-sessions` | `/devcode/terminal-sessions` | Tmux/terminal session state |
| `./.venv` | `/devcode/.venv` | Python virtualenv |
| `./milestones` | `/devcode/milestones` | Milestone artifacts |
| `./skills` | `/devcode/skills` | Skill definitions and templates |
| `./core` | `/devcode/core` | Runtime core modules |
| `./data` | `/devcode/data` | Data layer |
| `./docs` | `/devcode/docs` | Documentation layer |
| `./CONTRACTS` | `/devcode/CONTRACTS` | Contract artifacts |

### State / Cache / Mental Model Paths

| Path | Purpose |
|------|---------|
| `sessions/` | Active session state |
| `cache/` | Runtime cache |
| `blobs/` | OMP state/media |
| `terminal-sessions/` | Tmux/terminal session state |
| `.aef-env/` | Workspace environment isolation |
| `.omp/graph/` | Ladybug graph state |
| `.venv/` | Python virtualenv |
| `code_index_*.db` | Code search indexer databases |

**Excluded from mounts by design:** `.git/`, `__pycache__/`, `.pytest_cache/`, `node_modules/`, `*.log`, `*.jsonl`

---

## 4. Minimal Dockerfile

```dockerfile
FROM python:3.12-slim-bookworm

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tmux \
    nodejs \
    npm \
    git \
    curl \
    ca-certificates \
    less \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r omp && useradd -r -g omp -d /home/omp -s /bin/bash omp \
    && mkdir -p /devcode /home/omp \
    && chown -R omp:omp /devcode /home/omp

USER omp
WORKDIR /devcode

# Python dependencies
COPY --chown=omp:omp pyproject.toml ./
RUN pip install --no-cache-dir --user click pyyaml

# Copy workspace
COPY --chown=omp:omp . .

# Ensure bin tools are executable
RUN chmod +x bin/* || true

# Environment
ENV PATH="/devcode/bin:/home/omp/.local/bin:${PATH}"
ENV TERM=xterm-256color
ENV HOME=/home/omp
ENV WORKSPACE_ROOT=/devcode
ENV PROJECT_ROOT=/devcode
ENV ARTIFACT_REGISTRY_PATH=/devcode/milestones
ENV PYTHONPATH=/devcode

# FreeLLMAPI local gateway exposure
EXPOSE 3001

CMD ["bash", "-lc", "tmux new-session -A -s omp 'bash'"]
```

**Rationale:**
- Debian slim base for apt-installed `tmux`, `nodejs`, `npm`.
- Non-root `omp` user with home at `/home/omp`.
- `WORKSPACE_ROOT`, `PROJECT_ROOT`, and `ARTIFACT_REGISTRY_PATH` set explicitly so skills and scripts resolve paths consistently.
- `EXPOSE 3001` keeps the local FreeLLMAPI gateway accessible from the host if needed.

---

## 5. docker-compose.yml for Coolify

```yaml
name: omp-agent

services:
  omp:
    build: .
    restart: unless-stopped
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - WORKSPACE_ROOT=/devcode
      - PROJECT_ROOT=/devcode
      - ARTIFACT_REGISTRY_PATH=/devcode/milestones
      - PYTHONPATH=/devcode
      - PATH=/devcode/bin:/home/omp/.local/bin:${PATH}
      - TERM=xterm-256color
      - HOME=/home/omp
    volumes:
      - /home/<user>/devcode:/devcode:rw
      - ./.aef-env:/home/omp/.aef-env
    # If Coolify manages networking with other services, use a shared network.
    # networks:
    #   - omp-net

    # Optional: if FreeLLMAPI is deployed as a separate Coolify service,
    # reference it by service name and update .omp/config.yml api_base.
    # depends_on:
    #   - free-llm-api

    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3

# networks:
#   omp-net:
#     external: false
```

**Coolify notes:**
- Set `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in the Coolify environment variables UI.
- Mount only the specific subdirectories you need if you do not want the entire host tree inside the container.
- If you later separate FreeLLMAPI into its own Coolify service, switch `.omp/config.yml` `api_base` to the Docker network service name.

---

## 6. Transfer Steps

### Option A: Git Clone (Recommended)

```bash
mkdir -p /home/<user>/devcode
cd /home/<user>/devcode
git clone git@github.com:youruser/aef-agent.git
# Repeat for other projects...
```

### Option B: rsync from Mac

```bash
rsync -avzP \
  --exclude 'node_modules' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  ~/devcode/ <VPS_USER>@<VPS_IP>:/home/<user>/devcode/
```

**Important:** Do not copy your Mac `.venv` or local caches. Recreate them in the Linux container using the project toolchain.

---

## 7. Verification Checklist

1. Deploy the Coolify stack.
2. SSH/exec into the container:
   ```bash
   docker exec -it <container_name_or_id> bash
   ```
3. Verify workspace visibility:
   ```bash
   ls /devcode
   ```
4. Verify OMP state paths:
   ```bash
   ls /devcode/.omp /devcode/skills /devcode/milestones /devcode/sessions
   ```
5. Start tmux and run an OMP skill or CLI tool:
   ```bash
   tmux new-session -A -s omp 'bash'
   ```
6. Verify FreeLLMAPI gateway reachability from inside container:
   ```bash
   curl -sS http://localhost:3001/v1
   ```

---

## 8. Local Dependencies OMP Skills Rely On

### Interpreters / Runtimes

| Dependency | Version | Used By |
|------------|---------|---------|
| Python | 3.12 | `core/`, `skills/*`, tests |
| Node.js | 22 | `mise.toml` toolchain, `pyright`, MCP-related tooling |
| Bash | POSIX | All `.sh` scripts in `bin/` and `tests/` |
| tmux | Latest | Non-interactive headless session multiplexing |

### CLI Tools in `bin/`

| Binary | Purpose |
|--------|---------|
| `bootstrap-project` | Skill wrapper script |
| `omp` | Main OMP CLI dispatcher |
| `omp-discover` | Skill discovery |
| `omp-verify-metadata` | Metadata validation |
| `omp-verify-traceability` | Traceability checks |
| `omp-verify-git-integrity` | Git integrity |
| `omp-test` | Test runner |
| `aef-test-runner` | AEF test runner |
| `validate_metadata.py` | Metadata validation |
| `ground-truth-check.sh` | Read-only state checks |
| `resolve_artifact.py` | Artifact resolution CLI |
| `env-*` | Environment management |
| `workspace-*` | Workspace management |
| `runtime-*` | Runtime management |

### LSP / Type Checkers

| Tool | Purpose |
|------|---------|
| `pyright` | Python type checking |

### Python Libraries

| Package | Purpose |
|---------|---------|
| `click` | CLI framework |
| `PyYAML` | YAML parsing |

### Databases

| File Pattern | Purpose |
|--------------|---------|
| `code_index_*.db` | Code search indexer |

### External Services

| Service | Purpose |
|---------|---------|
| FreeLLMAPI | Local LLM gateway on port 3001 |
| MCP servers | Defined in `mcp.json`; currently empty |
