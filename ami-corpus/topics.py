import os
import json
import utils

def run(topic):
    id = topic['@nite:id']
    default_topic_type_name = 'None'
    other_description = 'None'

    try:
        topic_type_id = topic['nite:pointer']['@href'].split('#')[1].split('(')[1].split(')')[0]
        default_topic_type_name = default_topic_types[topic_type_id]
    except:
        print('missing <default topic>', id)

    if 'other_description' in topic:
        other_description = topic['other_description']

    dialogueacts = []
    try:
        for item in topic['nite:child']:
            # href=IS1002d.A.words.xml#id(IS1002d.A.words150)..id(IS1002d.A.words162)
            # href=IS1002d.B.words.xml#id(IS1002d.B.words536)
            words_ids = item['@href'].split('#')[1]
            try:
                start, end = words_ids.split('..')
            except:
                # case of single word
                start = words_ids
                end = words_ids
            words_start = int(start.split('(')[1].split(')')[0].split('.words')[1])
            words_end = int(end.split('(')[1].split(')')[0].split('.words')[1])
            words_meetingid_spearker = start.split('(')[1].split(')')[0].split('.words')[0]
            # from start and end word id to find corresponding dialougue acts
            for dialogueAct in list(dialogueActs.values()):
                da_start = int(dialogueAct['startwordid'].split('.words')[1])
                da_end = int(dialogueAct['endwordid'].split('.words')[1])
                da_meetingid_spearker = dialogueAct['startwordid'].split('.words')[0]

                if words_meetingid_spearker != da_meetingid_spearker:
                    continue
                # topic boundary is annotated based on words not dialogue acts
                # thus its boundary is not aligned with that of DAs
                if set(range(da_start, da_end+1)).intersection(set(range(words_start, words_end+1))) != set():
                    dialogueacts.append(dialogueAct)
    except:
        print('missing <topic content>', id)

    return id, default_topic_type_name, other_description, dialogueacts

paths = utils.get_paths('manual')

file_name_list = [f for f in os.listdir(paths['topics']) if f.endswith('.topic.xml')]

for file_name in file_name_list:
    meeting_id = utils.get_meeting_id(file_name)

    # load dialogueActs
    try:
        dialogueActs = {}
        dialogueAct_json = json.load(open('output/dialogueActs/' + meeting_id + '.json'))
        for dialogueAct in dialogueAct_json:
            dialogueActs[dialogueAct['id']] = dialogueAct
    except:
        print('missing ' + 'output/dialogueActs/' + meeting_id + '.json')
        continue

    # load default-topics.xml
    default_topic_types = {}
    default_topics_xml = utils.xml_to_dict(
        paths['ontologies-default-topics']
    )
    for item in default_topics_xml['topicname']['topicname']:
        try:
            for default_topic in item['topicname']:
                default_topic_types[default_topic['@nite:id']] = default_topic['@name']
        except:
            default_topic_types[item['@nite:id']] = item['@name']

    # load .topic.xml
    topics = []
    topics_xml = utils.xml_to_dict(
        paths['topics'] + file_name,
        force_list=('nite:child', 'topic')
    )

    for topic in topics_xml['nite:root']['topic']:
        id, default_topic_type_name, other_description, dialogueacts = run(topic)

        # precess subtopic
        subtopics = 'None'
        if 'topic' in topic:
            subtopics = []
            for subtopic in topic['topic']:
                sub_id, sub_default_topic_type_name, sub_other_description, sub_dialogueacts = run(subtopic)
                subtopics.append({
                    'id': sub_id,
                    'topic': sub_default_topic_type_name,
                    'description': sub_other_description,
                    'dialogueacts': sub_dialogueacts
                })

        topics.append({
            'id': id,
            'topic': default_topic_type_name,
            'description': other_description,
            'dialogueacts': dialogueacts,
            'subtopics': subtopics
        })

    output_dir = 'output/topics/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir+meeting_id+'.json', 'w') as f:
        json.dump(topics, f)

