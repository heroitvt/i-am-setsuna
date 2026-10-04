def main():
    p = open(r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll", "rb").read()
    idx = 0
    while True:
        idx = p.find(b"SetsunaFontFix", idx)
        if idx == -1:
            break
        print(f"Found SetsunaFontFix at {idx}: {p[max(0, idx-40):min(len(p), idx+60)]}")
        idx += 14

if __name__ == "__main__":
    main()
