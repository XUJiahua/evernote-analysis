from __future__ import print_function
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

# data collection: collect all notes, key elements of a note: title, tags
# TODO app: kmean classification, high frequency word


def GetEvernoteNotesGUID():
    with open('dev_token.txt', 'r') as myfile:
        dev_token = myfile.read().replace('\n', '')
    client = EvernoteClient(token=dev_token, sandbox=False)
    noteStore = client.get_note_store()

    tags_dict = {}

    tags = noteStore.listTags()
    for t in tags:
        tags_dict[t.guid] = t.name

    notebooks = noteStore.listNotebooks()
    # no need to get the content of a note
    f = open('notes', 'w')
    for n in notebooks:
        print("*** ", n.name)
        fi = NoteFilter(notebookGuid=n.guid)
        result_spec = NotesMetadataResultSpec(
            includeTitle=True, includeTagGuids=True)
        # NOTE: frequently API calls will result in rate limiting
        # assume 250 notes in a single notebook at most
        metadataList = noteStore.findNotesMetadata(
            dev_token, fi, 0, 250, result_spec)
        for n in metadataList.notes:
            tags_str = ''
            if n.tagGuids != None:
                for t in n.tagGuids:
                    tags_str += tags_dict[t] + ' '
            if tags_str == '':
                tags_str = 'NOTAG'
            print(n.title, tags_str, file=f)
    f.close()


GetEvernoteNotesGUID()
