# Extra checks — after_rerun

- Produced by: `run_extra_checks.py::main`
- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_log`, `app.py::health`
- 3 trials · 2026-11-08 20:53

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
      "content_id": "6770f15e-6648-4831-b57d-7fae989e3093",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "5672bc80-d3cf-41ee-88ec-26b24801c7be",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "39d00eca-e7c0-4923-bc13-55445d4068bf",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "2e3d83d5-3f80-4b8d-8e4a-b53180ee4f1b",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "dc28913e-b451-4639-b5f9-8b9cd5f9a746",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "80301def-7095-4656-ab0b-08e0fa732777",
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
      "content_id": "e00fa8a7-7956-4545-a2b1-cd35ab837ee3",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "918bf9b8-d08a-4861-aef3-d1aa846d2b80",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "7022eb0f-bad7-4f94-96d7-7159bb0bdef8",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "da30f486-5089-481f-8141-9ada0fe64c07",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "adfc9852-cd72-4d7b-9e97-030ca92d466f",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "5d15ef74-aa6d-4303-b520-6dc4967f5e4d",
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
      "content_id": "a2d98bea-4e6f-4630-b671-24beb712648d",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "7471f943-8f20-4200-b15d-9a5223bb3be9",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "d0a7d943-c157-49d7-bf45-fd2a4ba584f5",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "052a7040-2562-4b41-89fd-e63b9433a620",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "f67da7f8-8c16-45c0-851a-204cb562bbad",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "e7bbd290-a1d3-4e8e-beb3-9483a6862617",
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
