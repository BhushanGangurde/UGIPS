#!/usr/bin/env python3

import argparse
import json
import os
import sys
from jsonschema import validate, Draft7Validator, exceptions as jsonschema_exceptions

def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON file: {path}\n   {e}")
        sys.exit(1)

def validate_prompt(prompt_file, schema_file):
    prompt_data = load_json_file(prompt_file)
    schema_data = load_json_file(schema_file)

    try:
        validator = Draft7Validator(schema_data)
        errors = sorted(validator.iter_errors(prompt_data), key=lambda e: e.path)
        if errors:
            print(f"❌ Prompt file '{prompt_file}' failed validation against UGIPS schema:\n")
            for err in errors:
                path = ".".join(str(x) for x in err.path)
                print(f" - [path: {path}] {err.message}")
            print("\n⚠️ Validation completed with errors.")
            sys.exit(1)
        else:
            print(f"✅ '{prompt_file}' is valid UGIPS format.")
    except jsonschema_exceptions.SchemaError as e:
        print(f"❌ Invalid UGIPS schema: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="UGIPS Prompt Validator – Validate your prompts against the UGIPS schema."
    )
    parser.add_argument(
        "--file", "-f", required=True,
        help="Path to UGIPS prompt file (e.g., examples/sample.ugips.json)"
    )
    parser.add_argument(
        "--schema", "-s", default=os.path.join("..", "schema", "ugips-schema.json"),
        help="Path to UGIPS schema file (default: ../schema/ugips-schema.json)"
    )

    args = parser.parse_args()
    validate_prompt(args.file, args.schema)

if __name__ == "__main__":
    main()

