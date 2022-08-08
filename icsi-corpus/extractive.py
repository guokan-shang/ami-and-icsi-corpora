import os
import json
import utils

paths = utils.get_paths('plus')

file_name_list = [f for f in os.listdir(paths['extractive']) if f.endswith('.extsumm.xml')]

for file_name in file_name_list:
    meeting_id = utils.get_meeting_id(file_name)

    # load dialogueActs
    dialogueActs = {}
    dialogueAct_json = json.load(open('output/dialogueActs/' + meeting_id + '.json'))
    for dialogueAct in dialogueAct_json:
        dialogueActs[dialogueAct['id']] = dialogueAct

    # load extractive
    extractive = []
    extractive_xml = utils.xml_to_dict(
        paths['extractive'] + meeting_id + '.extsumm.xml'
    )
    for ext in extractive_xml['nite:root']['extsumm']['nite:child']:
        if '..' in ext['@href']:
            start, end = ext['@href'].split('#')[1].split('..')
            start = start.split('(')[1].split(')')[0]
            end = end.split('(')[1].split(')')[0]
            assert start.split('.')[0:-1] == end.split('.')[0:-1]

            for i in range(int(start.split('dialogueact')[-1]), int(end.split('dialogueact')[-1]) + 1):
                da_id = '.'.join(start.split('.')[0:-1]) + '.dialogueact' + str(i)
                try:
                    extractive.append(dialogueActs[da_id])
                except:
                    print('missing dialogue act', da_id)
        else:
            da_id = ext['@href'].split('#')[1].split('(')[1].split(')')[0]
            extractive.append(dialogueActs[da_id])


    output_dir = 'output/extractive/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(extractive, f)

