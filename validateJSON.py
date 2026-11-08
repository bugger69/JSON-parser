from pathlib import Path
import argparse

BrcStk = []
kvpStk = []
strStk = []

def symbol(sym):
    if sym == "{":
        return {}
    if sym == "[":
        return []
    if sym == "\"":
        return ""


def parseJSON(text):
    obj = 0
    isStr = False
    latest = 0
    if len(text) == 0 or text[0] != '{':
        return 0
    for s in text:
        # print(s)
        if s == '{':
            if obj == 0:
                obj = symbol(s)
                BrcStk.append('{')
        elif s in ['}', ',']:
            if len(BrcStk) == 0: return 0
            if len(kvpStk) > 0:
                val = kvpStk[-1]
                kvpStk.pop()
                if kvpStk[-1] != ':': return 0
                kvpStk.pop()
                key = kvpStk[-1]
                kvpStk.pop()
                if len(kvpStk) == 0 or len(BrcStk) == 1:
                    obj[key] = val
            if s == '}': 
                if latest != ',': BrcStk.pop(0)
                else: return 0
        elif s == '\"':
            if len(BrcStk) == 0 or obj == 0: return 0
            if len(strStk) == 0:
                strn = symbol(s)
                isStr = True
                kvpStk.append(strn)
                strStk.append('\"')
            else:
                isStr = False
                strStk.pop()
        elif s == ':':
            if len(kvpStk) == 0: return 0
            kvpStk.append(s)
        elif s.isdigit() or s.isalpha():
            if isStr == False: return 0
            if len(kvpStk[-1]) == 0 and s.isdigit(): return 0
            if not isinstance(kvpStk[-1], str) : return 0
            kvpStk[-1] += s
        latest = s
        print(kvpStk)

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