import xmltodict


def get_paths(source):
    paths = {}
    if source == 'plus':
        path = 'input/ICSI_plus_NXT/ICSIplus/'
        paths = {
            'words'          : path + 'Words/',
            'dialogueActs'   : path + 'DialogueActs/',
            # 'topics'         : path + 'topics/',
            # 'segments'       : path + 'Segments/',
            'abstractive'    : path + 'Contributions/Summarization/abstractive/',
            'extractive'     : path + 'Contributions/Summarization/extractive/',
            # 'corpusResources-meetings'    : path + 'corpusResources/meetings.xml',
            # 'corpusResources-participants': path + 'corpusResources/participants.xml',
            # 'ontologies-da-types': path + 'ontologies/da-types.xml',
            # 'ontologies-ap-types': path + 'ontologies/ap-types.xml',
            # 'ontologies-default-topics': path + 'ontologies/default-topics.xml',
            'speakers'          : path + 'speakers.xml',
        }
    else:
        pass

    return paths


def xml_to_dict(file, force_list=None):
    with open(file) as f:
        doc = xmltodict.parse(f.read(), force_list=force_list)
    return doc


def get_meeting_id(file_name):
    return file_name.split('.')[0]

def get_meeting_speaker(file_name):
    return file_name.split('.')[1]

