from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "schema-folder-input.md"

ALLOWED_H1 = "Character concept (staging selection)"
ALLOWED_H2 = {
    "Display name",
    "Elaborate prompt notes",
    "Draft edits (manual)",
    "Audit notes",
    "Variant notes",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError("Frontmatter must start with '---'.")

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            frontmatter = "\n".join(lines[: index + 1])
            body = "\n".join(lines[index + 1 :])
            return frontmatter, body

    raise AssertionError("Frontmatter must end with '---'.")


def test_schema_folder_input_fixture_is_valid():
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    assert "version:" in frontmatter, "Frontmatter must include a version field."
    assert "prompts:" in frontmatter, "Frontmatter must include a prompts mapping."

    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    headings = []
    for line in body.splitlines():
        match = heading_re.match(line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))

    h1s = [title for level, title in headings if level == 1]
    assert h1s == [ALLOWED_H1], (
        "Schema-folder input must include exactly one H1 titled "
        f"'{ALLOWED_H1}'. Found: {h1s}"
    )

    for level, title in headings:
        if level == 2:
            assert title in ALLOWED_H2, f"Unsupported H2 section '{title}'."
        elif level >= 3:
            raise AssertionError(
                f"Unsupported heading level {level} ('{title}'); use bullets under '## Variant notes'."
            )

    assert any(title == "Variant notes" for level, title in headings), (
        "Schema-folder input must include a '## Variant notes' section."
    )
