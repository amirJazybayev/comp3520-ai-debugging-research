# Results summary

Models: qwen/qwen3.8-27b

| Metric | baseline | diagnostics |
|---|---|---|
| Sessions | 45 | 45 |
| Total attempts | 45 | 47 |
| Compilation rate (all attempts) | 100% | 100% |
| First attempt compiles | 45/45 (100%) | 45/45 (100%) |
| Plausible repair (visible test passes) | 45/45 (100%) | 45/45 (100%) |
| Correct repair (visible + hidden pass) | 44/45 (98%) | 41/45 (91%) |
| Correct on first attempt | 44/45 (98%) | 39/45 (87%) |
| Overfitting (plausible but hidden fails) | 1/45 (2%) | 4/45 (9%) |
| Mean attempts per plausible repair | 1.00 | 1.04 |
| Mean tokens per session | 722 | 833 |
| Mean LLM time per session (s) | 11.7 | 9.9 |

## Paired comparison (correct repairs, exact McNemar test)

Both correct: 41, neither: 1, only baseline: 3, only diagnostics: 0, p = 0.2500

## Correct repairs per bug

| Bug | Category | baseline | diagnostics |
|---|---|---|---|
| b01 | boundary / relational operator | 3/3 | 3/3 |
| b02 | arithmetic / integer division | 3/3 | 2/3 |
| b03 | null handling | 2/3 | 0/3 |
| b04 | array index / wrap-around | 3/3 | 3/3 |
| b05 | missing condition | 3/3 | 3/3 |
| b06 | loop condition / off-by-one | 3/3 | 3/3 |
| b07 | missing step | 3/3 | 3/3 |
| b08 | logical operator | 3/3 | 3/3 |
| b09 | missing validation | 3/3 | 3/3 |
| b10 | operator precedence | 3/3 | 3/3 |
| b11 | API misuse (String.split) | 3/3 | 3/3 |
| b12 | algorithm direction | 3/3 | 3/3 |
| b13 | API misuse (String.split) | 3/3 | 3/3 |
| b14 | state reset | 3/3 | 3/3 |
| b15 | wrong comparison semantics | 3/3 | 3/3 |
