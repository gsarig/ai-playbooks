# Resource Library

A curated library of evaluated methodologies, workflows, and patterns. Grouped by verdict — focus on `adopt` and `adapt` first.

**Verdicts:** `adopt` — use as-is · `adapt` — sound idea, needs adjustment · `watch` — promising, not yet ready · `catalog` — good tool, out of scope · `skip` — not worth it (reasoning documented)

> This index is maintained automatically via Dataview. Install the Dataview community plugin if the tables below are not rendering.

## Adopt

```dataview
TABLE author, tags FROM "" WHERE verdict = "adopt" SORT date_evaluated DESC
```

## Adapt

```dataview
TABLE author, tags FROM "" WHERE verdict = "adapt" SORT date_evaluated DESC
```

## Watch

```dataview
TABLE author, tags FROM "" WHERE verdict = "watch" SORT date_evaluated DESC
```

## Catalog

```dataview
TABLE author, tags FROM "" WHERE verdict = "catalog" SORT date_evaluated DESC
```

## Skip

```dataview
TABLE author, tags FROM "" WHERE verdict = "skip" SORT date_evaluated DESC
```
