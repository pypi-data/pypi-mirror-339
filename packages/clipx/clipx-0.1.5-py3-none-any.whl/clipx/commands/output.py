import click
import os
from pathlib import Path


def add_output_options(command):
    """
    Add output-related options to command
    """
    command = click.option(
        '-o', '--output',
        type=click.Path(file_okay=True, dir_okay=True, writable=True),
        help='Output image or folder. Default: [input_name]_remove.[ext]'
    )(command)

    return command


def get_output_path(input_path, output_path=None, suffix="_remove"):
    input_path = Path(input_path)

    if output_path is None:
        # Generate output path with suffix
        stem = input_path.stem
        ext = input_path.suffix
        return str(input_path.with_name(f"{stem}{suffix}{ext}"))

    output_path = Path(output_path)

    if output_path.exists() and output_path.is_dir():
        # Output path is a directory, use input filename
        stem = input_path.stem
        ext = input_path.suffix
        return str(output_path / f"{stem}{suffix}{ext}")

    # Output path is a file, use as is
    return str(output_path)