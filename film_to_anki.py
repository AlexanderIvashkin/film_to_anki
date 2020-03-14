# Author: Alexander Ivashkin

import subprocess
import sys

class InvalidTimestamp(ValueError):
    """Timestamp must be in the H:M:S.SS format"""

def main():
    """Split film into Anki pieces by calling ffmpeg from the shell"""

    # check command line for original file and track list file
    if len(sys.argv) != 5:
        print ('usage: {0} <film> <orig.ass> <eng.ass> <anki.csv>'.format(sys.argv[0]))
        exit(1)

    # record command line args
    flnm_film = sys.argv[1]
    flnm_origass = sys.argv[2]
    flnm_engass = sys.argv[3]
    flnm_ankicsv = sys.argv[4]

    # create a template of the ffmpeg call in advance
    #cmd_string_audio = 'ffmpeg -y -i "{tr}" -acodec copy -ss {st} -to {en} /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    cmd_string_audio = 'ffmpeg -y -i "{film}" -map 0:2 -acodec copy -ss {start} -to {end} "{flnm_output}"'
    #cmd_string_image = 'ffmpeg -y -i "{tr}" -ss {st} -to {en} -pix_fmt rgb8 -r 1 /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    #cmd_string_im_1 =  'ffmpeg -y -ss {st} -to {en} -i "{tr}" -vf fps=2,scale=320:-1:flags=lanczos,palettegen pallete.png'
    #cmd_string_im_2 = 'ffmpeg -y -ss {st} -to {en} -i "{tr}" -i pallete.png -filter_complex "fps=2,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" /Users/AlexanderIvashkin/Library/Application\ Support/Anki2/User\ 1/collection.media/"{nm}"'
    #command_im_cleanup = 'rm pallete.png'


    engass = parse_ass(flnm_engass)
    origass = parse_ass(flnm_origass)
    #print(engass)
    #print()
    finalass = []
    for sub in engass:
        for origsub in origass:
            # Less than a second of disparity between English sub and original language sub
            if abs(sub[0] - origsub[0]) < 1:
                finalass += [(origsub[0]-0.5, origsub[1]+0.5, sub[2].replace('\\N', '<br>'), origsub[2].replace('\\N', '<br>'))]

    with open(flnm_ankicsv, 'w') as ankicsv:
        # CSV header
        ankicsv.write('Original,Translation,Sound,Image,Source\n')
        for anki in finalass:
            csv_anki = ''
            flnm_audio = str(anki[0]) + '.ac3'
            flnm_image = str(anki[0]) + '.gif'
            #command_audio = cmd_string_audio.format(film=flnm_film, start=anki[0], end=anki[1],flnm_output=flnm_film + '_' + flnm_audio
            #print(command_audio)
            #subprocess.call(command_audio, shell=True)
            csv_anki += '"' + anki[2] + '","' + anki[3] + '","' + flnm_audio + '","' + flnm_image + '"'
            ankicsv.write(csv_anki + '\n')



#    # create command string for a given track
#    orig, trans, start, end, sound, image = line.strip().split(';')
#    command_au = cmd_string_audio.format(tr=original_track, st=start, en=end, nm=sound)
#    command_im_1 = cmd_string_im_1.format(tr=original_track, st=start, en=end, nm=image)
#    command_im_2 = cmd_string_im_2.format(tr=original_track, st=start, en=end, nm=image)
#
#    # use subprocess to execute the command in the shell
#    subprocess.call(command_au, shell=True)
#    subprocess.call(command_im_1, shell=True)
#    subprocess.call(command_im_2, shell=True)
#
#    # Remove the palette.png
#    subprocess.call(command_im_cleanup, shell=True)

def parse_ass(flnm):
    """Read .ass subtitle and parse [Events]"""

    with open(flnm, 'r') as f:
        is_events = False
        is_events_fmt = False
        dic_fmt = {}
        fullsub = []
        for line in f:
            # skip comments and empty lines
            if line.startswith(';') or len(line) <= 1:
                continue
            # look for [Events]
            if not is_events:
                if line.strip() == '[Events]':
                    line = next(f)
                    for i, fld in enumerate(line.split(',')):
                        dic_fmt[fld.strip()] = i
                    is_events = True
                    continue

            # We're inside [Events]
            else:
                if line.strip()[0] == '[':
                    is_events = False
                    continue
                sub_strt = line.split(',')[dic_fmt['Start']].strip()
                sub_strt = timestamp_to_secs(sub_strt)
                sub_end = line.split(',')[dic_fmt['End']].strip()
                sub_end = timestamp_to_secs(sub_end)
                sub_text = line.split(',')[dic_fmt['Text']].strip()
                fullsub = fullsub + [(sub_strt, sub_end, sub_text)]

    return fullsub


def timestamp_to_secs(timestamp):
    """Convert a H:M:S.SS timestamp into decimal seconds (S.SS)"""
    time = timestamp.split(':')
    if len(time) != 3:
        raise InvalidTimestamp
    return sum(list(map(lambda tt, mm: float(tt)*mm, time, [3600, 60, 1])))



if __name__ == '__main__':
    main()
