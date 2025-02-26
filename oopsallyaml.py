import functools
import re
import sys
from typing import Optional

import yamale
import yaml


class ValidationError(Exception):
  messages: list[str]

  def __init__(self, messages: list[str]):
    self.messages = messages


def extract_schema_name(filename) -> Optional[str]:
  with open(filename) as f:
    first_line = f.readline()
    match = re.match("# (no )?schema: (.+)", first_line)
    if not match:
      raise ValidationError(["no schema name found", "add a '# schema: <name>' declaration in the first line"])
    if match.group(1):
      return None
    return match.group(2)


@functools.cache
def load_schema(schema_name: str) -> yamale.schema.Schema:
  try:
    schema_path = f".yamlschemas/{schema_name}.schema.yaml"
    return yamale.make_schema(schema_path)
  except FileNotFoundError as e:
    raise ValidationError([f"schema '{schema_name}' not found"]) from e


def scan_files(files: list[str]) -> list[tuple[str, str]]:
  errors: list[tuple[str, str]] = []
  for filename in files:
    try:
      schema_name = extract_schema_name(filename)
      if not schema_name:
        continue
      schema = load_schema(schema_name)
      data = yamale.make_data(filename)
      try:
        yamale.validate(schema, data)
      except yamale.yamale_error.YamaleError as e:
        error_strings = []
        for result in e.results:
          if result.isValid():
            continue
          if result.data:
            error_strings.append(f"in {result.data}:")
          for error in result.errors:
            error_strings.append(f"  {error}")
        raise ValidationError(error_strings) from e
    except ValidationError as e:
      for message in e.messages:
        errors.append((filename, message))
    except yaml.YAMLError as e:
      for error_line in str(e).splitlines():
        errors.append((filename, error_line))
    except FileNotFoundError as e:
      errors.append((filename, f"file not found: {e.filename}"))
  return errors


def main() -> int:
  errors = scan_files(sys.argv[1:])
  for filename, message in errors:
    print(f"{filename}: {message}")
  return 1 if errors else 0


if __name__ == "__main__":
  main()
