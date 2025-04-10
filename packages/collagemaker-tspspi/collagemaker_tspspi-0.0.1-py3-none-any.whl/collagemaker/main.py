import argparse
import random
from PIL import Image, ImageColor

def parse_color(value):
    if value.lower() == "transparent":
        return (0, 0, 0, 0)
    try:
        rgba = ImageColor.getcolor(value, "RGBA")
        return rgba
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid color value: {value}")

def create_collage(
    image_paths,
    output_path,
    num_lines=2,
    image_size=(400, 400),
    padding=60,
    rotation_range=8,
    background=(0, 0, 0, 0),
    overlap=0.5,
    line_overlap=0.1
):
    # Load images and resize into desired format
    images = [Image.open(path).convert("RGBA") for path in image_paths]
    resized_images = [img.resize(image_size) for img in images]

    # Calculate how many images per line and how many on last line ...
    images_per_line = len(images) // num_lines
    remainder = len(images) % num_lines

    lines = []
    idx = 0
    for i in range(num_lines):
        count = images_per_line + (1 if i < remainder else 0)
        lines.append(resized_images[idx:idx+count])
        idx += count

    # Calculate x and y axis steps ...
    horizontal_step = int(image_size[0] * (1 - overlap))
    vertical_step = int(image_size[1] * (1 - line_overlap))

    # Maximum line width as well as image dimensions
    max_line_width = max(len(line) * horizontal_step for line in lines)
    collage_width = max_line_width + padding * 2
    collage_height = vertical_step * num_lines + padding * 2

    # Output image ...
    collage = Image.new("RGBA", (collage_width, collage_height), background)

    # Rotate and paste images
    for line_idx, line_imgs in enumerate(lines):
        y = padding + line_idx * vertical_step
        available_width = collage_width - padding * 2
        total_width = len(line_imgs) * horizontal_step
        x = padding + (available_width - total_width) // 2

        for img in line_imgs:
            angle = random.uniform(-rotation_range, rotation_range)
            rotated = img.rotate(angle, expand=True)
            collage.paste(rotated, (x, y), rotated)
            x += horizontal_step

    # Store collage
    collage.save(output_path, "PNG")

def main():
    parser = argparse.ArgumentParser(description="Create a flowing image collage with overlap and rotation.")
    parser.add_argument("images", nargs="+", help="Input image files")
    parser.add_argument("--output", type=str, required=True, help="Output file")
    parser.add_argument("--lines", type=int, default=2, help="Number of lines (default: 2)")
    parser.add_argument("--bgcolor", type=parse_color, default=(0, 0, 0, 0), help="Background color (CSS name or #RRGGBB[AA], default: transparent)")
    parser.add_argument("--overlap", type=float, default=0.3, help="Fractional horizontal overlap between images (default: 0.3)")
    parser.add_argument("--lineoverlap", type=float, default=0.1, help="Fractional vertical overlap between lines (default: 0.1)")

    args = parser.parse_args()
    create_collage(args.images, args.output, num_lines=args.lines, background=args.bgcolor, overlap=args.overlap, line_overlap=args.lineoverlap)

if __name__ == "__main__":
    main()

