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

**The rule:**

I use a weighted average to combine the model signal and stylometry signal into one AI-likelihood score between 0 and 1. I give stylometry a higher weight because my initial testing showed that GPT-2 can assign relatively high AI-likelihood scores to human-written text.

When the two signals disagree by more than 0.30, I cap the combined score at 0.60. This prevents a high-confidence AI label when the signals strongly disagree, reducing the risk of falsely accusing a human writer. However, this may also cause some AI-generated writing to receive an unsure label.

**The numbers:**

- Model signal weight: `0.40` (40%)
- Stylometry signal weight: `0.60` (60%)
- Formula: `combined_score = 0.4 * model_score + 0.6 * style_score`
- Disagreement threshold: `0.30`
- Disagreement cap: `0.60`
- Current AI threshold: `0.65`

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

I submitted a paragraph I wrote myself about my education and software engineering experience.

- Model signal: `0.7206`
- Stylometry signal: `0.4638`
- Difference: `0.2568`
- Combined score: `0.5665`

The model signal assigned relatively strong AI-like characteristics to my writing, while the stylometry signal returned a lower score.

Using my weighted average:

`0.4 * 0.7206 + 0.6 * 0.4638 = 0.5665`

Since the difference between the signals was below 0.30, the disagreement cap was not triggered.

The combined score falls within my current unsure range of 0.35–0.65. This demonstrates how combining both signals reduces the likelihood of making a confident AI accusation based solely on the model's prediction.

Although this example demonstrates a difference between the signals, it does not test the disagreement cap itself. The scoring weights and thresholds remain heuristic choices that will need further evaluation.

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
  "confidence": 0.69,
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

**High-confidence human — 0.00 to 0.35 (inclusive)**

"This writing appears to have been written by a person, although its origin cannot be verified automatically."

**Unsure — above 0.35 and below 0.65**

"We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct."

**High-confidence AI — 0.65 to 1.00 (inclusive)**

"This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect."

| Label                 | Score range           | The exact text a reader sees                                                                                                                                 |
| --------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| high-confidence human | `0.00 ≤ score ≤ 0.35` | This writing appears to have been written by a person, although its origin cannot be verified automatically.                                                 |
| unsure                | `0.35 < score < 0.65` | We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct. |
| high-confidence AI    | `0.65 ≤ score ≤ 1.00` | This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.                           |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I worded the unsure label to acknowledge that the system cannot reliably determine who wrote the content without implying that the writer did anything wrong. My experiments showed that even human-written text can receive relatively high AI-likelihood scores. I included the statement about misconduct because an uncertain prediction should not be treated as evidence of cheating or dishonesty.

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
  "confidence": 0.7336,
  "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
  "guess": "ai",
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "model_score": 0.7218,
  "style_score": 0.7415
}
```

```bash
$ curl -i -X POST "http://127.0.0.1:5000/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Mr. Bennet was so odd a mixture of quick parts, sarcastic humour, reserve, and caprice, that the experience of three-and-twenty years had been insufficient to make his wife understand his character. Her mind was less difficult to develop. She was a woman of mean understanding, little information, and uncertain temper. When she was discontented, she fancied herself nervous. The business of her life was to get her daughters married; its solace was visiting and news.",
    "creator_id": "Jane_Austen"
  }'
```

```json
{
  "confidence": 0.2856,
  "content_id": "1ee14c59-db82-4b9b-8a81-17ace5caf08f",
  "guess": "human",
  "label": "This writing appears to have been written by a person, although its origin cannot be verified automatically.",
  "model_score": 0.4585,
  "style_score": 0.1703
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
    "reasoning": "I wrote this myself and would like it reviewed."
  }'
```

```json
{
  "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
  "message": "Your appeal has been recorded.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=10"
```

```json
{
  "count": 10,
  "entries": [
    {
      "combined_score": 0.5412,
      "content_id": "9cf72ea2-a057-4de8-99fb-685c81b71cde",
      "creator_id": "writer_123",
      "guess": "unsure",
      "label": "The writing has not yet been fully evaluated.",
      "model_score": 0.6981,
      "status": "decided",
      "style_score": 0.4366,
      "timestamp": "2026-11-02T00:20:21+00:00"
    },
    {
      "combined_score": 0.5665,
      "content_id": "1c9aa50d-6aab-4402-9a79-ef0c0ae4c417",
      "creator_id": "milestone4_test",
      "guess": "unsure",
      "label": "The writing has not yet been fully evaluated.",
      "model_score": 0.7206,
      "status": "decided",
      "style_score": 0.4638,
      "timestamp": "2026-11-02T00:36:13+00:00"
    },
    {
      "content_id": "1c9aa50d-6aab-4402-9a79-ef0c0ae4c417",
      "creator_id": "milestone4_test",
      "event": "appeal",
      "reasoning": "I wrote this content myself and would like to request a review.",
      "status": "under_review",
      "timestamp": "2026-11-02T00:53:21+00:00"
    },
    {
      "content_id": "1c9aa50d-6aab-4402-9a79-ef0c0ae4c417",
      "creator_id": "milestone4_test",
      "event": "appeal",
      "reasoning": "I wrote this content myself and would like to request a review.",
      "status": "under_review",
      "timestamp": "2026-11-02T00:54:01+00:00"
    },
    {
      "content_id": "1c9aa50d-6aab-4402-9a79-ef0c0ae4c417",
      "creator_id": "milestone4_test",
      "event": "appeal",
      "reasoning": "I wrote this content myself and would like to request a review.",
      "status": "under_review",
      "timestamp": "2026-11-02T00:56:22+00:00"
    },
    {
      "combined_score": 0.7336,
      "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
      "creator_id": "writer_321",
      "guess": "ai",
      "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
      "model_score": 0.7218,
      "status": "decided",
      "style_score": 0.7415,
      "timestamp": "2026-11-02T01:00:20+00:00"
    },
    {
      "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
      "creator_id": "writer_321",
      "event": "appeal",
      "reasoning": "I wrote this myself and would like it reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-02T01:45:10+00:00"
    },
    {
      "combined_score": 0.6398,
      "content_id": "8d3aaa5f-d7f5-4f06-965f-855b7cd72a25",
      "creator_id": "self-writing",
      "guess": "unsure",
      "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
      "model_score": 0.6964,
      "status": "decided",
      "style_score": 0.602,
      "timestamp": "2026-11-02T01:46:27+00:00"
    },
    {
      "combined_score": 0.2856,
      "content_id": "1ee14c59-db82-4b9b-8a81-17ace5caf08f",
      "creator_id": "Jane_Austen",
      "guess": "human",
      "label": "This writing appears to have been written by a person, although its origin cannot be verified automatically.",
      "model_score": 0.4585,
      "status": "decided",
      "style_score": 0.1703,
      "timestamp": "2026-11-02T01:47:48+00:00"
    },
    {
      "content_id": "73244e70-6ba2-40bd-be29-eea9c83018a2",
      "creator_id": "writer_321",
      "event": "appeal",
      "reasoning": "I disagree with this classification and would like to request a review.",
      "status": "under_review",
      "timestamp": "2026-11-02T01:57:47+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- _What I asked for:_ I asked Claude to check whether I have added all the implementation and examples needed inside README.md for Unit 7.
- _What came back:_ Claude pointed out that I do not currently have evidence that all three labels can be reached and that I am missing "human" label.
- _What I changed:_ I searched online and took a paragraph from `Pride and Prejudice, Chapter 1 — Jane Austen (1813)` to test whether my implementation is correctly identifying the texts written by a human.

**Moment 2 — Implementing and Refining Stylometry (Unit 7)**

- _What I asked for:_ I asked Claude to help implement the initial `stylometry.py` and the combining rule for my two detection signals.
- _What came back:_ Claude provided an implementation with three stylometry measurements: sentence-length spread, vocabulary variety, and punctuation density. It also included a weighted scoring rule to combine these measurements into a single style signal.
- _What I changed:_ After reviewing the implementation, I refined `punctuation_density()` to avoid counting apostrophes in contractions and hyphens within compound words as separate punctuation marks. I also improved how `style_signal()` handles submissions with fewer than two usable sentences and tested the measurements against my own writing samples. Claude later confirmed the behavior of my refinements.

**Moment 3 — Selecting and Measuring an Improvement (Unit 8)**

- _What I asked for:_ I asked Claude to analyze my evaluation results and compare possible improvements to the detector, including changing the AI classification threshold and reweighting the stylometry signal.
- _What came back:_ Claude simulated several alternatives using my existing evaluation samples. One option suggested increasing the AI threshold from 0.65 to 0.70, while another suggested changing the stylometry weights to 30% sentence-length spread and 70% vocabulary variety. The simulation indicated that reweighting the style signal could improve score separation and AI detection while reducing false positives.
- _What I changed:_ I initially tested the higher AI threshold, but it reduced AI detection from 4/10 to 1/10. I then restored the original threshold and selected the stylometry reweighting as my final improvement. After rerunning the full attack set and acceptance criteria, the score separation improved from 0.1133 to 0.2676, AI detection increased from 4/10 to 6/10, and false-positive classifications of my own writing decreased from 1/10 to 0/10. I documented that Criterion 2 still missed its target and that the new weights could be overfitted to my evaluation samples.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

I chose 10 submissions per minute because a legitimate writer may need to submit or revise their writing multiple times, but 10 requests provides enough room for normal usage without allowing unlimited rapid submissions.

I chose 200 submissions per day as an additional safeguard against automated scripts repeatedly probing the detector. These limits are initial design choices and would need further evaluation using real traffic patterns.

**What a caller counts as:** The rate limiter identifies callers using `creator_id` when a valid identifier is provided. If `creator_id` is missing or invalid, it falls back to the requester's IP address. This is not a secure identity mechanism because someone could use multiple creator IDs to bypass the limit. However, it is sufficient for testing basic rate-limiting behavior in this project.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 200
  [10/15] 200
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
============================================================

5 of 15 were rate limited.
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-08T22:03:15+00:00", "content_id": "9a81a41d-0870-463d-a1e9-83f5852a7655", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.5702, "combined_score": 0.6642, "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:15+00:00", "content_id": "ab0a4c7b-9428-4202-9680-b95f3e7d8d5a", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.7387, "style_score": 0.5562, "combined_score": 0.6292, "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:14+00:00", "content_id": "119c55df-695e-4571-936a-62579847b514", "creator_id": "attacker_EV05", "guess": "human","model_score": 0.3212, "style_score": 0.3503, "combined_score": 0.3387, "label": "This writing appears to have been written by a person, althoughits origin cannot be verified automatically.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:15+00:00", "content_id": "52c0bd85-7469-403d-b27e-4d80e2f3cdb1", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.5659, "combined_score": 0.6212, "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:14+00:00", "content_id": "6557f81b-a8bb-4caa-a032-0a47a1fae681", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.8305, "combined_score": 0.5637, "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:16+00:00", "content_id": "59a0c2e3-7b0c-4976-a3d2-9b3c1b8ecb29", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.75, "combined_score": 0.849, "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:16+00:00", "content_id": "28ebe35f-0907-45ff-8972-b4638b9ae4f6", "creator_id": "attacker_MF04", "guess": "human","model_score": 0.0112, "style_score": 0.45, "combined_score": 0.2745, "label": "This writing appears to have been written by a person, although its origin cannot be verified automatically.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:16+00:00", "content_id": "57d5106a-7680-47ac-9fa6-4caf728dfcc8", "creator_id": "attacker_MF03", "guess": "unsure", "model_score": 0.0, "style_score": 0.75, "combined_score": 0.45, "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.", "status": "decided"}
{"timestamp": "2026-11-08T22:03:16+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
{"timestamp": "2026-11-08T22:03:16+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_json", "limit":"none"}
```

**The single worst outcome** — The worst outcome was **FP03**, which contained carefully written human text from a non-native English speaker. My system classified it as AI-generated with a combined score of **0.6642**, above the 0.65 AI threshold. This is the outcome I would least want to explain to a writer because someone who wrote their own work could be incorrectly accused of using AI, potentially affecting their credibility.

**Full attack results:**

See [Baseline Attack Results](results/attack_run_2026-11-08_1703.md)
for all 56 attacks, their responses, and HELD/BROKE verdicts.

**Attack results by family**

| Attack family      |  Total |   HELD |  BROKE |
| ------------------ | -----: | -----: | -----: |
| Evasion            |     10 |      1 |      9 |
| False positive     |      8 |      7 |      1 |
| Prompt injection   |      6 |      6 |      0 |
| Malformed requests |     20 |     18 |      2 |
| Same-creator flood |     12 |     12 |      0 |
| **Total**          | **56** | **44** | **12** |

These results use an evasion definition where AI-generated writing receiving `human` or `unsure` counts as a successful evasion. Malformed inputs receiving `unsure` count as safely handled, while nonsensical inputs receiving confident human or AI labels count as failures. The prompt-injection totals assume the response labels and audit records were not manipulated.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion             | Target                       | Run 1  | Run 2  | Run 3  | Verdict |
| --------------------- | ---------------------------- | ------ | ------ | ------ | ------- |
| 1. False positives    | At most 1/10                 | 1/10   | 1/10   | 1/10   | MET     |
| 2. Score separation   | AI mean >= human mean + 0.35 | 0.1133 | 0.1133 | 0.1133 | MISSED  |
| 3. Label coverage     | 3 distinct labels            | 3/3    | 3/3    | 3/3    | MET     |
| 4. Appeal reliability | 6/6 checks                   | 6/6    | 6/6    | 6/6    | MET     |
| 5. Bad-input handling | 7/7 checks                   | 7/7    | 7/7    | 7/7    | MET     |

All three trials produced identical results for every criterion. This was expected because both the model signal and stylometry calculations are deterministic for the same input.

Criterion 4 and the seventh case of Criterion 5 were tested using my additional script, `run_extra_checks.py`, because the standard `run_eval.py` scenario format does not support the appeal workflow or sending unparseable JSON directly.

The Criterion 3 samples were selected during Unit 7 and were not modified for this evaluation.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

**Run Log Before**

### Criterion 1 — False positives

Source: results/run_2026-11-08_1854_before.md, produced by run_eval.py::main, trial 1, scenario my own writing.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.577,
    "model_score": 0.5795,
    "style_score": 0.5753,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "I am a computer science graduate, currently working as an iOS engineer"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5916,
    "model_score": 0.7528,
    "style_score": 0.4841,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Apple Magic Keyboard is a wireless keyboard that allows a user to conn"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5103,
    "model_score": 0.7079,
    "style_score": 0.3785,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "A lot of New Yorkers love to go shopping at the Whole Foods Market. Th"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6916,
    "model_score": 0.8482,
    "style_score": 0.5872,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "With advanced technologies, people are now starting to use contactless"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5222,
    "model_score": 0.5752,
    "style_score": 0.4868,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "The use of digital wallets or mobile wallets starts in 2011 where Goog"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4152,
    "model_score": 0.6441,
    "style_score": 0.2626,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "In order to have a more streamlined and user-friendly customer experie"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4515,
    "model_score": 0.3673,
    "style_score": 0.5077,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "This feature functions much like the shopping list from the legacy Who"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3729,
    "model_score": 0.4707,
    "style_score": 0.3077,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Year 1 represents the greatest incurred cost as this contains the cost"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4868,
    "model_score": 0.5355,
    "style_score": 0.4543,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "The magnetic connection between the iPad and the Magic Keyboard plays "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5876,
    "model_score": 0.6929,
    "style_score": 0.5174,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "The most realistic way to improve the usage of the contactless payment"
  }
]
```

### Criterion 2 — Score separation

Source: results/run_2026-11-08_1854_before.md, produced by run_eval.py::main, trial 1, scenarios my own writing and AI samples.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6536,
    "model_score": 0.7376,
    "style_score": 0.5976,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "A consistent morning routine can set the tone for the entire day. Star"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6147,
    "model_score": 0.6344,
    "style_score": 0.6015,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Reading offers benefits that extend far beyond entertainment. It stren"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.603,
    "model_score": 0.6022,
    "style_score": 0.6035,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Learning a new language is a challenging but deeply rewarding experien"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7163,
    "model_score": 0.8647,
    "style_score": 0.6174,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "Regular exercise is one of the most effective ways to improve both phy"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6404,
    "model_score": 0.7628,
    "style_score": 0.5588,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Social media has transformed the way people communicate, share informa"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5951,
    "model_score": 0.6815,
    "style_score": 0.5375,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "There is something quietly comforting about a rainy day. The steady rh"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6786,
    "model_score": 0.7512,
    "style_score": 0.6302,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "Volunteering is a powerful way to make a positive difference in the co"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6,
    "model_score": 0.8373,
    "style_score": 0.5364,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Cities play a central role in the fight against climate change. Becaus"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6658,
    "model_score": 0.8005,
    "style_score": 0.576,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "The first day at a new job is often a mix of excitement and nervousnes"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5719,
    "model_score": 0.7471,
    "style_score": 0.4551,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Technology has reshaped education in profound ways. Online platforms, "
  }
]
```

**Average combined scores:**

- Human-written samples: `0.5207`
- AI-generated samples: `0.6339`
- Score separation: `0.6339 - 0.5207 = 0.1133`
- Required separation: `0.35`

**Verdict: MISSED.** The difference between the groups was substantially smaller than my original target.

### Criterion 3 — Label coverage

Source: results/run_2026-11-08_1854_before.md, produced by run_eval.py::main, trial 1, scenario label coverage.

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2856,
    "model_score": 0.4585,
    "style_score": 0.1703,
    "label": "This writing appears to have been written by a person, although its origin cannot be verified automatically.",
    "sent": "Mr. Bennet was so odd a mixture of quick parts, sarcastic humour, rese"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5768,
    "model_score": 0.7626,
    "style_score": 0.453,
    "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
    "sent": "Remote work has changed how lots of people think about their jobs. Man"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7336,
    "model_score": 0.7218,
    "style_score": 0.7415,
    "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
    "sent": "On a quiet Sunday afternoon, the small town of Willow Creek seemed to "
  }
]
```

### Criterion 4 — Appeal reliability

Source: results/extra_checks_2026-11-08_1854_before.md, produced by run_extra_checks.py::main, trial 1.

```json
"appeals": [
    {
      "check": "appeal 1",
      "content_id": "a1abd3b2-1f10-40dd-b309-ce162ebbfe28",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "fe54a035-e1ba-44e0-afb4-72edaa225fe2",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "ca904363-61f8-49f5-8452-47c4a3ad5de1",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "e9c60d81-8136-4043-91a2-d35000cda690",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "1b05ef00-a25e-4315-a8c0-0a448af52134",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "e13695fb-349a-4fca-b999-b1707d0b5a14",
      "appeal_status_code": 404,
      "appeal_in_log": false,
      "passed": true
    }
  ]
```

### Criterion 5 — Bad-input handling

Source: results/extra_checks_2026-11-08_1854_before.md, produced by run_extra_checks.py::main, trial 1.

```json
"bad_input": [
    {
      "check": "missing text",
      "expected": 400,
      "status": 400,
      "json_error": "text must be a non-empty string.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "empty text",
      "expected": 400,
      "status": 400,
      "json_error": "text must be a non-empty string.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "missing creator_id",
      "expected": 400,
      "status": 400,
      "json_error": "creator_id must be a non-empty string.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "numeric text",
      "expected": 400,
      "status": 400,
      "json_error": "text must be a non-empty string.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "text over 10,000 chars",
      "expected": 413,
      "status": 413,
      "json_error": "text exceeds 10000 characters.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "whitespace-only text",
      "expected": 400,
      "status": 400,
      "json_error": "text must be a non-empty string.",
      "health_after": 200,
      "passed": true
    },
    {
      "check": "unparseable JSON",
      "expected": 400,
      "status": 400,
      "json_error": "A valid JSON object is required.",
      "health_after": 200,
      "passed": true
    }
  ]
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

### Criterion 2 — Score separation (MISSED)

**Stage:** Signal one, signal two, and the combining rule.

**Mechanism:** My detector did not sufficiently separate human-written and AI-generated writing. The average combined score for human writing was 0.5207, while AI-generated writing averaged 0.6339, giving a difference of only 0.1133 against my required 0.35.

Although the AI samples generally received higher scores, many human samples also had relatively high model scores. My combining rule uses 40% model signal and 60% stylometry signal, but the two signals still produced overlapping scores for these samples. This suggests that the statistical characteristics I measure are not distinctive enough to reliably determine authorship.

### Evasion attacks — 9 BROKE

**Stage:** Model signal, stylometry signal, and combining rule.

**Mechanism:** Nine of the ten evasion attacks avoided the high-confidence AI label. These attacks changed the structure or wording of AI-origin content, producing scores that fell below the AI threshold of 0.65.

The attacks exposed several different weaknesses:

- **EV01:** The model signal was very low (0.1635), while the style signal was high (0.8305). The resulting combined score was 0.5637, producing `unsure`. The unusually low model score prevented the high style score from producing an AI label.
- **EV02, EV03, EV06, and EV07:** Changes involving sentence structure, quotations, and punctuation resulted in combined scores within the unsure range. These modifications altered the statistical features that my detector uses.
- **EV05:** A heavy human-editing pass produced low scores from both signals (0.3212 and 0.3503), giving a combined score of 0.3387 and a `human` label.
- **EV08:** The model signal returned a low score of 0.2452, while the stylometry signal returned a high score of 0.8025. Their disagreement of 0.5573 exceeded my disagreement threshold of 0.30. However, the weighted average was already 0.5796, below the disagreement cap of 0.60, so applying the cap did not change the result. The low model score pulled the combined score into the unsure range, allowing the AI-origin text to avoid a high-confidence AI classification.
- **EV09:** Combining AI-origin text with a human-style introduction produced a combined score of 0.6212, below the AI threshold.
- **EV10:** The model score was 0.9792, but the style score was only 0.4206. Because the difference exceeded 0.30, my disagreement cap reduced the final score to 0.60, resulting in `unsure`.

These results demonstrate that an attacker can change the form of AI-generated writing to avoid a confident AI classification. My disagreement cap also creates a tradeoff: it reduces the risk of false accusations but can make evasion easier.

### FP03 — Human writing falsely labeled AI

**Stage:** Model signal and label mapping.

**Mechanism:** FP03 contained carefully written human text from a non-native English speaker. The model signal returned 0.8051, while stylometry returned 0.5702. Their weighted average was 0.6642.

The difference between the signals was approximately 0.2349, below my disagreement threshold of 0.30, so the cap did not activate. Because the combined score exceeded the AI threshold of 0.65, the system returned a high-confidence AI label.

This is particularly concerning because the detector treated writing characteristics as evidence of AI authorship even though the text was human-written.

### MF04 — Punctuation-only input classified as human

**Stage:** Route validation and signal processing.

**Mechanism:** My route checks whether the submitted text is a nonempty string, but it does not require meaningful words or sentences. As a result, punctuation-only input passed validation and was evaluated by the detector.

The model signal returned 0.0112, and the style signal returned 0.45. The combined score was 0.2745, causing the system to label the input as human-written even though it contained no meaningful writing.

### MF05 — A single long word classified as AI

**Stage:** Route validation and model signal.

**Mechanism:** The route accepted a single extremely long word as valid text. The model signal returned 0.9976, while the style signal returned 0.75. Their combined score was 0.8490, producing a high-confidence AI label.

This demonstrates that my system can make confident authorship predictions for inputs that do not contain enough meaningful language to support such a conclusion.

### Overall pattern

The most common problem is that my detector relies on statistical writing characteristics rather than actual evidence of authorship. Human and AI writing can have overlapping scores, while changes in wording, sentence structure, and punctuation can influence the signals.

My disagreement cap helps protect genuine writers from false accusations, but it also contributes to missed AI detections. The malformed-input failures reveal another weakness: my validation checks the type and length of submitted text without verifying that it contains meaningful language.

These failures suggest that the system needs better handling of unreliable input and greater caution before returning confident authorship labels.

### Criteria that met their targets

**Criterion 1 — MET:** Only one of my ten human-written samples received an AI label in each trial, meeting my maximum of one false positive per ten samples. However, most other samples received `unsure` rather than `human`.

**Criterion 3 — MET:** All three predetermined samples received distinct labels (`human`, `unsure`, and `ai`) in all three trials.

**Criterion 4 — MET:** All five valid appeals returned HTTP 200 with `under_review` and appeared in the audit log. The nonexistent content ID returned HTTP 404 without creating an appeal entry in all three trials.

**Criterion 5 — MET:** All seven malformed-input cases returned their expected HTTP error codes, and the health endpoint continued returning HTTP 200 afterward in every trial.

---

## The Improvement

**What I changed:**

I reweighted the stylometry signal in `stylometry.py::style_signal` from 50% sentence-length spread, 30% vocabulary variety, and 20% punctuation density to 30% sentence-length spread and 70% vocabulary variety.

```python
score = 0.3 * spread_ai + 0.7 * ttr_ai
```

For my final measured comparison, I kept the original AI threshold at 0.65 and made no other changes to the scoring pipeline.

**Which diagnosis pointed at it:**

My Criterion 2 diagnosis showed that human and AI writing received overlapping combined scores. My exploratory measurements suggested vocabulary variety separated the two groups more effectively than sentence-length variation, while punctuation density was not useful for this sample set. I therefore increased the contribution of vocabulary variety.

**Measured before and after:**

| Metric                            | Before |  After |
| --------------------------------- | -----: | -----: |
| Human mean score                  | 0.5207 | 0.4149 |
| AI mean score                     | 0.6339 | 0.6825 |
| Score separation                  | 0.1133 | 0.2676 |
| Human samples flagged AI          |   1/10 |   0/10 |
| AI samples flagged AI             |   4/10 |   6/10 |
| Evasion attacks detected          |   1/10 |   3/10 |
| False-positive attacks flagged AI |    1/8 |    0/8 |
| Total attacks HELD                |  44/56 |  47/56 |

### Attack Run — After

From `results/attack_run_2026-11-08_2038_after.md`, produced by `run_attacks.py::main`, compared with the before run in `results/attack_run_2026-11-08_1703.md`.

| Attack family      | Total | Before HELD | Before BROKE | After HELD | After BROKE |
| ------------------ | ----: | ----------: | -----------: | ---------: | ----------: |
| Evasion            |    10 |           1 |            9 |          3 |           7 |
| False positive     |     8 |           7 |            1 |          8 |           0 |
| Prompt injection   |     6 |           6 |            0 |          6 |           0 |
| Malformed requests |    20 |          18 |            2 |         18 |           2 |
| Same-creator flood |    12 |          12 |            0 |         12 |           0 |
| **Total**          |    56 |      **44** |       **12** |     **47** |       **9** |

Attacks whose outcome changed:

| Attack | Before         | After          |
| ------ | -------------- | -------------- |
| EV03   | unsure (0.601) | ai (0.745)     |
| EV05   | human (0.339)  | unsure (0.396) |
| EV09   | unsure (0.621) | ai (0.733)     |
| FP03   | ai (0.664)     | unsure (0.564) |
| PI03   | unsure (0.602) | ai (0.693)     |
| PI05   | unsure (0.544) | ai (0.740)     |

**Did it help, and how do I know:**

Yes. The difference between the mean AI and human scores increased from 0.1133 to 0.2676, and correctly identified AI samples increased from four to six. The FP03 false-positive attack also changed from `ai` to `unsure`, reducing the number of false-positive attacks from one to zero.

However, the score-separation criterion remains MISSED because 0.2676 is still below my original target of 0.35.

These weights were selected using the same writing samples used for evaluation, so the improvement may be partly due to overfitting. Performance on previously unseen writing has not been established.

I also explored raising the AI threshold to 0.70 as an alternative, but that reduced the number of detected AI samples to one out of ten. I selected the stylometry reweighting as the final improvement because it improved both score separation and AI detection on my test set.

After the changes, criterion 5 switched from `MET` to `MISSED`. This wasn't caused by reweighting, which only changes scores. Running all three scripts back to back hit the rate limiter for requests without a `creator_id`. As you can see in [extra_checks_2026-11-08_2106_after.md](results/extra_checks_2026-11-08_2106_after.md), which was run after some time and all three runs for the criterion 5 resulted in `MET`. However I decided to put the initial run the table under for the criterion 5 as `MISSED`.

**Run Log After**

| Criterion             | Target                       | Run 1  | Run 2  | Run 3  | Verdict |
| --------------------- | ---------------------------- | ------ | ------ | ------ | ------- |
| 1. False positives    | At most 1/10                 | 0/10   | 0/10   | 0/10   | MET     |
| 2. Score separation   | AI mean >= human mean + 0.35 | 0.2676 | 0.2676 | 0.2676 | MISSED  |
| 3. Label coverage     | 3 distinct labels            | 3/3    | 3/3    | 3/3    | MET     |
| 4. Appeal reliability | 6/6 checks                   | 6/6    | 6/6    | 6/6    | MET     |
| 5. Bad-input handling | 7/7 checks                   | 5/7    | 5/7    | 5/7    | MISSED  |

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

My improvement increased the average score separation between AI-generated and human-written text from 0.1133 to 0.2676, reduced false-positive classifications, and increased the number of detected evasion attacks from one to three. However, several weaknesses remain.

### 1. Seven evasion attacks still succeeded

**Affected attacks:** EV01, EV02, EV05, EV06, EV07, EV08, and EV10.

These inputs still avoided the high-confidence AI label. Their weaknesses involve several different stages of my detection pipeline:

- **EV01 and EV08:** Both attacks produced very low model scores (0.1635 and 0.2452), despite relatively high stylometry scores. Their uncapped weighted averages were approximately 0.612 and 0.627, respectively, already below the AI threshold of 0.65. Although the disagreement cap reduced both scores to 0.60, it did not cause their unsure classifications. The primary weakness was the low model signal pulling down the combined score.
- **EV02 and EV06:** Sentence-length changes affected the stylometry signal, keeping the combined scores below the AI threshold.
- **EV05:** Heavily edited AI-origin writing still received an unsure classification, even though the new weights improved its score.
- **EV07:** The punctuation-padding attack continued to receive an unsure label. After my improvement, punctuation density no longer contributes directly to the style signal. The model score was 0.5862 and the style score was 0.4839, producing a combined score of 0.5248. Both signals remained below the level needed for a confident AI classification, so the attack continued to evade detection. Punctuation could still indirectly affect other measurements, but the removed punctuation-density measure was not responsible for this result.
- **EV10:** This attack demonstrates a new weakness introduced by my improvement. The repeated stanza structure uses repeated vocabulary, which reduces the vocabulary-diversity measurement. Because vocabulary variety now contributes 70% of the stylometry signal, EV10's style score decreased from 0.4206 to 0.1324.

The model score remained high at 0.9792, but the final weighted score fell to 0.4711, resulting in unsure. The disagreement cap did not reduce this score because the uncapped average was already below 0.60.

Although EV10 was classified as unsure before and after the improvement, the new weighting made the attack more effective by moving its combined score farther from the AI threshold.

**What I would fix next:** I would evaluate the detector against a broader collection of adversarially edited text and reconsider how the two signals handle extreme disagreement. I would also test additional features that are less sensitive to superficial formatting changes.

**Why I stopped:** My assignment required one isolated, measurable improvement. Changing the model signal or disagreement rule would introduce additional variables and make it harder to attribute the observed improvement to the stylometry reweighting.

### 2. Malformed inputs still receive confident labels

**Affected attacks:** MF04 and MF05.

MF04, containing only punctuation, received a `human` classification with a combined score of 0.0945. MF05, containing an unusually long single word, received an `ai` classification with a score of 0.9090.

**Stage:** Route validation.

**Mechanism:** My validation checks that the input is a nonempty string within the length limit, but it does not adequately verify that the text contains meaningful language suitable for authorship analysis.

**What I would fix next:** Add validation for minimum usable word count and sufficient meaningful language before running the detector.

**Why I stopped:** Input validation is a separate issue from the scoring improvement I selected. I would evaluate it as another independent change.

### 3. Criterion 2 still misses its target

**Original target:** AI-generated writing must have an average combined score at least 0.35 higher than human writing.

**Measured improvement:** 0.1133 before → 0.2676 after.

Although the separation improved substantially, it remains below my required target.

**What I would fix next:** Test on an independent dataset and investigate additional signals that can distinguish AI-generated writing from human writing more reliably.

**Why I stopped:** I selected my new weights using the same evaluation samples, which introduces overfitting risk. Further tuning on those samples would make the evaluation less trustworthy.

### 4. Rate limiting interferes with validation errors

**Affected criterion:** Criterion 5.

The first after-run returned 5/7 successful checks because requests missing a usable `creator_id` shared an IP-based rate-limit bucket. Two requests received HTTP 429 instead of the expected HTTP 400.

A later isolated rerun returned 7/7 in all three trials without code changes, supporting the conclusion that the failure depended on rate-limit state.

**What I would fix next:** Investigate how the limiter identifies requests with missing or invalid creator IDs and how validation errors should interact with rate limiting.

**Why I stopped:** Changing the limiter would introduce a second implementation improvement unrelated to stylometry. I preserved both results rather than hiding the original failure.

### 5. Limitations of the new style weights

The style signal now depends 70% on vocabulary variety. This may create a new evasion opportunity: an attacker could deliberately repeat common words to reduce the vocabulary-variety score.

Very short texts may also have artificially high vocabulary variety because nearly every word is unique.

My current results use the same texts that helped me choose the weights, so the measured improvement may overestimate performance on unseen writing.

Before using this system in a real setting, I would evaluate it on independent human and AI writing samples with a wider variety of writing styles and lengths.

**The trade I'd make if this ran for real:**

If I deployed this system, I would prioritize reducing false accusations against genuine writers, even if that meant allowing more AI-generated writing to receive an unsure label. The cost of this decision would fall on instructors or reviewers, who would need to investigate uncertain cases manually, but I consider that preferable to wrongly accusing someone based solely on an unreliable detector score.

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [x] criteria.md has five numbered criteria, each naming a target
       [x] Each has a reason underneath
       [x] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [x] Two signals that measure DIFFERENT things, each with a named blind spot
       [x] Three label variants, all reachable, written out in full
       [x] POST /appeal changes status and writes to the log
       [x] Signals and Scoring names scoring.py::combine_signals
       [x] Sample Run: a submission AND an appeal, as pasted text
       [x] At least four new commits
       [x] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [x] Rate limiting on /submit, with your numbers justified
       [x] The pasted run of status codes showing 429
       [x] Audit log with all nine fields, recording rejections too
       [x] The attack set run IN FULL, every input with an outcome
       [x] Ten audit log entries pasted as text
       [x] Five criteria across three trials
       [x] A diagnosis for every miss and every broken attack — stage AND mechanism
       [x] One improvement, with Attack Run — After
       [x] What's Still Broken, including the production trade
       [x] At least four new commits
       [x] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
