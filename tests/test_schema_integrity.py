import json
from pathlib import Path
from urllib.parse import urlparse

import pytest

jsonschema = pytest.importorskip(
    "jsonschema",
    reason="jsonschema is required to validate JSON Schema meta-schema compliance",
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"


def load_schema(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"Invalid JSON in schema {path}: {exc}") from exc


def iter_schema_files() -> list[Path]:
    if not SCHEMAS_DIR.exists():
        raise AssertionError(f"Expected schemas directory at {SCHEMAS_DIR}")
    return sorted(SCHEMAS_DIR.rglob("*.schema.json"))


def resolve_json_pointer(document, pointer: str) -> bool:
    if pointer in ("", None):
        return True
    if not pointer.startswith("/"):
        return False
    current = document
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if part not in current:
                return False
            current = current[part]
        elif isinstance(current, list):
            try:
                index = int(part)
            except ValueError:
                return False
            if index < 0 or index >= len(current):
                return False
            current = current[index]
        else:
            return False
    return True


def iter_refs(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from iter_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_refs(item)


def split_ref(ref: str):
    parsed = urlparse(ref)
    if parsed.scheme and parsed.scheme != "file":
        return None, None, f"Non-local ref scheme '{parsed.scheme}' in $ref '{ref}'"

    if parsed.scheme == "file":
        path_part = parsed.path
        fragment = parsed.fragment
    else:
        if "#" in ref:
            path_part, fragment = ref.split("#", 1)
        else:
            path_part, fragment = ref, ""

    return path_part, fragment, None


def resolve_ref(ref: str, base_path: Path, schemas_by_path: dict[Path, dict]) -> str | None:
    path_part, fragment, error = split_ref(ref)
    if error:
        return error

    if path_part in ("", None):
        target_path = base_path
    else:
        target_path = (base_path.parent / path_part).resolve()

    if target_path not in schemas_by_path:
        return f"$ref '{ref}' in {base_path} points to missing schema {target_path}"

    if fragment and not fragment.startswith("/"):
        return f"$ref '{ref}' in {base_path} uses unsupported fragment '{fragment}'"

    if not resolve_json_pointer(schemas_by_path[target_path], fragment):
        return f"$ref '{ref}' in {base_path} points to missing fragment '#{fragment}'"

    return None


def test_schema_validity():
    schema_files = iter_schema_files()
    assert schema_files, "No schema files found under schemas/"

    for path in schema_files:
        schema = load_schema(path)
        schema_draft = schema.get("$schema")
        assert schema_draft, f"Schema {path} must declare $schema"
        try:
            validator_cls = jsonschema.validators.validator_for(schema)
            validator_cls.check_schema(schema)
        except jsonschema.exceptions.SchemaError as exc:
            raise AssertionError(
                f"Schema {path} does not conform to declared meta-schema {schema_draft}: {exc}"
            ) from exc


def test_internal_consistency():
    schema_files = iter_schema_files()
    schemas_by_path = {path.resolve(): load_schema(path) for path in schema_files}

    ids = {}
    for path, schema in schemas_by_path.items():
        schema_id = schema.get("$id")
        if schema_id:
            if schema_id in ids:
                raise AssertionError(
                    f"Duplicate $id '{schema_id}' found in {path} and {ids[schema_id]}"
                )
            ids[schema_id] = path

        for ref in iter_refs(schema):
            error = resolve_ref(ref, path, schemas_by_path)
            if error:
                raise AssertionError(error)


def test_no_downstream_leakage():
    allowed_top_level = {
        "schemas",
        "tests",
        "docs",
        "README.md",
        "PROJECT.md",
        "VERSION",
        "pyproject.toml",
        "pytest.ini",
        "setup.cfg",
        ".git",
        ".gitignore",
    }

    unexpected = [
        path.name
        for path in REPO_ROOT.iterdir()
        if path.name not in allowed_top_level
    ]
    assert not unexpected, (
        "Unexpected top-level entries found (schemas/docs/config only): "
        + ", ".join(sorted(unexpected))
    )

    banned_dirs = {
        "site",
        "dist",
        "build",
        "public",
        "node_modules",
        "out",
        "generated",
        "__pycache__",
        ".pytest_cache",
    }

    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if any(part in banned_dirs for part in path.parts):
            raise AssertionError(f"Generated/site artifact detected at {path}")


def test_version_integrity():
    version_path = REPO_ROOT / "VERSION"
    assert version_path.exists(), "VERSION file is required at repository root"
    version_value = version_path.read_text(encoding="utf-8").strip()
    assert version_value, "VERSION file must be non-empty"
