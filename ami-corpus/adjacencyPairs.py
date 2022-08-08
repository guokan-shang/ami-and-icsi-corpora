import os
import json
import utils

paths = utils.get_paths('manual')

file_name_list = [f for f in os.listdir(paths['dialogueActs']) if f.endswith('.adjacency-pairs.xml')]

for file_name in file_name_list:
    meeting_id = utils.get_meeting_id(file_name)

    # load dialogueActs
    dialogueActs = {}
    dialogueAct_json = json.load(open('output/dialogueActs/' + meeting_id + '.json'))
    for dialogueAct in dialogueAct_json:
        dialogueActs[dialogueAct['id']] = dialogueAct

    # load ap_type.xml
    ap_types = {}
    ap_types_xml = utils.xml_to_dict(
        paths['ontologies-ap-types']
    )
    for ap_type in ap_types_xml['ap-type']['ap-type']:
        ap_types[ap_type['@nite:id']] = ap_type

    # load adjacency-pairs.xml
    adjacencyPairs = []
    adjacencyPairs_xml = utils.xml_to_dict(
        paths['dialogueActs'] + file_name,
        force_list=('nite:pointer',)
    )

    for adjacencyPair in adjacencyPairs_xml['nite:root']['adjacency-pair']:
        id = adjacencyPair['@nite:id']
        ap_type_name = 'None'
        ap_type_gloss = 'None'
        source = 'None'
        target = 'None'

        found_type = False
        found_source = False
        found_target = False

        for item in adjacencyPair['nite:pointer']:
            if item['@role'] == 'type':
                # 'ap-types.xml#id(apt_1)'
                ap_type_id = item['@href'].split('#')[1].split('(')[1].split(')')[0]
                ap_type_name = ap_types[ap_type_id]['@name']
                ap_type_gloss = ap_types[ap_type_id]['@gloss']
                found_type = True
            elif item['@role'] == 'source':
                # 'TS3005c.A.dialog-act.xml#id(TS3005c.A.dialog-act.vkaraisk.16)')
                dialogueAct_id = item['@href'].split('#')[1].split('(')[1].split(')')[0]
                source = dialogueActs[dialogueAct_id]
                found_source = True
            elif item['@role'] == 'target':
                dialogueAct_id = item['@href'].split('#')[1].split('(')[1].split(')')[0]
                target = dialogueActs[dialogueAct_id]
                found_target = True
            else:
                raise RuntimeError()

        if not found_type:
            print('missing <ap-type>:', id)
        if not found_source:
            print('missing <source>:', id)
        if not found_target:
            print('missing <target>:', id)

        adjacencyPairs.append({
            'id': id,
            'type': ap_type_name,
            'source': source,
            'target': target
        })

    output_dir = 'output/adjacencyPairs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(adjacencyPairs, f)

