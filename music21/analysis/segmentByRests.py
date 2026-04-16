# ------------------------------------------------------------------------------
# Name:         segmentByRests.py
# Purpose:      Break up a part into its contiguous melodies.
#
# Authors:      Mark Gotham
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2018 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import unittest

from music21 import clef
from music21 import converter
from music21 import environment
from music21 import note
from music21 import interval

environLocal = environment.Environment('analysis.segmentByRests')

# ------------------------------------------------------------------------------
class Segmenter:
    '''
    Given a work or part, returns a list of melodic segments or intervals.
    '''
    @classmethod
    def getSegmentsList(cls,
                        workOrPart,
                        removeEmptyLists=True):
        # noinspection PyShadowingNames
        '''
        Segments a part by its rests (and clefs) and returns a list of lists where
        each sublist is one segment of contiguous notes. NB Uses .recurse() internally.

        >>> example = converter.parse("tinyNotation: C4 r D E r r F r G r A B r c")
        >>> segments = analysis.segmentByRests.Segmenter.getSegmentsList(example)
        >>> segments
        [[<music21.note.Note C>],
         [<music21.note.Note D>, <music21.note.Note E>],
         [<music21.note.Note F>],
         [<music21.note.Note G>],
         [<music21.note.Note A>, <music21.note.Note B>],
         [<music21.note.Note C>]]
        '''
        pass

    @classmethod
    def getIntervalList(cls, workOrPart):
        '''
        Given a work or part, returns a list of intervals between contiguous notes.
        NB Uses .recurse() internally so
        if called on a work then returns a list of lists with one list per part.

        >>> example = converter.parse("tinyNotation: 4/4 E4 r F G A r g c r c")
        >>> intList = analysis.segmentByRests.Segmenter.getIntervalList(example)
        >>> [x.name for x in intList]
        ['M2', 'M2', 'P5']
        '''
        pass

# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testGetSegmentsList(self):
        pass

    def testGetIntervalList(self):
        pass


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
