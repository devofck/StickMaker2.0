import os


def get_converted_file(
        source_file: str,
        content_type='regular'
):

    new_name = source_file.split('.')[0] + '.webm'
    if content_type == 'video_note':
        os.system(
            f'ffmpeg -i {source_file} -vf colorkey=0xFBFBFB:0.1:0.1 -pix_fmt yuva420p {new_name}'
        )
        os.system(f"ffmpeg -y -i {new_name} -r 20 -an -c:v"
                  f" libvpx-vp9 -pix_fmt yuva420p"
                  f" -vf 'scale=512:512:force_original_aspect_ratio=decrease:'"
                  f" -t 2.50 -b:v 300K {new_name}")
    else:
        os.system(f"ffmpeg -y -i {source_file} -r 20 -an -c:v"
                  f" libvpx-vp9 -pix_fmt yuva420p"
                  f" -vf 'scale=512:512:force_original_aspect_ratio=decrease'"
                  f" -t 2.99 -b:v 400K {new_name}")
    os.remove(source_file)
    # os.system('clear')
    return new_name
