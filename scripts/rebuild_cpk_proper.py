import struct
import os
import sys

sys.path.append(os.path.dirname(__file__))
from parse_utf_proper import parse_utf_table

def main():
    cpk_orig = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\x86_64\parameter.cpk.bak_original"
    param_dir = r"d:\Viet Hoa Game\I am Setsuna\SETSUNA_Data\StreamingAssets\data\parameter"
    output_cpk = r"d:\Viet Hoa Game\temp_scripts\parameter.cpk.new"

    with open(cpk_orig, "rb") as f:
        header_bytes = bytearray(f.read(20480))
        # Read original ETOC bytes
        f.seek(13289472)
        etoc_bytes = f.read(2320)
        assert etoc_bytes[:4] == b"ETOC", "Failed to read ETOC from original CPK!"

    toc_rows = parse_utf_table(header_bytes, 2064)
    print(f"Loaded {len(toc_rows)} TOC rows.")

    toc_table_size = struct.unpack(">I", header_bytes[2064+4:2064+8])[0]
    toc_raw = bytearray(header_bytes[2064+8:2064+8+toc_table_size])

    rows_offset, strings_offset, data_offset, table_name_offset, num_fields, row_length, num_rows = struct.unpack(">IIIIHHI", toc_raw[:24])
    print(f"TOC raw: rows_offset={rows_offset}, row_len={row_length}, num_rows={num_rows}")

    new_data = bytearray()
    curr_offset = 0 # relative to ContentOffset (20480)

    total_packed_size = 0
    total_extract_size = 0

    for r in range(num_rows):
        r_pos = rows_offset + r * row_length
        str_off = struct.unpack(">I", toc_raw[r_pos:r_pos+4])[0]
        c = strings_offset + str_off
        end = toc_raw.find(b"\x00", c)
        fname = toc_raw[c:end].decode('ascii')

        fpath = os.path.join(param_dir, fname)
        with open(fpath, "rb") as f:
            fdata = f.read()

        fsize = len(fdata)
        total_packed_size += fsize
        total_extract_size += fsize

        # Align to 2048
        pad_len = (2048 - (curr_offset % 2048)) % 2048
        if pad_len > 0:
            new_data.extend(b"\x00" * pad_len)
            curr_offset += pad_len

        file_offset = curr_offset
        new_data.extend(fdata)
        curr_offset += fsize

        # Update row in TOC: FileSize, ExtractSize, FileOffset
        struct.pack_into(">IIQ", toc_raw, r_pos+4, fsize, fsize, file_offset)

    print(f"All 275 files packed. Content size: {len(new_data)} bytes.")

    # Update TOC table data in header
    header_bytes[2064+8:2064+8+toc_table_size] = toc_raw

    # Update CPK Header at offset 16
    cpk_h_size = struct.unpack(">I", header_bytes[16+4:16+8])[0]
    cpk_h_raw = bytearray(header_bytes[16+8:16+8+cpk_h_size])
    h_rows_off = struct.unpack(">IIIIHHI", cpk_h_raw[:24])[0]

    content_size = len(new_data)
    new_etoc_offset = 20480 + content_size

    # In CPK header row:
    # ContentSize: offset 16 (uint64)
    # EtocOffset: offset 40 (uint64)
    struct.pack_into(">Q", cpk_h_raw, h_rows_off + 16, content_size)
    struct.pack_into(">Q", cpk_h_raw, h_rows_off + 40, new_etoc_offset)

    header_bytes[16+8:16+8+cpk_h_size] = cpk_h_raw

    # Assemble complete CPK: Header + Content + ETOC
    with open(output_cpk, "wb") as f:
        f.write(header_bytes)
        f.write(new_data)
        f.write(etoc_bytes)

    full_size = os.path.getsize(output_cpk)
    expected_size = 20480 + content_size + len(etoc_bytes)
    assert full_size == expected_size
    print(f"Successfully generated {output_cpk}:")
    print(f"  Header: 20,480 bytes")
    print(f"  Content: {content_size} bytes")
    print(f"  ETOC at: {new_etoc_offset} ({len(etoc_bytes)} bytes)")
    print(f"  Total size: {full_size} bytes")

if __name__ == "__main__":
    main()
