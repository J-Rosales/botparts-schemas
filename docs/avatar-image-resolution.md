# Avatar Image Resolution Standard

This document defines the canonical avatar image location used by Botparts data consumers and producers.

## Canonical location

All characters must use a single, canonical avatar image located at:

```
data/characters/<slug>/avatarImage.png
```

## Usage

The canonical avatar image is used for:
- catalogue cards
- character detail views
- all prose variants
- all character variants (e.g. `/variants/<variantSlug>/`)
- character downloads that embed PNG metadata (variants included)

## Implications

- Variant folders **must not** include their own `avatarImage.png`.
- Variant selection changes only the spec JSON (`spec_v2_<prose>.json`) and does **not** change the avatar image.

## Schema alignment

When schema fields refer to a thumbnail or avatar path, they should resolve to the canonical location above.
