# ------------------------------------------------------------------------------
# Name:         reduceChords.py
# Purpose:      Tools for eliminating passing chords, etc.
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2013-14 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Automatically reduce a MeasureStack to a single chord or group of chords.
'''
from __future__ import annotations

import copy
import unittest

from music21 import chord
from music21.common.types import DocOrder
from music21 import clef
from music21 import meter
from music21 import stream
from music21 import tie

def testMeasureStream1():
    # noinspection PyShadowingNames
    '''
    returns a simple measure stream for testing:

    >>> s = analysis.reduceChordsOld.testMeasureStream1()
    >>> s.show('text')
    {0.0} <music21.meter.TimeSignature 4/4>
    {0.0} <music21.chord.Chord C4 E4 G4 C5>
    {2.0} <music21.chord.Chord C4 E4 F4 B4>
    {3.0} <music21.chord.Chord C4 E4 G4 C5>
    '''
    pass

class ChordReducer:
    def __init__(self):
        self.printDebug = False
        self.weightAlgorithm = self.qlbsmpConsonance
        self.maxChords = 3
        self.positionInMeasure = None
        self.numberOfElementsInMeasure = None

        # for working
        self._lastPitchedObject = None
        self._lastTs = None

    def reduceMeasureToNChords(self,
                               measureObj,
                               numChords=1,
                               weightAlgorithm=None,
                               trimBelow=0.25):
        '''
        Takes a measure and reduces it to only one chord or `numChords` chords.

        >>> s = analysis.reduceChordsOld.testMeasureStream1()
        >>> cr = analysis.reduceChordsOld.ChordReducer()

        Reduce to a maximum of 3 chords; though here we will
        only get one because the other chord is
        below the trimBelow threshold.

        >>> newS = cr.reduceMeasureToNChords(s, 3,
        ...    weightAlgorithm=cr.qlbsmpConsonance, trimBelow = 0.3)
        >>> newS.show('text')
        {0.0} <music21.chord.Chord C4 E4 G4 C5>
        >>> newS.notes.first().quarterLength
        4.0
        '''
        from music21 import note
        if measureObj.isFlat is False:
            mObj = measureObj.flatten().notes.stream()
        else:
            mObj = measureObj.notes.stream()

        chordWeights = self.computeMeasureChordWeights(mObj, weightAlgorithm)

        numChords = min(numChords, len(chordWeights))

        maxNChords = sorted(chordWeights, key=chordWeights.get, reverse=True)[:numChords]
        if not maxNChords:
            r = note.Rest()
            r.quarterLength = mObj.duration.quarterLength
            for c in mObj:
                mObj.remove(c)
            mObj.insert(0, r)
            return mObj
        maxChordWeight = chordWeights[maxNChords[0]]

        trimmedMaxChords = []
        for pcTuples in maxNChords:
            if chordWeights[pcTuples] >= maxChordWeight * trimBelow:
                trimmedMaxChords.append(pcTuples)
                # print(chordWeights[pcTuples], maxChordWeight)
            else:
                break

        currentGreedyChord = None
        currentGreedyChordPCs = None
        currentGreedyChordNewLength = 0.0
        for c in mObj:
            p = tuple({x.pitchClass for x in c.pitches})
            if p in trimmedMaxChords and p != currentGreedyChordPCs:
                # keep this chord
                if currentGreedyChord is None and c.offset != 0.0:
                    currentGreedyChordNewLength = c.offset
                    c.offset = 0.0
                elif currentGreedyChord is not None:
                    currentGreedyChord.quarterLength = currentGreedyChordNewLength
                    currentGreedyChordNewLength = 0.0
                currentGreedyChord = c
                for n in c:
                    n.tie = None
                    if n.pitch.accidental is not None:
                        n.pitch.accidental.displayStatus = None
                currentGreedyChordPCs = p
                currentGreedyChordNewLength += c.quarterLength
            else:
                currentGreedyChordNewLength += c.quarterLength
                mObj.remove(c)
        if currentGreedyChord is not None:
            currentGreedyChord.quarterLength = currentGreedyChordNewLength
            currentGreedyChordNewLength = 0.0

        # even chord lengths
        for i in range(1, len(mObj)):
            c = mObj[i]
            cOffsetCurrent = c.offset
            cOffsetSyncop = cOffsetCurrent - int(cOffsetCurrent)
            if round(cOffsetSyncop, 3) in [0.250, 0.125, 0.333, 0.063, 0.062]:
                lastC = mObj[i - 1]
                lastC.quarterLength -= cOffsetSyncop
                c.offset = int(cOffsetCurrent)
                c.quarterLength += cOffsetSyncop

        # Remove zero-duration chords
        for c in list(mObj):
            if not c.quarterLength:
                mObj.remove(c)

        return mObj
        # closed position

    def computeMeasureChordWeights(self, measureObj, weightAlgorithm=None):
        '''

        >>> s = analysis.reduceChordsOld.testMeasureStream1().notes
        >>> cr = analysis.reduceChordsOld.ChordReducer()
        >>> cws = cr.computeMeasureChordWeights(s)
        >>> for pcs in sorted(cws):
        ...     print(f'{pcs!r:18}  {cws[pcs]:2.1f}')
             (0, 4, 7)  3.0
         (0, 11, 4, 5)  1.0

        Add beatStrength:

        >>> cws = cr.computeMeasureChordWeights(s, weightAlgorithm=cr.quarterLengthBeatStrength)
        >>> for pcs in sorted(cws):
        ...     print(f'{pcs!r:18}  {cws[pcs]:2.1f}')
             (0, 4, 7)  2.2
         (0, 11, 4, 5)  0.5

        Give extra weight to the last element in a measure:

        >>> cws = cr.computeMeasureChordWeights(s,
        ...              weightAlgorithm=cr.quarterLengthBeatStrengthMeasurePosition)
        >>> for pcs in sorted(cws):
        ...     print(f'{pcs!r:18}  {cws[pcs]:2.1f}')
             (0, 4, 7)  3.0
         (0, 11, 4, 5)  0.5

        Make consonance count a lot:

        >>> cws = cr.computeMeasureChordWeights(s, weightAlgorithm=cr.qlbsmpConsonance)
        >>> for pcs in sorted(cws):
        ...     print(f'{pcs!r:18}  {cws[pcs]:2.1f}')
                 (0, 4, 7)  3.0
             (0, 11, 4, 5)  0.5
        '''
        if weightAlgorithm is None:
            weightAlgorithm = self.quarterLengthOnly
        presentPCs = {}

        self.positionInMeasure = 0
        self.numberOfElementsInMeasure = len(measureObj)

        for i, c in enumerate(measureObj):
            self.positionInMeasure = i
            p = tuple({x.pitchClass for x in c.pitches})
            if p not in presentPCs:
                presentPCs[p] = 0.0
            presentPCs[p] += weightAlgorithm(c)

        self.positionInMeasure = 0
        self.numberOfElementsInMeasure = 0

        return presentPCs

    def quarterLengthOnly(self, c):
        pass

    def quarterLengthBeatStrength(self, c):
        pass

    def quarterLengthBeatStrengthMeasurePosition(self, c):
        pass

    def qlbsmpConsonance(self, c):
        '''
        Everything from before plus consonance
        '''
        pass

    def multiPartReduction(self, inStream, maxChords=2, closedPosition=False, forceOctave=False):
        '''
        Return a multipart reduction of a stream.
        '''
        pass


    def reduceThisMeasure(self, mI, measureIndex, maxChords, closedPosition, forceOctave):
        pass
# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testSimpleMeasure(self):
        pass

class TestExternal(unittest.TestCase):
    show = True

    def testTrecentoMadrigal(self):
        pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER: DocOrder = []



if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

