# Extra checks — after

- Produced by: `run_extra_checks.py::main`
- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_log`, `app.py::health`
- 3 trials · 2026-11-08 21:06

| Criterion             | Target | Run 1 | Run 2 | Run 3 |
| --------------------- | ------ | ----- | ----- | ----- |
| 4. Appeal reliability | 6 of 6 | 6/6   | 6/6   | 6/6   |
| 5. Bad input handling | 7 of 7 | 7/7   | 7/7   | 7/7   |

---

## What actually came back

**Trial 1**

```json
{
  "appeals": [
    {
      "check": "appeal 1",
      "content_id": "3100a2c0-9328-4644-abbe-3bf342587918",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "ad6ff2cc-0f8e-4d70-8e9e-93c1c7b52715",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "6cd4832b-3912-4974-a88b-4e8cb3c7de51",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "a912851e-7556-44c1-b6ec-7be0c465bae9",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "7abd7c45-8b26-4a34-9bbe-6ab096358b41",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "f84fd872-e13e-4c2a-8cea-e5dcd197cdc8",
      "appeal_status_code": 404,
      "appeal_in_log": false,
      "passed": true
    }
  ],
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
}
```

**Trial 2**

```json
{
  "appeals": [
    {
      "check": "appeal 1",
      "content_id": "72525a78-106d-4bd1-9444-3256c685e4a3",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "640821a7-561c-4e52-a831-703594937a47",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "02dfaf1f-4663-4bbb-b1d7-b3335d2cb628",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "0bf9844a-d1ae-44da-9237-8ee867062d6f",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "2e1cf0f1-a79f-463f-b5f0-e092e897dff4",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "739c1ae3-dec7-40ba-97ac-d28f6ec55678",
      "appeal_status_code": 404,
      "appeal_in_log": false,
      "passed": true
    }
  ],
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
}
```

**Trial 3**

```json
{
  "appeals": [
    {
      "check": "appeal 1",
      "content_id": "eb0a0dde-b2ee-4615-8874-8f8485e2b5e4",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "08262cc6-2883-4d28-830b-c1d81107cb75",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "7361edc3-cb36-43f3-bb0f-0781db6388a6",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "a0f5a624-ec31-4d95-9900-63437296d170",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "6f3086e8-3a32-43c5-a502-81b0180ba87c",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "fbd6112a-2407-40b8-8792-fbe2d68735c7",
      "appeal_status_code": 404,
      "appeal_in_log": false,
      "passed": true
    }
  ],
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
}
```
