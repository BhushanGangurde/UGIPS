#!/usr/bin/env python3

import argparse
import json
import os
import sys
from jinja2 import Template

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        sys.exit(1)

def render_prompt(template_str, variables):
    try:
        template = Template(template_str)
        return template.render(**variables)
    except Exception as e:
        print(f"❌ Failed to render prompt: {e}")
        sys.exit(1)

def convert_to_openai(prompt_file, output_file=None):
    prompt_json = load_json(prompt_file)

    system_msg = prompt_json.get("context", "You are a helpful assistant.")
    template_str = prompt_json["prompt_template"]
    examples = prompt_json.get("examples", [])

    messages_list = []

    for example in examples:
        input_data = { "input": example["input"] }
        rendered_prompt = render_prompt(template_str, input_data)
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": rendered_prompt}
        ]
        messages_list.append({
            "messages": messages,
            "expected_output": example["output"]
        })

    if output_file:
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(messages_list, out, indent=2)
        print(f"✅ OpenAI message format saved to: {output_file}")
    else:
        print(json.dumps(messages_list, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Convert UGIPS prompt to OpenAI-compatible message format.")
    parser.add_argument(
        "--file", "-f", required=True,
        help="Path to .ugips.json prompt file"
    )
    parser.add_argument(
        "--output", "-o", required=False,
        help="Output file to write OpenAI format JSON (optional)"
    )
    args = parser.parse_args()
    convert_to_openai(args.file, args.output)

if __name__ == "__main__":
    main()
