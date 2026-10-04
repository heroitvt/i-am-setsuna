import re

def get_strings(data):
    # ASCII
    s1 = set(re.findall(b"[\x20-\x7e]{5,}", data))
    # UTF-16LE
    s2 = set(re.findall(b"(?:[\x20-\x7e]\x00){5,}", data))
    return {s.decode('ascii', errors='ignore') for s in s1} | {s.decode('utf-16le', errors='ignore') for s in s2}

def main():
    p1 = open(r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll", "rb").read()
    p2 = open(r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll.bak", "rb").read()

    s1 = get_strings(p1)
    s2 = get_strings(p2)

    only_in_p1 = s1 - s2
    only_in_p2 = s2 - s1

    print(f"Only in Assembly-CSharp.dll (modified): {len(only_in_p1)}")
    for s in sorted(only_in_p1)[:30]:
        print("  +", repr(s))

    print(f"Only in Assembly-CSharp.dll.bak (original): {len(only_in_p2)}")
    for s in sorted(only_in_p2)[:30]:
        print("  -", repr(s))

if __name__ == "__main__":
    main()
