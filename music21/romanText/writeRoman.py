# ------------------------------------------------------------------------------
# Name:         romanText/writeRoman.py
# Purpose:      Writer for the 'RomanText' format
#
# Authors:      Mark Gotham
#
# Copyright:    Copyright © 2020 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Writer for the 'RomanText' format (Tymoczko, Gotham, Cuthbert, & Ariza ISMIR 2019)
'''
from __future__ import annotations

import fractions
import textwrap
import unittest

from music21 import bar
from music21 import base
from music21 import metadata
from music21 import meter
from music21 import prebase
from music21 import roman
from music21 import romanText
from music21 import stream


# ------------------------------------------------------------------------------

class RnWriter(prebase.ProtoM21Object):
    '''
    Extracts the relevant information from a source
    (usually a :class:`~music21.stream.Stream` of
    :class:`~music21.roman.RomanNumeral` objects) for
    writing to text files in the 'RomanText' format (rntxt).

    Writing rntxt is handled externally in the
    :meth:`~music21.converter.subConverters.WriteRoman` so
    most users will never need to call this class directly, only invoking
    it indirectly through .write('rntxt').
    Possible exceptions include users who want to convert Roman numerals into rntxt type
    strings and want to work with those strings directly, without writing to disk.

    For consistency with the
    :meth:`~music21.base.Music21Object.show` and :meth:`~music21.base.Music21Object.write`
    methods across music21, this class is theoretically callable on
    any type of music21 object.
    Most relevant use cases will involve calling a
    stream containing one or more Roman numerals.
    This class supports any such stream:
    an :class:`~music21.stream.Opus` object of one or more scores,
    a :class:`~music21.stream.Score` with or without :class:`~music21.stream.Part` (s),
    a :class:`~music21.stream.Part`, or
    a :class:`~music21.stream.Measure`.

    >>> scoreBach = corpus.parse('bach/choraleAnalyses/riemenschneider004.rntxt')
    >>> rnWriterFromScore = romanText.writeRoman.RnWriter(scoreBach)

    The strings are stored in the RnWriter's combinedList variable, starting with the metadata:

    >>> rnWriterFromScore.combinedList[0]
    'Composer: J. S. Bach'

    Composer and work metadata is inherited from score metadata wherever possible.
    A composer entry will register directly as will any entries for
    workTitle, movementNumber, and movementName
    (see :meth:`~music21.romanText.writeRoman.RnWriter.prepTitle` for details).

    >>> rnWriterFromScore.combinedList[0] == 'Composer: ' + rnWriterFromScore.composer
    True

    As always, these metadata entries are user-settable.
    Make any adjustments to the metadata before calling this class.

    After the metadata, the list continues with strings for each measure in order.
    Here's the last in our example:

    >>> rnWriterFromScore.combinedList[-1]
    'm10 V6/V b2 V b3 I'

    In the case of the score, the top part is assumed to contain the Roman numerals.
    This is consistent with the parsing of rntxt which involves putting Roman numerals in a part
    (the top, and only part) within a score.

    In all other cases, the objects are iteratively inserted into larger streams until we end up
    with a part object (e.g. measure > part).

    >>> rn = roman.RomanNumeral('viio64', 'a')
    >>> rnWriterFromRn = romanText.writeRoman.RnWriter(rn)
    >>> rnWriterFromRn.combinedList[0]
    'Composer: Composer unknown'

    >>> rnWriterFromRn.combinedList[-1]
    'm0 a: viio64'

    OMIT_FROM_DOCS

    Users can do these insertions themselves, but don't need to:

    >>> m = stream.Measure()
    >>> m.insert(0, rn)
    >>> rnWriterFromMeasure = romanText.writeRoman.RnWriter(m)
    >>> rnWriterFromMeasure.combinedList == rnWriterFromRn.combinedList
    True

    >>> p = stream.Part()
    >>> p.insert(0, m)
    >>> rnWriterFromPart = romanText.writeRoman.RnWriter(p)
    >>> rnWriterFromPart.combinedList == rnWriterFromMeasure.combinedList
    True

    >>> s = stream.Score()
    >>> s.insert(0, m)
    >>> rnWriterFromScoreWithoutPart = romanText.writeRoman.RnWriter(p)
    >>> rnWriterFromScoreWithoutPart.combinedList == rnWriterFromMeasure.combinedList
    True
    '''

    def __init__(self,
                 obj: base.Music21Object,
                 ):

        self.composer = 'Composer unknown'
        self.title = 'Title unknown'
        self.analyst = ''
        self.proofreader = ''
        self.combinedList: list[str] = []
        self.container: stream.Part|stream.Score

        if isinstance(obj, stream.Stream):
            if isinstance(obj, stream.Opus):
                constituentElements = [RnWriter(x) for x in obj]
                for scoreOrSim in constituentElements:
                    for x in scoreOrSim.combinedList:
                        self.combinedList.append(x)
                    self.combinedList.append('\n')  # one between scores
                return

            elif isinstance(obj, stream.Score):
                p = obj.parts.first()
                if p is not None:
                    self.container = p
                else:  # score with no parts
                    self.container = obj

            elif isinstance(obj, stream.Part):
                self.container = obj

            elif isinstance(obj, stream.Measure):
                self.container = stream.Part()
                self.container.insert(0, obj)

            else:  # A stream, but not a measure, part, or score
                self.container = self._makeContainer(obj)

            if obj.metadata:  # Check the obj (not container) for metadata if obj is a stream
                self.prepTitle(obj.metadata)
                if obj.metadata.composer:
                    self.composer = obj.metadata.composer
                if obj.metadata.analyst:
                    self.analyst = obj.metadata.analyst
                if obj.metadata.proofreader:
                    self.proofreader = obj.metadata.proofreader

        else:  # Not a stream
            self.container = self._makeContainer([obj])

        self.combinedList = [f'Composer: {self.composer}',
                             f'Title: {self.title}',
                             f'Analyst: {self.analyst}',
                             f'Proofreader: {self.proofreader}',
                             '']  # One blank line between metadata and analysis

        if not self.container[meter.TimeSignature]:
            self.container.insert(0, meter.TimeSignature('4/4'))  # Placeholder

        self.currentKeyString: str = ''
        self.prepSequentialListOfLines()

    def _makeContainer(self,
                       obj: stream.Stream|list):
        '''
        Makes a placeholder container for the unusual cases where this class is called on
        generic- or non-stream object as opposed to
        a :class:`~music21.stream.Score`, :class:`~music21.stream.Part`,
        or :class:`~music21.stream.Measure`.
        '''
        pass

    def prepTitle(self,
                  md: metadata.Metadata):
        '''
        Attempt to prepare a single work title from the score metadata looking at each of
        the title, movementNumber and movementName attributes.
        Failing that, a placeholder 'Title unknown' stands in.

        >>> s = stream.Score()
        >>> rnScore = romanText.writeRoman.RnWriter(s)
        >>> rnScore.title
        'Title unknown'

        >>> s.insert(0, metadata.Metadata())
        >>> s.metadata.title = 'Fake title'
        >>> s.metadata.movementNumber = 123456789
        >>> s.metadata.movementName = 'Fake movementName'
        >>> rnScoreWithMD = romanText.writeRoman.RnWriter(s)
        >>> rnScoreWithMD.title
        'Fake title - No.123456789: Fake movementName'
        '''
        pass

# ------------------------------------------------------------------------------

    def prepSequentialListOfLines(self):
        '''
        Prepares a sequential list of text lines, with time signatures and Roman numerals
        adding this to the (already prepared) metadata preamble ready for printing.

        >>> p = stream.Part()
        >>> m = stream.Measure(number=1)
        >>> m.insert(0, meter.TimeSignature('4/4'))
        >>> m.insert(0, roman.RomanNumeral('V', 'G'))
        >>> p.insert(0, m)
        >>> testCase = romanText.writeRoman.RnWriter(p)
        >>> testCase.combinedList[-1]  # Last entry, after the metadata
        'm1 G: V'

        This follows the wider rntxt syntax in supporting
        Time Signature (:class:`~music21.meter.TimeSignature`) changes and
        Repeats marks (:class:`~music21.bar.Repeat`)
        but only (currently) between measures.

        Let's add a new measure to the stream we started,
        with a time signature change beforehand and
        both start and end repeats in it:

        >>> m2 = stream.Measure(number=2)
        >>> m2.insert(0, meter.TimeSignature('3/4'))
        >>> m2.leftBarline = bar.Repeat(direction='start')
        >>> m2.rightBarline = bar.Repeat(direction='end')
        >>> m2.insert(0, roman.RomanNumeral('I', 'G'))
        >>> p.insert(0, m2)
        >>> testCase = romanText.writeRoman.RnWriter(p)

        The last line of the `.combinedList` gives the new measure:

        >>> testCase.combinedList[-1]
        'm2 ||: I :||'

        The line before that gives the time signature change:

        >>> testCase.combinedList[-2]
        'Time Signature: 3/4'

        '''
        pass

    def getChordString(self,
                       rn: roman.RomanNumeral):
        '''
        Produce a string from a Roman numeral with the chord and
        the key if that key constitutes a change from the foregoing context.

        >>> p = stream.Part()
        >>> m = stream.Measure()
        >>> m.insert(0, meter.TimeSignature('4/4'))
        >>> m.insert(0, roman.RomanNumeral('V', 'G'))
        >>> p.insert(0, m)
        >>> testCase = romanText.writeRoman.RnWriter(p)
        >>> sameKeyChord = testCase.getChordString(roman.RomanNumeral('I', 'G'))
        >>> sameKeyChord
        'I'

        >>> changeKeyChord = testCase.getChordString(roman.RomanNumeral('V', 'D'))
        >>> changeKeyChord
        'D: V'
        '''
        pass


# ------------------------------------------------------------------------------

def rnString(measureNumber: int|str,
             beat: str|int|float|fractions.Fraction,
             chordString: str,
             inString: str|None = ''):
    '''
    Creates or extends a string of RomanText such that the output corresponds to a single
    measure line.

    If the inString is not given, None, or an empty string then this function starts a new line.

    >>> lineStarter = romanText.writeRoman.rnString(14, 1, 'G: I')
    >>> lineStarter
    'm14 G: I'

    For any other inString, that string is the start of a measure line continued by the new values

    >>> continuation = romanText.writeRoman.rnString(14, 2, 'viio6', 'm14 G: I')
    >>> continuation
    'm14 G: I b2 viio6'

    Naturally, this function requires the measure number of any such continuation to match
    that of the inString and raises an error where that is not the case.

    As these examples show, the chordString can be a Roman numeral alone (e.g. 'viio6')
    or one prefixed by a change of key ('G: I').

    '''
    pass


def intBeat(beat: str|int|float|fractions.Fraction,
            roundValue: int = 2):
    '''
    Converts beats to integers if possible, and otherwise to rounded decimals.
    Accepts input as string, int, float, or fractions.Fraction.

    >>> testInt = romanText.writeRoman.intBeat(1, roundValue=2)
    >>> testInt
    1

    >>> testFrac = romanText.writeRoman.intBeat(8 / 3, roundValue=2)
    >>> testFrac
    2.67

    >>> testStr = romanText.writeRoman.intBeat('0.666666666', roundValue=2)
    >>> testStr
    0.67

    The roundValue sets the number of decimal places to round to. The default is two:

    >>> testRound2 = romanText.writeRoman.intBeat(1.11111111, roundValue=2)
    >>> testRound2
    1.11

    But this can be set to any integer:

    >>> testRound1 = romanText.writeRoman.intBeat(1.11111111, roundValue=1)
    >>> testRound1
    1.1

    Raises an error if called on a negative value.
    '''
    pass


# ------------------------------------------------------------------------------

class Test(unittest.TestCase):
    '''
    Tests for two analysis cases (the smallest rntxt files in the music21 corpus)
    along with two test by modifying those scores.

    Additional tests for the standalone functions rnString and intBeat and
    for handling the special case of opus objects.
    '''

    def testOpus(self):
        '''
        As the rntxt input parser handles Opus objects
        (i.e. more than one score within the same rntxt files),
        this RnWriter also needs to accept that type.

        This test parses a fake (tiny) Opus file in three (really tiny!) movements.
        Checks ensure that the parsed version is indeed an Opus object and that
        the data is faithfully transferred through that process.

        In practice, Opus handling will bypass this module in the typical case of a simple
        .write() because writing Opus objects explicitly separates them into their constituent
        score files prior to invoking this module.
        '''
        pass

    def testTwoCorpusPiecesAndTwoCorruptions(self):
        '''
        Tests for two analysis cases (the smallest rntxt files in the music21 corpus)
        along with two test by modifying those scores.
        '''
        pass

    def testTypeParses(self):
        '''
        Tests successful init on a range of supported objects (score, part, even RomanNumeral).
        '''
        pass

    def testRepeats(self):
        pass

    def testRnString(self):
        pass

    def testIntBeat(self):
        pass


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
