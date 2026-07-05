# Terminal-Bench 3 Task: Fix Billing Processor Signedness Bug
[View analysis](./analize.md)

A Terminal-Bench 3 task that requires diagnosing and fixing a signed/unsigned integer
bug in a compiled C binary with no source code available.

## Task Summary

A legacy billing processor binary reads transaction records from a binary file and
computes per-customer net totals. The binary has a signedness bug: negative refund
amounts are treated as large positive charges due to use of `unsigned short` instead
of `int16_t`. The agent must patch the binary to fix the bug.

**Difficulty:** Medium-Hard
**Category:** Software Engineering / Reverse Engineering
**Expected expert time:** ~1 hour

## Results

| Run | Agent | Model | Reward |
|-----|-------|-------|--------|
| Oracle | Reference solution | — | **1.000** |
| Agent | Codex CLI | GPT-4o | **0.000** |

GPT-4o ran for 8 minutes 42 seconds, consumed 174,039 tokens, and produced no output.
See `analysis.md` for the full failure trace.

## Repository Structure

```
├── task.toml               — task config and metadata
├── instruction.md          — task prompt shown to the agent
├── analysis.md             — root-cause analysis of GPT-4o failure
├── environment/
│   ├── Dockerfile          — builds the buggy binary, generates test data
│   └── billing.c           — buggy C source (compiled + deleted in Docker)
├── solution/
│   ├── solve.sh            — oracle solution (recompiles with fix)
│   └── billing_fixed.c     — fixed source (int16_t instead of unsigned short)
├── tests/
│   ├── Dockerfile          — verifier container
│   ├── test.sh             — runs pytest, writes reward to /logs/verifier/reward.txt
│   └── test_billing.py     — 5 tests checking exact per-customer net totals
└── jobs/
    ├── 2026-07-05__21-03-16/   — Oracle run (reward 1.0)
    └── 2026-07-05__21-33-40/   — GPT-4o run (reward 0.0)
```

## Running the Task

### Prerequisites
- Docker running (Rancher Desktop, Docker Desktop, or cloud sandbox)
- [Harbor](https://harborframework.com) installed: `uv tool install harbor`

### Run Oracle (verify task is solvable)
```bash
harbor run -p . -a oracle
# Expected: reward 1.0
```

### Run GPT-4o
```bash
export OPENAI_API_KEY="sk-..."
harbor run -p . -a codex -m openai/gpt-4o
# Expected: reward 0.0
```

### Analyze failure
```bash
harbor analyze jobs/<gpt4o-job-dir>
```

## The Bug

```c
// buggy
unsigned short amount;   // zero-extends: -1500 becomes 64036
int32_t amt = amount;    // movzwl instruction

// fixed
int16_t amount;          // sign-extends: -1500 stays -1500
int32_t amt = amount;    // movswl instruction
```

Single-byte binary patch: opcode `0xB7` → `0xBF` at the `movzwl` instruction in `main()`.
