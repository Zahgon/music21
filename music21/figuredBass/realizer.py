# ------------------------------------------------------------------------------
# Name:         realizer.py
# Purpose:      figured bass lines, consisting of notes
#                and figures in a given key.
# Authors:      Jose Cabal-Ugaz
#
# Copyright:    Copyright © 2011 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
This module, the heart of fbRealizer, is all about realizing
a bass line of (bassNote, notationString)
pairs. All it takes to create well-formed realizations of a
bass line is a few lines of music21 code,
from start to finish. See :class:`~music21.figuredBass.realizer.FiguredBassLine` for more details.

>>> from music21.figuredBass import realizer
>>> fbLine = realizer.FiguredBassLine()
>>> fbLine.addElement(note.Note('C3'))
>>> fbLine.addElement(note.Note('D3'), '4,3')
>>> fbLine.addElement(note.Note('C3', quarterLength = 2.0))
>>> allSols = fbLine.realize()
>>> allSols.getNumSolutions()
30
>>> #_DOCS_SHOW allSols.generateRandomRealizations(14).show()

    .. image:: images/figuredBass/fbRealizer_intro.*
        :width: 500


The same can be accomplished by taking the notes and notations
from a :class:`~music21.stream.Stream`.
See :meth:`~music21.figuredBass.realizer.figuredBassFromStream` for more details.


>>> s = converter.parse('tinynotation: C4 D4_4,3 C2', makeNotation=False)
>>> fbLine = realizer.figuredBassFromStream(s)
>>> allSols2 = fbLine.realize()
>>> allSols2.getNumSolutions()
30
'''
from __future__ import annotations

import collections
import copy
import random
import typing as t
import unittest

from music21 import chord
from music21 import clef
from music21 import exceptions21
from music21 import key
from music21 import meter
from music21 import note
from music21 import pitch
from music21 import stream
from music21.figuredBass import checker
from music21.figuredBass import notation
from music21.figuredBass import realizerScale
from music21.figuredBass import rules
from music21.figuredBass import segment


def figuredBassFromStream(streamPart: stream.Stream) -> FiguredBassLine:
    # noinspection PyShadowingNames
    '''
    Takes a :class:`~music21.stream.Part` (or another :class:`~music21.stream.Stream` subclass)
    and returns a :class:`~music21.figuredBass.realizer.FiguredBassLine` object whose bass notes
    have notations taken from the lyrics in the source stream. This method along with the
    :meth:`~music21.figuredBass.realizer.FiguredBassLine.realize` method provide the easiest
    way of converting from a notated version of a figured bass (such as in a MusicXML file) to
    a realized version of the same line.

    >>> s = converter.parse('tinynotation: 4/4 C4 D8_6 E8_6 F4 G4_7 c1', makeNotation=False)
    >>> fb = figuredBass.realizer.figuredBassFromStream(s)
    >>> fb
    <music21.figuredBass.realizer.FiguredBassLine object at 0x...>

    >>> fbRules = figuredBass.rules.Rules()
    >>> fbRules.partMovementLimits = [(1, 2), (2, 12), (3, 12)]
    >>> fbRealization = fb.realize(fbRules)
    >>> fbRealization.getNumSolutions()
    13
    >>> #_DOCS_SHOW fbRealization.generateRandomRealizations(8).show()

    .. image:: images/figuredBass/fbRealizer_fbStreamPart.*
        :width: 500

    * Changed in v7.3: multiple figures in same lyric (e.g. '64') now supported.
    '''
    pass


def addLyricsToBassNote(bassNote, notationString=None):
    '''
    Takes in a bassNote and a corresponding notationString as arguments.
    Adds the parsed notationString as lyrics to the bassNote, which is
    useful when displaying the figured bass in external software.

    >>> from music21.figuredBass import realizer
    >>> n1 = note.Note('G3')
    >>> realizer.addLyricsToBassNote(n1, '6,4')
    >>> n1.lyrics[0].text
    '6'
    >>> n1.lyrics[1].text
    '4'
    >>> #_DOCS_SHOW n1.show()

    .. image:: images/figuredBass/fbRealizer_lyrics.*
        :width: 100
    '''
    pass


class FiguredBassLine:
    '''
    A FiguredBassLine is an interface for realization of a line of (bassNote, notationString) pairs.
    Currently, only 1:1 realization is supported, meaning that every bassNote is realized and the
    :attr:`~music21.note.GeneralNote.quarterLength` or duration of a realization above a bassNote
    is identical to that of the bassNote.


    `inKey` defaults to C major.

    `inTime` defaults to 4/4.

    >>> from music21.figuredBass import realizer
    >>> fbLine = realizer.FiguredBassLine(key.Key('B'), meter.TimeSignature('3/4'))
    >>> fbLine.inKey
    <music21.key.Key of B major>
    >>> fbLine.inTime
    <music21.meter.TimeSignature 3/4>
    '''
    _DOC_ORDER = ['addElement', 'generateBassLine', 'realize']
    _DOC_ATTR: dict[str, str] = {
        'inKey': '''
            A :class:`~music21.key.Key` which implies a scale value,
            scale mode, and key signature for a
            :class:`~music21.figuredBass.realizerScale.FiguredBassScale`.
            ''',
        'inTime': '''
            A :class:`~music21.meter.TimeSignature` which specifies the
            time signature of realizations outputted to a
            :class:`~music21.stream.Score`.
            ''',
    }

    def __init__(self, inKey=None, inTime=None):
        if inKey is None:
            inKey = key.Key('C')
        if inTime is None:
            inTime = meter.TimeSignature('4/4')

        self.inKey = inKey
        self.inTime = inTime
        self._paddingLeft = 0.0
        self._overlaidParts = stream.Part()
        self._fbScale = realizerScale.FiguredBassScale(inKey.pitchFromDegree(1), inKey.mode)
        self._fbList = []

    def addElement(self, bassObject: note.Note, notationString=None):
        '''
        Use this method to add (bassNote, notationString) pairs to the bass line. Elements
        are realized in the order they are added.


        >>> from music21.figuredBass import realizer
        >>> fbLine = realizer.FiguredBassLine(key.Key('B'), meter.TimeSignature('3/4'))
        >>> fbLine.addElement(note.Note('B2'))
        >>> fbLine.addElement(note.Note('C#3'), '6')
        >>> fbLine.addElement(note.Note('D#3'), '6')
        >>> #_DOCS_SHOW fbLine.generateBassLine().show()

        .. image:: images/figuredBass/fbRealizer_bassLine.*
            :width: 200

        OMIT_FROM_DOCS

        >>> fbLine = realizer.FiguredBassLine(key.Key('C'), meter.TimeSignature('4/4'))
        >>> fbLine.addElement(harmony.ChordSymbol('C'))
        >>> fbLine.addElement(harmony.ChordSymbol('G'))

        >>> fbLine = realizer.FiguredBassLine(key.Key('C'), meter.TimeSignature('4/4'))
        >>> fbLine.addElement(roman.RomanNumeral('I'))
        >>> fbLine.addElement(roman.RomanNumeral('V'))
        '''
        pass

    def generateBassLine(self):
        '''
        Generates the bass line as a :class:`~music21.stream.Score`.

        >>> from music21.figuredBass import realizer
        >>> fbLine = realizer.FiguredBassLine(key.Key('B'), meter.TimeSignature('3/4'))
        >>> fbLine.addElement(note.Note('B2'))
        >>> fbLine.addElement(note.Note('C#3'), '6')
        >>> fbLine.addElement(note.Note('D#3'), '6')
        >>> #_DOCS_SHOW fbLine.generateBassLine().show()

        .. image:: images/figuredBass/fbRealizer_bassLine.*
            :width: 200


        >>> sBach = corpus.parse('bach/bwv307')
        >>> sBach.parts.last().measure(0).show('text')
        {0.0} ...
        {0.0} <music21.clef.BassClef>
        {0.0} <music21.key.Key of B- major>
        {0.0} <music21.meter.TimeSignature 4/4>
        {0.0} <music21.note.Note B->
        {0.5} <music21.note.Note C>

        >>> fbLine = realizer.figuredBassFromStream(sBach.parts.last())
        >>> fbLine.generateBassLine().measure(1).show('text')
        {0.0} <music21.clef.BassClef>
        {0.0} <music21.key.KeySignature of 2 flats>
        {0.0} <music21.meter.TimeSignature 4/4>
        {3.0} <music21.note.Note B->
        {3.5} <music21.note.Note C>
        '''
        bassLine = stream.Part()
        bassLine.append(clef.BassClef())
        bassLine.append(key.KeySignature(self.inKey.sharps))
        bassLine.append(copy.deepcopy(self.inTime))
        r = None
        if self._paddingLeft != 0.0:
            r = note.Rest(quarterLength=self._paddingLeft)
            bassLine.append(r)

        for (bassNote, unused_notationString) in self._fbList:
            bassLine.append(bassNote)

        bl2 = bassLine.makeNotation(inPlace=False, cautionaryNotImmediateRepeat=False)
        if r is not None:
            m0 = bl2.getElementsByClass(stream.Measure).first()
            m0.remove(m0.getElementsByClass(note.Rest).first())
            m0.padAsAnacrusis()
        return bl2

    def retrieveSegments(self, fbRules=None, numParts=4, maxPitch=None):
        '''
        generates the segmentList from an fbList, including any overlaid Segments

        if fbRules is None, creates a new rules.Rules() object

        if maxPitch is None, uses pitch.Pitch('B5')
        '''
        if fbRules is None:
            fbRules = rules.Rules()
        if maxPitch is None:
            maxPitch = pitch.Pitch('B5')
        segmentList = []
        bassLine = self.generateBassLine()
        if len(self._overlaidParts) >= 1:
            self._overlaidParts.append(bassLine)
            currentMapping = checker.extractHarmonies(self._overlaidParts)
        else:
            currentMapping = checker.createOffsetMapping(bassLine)
        allKeys = sorted(currentMapping.keys())
        bassLine = bassLine.flatten().notes
        bassNoteIndex = 0
        previousBassNote = bassLine[bassNoteIndex]
        bassNote = currentMapping[allKeys[0]][-1]
        previousSegment = segment.OverlaidSegment(bassNote, bassNote.editorial.notationString,
                                                   self._fbScale,
                                                   fbRules, numParts, maxPitch)
        previousSegment.quarterLength = previousBassNote.quarterLength
        segmentList.append(previousSegment)
        for k in allKeys[1:]:
            (startTime, unused_endTime) = k
            bassNote = currentMapping[k][-1]
            currentSegment = segment.OverlaidSegment(bassNote, bassNote.editorial.notationString,
                                                      self._fbScale,
                                                      fbRules, numParts, maxPitch)
            for partNumber in range(1, len(currentMapping[k])):
                upperPitch = currentMapping[k][partNumber - 1]
                currentSegment.fbRules._partPitchLimits.append((partNumber, upperPitch))
            if startTime == previousBassNote.offset + previousBassNote.quarterLength:
                bassNoteIndex += 1
                previousBassNote = bassLine[bassNoteIndex]
                currentSegment.quarterLength = previousBassNote.quarterLength
            else:
                for partNumber in range(len(currentMapping[k]), numParts + 1):
                    previousSegment.fbRules._partsToCheck.append(partNumber)
                # Fictitious, representative only for harmonies preserved
                # with addition of melody or melodies
                currentSegment.quarterLength = 0.0
            segmentList.append(currentSegment)
            previousSegment = currentSegment
        return segmentList

    def overlayPart(self, music21Part):
        pass

    def realize(self, fbRules=None, numParts=4, maxPitch=None):
        # noinspection PyShadowingNames
        '''
        Creates a :class:`~music21.figuredBass.segment.Segment`
        for each (bassNote, notationString) pair
        added using :meth:`~music21.figuredBass.realizer.FiguredBassLine.addElement`.
        Each Segment is associated
        with the :class:`~music21.figuredBass.rules.Rules` object provided, meaning that rules are
        universally applied across all Segments. The number of parts in a realization
        (including the bass) can be controlled through numParts, and the maximum pitch can
        likewise be controlled through maxPitch.
        Returns a :class:`~music21.figuredBass.realizer.Realization`.

        If this method is called without having provided any (bassNote, notationString) pairs,
        a FiguredBassLineException is raised. If only one pair is provided, the Realization will
        contain :meth:`~music21.figuredBass.segment.Segment.allCorrectConsecutivePossibilities`
        for the one note.

        if `fbRules` is None, creates a new rules.Rules() object

        if `maxPitch` is None, uses pitch.Pitch('B5')

        >>> from music21.figuredBass import realizer
        >>> from music21.figuredBass import rules
        >>> fbLine = realizer.FiguredBassLine(key.Key('B'), meter.TimeSignature('3/4'))
        >>> fbLine.addElement(note.Note('B2'))
        >>> fbLine.addElement(note.Note('C#3'), '6')
        >>> fbLine.addElement(note.Note('D#3'), '6')
        >>> fbRules = rules.Rules()
        >>> r1 = fbLine.realize(fbRules)
        >>> r1.getNumSolutions()
        208
        >>> fbRules.forbidVoiceOverlap = False
        >>> r2 = fbLine.realize(fbRules)
        >>> r2.getNumSolutions()
        7908

        OMIT_FROM_DOCS
        >>> fbLine3 = realizer.FiguredBassLine(key.Key('C'), meter.TimeSignature('2/4'))
        >>> h1 = harmony.ChordSymbol('C')
        >>> h1.bass().octave = 4
        >>> fbLine3.addElement(h1)
        >>> h2 = harmony.ChordSymbol('G')
        >>> h2.bass().octave = 4
        >>> fbLine3.addElement(h2)
        >>> r3 = fbLine3.realize()
        >>> r3.getNumSolutions()
        13
        >>> fbLine4 = realizer.FiguredBassLine(key.Key('C'), meter.TimeSignature('2/4'))
        >>> fbLine4.addElement(roman.RomanNumeral('I'))
        >>> fbLine4.addElement(roman.RomanNumeral('IV'))
        >>> r4 = fbLine4.realize()
        >>> r4.getNumSolutions()
        13

        '''
        if fbRules is None:
            fbRules = rules.Rules()
        if maxPitch is None:
            maxPitch = pitch.Pitch('B5')

        segmentList = []

        listOfHarmonyObjects = False
        for item in self._fbList:
            try:
                c = item.classes
            except AttributeError:
                continue
            if 'Note' in c:
                break
            # Added to accommodate harmony.ChordSymbol and roman.RomanNumeral objects
            if 'RomanNumeral' in c or 'ChordSymbol' in c:
                listOfHarmonyObjects = True
                break

        if listOfHarmonyObjects:
            for harmonyObject in self._fbList:
                listOfPitchesJustNames = []
                for thisPitch in harmonyObject.pitches:
                    listOfPitchesJustNames.append(thisPitch.name)
                # remove duplicates just in case
                d = {}
                for x in listOfPitchesJustNames:
                    d[x] = x
                outputList = d.values()

                def g(y):
                    return y if y != 0.0 else 1.0

                passedNote = note.Note(harmonyObject.bass().nameWithOctave,
                                       quarterLength=g(harmonyObject.duration.quarterLength))
                correspondingSegment = segment.Segment(bassNote=passedNote,
                                                       fbScale=self._fbScale,
                                                       fbRules=fbRules,
                                                       numParts=numParts,
                                                       maxPitch=maxPitch,
                                                       listOfPitches=outputList)
                correspondingSegment.quarterLength = g(harmonyObject.duration.quarterLength)
                segmentList.append(correspondingSegment)
        # ---------- Original code - Accommodates a tuple (figured bass)  --------
        else:
            segmentList = self.retrieveSegments(fbRules, numParts, maxPitch)

        if len(segmentList) >= 2:
            for segmentIndex in range(len(segmentList) - 1):
                segmentA = segmentList[segmentIndex]
                segmentB = segmentList[segmentIndex + 1]
                correctAB = segmentA.allCorrectConsecutivePossibilities(segmentB)
                segmentA.movements = collections.defaultdict(list)
                listAB = list(correctAB)
                for (possibA, possibB) in listAB:
                    segmentA.movements[possibA].append(possibB)
            self._trimAllMovements(segmentList)
        elif len(segmentList) == 1:
            segmentA = segmentList[0]
            segmentA.correctA = list(segmentA.allCorrectSinglePossibilities())
        elif not segmentList:
            raise FiguredBassLineException('No (bassNote, notationString) pairs to realize.')

        return Realization(realizedSegmentList=segmentList, inKey=self.inKey,
                           inTime=self.inTime, overlaidParts=self._overlaidParts[0:-1],
                           paddingLeft=self._paddingLeft)

    def _trimAllMovements(self, segmentList):
        '''
        Each :class:`~music21.figuredBass.segment.Segment` which resolves to another
        defines a list of movements, nextMovements. Keys for nextMovements are correct
        single possibilities of the current Segment. For a given key, a value is a list
        of correct single possibilities in the subsequent Segment representing acceptable
        movements between the two. There may be movements in a string of Segments which
        directly or indirectly lead nowhere. This method is designed to be called on
        a list of Segments **after** movements are found, as happens in
        :meth:`~music21.figuredBass.realizer.FiguredBassLine.realize`.
        '''
        if len(segmentList) == 1 or len(segmentList) == 2:
            return True
        elif len(segmentList) >= 3:
            segmentList.reverse()
            # gets this wrong  # pylint: disable=cell-var-from-loop
            movementsAB = None
            for segmentIndex in range(1, len(segmentList) - 1):
                movementsAB = segmentList[segmentIndex + 1].movements
                movementsBC = segmentList[segmentIndex].movements
                # eliminated = []
                for (possibB, possibCList) in list(movementsBC.items()):
                    if not possibCList:
                        del movementsBC[possibB]
                for (possibA, possibBList) in list(movementsAB.items()):
                    movementsAB[possibA] = list(
                        filter(lambda possibBB: (possibBB in movementsBC), possibBList))

            for (possibA, possibBList) in list(movementsAB.items()):
                if not possibBList:
                    del movementsAB[possibA]

            segmentList.reverse()
            return True


class Realization:
    '''
    Returned by :class:`~music21.figuredBass.realizer.FiguredBassLine` after calling
    :meth:`~music21.figuredBass.realizer.FiguredBassLine.realize`. Allows for the
    generation of realizations as a :class:`~music21.stream.Score`.


    * See the :mod:`~music21.figuredBass.examples` module for examples on the generation
      of realizations.
    * A possibility progression is a valid progression through a string of
      :class:`~music21.figuredBass.segment.Segment` instances.
      See :mod:`~music21.figuredBass.possibility` for more details on possibilities.
    '''
    _DOC_ORDER = ['getNumSolutions', 'generateRandomRealization',
                  'generateRandomRealizations', 'generateAllRealizations',
                  'getAllPossibilityProgressions', 'getRandomPossibilityProgression',
                  'generateRealizationFromPossibilityProgression']
    _DOC_ATTR: dict[str, str] = {
        'keyboardStyleOutput': '''
            True by default. If True, generated realizations
            are represented in keyboard style, with two staves. If False,
            realizations are represented in chorale style with n staves,
            where n is the number of parts. SATB if n = 4.''',
    }

    def __init__(self, **fbLineOutputs):
        # fbLineOutputs always will have three elements, checks are for sphinx documentation only.
        if 'realizedSegmentList' in fbLineOutputs:
            self._segmentList = fbLineOutputs['realizedSegmentList']
        if 'inKey' in fbLineOutputs:
            self._inKey = fbLineOutputs['inKey']
            self._keySig = key.KeySignature(self._inKey.sharps)
        if 'inTime' in fbLineOutputs:
            self._inTime = fbLineOutputs['inTime']
        if 'overlaidParts' in fbLineOutputs:
            self._overlaidParts = fbLineOutputs['overlaidParts']
        if 'paddingLeft' in fbLineOutputs:
            self._paddingLeft = fbLineOutputs['paddingLeft']
        self.keyboardStyleOutput = True

    def getNumSolutions(self):
        '''
        Returns the number of solutions (unique realizations) to a Realization by calculating
        the total number of paths through a string of :class:`~music21.figuredBass.segment.Segment`
        movements. This is faster and more efficient than compiling each unique realization into a
        list, adding it to a master list, and then taking the length of the master list.

        >>> from music21.figuredBass import examples
        >>> fbLine = examples.exampleB()
        >>> fbRealization = fbLine.realize()
        >>> fbRealization.getNumSolutions()
        422
        >>> fbLine2 = examples.exampleC()
        >>> fbRealization2 = fbLine2.realize()
        >>> fbRealization2.getNumSolutions()
        833
        '''
        pass

    def getAllPossibilityProgressions(self):
        '''
        Compiles each unique possibility progression, adding
        it to a master list. Returns the master list.


        .. warning:: This method is unoptimized, and may take a prohibitive amount
            of time for a Realization which has more than 200,000 solutions.
        '''
        pass

    def getRandomPossibilityProgression(self):
        '''
        Returns a random unique possibility progression.
        '''
        pass

    def generateRealizationFromPossibilityProgression(self, possibilityProgression):
        '''
        Generates a realization as a :class:`~music21.stream.Score` given a possibility progression.
        '''
        pass

    def generateAllRealizations(self):
        '''
        Generates all unique realizations as a :class:`~music21.stream.Score`.


        .. warning:: This method is unoptimized, and may take a prohibitive amount
            of time for a Realization which has more than 100 solutions.
        '''
        pass

    def generateRandomRealization(self):
        '''
        Generates a random unique realization as a :class:`~music21.stream.Score`.
        '''
        pass

    def generateRandomRealizations(self, amountToGenerate=20):
        '''
        Generates *amountToGenerate* unique realizations as a :class:`~music21.stream.Score`.


        .. warning:: This method is unoptimized, and may take a prohibitive amount
            of time if amountToGenerate is more than 100.
        '''
        pass


_DOC_ORDER = [figuredBassFromStream, addLyricsToBassNote,
              FiguredBassLine, Realization]


class FiguredBassLineException(exceptions21.Music21Exception):
    pass

# ------------------------------------------------------------------------------


class Test(unittest.TestCase):
    def testMultipleFiguresInLyric(self):
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

