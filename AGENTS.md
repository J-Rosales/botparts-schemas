# AGENTS.md — botparts-schemas

Date: 2025-12-30

## Repository role (authoritative)
This repository is the **single source of truth for all JSON Schemas** used by the Botparts project.

It defines:
- the catalogue index schema
- the character schema
- the output / manifest schema
- attribution, licensing, and redistribution fields

No other repository may *authoritatively* define or modify schemas.

## Scope boundaries (non-negotiable)
This repository MUST NOT:
- generate data
- consume generator output
- contain site UI logic
- depend on other Botparts repositories

Other repositories **vendor** schemas from here verbatim.

## What agents may do here
Agents working in this repository may:
- draft and evolve JSON Schemas
- add schema documentation and examples
- add schema validation tests
- bump VERSION when schemas change
- ensure backward compatibility or document breaking changes

## What agents must not do here
- Do not add generator logic.
- Do not add site logic.
- Do not tailor schemas to implementation quirks of downstream repos.
- Do not embed sample content that is not schema-related.

## Directory contract
Expected structure:
- /schemas/*.schema.json   (authoritative schemas)
- /docs/                   (schema explanations, rationale)
- VERSION                  (schema version)

No other top-level concerns belong here.

## Integration contracts
- `botparts-generator` must validate its output against schemas from this repo.
- `botparts-site` must validate consumed data against vendored copies of these schemas.
- Any schema drift must be resolved **here first**, then re-vendored.

## Testing expectations
Agents may generate:
- pytest-based schema validation tests
- JSON Schema meta-schema checks
- reference-resolution tests

All tests must run offline.

## Mental model
Think of this repo as a **standards body**, not an application.
