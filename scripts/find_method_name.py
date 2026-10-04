import struct

def main():
    dll = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\Managed\Assembly-CSharp.dll"
    with open(dll, "rb") as f:
        data = f.read()

    # We know #~ stream is at 969636 (0xecbb4)
    tilde = data[969636:969636+570728]
    strings = data[1540364:1540364+228996]
    
    # In #~ stream:
    # 4 bytes reserved
    # 1 byte major, 1 byte minor
    # 1 byte heap sizes
    # 1 byte reserved
    # 8 bytes valid (bitmask of present tables)
    # 8 bytes sorted
    valid = struct.unpack("<Q", tilde[8:16])[0]
    
    # Counts of rows for each present table
    cur = 24
    row_counts = {}
    for t in range(64):
        if (valid >> t) & 1:
            cnt = struct.unpack("<I", tilde[cur:cur+4])[0]
            row_counts[t] = cnt
            cur += 4
            
    print("MethodDef row count:", row_counts.get(6)) # table 6 is MethodDef
    print("TypeDef row count:", row_counts.get(2))   # table 2 is TypeDef

    # Find size of each table before MethodDef (0: Module, 1: TypeRef, 2: TypeDef, 3: FieldPtr, 4: Field, 5: MethodPtr)
    # Let's see: String index size is (tilde[6] & 1) ? 4 : 2
    str_idx_size = 4 if (tilde[6] & 1) else 2
    guid_idx_size = 4 if (tilde[6] & 2) else 2
    blob_idx_size = 4 if (tilde[6] & 4) else 2
    
    # MethodDef row size: RVA (4) + ImplFlags (2) + Flags (2) + Name (str_idx_size) + Signature (blob_idx_size) + ParamList (2 or 4)
    param_idx_size = 4 if row_counts.get(8, 0) >= 65536 else 2
    method_row_size = 4 + 2 + 2 + str_idx_size + blob_idx_size + param_idx_size
    
    # Calculate offset of table 6
    # Calculate sizes of tables 0 to 5
    # Table 0: Module: 2 + str_idx + guid_idx * 3
    # Table 1: TypeRef: ResolutionScope (2 or 4) + str_idx + str_idx
    # Table 2: TypeDef: 4 + str_idx + str_idx + Extends (2 or 4) + FieldList + MethodList
    # Table 4: Field: 2 + str_idx + blob_idx
    # Let's just search for target RVA in the table
    target_rva = 0x8045c + 0x2000 - 0x200 # approx 0x8225c
    print(f"Target approx RVA: {hex(target_rva)}")
    
    # Let's search for RVA in range [0x80000, 0x85000] in tilde table
    for off in range(cur, len(tilde) - 10, method_row_size):
        rva = struct.unpack("<I", tilde[off:off+4])[0]
        if 0x80000 <= rva <= 0x83000:
            name_off = struct.unpack("<I" if str_idx_size == 4 else "<H", tilde[off+8:off+8+str_idx_size])[0]
            name = ""
            c = name_off
            while strings[c] != 0:
                name += chr(strings[c])
                c += 1
            print(f"Found method: {name} with RVA {hex(rva)} at tilde offset {off}")

if __name__ == "__main__":
    main()
