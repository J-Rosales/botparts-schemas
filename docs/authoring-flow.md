# Schema Authoring Flow

This flow describes the high-level order of operations during schema authoring.

1. Draft the base combined schema input.
2. Run elaboration on the base specification.
3. Generate the idiosyncrasy module from the elaborated spec.
4. Run extraction to produce the structured schema outputs.
5. Mid-point confirmation (author review).
6. Create variants using `## Variant notes` deltas.
7. Final validation and publication.

See `docs/schema-folder-input.md` for the markdown structure expected by `bp author schema-folder`.
