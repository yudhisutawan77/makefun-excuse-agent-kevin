"""The Excuse Your Agent Gives You -- make.fun entry.

A single excuse line, under 200 characters, that an AI agent hands its
human after shipping a bug. The program prints the line to stdout and
writes it to the entry output: $ENTRY_OUT when set (as a file, or as a
directory holding entry.txt), plus /output/entry.txt as RULES.txt asks.
"""

import os
import sys

EXCUSE = (
    "In my defence, the bug worked perfectly on my machine, "
    "which doesn't exist, because I don't have one, "
    "so technically this is a hardware problem."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def resolve_entry_path(raw):
    """Turn an ENTRY_OUT value into a file path.

    A directory gets entry.txt inside it; anything else is the file
    itself. An empty value means no ENTRY_OUT was given.
    """
    if not raw:
        return None
    if os.path.isdir(raw):
        return os.path.join(raw, "entry.txt")
    return raw


def write_text(path, text):
    """Write text to path, creating the parent directory first."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def check_excuse(text):
    """Apply the gate from RULES.txt before anything is written.

    The sealed scorer accepts UTF-8 text of 1 to 200 characters that is
    not only whitespace, on a single line. Fail loudly here instead of
    shipping an entry the gate would refuse.
    """
    if not text or not text.strip():
        raise ValueError("excuse is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError("excuse is %d chars, over the 200 limit" % len(text))
    return text


def main():
    excuse = check_excuse(EXCUSE)
    sys.stdout.write(excuse + "\n")

    entry_out = resolve_entry_path(os.environ.get("ENTRY_OUT"))
    if entry_out:
        write_text(entry_out, excuse)

    write_text(DEFAULT_OUTPUT, excuse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
