import sys
from clipx.utils import ClipxError


def version_command():
    from clipx import __version__
    print(f"clipx version {__version__}")
    return 0


def help_command():
    help_text = """
Usage: clipx [OPTIONS]

Options:
  -i, --input FILE/FOLDER   Input image or folder. [required]
  -o, --output FILE/FOLDER  Output image or folder. 
  -m, --model MODEL         Model to use: u2net, cascadepsp, auto (default).
  -k, --only-mask           Output only mask image.
  -u, --use-mask FILE       Use an existing mask image.
  -v, --version             Show version information.
  -h, --help                Show this help message.
  --fast                    Use fast mode for CascadePSP (less accurate but faster).

Example usage:
  clipx -i input.jpg -o output.png
  clipx -m u2net -i input.jpg -o mask.png -k
"""
    print(help_text)
    return 0


def main():
    if len(sys.argv) == 2:
        command = sys.argv[1]

        if command in ('-v', '--version'):
            return version_command()

        if command in ('-h', '--help'):
            return help_command()

    try:
        from clipx.commands.parser import create_cli_parser
        from clipx.core import process_command

        clipx_cli = create_cli_parser()
        options = clipx_cli()

        if options:
            process_command(options)

    except SystemExit:
        pass
    except ClipxError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())