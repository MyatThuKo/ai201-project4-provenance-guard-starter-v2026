# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

The Provenance Guard service analyzes submitted writing using two independent signals and produces a reader-facing label.

1. Receive submission: A writer sends a POST /submit request containing text and creator_id.
2. Validate the request: The service checks that the required fields exist and contain valid, nonempty strings. If validation fails, it returns an appropriate error response.
3. Generate a content ID: The service generates a unique content_id to identify the submission and connect it to future appeals.
4. Analyze the text: detector.py measures the text's predictability using a local language model, while stylometry.py analyzes writing characteristics such as sentence-length variation, vocabulary diversity, and punctuation frequency.
5. Combine the signals: scoring.py::combine_signals() combines both normalized scores into one AI-likelihood score between 0 and 1.
6. Generate a label: scoring.py::score_to_label() uses the combined score and configured thresholds to select one of three labels: high-confidence human, unsure, or high-confidence AI.
7. Record and return the decision: audit.log_decision() records the results, including the two signal scores, combined score, and label. The service returns structured JSON containing the content_id, guess, confidence, label, and individual signal scores.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** The model signal measures how predictable the submitted text is to a local language model. The detector uses perplexity to measure how surprising the sequence of words is to the model. Lower perplexity means the text is more predictable. The detector converts this measurement into a normalized score between 0 and 1, where higher scores indicate stronger AI-like patterns.

**Why that might differ between human and AI writing:** AI-generated text may follow common language patterns because language models learn statistical relationships between words and sentences. Human writing may contain more unexpected word choices, unusual sentence structures, and personal experiences. However, this is only a statistical tendency and not a reliable distinction between a human and an AI authorship.

**What it can't see:** The model cannot determine who actually wrote the text. A human might write highly predictable content, such as a formal email, technical documentation, or a simple essay. This could receive a high AI-likelihood score. Similarly, AI-generated writing that uses unexpected wording or has been heavily edited may receive a low AI-likelihood score. The model also does not have access to the writer's drafting history or other evidence of authorship.

### Signal two — the style signal

**What it measures:** The stylometry signal measures the structure and statistical characteristics of writing rather than relying on a language model's assessment of predictability.

It examines three properties:

- Sentence-length spread: How much sentence length varies throughout the text.
- Type-token ratio: The number of unique words relative to the total number of words, measuring vocabulary diversity.
- Punctuation density: How frequently punctuation appears relative to the length of the text.

These measurements are combined into a normalized AI-likelihood score between 0 and 1.

**Why that might differ between human and AI writing:** Some AI-generated writing can be consistently structured, with similar sentence lengths and repeated vocabulary patterns. Human writing can have greater variation in sentence structure, word choices, and punctuation because of individual writing styles. These differences may provide additional evidence to complement the model signal although none of these properties is exclusive to either human or AI writing.

**What it can't see:** Stylometry cannot understand the meaning of the text or verify who wrote it. A human writer may intentionally use consistent sentence lengths and vocabulary, especially in formal or technical writing. An AI model can also be prompted to use varied sentence lengths, diverse vocabulary, and unusual punctuation. Stylometry may be unreliable for very short submissions because there is insufficient text to measure meaningful variation.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

---

## Design Notes

### False-Positive Scenario

A student submits a formal essay that they wrote entirely on their own. Because formal academic writing often follows predictable patterns, the model signal returns a high AI-likelihood score of 0.75. The stylometry signal also returns 0.65 because the essay uses consistent sentence lengths and structured vocabulary.

Assuming equal weighting, the combined score is 0.70. With the starter's `AI_THRESHOLD` of 0.65, the system would classify the essay as high-confidence AI, even though it was written by a human.

This is a false positive. The student sees a label suggesting their work may be AI-generated, which could unfairly damage their credibility.

The student can submit an appeal using `POST /appeal`, providing their `content_id` and an explanation. The system records the appeal and changes the submission's status to `under_review`. However, the appeal does not automatically recheck the writing or correct the original classification.

To reduce false positives, I would consider raising the AI threshold from 0.65 to 0.80, creating a wider unsure range. This reduces the chance of incorrectly labeling human writing as AI-generated, but it may also cause more genuinely AI-generated content to receive an unsure label.

The priority is to avoid making confident accusations when the evidence is insufficient.

### API Contracts

#### POST /submit

**Purpose:** Analyze submitted writing and return a prediction.

**Request fields:**

| Field        | Type   | Requirement                                                    |
| ------------ | ------ | -------------------------------------------------------------- |
| `text`       | String | Required, nonempty, maximum 10,000 characters (proposed limit) |
| `creator_id` | String | Required, nonempty                                             |

**Example request:**

```json
{
  "text": "This is my original essay.",
  "creator_id": "student_123"
}
```

**Response fields:**

| Field         | Type   | Description                               |
| ------------- | ------ | ----------------------------------------- |
| `content_id`  | String | Unique submission identifier              |
| `guess`       | String | One of `human`, `ai` and `unsure`         |
| `confidence`  | Float  | Score between 0 and 1                     |
| `label`       | String | One of three reader-facing label variants |
| `model_score` | Float  | Language model score between 0 and 1      |
| `style_score` | Float  | Stylometry score between 0 and 1          |

**Example successful response (HTTP 200):**

```json
{
  "content_id": "abc-123",
  "guess": "ai",
  "confidence": 0.85,
  "label": "This writing shows patterns commonly associated with AI-generated content, but this assessment is not proof of authorship.",
  "model_score": 0.75,
  "style_score": 0.65
}
```

**Error handling:**

- `400 Bad Request` — Missing fields, empty text, invalid JSON, or incorrect data types.
- `413 Content Too Large` — Text exceeds 10,000 characters.
- `500 Internal Server Error` — Unexpected processing failure.

Example error response:

```json
{
  "error": "text is required and must be a non-empty string"
}
```

#### POST /appeal

**Purpose:** Allow a writer to challenge a classification.

**Request fields:**

| Field        | Type   | Requirement                      |
| ------------ | ------ | -------------------------------- |
| `content_id` | String | Required, existing submission ID |
| `reasoning`  | String | Required, nonempty explanation   |

**Example request:**

```json
{
  "content_id": "abc-123",
  "reasoning": "I wrote this essay myself."
}
```

**Example successful response (HTTP 200):**

```json
{
  "content_id": "abc-123",
  "status": "under_review",
  "message": "Appeal recorded successfully."
}
```

**Error handling:**

- `400 Bad Request` — Missing or invalid fields.
- `404 Not Found` — No submission exists for the provided `content_id`.
- `500 Internal Server Error` — Unexpected processing failure.

Example error response:

```json
{
  "error": "content_id not found"
}
```

The appeal endpoint records the writer's explanation and marks the submission for review. It does not automatically rerun the AI detector.

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "text": "On a quiet Sunday afternoon, the small town of Willow Creek seemed to move at its own pace. A gentle breeze carried the scent of freshly brewed coffee through the streets, while golden leaves drifted slowly from the trees. At the corner bookstore, a young woman discovered an old journal tucked behind a row of forgotten novels. Its pages were filled with handwritten stories, mysterious sketches, and notes from someone who had lived there nearly a century earlier. What began as an ordinary afternoon soon turned into an unexpected adventure, reminding her that even the simplest moments can lead to extraordinary discoveries.",
    "creator_id": "writer_321"
  }'
```

```json
{
  "confidence": 0.6964,
  "content_id": "2bb8f5f3-e974-4686-8b50-06c4e92e0dbf",
  "guess": "unsure",
  "label": "The writing has not yet been fully evaluated.",
  "model_score": 0.6964,
  "style_score": null
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": null,
      "content_id": "65085f5f-9047-432e-bc25-1a3cfa1244b2",
      "creator_id": "writer_123",
      "guess": "unsure",
      "label": "The writing has not yet been fully evaluated.",
      "model_score": 0.6964,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T00:03:30+00:00"
    },
    {
      "combined_score": null,
      "content_id": "7e25d3f7-f3ec-4007-8871-c2ab66715a68",
      "creator_id": "writer_321",
      "guess": "unsure",
      "label": "The writing has not yet been fully evaluated.",
      "model_score": 0.7218,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T00:09:52+00:00"
    },
    {
      "combined_score": null,
      "content_id": "2bb8f5f3-e974-4686-8b50-06c4e92e0dbf",
      "creator_id": "writer_123",
      "guess": "unsure",
      "label": "The writing has not yet been fully evaluated.",
      "model_score": 0.6964,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T00:12:40+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
