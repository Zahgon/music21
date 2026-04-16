# -----------------------------------------------------------------------------
# Name:         corpus/work.py
# Purpose:      Manage one work
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2015 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
'''
This is a lightweight module that stores information about individual corpus works.
'''
from __future__ import annotations

from collections import namedtuple, OrderedDict
import os

from music21 import common
from music21 import prebase

# -----------------------------------------------------------------------------
CorpusWork = namedtuple('CorpusWork', ['title', 'files', 'virtual'])
CorpusFile = namedtuple('CorpusFile', ['path', 'title', 'filename', 'format', 'ext'])
# VirtualCorpusFile = namedtuple('VirtualCorpusFile', ['path', 'title', 'url', 'format'])


class DirectoryInformation(prebase.ProtoM21Object):
    '''
    returns information about a directory in a Corpus.  Called from corpus.corpora.Corpus

    only tested with CoreCorpus so far.
    '''

    def __init__(self, dirName='', dirTitle='', isComposer=True, corpusObject=None):
        self.directoryName = dirName
        self.directoryTitle = dirTitle
        self.isComposer = isComposer
        self.works = OrderedDict()

        self.corpusObject = corpusObject

        self.findWorks()

    def _reprInternal(self):
        pass

    def findWorks(self):
        r'''
        Populate other information about the directory such as
        files and filenames.

        >>> di = corpus.work.DirectoryInformation('schoenberg',
        ...             corpusObject=corpus.corpora.CoreCorpus())
        >>> di.findWorks()
        OrderedDict([('opus19', CorpusWork(title='Opus 19',
                                    files=[CorpusFile(path='schoenberg...opus19...movement2.mxl',
                                                        title='Movement 2',
                                                        filename='movement2.mxl',
                                                        format='musicxml',
                                                        ext='.mxl'),
                                            CorpusFile(path='schoenberg...opus19...movement6.mxl',
                                                        title='Movement 6',
                                                        filename='movement6.mxl',
                                                        format='musicxml',
                                                        ext='.mxl')],
                                    virtual=False))])

        (The ellipses in the documentation above represent '/' on Mac/Unix systems and
        '\' on Windows.)
        '''
        pass

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest()
