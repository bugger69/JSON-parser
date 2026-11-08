from pathlib import Path
import argparse

BrcStk = []

def symbol(sym):
    if sym == "{":
        return {}
    if sym == "[":
        return []


def parseJSON(str):
    obj = 0
    if len(str) == 0 or str[0] != '{':
        return 0
    for s in str:
        if s == '{':
            if obj == 0:
                obj = symbol(s)
                BrcStk.append('{')
        elif s == '}':
            if len(BrcStk) == 0: return 0
            BrcStk.pop(0)

    return obj

def main(filepath):
    path = Path(filepath)
    if path.suffix == ".json":
        txt = path.read_text(encoding="utf-8")
        if parseJSON(txt) != 0:
            print("valid")
        else:
            print("invalid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    main(args.filepath)