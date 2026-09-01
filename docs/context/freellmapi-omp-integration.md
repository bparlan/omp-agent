# FreeLLMAPI Integration Guide for OhMyPi (OMP) Framework

This document outlines the most stable and efficient methodology for integrating **FreeLLMAPI** into your OhMyPi (OMP) Agentic Engineering Framework. Because FreeLLMAPI natively implements both the **OpenAI Chat Completions API** (`/v1/chat/completions`) and the **Anthropic Messages API** (`/v1/messages`), we can bypass translation bridges (like LiteLLM) entirely, establishing direct, zero-overhead connectivity.

---

## I. Architectural Integration Architecture

FreeLLMAPI acts as a local proxy (running on `http://localhost:3001` by default) that aggregates and coordinates your free-tier keys from Google, Groq, Mistral, Cerebras, GitHub Models, etc. It handles automatic failover, per-key rate tracking, and sticky multi-turn sessions behind a single unified key.

```
       [ OMP Strategic & Tactical Layers ]
         /                             \
        / (Anthropic API Calls)         \ (OpenAI API Calls)
       ▼                                 ▼
 [ ANTHROPIC_BASE_URL ]            [ OPENAI_BASE_URL ]
  http://localhost:3001             http://localhost:3001/v1
       \                                 /
        \                               /
         ▼                             ▼
       [     FreeLLMAPI Gateway (:3001)     ]
         └── Local Encryption (AES-256-GCM)
         └── Smart Routing & Auto-Failover (429/5xx)
         └── Fallback Chains (Groq -> Cerebras -> Gemini)
       /                 |             \
      ▼                  ▼              ▼
[ Groq Free ]     [ Gemini Free ]  [ Mistral Free ]
```

---

## II. Stable Integration Steps

To establish a production-grade link that aligns with OMP's **Mechanical Tooling Stack** and project isolation barriers, follow these steps:

### Step 1: Initialize and Run FreeLLMAPI Locally
Start FreeLLMAPI using Docker Compose (recommended for persistence and isolation) or Node.js:

```bash
# Clone the repository
git clone https://github.com/tashfeenahmed/freellmapi.git
cd freellmapi

# Generate an encryption key (stable across runs)
ENCRYPTION_KEY="$(openssl rand -hex 32)"
printf "ENCRYPTION_KEY=%s\nPORT=3001\n" "$ENCRYPTION_KEY" > .env

# Start the gateway
docker compose up -d
```
*Access the dashboard at `http://localhost:3001` to add your free-tier developer keys (Gemini, Groq, Mistral, Cerebras, etc.) and copy your unified key (`freellmapi-...`).*

### Step 2: Configure Environment Variables
OMP subagents and Claude Code rely on standard SDK environment variables. Export these in your terminal or append them to your project's local `.env` file (ensure `.env` is added to your `.gitignore` to protect your keys):

```bash
# Redirect Anthropic-compatible clients (e.g., Claude Code, Claude SDK)
export ANTHROPIC_BASE_URL="http://localhost:3001"
export ANTHROPIC_API_KEY="freellmapi-your-unified-key"

# Redirect OpenAI-compatible clients (e.g., OpenAI SDK, standard LLM subagents)
export OPENAI_BASE_URL="http://localhost:3001/v1"
export OPENAI_API_KEY="freellmapi-your-unified-key"
```

### Step 3: Align OMP Configuration (`.omp/config.yml`)
To ensure that all OMP skills resolve to FreeLLMAPI natively, update your project-scoped `.omp/config.yml` configuration:

```yaml
project_id: rebalancer
mode: application

# Model Routing & Provider Configuration
model_routing:
  default_provider: freellmapi
  providers:
    freellmapi:
      api_base: "http://localhost:3001/v1"
      api_key_env: "OPENAI_API_KEY" # Reads from process.env.OPENAI_API_KEY
      default_model: "auto"         # Leverages FreeLLMAPI's smart failover chain
    anthropic_proxy:
      api_base: "http://localhost:3001"
      api_key_env: "ANTHROPIC_API_KEY"
      default_model: "claude-3-7-sonnet"

  # Skill-Specific Model Bindings
  skills:
    generate-spec: "auto"
    implement-specification: "auto"
    evaluate-implementation: "auto"
```

---

## III. The Most Efficient Prompt to Implement the Integration

To automate the implementation of this integration within your project, copy and execute the following **Spec-Driven Prompt** in OMP. This prompt is structured according to OMP's strict behavioral guidelines, ensuring that the integration is treated as a verifiable technical contract rather than a loose prompt-engineered guess.

```markdown
<USER_REQUEST>
We need to integrate FreeLLMAPI as the authoritative model-routing gateway for this project. This must be implemented via a strict, spec-driven milestone.

Please execute the milestone skill to create "Milestone M11: FreeLLMAPI Gateway Integration".

### Milestone Requirements:
1. **Provider Mapping Contract**: Initialize the OMP configuration (.omp/config.yml) to map "freellmapi" as the primary provider, routing all standard completion requests to "http://localhost:3001/v1" with "auto" as the model target to leverage multi-provider failover.
2. **Environment Contract**: Read process.env.OPENAI_API_KEY and process.env.ANTHROPIC_API_KEY to fetch the unified FreeLLMAPI token. Validate their presence at startup.
3. **Double-API Redirection**: Ensure that both Anthropic SDK clients and OpenAI SDK clients are redirected to the local port 3001 endpoints natively, bypassing external cloud relays.
4. **Fallback & Error Handling**: Implement a graceful degrade pattern—if the local FreeLLMAPI server at port 3001 is unreachable, throw a descriptive NetworkError and exit with code 1 rather than thrashing.

### Negative Guardrails:
* Do NOT hardcode the encryption key or unified token anywhere in the codebase.
* Do NOT use external translation servers; keep all proxying local.

Please present the full drafted Milestone M11 for my approval.
</USER_REQUEST>
```

---

## IV. Critical Success parameters & Best Practices

1. **Keep the Model Parameter as `"auto"`**: By passing `"model": "auto"`, FreeLLMAPI will dynamically route your query to the best available free model. If a provider throws a `429 (Rate Limit)` or `500 (Internal Server Error)`, the proxy automatically fails over to the next provider in your chain without interrupting the active OMP pipeline run.
2. **Handle rate limits with loop-awareness**: Free tiers have stricter rate limits (RPM/TPM). Ensure your OMP `MAX_AUTO_REPAIR_CYCLES` and loop cadence are adjusted (e.g., using a `/loop` cron cadence of `10m` or `15m` rather than `1m`) to prevent exhausting your provider tokens too quickly.
3. **Isolate keys on your local machine**: Always use FreeLLMAPI's local AES-256-GCM encryption. Never check the `.env` containing your provider keys or FreeLLMAPI access keys into GitHub.
