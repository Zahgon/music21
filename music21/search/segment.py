# ------------------------------------------------------------------------------
# Name:         search/segment.py
# Purpose:      music21 classes for searching via segment matching
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011-2018 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
tools for segmenting -- that is, dividing up a score into small, possibly overlapping
sections -- for searching across pieces for similarity.

Speed notes:

   this module is definitely a case where running PyPy rather than cPython will
   give you a 3-5x speedup.

   If you really want to do lots of comparisons, the `scoreSimilarity` method will
   use python-Levenshtein if it is installed, unless forceDifflib is set to True.
   python-Levenshtein can be installed via **pip install python-Levenshtein**.
   The ratios are very slightly different, but the speedup is between 10 and 100x!
   (But then PyPy probably won't work.)
'''

from __future__ import annotations

from collections import OrderedDict
import difflib
from functools import partial
import json
import math
import pathlib
import random

from music21 import common
from music21 import converter
from music21 import corpus
from music21 import environment

environLocal = environment.Environment('search.segment')


# noinspection SpellCheckingInspection
def translateMonophonicPartToSegments(
    inputStream,
    *,
    segmentLengths=30,
    overlap=12,
    algorithm=None,
    jitter=0,
):
    '''
    Translates a monophonic part with measures to a set of segments of length
    `segmentLengths` (measured in number of notes) with an overlap of `overlap` notes
    using a conversion algorithm of `algorithm` (default: search.translateStreamToStringNoRhythm).
    Returns two lists, a list of segments, and a list of tuples of measure start and end
    numbers that match the segments.

    If algorithm is None then a default algorithm of music21.search.translateStreamToStringNoRhythm
    is used

    >>> luca = corpus.parse('luca/gloria')
    >>> lucaCantus = luca.parts[0]
    >>> segments, measureLists = search.segment.translateMonophonicPartToSegments(lucaCantus)
    >>> segments[0:2]
    ['HJHEAAEHHCE@JHGECA@A>@A><A@AAE', '@A>@A><A@AAEEECGHJHGH@CAE@FECA']


    Segment zero begins at measure 1 and ends in m. 12.  Segment 1 spans m.7 - m.18:

    >>> measureLists[0:2]
    [(1, 12), (7, 18)]

    >>> segments, measureLists = search.segment.translateMonophonicPartToSegments(
    ...     lucaCantus,
    ...     algorithm=search.translateDiatonicStreamToString)
    >>> segments[0:2]
    ['CRJOMTHCQNALRQPAGFEFDLFDCFEMOO', 'EFDLFDCFEMOOONPJDCBJSNTHLBOGFE']

    >>> measureLists[0:2]
    [(1, 12), (7, 18)]

    '''
    pass


# noinspection SpellCheckingInspection
def indexScoreParts(scoreFile, **keywords):
    r'''
    Creates segment and measure lists for each part of a score
    Returns list of dictionaries of segment and measure lists

    >>> bach = corpus.parse('bwv66.6')
    >>> scoreList = search.segment.indexScoreParts(bach)
    >>> scoreList[1]['segmentList'][0]
    '@B@@@@ED@DBDA=BB@?==B@@EBBDBBA'
    >>> scoreList[1]['measureList'][0:3]
    [(0, 7), (4, 9), (8, 9)]
    '''
    pass


def _indexSingleMulticore(filePath, failFast=False, **keywords):
    '''
    Index one path in the context of multicore.
    '''
    pass


def _giveUpdatesMulticore(numRun, totalRun, latestOutput):
    pass


# noinspection SpellCheckingInspection
def indexScoreFilePaths(scoreFilePaths,
                        *,
                        giveUpdates=False,
                        runMulticore=True,
                        **keywords):
    # noinspection PyShadowingNames
    '''
    Returns a dictionary of the lists from indexScoreParts for each score in
    scoreFilePaths

    >>> #_DOCS_SHOW searchResults = corpus.search('bwv190')
    >>> searchResults = corpus.corpora.CoreCorpus().search('bwv190') #_DOCS_HIDE
    >>> fpsNamesOnly = sorted([searchResult.sourcePath for searchResult in searchResults])
    >>> len(fpsNamesOnly)
    2

    >>> scoreDict = search.segment.indexScoreFilePaths(fpsNamesOnly)
    >>> len(scoreDict['bwv190.7.mxl'])
    4

    >>> scoreDict['bwv190.7.mxl'][0]['measureList']
    [(0, 9), (6, 15), (11, 20), (17, 25), (22, 31), (27, 32)]

    >>> scoreDict['bwv190.7.mxl'][0]['segmentList'][0]
    'NNJLNOLLLJJIJLLLLNJJJIJLLJNNJL'
    '''
    pass


def indexOnePath(filePath, **keywords):
    '''
    Index a single path.  Returns a scoreDictEntry
    '''
    pass


def saveScoreDict(scoreDict, filePath=None):
    '''
    Save the score dict from indexScoreFilePaths as a .json file for quickly
    reloading

    Returns the filepath (assumes you'll probably be using a temporary file)
    as a pathlib.Path()
    '''
    pass


def loadScoreDict(filePath):
    '''
    Load the scoreDictionary from filePath.
    '''
    pass


def getDifflibOrPyLev(
    seq2=None,
    junk=None,
    forceDifflib=False,
):
    '''
    Returns either a difflib.SequenceMatcher or pyLevenshtein
    StringMatcher.StringMatcher object depending on what is installed.

    If forceDifflib is True then use difflib even if pyLevenshtein is installed:
    '''
    pass


def scoreSimilarity(
    scoreDict,
    minimumLength=20,
    giveUpdates=False,
    includeReverse=False,
    forceDifflib=False,
):
    # noinspection PyShadowingNames
    r'''
    Find the level of similarity between each pair of segments in a scoreDict.

    This takes twice as long as it should because it does not cache the
    pairwise similarity.

    >>> filePaths = []
    >>> for p in ('bwv197.5.mxl', 'bwv190.7.mxl', 'bwv197.10.mxl'):
    ...     #_DOCS_SHOW source = corpus.search(p)[0].sourcePath
    ...     source = corpus.corpora.CoreCorpus().search(p)[0].sourcePath #_DOCS_HIDE
    ...     filePaths.append(source)
    >>> scoreDict = search.segment.indexScoreFilePaths(filePaths)
    >>> scoreSim = search.segment.scoreSimilarity(scoreDict, forceDifflib=True) #_DOCS_HIDE
    >>> #_DOCS_SHOW scoreSim = search.segment.scoreSimilarity(scoreDict)
    >>> len(scoreSim)
    496

    Returns a list of tuples of first score name, first score voice number, first score
    measure number, second score name, second score voice number, second score
    measure number, and similarity score (0 to 1).

    >>> for result in scoreSim[133:137]:
    ...     result
    ('bwv197.5.mxl', 1, 1, (4, 10), 'bwv190.7.mxl', 3, 4, (22, 30), 0.13...)
    ('bwv197.5.mxl', 1, 1, (4, 10), 'bwv197.10.mxl', 0, 0, (0, 8), 0.2)
    ('bwv197.5.mxl', 1, 1, (4, 10), 'bwv197.10.mxl', 1, 0, (0, 7), 0.266...)
    ('bwv197.5.mxl', 1, 1, (4, 10), 'bwv197.10.mxl', 1, 1, (4, 9), 0.307...)
    '''
    pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER: list[type] = []


if __name__ == '__main__':
    import music21
    music21.mainTest()
