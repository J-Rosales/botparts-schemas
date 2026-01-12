# Date Fields Standard

This document defines the canonical behavior for date fields in Botparts data outputs. It reflects the authoritative standard for all repositories that emit or consume the catalogue and character manifests.

## Overview
- Both `uploadDate` and `updatedAt` are required in the catalogue index entry records.
- Character manifests must include `site.uploadDate` and `site.updatedAt`.
- When a character is initially created, `updatedAt` defaults to the same value as `uploadDate`.

## Canonical formatting
- Both fields are strings.
- The canonical form is **date-only ISO-8601** (`YYYY-MM-DD`).
- The empty string (`""`) is allowed to represent unknown dates.

## Field sources and precedence
The canonical resolution order for data producers is:

### `uploadDate`
1. Catalogue seed entry `uploadDate`.
2. Character source manifest `uploadDate` (top-level or `x.uploadDate`).
3. Character source manifest legacy field `updated`.
4. Default: `""` (empty string).

### `updatedAt`
1. Catalogue seed entry `updatedAt`.
2. Character source manifest `updatedAt` (top-level or `x.updatedAt`).
3. Default: value of `uploadDate`.

## Emission requirements
Data producers must emit the following fields:

- **Catalogue index entries**
  - `entries[].uploadDate`
  - `entries[].updatedAt`

- **Character manifest**
  - `site.uploadDate`
  - `site.updatedAt`
  - `x.uploadDate` (recommended for traceability)
  - `x.updatedAt` (recommended for traceability)

## Consumer expectations
Consumers should:
- Accept the empty string as "unknown" for either date field.
- Treat `updatedAt` as the authoritative change indicator when both fields are present.

## Related schemas
- `schemas/index.schema.json`
- `schemas/manifest.schema.json`
