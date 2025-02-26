import json
import os

import pytest

from oopsallyaml import scan_files


@pytest.mark.parametrize(
  "test_directory",
  [
    "file-not-found",
    "invalid-yaml",
    "no-schema",
    "no-schema-header",
    "schema-opt-out",
    "schema-valid",
    "yaml-from-hell",
  ],
)
def test_with_subdirectory(test_directory: str):
  current_directory = os.getcwd()
  try:
    os.chdir(f"tests/{test_directory}")
    with open("test_spec.json") as f:
      spec = json.load(f)
    errors = [list(e) for e in scan_files(spec["files"])]
    assert spec["errors"] == errors
  finally:
    os.chdir(current_directory)
