import os

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # In .NET PE files, find user strings or search UTF-16LE strings
    import re
    # UTF-16LE strings of length >= 3
    pattern = re.compile(b'(?:[\x20-\x7e]\x00){3,}')
    strings = []
    for m in pattern.finditer(data):
        try:
            s = m.group().decode('utf-16le')
            if any(k in s.lower() for k in ["cpk", "parameter", "scenariomessage", "setsuna", "streaming"]):
                strings.append(s)
        except:
            pass

    print(f"Total matching UTF-16LE strings: {len(strings)}")
    for s in sorted(set(strings))[:50]:
        print("  ", repr(s))

if __name__ == "__main__":
    main()
