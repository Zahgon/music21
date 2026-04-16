# ------------------------------------------------------------------------------
# Name:         alpha/analysis/ornamentRecognizer.py
# Purpose:      Identifies expanded ornaments
#
# Authors:      Janelle Sands
#
# Copyright:    Copyright © 2016 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

from copy import deepcopy
import unittest

from music21.common.numberTools import opFrac
from music21.common.types import OffsetQL
from music21 import duration
from music21 import expressions
from music21 import interval
from music21 import note
from music21 import stream


class OrnamentRecognizer:
    '''
    An object to identify if a stream of notes is an expanded ornament.
    Busy notes refer to the expanded ornament notes.
    Simple note(s) refer to the base note of ornament which is often shown
    with the ornament marking on it.
    '''
    def calculateOrnamentNoteQl(
        self,
        busyNotes,
        simpleNotes=None
    ):
        '''
        Finds the quarter length value for each ornament note
        assuming busy notes all are an expanded ornament.

        Expanded ornament total duration is time of all busy notes combined or
        duration of the first note in simpleNotes when provided.
        '''
        pass

    def calculateOrnamentTotalQl(
        self,
        busyNotes: list[note.GeneralNote],
        simpleNotes: list[note.GeneralNote]|None = None
    ) -> OffsetQL:
        '''
        Returns total length of trill assuming busy notes are all an expanded trill.
        This is either the time of all busy notes combined or
        duration of the first note in simpleNotes when provided.
        '''
        pass


class TrillRecognizer(OrnamentRecognizer):
    '''
    An object to identify if a stream of ("busy") notes is an expanded trill.

    By default, does not consider Nachschlag trills, but setting checkNachschlag will consider.

    When optional stream of simpleNotes are provided, considers if busyNotes are
    an expansion of a trill which would be denoted on the first note in simpleNotes.
    '''
    def __init__(self, checkNachschlag=False):
        self.checkNachschlag = checkNachschlag
        self.acceptableInterval = 3
        self.minimumLengthForNachschlag = 5

    def recognize(self, busyNotes, simpleNotes=None) -> bool|expressions.Trill:
        '''
        Tries to identify the busy notes as a trill.

        When simple notes is provided, tries to identify busy notes
        as the trill shortened by simple notes.
        Currently only supports one simple note in simple notes.

        Only when checkNachschlag is true, allows last few notes to break trill rules.

        Trill interval size is interval between busy notes.

        Returns: False if not possible or the Trill Expression
        '''
        pass

class TurnRecognizer(OrnamentRecognizer):
    def __init__(self, ):
        self.acceptableInterval = 3
        self.minimumLengthForNachschlag = 6
        self.acceptableIntervals = [
            interval.Interval('M2'), interval.Interval('M-2'),
            interval.Interval('m2'), interval.Interval('m-2'),
            interval.Interval('A2'), interval.Interval('A-2'),
        ]

    def isAcceptableInterval(self, intervalToCheck: interval.Interval) -> bool:
        '''
        Returns whether that interval can occur in a turn
        '''
        pass

    def recognize(
        self,
        busyNotes,
        simpleNotes=None,
    ) -> bool|expressions.Turn|expressions.InvertedTurn:
        '''
        Tries to identify the busy notes as a turn or inverted turn.

        When simple notes is provided, tries to identify busy notes
        as the turn shortened by simple notes.
        Currently only supports one simple note in simple notes.

        Turns and inverted turns have four notes separated by m2, M2, A2.

        Turns:
        start above base note
        go down to base note,
        go down again,
        and go back up to base note

        Inverted Turns:
        start below base note
        go up to base note,
        go up again,
        and go back down to base note

        When going up or down, must go to the adjacent note name,
        so A goes down to G, G#, G flat, G##, etc

        Returns: False if not possible or the Turn/Inverted Turn Expression
        '''
        pass

class _TestCondition:
    def __init__(
        self, name, busyNotes, isOrnament,
        simpleNotes=None, ornamentSize=None, isNachschlag=False, isInverted=False
    ):
        self.name = name
        self.busyNotes = busyNotes
        self.isOrnament = isOrnament
        self.simpleNotes = simpleNotes
        self.ornamentSize = ornamentSize
        self.isNachschlag = isNachschlag
        self.isInverted = isInverted

class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def testRecognizeTurn(self):
        # set up experiment
        pass

    def testRecognizeTrill(self):
        # set up the experiment
        pass


def calculateTrillNoteDuration(numTrillNotes, totalDuration):
    pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
