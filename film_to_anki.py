# Author: Alexander Ivashkin

import subprocess
import sys


def main():
    """Split film into Anki pieces by calling ffmpeg from the shell"""

    # check command line for original file and track list file
    if len(sys.argv) != 3:
        print ('usage: {0} <film> <orig.ass> <eng.ass>'.format(sys.argv[0]))
        exit(1)

    # record command line args
    flnm_film = sys.argv[1]
    flnm_origass = sys.argv[2]
    flnm_engass = sys.argv[3]

    # create a template of the ffmpeg call in advance
    cmd_string_audio = 'ffmpeg -y -i "{tr}" -acodec copy -ss {st} -to {en} /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    #cmd_string_image = 'ffmpeg -y -i "{tr}" -ss {st} -to {en} -pix_fmt rgb8 -r 1 /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    cmd_string_im_1 =  'ffmpeg -y -ss {st} -to {en} -i "{tr}" -vf fps=2,scale=320:-1:flags=lanczos,palettegen pallete.png'
    cmd_string_im_2 = 'ffmpeg -y -ss {st} -to {en} -i "{tr}" -i pallete.png -filter_complex "fps=2,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    command_im_cleanup = 'rm pallete.png'

    # read each line of the track list and split into start, end, name
    with open(track_list, 'r') as f:
        for line in f:
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue

            # create command string for a given track
            orig, trans, start, end, sound, image = line.strip().split(';')
            command_au = cmd_string_audio.format(tr=original_track, st=start, en=end, nm=sound)
            command_im_1 = cmd_string_im_1.format(tr=original_track, st=start, en=end, nm=image)
            command_im_2 = cmd_string_im_2.format(tr=original_track, st=start, en=end, nm=image)

            # use subprocess to execute the command in the shell
            subprocess.call(command_au, shell=True)
            subprocess.call(command_im_1, shell=True)
            subprocess.call(command_im_2, shell=True)

    # Remove the palette.png
    subprocess.call(command_im_cleanup, shell=True)

    return None


if __name__ == '__main__':
    main()
