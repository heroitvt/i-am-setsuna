import os
import re

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()
    
    # search for strings containing parameter or cpk
    matches = re.findall(b"[\x20-\x7e]{3,}", data)
    relevant = []
    for m in matches:
        s = m.decode('ascii', errors='ignore')
        if any(w in s.lower() for w in ["parameter", "cpk", "scenariomessage", "cri", "streamingassets"]):
            relevant.append(s)
            
    print(f"Total relevant strings: {len(relevant)}")
    for s in sorted(set(relevant))[:50]:
        print("  ", s)

if __name__ == "__main__":
    main()
