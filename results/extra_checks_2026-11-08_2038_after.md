# Extra checks — after

- Produced by: `run_extra_checks.py::main`
- Service: `app.py::submit`, `app.py::appeal`, `app.py::get_log`, `app.py::health`
- 3 trials · 2026-11-08 20:38

| Criterion             | Target | Run 1 | Run 2 | Run 3 |
| --------------------- | ------ | ----- | ----- | ----- |
| 4. Appeal reliability | 6 of 6 | 6/6   | 6/6   | 6/6   |
| 5. Bad input handling | 7 of 7 | 5/7   | 5/7   | 5/7   |

---

## What actually came back

**Trial 1**

```json
{
  "appeals": [
    {
      "check": "appeal 1",
      "content_id": "57576dd2-c61d-48de-914f-07976e154af3",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "ce7d9f4e-49dc-416d-9930-13eadb9e7ecd",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "cec8fbb8-6125-45f2-816c-1343935b2a4d",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "e58e3a91-5999-4450-9951-eaffbd392fcb",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "25ab9b26-d6ce-4db5-97ec-60469854e296",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "9ffda28e-00fa-4be7-8af6-5fe5b6e43c9a",
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
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
      "content_id": "8e72a362-45f5-4f86-b20d-7e81c632326e",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "65045533-0101-4cb6-b0c7-56ed68745b15",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "a6e60f2b-7cd6-4991-b901-1f9688ee29f3",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "62b23fc6-6aa3-41d2-a4d3-5b3419bc317a",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "6097f930-4d20-44f0-963d-52c3385c4bc7",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "c7823326-591b-49e9-b63d-38ca2bdd5e98",
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
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
      "content_id": "9e7a253b-c9a9-485c-a515-ee948a2d59c8",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 2",
      "content_id": "4e93cf0d-52a7-4c1f-a531-7ebacb239d75",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 3",
      "content_id": "0925602a-f639-4967-a389-60f9a85c5617",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 4",
      "content_id": "119530c5-5f83-4a6a-b5f7-3e1a87d84a92",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "appeal 5",
      "content_id": "1729507d-0863-4459-b739-d8d114fa3852",
      "appeal_status_code": 200,
      "response_status": "under_review",
      "appeal_in_log": true,
      "latest_status_in_log": "under_review",
      "passed": true
    },
    {
      "check": "nonexistent content_id",
      "content_id": "bceb4c5c-cdff-48ef-b19d-8189b2350e47",
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
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
      "status": 429,
      "json_error": "rate_limited",
      "health_after": 200,
      "passed": false
    }
  ]
}
```
