# -----------------------------------------------------------------------------
# Name:         meter.tests.py
# Purpose:      Tests of meter
#
# Authors:      Christopher Ariza
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2009-2024 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
from __future__ import annotations

import copy
import random
import unittest

from music21 import common
from music21 import duration
from music21 import note
from music21 import stream
from music21.meter.base import TimeSignature
from music21.meter.core import MeterSequence, MeterTerminal

class TestExternal(unittest.TestCase):
    show = True

    def testSingle(self):
        '''
        Need to test direct meter creation w/o stream
        '''
        pass

    def testBasic(self):
        pass

    def testCompound(self):
        pass

    def testMeterBeam(self):
        pass


class Test(unittest.TestCase):
    def testMeterSubdivision(self):
        pass

    def testMeterSequenceDeepcopy(self):
        pass
        # TODO: equity of meter sequences not yet defined.
        # self.assertEqual(a, b)

    def testTimeSignatureDeepcopy(self):
        pass

    def testGetBeams(self):
        pass

    def test_getBeams_offset(self):
        '''
        Test getting Beams from a Measure that has an anacrusis that makes the
        first note not beamed.
        '''
        pass


    def testOffsetToDepth(self):
        # get a maximally divided 4/4 to the level of 1/8
        pass

    def testDefaultBeatPartitions(self):
        pass

    def testBeatProportionFromTimeSignature(self):
        # given meter, ql, beat proportion, and beat ql
        pass

    def testSubdividePartitionsEqual(self):
        pass

    def testSetDefaultAccentWeights(self):
        # these tests take the level to 3. in some cases, a level of 2
        # is not sufficient to normalize all denominators
        pass

    def testMusicxmlDirectOut(self):
        # test rendering musicxml directly from meter
        pass

    def testSlowSixEight(self):
        pass

    def testMixedDurationsBeams(self):
        pass

    def testMixedDurationBeams2(self):
        pass

    def testBestTimeSignature(self):
        pass

    def testBestTimeSignatureB(self):
        '''
        Correct the TimeSignatures (4/4 in m. 1; no others) in a 4-measure score
        of 12, 11.5, 12, 13 quarters, where one of the parts is a PartStaff with
        multiple voices.
        '''
        pass

    def testBestTimeSignatureDoubleDotted(self):
        pass

    def testBestTimeSignatureDoubleDottedB(self):
        '''
        These add up the same as testBestTimeSignatureDoubleDotted, but
        use multiple notes.
        '''
        pass

    def testBestTimeSignatureDoubleDottedC(self):
        '''
        These add up the same as testBestTimeSignatureDoubleDotted, but
        use multiple notes which are dotted divisions of the original
        '''
        pass

    def testCompoundSameDenominator(self):
        pass

    def testEquality(self):
        '''
        Additional tests of TimeSignature object equality.
        Apart from this and the doc tests,
        see also testTimeSignatureDeepcopy for a test of
        time signatures with different structure with same ratioString
        (fast vs slow 6/8).
        '''
        pass
        # NB: not self.assertRaises(AttributeError). Do we want that instead?


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
