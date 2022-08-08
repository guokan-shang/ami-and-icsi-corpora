import os
import json
import utils

paths = utils.get_paths('manual')

file_name_list = [f for f in os.listdir(paths['abstractive']) if f.endswith('.abssumm.xml')]

for file_name in file_name_list:
    meeting_id = utils.get_meeting_id(file_name)

    # load abstractive
    abstractive = []
    abstractive_xml = utils.xml_to_dict(
        paths['abstractive'] + meeting_id + '.abssumm.xml',
        force_list=('sentence',)
    )
    for type in ['abstract', 'actions', 'decisions', 'problems']:
        if 'sentence' not in abstractive_xml['nite:root'][type].keys():
            print(str(meeting_id) + ": Missing " + type + " sentence")
            continue

        for abstractive_sentence in abstractive_xml['nite:root'][type]['sentence']:
            abstractive_sentence_id = abstractive_sentence['@nite:id']
            abstractive_sentence_text = abstractive_sentence['#text']

            abstractive.append({
                'id': abstractive_sentence_id,
                'text': abstractive_sentence_text,
                'type': type
            })

    output_dir = 'output/abstractive/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(abstractive, f)

