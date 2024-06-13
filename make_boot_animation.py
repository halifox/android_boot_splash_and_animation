import os
import zipfile

from PIL import Image


def make_boot_animation():
    """
    Convert an image into an Android boot animation zip file.
    """

    # Define the image file name
    logo = "bootanimation.png"

    # Open the image and get width and height
    image = Image.open(logo)
    width, height = image.size

    # Define the output directories
    output_dir = "out/bootanimation"
    part0_dir = os.path.join(output_dir, "part0")
    part1_dir = os.path.join(output_dir, "part1")

    # Create necessary directories (ignore if they already exist)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(part0_dir, exist_ok=True)
    os.makedirs(part1_dir, exist_ok=True)

    # Create description file and write content
    desc_file = os.path.join(output_dir, "desc.txt")
    with open(desc_file, "w") as f:
        f.write(f"{width} {height} 30\n")
        f.write("p 1 0 part0\n")
        f.write("p 0 0 part1\n")

    # Copy image to animation parts
    target_paths = [
        (logo, os.path.join(part0_dir, "00001.png")),
        (logo, os.path.join(part1_dir, "00001.png"))
    ]

    for src, dst in target_paths:
        with open(src, 'rb') as f_in, open(dst, 'wb') as f_out:
            f_out.write(f_in.read())

    # Create the zip file with no compression
    zip_file = "out/bootanimation.zip"
    with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_STORED) as zip_ref:
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.png') or file == 'desc.txt':
                    file_path = os.path.join(root, file)
                    zip_ref.write(file_path, arcname=os.path.relpath(file_path, output_dir))

    print(f"Boot animation created successfully: {zip_file}")


if __name__ == '__main__':
    make_boot_animation()
