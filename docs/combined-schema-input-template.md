# Combined Schema Input Template

Use this template when drafting combined schema inputs for the generator. It lists the expected headers and the optional sections that may appear in a combined schema submission.

## Required headers

- `# Title`
- `## Summary`
- `## Display name`
- `## Base spec`
- `## Prompt manifest`
- `## Elaborate prompt notes`
- `## Draft edits (manual)`
- `## Audit notes`
- `## Variant notes`

## Optional headers

- `## Attribution`
- `## Notes`

### Variant notes

Variant notes are optional and describe deltas that should be applied to create variants from the base specification.

Structure:

- `## Variant notes`
  - `### Variant Name`
    - Freeform notes describing the delta from the base spec.

### Heading nesting rules

The generator validation only permits H3 headings under `## Variant notes`. Any other nested structure should use bullet list items (including nested bullets under `## Variant notes` as needed).

## Template (skeleton)

```
# Title

## Summary

## Display name

## Base spec

## Prompt manifest

## Elaborate prompt notes

## Draft edits (manual)

## Audit notes

## Attribution

## Notes

## Variant notes

### Variant Name

```
