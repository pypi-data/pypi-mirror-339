# imagecli/cli.py
import json
import click
from typing import List
from imagecli.image import ImageCli, ImageSize
from imagecli.siticher import ImageStitcher
from imagecli.macocr import MacOCR
from imagecli.element import OCRElement

@click.group()
def main():
    """ImageCLI: A tool for image processing through CLI and Python package.""" 
    pass

@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True))
def size(file):
    """Show the size of the image."""
    size: ImageSize = ImageCli(file).size
    click.echo(f"Image Pixels Size: {size.width}x{size.height}")


@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True))
@click.option('-u', '--unit', default='bytes', type=click.Choice(['bytes', 'KB', 'MB', 'GB'], case_sensitive=False))
def file_size(file, unit):
    """Show the size of the file."""
    image_cli = ImageCli(file)
    formatted_size = image_cli.get_formatted_size(unit)
    click.echo(f"Image File Size: {formatted_size}")


@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Path to the image file.')
@click.option('-t', '--target_size', required=True, type=float, help='Target size for the compressed image.')
@click.option('-u', '--unit', default='MB', type=click.Choice(['bytes', 'KB', 'MB', 'GB'], case_sensitive=False), help='Unit for target size. Default is MB.')
def compress(file, target_size, unit):
    """Compress the image to a target file size."""
    image_cli = ImageCli(file)
    compressed_image_path = image_cli.compress_image(target_size=target_size, unit=unit)
    click.echo(f"Compressed image saved to: {compressed_image_path}")
    compressed_size = ImageCli(compressed_image_path).get_formatted_size(unit)
    click.echo(f"Compressed Image Size: {compressed_size}")

@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Path to the image file.')
@click.option('-c', '--color', default='BLUE', type=click.Choice(['BLUE', 'WHITE', 'RED'], case_sensitive=False), help='Background color to change to. Default is BLUE.')
def background(file, color):
    """Modify the image background color."""""
    image_cli = ImageCli(file)
    modified_image_path = image_cli.change_photo_backgroundcolor(color)
    click.echo(f"Modified image background `{color.lower()}` saved to: {modified_image_path}")


@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Path to the image file.')
@click.option('-d', '--direction', required=True, type=click.Choice(['LEFT', 'RIGHT'], case_sensitive=False), help='Direction to rotate the image.')
@click.option('-a', '--angle', required=True, type=int, help='Angle in degrees to rotate the image.')
def turn(file, direction, angle):
    """Compress the image to a target file size."""
    image_cli = ImageCli(file)
    modified_image_path = image_cli.turn(direction=direction, angle=angle)
    click.echo(f"Turn file {direction} {angle} degrees, saved to: {modified_image_path}")

@main.command()
@click.option('-i', '--input-paths', required=True, multiple=True, type=click.Path(exists=True),
              help='Paths to the image files to be stitched. Provide each path separately with `-i`.')
@click.option('-o', '--output-path', required=True, type=click.Path(),
              help='Path where the stitched image will be saved.')
@click.option('--padding-width', default=80, type=int,
              help='Width of padding to be added around images. Default is 80.')
@click.option('--remove-padding/--keep-padding', default=False,
              help='Specify whether to remove the padding from the final result.')
def merge(input_paths, output_path, padding_width, remove_padding):
    """Stitch images together using specified parameters."""
    print(f'input_paths: {input_paths}, output_path: {output_path}, padding_width: {padding_width}, remove_padding: {remove_padding}')
    
    stitcher = ImageStitcher(input_paths, padding_width)
    try:
        merged_image_path = stitcher.stitch_images(output_path, True)
        click.echo(f"Merged image saved to: {merged_image_path}")
    except IOError as e:
        click.echo(f"Error during stitching: {e}", err=True)


@main.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True), help='Image ocr result.')
def ocr(file):
    """Image ocr result."""
    macocr = MacOCR()
    ocr_elements: List[OCRElement] = macocr.ocr(file)
    click.echo(json.dumps([OCRElement.to_dict(element) for element in ocr_elements], indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
