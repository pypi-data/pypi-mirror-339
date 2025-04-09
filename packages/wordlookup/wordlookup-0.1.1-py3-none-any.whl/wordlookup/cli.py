import argparse
import json
import os
import sys
import textwrap

import httpx


def fetch_word_data(word: str) -> list:
    """Fetches word data from the dictionary API"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        return None
    except json.JSONDecodeError as exc:
        print(f"Error decoding JSON for '{word}': {exc}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def main():
    """Fetches and prints definitions for a given word"""
    parser = argparse.ArgumentParser(description="Fetch definitions for a word.")
    parser.add_argument("word", type=str, help="The word to look up.")
    args = parser.parse_args()
    word = args.word

    data = fetch_word_data(word)
    if data:
        print(f"Definitions for '{word}':")
        try:
            terminal_width = os.get_terminal_size().columns - 4  # 4 for padding
        except OSError:
            terminal_width = 80  # default if terminal size can't be determined

        for entry in data:
            for meaning in entry.get("meanings", []):
                part_of_speech = meaning.get("partOfSpeech")
                definitions = meaning.get("definitions", [])
                if part_of_speech and definitions:
                    print(f"\n{part_of_speech}:")
                    for definition_data in definitions:
                        definition = definition_data.get("definition")
                        if definition:
                            wrapped_lines = textwrap.wrap(
                                definition, width=terminal_width, subsequent_indent=""
                            )
                            for i, line in enumerate(wrapped_lines):
                                if i == 0:
                                    print(f"- {line}")
                                else:
                                    print(f"  {line}")
    else:
        print(f"Could not retrieve definition for '{word}'.")


if __name__ == "__main__":
    sys.exit(main())