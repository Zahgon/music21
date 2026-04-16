# ------------------------------------------------------------------------------
# Name:         serial.py
# Purpose:      music21 classes for serial transformations
#
# Authors:      Michael Scott Asato Cuthbert
#               Christopher Ariza
#
# Copyright:    Copyright © 2009-2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
This module defines objects for defining and manipulating structures
common to serial and/or twelve-tone music,
including :class:`~music21.serial.ToneRow` subclasses.

Serial searching methods that were previously here have been moved to
:mod:`~music21.search.serial`.
'''
from __future__ import annotations

import typing as t
import unittest

from music21 import chord
from music21 import environment
from music21 import exceptions21
from music21 import note
from music21 import pitch
from music21 import stream

environLocal = environment.Environment('serial')


# ------------------------------------------------------------------------------
class SerialException(exceptions21.Music21Exception):
    pass


# ------------------------------------------------------------------------------
class TwelveToneMatrix(stream.Stream):
    '''
    An object representation of a 2-dimensional array of 12 pitches.
    Internal representation is as a :class:`~music21.stream.Stream`,
    which stores 12 Streams, each Stream a horizontal row of pitches
    in the matrix.

    This object is commonly used by calling the
    :meth:`~music21.stream.TwelveToneRow.matrix` method of
    :class:`~music21.stream.TwelveToneRow` (or a subclass).

    >>> ttr = serial.TwelveToneRow([0, 2, 11, 7, 8, 3, 9, 1, 4, 10, 6, 5])
    >>> aMatrix = ttr.matrix()
    >>> print(aMatrix)
      0  2  B  7  8  3  9  1  4  A  6  5
      A  0  9  5  6  1  7  B  2  8  4  3
      1  3  0  8  9  4  A  2  5  B  7  6
      5  7  4  0  1  8  2  6  9  3  B  A
      4  6  3  B  0  7  1  5  8  2  A  9
      9  B  8  4  5  0  6  A  1  7  3  2
      3  5  2  A  B  6  0  4  7  1  9  8
      B  1  A  6  7  2  8  0  3  9  5  4
      8  A  7  3  4  B  5  9  0  6  2  1
      2  4  1  9  A  5  B  3  6  0  8  7
      6  8  5  1  2  9  3  7  A  4  0  B
      7  9  6  2  3  A  4  8  B  5  1  0

    >>> repr(aMatrix)
    '<music21.serial.TwelveToneMatrix for [<music21.serial.TwelveToneRow row-1>]>'

    >>> fourthQuartetMatrix = serial.getHistoricalRowByName('SchoenbergOp37').matrix()
    >>> repr(fourthQuartetMatrix)
    '<music21.serial.TwelveToneMatrix for
         [<music21.serial.HistoricalTwelveToneRow Schoenberg Op. 37 Fourth String Quartet>]>'
    '''

    def __str__(self):
        '''
        Return a string representation of the matrix.
        '''
        ret = []
        for rowForm in self:
            msg = []
            for n in rowForm:
                msg.append(str(n.pitch.pitchClassString).rjust(3))
            ret.append(''.join(msg))
        return '\n'.join(ret)

    def _reprInternal(self):
        pass
# ------------------------------------------------------------------------------


# noinspection SpellCheckingInspection
historicalDict = {
    'WebernOp29': ('Webern', 'Op. 29', 'Cantata I',
                        [3, 11, 2, 1, 5, 4, 7, 6, 10, 9, 0, 8]),
    'WebernOp28': ('Webern', 'Op. 28', 'String Quartet',
                        [1, 0, 3, 2, 6, 7, 4, 5, 9, 8, 11, 10]),
    'SchoenbergOp24Mvmt5': ('Schoenberg', 'Op. 24', 'Serenade, Mvt. 5, "Tanzscene"',
                                 [9, 10, 0, 3, 4, 6, 5, 7, 8, 11, 1, 2]),
    'SchoenbergOp24Mvmt4': ('Schoenberg', 'Op. 24', 'Serenade, Mvt. 4, "Sonett"',
                                 [4, 2, 3, 11, 0, 1, 8, 6, 9, 5, 7, 10]),
    'SchoenbergJakobsleiter': ('Schoenberg', None, 'Die Jakobsleiter',
                                    [1, 2, 5, 4, 8, 7, 0, 3, 11, 10, 6, 9]),
    'SchoenbergOp27No4': ('Schoenberg', 'Op. 27 No. 4', 'Four Pieces for Mixed Chorus, No. 4',
                               [1, 3, 10, 6, 8, 4, 11, 0, 2, 9, 5, 7]),
    'WebernOp23': ('Webern', 'Op. 23', 'Three Songs',
                        [8, 3, 7, 4, 10, 6, 2, 5, 1, 0, 9, 11]),
    'BergLuluActIIScene1': ('Berg', 'Lulu, Act II, Scene 1',
                                 'Perm. (Every 5th Note Of Transposed Primary Row)',
                                 [10, 7, 1, 0, 9, 2, 4, 11, 5, 8, 3, 6]),
    'SchoenbergOp27No1': ('Schoenberg', 'Op. 27 No. 1', 'Four Pieces for Mixed Chorus, No. 1',
                               [6, 5, 2, 8, 7, 1, 3, 4, 10, 9, 11, 0]),
    'BergLuluActIScene20': ('Berg', 'Lulu, Act I , Scene XX',
                                 'Perm. (Every 7th Note Of Transposed Primary Row)',
                                 [10, 6, 3, 8, 5, 11, 4, 2, 9, 0, 1, 7]),
    'SchoenbergOp27No3': ('Schoenberg', 'Op. 27 No. 3', 'Four Pieces for Mixed Chorus, No. 3',
                               [7, 6, 2, 4, 5, 3, 11, 0, 8, 10, 9, 1]),
    'SchoenbergOp27No2': ('Schoenberg', 'Op. 27 No. 2', 'Four Pieces for Mixed Chorus, No. 2',
                               [0, 11, 4, 10, 2, 8, 3, 7, 6, 5, 9, 1]),
    'SchoenbergFragPiano': ('Schoenberg', None, 'Fragment For Piano',
                                 [6, 9, 0, 7, 1, 2, 8, 11, 5, 10, 4, 3]),
    'SchoenbergOp50B': ('Schoenberg', 'Op. 50B', 'De Profundis',
                             [3, 9, 8, 4, 2, 10, 7, 11, 0, 6, 5, 1]),
    'SchoenbergOp50C': ('Schoenberg', 'Op. 50C', 'Modern Psalms, The First Psalm',
                             [4, 3, 0, 8, 11, 7, 5, 9, 6, 10, 1, 2]),
    'SchoenbergOp50A': ('Schoenberg', 'Op. 50A', 'Three Times A Thousand Years',
                             [7, 9, 6, 4, 5, 11, 10, 2, 0, 1, 3, 8]),
    'SchoenbergMosesAron': ('Schoenberg', None, 'Moses And Aron',
                                 [9, 10, 4, 2, 3, 1, 7, 5, 6, 8, 11, 0]),
    'WebernOp25': ('Webern', 'Op. 25', 'Three Songs',
                        [7, 4, 3, 6, 1, 5, 2, 11, 10, 0, 9, 8]),
    'SchoenbergOp23No5': ('Schoenberg', 'Op. 23, No. 5', 'Five Piano Pieces',
                               [1, 9, 11, 7, 8, 6, 10, 2, 4, 3, 0, 5]),
    'SchoenbergOp28No1': ('Schoenberg', 'Op. 28 No. 1',
                               'Three Satires for Mixed Chorus, No. 1',
                               [0, 4, 7, 1, 9, 11, 5, 3, 2, 6, 8, 10]),
    'SchoenbergOp28No3': ('Schoenberg', 'Op. 28 No. 3',
                               'Three Satires for Mixed Chorus, No. 3',
                               [5, 6, 4, 8, 2, 10, 7, 9, 3, 11, 1, 0]),
    'WebernOp21': ('Webern', 'Op. 21', 'Chamber Symphony',
                        [5, 8, 7, 6, 10, 9, 3, 4, 0, 1, 2, 11]),
    'SchoenbergIsraelExists': ('Schoenberg', None, 'Israel Exists Again',
                                    [0, 3, 4, 9, 11, 5, 2, 1, 10, 8, 6, 7]),
    'SchoenbergOp35No2': ('Schoenberg', 'Op. 35', 'Six Pieces for Male Chorus, No. 2',
                               [6, 9, 7, 1, 0, 2, 5, 11, 10, 3, 4, 8]),
    'SchoenbergOp35No3': ('Schoenberg', 'Op. 35', 'Six Pieces for Male Chorus, No. 3',
                               [3, 6, 7, 8, 5, 0, 9, 10, 4, 11, 2, 1]),
    'SchoenbergOp35No1': ('Schoenberg', 'Op. 35', 'Six Pieces for Male Chorus, No. 1',
                               [2, 11, 3, 5, 4, 1, 8, 10, 9, 6, 0, 7]),
    'SchoenbergOp48No1': ('Schoenberg', 'Op. 48', 'Three Songs, No. 1, "Sommermud"',
                               [1, 2, 0, 6, 3, 5, 4, 10, 11, 7, 9, 8]),
    'SchoenbergOp35No5': ('Schoenberg', 'Op. 35', 'Six Pieces for Male Chorus, No. 5',
                               [1, 7, 10, 2, 3, 11, 8, 4, 0, 6, 5, 9]),
    'SchoenbergOp29': ('Schoenberg', 'Op. 29', 'Suite',
                            [3, 7, 6, 10, 2, 11, 0, 9, 8, 4, 5, 1]),
    'BergLyricSuitePerm': ('Berg', None, 'Lyric Suite, Last Mvt. Permutation',
                                [5, 6, 10, 4, 1, 9, 2, 8, 7, 3, 0, 11]),
    'WebernOp20': ('Webern', 'Op. 20', 'String Trio',
                        [8, 7, 2, 1, 6, 5, 9, 10, 3, 4, 0, 11]),
    'SchoenbergOp46': ('Schoenberg', 'Op. 46', 'A Survivor From Warsaw',
                            [6, 7, 0, 8, 4, 3, 11, 10, 5, 9, 1, 2]),
    'SchoenbergFragOrganSonata': ('Schoenberg', None, 'Fragment of Sonata For Organ',
                                       [1, 7, 11, 3, 9, 2, 8, 6, 10, 5, 0, 4]),
    'SchoenbergOp44': ('Schoenberg', 'Op. 44', 'Prelude To A Suite From "Genesis"',
                            [10, 6, 2, 5, 4, 0, 11, 8, 1, 3, 9, 7]),
    'SchoenbergOp45': ('Schoenberg', 'Op. 45', 'String Trio',
                            [2, 10, 3, 9, 4, 1, 11, 8, 6, 7, 5, 0]),
    'SchoenbergOp33A': ('Schoenberg', 'Op. 33A', 'Two Piano Pieces, No. 1',
                             [10, 5, 0, 11, 9, 6, 1, 3, 7, 8, 2, 4]),
    'SchoenbergOp25': ('Schoenberg', 'Op.25', 'Suite for Piano',
                            [4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10]),
    'SchoenbergOp26': ('Schoenberg', 'Op. 26', 'Wind Quintet',
                            [3, 7, 9, 11, 1, 0, 10, 2, 4, 6, 8, 5]),
    'SchoenbergOp33B': ('Schoenberg', 'Op. 33B', 'Two Piano Pieces, No. 2',
                             [11, 1, 5, 3, 9, 8, 6, 10, 7, 4, 0, 2]),
    'BergViolinConcerto': ('Berg', None, 'Concerto For Violin And Orchestra',
                                [7, 10, 2, 6, 9, 0, 4, 8, 11, 1, 3, 5]),
    'WebernOp22': ('Webern', 'Op. 22', 'Quartet For Violin, Clarinet, Tenor Sax, And Piano',
                        [6, 3, 2, 5, 4, 8, 9, 10, 11, 1, 7, 0]),
    'BergLulu': ('Berg', None, 'Lulu: Primary Row',
                        [0, 4, 5, 2, 7, 9, 6, 8, 11, 10, 3, 1]),
    'WebernOp30': ('Webern', 'Op. 30', 'Variations For Orchestra',
                        [9, 10, 1, 0, 11, 2, 3, 6, 5, 4, 7, 8]),
    'WebernOp31': ('Webern', 'Op. 31', 'Cantata II',
                        [6, 9, 5, 4, 8, 3, 7, 11, 10, 2, 1, 0]),
    'WebernOpNo17No1': ('Webern', 'Op. 17, No. 1', '"Armer Sunder, Du"',
                             [11, 10, 5, 6, 3, 4, 7, 8, 9, 0, 1, 2]),
    'WebernOp24': ('Webern', 'Op. 24', 'Concerto For Nine Instruments',
                        [11, 10, 2, 3, 7, 6, 8, 4, 5, 0, 1, 9]),
    'SchoenbergOp48No2': ('Schoenberg', 'Op. 48', 'Three Songs, No. 2, "Tot"',
                               [2, 3, 9, 1, 10, 4, 8, 7, 0, 11, 5, 6]),
    'WebernOp27': ('Webern', 'Op. 27', 'Variations For Piano',
                        [3, 11, 10, 2, 1, 0, 6, 4, 7, 5, 9, 8]),
    'SchoenbergOp47': ('Schoenberg', 'Op. 47', 'Fantasy For Violin And Piano',
                            [10, 9, 1, 11, 5, 7, 3, 4, 0, 2, 8, 6]),
    'WebernOp19No2': ('Webern', 'Op. 19, No. 2', '"Ziehn Die Schafe"',
                           [8, 4, 9, 6, 7, 0, 11, 5, 3, 2, 10, 1]),
    'WebernOp19No1': ('Webern', 'Op. 19, No. 1', '"Weiss Wie Lilien"',
                           [7, 10, 6, 5, 3, 9, 8, 1, 2, 11, 4, 0]),
    'WebernOp26': ('Webern', 'Op. 26', 'Das Augenlicht',
                        [8, 10, 9, 0, 11, 3, 4, 1, 5, 2, 6, 7]),
    'SchoenbergFragPianoPhantasia': ('Schoenberg', None, 'Fragment of Phantasia For Piano',
                                          [1, 5, 3, 6, 4, 8, 0, 11, 2, 9, 10, 7]),
    'BergDerWein': ('Berg', None, 'Der Wein',
                         [2, 4, 5, 7, 9, 10, 1, 6, 8, 0, 11, 3]),
    'BergWozzeckPassacaglia': ('Berg', None, 'Wozzeck, Act I, Scene 4 "Passacaglia"',
                                    [3, 11, 7, 1, 0, 6, 4, 10, 9, 5, 8, 2]),
    'WebernOp18No1': ('Webern', 'Op. 18, No. 1', '"Schatzerl Klein"',
                           [0, 11, 5, 8, 10, 9, 3, 4, 1, 7, 2, 6]),
    'WebernOp18No2': ('Webern', 'Op. 18, No. 2', '"Erlosung"',
                           [6, 9, 5, 8, 4, 7, 3, 11, 2, 10, 1, 0]),
    'WebernOp18No3': ('Webern', 'Op. 18, No. 3', '"Ave, Regina Coelorum"',
                           [4, 3, 7, 6, 5, 11, 10, 2, 1, 0, 9, 8]),
    'SchoenbergOp42': ('Schoenberg', 'Op. 42', 'Concerto For Piano And Orchestra',
                            [3, 10, 2, 5, 4, 0, 6, 8, 1, 9, 11, 7]),
    'SchoenbergOp48No3': ('Schoenberg', 'Op. 48', 'Three Songs, No, 3, "Madchenlied"',
                               [1, 7, 9, 11, 3, 5, 10, 6, 4, 0, 8, 2]),
    'SchoenbergOp37': ('Schoenberg', 'Op. 37', 'Fourth String Quartet',
                            [2, 1, 9, 10, 5, 3, 4, 0, 8, 7, 6, 11]),
    'SchoenbergOp36': ('Schoenberg', 'Op. 36', 'Concerto for Violin and Orchestra',
                            [9, 10, 3, 11, 4, 6, 0, 1, 7, 8, 2, 5]),
    'SchoenbergOp34': ('Schoenberg', 'Op. 34', 'Accompaniment to a Film Scene',
                            [3, 6, 2, 4, 1, 0, 9, 11, 10, 8, 5, 7]),
    'BergChamberConcerto': ('Berg', None, 'Chamber Concerto',
                                 [11, 7, 5, 9, 2, 3, 6, 8, 0, 1, 4, 10]),
    'SchoenbergOp32': ('Schoenberg', 'Op. 32', 'Von Heute Auf Morgen',
                            [2, 3, 9, 1, 11, 5, 8, 7, 4, 0, 10, 6]),
    'SchoenbergOp31': ('Schoenberg', 'Op. 31', 'Variations for Orchestra',
                            [10, 4, 6, 3, 5, 9, 2, 1, 7, 8, 11, 0]),
    'SchoenbergOp30': ('Schoenberg', 'Op. 30', 'Third String Quartet',
                            [7, 4, 3, 9, 0, 5, 6, 11, 10, 1, 8, 2]),
    'BergLyricSuite': ('Berg', None, 'Lyric Suite Primary Row',
                            [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]),
    'SchoenbergOp41': ('Schoenberg', 'Op. 41', 'Ode To Napoleon',
                            [1, 0, 4, 5, 9, 8, 3, 2, 6, 7, 11, 10]),
    'WebernOp17No3': ('Webern', 'Op. 17, No. 3', '"Heiland, Unsere Missetaten..."',
                           [8, 5, 4, 3, 7, 6, 0, 1, 2, 11, 10, 9]),
    'WebernOp17No2': ('Webern', 'Op. 17, No. 2', '"Liebste Jungfrau"',
                           [1, 0, 11, 7, 8, 2, 3, 6, 5, 4, 9, 10])
}

# ------------------------------------------------------------------------------


class ToneRow(stream.Stream):
    '''
    A Stream representation of a tone row, or an ordered sequence of pitches;
    can most importantly be used to deal with
    serial transformations.

    Unlike a normal Stream, the first argument is assumed to be a ToneRow:

    >>> toneRow = serial.ToneRow([10, 9, 4, 5, 6, 3, 2, 8, 7, 11, 0, 1])

    The representation of a ToneRow will be the contents:

    >>> toneRow
    <music21.serial.ToneRow A94563287B01>

    Unless (like a Stream), the id is set:

    >>> toneRow.id = 'retrograde_jungfrau'
    >>> toneRow
    <music21.serial.ToneRow retrograde_jungfrau>

    A ToneRow does not need to have twelve pitches, like this ten-tone row
    from Ruth Crawford Seeger's String Quartet 1931

    >>> rcsRow = serial.ToneRow([2, 4, 5, 3, 6, 9, 8, 7, 1, 0])
    >>> rcsRow
    <music21.serial.ToneRow 2453698710>
    >>> len(rcsRow)
    10
    '''
    _DOC_ATTR: dict[str, str] = {
        'row': 'A list representing the pitch class values of the row.',
    }

    _DOC_ORDER = ['pitchClasses', 'noteNames', 'isTwelveToneRow', 'isSameRow',
                  'getIntervalsAsString',
                  'zeroCenteredTransformation', 'originalCenteredTransformation',
                  'findZeroCenteredTransformations', 'findOriginalCenteredTransformations']

    def __init__(self, row=None, **keywords):
        super().__init__(**keywords)
        if row is not None:
            self.row = row
        else:
            self.row = []

        for pc in self.row:
            if not isinstance(pc, (pitch.Pitch, note.Note)):
                pc = pitch.Pitch(pc)

            if not isinstance(pc, note.Note):
                n = note.Note(pitch=pc)
            else:
                n = pc

            n.pitch.octave = None
            self.append(n)

    def _reprInternal(self):
        pass

    def pitchClasses(self):
        '''
        Convenience function showing the pitch classes of a
        :class:`~music21.serial.ToneRow` as a list.

        >>> fiveFold = [5 * i for i in range(12)]
        >>> fiveFold
        [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

        >>> quintupleRow = serial.pcToToneRow(fiveFold)
        >>> quintupleRow
        <music21.serial.TwelveToneRow 05A3816B4927>
        >>> quintupleRow.pitchClasses()
        [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7]

        >>> halfStep = serial.pcToToneRow([0, 1])
        >>> halfStep.pitchClasses()
        [0, 1]
        '''
        pitchList = [n.pitch.pitchClass for n in self]
        return pitchList

    def noteNames(self):
        '''
        Convenience function showing the note names of a
        :class:`~music21.serial.ToneRow` as a list.

        >>> chromatic = serial.TwelveToneRow(range(12))
        >>> chromatic.noteNames()
        ['C', 'C#', 'D', 'E-', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B-', 'B']

        >>> halfStep = serial.ToneRow([0, 1])
        >>> halfStep.noteNames()
        ['C', 'C#']
        '''
        pass

    def isTwelveToneRow(self):
        '''
        Describes whether a :class:`~music21.serial.ToneRow` constitutes
        a twelve-tone row. Note that a
        :class:`~music21.serial.TwelveToneRow` object might not be a twelve-tone row.

        >>> serial.ToneRow([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]).isTwelveToneRow()
        True
        >>> serial.ToneRow([0, 4, 8]).isTwelveToneRow()
        False
        >>> serial.ToneRow([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]).isTwelveToneRow()
        False
        '''
        pass

    def makeTwelveToneRow(self):
        # noinspection PyShadowingNames
        '''
        Convenience function returning a :class:`~music21.serial.TwelveToneRow` with the
        same pitches.
        Note that a :class:`~music21.serial.ToneRow` may be created without being a
        true twelve tone row.

        >>> r1 = serial.pcToToneRow(range(11))
        >>> type(r1)
        <class 'music21.serial.ToneRow'>
        >>> n = note.Note()
        >>> n.pitch.pitchClass = 11
        >>> r1.append(n)
        >>> r2 = r1.makeTwelveToneRow()
        >>> type(r2)
        <class 'music21.serial.TwelveToneRow'>
        '''
        pass

    def isSameRow(self, other):
        '''
        Convenience function describing if two rows are the same.

        >>> row1 = serial.pcToToneRow([6, 7, 8])
        >>> row2 = serial.pcToToneRow([-6, 19, 128])
        >>> row3 = serial.pcToToneRow([6, 7, -8])
        >>> row1.isSameRow(row2)
        True
        >>> row2.isSameRow(row1)
        True
        >>> row1.isSameRow(row3)
        False
        '''
        pass

    def getIntervalsAsString(self):
        '''

        Returns the string of intervals between consecutive pitch classes of
        a :class:`~music21.serial.ToneRow`.
        'T' = 10, 'E' = 11.

        >>> cRow = serial.pcToToneRow([0])
        >>> cRow.getIntervalsAsString()
        ''
        >>> reverseChromatic = serial.pcToToneRow([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
        >>> reverseChromatic.getIntervalsAsString()
        'EEEEEEEEEEE'
        '''
        numPitches = len(self)
        pitchList = self.pitchClasses()
        intervalString = ''
        for i in range(numPitches - 1):
            interval = (pitchList[i + 1] - pitchList[i]) % 12
            if interval in range(10):
                intervalString = intervalString + str(interval)
            if interval == 10:
                intervalString = intervalString + 'T'
            if interval == 11:
                intervalString = intervalString + 'E'
        return intervalString

    def zeroCenteredTransformation(self, transformationType, index):
        '''
        Returns a :class:`~music21.serial.ToneRow` giving a transformation of a tone row.
        Admissible transformationTypes are 'P' (prime), 'I' (inversion),
        'R' (retrograde), and 'RI' (retrograde inversion).

        In the "zero-centered" convention,
        the transformations Pn and In start on the pitch class n, and the transformations
        Rn and RIn end on the pitch class n.

        >>> chromatic = serial.pcToToneRow(range(12))
        >>> chromatic.pitchClasses()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        >>> chromaticP3 = chromatic.zeroCenteredTransformation('P',3)
        >>> chromaticP3.pitchClasses()
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]
        >>> chromaticI6 = chromatic.zeroCenteredTransformation('I',6)
        >>> chromaticI6.pitchClasses()
        [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]
        >>> schoenberg = serial.getHistoricalRowByName('SchoenbergOp26')
        >>> schoenberg.pitchClasses()
        [3, 7, 9, 11, 1, 0, 10, 2, 4, 6, 8, 5]
        >>> schoenbergR8 = schoenberg.zeroCenteredTransformation('R',8)
        >>> schoenbergR8.pitchClasses()
        [10, 1, 11, 9, 7, 3, 5, 6, 4, 2, 0, 8]
        >>> schoenbergRI9 = schoenberg.zeroCenteredTransformation('RI',9)
        >>> schoenbergRI9.noteNames()
        ['G', 'E', 'F#', 'G#', 'B-', 'D', 'C', 'B', 'C#', 'E-', 'F', 'A']
        '''
        numPitches = len(self)
        pitchList = self.pitchClasses()
        if int(index) != index:
            raise SerialException('Transformation must be by an integer.')

        firstPitch = pitchList[0]
        transformedPitchList = []
        if transformationType in ('P', 'T'):
            for i in range(numPitches):
                newPitch = (pitchList[i] - firstPitch + index) % 12
                transformedPitchList.append(newPitch)
        elif transformationType == 'I':
            for i in range(numPitches):
                newPitch = (index + firstPitch - pitchList[i]) % 12
                transformedPitchList.append(newPitch)
        elif transformationType == 'R':
            for i in range(numPitches):
                newPitch = (index + pitchList[numPitches - 1 - i] - firstPitch) % 12
                transformedPitchList.append(newPitch)
        elif transformationType == 'RI':
            for i in range(numPitches):
                newPitch = (index - pitchList[numPitches - 1 - i] + firstPitch) % 12
                transformedPitchList.append(newPitch)
        else:
            raise SerialException(f'Invalid transformation type: {transformationType}')

        return pcToToneRow(transformedPitchList)

    def originalCenteredTransformation(self, transformationType: str, index: int):
        '''
        Returns a :class:`~music21.serial.ToneRow` giving a transformation of a tone row.
        Admissible transformations are 'T' (transposition), 'I' (inversion),
        'R' (retrograde), and 'RI' (retrograde inversion).

        In the "original-centered" convention,
        which is less common than the "zero-centered" convention, the original row is not initially
        transposed to start on the pitch class 0. Thus, the transformation Tn transposes
        the original row up by n semitones, and the transformations In, Rn, and RIn first
        transform the row appropriately (without transposition), then transpose the resulting
        row by n semitones.


        >>> chromatic = serial.pcToToneRow(range(12))
        >>> chromatic.pitchClasses()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        >>> chromaticP3 = chromatic.originalCenteredTransformation('T',3)
        >>> chromaticP3.pitchClasses()
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]
        >>> chromaticI6 = chromatic.originalCenteredTransformation('I',6)
        >>> chromaticI6.pitchClasses()
        [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]
        >>> schoenberg = serial.getHistoricalRowByName('SchoenbergOp26')
        >>> schoenberg.pitchClasses()
        [3, 7, 9, 11, 1, 0, 10, 2, 4, 6, 8, 5]
        >>> schoenbergR8 = schoenberg.originalCenteredTransformation('R',8)
        >>> schoenbergR8.pitchClasses()
        [1, 4, 2, 0, 10, 6, 8, 9, 7, 5, 3, 11]
        >>> schoenbergRI9 = schoenberg.originalCenteredTransformation('RI',9)
        >>> schoenbergRI9.noteNames()
        ['B-', 'G', 'A', 'B', 'C#', 'F', 'E-', 'D', 'E', 'F#', 'G#', 'C']
        '''
        pass

    def findZeroCenteredTransformations(self, otherRow) -> t.Union[bool, list[t.Any]]:
        '''
        Gives the list of zero-centered serial transformations
        taking one :class:`~music21.serial.ToneRow`
        to another, the second specified in the argument. Each transformation is given as a
        tuple of the transformation type and index.

        See :meth:`~music21.serial.ToneRow.zeroCenteredTransformation` for
        an explanation of this convention.


        >>> chromatic = serial.pcToToneRow([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1])
        >>> reverseChromatic = serial.pcToToneRow([8, 7, 6, 5, 4, 3, 2, 1, 0, 11, 10, 9])
        >>> chromatic.findZeroCenteredTransformations(reverseChromatic)
        [('I', 8), ('R', 9)]
        >>> schoenberg25 = serial.getHistoricalRowByName('SchoenbergOp25')
        >>> schoenberg26 = serial.pcToToneRow(serial.getHistoricalRowByName(
        ...                                        'SchoenbergOp26').row)
        >>> schoenberg25.findZeroCenteredTransformations(schoenberg26)
        []
        >>> schoenberg26.findZeroCenteredTransformations(
        ...     schoenberg26.zeroCenteredTransformation('RI', 8))
        [('RI', 8)]
        '''
        if len(self) != len(otherRow):
            return False

        otherRowPitches = otherRow.pitchClasses()
        transformationList = []
        firstPitch = otherRowPitches[0]
        lastPitch = otherRowPitches[-1]

        if otherRowPitches == self.zeroCenteredTransformation('P', firstPitch).pitchClasses():
            transformation = 'P', firstPitch
            transformationList.append(transformation)
        if otherRowPitches == self.zeroCenteredTransformation('I', firstPitch).pitchClasses():
            transformation = 'I', firstPitch
            transformationList.append(transformation)
        if otherRowPitches == self.zeroCenteredTransformation('R', lastPitch).pitchClasses():
            transformation = 'R', lastPitch
            transformationList.append(transformation)
        if otherRowPitches == self.zeroCenteredTransformation('RI', lastPitch).pitchClasses():
            transformation = 'RI', lastPitch
            transformationList.append(transformation)

        return transformationList

    def findOriginalCenteredTransformations(self, otherRow):
        '''
        Gives the list of original-centered serial transformations taking one
        :class:`~music21.serial.ToneRow`
        to another, the second specified in the argument. Each transformation is given as a tuple
        of the transformation type and index.

        See :meth:`~music21.serial.ToneRow.originalCenteredTransformation` for an
        explanation of this convention.

        >>> chromatic = serial.pcToToneRow(       [2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B',   0, 1])
        >>> reverseChromatic = serial.pcToToneRow([8, 7, 6, 5, 4, 3, 2, 1, 0,   'B', 'A', 9])
        >>> chromatic.findOriginalCenteredTransformations(reverseChromatic)
        [('I', 6), ('R', 7)]
        >>> schoenberg25 = serial.getHistoricalRowByName('SchoenbergOp25')
        >>> schoenberg26 = serial.getHistoricalRowByName('SchoenbergOp26')
        >>> schoenberg25.findOriginalCenteredTransformations(schoenberg26)
        []
        >>> schoenberg26.findOriginalCenteredTransformations(
        ...     schoenberg26.originalCenteredTransformation('RI',8))
        [('RI', 8)]
        '''
        pass


# ----------------------------------------------------------------------------------------

class TwelveToneRow(ToneRow):
    '''
    A Stream representation of a twelve-tone row, capable of producing a 12-tone matrix.
    '''
    _DOC_ORDER = ['matrix', 'isAllInterval',
                  'getLinkClassification', 'isLinkChord', 'areCombinatorial']

    def matrix(self):
        # noinspection PyShadowingNames
        '''
        Returns a :class:`~music21.serial.TwelveToneMatrix` object for the row.
        That object can just be printed (or displayed via .show())

        >>> src = serial.getHistoricalRowByName('SchoenbergOp37')
        >>> [p.name for p in src]
        ['D', 'C#', 'A', 'B-', 'F', 'E-', 'E', 'C', 'G#', 'G', 'F#', 'B']
        >>> len(src)
        12
        >>> s37 = serial.getHistoricalRowByName('SchoenbergOp37').matrix()
        >>> print(s37)
          0  B  7  8  3  1  2  A  6  5  4  9
          1  0  8  9  4  2  3  B  7  6  5  A
          5  4  0  1  8  6  7  3  B  A  9  2
          4  3  B  0  7  5  6  2  A  9  8  1
        ...
        >>> [str(e.pitch) for e in s37[0]]
        ['C', 'B', 'G', 'G#', 'E-', 'C#', 'D', 'B-', 'F#', 'F', 'E', 'A']
        '''
        pass

    def findHistorical(self):
        '''
        Checks if a given :class:`music21.serial.TwelveToneRow` is the same as
        any of the historical
        twelve-tone rows stored by music21: see :func:`music21.serial.getHistoricalRowByName`.
        Returns a list of names of historical rows to which the input row is identical.

        >>> row = serial.pcToToneRow([2, 3, 9, 1, 11, 5, 8, 7, 4, 0, 10, 6])
        >>> row.findHistorical()
        ['SchoenbergOp32']
        >>> chromatic = serial.pcToToneRow(range(12))
        >>> chromatic.findHistorical()
        []
        '''
        pass

    def findTransformedHistorical(self, convention):
        '''
        Checks if a given :class:`music21.serial.TwelveToneRow` is a transformation of
        any historical
        twelve-tone row stored by music21 (see :func:`music21.serial.getHistoricalRowByName`).
        Returns a list
        of tuples, the tuple consisting of the name of a historical row, and a
        list of transformations relating
        the input row to the historical row.

        The convention for serial transformations must also be specified as 'zero' or
        'original', as explained
        in :meth:`~music21.serial.ToneRow.findZeroCenteredTransformations` and
        :meth:`~music21.serial.ToneRow.findOriginalCenteredTransformations`.

        >>> row = serial.pcToToneRow([5, 9, 11, 3, 6, 7, 4, 10, 0, 8, 2, 1])
        >>> row.findTransformedHistorical('original')
        [('SchoenbergOp32', [('R', 11)])]
        '''
        pass

    def isAllInterval(self) -> bool:
        '''
        Describes whether a :class:`~music21.serial.TwelveToneRow` is an all-interval row.

        >>> chromatic = serial.pcToToneRow(range(12))
        >>> chromatic.pitchClasses()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        >>> chromatic.isAllInterval()
        False
        >>> bergLyric = serial.getHistoricalRowByName('BergLyricSuite')
        >>> bergLyric.pitchClasses()
        [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]
        >>> bergLyric.isAllInterval()
        True
        '''
        pass

    def getLinkClassification(self):
        '''
        Gives the classification number of a Link Chord
        (as given in http://www.johnlinkmusic.com/LinkChords.pdf),
        that is, is an all-interval twelve-tone row containing a voicing of the
        all-trichord hexachord: [0, 1, 2, 4, 7, 8].
        In addition, gives a list of sets of five contiguous intervals
        within the row representing a voicing
        of the all-trichord hexachord. Note that the interval sets may be transformed.

        Named for John Link who discovered them.


        >>> bergLyric = serial.getHistoricalRowByName('BergLyricSuite')
        >>> bergLyric.pitchClasses()
        [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]
        >>> bergLyric.isAllInterval()
        True
        >>> bergLyric.getLinkClassification()
        (None, [])
        >>> link = serial.pcToToneRow([0, 3, 8, 2, 10, 11, 9, 4, 1, 5, 7, 6])
        >>> link.getLinkClassification()
        (62, ['8352E'])
        >>> doubleLink = serial.pcToToneRow([0, 1, 8, 5, 7, 10, 4, 3, 11, 9, 2, 6])
        >>> doubleLink.getLinkClassification()
        (33, ['236E8', '36E8T'])
        '''
        pass

    def isLinkChord(self) -> bool:
        '''
        Describes whether a :class:`~music21.serial.TwelveToneRow` is a Link Chord.

        >>> bergLyric = serial.getHistoricalRowByName('BergLyricSuite')
        >>> bergLyric.pitchClasses()
        [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]
        >>> bergLyric.isAllInterval()
        True
        >>> bergLyric.isLinkChord()
        False
        >>> link = serial.pcToToneRow([0, 3, 8, 2, 10, 11, 9, 4, 1, 5, 7, 6])
        >>> link.isLinkChord()
        True
        >>> doubleLink = serial.pcToToneRow([0, 1, 8, 5, 7, 10, 4, 3, 11, 9, 2, 6])
        >>> doubleLink.isLinkChord()
        True
        '''
        pass

    def areCombinatorial(self,
                         transType1: str,
                         index1: int,
                         transType2: str,
                         index2: int) -> bool:
        '''
        Describes whether two transformations of a twelve-tone row are combinatorial.

        The first and second arguments describe one transformation, while the third and fourth
        describe another.

        First, let's take a row we know to have a combinatoriality pair:

        >>> moses = serial.getHistoricalRowByName('SchoenbergMosesAron')
        >>> moses.pitchClasses()
        [9, 10, 4, 2, 3, 1, 7, 5, 6, 8, 11, 0]

        Combinatoriality holds here between P0 and I3

        >>> moses.areCombinatorial('P', 0, 'I', 3)
        True

        And a combinatorial pair like this between P0 and I3 will also hold
        if you modify both rows in the same way, e.g.
        if you transpose both by the same amount

        >>> moses.areCombinatorial('P', 1, 'I', 4)
        True

        or if you retrograde both

        >>> moses.areCombinatorial('R', 1, 'RI', 4)
        True

        Any modification made to one row form and not the other means all bets are off

        >>> moses.areCombinatorial('R', 6, 'RI', 4)
        False

        * Changed in v7: `convention` is no longer necessary and no longer used.
          Renamed to `unused_convention` and defaults None; to be removed in v8.
        '''
        pass


class HistoricalTwelveToneRow(TwelveToneRow):
    '''
    Subclass of :class:`~music21.serial.TwelveToneRow` storing additional attributes of a
    twelve-tone row used in the historical literature.
    '''
    _DOC_ATTR: dict[str, str] = {
        'composer': 'The name of the composer, or None.  (String)',
        'opus': 'The opus of the work, or None.  (String)',
        'title': 'The title of the work, or None.  (String)',
    }

    composer: None|str = None
    opus: None|str = None
    title: None|str = None

    def __init__(self,
                 composer: None|str = None,
                 opus: None|str = None,
                 title: None|str = None,
                 row=None,
                 **keywords):
        super().__init__(row, **keywords)
        self.composer = composer
        self.opus = opus
        self.title = title

    def mergeAttributes(self, other):
        super().mergeAttributes(other)
        if not isinstance(other, HistoricalTwelveToneRow):
            return
        self.composer = other.composer
        self.opus = other.opus
        self.title = other.title

    def _reprInternal(self):
        pass


def getHistoricalRowByName(rowName):
    '''
    Given the name referring to a twelve-tone row used in the historical literature,
    returns a :class:`~music21.serial.HistoricalTwelveToneRow` object with attributes
    describing the row.

    The names of the rows with stored attributes are below (each must be passed as a string,
    in single quotes).

    >>> for r in sorted(list(serial.historicalDict)):
    ...     print(r)
    BergChamberConcerto
    BergDerWein
    BergLulu
    BergLuluActIIScene1
    BergLuluActIScene20
    BergLyricSuite
    BergLyricSuitePerm
    BergViolinConcerto
    BergWozzeckPassacaglia
    SchoenbergFragOrganSonata
    SchoenbergFragPiano
    SchoenbergFragPianoPhantasia
    SchoenbergIsraelExists
    SchoenbergJakobsleiter
    SchoenbergMosesAron
    SchoenbergOp23No5
    SchoenbergOp24Mvmt4
    SchoenbergOp24Mvmt5
    SchoenbergOp25
    SchoenbergOp26
    SchoenbergOp27No1
    SchoenbergOp27No2
    SchoenbergOp27No3
    SchoenbergOp27No4
    SchoenbergOp28No1
    SchoenbergOp28No3
    SchoenbergOp29
    SchoenbergOp30
    SchoenbergOp31
    SchoenbergOp32
    SchoenbergOp33A
    SchoenbergOp33B
    SchoenbergOp34
    SchoenbergOp35No1
    SchoenbergOp35No2
    SchoenbergOp35No3
    SchoenbergOp35No5
    SchoenbergOp36
    SchoenbergOp37
    SchoenbergOp41
    SchoenbergOp42
    SchoenbergOp44
    SchoenbergOp45
    SchoenbergOp46
    SchoenbergOp47
    SchoenbergOp48No1
    SchoenbergOp48No2
    SchoenbergOp48No3
    SchoenbergOp50A
    SchoenbergOp50B
    SchoenbergOp50C
    WebernOp17No2
    WebernOp17No3
    WebernOp18No1
    WebernOp18No2
    WebernOp18No3
    WebernOp19No1
    WebernOp19No2
    WebernOp20
    WebernOp21
    WebernOp22
    WebernOp23
    WebernOp24
    WebernOp25
    WebernOp26
    WebernOp27
    WebernOp28
    WebernOp29
    WebernOp30
    WebernOp31
    WebernOpNo17No1

    >>> web = serial.getHistoricalRowByName('WebernOp29')
    >>> web.row
    [3, 11, 2, 1, 5, 4, 7, 6, 10, 9, 0, 8]
    >>> web.composer
    'Webern'
    >>> web.opus
    'Op. 29'
    >>> web.title
    'Cantata I'
    >>> web.isLinkChord()
    False

    NOTE: before v6, these rows had 'Row' in front of them,
    like 'RowWebernOp29' instead of 'WebernOp29'.  They can still be accessed
    by the old name.

    >>> rowWeb = serial.getHistoricalRowByName('RowWebernOp29')
    >>> rowWeb.row == web.row
    True
    '''
    pass

# ------------------------------------------------------------------------------


def pcToToneRow(pcSet):
    # noinspection GrazieInspection
    '''
    A convenience function that, given a list of pitch classes represented as integers
    and turns it in to a :class:`~music21.serial.ToneRow` object.

    >>> chromaticRow = serial.pcToToneRow([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    >>> chromaticRow.show('text')
    {0.0} <music21.note.Note C>
    {1.0} <music21.note.Note C#>
    {2.0} <music21.note.Note D>
    {3.0} <music21.note.Note E->
    {4.0} <music21.note.Note E>
    {5.0} <music21.note.Note F>
    {6.0} <music21.note.Note F#>
    {7.0} <music21.note.Note G>
    {8.0} <music21.note.Note G#>
    {9.0} <music21.note.Note A>
    {10.0} <music21.note.Note B->
    {11.0} <music21.note.Note B>
    >>> matrixObj = chromaticRow.matrix()
    >>> print(matrixObj)
      0  1  2  3  4  5  6  7  8  9  A  B
      B  0  1  2  3  4  5  6  7  8  9  A
    ...

    >>> fancyRow = serial.pcToToneRow([4, 5, 0, 6, 7, 2, 'a', 8, 9, 1, 'b', 3])
    >>> matrixObj = fancyRow.matrix()
    >>> print(matrixObj)
      0  1  8  2  3  A  6  4  5  9  7  B
      B  0  7  1  2  9  5  3  4  8  6  A
    ...

    Note that the Row does not have to be a valid row to exist:

    >>> multiSetRow = serial.pcToToneRow([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    >>> multiSetRow.pitchClasses()
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    Or even have 12 notes:

    >>> shortRow = serial.pcToToneRow([3, 4])
    >>> shortRow.pitchClasses()
    [3, 4]

    If the row does have twelve notes (whether unique or not) the object returned
    is a `TwelveToneRow`:

    >>> multiSetRow
    <music21.serial.TwelveToneRow 111111111111>

    Otherwise, it is simply a `ToneRow`:

    >>> shortRow
    <music21.serial.ToneRow 34>
    '''
    if len(pcSet) == 12:
        a = TwelveToneRow()
    else:
        a = ToneRow()

    for thisPc in pcSet:
        n = note.Note()
        n.pitch.pitchClass = thisPc
        n.pitch.octave = None
        a.append(n)
    return a


def rowToMatrix(p: list[int]) -> str:
    # noinspection PyShadowingNames
    '''
    Takes a list of numbers of converts it to a string representation of a
    12-tone matrix.

    >>> aMatrix = serial.rowToMatrix([0, 2, 11, 7, 8, 3, 9, 1, 4, 10, 6, 5])
    >>> print(aMatrix)
      0  2 11  7  8  3  9  1  4 10  6  5
     10  0  9  5  6  1  7 11  2  8  4  3
      1  3  0  8  9  4 10  2  5 11  7  6
      5  7  4  0  1  8  2  6  9  3 11 10
      4  6  3 11  0  7  1  5  8  2 10  9
      9 11  8  4  5  0  6 10  1  7  3  2
      3  5  2 10 11  6  0  4  7  1  9  8
     11  1 10  6  7  2  8  0  3  9  5  4
      8 10  7  3  4 11  5  9  0  6  2  1
      2  4  1  9 10  5 11  3  6  0  8  7
      6  8  5  1  2  9  3  7 10  4  0 11
      7  9  6  2  3 10  4  8 11  5  1  0

    This function survives today (2020) because it's been
    an example function for `music21` since the very first demonstrations
    of predecessors from around 2000 onwards.  Nowadays, better to create
    a `TwelveToneRow()` object and then get a matrix from that:

    >>> ttr = serial.TwelveToneRow([0, 2, 11, 7, 8, 3, 9, 1, 4, 10, 6, 5])
    >>> matrix = ttr.matrix()
    >>> print(matrix)
      0  2  B  7  8  3  9  1  4  A  6  5
      A  0  9  5  6  1  7  B  2  8  4  3
      1  3  0  8  9  4  A  2  5  B  7  6
      5  7  4  0  1  8  2  6  9  3  B  A
      4  6  3  B  0  7  1  5  8  2  A  9
      9  B  8  4  5  0  6  A  1  7  3  2
      3  5  2  A  B  6  0  4  7  1  9  8
      B  1  A  6  7  2  8  0  3  9  5  4
      8  A  7  3  4  B  5  9  0  6  2  1
      2  4  1  9  A  5  B  3  6  0  8  7
      6  8  5  1  2  9  3  7  A  4  0  B
      7  9  6  2  3  A  4  8  B  5  1  0
    '''
    pass


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testMatrix(self):
        pass

    def testLabelingA(self):
        pass
        # s.show()

    def testHistorical(self):
        pass

    def testExtractRowParts(self):
        '''
        Was a problem in slices
        '''
        pass

    def testPostTonalDocs(self):
        pass

    def testCopyAndDeepcopy(self):
        pass


    # def testRows(self):
    #     from music21 import interval
    #
    #     self.assertEqual(len(vienneseRows), 71)
    #
    #     totalRows = 0
    #     cRows = 0
    #     for thisRow in vienneseRows:
    #         thisRow = thisRow()
    #         self.assertIsInstance(thisRow, TwelveToneRow)
    #
    #         if thisRow.composer == 'Berg':
    #             continue
    #         post = thisRow.title
    #
    #         totalRows += 1
    #         if thisRow[0].pitchClass == 0:
    #             cRows += 1
    #
    #          if interval.Interval(thisRow[0],
    #                               thisRow[6]).intervalClass == 6:
    #           # between element 1 and element 7 is there a TriTone?
    #           rowsWithTTRelations += 1


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER = [ToneRow, TwelveToneRow, HistoricalTwelveToneRow,
              pcToToneRow, TwelveToneMatrix, rowToMatrix, getHistoricalRowByName,
              ]

if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

