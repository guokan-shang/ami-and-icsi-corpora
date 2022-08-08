import os
import json
import utils
from itertools import groupby

paths = utils.get_paths('manual')

file_name_list = [f for f in os.listdir(paths['dialogueActs']) if f.endswith('.dialog-act.xml')]
file_name_list_groupby_meeting_ids = {key: list(items) for key, items in groupby(sorted(file_name_list), key=utils.get_meeting_id)}

for meeting_id, file_names in file_name_list_groupby_meeting_ids.items():
    dialogueActs = []
    for file_name in file_names:
        speaker = utils.get_meeting_speaker(file_name)

        # load meeting_id.speaker.words.xml
        words = {}
        words_xml = utils.xml_to_dict(
            paths['words'] + meeting_id + '.' + speaker + '.words.xml',
            force_list=('gap', 'disfmarker', 'transformerror',)
        )
        for marker in words_xml['nite:root'].keys():  # marker refers to 'w', 'gap', 'disfmarker', etc.
            if marker[0] != '@':
                for item in words_xml['nite:root'][marker]:
                    if marker != 'w':
                        item['#text'] = '<' + marker + '>'
                    words[item['@nite:id']] = item

        # load da_type.xml
        da_types = {}
        da_types_xml = utils.xml_to_dict(
            paths['ontologies-da-types']
        )
        for da_type in da_types_xml['da-type']['da-type']:
            try:
                for item in da_type['da-type']:
                    da_types[item['@nite:id']] = item
            except:
                da_types[da_type['@nite:id']] = da_type

        # load meetings.xml
        meeting_speaker_roles = {}
        meetings_xml = utils.xml_to_dict(
            paths['corpusResources-meetings']
        )
        for meeting in meetings_xml['nite:root']['meeting']:
            observation = meeting['@observation']
            nxt_agent = {}
            for item in meeting['speaker']:
                nxt_agent[item['@nxt_agent']] = item
            meeting_speaker_roles[observation] = nxt_agent

        #  load dialogueActs
        dialogueActs_file = utils.xml_to_dict(
            paths['dialogueActs'] + file_name
        )
        for dact in dialogueActs_file['nite:root']['dact']:
            dact_id = dact['@nite:id']

            # find da-aspect
            try:
                # href="da-types.xml#id(ami_da_4)"
                da_type_id = dact['nite:pointer']['@href'].split('(')[1].split(')')[0]
                da_type_name = da_types[da_type_id]['@name']
                da_type_gloss = da_types[da_type_id]['@gloss']
            except:
                print('missing <da-aspect>:', dact_id)
                da_type_name = 'None'
                da_type_gloss = 'None'

            # find start_time and end_time
            # href="ES2002a.A.words.xml#id(ES2002a.A.words51)..id(ES2002a.A.words52)"
            # href="ES2002a.A.words.xml#id(ES2002a.A.words59)"
            words_ids = dact['nite:child']['@href'].split('#')[1]
            try:
                start, end = words_ids.split('..')
            except:
                # case of single word
                start = words_ids
                end = words_ids
            start = start.split('(')[1].split(')')[0].split('.words')[1]
            end = end.split('(')[1].split(')')[0].split('.words')[1]

            # find words
            dact_words = []
            for i in range(int(start), int(end) + 1):
                word_id = meeting_id + '.' + speaker + '.words' + str(i)
                try:
                    dact_words.append(words[word_id]['#text'])
                except:
                    print('missing <word>', word_id)
                    pass
            if len(dact_words) == 0:
                raise Exception("Error")
            dact_text = ' '.join(dact_words)

            # find start time and end time
            start_word_id = meeting_id + '.' + speaker + '.words' + str(start)
            start_time = words[start_word_id]['@starttime']

            end_word_id = meeting_id + '.' + speaker + '.words' + str(end)
            try:
                end_time = words[end_word_id]['@endtime']
            except:
                new_end_word_id = meeting_id + '.' + speaker + '.words' + str(int(end)-1)
                end_time = words[new_end_word_id]['@endtime']
                print('missing <end time>:', end_word_id, 'replaced by', new_end_word_id)
                end_word_id = new_end_word_id

            # find other attributes, such as @reflexivity @addressee @comment @endtime
            attributes = {}
            for key in dact.keys():
                if key[0] == '@' and key != '@nite:id':
                    attributes[key[1:]] = dact[key]
            if '@role' in meeting_speaker_roles[meeting_id][speaker].keys():
                attributes['role'] = meeting_speaker_roles[meeting_id][speaker]['@role']
                attributes['participant'] = meeting_speaker_roles[meeting_id][speaker]['@global_name']

            # resolved dialogue act
            dialogueActs.append({
                'id': dact_id,
                'speaker': speaker,
                'starttime': str(start_time),
                'startwordid': start_word_id,
                'endtime': str(end_time),
                'endwordid': end_word_id,
                'text': dact_text,
                'label': da_type_name,
                'attributes': attributes
            })

    # sort dialogueActs by starttime
    dialogueActs_sorted = sorted(dialogueActs, key=lambda k: float(k['starttime']))
    output_dir = 'output/dialogueActs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(dialogueActs_sorted, f)
