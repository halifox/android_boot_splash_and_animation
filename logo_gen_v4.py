import io
import os
import struct
import sys

from PIL import Image

SUPPORT_RLE24_COMPRESSION = 1


def GetImgHeader(size, compressed=0, real_bytes=0):
    """
    Generate header for the image file.
    """
    SECTOR_SIZE_IN_BYTES = 512
    header = bytearray(SECTOR_SIZE_IN_BYTES)

    width, height = size
    real_size = (real_bytes + 511) // 512

    # Magic
    header[:8] = b'SPLASH!!'

    # Width
    struct.pack_into("<I", header, 8, width)

    # Height
    struct.pack_into("<I", header, 12, height)

    # Compression flag
    struct.pack_into("<I", header, 16, compressed)

    # Block number
    struct.pack_into("<I", header, 20, real_size)

    return bytes(header)


def encode(line):
    count = 0
    lst = []
    repeat = -1
    run = []
    total = len(line) - 1
    for index, current in enumerate(line[:-1]):
        if current != line[index + 1]:
            run.append(current)
            count += 1
            if repeat == 1:
                entry = (count + 128, run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
                if index == total - 1:
                    run = [line[index + 1]]
                    entry = (1, run)
                    lst.append(entry)
            else:
                repeat = 0

                if count == 128:
                    entry = (128, run)
                    lst.append(entry)
                    count = 0
                    run = []
                    repeat = -1
                if index == total - 1:
                    run.append(line[index + 1])
                    entry = (count + 1, run)
                    lst.append(entry)
        else:
            if repeat == 0:
                entry = (count, run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
                if index == total - 1:
                    run.append(line[index + 1])
                    run.append(line[index + 1])
                    entry = (2 + 128, run)
                    lst.append(entry)
                    break
            run.append(current)
            repeat = 1
            count += 1
            if count == 128:
                entry = (256, run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
            if index == total - 1:
                if count == 0:
                    run = [line[index + 1]]
                    entry = (1, run)
                    lst.append(entry)
                else:
                    run.append(current)
                    entry = (count + 1 + 128, run)
                    lst.append(entry)
    return lst


def encodeRLE24(img):
    width, height = img.size
    output = io.BytesIO()

    for h in range(height):
        line = []
        result = []
        for w in range(width):
            (r, g, b) = img.getpixel((w, h))
            line.append((r << 16) + (g << 8) + b)
        result = encode(line)
        for count, pixel in result:
            output.write(struct.pack("B", count - 1))
            if count > 128:
                output.write(struct.pack("B", (pixel[0]) & 0xFF))
                output.write(struct.pack("B", ((pixel[0]) >> 8) & 0xFF))
                output.write(struct.pack("B", ((pixel[0]) >> 16) & 0xFF))
            else:
                for item in pixel:
                    output.write(struct.pack("B", (item) & 0xFF))
                    output.write(struct.pack("B", (item >> 8) & 0xFF))
                    output.write(struct.pack("B", (item >> 16) & 0xFF))
    content = output.getvalue()
    output.close()
    return content


def GetImageBody(img, compressed=0):
    """
    Get image body data.
    """
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
    elif img.mode == "RGB":
        background = img
    else:
        print("Unsupported image mode:", img.mode)
        sys.exit(1)

    if compressed == 1:
        return encodeRLE24(background)
    else:
        return background.tobytes()


def MakeLogoImage(input_file, output_file):
    """
    Convert PNG image to splash.img format.
    """
    img = Image.open(input_file)
    body_data = GetImageBody(img, SUPPORT_RLE24_COMPRESSION)
    header_data = GetImgHeader(img.size, SUPPORT_RLE24_COMPRESSION, len(body_data))
    with open(output_file, "wb") as f:
        f.seek(4096)  # Skip to 4096 bytes as per your original code
        f.write(header_data)
        f.write(body_data)


if __name__ == "__main__":
    input_file = "splash.png"
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    output_file = "out/splash.img"  # Adjust output file path as needed
    MakeLogoImage(input_file, output_file)
    print(f"Image conversion successful. Output file: {output_file}")
