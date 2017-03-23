# -*- coding: utf-8 -*-
from __future__ import print_function
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import jieba

# data collection: collect all notes, key elements of a note: title, tags

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
    f = open('output/notes', 'w')
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
            print(n.title, tags_str, file=f)
    f.close()


def KeywordExtractor(str):
    return jieba.cut(str, cut_all=True)

# 单词云，统计词频
def WordFrequencyApp():
    hot_word_frequency = {}
    with open('output/notes', 'r') as f:
        for line in f:
            seg_list = KeywordExtractor(line)
            for w in seg_list:
                if w in hot_word_frequency:
                    hot_word_frequency[w] = hot_word_frequency[w] + 1
                else:
                    hot_word_frequency[w] = 1
    with open('output/frequency.txt', 'w') as f:
        for w in hot_word_frequency:
            print(w.encode('utf-8'), hot_word_frequency[w], file=f)



# GetEvernoteNotesGUID()
# print("/ ".join(KeywordExtractor('evernote的API都是用的thrift生成的。。自己手写REST接口太奇怪！效率低！')))
# WordFrequencyApp()