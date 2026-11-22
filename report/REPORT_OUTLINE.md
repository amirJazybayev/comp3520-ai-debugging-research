# Report layout: COMP3520_TeamXX_ResearchPaper.pdf

Suggested format: IEEE two-column conference template (Overleaf "IEEE Conference Template" or the Word version),
8 to 10 pages plus references. Every section required by the assignment brief (Section 5A) is included below.
**[N]** marks where a number comes from `results/summary.md`. **[LN-x]** marks where you need your lab-notebook entry
from stage x (see `LAB_NOTEBOOK.md`).

---

## Title
*Does Failure Context Help? An Empirical Study of LLM-Based Repair of Java Bugs from Failing JUnit Tests*

## Authors
Name 1, Name 2. COMP 3520, Thompson Rivers University. Emails.

## Abstract (150 to 200 words)
One sentence each for: the problem (developers paste failing tests into AI assistants; it is unclear what context
helps); the question; the method (15 curated single-fault Java bugs, 2 prompt conditions, visible vs hidden tests,
N repeats, model X); the headline results **[N]** (correct-repair rate per condition, overfitting, McNemar p);
the implication.

## Keywords
Automated program repair; large language models; debugging; JUnit; test overfitting; prompt context.

## 1. Introduction (about 0.75 page)
- Problem: debugging takes a large share of developer time; LLM assistants are now used to propose fixes.
- Industry relevance: developers paste failing CI output into ChatGPT/Copilot. Does the stack trace actually help,
  or is code + test enough? Cost implications (tokens) of adding context.
- Gap (short; detailed in Section 3): prior LLM-APR studies mix several context types; few isolate execution
  diagnostics on small, uncontaminated bugs with hidden tests.
- Contributions (bullet list): (1) a 15-bug benchmark with hidden tests; (2) an open, reproducible repair harness
  with CI; (3) a controlled comparison of two conditions; (4) analysis of overfitting and failure modes.

## 2. Research Question
- **RQ1**: Does adding execution diagnostics to the prompt increase the rate of *correct* repairs (visible + hidden
  tests pass) compared with code + failing test alone?
- **RQ2**: Does it change compilation rate, attempts needed, and overfitting (plausible but incorrect patches)?
- **RQ3**: For which fault categories does the diagnostic context matter (qualitative, per-bug table)?
- State hypotheses: H0 = no difference in correct-repair rate between conditions.

## 3. Background and Related Work (about 1.5 pages)
3.1 Automated program repair (APR): generate-and-validate, test suites as oracles (GenProg).
3.2 Patch overfitting / plausible vs correct patches (Qi et al. 2015; Smith et al. 2015) gives our hidden-test design.
3.3 Benchmarks: Defects4J, QuixBugs; data contamination concern motivates our self-written bugs.
3.4 LLM-based APR: Codex on QuixBugs, ChatGPT studies, conversational repair (ChatRepair), self-debugging,
    agents (SWE-bench, RepairAgent); what context they give the model.
3.5 Fault localisation and stack traces as debugging aids.
3.6 **Gap and positioning** paragraph: how this literature shaped the RQ, baseline, hidden tests and metrics.

**Table 1: Literature comparison** (required by the brief). Columns:
| Study and year | Problem addressed | Approach | Dataset / evaluation setting | Main findings | Limitations |
Fill 8 to 12 rows from the candidate list below, **only after reading each paper**.

## 4. Methodology (about 1.5 pages)
4.1 **Evaluation cases**: 15 bugs, table of id / class / fault category (from `bugs/bugs.json`); how they were
    written (Javadoc spec first, reference implementation, single-fault mutation, tests written from spec);
    validity check (`repair.experiment validate`, CI). Counts of visible vs hidden tests per bug.
4.2 **Conditions**: baseline vs diagnostics (table from README); everything else held constant (model, temperature,
    system prompt, output format, attempt budget).
4.3 **Procedure**: session = up to 3 attempts, stop when visible test passes; conditions interleaved per bug;
    R repeats; model, provider, temperature, dates **[LN-4]**.
4.4 **Measurements**: compilation rate, plausible repair, correct repair, first-attempt correctness, overfitting,
    attempts per plausible repair, patch size (changed lines), tokens and time.
4.5 **Independent ground truth**: hidden tests written from the spec before any model run; manual review of all
    plausible patches by both members independently, with disagreement resolution **[LN-6]**. Never use the LLM
    to judge its own patches.
4.6 **Statistics**: exact McNemar test on paired sessions (same bug, same repeat); report counts, not only p.

## 5. Implementation (about 1 page)
- Architecture diagram: bug manifest, prompt builder, LLM client, patch extractor, Maven/Surefire runner, JSONL log,
  analysis.
- Design decisions and why: full-class replacement instead of diffs (robust extraction); OpenAI-compatible client so
  any provider works; Surefire XML parsing; trimming stack traces to project frames; workspace copy and restore;
  fork timeout for infinite loops; stdlib-only Python.
- Quality assurance of the harness itself: unit tests with a fake LLM, integration tests with real Maven, CI on
  every push (screenshot of the green Actions run and the job summary table) **[LN-0]**.
- Repository link + final commit hash (required).

## 6. Results (about 1.5 pages)
- **Table 2**: metrics per condition (copy from `results/summary.md`) **[N]**.
- **Table 3**: correct repairs per bug and category **[N]**.
- **Figure 1**: bar chart of plausible vs correct per condition (shows overfitting gap).
- McNemar result **[N]**. Manual-review agreement and corrections **[LN-6]**.
- Report failures honestly: no-code replies, compile errors, timeouts, API errors, reruns **[LN-3, LN-4]**.

## 7. Discussion
- Answer each RQ in one paragraph.
- Interpretation: which fault categories benefited from stack traces (e.g. exceptions with line numbers) vs those
  where the test already reveals the expected value (assertion failures).
- Overfitting examples: show 1 or 2 short patches that pass the visible test but violate the spec.
- Practical implications for developers and teams (when to paste the stack trace; why to keep a second test set;
  CI integration).

## 8. Limitations and Threats to Validity
- Internal: prompt wording, single model, temperature/non-determinism (repeats mitigate), harness bugs (unit tested).
- Construct: hidden tests do not prove correctness (mitigated by manual review); "correct" is test-relative.
- External: 15 small self-written bugs, single-fault, Java only, not real-world industrial bugs.
- Conclusion validity: small sample, low statistical power; report effect sizes and counts.

## 9. Conclusion and Future Work
Summary of the answer. Future work: Defects4J/QuixBugs subset, more models, fault-localisation-only context,
agentic repair with tool use, multi-fault bugs.

## References
IEEE style, consistent. Only works you have opened and read.

## Team Contribution Statement
Table: member, contributions (benchmark, harness, experiments, analysis, writing sections). Must show both
contributed to implementation, analysis and writing.

## Disclosure of AI Use
List each tool and its role, e.g.: Claude Code (Anthropic) was used to scaffold the repository, write the benchmark
classes, the harness and its tests, and the CI workflow; all code was reviewed and run by the authors. Model X via
provider Y is the *subject* of the experiment. Any AI help with writing or literature search. State what you verified
manually.

---

## Candidate sources for the literature survey (VERIFY EVERY ONE BEFORE CITING)

These titles were suggested by an AI assistant. Find each in IEEE Xplore / ACM DL / arXiv, read it, check the
authors, year and venue, and drop any you cannot find or did not read.

| # | Candidate | Why relevant |
|---|---|---|
| 1 | Le Goues, Nguyen, Forrest, Weimer, "GenProg: A generic method for automatic software repair," IEEE TSE, 2012 | classic test-based APR |
| 2 | Qi, Long, Achour, Rinard, "An analysis of patch plausibility and correctness for generate-and-validate patch generation systems," ISSTA 2015 | plausible vs correct patches |
| 3 | Smith, Barr, Le Goues, Brun, "Is the cure worse than the disease? Overfitting in automated program repair," ESEC/FSE 2015 | overfitting, held-out tests |
| 4 | Just, Jalali, Ernst, "Defects4J: A database of existing faults to enable controlled testing studies for Java programs," ISSTA 2014 | Java bug benchmark |
| 5 | Lin, Koppel, Chen, Solar-Lezama, "QuixBugs: A multi-lingual program repair benchmark set based on the Quixey Challenge," SPLASH Companion 2017 | small-bug benchmark |
| 6 | Durieux, Madeiral, Martinez, Abreu, "Empirical review of Java program repair tools: a large-scale experiment on 2,141 bugs and 23,551 repair attempts," ESEC/FSE 2019 | Java APR evaluation |
| 7 | Gazzola, Micucci, Mariani, "Automatic software repair: A survey," IEEE TSE, 2019 | survey |
| 8 | Monperrus, "Automatic software repair: A bibliography," ACM Computing Surveys, 2018 | survey |
| 9 | Wong, Gao, Li, Abreu, Wotawa, "A survey on software fault localization," IEEE TSE, 2016 | stack traces / localisation |
| 10 | Prenner, Babii, Robbes, "Can OpenAI's Codex fix bugs? An evaluation on QuixBugs," APR Workshop (ICSE) 2022 | early LLM repair |
| 11 | Xia, Wei, Zhang, "Automated program repair in the era of large pre-trained language models," ICSE 2023 | LLM APR study |
| 12 | Jiang, Liu, Lutellier, Tan, "Impact of code language models on automated program repair," ICSE 2023 | LLM APR, Java |
| 13 | Sobania, Briesch, Hanna, Petke, "An analysis of the automatic bug fixing performance of ChatGPT," APR Workshop (ICSE) 2023 | ChatGPT + feedback |
| 14 | Xia, Zhang, "Automated program repair via conversation: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT," ISSTA 2024 | conversational repair with test feedback |
| 15 | Chen, Lin, Schärli, Zhou, "Teaching large language models to self-debug," ICLR 2024 | execution feedback |
| 16 | Jimenez et al., "SWE-bench: Can language models resolve real-world GitHub issues?," ICLR 2024 | real-world issues |
| 17 | Bouzenia, Devanbu, Pradel, "RepairAgent: An autonomous, LLM-based agent for program repair," ICSE 2025 | agentic repair |
| 18 | Parasaram et al., "The fact selection problem in LLM-based program repair," ICSE 2025 | which context facts help: closest to our RQ |
| 19 | Fan et al., "Automated repair of programs from large language models," ICSE 2023 | repairing LLM code |
| 20 | Hou et al., "Large language models for software engineering: A systematic literature review," ACM TOSEM, 2024 | broad context |
| 21 | Zhang et al., "A survey of learning-based automated program repair," ACM TOSEM, 2023 | survey |
