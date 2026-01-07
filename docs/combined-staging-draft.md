# Combined Staging Draft (Schema Authoring)

This document describes the combined staging draft format used during schema authoring.

## Prompt manifest list

The prompt manifest should enumerate all prompt keys expected by the generator:

- `elaboration`
- `extraction`
- `idiosyncrasy_module`
- `rewrite_variants`

## Optional headers

The combined staging draft may include optional headers when relevant:

- `## Attribution`
- `## Notes`
- `## Variant notes`

`## Variant notes` supports a flat list of variant names (as `###` headers) to capture per-variant deltas for authoring.
