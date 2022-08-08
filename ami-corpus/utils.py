import xmltodict


def get_paths(source):
    paths = {}
    if source == 'manual':
        path = 'input/ami_public_manual_1.6.2/'
        paths = {
            'words'          : path + 'words/',
            'dialogueActs'   : path + 'dialogueActs/',
            'topics'         : path + 'topics/',
            'segments'       : path + 'segments/',
            'abstractive'    : path + 'abstractive/',
            'extractive'     : path + 'extractive/',
            'corpusResources-meetings'    : path + 'corpusResources/meetings.xml',
            'corpusResources-participants': path + 'corpusResources/participants.xml',
            'ontologies-da-types': path + 'ontologies/da-types.xml',
            'ontologies-ap-types': path + 'ontologies/ap-types.xml',
            'ontologies-default-topics': path + 'ontologies/default-topics.xml',
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

