import struct
import os
from parse_utf_proper import parse_utf_table

def main():
    cpk_orig = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk"
    param_dir = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter"
    output_cpk = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.new"

    with open(cpk_orig, "rb") as f:
        header_bytes = f.read(20480) # read up to ContentOffset (20480)
        
    toc_rows = parse_utf_table(header_bytes, 2064)
    print(f"Loaded {len(toc_rows)} TOC rows.")
    
    # In TOC, rows start at rows_offset = 67, each row is 24 bytes:
    # FileName (4), FileSize (4), ExtractSize (4), FileOffset (8), ID (4)
    # Let's inspect the raw TOC @UTF block:
    # It starts at offset 2064 in header_bytes.
    toc_table_size = struct.unpack(">I", header_bytes[2064+4:2064+8])[0]
    print("TOC table size:", toc_table_size)
    toc_raw = bytearray(header_bytes[2064+8:2064+8+toc_table_size])
    
    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", toc_raw[:24])
    print(f"TOC raw: rows_offset={rows_offset}, row_len={row_length}, num_rows={num_rows}")
    
    # Let's verify each row in toc_raw
    new_data = bytearray()
    curr_offset = 0 # relative to ContentOffset (20480)
    
    for r in range(num_rows):
        r_pos = rows_offset + r * row_length
        # FileName offset into strings_offset
        str_off = struct.unpack(">I", toc_raw[r_pos:r_pos+4])[0]
        # read name from strings
        c = strings_offset + str_off
        end = toc_raw.find(b"\x00", c)
        fname = toc_raw[c:end].decode('ascii')
        
        # Read file from param_dir
        fpath = os.path.join(param_dir, fname)
        with open(fpath, "rb") as f:
            fdata = f.read()
            
        fsize = len(fdata)
        
        # Align curr_offset to 2048
        pad_len = (2048 - (curr_offset % 2048)) % 2048
        if pad_len > 0:
            new_data.extend(b"\x00" * pad_len)
            curr_offset += pad_len
            
        file_offset = curr_offset
        new_data.extend(fdata)
        curr_offset += fsize
        
        # Update row in toc_raw:
        # FileSize (uint32 at r_pos+4)
        # ExtractSize (uint32 at r_pos+8)
        # FileOffset (uint64 at r_pos+12)
        struct.pack_into(">IIQ", toc_raw, r_pos+4, fsize, fsize, file_offset)
        
    print(f"All files packed. Content size: {len(new_data)} bytes.")
    
    # Rebuild header_bytes
    new_header = bytearray(header_bytes)
    # Replace TOC table data
    new_header[2064+8:2064+8+toc_table_size] = toc_raw
    
    # Update CPK header at offset 16:
    # In CPK header (@UTF at 16):
    # ContentSize is at rows_offset + 0 * row_len + col_offset
    # Let's inspect CPK header columns
    cpk_h_size = struct.unpack(">I", new_header[16+4:16+8])[0]
    cpk_h_raw = bytearray(new_header[16+8:16+8+cpk_h_size])
    h_rows_off, h_str_off, h_data_off, h_tbl_name, h_num_fields, h_row_len, h_num_rows = struct.unpack(">IIIIHHI", cpk_h_raw[:24])
    print(f"CPK Header raw: rows_off={h_rows_off}, row_len={h_row_len}")
    
    # In CPK header, ContentSize is uint64 at row offset
    # Let's find ContentSize column index
    # We know from parse_utf_proper:
    # UpdateDateTime (U64), FileSize (ZERO), ContentOffset (U64), ContentSize (U64)...
    # Let's update ContentSize
    # ContentOffset is at h_rows_off + 8 (U64)
    # ContentSize is at h_rows_off + 16 (U64)
    struct.pack_into(">Q", cpk_h_raw, h_rows_off + 16, len(new_data))
    new_header[16+8:16+8+cpk_h_size] = cpk_h_raw
    
    # Total CPK = new_header + new_data
    with open(output_cpk, "wb") as f:
        f.write(new_header)
        f.write(new_data)
        
    print(f"Successfully created {output_cpk}, total size: {os.path.getsize(output_cpk)} bytes!")

if __name__ == "__main__":
    main()
