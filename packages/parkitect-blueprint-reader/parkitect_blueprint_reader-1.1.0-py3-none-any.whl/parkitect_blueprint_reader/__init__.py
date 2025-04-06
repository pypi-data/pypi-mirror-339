from parkitect_blueprint_reader.__version__ import __version__
from typing import Dict, BinaryIO, Tuple
from bitstring import Bits, BitArray
from argparse import ArgumentParser
from hashlib import md5
from io import BytesIO
from math import floor
from sys import stdout
from PIL import Image
import json
import gzip


def _pixel_to_coords(img: Image, pixel: int) -> Tuple[int, int]:
    return (
        pixel % img.width,
        floor(pixel / img.height)
    )


def _pixels_to_bitarray(img: Image, start: int, length: int) -> BitArray:
    ret = BitArray()

    start *= 2
    length *= 2

    for pixel in range(start, start + length, 2):
        for p in (pixel + 1, pixel):
            for band in reversed(img.getpixel(_pixel_to_coords(img, p))):
                ret.append(
                    Bits(uint8=band)[-1:]
                )

    return ret


def load(fp: BinaryIO) -> Dict:
    with Image.open(fp, formats=('PNG',)) as img:
        magic_number = _pixels_to_bitarray(img, 0, 3)

        if magic_number.bytes != b'SM\x01':
            raise ValueError('This image is not a Parkitect blueprint')

        gzip_size = _pixels_to_bitarray(img, 3, 4).uintle

        checksum = _pixels_to_bitarray(img, 7, 16).bytes

        compressed = _pixels_to_bitarray(img, 23, gzip_size).bytes

    checksum_calculated = md5(compressed).digest()

    if checksum != checksum_calculated:
        raise ValueError(f'Checksum mismatch (stored: {checksum}; calculated: {checksum_calculated})')

    with BytesIO(gzip.decompress(compressed)) as decompressed:
        ret = {}

        for line in decompressed.readlines():
            json_line = json.loads(line.replace(b'.,', b'.0,').replace(b'.]', b'.0]').replace(b'.}', b'.0}'))
            json_line_cleaned = {
                key: value for key, value in json_line.items() if key not in ('@type', '@id')
            }

            type_ = json_line['@type']

            if type_ not in ret:
                ret[type_] = {}

            if type_ == 'BlueprintHeader':
                ret[type_] = json_line_cleaned
            else:
                id_ = json_line['@id']

                ret[type_][id_] = json_line_cleaned

        return ret


def cli() -> None:
    arg_parser = ArgumentParser(
        description='CLI tool to read Parkitect\'s blueprints metadata.'
    )

    arg_parser.add_argument(
        'filename',
        help='The blueprint file to read metadata from'
    )

    arg_parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'parkitect-blueprint-reader {__version__}'
    )

    arg_parser.add_argument(
        '-p', '--pretty',
        help='Pretty-print output',
        action='store_true'
    )

    args = arg_parser.parse_args()

    with open(args.filename, 'rb') as fp:
        json.dump(
            load(fp),
            stdout,
            indent=2 if args.pretty else None,
            separators=None if args.pretty else (',', ':')
        )


__all__ = ['load']
