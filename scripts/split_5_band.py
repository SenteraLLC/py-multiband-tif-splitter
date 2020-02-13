# Imports
import os
import re
import io
import struct
import random
import argparse

from time import time

IMX265_IMAGE_OFFSETS = [0x00000000, 0x00484000, 0x00908000, 0x00d8c000, 0x01210000]
IMX265_IMAGE_SIZE = 23674880


def _shift_bytes(idx, single_band_bytes, offset, tag_num):
    single_band_bytes[(idx + 4) + (tag_num * 12) + 6:(idx + 4) + (tag_num * 12) + 10] = \
        struct.pack('i', struct.unpack('i', single_band_bytes[
                                            (idx + 4) + (tag_num * 12) + 6:(idx + 4) + (tag_num * 12) + 10])[
            0] - offset)


def _modify_group(idx, single_band_bytes, offset):
    # Get number of tags in group:
    num_tags = struct.unpack('h', single_band_bytes[idx:idx+2])[0]

    # Loop through tags and modify the byte offsets:
    for tag_num in range(num_tags):

        # Check if tag is the ExifIFD or GPS group offset:
        if (single_band_bytes[(tag_num*12) + (idx+2):(tag_num*12) + (idx+4)] == bytearray(b'i\x87')) \
                or (single_band_bytes[(tag_num*12) + (idx+2):(tag_num*12) + (idx+4)] == bytearray(b'%\x88')):

            _shift_bytes(idx, single_band_bytes, offset, tag_num)
            _modify_group(struct.unpack('i', single_band_bytes[
                                                              (tag_num*12) + (idx+2) + 8:
                                                              (tag_num*12) + (idx+2) + 12
                                                              ])[0],
                          single_band_bytes,
                          offset)

        # Check if tag is a pointer, and change offset if it is:
        elif (single_band_bytes[(idx+4)+(tag_num*12)] == 5) \
                or ((single_band_bytes[(idx+4)+(tag_num*12)] in [1, 2]) and (single_band_bytes[(idx+6)+(tag_num*12)] > 4))\
                or single_band_bytes[(tag_num * 12) + (idx + 2):(tag_num * 12) + (idx + 4)] == bytearray(b'\x11\x01'):
            _shift_bytes(idx, single_band_bytes, offset, tag_num)

        else:
            continue


def modify_exif_pointers(single_band_bytes, offset):

    # Write identical header for each page:
    single_band_bytes[:8] = bytearray(b'II*\x00\x08\x00\x00\x00')

    # First group is always directly after 8-byte header:
    _modify_group(8, single_band_bytes, offset)


def parse_xmp(xmp_data):

    band_names = re.findall("<Camera:BandName>\n(?: *|\t)<rdf:Seq>\n(?: *|\t)<rdf:li>([A-Za-z]+)", xmp_data)
    central_waves = re.findall("<Camera:CentralWavelength>\n(?: *|\t)<rdf:Seq>\n(?: *|\t)<rdf:li>([0-9]+)", xmp_data)
    wave_fwhms = re.findall("<Camera:WavelengthFWHM>\n(?: *|\t)<rdf:Seq>\n(?: *|\t)<rdf:li>([0-9]+)", xmp_data)

    # Make sure XMP matches conform
    if any(not xmp_type for xmp_type in [band_names, central_waves, wave_fwhms]):
        raise ValueError('Input TIF files do not appear to conform to Sentera specification. If this is an error, '
                         'contact Sentera support.')

    return [str(i) for i in range(5)], band_names, central_waves, wave_fwhms


def split_5band_tif(input_folder, output_folder, output_dtype, delete_originals=False):

    if not output_folder:
        output_folder = input_folder

    # Determine folder names from XMP:
    with open(os.path.join(input_folder, random.choice(os.listdir(input_folder))), 'r', encoding='mbcs') as xmp_data_file:
        xmp_data = xmp_data_file.read()
        imager_num, band_name, central_wave, wave_fwhm = parse_xmp(xmp_data)

    # Make directories:
    folder_names = []
    for folder_parts in zip(imager_num, band_name, central_wave, wave_fwhm):
        folder_name = "-".join(folder_parts)
        folder_names.append(folder_name)

        if not os.path.exists(os.path.join(output_folder, folder_name)):
            os.makedirs(os.path.join(output_folder, folder_name))
        elif os.path.exists(os.path.join(output_folder, folder_name)) and os.listdir(os.path.join(output_folder, folder_name)):
            raise PermissionError('Single band files already present in output directory. Exiting to avoid overwriting.')

    # Loop through all 5-band tifs in input folder:
    for multi_band_file in [file for file in os.listdir(input_folder) if file.lower().endswith('.tif')]:
        with open(os.path.join(input_folder, multi_band_file), 'rb') as multi_band:

            # Ensure input is 5-band Sentera file:
            multi_band_size = os.path.getsize(os.path.join(input_folder, multi_band_file))
            if multi_band_size != IMX265_IMAGE_SIZE:
                raise ValueError('Input TIF may not be 5-band, or may not be in Sentera multiband format. If this is '
                                 'an error, contact Sentera support.')

            single_bands_bytes = []
            for left_offset, right_offset in zip(IMX265_IMAGE_OFFSETS,
                                                 (IMX265_IMAGE_OFFSETS + [multi_band_size])[1:]):

                multi_band.seek(left_offset)
                single_band_bytes = bytearray(multi_band.read(right_offset - left_offset))

                modify_exif_pointers(single_band_bytes, left_offset)
                single_bands_bytes.append(single_band_bytes)

        if delete_originals:
            os.remove(os.path.join(input_folder, multi_band_file))

        for folder_name, single_band_file in zip(folder_names, single_bands_bytes):
            with open(os.path.join(output_folder, folder_name, "".join([multi_band_file.split('.')[0], "_", "_".join(folder_name.split('-')[2:]), '.tif'])), 'wb') as f:
                f.write(single_band_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group()
    optional = parser.add_argument_group()

    required.add_argument('--input_folder', required=True,
                          help='Path to folder of 5-band .tif files to be split into individual bands.')
    optional.add_argument('--output_folder',
                          help='Path to folder where the individual band images will be stored. Each band will be '
                               'stored in its own subfolder within the specified folder. Default location is within the'
                               ' specified input folder.')
    optional.add_argument('--output_dtype', choices=['uint16', 'float32', 'pack12'], default='pack12',
                          help='Data type of the output rasters. Options are unsigned 16-bit, 32-bit floating point, '
                               'and packed 12-bit. Defaults to packed 12-bit.')
    optional.add_argument('--delete_originals', action='store_true',
                          help="Deletes original 5-band images after splitting them. Useful to avoid bloating one's "
                               "hard drive.")

    args = parser.parse_args()

    start = time()
    split_5band_tif(**vars(args))
    print(f'Time to split all tifs in directory: {time() - start} sec.')