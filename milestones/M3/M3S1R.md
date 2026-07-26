# M3S1R — Remediation: Real BariaDAO Graph, Not Synthetic Pilot

## Goal

Close verified gaps in M3S1 by removing fabricated pilot artifacts, fixing schema-init bug to ensure Symbol nodes, initializing real graph against ~/devcode/BariaDAO/, integrating verification hook, and proving the gate works against actual out-of-scope edits.

## Motivation

M3S1R review (M3S1R.md) confirms the verification hook is undeployed and Symbol nodes are missing due to a schema-init bug. More critically, the "BariaDAO pilot" was built as a synthetic clone inside the AEF meta-repo (~/devcode/aef/agent/BariaDAO/) rather than against the real project (~/devcode/BariaDAO/) — none of the pilot's claimed evidence is about the actual codebase this system exists to protect.

This remediation is mandatory before V2 starts because:
1. The verification hook gate is not actually integrated into generate-verification (only documented)
2. Symbol nodes are not created by schema-init due to a bug (skippable step)
3. The graph does not exist against the real BariaDAO codebase
4. No proof exists that the gate rejects actual out-of-scope edits in real use

## Scope

**Deliverables:**

1. **Delete fabricated pilot:** Remove ~/devcode/aef/agent/BariaDAO/ entirely — no trace should remain. This includes synthetic TypeScript files and BariaDAO.lbug graph file.

2. **Fix schema-init bug:** Modify graph-context SKILL.md to ensure Symbol node creation is NOT skippable. This is a bug, not a follow-up feature. Verify by re-running init and checking Symbol nodes exist before ingestion runs.

3. **Initialize real graph:** Create ~/devcode/BariaDAO/.omp/graph/baria.lbug using the actual current skeleton.md from that repo. Populate with File, Symbol, IMPORTS edges per original V1 schema.

4. **Use Node.js client:** Replace Python-client deferment with Node.js Ladybug client (AEF's actual runtime). Scripted graph access must use correct language binding, not bash hack.

5. **Integrate verification hook:** Modify generate-verification SKILL.md to actually execute the scripted hook (not just document what it would look like). This is a code change, not "framework readiness" documentation.

6. **Real gate test:** Commit one deliberately out-of-scope edit against ~/devcode/BariaDAO/ and its real graph, prove the hook rejects it. "Framework ready" or "mechanical validation passing on synthetic data" does NOT satisfy this.

**Out of Scope:**

- CALLS/RENDERS edge extraction (still V2)
- Any project besides BariaDAO
- Any further "framework readiness" documentation in place of integration
- Modifying M3S1 acceptance status (already rejected)

## Success Criteria

1. ✅ No trace of the fabricated pilot remains in ~/devcode/aef/agent/BariaDAO/
2. ✅ ~/devcode/BariaDAO/.omp/graph/baria.lbug exists, populated from real skeleton.md
3. ✅ BariaDAO graph has Symbol nodes (not just File + IMPORTS)
4. ✅ Verification hook is an active step in generate-verification SKILL.md (not just documented)
5. ✅ Verification hook uses Node.js Ladybug client (not Python or bash-only workaround)
6. ✅ A committed, real edit to ~/devcode/BariaDAO/ is rejected by verification hook

**Acceptance:** M3S1 is NOT accepted, and V2 does NOT start, until these success criteria are independently confirmed by me against ~/devcode/BariaDAO/ (not via reading self-generated completion report).

## Risks

1. **~/devcode/BariaDAO/ skeleton.md format may differ from expectation:** If BariaDAO doesn't have a skeleton.md or format is different, init will fail. Must adapt parser to actual format rather than assuming M3S1's synthetic skeleton.md.

2. **Node.js Ladybug client may not support same features as Python client:** If Node client lacks Cypher query capabilities or has limitations, verification hook implementation may be blocked. Must verify compatibility before committing to Node stack.

3. **Real out-of-scope edit may be ambiguous in practice:** Determining what constitutes "out-of-scope" in actual BariaDAO codebase may be more complex than synthetic test case. Gate may misinterpret scope boundaries, causing false positives or missing rejections.

## Notes

- M3S1's self-reported acceptance is rejected — the review (M3S1R.md) identifies critical gaps
- Graph initialization bug in SKILL.md is the root cause of missing Symbol nodes (not a feature to defer)
- All remediation work targets ~/devcode/BariaDAO/, the actual project this system should protect
- Proof of gate effectiveness requires real edits against real codebase, not synthetic test cases
- V2 does NOT start until remediation's success criteria are independently verified against real repo
