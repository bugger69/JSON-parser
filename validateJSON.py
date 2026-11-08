from pathlib import Path
import argparse

BrcStk = []
kvpStk = []
strStk = []
arrStk = []
cmbStk = []
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
                cmbStk.append(obj)
            else:
                if kvpStk[-1] != ':': return 0
                currObj = symbol(text[i])
                kvpStk.append(currObj)
                BrcStk.append('{')
                cmbStk.append(kvpStk[-1])
        elif text[i] in ['}', ',']:
            if len(BrcStk) == 0 or len(cmbStk) == 0: return 0
            if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                if len(kvpStk) > 0:
                    val = kvpStk[-1]
                    kvpStk.pop()
                    if kvpStk[-1] != ':': return 0
                    kvpStk.pop()
                    key = kvpStk[-1]
                    kvpStk.pop()
                    if len(kvpStk) == 0 or len(BrcStk) == 1:
                        obj[key] = val
                    else:
                        kvpStk[-1][key] = val
            elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                val = arrStk[-1]
                arrStk.pop()
            if text[i] == '}': 
                if latest != ',':
                    BrcStk.pop(0)
                    cmbStk.pop(0)
                else: return 0
        elif text[i] == '[':
            if kvpStk[-1] != ':': return 0
            arr = symbol(text[i])
            kvpStk.append(arr)
            cmbStk.append(kvpStk[-1])
        elif text[i] == ']':
            for val in arrStk:
                cmbStk[-1].append(val)
            cmbStk.pop()
        elif text[i] == '\"':
            if len(BrcStk) == 0 or obj == 0: return 0
            if len(strStk) == 0:
                strn = symbol(text[i])
                isStr = True
                if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                    kvpStk.append(strn)
                elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                    arrStk.append(strn)
                strStk.append('\"')
            else:
                isStr = False
                strStk.pop()
        elif text[i] == ':':
            if len(kvpStk) == 0: return 0
            if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                kvpStk.append(text[i])
            elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                arrStk.append(text[i])
        elif text[i].isdigit() or text[i].isalpha():
            if isStr == False:
                if len(kvpStk) > 0 and kvpStk[-1] != ':':
                    print(": not present")
                    return 0
                var = ''
                j = i
                while text[j] not in [',', '}', ' ']:
                    var += text[j]
                    j = j + 1
                sym = symbol(var)
                if sym is INVALID_SYMBOL: 
                    print("Invalid Symbol")
                    return 0
                if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                    kvpStk.append(sym)
                elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                    arrStk.append(sym)
                i = i + len(var) - 1
            else:
                if len(kvpStk[-1]) == 0 and text[i].isdigit(): return 0
                if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict) and not isinstance(kvpStk[-1], str) : return 0
                if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                    kvpStk[-1] += text[i]
                elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                    arrStk[-1] += text[i]
        else:
            if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                if len(kvpStk) > 0 and kvpStk[-1] != ':' and isStr == True:
                    if len(cmbStk) > 0 and isinstance(cmbStk[-1], dict):
                        kvpStk[-1] += text[i]
                    elif len(cmbStk) > 0 and isinstance(cmbStk[-1], list):
                        arrStk[-1] += text[i]
        latest = text[i]
        print(kvpStk)
        print(arrStk)
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