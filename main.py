import argparse
from pathlib import Path
from process import process

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input', help='input file')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-t', '--templates', default='templates', help='templates directory')
    parser.add_argument('-r', '--renderers', default='renderers', help='renderers directory')
    parser.add_argument('-e', '--extensions', default='.htm,.html', help='extensions to parse')

    args = parser.parse_args()
    extensions = args.extensions.split(',')

    process(Path(args.input), Path(args.output), Path(args.templates), Path(args.renderers), extensions)
