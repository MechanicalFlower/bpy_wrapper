import argparse

import ffmpeg  # type: ignore


def generate_palette(srcdir: str, filename: str) -> None:
    """Generate a palette image from the input images."""
    raw_input_pattern = f"{srcdir}/render/{filename}/raw/%04d.png"
    palette_output = f"{srcdir}/render/{filename}/palette.png"

    input_stream = ffmpeg.input(raw_input_pattern)
    palette_filter = ffmpeg.filter(input_stream, 'palettegen', reserve_transparent=1)
    palette_output_stream = ffmpeg.output(palette_filter, palette_output)
    ffmpeg.run(palette_output_stream)


def scale_and_crop(srcdir: str, filename: str) -> None:
    """Scale and crop the input images."""
    raw_input_pattern = f"{srcdir}/render/{filename}/raw/%04d.png"
    cropped_output_pattern = f"{srcdir}/render/{filename}/cropped/%04d.png"

    input_stream = ffmpeg.input(raw_input_pattern)
    scale_filter = ffmpeg.filter(input_stream, 'scale', w="if(gt(iw,ih),-1,360)", h="if(gt(iw,ih),360,-1)")
    crop_filter = ffmpeg.filter(scale_filter, 'crop', w=360, h=360, exact=1)
    cropped_output_stream = ffmpeg.output(crop_filter, cropped_output_pattern)
    ffmpeg.run(cropped_output_stream)


def generate_gif(srcdir: str, filename: str) -> None:
    """Generate a GIF animation using cropped images and a palette."""
    cropped_input_pattern = f"{srcdir}/render/{filename}/cropped/%04d.png"
    palette_input = f"{srcdir}/render/{filename}/palette.png"
    gif_output = f"{srcdir}/render/{filename}.gif"

    input_stream = ffmpeg.input(cropped_input_pattern, framerate=30)
    palette_input_stream = ffmpeg.input(palette_input)
    gif_filter = ffmpeg.filter([input_stream, palette_input_stream], filter_name="paletteuse", alpha_threshold=128)
    gif_output_stream = ffmpeg.output(gif_filter, gif_output, gifflags="+offsetting")
    ffmpeg.run(gif_output_stream)


def main() -> None:
    """Main function to process arguments and execute the pipeline."""
    parser = argparse.ArgumentParser(description="Generate a GIF animation using FFmpeg.")
    parser.add_argument("--srcdir", required=True, help="Source directory")
    parser.add_argument("--filename", required=True, help="Base filename")

    args = parser.parse_args()

    generate_palette(args.srcdir, args.filename)
    scale_and_crop(args.srcdir, args.filename)
    generate_gif(args.srcdir, args.filename)


if __name__ == "__main__":
    main()
