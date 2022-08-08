import os
import json
import utils
from itertools import groupby
import xml.etree.ElementTree as ET

paths = utils.get_paths('plus')

file_name_list = [f for f in os.listdir(paths['dialogueActs']) if f.endswith('.dialogue-acts.xml')]
file_name_list_groupby_meeting_ids = {key: list(items) for key, items in groupby(sorted(file_name_list), key=utils.get_meeting_id)}

# load speakers.xml
meeting_speaker_roles = {}
speakers_xml = utils.xml_to_dict(
    paths['speakers']
)
for speaker in speakers_xml['nite:root']['speaker']:
    speaker_tag = speaker['@tag']
    try:
        speaker_education = speaker['education']['#text']
    except:
        print('missing speaker education:', speaker_tag)
        speaker_education = 'None'
    meeting_speaker_roles[speaker_tag] = speaker_education


for meeting_id, file_names in file_name_list_groupby_meeting_ids.items():
    dialogueActs = []
    for file_name in file_names:
        speaker = utils.get_meeting_speaker(file_name)

        # load meeting_id.speaker.words.xml
        words = {}
        words_xml = utils.xml_to_dict(
            paths['words'] + meeting_id + '.' + speaker + '.words.xml',
            force_list=('vocalsound', 'nonvocalsound', 'disfmarker', 'pause', 'comment',)
        )
        for marker in words_xml['nite:root'].keys():  # marker refers to 'w', 'gap', 'disfmarker', etc.
            if marker[0] != '@':
                for item in words_xml['nite:root'][marker]:
                    if marker != 'w':
                        item['#text'] = '<' + marker + '>'
                    words[item['@nite:id']] = item

        # get word orderings
        word_id_list = []
        for elt in ET.parse(paths['words'] + meeting_id + '.' + speaker + '.words.xml').iter():
            word_id_list.append(elt.get('{http://nite.sourceforge.net/}id'))
        

        #  load dialogueActs
        dialogueActs_file = utils.xml_to_dict(
            paths['dialogueActs'] + file_name,
            force_list=('dialogueact',)
        )
        for dact in dialogueActs_file['nite:root']['dialogueact']:
            dact_id = dact['@nite:id']

            # find da-label
            da_original_label = dact['@original-type']
            try:
                da_label = dact['@type']
            except:
                print('missing da-type for', dact_id)
                da_label = da_original_label
            # if da_label != da_original_label:
            #     print(da_label,da_original_label)

            # find start_time and end_time
            start_time = dact['@starttime']
            end_time = dact['@endtime']

            # find startwordid and endwordid
            # href="ES2002a.A.words.xml#id(ES2002a.A.words51)..id(ES2002a.A.words52)"
            # href="ES2002a.A.words.xml#id(ES2002a.A.words59)"
            try:
                words_ids = dact['nite:child']['@href'].split('#')[1]
            except:
                print('missing text for dialogue act', dact_id)
                continue

            try:
                start, end = words_ids.split('..')
            except:
                # case of single word
                start = words_ids
                end = words_ids
            start_word_id = start.split('(')[1].split(')')[0]
            end_word_id = end.split('(')[1].split(')')[0]
            # print(start_word_id, end_word_id)

            # find words
            dact_words = []
            for word_id in word_id_list[word_id_list.index(start_word_id): word_id_list.index(end_word_id)+1]:
                try:
                    dact_words.append(words[word_id]['#text'])
                except:
                    print('missing <word>', word_id)
                    pass
            if len(dact_words) == 0:
                raise Exception("Error")
            dact_text = ' '.join(dact_words)
            #print(dact_text)

            # find other attributes
            attributes = {}
            attributes['role'] = meeting_speaker_roles[dact['@participant']]
            attributes['participant'] = dact['@participant']
            try:
                attributes['adjacency'] = dact['@adjacency']
            except:
                pass
                # attributes['adjacency'] = 'None'
            attributes['channel'] = dact['@channel']

            # resolved dialogue act
            dialogueActs.append({
                'id': dact_id,
                'speaker': speaker,
                'starttime': str(start_time),
                'startwordid': start_word_id,
                'endtime': str(end_time),
                'endwordid': end_word_id,
                'text': dact_text,
                'label': da_label,
                'original_label': da_original_label,
                'attributes': attributes
            })

    # sort dialogueActs by starttime
    dialogueActs_sorted = sorted(dialogueActs, key=lambda k: float(k['starttime']))
    output_dir = 'output/dialogueActs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(dialogueActs_sorted, f)
