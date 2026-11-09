# Extra checks — before

- Produced by: `run_extra_checks.py::main`
- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_log`, `app.py::health`
- 3 trials · 2026-11-08 18:54

| Criterion | Target | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| 4. Appeal reliability | 6 of 6 | 6/6 | 6/6 | 6/6 |
| 5. Bad input handling | 7 of 7 | 7/7 | 7/7 | 7/7 |

---

## What actually came back

**Trial 1**

```json
{
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
      "content_id": "00ea2834-f42f-46e3-8318-a613c99df4e2",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "159e0ceb-1c92-4117-bd99-683d491851b2",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "fb2c6460-410b-4bb1-8b0c-55276130bc71",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "741fce83-d25a-419c-a564-661ac0bf0c48",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "27dd61a7-24a6-40de-9044-752a6c5f6b8f",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "0a43ef0b-e794-47e6-aa71-b3a8b9b2d844",
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
      "content_id": "04886b65-f365-4a3c-8b45-a085a4247f54",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "ffdca431-f9d5-4897-960f-f4d7645a9a8a",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "269d6f46-fdc9-4208-9034-512289d3d7f9",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "81e6a525-bc12-47fd-8e69-ecafee92c535",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "ff5a1f47-0bd5-4f14-93ee-2cb18b0cad1e",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "5eb95fea-75ed-419a-a592-41376a929f25",
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
