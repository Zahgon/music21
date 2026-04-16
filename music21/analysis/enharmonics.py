# ------------------------------------------------------------------------------
# Name:         enharmonics.py
# Purpose:      Tools for returning best enharmonics
#
# Authors:      Mark Gotham
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2017 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import itertools
from math import inf
import unittest

from music21 import environment
from music21 import pitch
from music21 import musedata

environLocal = environment.Environment('analysis.enharmonics')


class EnharmonicScoreRules:
    def __init__(self):
        self.sameStaffLine = False
        self.alterationPenalty = 4
        self.augDimPenalty = 2
        self.mixSharpsFlatsPenalty = False

class ChordEnharmonicScoreRules(EnharmonicScoreRules):
    def __init__(self):
        super().__init__()
        self.mixSharpsFlatsPenalty = 2

class EnharmonicSimplifier:
    '''
    Takes any pitch list input and returns the best enharmonic respelling according to the input
    criteria and rule weightings.
    Those criteria and rule weightings are currently fixed, but in future the user should be able
    to select their own combination and weighting of rules according to preferences,
    with predefined defaults for melodic and harmonic norms.
    Note: EnharmonicSimplifier itself returns nothing.
    '''
    def __init__(self, pitchList, ruleClass=EnharmonicScoreRules):
        if isinstance(pitchList[0], str):
            pitchList = [pitch.Pitch(p) for p in pitchList]

        self.pitchList = pitchList
        self.ruleObject = ruleClass()
        self.allPossibleSpellings = None
        self.allSpellings = []
        self.getRepresentations()

    def getRepresentations(self):
        '''
        Takes a list of pitches or pitch names and retrieves all enharmonic spellings.
        Note: getRepresentations itself returns nothing.
        '''
        pass

    def getProduct(self):
        pass

    def bestPitches(self):
        '''
        Returns a list of pitches in the best enharmonic
        spelling according to the input criteria.

        >>> pList1 = [pitch.Pitch('C'), pitch.Pitch('D'), pitch.Pitch('E')]
        >>> es = analysis.enharmonics.EnharmonicSimplifier(pList1)
        >>> es.bestPitches()
        (<music21.pitch.Pitch C>, <music21.pitch.Pitch D>, <music21.pitch.Pitch E>)
        >>> pList2 = ['D--', 'E', 'F##']
        >>> es = analysis.enharmonics.EnharmonicSimplifier(pList2)
        >>> es.bestPitches()
        (<music21.pitch.Pitch C>, <music21.pitch.Pitch E>, <music21.pitch.Pitch G>)
        '''
        pass

    def getAlterationScore(self, possibility):
        '''
        Returns a score according to the number of sharps and flats in a possible spelling.
        The score is the sum of the flats and sharps + 1, multiplied by the alterationPenalty.
        '''
        pass

    def getMixSharpFlatsScore(self, possibility):
        '''
        Returns a score based on the mixture of sharps and flats in a possible spelling:
        the score is given by the number of the lesser used accidental (sharps or flats)
        multiplied by the mixSharpsFlatsPenalty.
        '''
        pass

    def getAugDimScore(self, possibility):
        '''
        Returns a score based on the number of augmented and diminished intervals between
        successive pitches in the given spelling.
        '''
        pass

# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testBestPitches(self):
        pass

    def testGetAlterationScore(self):
        pass

    def testGetMixSharpFlatsScore(self):
        pass

    def testGetAugDimScore(self):
        pass


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
