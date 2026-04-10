# Resource evaluation queue

Drop a clipped page here and the hourly cron job will evaluate it automatically, writing the result to `resources/reviews/`.

## Expected format

Obsidian Web Clipper's default output works as-is. The evaluator reads the `source` or `url` frontmatter field for the URL. Everything else in the file is ignored.

```yaml
---
title: "Some Article Title"
source: https://example.com/article
author: "Author Name"
published: 2026-01-15
created: 2026-04-10
description: "A brief description."
tags: []
---
```

## What happens next

- The cron job runs hourly and processes any `.md` files it finds here (except this README).
- Successful evaluations are written to `resources/reviews/` and the source file moves to `processed/`.
- Failed evaluations (bad URL, fetch error, missing URL field) move to `failed/` with an error note appended.
