import struct

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # Search method def table or method headers in MethodDef (#~)
    # Let's inspect strings around 0x8045c or search backward for method header (e.g. 0x13 or 0x02 or 0x03)
    target = 0x8045c
    # In CIL, tiny header is 2 bits 0x02 | (code_size << 2) (1 byte)
    # Fat header is 0x03 0x30 ... (12 bytes)
    for off in range(target, target - 500, -1):
        # Fat header
        if data[off:off+2] == b"\x1b\x30" or data[off:off+2] == b"\x03\x30":
            size = struct.unpack("<I", data[off+4:off+8])[0]
            if off + 12 + size > target:
                print(f"Fat header at {hex(off)}, code size {size}")
                # RVA of this method is:
                # off to RVA
                # In text section (offset 0x200 to 0xecb00, RVA 0x2000)
                rva = off - 0x200 + 0x2000
                print(f"Method RVA: {hex(rva)}")

if __name__ == "__main__":
    main()
