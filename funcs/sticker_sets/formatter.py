import os


def get_converted_file(
        source_file: str
):

    new_name = source_file.split('.')[0] + '.webm'

    os.system(f"ffmpeg -y -i {source_file} -r 20 -an -c:v"
              f" libvpx-vp9 -pix_fmt yuva420p"
              f" -vf 'scale=512:512:force_original_aspect_ratio=decrease'"
              f" -t 2.99 -b:v 400K {new_name}")
    os.remove(source_file)
    os.system('clear')
    return new_name
