# AMI and ICSI Corpora
This is a python3 project that converts some annotations of the [AMI and ISCI Corpora](https://groups.inf.ed.ac.uk/ami/) from the original XML format into the JSON format.

The processed corpora can be directly downloaded from [here](https://drive.google.com/drive/folders/1BbmaZnzG9WrqOO-D3h211NOJePotqwQJ?usp=sharing) (last update 08/08/2022).

If you want to run the code yourself, please follow the following instructions. Dependency requirements: [xmltodict](https://github.com/martinblech/xmltodict).

# AMI Corpus
1. Extract [AMI manual annotations v1.6.2 (ami_public_manual_1.6.2.zip)](http://groups.inf.ed.ac.uk/ami/download/) under `input/ami_public_manual_1.6.2`.

2. Run the following Python scripts to obtain respective annotations in JSON format under `output/`.

* **Manual meeting transcriptions** (dialogueActs.py). Note: you should run this script first.
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.B.dialog-act.dharshi.7",
      "speaker":"B",
      "starttime":"74.42",
      "startwordid":"ES2002a.B.words63",
      "endtime":"77.29",
      "endwordid":"ES2002a.B.words71",
      "text":"<vocalsound> Do you want to introduce yourself again ?",
      "label":"el.inf",
      "attributes":{ # reflexivity, addressee, comment, endtime
         "addressee":"A,D,C",
         "role":"PM",
         "participant":"FEE005"
      }
   },
  ...
]
```
`label` denotes dialogue act labels, the taxonomy can be found in the `/input/ami_public_manual_1.6.2/ontologies/da-types.xml`.

`participant` denotes speaker tags, their profiles (e.g., age) can be found in the `input/ami_public_manual_1.6.2/corpusResources/participants.xml`.
</details>

* **Abstractive summaries** (abstractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.rdhillon.s.1",
      "text":"The project manager introduced the upcoming project to the team members and then the team members participated in an exercise in which they drew their favorite animal and discussed what they liked about the animal.",
      "type":"abstract"
   },
   {
      "id":"ES2002a.rdhillon.s.2",
      "text":"The project manager talked about the project finances and selling prices.",
      "type":"abstract"
   },
   ...
]
```
</details>

* **Extractive summaries** (extractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.B.dialog-act.dharshi.3",
      "speaker":"B",
      "starttime":"55.415",
      "startwordid":"ES2002a.B.words4",
      "endtime":"60.35",
      "endwordid":"ES2002a.B.words16",
      "text":"<vocalsound> Um well this is the kick-off meeting for our our project .",
      "label":"inf",
      "attributes":{
         "reflexivity":"true",
         "role":"PM",
         "participant":"FEE005"
      }
   },
   {
      "id":"ES2002a.B.dialog-act.dharshi.12",
      "speaker":"B",
      "starttime":"92.79",
      "startwordid":"ES2002a.B.words80",
      "endtime":"96.34",
      "endwordid":"ES2002a.B.words89",
      "text":"so we're designing a new remote control and um <disfmarker>",
      "label":"inf",
      "attributes":{
         "reflexivity":"true",
         "role":"PM",
         "participant":"FEE005"
      }
   },
   ...
]
```
</details>

* **Abstractive-Extractive linkings / Abstractive communities** (summlink.py)
<details>
  <summary>example</summary>

```json
[
...,
   {
      "abstractive":{
         "id":"ES2002a.rdhillon.s.7",
         "text":"The remote will sell for 25 Euro.",
         "type":"decisions"
      },
      "extractive":[
         {
            "id":"ES2002a.B.dialog-act.dharshi.89",
            "speaker":"B",
            "starttime":"470.01",
            "startwordid":"ES2002a.B.words636",
            "endtime":"476.53",
            "endwordid":"ES2002a.B.words654",
            "text":"Um so according to the brief um we're gonna be selling this remote control for twenty five Euro ,",
            "label":"inf",
            "attributes":{
               "role":"PM",
               "participant":"FEE005"
            }
         },
         {
            "id":"ES2002a.B.dialog-act.dharshi.129",
            "speaker":"B",
            "starttime":"681.66",
            "startwordid":"ES2002a.B.words912",
            "endtime":"687.09",
            "endwordid":"ES2002a.B.words928",
            "text":"Well twenty five Euro , I mean that's um that's about like eighteen pounds or something ,",
            "label":"inf",
            "attributes":{
               "role":"PM",
               "participant":"FEE005"
            }
         }
      ]
   },
  ...
]
```
</details>

* **Adjacency pairs** (adjacencyPairs.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"ES2002a.adjacency-pairs.dharshi.1",
      "type":"POS",
      "source":{
         "id":"ES2002a.B.dialog-act.dharshi.7",
         "speaker":"B",
         "starttime":"74.42",
         "startwordid":"ES2002a.B.words63",
         "endtime":"77.29",
         "endwordid":"ES2002a.B.words71",
         "text":"<vocalsound> Do you want to introduce yourself again ?",
         "label":"el.inf",
         "attributes":{
            "addressee":"A,D,C",
            "role":"PM",
            "participant":"FEE005"
         }
      },
      "target":{
         "id":"ES2002a.A.dialog-act.dharshi.1",
         "speaker":"A",
         "starttime":"77.44",
         "startwordid":"ES2002a.A.words0",
         "endtime":"80.87",
         "endwordid":"ES2002a.A.words12",
         "text":"Hi , I'm David and I'm supposed to be an industrial designer .",
         "label":"inf",
         "attributes":{
            "role":"ID",
            "participant":"MEE006"
         }
      }
   },
  ...
]
```
</details>

* **Topic segmentation** (topic.py)
<details>
  <summary>example</summary>

```json
[
  {
    "id": "ES2003d.topic.rdhillon.6",
    "topic": "evaluation of prototype(s)",
    "description": "None",
    "dialogueacts": [
      {
        "id": "ES2003d.C.dialog-act.vkaraisk.8",
        "speaker": "C",
        "starttime": "329.94",
        "startwordid": "ES2003d.C.words23",
        "endtime": "336.2",
        "endwordid": "ES2003d.C.words39",
        "text": "Basic point uh have a list of criteria that we need to rate the prototype by .",
        "aspect": "inf",
        "attributes": {
          "reflexivity": "true",
          "role": "ME",
          "participant":"MEE012"
        }
      },
      ... # more DAs
    ],
    "subtopics": [
      {
        "id": "ES2003d.topic.rdhillon.7",
        "topic": "how to find when misplaced",
        "description": "None",
        "dialogueacts": [
          {
            "id": "ES2003d.C.dialog-act.vkaraisk.34",
            "speaker": "C",
            "starttime": "421.78",
            "startwordid": "ES2003d.C.words229",
            "endtime": "423.51",
            "endwordid": "ES2003d.C.words230",
            "text": "So um",
            "aspect": "stl",
            "attributes": {
              "role": "ME",
              "participant":"MEE012"
            }
          },
          ... # more DAs
        ]
      },
      {
        "id": "ES2003d.topic.rdhillon.8",
        "topic": "agenda/equipment issues",
        "description": "None",
        "dialogueacts": [
          {
            "id": "ES2003d.B.dialog-act.vkaraisk.44",
            "speaker": "B",
            "starttime": "516.29",
            "startwordid": "ES2003d.B.words301",
            "endtime": "521.8",
            "endwordid": "ES2003d.B.words317",
            "text": "just before we go through all of the steps here , um well what we'll do is",
            "aspect": "fra",
            "attributes": {
              "role": "PM",
              "participant":"MEE009"
            }
          },
          ... # more DAs
        ]
      },
      ... # more subtopics
    ]
  },
  ... # more topics
]
```
</details>

For more details of these annotations, please refer to the [annotation guidelines](https://groups.inf.ed.ac.uk/ami/corpus/guidelines.shtml) or the citations in below.

# ICSI Corpus
1. Extract [ICSI core plus contributed annotations v1.0 (ICSI_plus_NXT.zip)](https://groups.inf.ed.ac.uk/ami/icsi/download/) under `input/ICSI_plus_NXT`.

2. Run the following Python scripts to obtain respective annotations in JSON format under `output/`.

* **Manual meeting transcriptions** (dialogueActs.py). Note: you should run this script first.
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.C.dialogueact0",
      "speaker":"C",
      "starttime":"0.216",
      "startwordid":"Bdb001.w.1",
      "endtime":"5.914",
      "endwordid":"Bdb001.w.25",
      "text":"Yeah , we had a long discussion about how much w how easy we want to make it for people to bleep things out .",
      "label":"z",
      "original_label":"z",
      "attributes":{ # role, participant, adjacency, channel
         "role":"Grad",
         "participant":"me011",
         "channel":"c3"
      }
   },
  ...
]
```
`label` denotes dialogue act labels.

`participant` denotes speaker tags, their profiles (e.g., age) can be found in the `input/ICSI_plus_NXT/ICSIplus/speakers.xml`.
</details>

* **Abstractive summaries** (abstractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.s.1",
      "text":"Two main options were discussed as to the organisation of the collected data.",
      "type":"abstract"
   },
   {
      "id":"Bdb001.s.2",
      "text":"On the one hand, a bespoke XML structure that connects transcriptions and annotations (down to the word-level) to a common timeline.",
      "type":"abstract"
   },
   ...
]
```
</details>

* **Extractive summaries** (extractive.py)
<details>
  <summary>example</summary>

```json
[
   {
      "id":"Bdb001.F.dialogueact37",
      "speaker":"F",
      "starttime":"68.88",
      "startwordid":"Bdb001.w.335",
      "endtime":"89.054",
      "endwordid":"Bdb001.w.376",
      "text":"and <vocalsound> the main thing that I was gonna ask people to help with today is <pause> to give input on what kinds of database format we should <pause> use in starting to link up things like word transcripts and annotations of word transcripts ,",
      "label":"s",
      "original_label":"s",
      "attributes":{
         "role":"PhD",
         "participant":"fe016",
         "channel":"cB"
      }
   },
   {
      "id":"Bdb001.C.dialogueact44",
      "speaker":"C",
      "starttime":"113.159",
      "startwordid":"Bdb001.w.461",
      "endtime":"118.67",
      "endwordid":"Bdb001.w.487",
      "text":"I mean , we <disfmarker> I sort of already have developed an XML format for this sort of stuff .",
      "label":"s",
      "original_label":"s",
      "attributes":{
         "role":"Grad",
         "participant":"me011",
         "adjacency":"1b+",
         "channel":"c3"
      }
   },
   ...
]
```
</details>

* **Abstractive-Extractive linkings / Abstractive communities** (summlink.py)
<details>
  <summary>example</summary>

```json
[
   {
      "abstractive":{
         "id":"Bdb001.s.1",
         "text":"Two main options were discussed as to the organisation of the collected data.",
         "type":"abstract"
      },
      "extractive":[
         {
            "id":"Bdb001.F.dialogueact37",
            "speaker":"F",
            "starttime":"68.88",
            "startwordid":"Bdb001.w.335",
            "endtime":"89.054",
            "endwordid":"Bdb001.w.376",
            "text":"and <vocalsound> the main thing that I was gonna ask people to help with today is <pause> to give input on what kinds of database format we should <pause> use in starting to link up things like word transcripts and annotations of word transcripts ,",
            "label":"s",
            "original_label":"s",
            "attributes":{
               "role":"PhD",
               "participant":"fe016",
               "channel":"cB"
            }
         },
         {
            "id":"Bdb001.C.dialogueact404",
            "speaker":"C",
            "starttime":"790.456",
            "startwordid":"Bdb001.w.3,414",
            "endtime":"791.666",
            "endwordid":"Bdb001.w.3,422",
            "text":"Th - there are sort of two choices .",
            "label":"s",
            "original_label":"s",
            "attributes":{
               "role":"Grad",
               "participant":"me011",
               "channel":"c3"
            }
         }
      ]
   },
  ...
]
```
</details>

For more details of these annotations, please refer to the [annotation guidelines](https://groups.inf.ed.ac.uk/ami/corpus/guidelines.shtml) or the citations in below.

# Training, Validation, and Test Sets
For the AMI corpus, multiple official suggestions exist [here](https://groups.inf.ed.ac.uk/ami/corpus/datasets.shtml), "scenario-only partition of meetings" in below is the most adopted one in the litterature:
```python
def flatten(list_of_list):
    return [item for sublist in list_of_list for item in sublist]
 
ami_train = ['ES2002', 'ES2005', 'ES2006', 'ES2007', 'ES2008', 'ES2009', 'ES2010', 'ES2012', 'ES2013', 'ES2015', 'ES2016', 'IS1000', 'IS1001', 'IS1002', 'IS1003', 'IS1004', 'IS1005', 'IS1006', 'IS1007', 'TS3005', 'TS3008', 'TS3009', 'TS3010', 'TS3011', 'TS3012']
ami_train = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_train])
ami_train.remove('IS1002a')
ami_train.remove('IS1005d')

ami_validation = ['ES2003', 'ES2011', 'IS1008', 'TS3004', 'TS3006']
ami_validation = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_validation])

ami_test = ['ES2004', 'ES2014', 'IS1009', 'TS3003', 'TS3007']
ami_test = flatten([[m_id+s_id for s_id in 'abcd'] for m_id in ami_test])
```

For the ICSI corpus, the traditional test set (see citations [4]) is shown in below, training and validation sets are not specified. 
```
icsi_test = ['Bed004', 'Bed009', 'Bed016', 'Bmr005', 'Bmr019', 'Bro018']
```
# Citations
If you find this repository helpful, please consider to cite the publications:

[1] [Abstractive Meeting Summarization: A Survey](https://arxiv.org/abs/2208.04163)
```
@article{rennard2022abstractive,
  title={Abstractive Meeting Summarization: A Survey},
  author={Rennard, Virgile and Shang, Guokan and Hunter, Julie and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2208.04163},
  year={2022}
}
```
[2] [Energy-based Self-attentive Learning of Abstractive Communities for Spoken Language Understanding](https://aclanthology.org/2020.aacl-main.34/)
```
@inproceedings{shang2020energy,
  title={Energy-based Self-attentive Learning of Abstractive Communities for Spoken Language Understanding},
  author={Shang, Guokan and Tixier, Antoine and Vazirgiannis, Michalis and Lorr{\'e}, Jean-Pierre},
  booktitle={Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing},
  pages={313--327},
  year={2020}
}
```
[3] [Spoken Language Understanding for Abstractive Meeting Summarization](https://tel.archives-ouvertes.fr/tel-03169877/document)
```
@phdthesis{shang2021spoken,
  title={Spoken Language Understanding for Abstractive Meeting Summarization},
  author={Shang, Guokan},
  year={2021},
  school={Institut polytechnique de Paris}
}
```
[4] [Unsupervised abstractive meeting summarization with multi-sentence compression and budgeted submodular maximization](https://aclanthology.org/P18-1062/)
```
@article{shang2018unsupervised,
  title={Unsupervised abstractive meeting summarization with multi-sentence compression and budgeted submodular maximization},
  author={Shang, Guokan and Ding, Wensi and Zhang, Zekun and Tixier, Antoine Jean-Pierre and Meladianos, Polykarpos and Vazirgiannis, Michalis and Lorr{\'e}, Jean-Pierre},
  journal={arXiv preprint arXiv:1805.05271},
  year={2018}
}
```
