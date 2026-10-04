import os
import struct

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search for how parameter files are loaded.
    # In earlier search we saw:
    # LoadCpkCoroutine
    # LoadFileFromCpkCoroutine
    # LoadResourceParameter
    # BindCpk
    # Let's search for "LoadFileFromCpkCoroutine" or strings related to parameter loading.
    import re
    matches = re.findall(b"[a-zA-Z0-9_/\\.]{4,}", data)
    relevant = set()
    for m in matches:
        try:
            s = m.decode('ascii')
            if any(k in s.lower() for k in ["parameter", "cpk", "scenariomessage"]):
                relevant.add(s)
        except:
            pass
    print("Relevant strings count:", len(relevant))
    for s in sorted(relevant)[:40]:
        print(" ", s)

if __name__ == "__main__":
    main()
