# Lab notebook

Write an entry at the end of every stage. Date each entry. These notes become the Methodology, Results,
Limitations, Contribution and AI-disclosure sections, so record facts (numbers, links, versions), not impressions.
The tag **[LN-x]** in `REPORT_OUTLINE.md` points here.

---

## Stage 0: Repository and CI set up (done by Claude Code)
Note down:
- [ ] Repository URL, and the URL of the first green Actions run.
- [ ] Screenshot of the Actions run **Summary** page with the test tables (goes in the Implementation section).
- [ ] Tool versions: Java (`java -version`), Maven (`mvn -v`), Python (`python --version`), OS.
- [ ] AI disclosure item: "Claude Code (Claude Opus 5.5) generated the initial repository, benchmark, harness, tests
      and CI." Write down what you checked yourself.
- [ ] Who did what so far (for the contribution statement).

## Stage 1: Understand and verify the benchmark (you)
For each of the 15 bugs in `bugs/bugs.json`, open the buggy file, the reference file, and both tests. Then:
- [ ] Confirm, in your own words, what the fault is and why the visible test fails (1 line per bug).
- [ ] Check that every hidden test follows from the Javadoc, not from the reference implementation. Note any test
      you changed and why (manual correction, so report it).
- [ ] Note which bugs throw an exception (stack trace points to the line: RingBuffer, TextUtils) vs which give
      only an assertion mismatch. This is your hypothesis for RQ3.
- [ ] Record the output of `python -m repair.experiment validate` (all 15 OK).

## Stage 2: Literature survey (both)
- [ ] For each paper you read: full reference, the problem it addresses, approach, dataset, main finding, limitation.
      These are the rows of Table 1.
- [ ] Mark which candidate papers you could not find or verify, and drop them.
- [ ] Write 3 to 5 sentences on the gap your study fills (needed for Section 3.6).

## Stage 3: Pilot run (you)
Run `python -m repair.experiment run --bugs b01,b04 --repeats 1` with your chosen model.
- [ ] Provider, exact model name, date and time, temperature, and whether the API is free or paid.
- [ ] Did the replies contain a single ```java block? Any extraction failures?
- [ ] Wall-clock time per session; any rate-limit (HTTP 429) errors.
- [ ] Any change you made to prompts or code after the pilot. **Freeze the prompts after this stage**; note the
      commit hash of the frozen version.
- [ ] Delete or keep the pilot run folder? If kept, say it is a pilot and exclude it from analysis explicitly.

## Stage 4: Full experiment (you)
`python -m repair.experiment run --repeats 3 --max-attempts 3`
- [ ] Run id(s) (folder names under `results/runs/`), start and end time, total cost or token count.
- [ ] Any crash, network error or rerun, and exactly which sessions were rerun. Do not silently drop failed runs.
- [ ] Anything surprising in the console output (e.g. a bug fixed by both conditions on attempt 1 every time).
- [ ] Commit the raw results folder.

## Stage 5: Analysis (both)
`python -m repair.analyze`
- [ ] Copy Table 2 (per-condition metrics) and Table 3 (per-bug) from `results/summary.md`.
- [ ] McNemar counts and p-value.
- [ ] Which categories favoured diagnostics, which did not, and which were never fixed.
- [ ] Pick 2 interesting patches (one overfitting, one correct) for the Discussion section; note their file paths.

## Stage 6: Manual review of plausible patches (both, independently)
Open `results/manual_review.csv`. Each member fills in their own column without looking at the other's.
- [ ] For each patch: is it semantically correct against the Javadoc? Y/N, with a short reason.
- [ ] Agreement count (and Cohen's kappa if you want), how disagreements were resolved.
- [ ] Cases where the hidden tests passed but the patch is still wrong (or the reverse). These are limitations of
      the test oracle; report them.

## Stage 7: Writing (both)
- [ ] Who wrote which section (contribution statement).
- [ ] Every AI tool used for writing or literature search, and for what (AI disclosure).
- [ ] Re-check every reference against the original paper.

## Stage 8: Submission
- [ ] Final commit hash: `git rev-parse HEAD`. Put it and the clickable repo link in the paper.
- [ ] Make sure the instructor can open the repository (public, or add them as a collaborator).
- [ ] ZIP of that commit, without credentials: `git archive -o COMP3520_TeamXX_Implementation.zip HEAD`.
- [ ] Confirm the CI run for the final commit is green; screenshot.
