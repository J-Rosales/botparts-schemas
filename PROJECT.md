# PROJECT.md — botparts-schemas

## Role
`botparts-schemas` is the **source of truth** for all structural contracts in the Botparts project.

It defines how character data, manifests, fragments, and indexes are shaped and validated.

## Authority
- This repository owns schema definitions.
- Other repos **vendor** these schemas and must not modify them locally.

## Consumers
- `botparts-generator` validates outputs against these schemas.
- `botparts-site` validates and consumes generated data using these schemas.

## Versioning
- Schema changes should be deliberate and reviewed.
- Tag releases when breaking or significant changes occur (e.g. `v0.2.0`).
- Downstream repos update schemas via subtree pulls.

## Design Principles
- Schemas should be:
  - explicit but permissive
  - forward‑compatible where possible
  - stable once published
- Extension points should use `x-*` fields rather than breaking changes.

## Codex Rules
When working in this repo:
- Edit schemas only.
- Do not introduce site or generator logic.
- Document breaking changes clearly.
