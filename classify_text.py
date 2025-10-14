"""
# classify_sequences.py
import re
import sys
import argparse
from pathlib import Path

def classify_seq(s):
    found = False
    if re.search(r'\d', s):
        print("there are numbers in the seq"); found = True
    if re.search(r'\s', s):
        print("there are spaces in the seq"); found = True
    if re.search(r'[A-Z]', s):
        print("there are upper letters"); found = True
    if re.search(r'[a-z]', s):
        print("there are lower letters"); found = True
    if not found:
        print("none types are found")

def main():
    ap = argparse.ArgumentParser(
        description="Report which character classes occur in a string."
    )
    ap.add_argument('text', nargs="?", help="Input string (if omitted, read from stdin)")
    ap.add_argument('-f', '--file', type=Path, help="Read input from a file")
    args = ap.parse_args()
    # 1. 从文件读取
    if args.file:
        if not args.file.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        text = args.file.read_text(encoding="utf-8")
    # 2. 命令行直接给出文本
    elif args.text is not None:
        text = args.text
    # 3. 从 stdin 读取
    else:
        try:
            text = input("please enter the sequence: ")
        except EOFError:
            print("❌ no valid input")
            sys.exit(1)

    classify_seq(text)

if __name__ == "__main__":
    main()
