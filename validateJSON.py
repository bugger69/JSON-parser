from pathlib import Path
import argparse

BrcStk = []
kvpStk = []
strStk = []
INVALID_SYMBOL = object()

def is_integer_string(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def symbol(sym):
    if sym == "{":
        return {}
    elif sym == "[":
        return []
    elif sym == "\"":
        return ""
    elif sym == "true":
        return True
    elif sym == "false":
        return False
    elif sym == "null":
        return None
    elif is_integer_string(sym):
        return int(sym)
    else:
        return INVALID_SYMBOL


def parseJSON(text):
    obj = 0
    isStr = False
    latest = ''
    i = 0
    if len(text) == 0 or text[0] != '{':
        return 0
    while i < len(text):
        print(text[i])
        if text[i] == '{':
            if obj == 0:
                obj = symbol(text[i])
                BrcStk.append('{')
        elif text[i] in ['}', ',']:
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
            if text[i] == '}': 
                if latest != ',': BrcStk.pop(0)
                else: return 0
        elif text[i] == '\"':
            if len(BrcStk) == 0 or obj == 0: return 0
            if len(strStk) == 0:
                strn = symbol(text[i])
                isStr = True
                kvpStk.append(strn)
                strStk.append('\"')
            else:
                isStr = False
                strStk.pop()
        elif text[i] == ':':
            if len(kvpStk) == 0: return 0
            kvpStk.append(text[i])
        elif text[i].isdigit() or text[i].isalpha():
            if isStr == False:
                if kvpStk[-1] != ':': return 0
                var = ''
                j = i
                while text[j] not in [',', '}', ' ']:
                    var += text[j]
                    j = j + 1
                sym = symbol(var)
                if sym is INVALID_SYMBOL: return 0
                kvpStk.append(sym)
                i = i + len(var)
            else:
                if len(kvpStk[-1]) == 0 and text[i].isdigit(): return 0
                if not isinstance(kvpStk[-1], str) : return 0
                kvpStk[-1] += text[i]
        latest = text[i]
        print(kvpStk)
        i = i + 1

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