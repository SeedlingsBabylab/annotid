import os.path
import csv
import add_annotation_ID_audio as audio
import add_annotation_id_video as video

CHA_PATH='/home/sarp/work/BergelsonLab/annotated_cha/annotated_cha'
OPF_PATH='/home/sarp/work/BergelsonLab/annotated_opf/annotated_opf'


def run_annotid_script(ddict):
    for annotid, lst in ddict.items():
        print('Processing {}'.format(annotid))
        for f in lst:
            pth = os.path.join(CHA_PATH, f)
            audio.process_file(pth, pth)


def parse_name(row):
    if row['audio_video'] == 'audio':
        return row['id'].replace('.csv', '.cha').replace('audio_', '')
    elif row['audio_video'] == 'video':
        return row['id'].replace('.csv', '').replace('video_', '')

with open('final_duplicates.csv') as inf:
    duplicates = csv.DictReader(inf)
    ddict = {}
    for row in duplicates:
        if row['annotid'] in ddict:
            ddict[row['annotid']].append(parse_name(row))
        else:
            ddict[row['annotid']] = [parse_name(row)]

    run_annotid_script(ddict)

        

