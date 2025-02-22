import functools
import re
import sys
from typing import Optional

import yamale


class ValidationError(Exception):
  messages: list[str]

  def __init__(self, messages: list[str]):
    self.messages = messages

def extract_schema_name(filename) -> Optional[str]:
  with open(filename) as f:
    first_line = f.readline()
    match = re.match('# (no )?schema: (.+)', first_line)
    if not match:
      raise ValidationError([
          "no schema name found",
          "add a '# schema: <name>' declaration in the first line"])
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

def main() -> int:
  had_errors = False
  for filename in sys.argv[1:]:
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
        print(f"{filename}: {message}")
      had_errors = True
  return 1 if had_errors else 0

if __name__ == "__main__":
  main()
