# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 20:38
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator*id `attacker*<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID      | Family             | Targeting                                              | Status | Content ID                             | Guess  | Score | Verdict |
| ------- | ------------------ | ------------------------------------------------------ | ------ | -------------------------------------- | ------ | ----- | ------- |
| EV01    | evasion            | signal two: typos raise word variety                   | 200    | `d5c3b2a0-9925-40c1-b696-1161249cdc49` | unsure | 0.600 | BROKE   |
| EV02    | evasion            | signal two: broken-up sentences raise length spread    | 200    | `bebe1b00-b0dc-4efc-8f17-3c1e7845d928` | unsure | 0.567 | BROKE   |
| EV03    | evasion            | signal two: a pasted quotation changes the shape       | 200    | `9d62572a-3504-4e5c-b68b-c25bfed81238` | ai     | 0.745 | HELD    |
| EV04    | evasion            | signal one: unusual words raise perplexity             | 200    | `81335c1d-14fa-49c9-be38-9399b4f31819` | ai     | 0.789 | HELD    |
| EV05    | evasion            | both signals: heavy human editing pass                 | 200    | `60064db0-8fe5-4b0b-a509-d2b31a074157` | unsure | 0.396 | BROKE   |
| EV06    | evasion            | signal two: one very long sentence and one very short  | 200    | `b6f178c6-c0d2-4e75-8e9a-92ef3a4dd155` | unsure | 0.451 | BROKE   |
| EV07    | evasion            | signal two: padding with punctuation                   | 200    | `5844e5e8-91bf-46bd-9150-9684526cc092` | unsure | 0.525 | BROKE   |
| EV08    | evasion            | signal one: text below the token window                | 200    | `74772028-bbc5-41e3-93d5-bd79a18678fc` | unsure | 0.600 | BROKE   |
| EV09    | evasion            | both: AI text with a human opening paragraph bolted on | 200    | `163ac57b-96b7-40f9-b285-927cc471acad` | ai     | 0.733 | HELD    |
| EV10    | evasion            | signal two: repeated stanza structure                  | 200    | `cbb19330-b1c0-4bfc-ba69-6f60fcc964a6` | unsure | 0.471 | BROKE   |
| FP01    | false_positive     | plain, clear human writing with no flourishes          | 200    | `60e54c38-f769-4eb9-b81b-86507af5a924` | unsure | 0.432 | HELD    |
| FP02    | false_positive     | human writing in a formal register                     | 200    | `99a88702-0a52-48da-ad41-84bcb0042b01` | unsure | 0.459 | HELD    |
| FP03    | false_positive     | a non-native English speaker writing carefully         | 200    | `45807559-bc97-4be4-a74f-f31f28d1765f` | unsure | 0.564 | HELD    |
| FP04    | false_positive     | a student essay written to a rubric                    | 200    | `78826ccf-642d-4e27-ab8f-6f271e253fcf` | unsure | 0.568 | HELD    |
| FP05    | false_positive     | technical documentation written by a person            | 200    | `f8b363ca-b0a0-4d9e-9cb8-b1cd2e54bdbd` | unsure | 0.431 | HELD    |
| FP06    | false_positive     | a person imitating a formal template                   | 200    | `69d8e684-38ef-4fc3-8021-fabe5f539220` | unsure | 0.421 | HELD    |
| FP07    | false_positive     | human writing that repeats a phrase deliberately       | 200    | `fc788862-80ec-4be8-9710-a06c270d0c79` | unsure | 0.386 | HELD    |
| FP08    | false_positive     | very short genuine human submission                    | 200    | `981e349d-bb41-48ec-a7a4-4d9d24147ae9` | unsure | 0.600 | HELD    |
| PI01    | prompt_injection   | instruction to ignore the check                        | 200    | `a503bd1e-c987-4b91-9c13-3566431aea0d` | unsure | 0.609 | HELD    |
| PI02    | prompt_injection   | instruction disguised as a system message              | 200    | `de34776b-ac24-4d13-ba24-310470ca8b55` | unsure | 0.542 | HELD    |
| PI03    | prompt_injection   | instruction wrapped in the writer's voice              | 200    | `2474bc50-38cf-4fe9-a93c-32ef4b61ebeb` | ai     | 0.693 | HELD    |
| PI04    | prompt_injection   | attempt to make the label text hostile                 | 200    | `63a20feb-e447-444e-b0cc-ab99e94c9985` | unsure | 0.510 | HELD    |
| PI05    | prompt_injection   | attempt to inject into the audit log                   | 200    | `0c141eb2-ccff-4ce7-b527-18a319782abd` | ai     | 0.740 | HELD    |
| PI06    | prompt_injection   | instruction plus real human text                       | 200    | `b862e143-696e-463a-b425-3d8e929703aa` | unsure | 0.423 | HELD    |
| MF01    | malformed          | text is only whitespace                                | 400    | `—`                                    | —      | —     | HELD    |
| MF02    | malformed          | text is a single character                             | 400    | `—`                                    | —      | —     | HELD    |
| MF03    | malformed          | text is control characters                             | 200    | `d2948907-ee08-486e-bcc1-d75711fc5730` | unsure | 0.510 | HELD    |
| MF04    | malformed          | text is only punctuation                               | 200    | `4fb754d4-76e8-442e-bae2-c6878c1c837d` | human  | 0.095 | BROKE   |
| MF05    | malformed          | text is a very long single word                        | 200    | `aeb368da-c035-4cea-a733-dadbc9607204` | ai     | 0.909 | BROKE   |
| MF06    | malformed          | text is emoji only                                     | 200    | `5cd9a851-6727-469c-ba88-b37f7819f012` | unsure | 0.489 | HELD    |
| MF07    | malformed          | text is right-to-left script                           | 200    | `ffbda418-fb78-4f54-b2cd-bf85efffb2ea` | unsure | 0.453 | HELD    |
| MF08    | malformed          | text is 60,000 characters                              | 413    | `—`                                    | —      | —     | HELD    |
| RQ01    | malformed          | no text field at all                                   | 400    | `—`                                    | —      | —     | HELD    |
| RQ02    | malformed          | no creator_id                                          | 400    | `—`                                    | —      | —     | HELD    |
| RQ03    | malformed          | text is a number                                       | 400    | `—`                                    | —      | —     | HELD    |
| RQ04    | malformed          | text is a list                                         | 400    | `—`                                    | —      | —     | HELD    |
| RQ05    | malformed          | text is null                                           | 400    | `—`                                    | —      | —     | HELD    |
| RQ06    | malformed          | creator_id is an object                                | 400    | `—`                                    | —      | —     | HELD    |
| RQ07    | malformed          | body is a JSON array, not an object                    | 400    | `—`                                    | —      | —     | HELD    |
| RQ08    | malformed          | body is unparseable JSON                               | 400    | `—`                                    | —      | —     | HELD    |
| RQ09    | malformed          | body is empty                                          | 400    | `—`                                    | —      | —     | HELD    |
| RQ10    | malformed          | body is form-encoded, not JSON                         | 400    | `—`                                    | —      | —     | HELD    |
| RQ11    | malformed          | body is JSON claiming to be plain text                 | 400    | `—`                                    | —      | —     | HELD    |
| RQ12    | malformed          | deeply nested JSON                                     | 400    | `—`                                    | —      | —     | HELD    |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c2ed925e-4511-4fd7-9f16-0ba5ae9e2480` | unsure | 0.521 | HELD    |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `dc7ff01c-555e-45fe-a97f-5bedad893ad6` | unsure | 0.521 | HELD    |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `5f4c7541-1358-487a-b57e-02f783ecafdc` | unsure | 0.521 | HELD    |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `5fe20bb0-7f1c-40b5-9de6-d27b818143d2` | unsure | 0.521 | HELD    |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `ff3b3a04-5696-4ee1-816b-e7cfb281c35a` | unsure | 0.521 | HELD    |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `ae59ed28-4f96-49c0-9c88-871d56c6d031` | unsure | 0.521 | HELD    |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `d21280ca-acfe-4108-8e87-227853d54d9c` | unsure | 0.521 | HELD    |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `05bd3c26-426a-4d87-b342-4c8dd9a91248` | unsure | 0.521 | HELD    |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `712b1839-9d2f-4dd1-90f3-7012bbe843e3` | unsure | 0.521 | HELD    |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `362f9f0a-8603-44d9-9a46-c9822b2a31b6` | unsure | 0.521 | HELD    |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |

---

## By family

| Family               | Attacks | Auto-BROKE | Left to judge |
| -------------------- | ------- | ---------- | ------------- |
| `evasion`            | 10      | 0          | 10            |
| `false_positive`     | 8       | 0          | 8             |
| `flood_same_creator` | 12      | 0          | 12            |
| `malformed`          | 20      | 0          | 20            |
| `prompt_injection`   | 6       | 0          | 6             |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

_Targeting:_ signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d5c3b2a0-9925-40c1-b696-1161249cdc49",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.1635,
  "style_score": 0.9107,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

_Targeting:_ signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "bebe1b00-b0dc-4efc-8f17-3c1e7845d928",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5669,
  "model_score": 0.5943,
  "style_score": 0.5486,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

_Targeting:_ signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "9d62572a-3504-4e5c-b68b-c25bfed81238",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.7449,
  "model_score": 0.6662,
  "style_score": 0.7973,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

_Targeting:_ signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "81335c1d-14fa-49c9-be38-9399b4f31819",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7889,
  "model_score": 0.6114,
  "style_score": 0.9073,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

_Targeting:_ both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "60064db0-8fe5-4b0b-a509-d2b31a074157",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3963,
  "model_score": 0.3212,
  "style_score": 0.4464,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

_Targeting:_ signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "b6f178c6-c0d2-4e75-8e9a-92ef3a4dd155",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.451,
  "model_score": 0.5727,
  "style_score": 0.3698,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

_Targeting:_ signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "5844e5e8-91bf-46bd-9150-9684526cc092",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5248,
  "model_score": 0.5862,
  "style_score": 0.4839,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

_Targeting:_ signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "74772028-bbc5-41e3-93d5-bd79a18678fc",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.2452,
  "style_score": 0.8815,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

_Targeting:_ both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "163ac57b-96b7-40f9-b285-927cc471acad",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.7325,
  "model_score": 0.7042,
  "style_score": 0.7514,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

_Targeting:_ signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "cbb19330-b1c0-4bfc-ba69-6f60fcc964a6",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.4711,
  "model_score": 0.9792,
  "style_score": 0.1324,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

_Targeting:_ plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "60e54c38-f769-4eb9-b81b-86507af5a924",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4317,
  "model_score": 0.6175,
  "style_score": 0.3078,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

_Targeting:_ human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "99a88702-0a52-48da-ad41-84bcb0042b01",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.459,
  "model_score": 0.7387,
  "style_score": 0.2725,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

_Targeting:_ a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "45807559-bc97-4be4-a74f-f31f28d1765f",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5635,
  "model_score": 0.8051,
  "style_score": 0.4025,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

_Targeting:_ a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "78826ccf-642d-4e27-ab8f-6f271e253fcf",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5683,
  "model_score": 0.8329,
  "style_score": 0.3919,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

_Targeting:_ technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "f8b363ca-b0a0-4d9e-9cb8-b1cd2e54bdbd",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.4309,
  "model_score": 0.8005,
  "style_score": 0.1845,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

_Targeting:_ a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "69d8e684-38ef-4fc3-8021-fabe5f539220",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.4214,
  "model_score": 0.8814,
  "style_score": 0.1147,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

_Targeting:_ human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "fc788862-80ec-4be8-9710-a06c270d0c79",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.3862,
  "model_score": 0.8816,
  "style_score": 0.056,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

_Targeting:_ very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "981e349d-bb41-48ec-a7a4-4d9d24147ae9",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.3223,
  "style_score": 0.8186,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

_Targeting:_ instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "a503bd1e-c987-4b91-9c13-3566431aea0d",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.6092,
  "model_score": 0.4625,
  "style_score": 0.707,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

_Targeting:_ instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "de34776b-ac24-4d13-ba24-310470ca8b55",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.542,
  "model_score": 0.2044,
  "style_score": 0.7671,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

_Targeting:_ instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2474bc50-38cf-4fe9-a93c-32ef4b61ebeb",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.6934,
  "model_score": 0.5943,
  "style_score": 0.7595,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

_Targeting:_ attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "63a20feb-e447-444e-b0cc-ab99e94c9985",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5097,
  "model_score": 0.4998,
  "style_score": 0.5163,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

_Targeting:_ attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "0c141eb2-ccff-4ce7-b527-18a319782abd",
  "creator_id": "attacker_PI05",
  "guess": "ai",
  "confidence": 0.74,
  "model_score": 0.6401,
  "style_score": 0.8066,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

_Targeting:_ instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "b862e143-696e-463a-b425-3d8e929703aa",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4233,
  "model_score": 0.5583,
  "style_score": 0.3333,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

_Targeting:_ text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

_Targeting:_ text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

_Targeting:_ text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "d2948907-ee08-486e-bcc1-d75711fc5730",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.51,
  "model_score": 0.0,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

_Targeting:_ text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "4fb754d4-76e8-442e-bae2-c6878c1c837d",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.0945,
  "model_score": 0.0112,
  "style_score": 0.15,
  "label": "This writing appears to have been written by a person, although its origin cannot be verified automatically.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

_Targeting:_ text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "aeb368da-c035-4cea-a733-dadbc9607204",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.909,
  "model_score": 0.9976,
  "style_score": 0.85,
  "label": "This writing shows patterns associated with AI-generated text. This assessment is not proof of AI authorship and may be incorrect.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

_Targeting:_ text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "5cd9a851-6727-469c-ba88-b37f7819f012",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.4888,
  "model_score": 0.9969,
  "style_score": 0.15,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

_Targeting:_ text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "ffbda418-fb78-4f54-b2cd-bf85efffb2ea",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.4526,
  "model_score": 0.9064,
  "style_score": 0.15,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

_Targeting:_ text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

_Targeting:_ no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

_Targeting:_ no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

_Targeting:_ text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

_Targeting:_ text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

_Targeting:_ text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

_Targeting:_ creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

_Targeting:_ body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

_Targeting:_ body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

_Targeting:_ body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

_Targeting:_ body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

_Targeting:_ body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

_Targeting:_ deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c2ed925e-4511-4fd7-9f16-0ba5ae9e2480",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "dc7ff01c-555e-45fe-a97f-5bedad893ad6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "5f4c7541-1358-487a-b57e-02f783ecafdc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "5fe20bb0-7f1c-40b5-9de6-d27b818143d2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "ff3b3a04-5696-4ee1-816b-e7cfb281c35a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "ae59ed28-4f96-49c0-9c88-871d56c6d031",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "d21280ca-acfe-4108-8e87-227853d54d9c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "05bd3c26-426a-4d87-b342-4c8dd9a91248",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "712b1839-9d2f-4dd1-90f3-7012bbe843e3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "362f9f0a-8603-44d9-9a46-c9822b2a31b6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5215,
  "model_score": 0.0287,
  "style_score": 0.85,
  "label": "We cannot reliably determine whether this writing was written by a person or generated with AI. This result should not be treated as evidence of misconduct.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
