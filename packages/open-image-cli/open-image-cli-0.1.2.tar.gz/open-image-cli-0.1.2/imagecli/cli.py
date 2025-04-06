# imagecli/cli.py

import click
from imagecli.image import ImageCli, ImageSize

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


if __name__ == '__main__':
    main()
