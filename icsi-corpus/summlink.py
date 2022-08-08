import os
import json
import utils
from collections import OrderedDict

paths = utils.get_paths('plus')

file_name_list = [f for f in os.listdir(paths['extractive']) if f.endswith('.summlink.xml')]

for file_name in file_name_list:
    meeting_id = utils.get_meeting_id(file_name)

    # load dialogueActs
    dialogueActs = {}
    dialogueAct_json = json.load(open('output/dialogueActs/' + meeting_id + '.json'))
    for dialogueAct in dialogueAct_json:
        dialogueActs[dialogueAct['id']] = dialogueAct

    # load abstractive
    abstractive = OrderedDict()
    abstractive_xml = utils.xml_to_dict(
        paths['abstractive'] + meeting_id + '.abssumm.xml',
        force_list=('sentence',)
    )
    for type in ['abstract', 'decisions', 'problems', 'progress']:
        if 'sentence' not in abstractive_xml['nite:root'][type].keys():
            print(str(meeting_id) + ": Missing " + type + " sentence")
            continue

        for abstractive_sentence in abstractive_xml['nite:root'][type]['sentence']:
            abstractive_sentence_id = abstractive_sentence['@nite:id']
            abstractive_sentence_text = abstractive_sentence['#text']

            abstractive[abstractive_sentence_id] = {
                'id': abstractive_sentence_id,
                'text': abstractive_sentence_text,
                'type': type
            }

    # load summlink
    summlinks = {}
    summlink_xml = utils.xml_to_dict(
        paths['extractive'] + file_name,
        force_list=()
    )

    for summlink in summlink_xml['nite:root']['summlink']:
        id = summlink['@nite:id']

        if summlink['nite:pointer'][0]['@role']=='extractive' and summlink['nite:pointer'][1]['@role']=='abstractive':
            extractive_id = summlink['nite:pointer'][0]['@href'].split('#')[1].split('(')[1].split(')')[0]
            abstractive_id = summlink['nite:pointer'][1]['@href'].split('#')[1].split('(')[1].split(')')[0]

            try:
                summlinks[abstractive_id].append(dialogueActs[extractive_id])
            except:
                summlinks[abstractive_id] = [dialogueActs[extractive_id]]
        else:
            raise RuntimeError()

    summlinks_output = []

    for abstractive_id in sorted(summlinks.keys(), key = lambda x: int(x.split('.')[-1])):
        summlinks_output.append({
            'abstractive': abstractive[abstractive_id],
            'extractive': summlinks[abstractive_id]
        })

    output_dir = 'output/summlink/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(summlinks_output, f)

