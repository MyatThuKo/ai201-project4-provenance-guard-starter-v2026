# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. False-Positive Rate

<!-- Your criterion. It must name a number. -->

Of 10 pieces I wrote myself, at most 1 should be labeled high-confidence AI in each of the three evaluation trials.

**Why this target:**
False accusations can damage a writer's credibility, especially when their work is used in academic or professional settings. I want to prioritize protecting human writers over detecting every AI-generated submission. Allowing at most 1 false positive in 10 is my initial benchmark, although a real production system would require a substantially lower false-positive rate.

---

## 2. Score Separation

<!-- Your criterion. -->

The average combined AI-likelihood score of 10 AI-generated writing samples should be at least 0.35 higher than the average score of 10 human-written samples in each of the three evaluation trials.

The human samples will be writing I produced myself. The AI samples will be generated using one identified language model with the same set of general writing prompts. I will document the model and prompts before testing. I will be using the same 10 samples from Criterion #1.

**Why this target:**

The two signals should produce meaningfully different scores for AI-generated and human-written text. A difference of 0.35 is a challenging initial target for measuring separation between the two groups. However, a difference in averages does not guarantee accurate individual classifications, so I will evaluate this alongside the false-positive and label-coverage criteria.

---

## 3. Label Coverage

<!-- Your criterion. -->

Of 3 predetermined text samples submitted through `POST /submit` — one known human-written, one AI-generated, and one intentionally borderline — all 3 should produce different label variants: high-confidence human, unsure, and high-confidence AI, respectively, in each of the three evaluation trials.

The test samples must be selected before running the detector, without adjusting them based on the resulting scores.

**Why this target:**
I want to verify that the complete service can produce all three labels from actual writing, rather than only checking the threshold logic with manually selected scores. This is especially important for the unsure label, which allows the system to acknowledge uncertainty instead of forcing a confident classification.

---

## 4. Appeal Reliability

<!-- Your criterion. -->

For each evaluation trial, I will create 5 new submissions and submit one valid appeal for each existing `content_id`.

All 5 appeals must return HTTP 200 with status: "under_review" in the response and produce a corresponding appeal entry in the audit log. The submission's effective status must also be under_review.

Additionally, submitting an appeal with a nonexistent `content_id` must return HTTP 404 without adding an appeal entry to the audit log.

All 6 checks must pass in each of the three evaluation trials.

**Why this target:**
Writers need a reliable way to challenge incorrect classifications. Checking both the API response and audit log ensures that an appeal is actually recorded rather than merely acknowledged. Rejecting nonexistent content IDs also prevents invalid appeals from being stored.

---

## 5. Bad Input Handling

<!-- Your criterion. -->

All 7 invalid submission requests must return the expected HTTP error code and a JSON error message. After each invalid request, GET /health must still return HTTP 200.

The seven invalid cases are:

1. Missing text — HTTP 400
2. Empty text — HTTP 400
3. Missing creator_id — HTTP 400
4. Numeric text instead of a string — HTTP 400
5. Text exceeding 10,000 characters — HTTP 413
6. Whitespace-only text — HTTP 400
7. Invalid JSON request body — HTTP 400.

All 7 cases must pass in each of the three evaluation trials.

**Why this target:**
The service should validate incoming requests before running expensive model inference. Invalid input should produce predictable error responses without crashing the application or leaving it unresponsive. Testing the health endpoint afterward verifies that the service continues operating correctly.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
