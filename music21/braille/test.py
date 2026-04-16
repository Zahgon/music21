# ------------------------------------------------------------------------------
# Name:         test.py
# Purpose:      Examples from "Introduction to Braille Music Transcription"
# Authors:      Jose Cabal-Ugaz
#
# Copyright:    Copyright © 2012, 2016 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
import textwrap
import unittest

from music21 import articulations
from music21.articulations import Fingering
from music21.braille.objects import BrailleSegmentDivision
from music21.braille.translate import partToBraille, measureToBraille, keyboardPartsToBraille
from music21 import bar
from music21 import chord
from music21 import clef
from music21 import converter
from music21 import dynamics
from music21 import expressions
from music21 import key
from music21 import meter
from music21 import note
from music21 import pitch
from music21 import spanner
from music21 import stream
from music21 import tempo

_DOC_IGNORE_MODULE_OR_PACKAGE = True

# called elsewhere:

def example11_2():
    pass


# Examples follow the order in:
#   Introduction to Braille Music Transcription, Second Edition (2005)
# Mary Turner De Garmo
# https://www.loc.gov/nls/services-and-resources/music-service-and-materials/
# ------------------------------------------------------------------------------
class Test(unittest.TestCase):
    '''
    A series of tests from the DeGarmo book that run automatically
    when self.b (expected braille) or self.e (expected english) are altered
    '''

    def _s(self, streamIn):
        pass

    s = property(fset=_s)

    def _neutralizeSpacing(self, sStr):
        pass

    def _b(self, brailleInput):
        '''
        Sets the expected brailleInput and runs assertMultilineEqual
        '''
        pass

    b = property(fset=_b)

    def _e(self, english):
        pass

    e = property(fset=_e)

    def runB(self):
        pass

    def runE(self):
        pass

    def setUp(self):
        self.maxDiff = None
        self.autoRun = True
        self.stream = None
        self.expectedBraille = ''
        self.expectedEnglish = ''
        self.method = partToBraille
        self.methodArgs = {}

# ------------------------------------------------------------------------------
# PART ONE
# Basic Procedures and Transcribing Single-Staff Music
#
# ------------------------------------------------------------------------------
# Chapter 2: Eighth Notes, the Eighth Rest, and Other Basic Signs

    def test_example02_1(self):
        pass

    def test_example02_2(self):
        pass

    def test_example02_3(self):
        pass

    def test_example02_4(self):
        pass

    def test_example02_5(self):
        pass

    def test_example02_6(self):
        pass

    def test_example02_7(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 3: Quarter Notes, the Quarter Rest, and the Dot

    def test_example03_1(self):
        pass

    def test_example03_2(self):
        pass

    def test_example03_3(self):
        pass

    def test_example03_4(self):
        pass

    def test_example03_5(self):
        pass

    def test_example03_6(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 4: Half Notes, the Half Rest, and the Tie

    def test_example04_1(self):
        pass

    def test_example04_2(self):
        pass

    def test_example04_3(self):
        pass

    def test_example04_4(self):
        pass

    def test_example04_5(self):
        pass

    def test_example04_6(self):
        pass

    def test_example04_7(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 5: Whole and Double Whole Notes and Rests, Measure Rests, and
# Transcriber-Added Signs

    def test_example05_1(self):
        pass

    def test_example05_2(self):
        pass

    def test_example05_3(self):
        pass

    def test_example05_4(self):
        pass

    def test_example05_5(self):
        pass

    def test_example05_6(self):
        # NOTE: Breve note and breve rest are transcribed using method (b) on page 24.
        pass

    # The following examples (as well as the rest of the examples in the chapter)
    # don't work correctly yet.
    #
    def xtest_example05_7a(self):
        pass

    def xtest_example05_7b(self):
        pass

    def xtest_example05_7c(self):
        pass
        # self.b = ''

# ------------------------------------------------------------------------------
# Chapter 6: Accidentals

    def test_example06_1(self):
        pass

    def test_example06_2(self):
        pass

    def test_example06_3(self):
        pass

    def test_example06_4(self):
        pass

    def test_example06_5(self):
        pass

    def test_example06_6(self):
        pass

    def test_example06_7(self):
        pass

    def test_example06_8(self):
        pass

    def test_example06_9(self):
        pass

    def test_example06_10(self):
        pass

    def test_example06_11(self):
        pass

    def test_example06_12(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 7: Octave Marks

    def test_example07_1(self):
        pass

    def test_example07_2(self):
        pass

    def test_example07_3a(self):
        pass

    def test_example07_3b(self):
        pass

    def test_example07_4a(self):
        pass

    def test_example07_4b(self):
        pass

    def test_example07_5a(self):
        pass

    def test_example07_5b(self):
        pass

    def test_example07_6(self):
        pass

    def test_example07_7(self):
        '''
        "Whenever the marking “8va” occurs in print over or under certain notes,
        these notes should be transcribed according to the octaves in which they
        are actually to be played." page 42, Braille Transcription Manual

        TODO: Replace with actual 8va spanner.
        '''
        pass

    def test_example07_8(self):
        pass

    def test_example07_9(self):
        pass

    def test_example07_10(self):
        pass

    def test_example07_11(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 8: The Music Heading: Signatures, Tempo, and Mood

    def test_example08_1a(self):
        pass

    def test_example08_1b(self):
        pass

    def test_example08_2(self):
        pass

    def xtest_example08_3(self):
        '''
        Time signatures with one number. Not currently supported.
        '''
        pass

    def xtest_example08_4(self):
        '''
        Combined time signatures. Not currently supported.
        '''
        pass

    def test_example08_5(self):
        '''
        Common/cut time signatures
        '''
        pass

    def test_example08_6(self):
        pass

    def test_example08_7a(self):
        pass

    def test_example08_8(self):
        pass

    def test_example08_9(self):
        pass

    def test_example08_10(self):
        '''
        Actual look is:

    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠇⠑⠝⠞⠕⠀⠁⠎⠎⠁⠊⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠝⠞⠁⠝⠞⠑⠀⠑⠀⠞⠗⠁⠝⠟⠥⠊⠇⠇⠕⠲⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠄⠶⠼⠑⠃⠀⠼⠑⠣⠼⠋⠦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        '''
        pass

    def test_drill08_1(self):
        pass

    def test_drill08_2(self):
        pass

    def test_drill08_3(self):
        pass

    def test_drill08_4(self):
        pass

    def test_drill08_5(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 9: Fingering

    def test_example09_1(self):
        pass

    def test_example09_2(self):
        pass

    def test_example09_3(self):
        pass

    def test_example09_4a(self):
        pass

    def test_example09_4b(self):
        pass

    def test_example09_5a(self):
        pass

    def test_example09_5b(self):
        pass

    def test_example09_6(self):
        pass

    def test_drill09_1(self):
        pass

    def test_drill09_2(self):
        pass

    def test_drill09_3(self):
        pass

    def test_drill09_4(self):
        pass

    def xtest_drill09_5(self):
        '''
        No longer working -- because of some changes in accidentals -- needs to
        be looked at.
        '''
        pass

# ------------------------------------------------------------------------------
# Chapter 10: Changes of Signature; the Braille Music Hyphen, Asterisk, and
# Parenthesis; Clef Signs

    def test_example10_1(self):
        pass

    def test_example10_2(self):
        pass

    def test_example10_3(self):
        pass

    def test_example10_4(self):
        pass

    def test_example10_5(self):
        pass

    def test_example10_6(self):
        pass

    def test_example10_9(self):
        pass

    def test_example10_10(self):
        pass

    def test_drill10_2(self):
        pass
    # test_drill10_3 -- requires alternate time signature symbols

    def test_drill10_4(self):
        # TODO: 4/4 as c symbol.
        pass

# ------------------------------------------------------------------------------
# Chapter 11: Segments for Single-Line Instrumental Music, Format for the
# Beginning of a Composition or Movement

    def test_example11_1(self):
        pass

    def test_example11_2(self):
        # this example was used elsewhere, so needed to be retained.
        pass

# ------------------------------------------------------------------------------
# Chapter 12: Slurs (Phrasing)

    def test_example12_1(self):
        pass

    def test_example12_2(self):
        pass

    def test_example12_3(self):
        pass

    def test_example12_4(self):
        pass

    def test_example12_5(self):
        pass

    def test_example12_6(self):
        pass

    def test_example12_7(self):
        pass

    def test_example12_8(self):
        pass

    def test_example12_9(self):
        pass

    def test_example12_10(self):
        pass

    def test_example12_11(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 13: Words, Abbreviations, Letters, and Phrases of Expression

    def test_example13_1(self):
        pass

    def test_example13_2(self):
        pass

    def xtest_example13_3(self):
        # Problem: How to plug in wedges into music21?
        pass
        # self.b = '''
        # '''

    def test_example13_9(self):
        pass

    def test_example13_10(self):
        pass

    def xtest_example13_11(self):
        # Problem: How to braille the pp properly?
        pass
        # self.b = '''
        # '''

    def test_example13_14(self):
        pass

    def test_example13_15(self):
        pass

    def test_example13_16(self):
        pass

    def test_example13_17(self):
        pass

    def test_example13_18(self):
        pass

    def xtest_example13_19(self):
        pass
        # self.b = '''
        # '''

    def test_example13_26(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 14: Symbols of Expression and Execution

    def test_example14_1(self):
        pass

    def test_example14_2(self):
        '''
        Doubling of Tenuto marking is demonstrated. Accent is used in place of
        Reversed Accent because music21
        doesn't support the latter.
        '''
        pass

    def test_example14_3(self):
        pass

    def test_example14_5(self):
        pass

    def test_example14_6(self):
        pass

    def test_example14_7(self):
        pass

    def test_example14_8(self):
        pass

    def test_example_14_14(self):
        pass

    def test_example_14_15(self):
        pass

    # ------------------------------------------------------------------------------
    # Chapter 15: Smaller Values and Regular Note-Grouping, the Music Comma

    def test_example15_1(self):
        pass

    def test_example15_2(self):
        pass

    def test_example15_3(self):
        pass

    def test_example15_4(self):
        pass

    def test_example15_5(self):
        pass

    def test_example15_6a(self):
        # beamed 16th notes
        pass

    def test_example15_6b(self):
        # unbeamed 16th notes
        pass

    def test_example15_7(self):
        pass

    def test_example15_8(self):
        pass

    def test_example15_9(self):
        pass

    def xtest_example15_10(self):
        # print(translate.partToBraille(test.test_example15_10(),
        #       inPlace=True, dummyRestLength = 24))
        # Division of measure at end of line of "4/4" bar occurs
        #  in middle of measure, when in reality
        # it could occur 3/4 into the bar. Hypothetical example that might not be worth attacking.
        pass
        # self.b = '''
        # '''

    def test_example15_11(self):
        pass

# ------------------------------------------------------------------------------
# Chapter 16: Irregular Note-Grouping

# Triplets
# --------
    def test_example16_1(self):
        pass

    def test_example16_2(self):
        pass

    def test_example16_4(self):
        pass

    def xtest_example16_6(self):
        pass
        # self.b = '''
        # '''

    def test_example16_15(self):
        pass

    # ------------------------------------------------------------------------------
    # Chapter 17: Measure Repeats, Full-Measure In-Accords

    def test_example17_1(self):
        pass

    def test_example17_2(self):
        pass

    def test_example17_3(self):
        pass

    def test_example17_4(self):
        pass

    def test_example17_5(self):
        pass

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# PART TWO
# Transcribing Two- and Three-Staff Music
#
# ------------------------------------------------------------------------------
# Chapter 24: Bar-over-Bar Format

    def test_example24_1a(self):
        pass

    def test_example24_1b(self):
        pass

    def test_example24_2(self):
        pass

    def test_example24_3(self):
        pass

    def test_example24_4(self):
        pass

    def xtest_example24_5(self):
        pass

    # ------------------------------------------------------------------------------
    # Chapter 26: Interval Signs and Chords

    def test_example26_1a(self):
        pass

    def test_example26_1b(self):
        pass

    def test_example26_2(self):
        pass

    def test_example26_3(self):
        pass

    def test_example26_4(self):
        pass

    def test_example26_5(self):
        pass

    def test_example26_6(self):
        pass
# ------------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , runTest='test_example10_4')

