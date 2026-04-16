# ------------------------------------------------------------------------------
# Name:         stream/tests.py
# Purpose:      Tests for streams
#
# Authors:      Michael Scott Asato Cuthbert
#               Christopher Ariza
#
# Copyright:    Copyright © 2009-2024 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
import os
import random
import unittest

import music21
from music21.note import GeneralNote

from music21.stream.base import StreamException
from music21.stream.base import Stream
from music21.stream.base import Voice
from music21.stream.base import Measure
from music21.stream.base import Score
from music21.stream.base import Part
from music21.stream.base import Opus

from music21 import bar
from music21.base import Music21Object
from music21 import beam
from music21 import chord
from music21 import clef
from music21 import common
from music21 import converter
from music21 import corpus
from music21 import defaults
from music21 import duration
from music21 import dynamics
from music21 import environment
from music21 import expressions
from music21 import instrument
from music21 import interval
from music21 import layout
from music21 import key
from music21 import metadata
from music21 import meter
from music21 import note
from music21 import pitch
from music21 import sites
from music21 import spanner
from music21 import tempo
from music21 import text
from music21 import tie
from music21 import variant

from music21.base import Music21Exception, _SplitTuple

from music21.musicxml import m21ToXml

from music21.midi import translate as midiTranslate

environLocal = environment.Environment('stream.tests')


# ------------------------------------------------------------------------------
class TestExternal(unittest.TestCase):
    show = True

    def testLilySimple(self):
        pass

    def testLilySemiComplex(self):
        pass

    def testScoreLily(self):
        '''
        Test the lilypond output of various score operations.
        '''
        pass

    def testMXOutput(self):
        '''
        A simple test of adding notes to measures in a stream.
        '''
        pass

    def testMxMeasures(self):
        '''
        A test of the automatic partitioning of notes in a measure and the creation of ties.
        '''
        pass

    def testMultipartStreams(self):
        '''
        Test the creation of multipart streams by simply having streams within streams.
        '''
        pass

    def testMultipartMeasures(self):
        '''
        This demonstrates obtaining slices from a stream and layering
        them into individual parts.
        '''
        pass

    def testCanons(self):
        '''
        A test of creating a canon with shifted presentations of a source melody.
        This also demonstrates
        the addition of rests to parts that start late or end early.

        The addition of rests happens with makeRests(), which is called in
        musicxml generation of a Stream.
        '''
        pass

    def testBeamsPartial(self):
        '''
        This demonstrates a partial beam; a beam that is not connected between more than one note.
        '''
        pass

    def testBeamsStream(self):
        '''
        A test of beams applied to different time signatures.
        '''
        pass

    def testBeamsMeasure(self):
        pass


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testIsFlat(self):
        pass

    def testAppendFails(self):
        pass


    def testSort(self):
        pass

    def testFlatSimple(self):
        pass

    def testFlattenDocTest(self):
        '''
        This test used to be in OMIT_FROM_DOCS in the flatten() doctest
        '''
        pass

    def testActiveSiteCopiedStreams(self):
        pass

    def testSimpleRecurse(self):
        pass

    def testStreamExceptionsOnAssert(self):
        pass

    def testStreamRecursion(self):
        pass

    def testStreamSortRecursion(self):
        pass

    def testOverlapsA(self):
        pass
        # print(dummy)

    def testOverlapsB(self):

        pass
        # a = Stream()
        # for x in [0, 0, 0, 0, 13, 13, 13]:
        #     n = note.Note('G#')
        #     n.duration = duration.Duration('half')
        #     n.offset = x
        #     a.insert(n)
        # d = a.getOverlaps()
        # len(d[0])
        # 4
        # len(d[13])
        # 3
        # a = Stream()
        # for x in [0, 0, 0, 0, 3, 3, 3]:
        #     n = note.Note('G#')
        #     n.duration = duration.Duration('whole')
        #     n.offset = x
        #     a.insert(n)
        #
        # # default is to not include coincident boundaries
        # d = a.getOverlaps()
        # len(d[0])
        # 7

    def testStreamDuration(self):
        pass

    def testStreamDurationRecalculated(self):
        pass

    def testMeasureStream(self):
        '''
        An approach to setting TimeSignature measures in offsets and durations
        '''
        pass

    def testMultipartStream(self):
        '''
        Test the creation of streams with multiple parts. See versions
        of this tests in TestExternal for more details
        '''
        pass

    def testActiveSites(self):
        '''
        Test activeSite relationships.

        Note that here we see why sometimes qualified class names are needed.
        This test passes fine with class names Part and Measure when run interactively,
        creating a Test instance. When run from the command line
        Part and Measure do not match, and instead music21.stream.Part has to be
        employed instead.
        '''
        pass

    def testActiveSitesMultiple(self):
        '''
        Test an object having multiple activeSites.
        '''
        pass

    def testExtractedNoteAssignLyric(self):
        pass

    def testGetInstrumentFromMxl(self):
        '''
        Test getting an instrument from an mxl file
        '''
        pass

    def testGetInstrumentManual(self):
        # import pdb; pdb.set_trace()
        # search activeSite from a measure within

        # a different test derived from a TestExternal
        pass

    def testMeasureAndTieCreation(self):
        '''
        A test of the automatic partitioning of notes in a measure and the creation of ties.
        '''
        pass

    def testStreamCopy(self):
        '''
        Test copying a stream
        '''
        pass

    def testIteration(self):
        '''
        This test was designed to illustrate a past problem with stream
        Iterations.
        '''
        pass

    def testGetTimeSignatures(self):
        pass

    def testElements(self):
        '''
        Test basic Elements wrapping non music21 objects
        '''
        pass

    def testClefs(self):
        pass

    def testFindConsecutiveNotes(self):
        pass

    def testMelodicIntervals(self):
        pass

        # TODO: Many more tests

    def testMelodicIntervalsB(self):
        pass

    def testStripTiesBuiltA(self):
        pass

    def testStripTiesImportedA(self):
        pass

    def testStripTiesNonMeasureContainers(self):
        '''
        Testing that ties are stripped from containers that are not Measures.
        https://github.com/cuthbertLab/music21/issues/266
        '''
        pass

    def testStripTiesUnlinked(self):
        '''
        After stripping ties, unlinked durations become linked.
        '''
        pass


    def testStripTiesConsecutiveInVoiceNotContainer(self):
        '''
        Testing that ties are stripped from notes consecutive in a voice
        but not consecutive in a flattened parent stream.
        https://github.com/cuthbertLab/music21/issues/568
        '''
        pass

    def testStripTiesChordMembersSomeTied(self):
        '''
        Testing ties NOT stripped where only some chord members are tied.
        https://github.com/cuthbertLab/music21/issues/502
        '''
        pass

    def testStripTiesChordMembersAllTied(self):
        '''
        Testing ties stripped where all chord members are tied.
        '''
        pass

    def testStripTiesReplaceSpannedElements(self):
        '''
        Testing elements in spanners replaced when stripTies removes them.
        '''
        pass

    def testStripTiesClearBeaming(self):
        pass

    def testStripTiesStopTieChordFollowsRest(self):
        '''
        Ensure stripTies() gracefully handles "stop" or "continue" tie types
        following rests as it flattens a stream.
        '''
        pass

    def testGetElementsByOffsetZeroLength(self):
        '''
        Testing multiple zero-length elements with mustBeginInSpan:
        '''
        pass

    def testStripTiesScore(self):
        '''
        Test stripTies using the Score method
        '''
        pass

    def testStripTiesChords(self):
        '''
        Test whether strip ties merges some chords that are the same and
        some that are not.
        '''
        pass

    def testStripTiesChordsAccidentals(self):
        '''
        Make sure chords are matched even if some have 'natural' accidentals and some
        have None accidentals.
        '''
        pass

    def testStripTiesComplexTies(self):
        '''
        Make sure tie types of "stop" or "continue" are not taken at face value
        for Chords if matchByPitch=False; they only represent that SOME
        chord member has that tie type.
        '''
        pass

    def testStripTiesIgnoresUnrealizedChordSymbol(self):
        pass

    def testTwoStreamMethods(self):
        pass

    #    trimPlayingWhileSounding = stream2.trimPlayingWhileSounding(n12)
    #    assert trimPlayingWhileSounding[0] == n22
    #    assert trimPlayingWhileSounding[1].duration.quarterLength == 3.5

    def testMeasureRange(self):
        pass

        # b.show()

    def testMeasureOffsetMap(self):
        pass

    def testMeasureOffsetMapPostTie(self):
        pass

    def testMusicXMLGenerationViaPropertyA(self):
        '''
        Test output tests above just by calling the musicxml attribute
        '''
        pass

    def testMusicXMLGenerationViaPropertyB(self):
        '''
        Test output tests above just by calling the musicxml attribute
        '''
        pass

    def testMusicXMLGenerationViaPropertyC(self):
        '''
        Test output tests above just by calling the musicxml attribute
        '''
        pass

    def testContextNestedA(self):
        '''
        Testing getting clefs from higher-level streams
        '''
        pass

    def testContextNestedB(self):
        '''
        Testing getting clefs from higher-level streams
        '''
        pass

        # 2014 April -- tree version -- not needed
        # this will only work if the callerFirst is manually set to sInnerFlat
        # otherwise, this interprets the DefinedContext object as the first
        # caller
        # pst = sInnerFlat.sites.getObjByClass(clef.Clef, callerFirst=sInnerFlat)
        # self.assertIsInstance(post, clef.AltoClef)

    def testContextNestedC(self):
        '''
        Testing getting clefs from higher-level streams
        '''
        pass

    def testContextNestedD(self):
        '''
        Testing getting clefs from higher-level streams
        '''
        pass

        # s3.show()

    def testMakeRestsA(self):
        pass

    def testMakeRestsB(self):
        # test makeRests fillGaps
        pass
        # s.show('text')
        # s.show()

    def testMakeRestsInMeasures(self):
        pass

    def testMakeRestsInMeasuresWithVoices(self):
        pass

    def testMakeRestsByMakingVoices(self):
        # Create incomplete measure with overlaps, like a MIDI file
        pass

    def testMakeMeasuresInPlace(self):
        pass

    def testMakeMeasuresMeterStream(self):
        '''
        Testing making measures of various sizes with a supplied single element meter stream.
        This illustrates an approach to partitioning elements by various sized windows.
        '''
        pass

    def testMakeMeasuresWithBarlines(self):
        '''
        Test makeMeasures with optional barline parameters.
        '''
        pass

    def testMakeMeasuresLastElementNoDuration(self):
        pass

    def testRemove(self):
        '''
        Test removing components from a Stream.
        '''
        pass

    def testRemoveByClass(self):
        pass

    def testReplace(self):
        '''
        Test replacing components from a Stream.
        '''
        pass

    def testReplaceA1(self):
        pass

    def testReplaceB(self):
        pass

    def testReplaceDerived(self):
        pass

    def testDoubleStreamPlacement(self):
        pass

    def testBestTimeSignature(self):
        '''
        Get a time signature based on components in a measure.
        '''
        pass

    def testGetKeySignatures(self):
        '''
        Searching contexts for key signatures
        '''
        pass

    def testGetKeySignaturesThreeMeasures(self):
        '''
        Searching contexts for key signatures
        '''
        pass

    def testMakeAccidentalsA(self):
        '''
        Test accidental display setting
        '''
        pass

    def testMakeAccidentalsB(self):
        pass

    def testMakeAccidentalsC(self):
        # this isolates the case where a new measure uses an accidental
        # that was used in a past measure

        pass

    def testMakeAccidentalsD(self):
        pass

    def testMakeAccidentalsInScore(self):
        '''
        Making accidentals on a score having a part with measures
        should still reiterate accidentals measure by measure.
        '''
        pass

    def testMakeAccidentalsWithKeysInMeasures(self):
        pass
        # TODO: add tests
        # s.show()

    def testMakeAccidentalsTies(self):
        '''
        tests to make sure that Accidental display status is correct after a tie.
        '''
        pass

    def testMakeAccidentalsRespectsDisplayType(self):
        pass

        # TODO: other types

    def testMakeAccidentalsOnChord(self):
        pass

    def testMakeNotationTiesKeyless(self):
        pass

    def testMakeNotationTiesKeyChange(self):
        pass

    def testMakeAccidentalsOctaveKS(self):
        pass

    def testScaleOffsetsBasic(self):
        pass

    def testScaleOffsetsBasicInPlaceA(self):
        pass

    def testScaleOffsetsBasicInPlaceB(self):
        pass

    def testScaleOffsetsBasicInPlaceC(self):
        pass

    def testScaleOffsetsBasicInPlaceD(self):
        pass

    def testScaleOffsetsNested(self):
        pass

    def testScaleDurationsBasic(self):
        '''
        Scale some durations, independent of offsets.
        '''
        pass

    def testAugmentOrDiminishBasic(self):

        pass

    def testAugmentOrDiminishHighestTimes(self):
        '''
        Need to make sure that highest offset and time are properly updated
        '''
        pass

    def testAugmentOrDiminishCorpus(self):
        '''
        Extract phrases from the corpus and use for testing
        '''
        pass
        # s.show()

    def testMeasureBarDurationProportion(self):
        pass

        # m.shiftElementsAsAnacrusis()
        # self.assertEqual(m.notesAndRests[0].offset, 3.0)
        # self.assertEqual(n1.offset, 3.0)
        # self.assertEqual(n2.offset, 3.5)
        # self.assertAlmostEqual(m.barDurationProportion(), 1.0, 4)

    def testInsertAndShiftBasic(self):
        pass

    def testInsertAndShiftNoDuration(self):
        pass

    def testInsertAndShiftMultipleElements(self):
        pass

    def testMetadataOnStream(self):

        pass
        # s.show()

    def testMeasureBarline(self):
        pass

    def testMeasureLayout(self):
        '''
        test both system layout and measure width
        '''
        pass

    def testYieldContainers(self):
        pass

        # environLocal.printDebug(['upward, with skipDuplicates:'])
        # match = []
        # # must provide empty list for memo
        # for x in s7._yieldReverseUpwardsSearch([], streamsOnly=True, skipDuplicates=True):
        #     match.append(x.id)
        #     # environLocal.printDebug([x, x.id, 'activeSite', x.activeSite])
        # self.assertEqual(match, ['3c', '2a', '1a', '2b', '2c', '3a', '3b'] )

        # environLocal.printDebug(['upward from a single node, with skipDuplicates'])
        # match = []
        # for x in s10._yieldReverseUpwardsSearch([], streamsOnly=True):
        #     match.append(x.id)
        #     # environLocal.printDebug([x, x.id, 'activeSite', x.activeSite])
        #
        # self.assertEqual(match, ['3f', '2c', '1a', '2a', '2b'] )

        # environLocal.printDebug(['upward with skipDuplicates=False:'])
        # match = []
        # for x in s10._yieldReverseUpwardsSearch([], streamsOnly=True, skipDuplicates=False):
        #     match.append(x.id)
        #     # environLocal.printDebug([x, x.id, 'activeSite', x.activeSite])
        # self.assertEqual(match, ['3f', '2c', '1a', '2a', '1a', '2b', '1a'] )

        # environLocal.printDebug(['upward, with skipDuplicates, streamsOnly=False:'])
        # match = []
        # # must provide empty list for memo
        # for x in s8._yieldReverseUpwardsSearch([], streamsOnly=False,
        #     skipDuplicates=True):
        #     match.append(x.id)
        #     environLocal.printDebug([x, x.id, 'activeSite', x.activeSite])
        # self.assertEqual(match, ['3d', 'n2(2b)', '2b', 'n(1a)', '1a', '2a', '2c', '3e'] )

        # environLocal.printDebug(['upward, with skipDuplicates, streamsOnly=False:'])
        # match = []
        # # must provide empty list for memo
        # for x in s4._yieldReverseUpwardsSearch([], streamsOnly=False,
        #     skipDuplicates=True):
        #     match.append(x.id)
        #     # environLocal.printDebug([x, x.id, 'activeSite', x.activeSite])
        # # notice that this does not get the nonContainers for 2b
        # self.assertEqual(match, ['2c', 'n(1a)', '1a', '2a', '2b'] )

    def testMidiEventsBuilt(self):
        pass

    def testFindGaps(self):
        pass

    def testQuantize(self):

        pass

    def testQuantizeMinimumDuration(self):
        '''
        Notes (not rests!) of nonzero duration should retain a nonzero
        duration after quantizing. Zero duration rests should be removed.
        '''
        pass

    def testAnalyze(self):

        pass

    def testMakeTupletBracketsA(self):
        '''
        Creating brackets
        '''
        pass
        # s.show()

    def testMakeTupletBracketsB(self):
        '''
        Creating brackets
        '''
        pass
        # s.show()

    def testMakeNotationA(self):
        '''
        This is a test of many make procedures
        '''
        pass

        # s.show()

    def testMakeNotationB(self):
        '''
        Testing voices making routines within make notation
        '''
        pass

    def testMakeNotationC(self):
        '''
        Test creating diverse, overlapping durations and notes
        '''
        pass

    def testMakeNotationScoreA(self):
        '''
        Test makeNotation on Score objects
        '''
        pass

    def testMakeNotationScoreB(self):
        '''
        Test makeNotation on Score objects
        '''
        pass

    def testMakeNotationScoreC(self):
        '''
        Test makeNotation on Score objects
        '''
        pass

    def testMakeNotationKeySignatureOneVoice(self):
        '''
        The base-case: Stream should keep it's key.KeySignature element when a
        single-voice score is prepared for notation.
        '''
        pass

    def testMakeNotationKeySignatureMultiVoice(self):
        '''
        Stream should keep its key.KeySignature element
        when a multi-voice score is prepared for notation.
        '''
        pass

    def testMakeTies(self):
        pass

    def testMakeTiesAddNewMeasure(self):
        '''
        Test that makeTies adds a new measure when the last note is too long,
        both when called directly and when called from makeNotation
        '''
        pass

    def testMeasuresAndMakeMeasures(self):
        pass
        # sSub.show()

    def testSortAndAutoSort(self):
        pass

    def testMakeChordsBuiltA(self):
        # test with equal durations
        pass
        # print('post chordify')
        # s.show('t')
        # sMod.show('t')
        # s.show()

    def testMakeChordsBuiltB(self):
        pass

    def testMakeChordsBuiltC(self):
        # test removal of redundant pitches
        pass

    def testMakeChordsBuiltD(self):
        # attempt to isolate case
        pass
        # post.show()

    def testGetElementAtOrBeforeBarline(self):
        '''
        problems with getting elements at or before when triplets were involved.
        '''
        pass

    def testElementsHighestTimeA(self):
        '''
        Test adding elements at the highest time position
        '''
        pass

    def testStoreAtEndFailures(self):
        pass

    def testElementsHighestTimeB(self):
        '''
        Test adding elements at the highest time position
        '''
        pass

    def testElementsHighestTimeC(self):

        pass

    def testSliceByQuarterLengthsBuilt(self):
        pass

    def testSliceByQuarterLengthsImported(self):

        pass

    def testSliceByGreatestDivisorBuilt(self):

        pass

    def testSliceByGreatestDivisorImported(self):

        pass

        # s = corpus.parse('bwv66.6')
        # s.sliceByGreatestDivisor(inPlace=True, addTies=True)
        # s.flatten().chordify().show()
        # s.show()

    def testSliceAtOffsetsSimple(self):
        pass

    def testSliceAtOffsetsBuilt(self):
        pass

    def testSliceAtOffsetsImported(self):
        pass

    def testSliceByBeatBuilt(self):
        pass

    def testSliceByBeatImported(self):
        pass

        # post.show()

    def testChordifyImported(self):
        pass
        # Careful! one version of the caching is screwing up m. 20 which definitely should
        # not have rests in it -- was creating 69 notes, not 71.

    def testChordifyRests(self):
        # test that chordify does not choke on rests
        pass

    def testChordifyA(self):
        pass
        # post.show()

        # s.show()

    def testChordifyB(self):
        pass
        # post.show()

    def testChordifyC(self):
        '''
        Chordifies with triplets (floating point errors)
        '''
        pass

    def testChordifyD(self):
        # test on a Stream of Streams.
        pass

    def testChordifyE(self):
        pass

    # noinspection SpellCheckingInspection
    def testOpusSearch(self):
        pass

    def testOpusSequence(self):
        '''
        Providing a sequence of Scores to an Opus container should append
        rather than insert each at 0.0.
        '''
        pass

    def testActiveSiteMangling(self):
        pass

    def testGetElementsByContextStream(self):

        pass

    def testVoicesA(self):

        pass

    def testVoicesALonger(self):

        # try version longer than 1 measure, more than 2 voices
        pass
        # s.show()

    def testVoicesB(self):

        # make sure strip ties works
        pass

        # s.show()

    def testVoicesC(self):
        pass

        # sPost.show()

    def testPartsToVoicesA(self):
        pass

        # s1.show()
        # p1.show()

    def testPartsToVoicesB(self):
        # this work has five parts: results in e parts
        pass

        # s1.show()

        # s0 = corpus.parse('hwv56', '1-05')
        # # can use index values
        # s2 = s0.partsToVoices(([0, 1], [2, 4], 3), permitOneVoicePerPart=True)
        # self.assertEqual(len(s2.parts), 3)
        # self.assertEqual(len(s2.parts[0].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[1].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[2].getElementsByClass(
        #     'Measure')[0].voices), 1)

        # s2 = s0.partsToVoices((['Violino I', 'Violino II'], ['Viola', 'Bassi'], ['Basso']),
        #        permitOneVoicePerPart=True)
        # self.assertEqual(len(s2.parts), 3)
        # self.assertEqual(len(s2.parts[0].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[1].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[2].getElementsByClass(
        #     'Measure')[0].voices), 1)
        # # this will keep the voice part unaltered
        # s2 = s0.partsToVoices((['Violino I', 'Violino II'], ['Viola', 'Bassi'], 'Basso'),
        #        permitOneVoicePerPart=False)
        # self.assertEqual(len(s2.parts), 3)
        # self.assertEqual(len(s2.parts[0].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[1].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(s2.parts[2].getElementsByClass(
        #     'Measure')[0].hasVoices(), False)

        # # mm 16-19 are a good examples
        # s1 = corpus.parse('hwv56', '1-05').measures(16, 19)
        # s2 = s1.partsToVoices((['Violino I', 'Violino II'], ['Viola', 'Bassi'], 'Basso'))
        # # s.show()

        # self.assertEqual(len(s2.parts), 3)
        # self.assertEqual(len(s2.parts[0].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(len(s2.parts[1].getElementsByClass(
        #     'Measure')[0].voices), 2)
        # self.assertEqual(s2.parts[2].getElementsByClass(
        #     'Measure')[0].hasVoices(), False)

    def testPartsToVoicesSpanner(self):
        # NOTE: this test spanners merged from two parts into one part
        pass

    def testVoicesToPartsA(self):

        pass

        # s1.show()

    def testVoicesToPartsNonNoteElementPropagation(self):
        pass

    def testMergeElements(self):
        pass

    def testDeepcopySpanners(self):
        pass
        # s2.show('t')
        # s2.show()

    def testAddSlurByMelisma(self):
        pass
            # environLocal.printDebug(['melisma beat:', beatStr.ljust(6), 'average duration:', avg])

    def testTwoZeroOffset(self):
        pass
        # environLocal.printDebug([p.offsetMap()])

    def testStripTiesBuiltB(self):
        pass

        # s3.show()

    def testStripTiesImportedB(self):

        # this file was imported by sibelius and does not have completed ties
        pass

    def testDerivationA(self):

        pass

    def testDerivationB(self):
        pass

    def testDerivationC(self):
        pass

    def testDerivationMethodA(self):
        pass

    def testContainerHierarchyA(self):
        pass

        # still cannot get hierarchy
        # self.assertEqual([str(e.__class__) for e in s.parts[0].containerHierarchy()], [])

    def testMakeMeasuresTimeSignatures(self):
        pass

    def testDeepcopyActiveSite(self):
        # test that active sites make sense after deepcopying
        pass

    def testRecurseA(self):
        pass

        # rElements = list(s.recurse(streamsOnly=True))
        # self.assertEqual(len(rElements), 45)
        #
        # p1 = rElements[1]
        # m1 = rElements[2]
        # # m = rElements[3]
        # m2 = rElements[4]
        # self.assertIs(p1.activeSite, s)
        # self.assertIs(m1.activeSite, p1)
        # self.assertIs(m2.activeSite, p1)
        #
        #
        # rElements = list(s.recurse(classFilter='KeySignature'))
        # self.assertEqual(len(rElements), 4)
        # # the first elements active site is the measure
        # self.assertEqual(id(rElements[0].activeSite), id(m1))
        #
        # rElements = list(s.recurse(classFilter=['TimeSignature']))
        # self.assertEqual(len(rElements), 4)
        #
        #
        # s = corpus.parse('bwv66.6')
        # m1 = s[2][1]  # cannot use parts here as breaks active site
        # rElements = list(m1.recurse(direction='upward'))
        # self.assertEqual([str(e.classes[0]) for e in rElements], ['Measure',
        #                                                           'Instrument',
        #                                                           'Part',
        #                                                           'Metadata',
        #                                                           'Part',
        #                                                           'Score',
        #                                                           'Part',
        #                                                           'Part',
        #                                                           'StaffGroup',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure',
        #                                                           'Measure'])
        # self.assertEqual(len(rElements), 18)


    def testRecurseB(self):

        pass

    def testTransposeScore(self):

        pass

    def testExtendDurationA(self):
        # spanners in this were causing some problems
        pass
        # b= a.flatten().extendDuration(dynamics.Dynamic)

    def testSpannerTransferA(self):
        # test getting spanners after .measures extraction
        pass
        # self.assertEqual()
        # TODO: compare ids of new measures

    def testMeasureGrouping(self):

        pass

    def testMakeNotationByMeasuresA(self):
        pass

    def testMakeNotationByMeasuresB(self):
        pass

    def testHaveAccidentalsBeenMadeA(self):
        pass

    def testHaveAccidentalsBeenMadeB(self):
        pass

    def testHaveAccidentalsBeenMadeInVoices(self):
        pass

    def testHaveBeamsBeenMadeA(self):
        pass

    def testHaveBeamsBeenMadeB(self):
        pass

    def testFlatCachingA(self):
        pass

    def testFlatCachingB(self):
        pass

    def testFlatCachingC(self):
        pass
        # q2.measures(1, 2).show('text')

    def testInvertDiatonicQuickSearch(self):
        '''
        doctests sufficiently search invertDiatonic for complex cases,
        but not simple ones.
        '''
        pass

    def testSemiFlatCachingA(self):

        pass
        # environLocal.printDebug(['beatStr', beatStr])

    def testFlattenUnnecessaryVoicesA(self):
        pass

    def testGetElementBeforeOffsetA(self):
        pass

    def testGetElementBeforeOffsetB(self):
        pass

    def testFinalBarlinePropertyA(self):
        pass
        # s.show()

    def testFinalBarlinePropertyB(self):
        pass

    def testSetElementsFromOtherStreamWithEndElements(self):
        pass

    def testStreamElementsComparison(self):
        pass

    def testSecondsPropertyA(self):
        # simple case of one tempo
        pass

    def testSecondsPropertyB(self):
        pass

    def testSecondsPropertyC(self):
        pass

    # TODO: New piece with Metronome Mark Boundaries
    # def testMetronomeMarkBoundaries(self):
    #     s = corpus.parse('hwv56/movement2-09.md')
    #     mmBoundaries = s.metronomeMarkBoundaries()
    #     self.assertEqual(str(mmBoundaries),
    #            '[(0.0, 20.0, <music21.tempo.MetronomeMark Largo e piano Quarter=46>)]')

    def testAccumulatedTimeA(self):
        pass

    def testAccumulatedTimeB(self):
        # changing in the middle of boundary
        pass

    def testSecondsMapA(self):
        pass

    def testSecondsMapB(self):
        # one start stream
        pass

    def testPartDurationA(self):
        # s= corpus.parse('bach/bwv7.7')
        pass

        # sPost = sNew.chordify()
        # sPost.show()

    def testPartDurationB(self):
        pass

    def testChordifyTagPartA(self):
        pass

    def testChordifyTagPartB(self):
        pass

    def testTransposeByPitchA(self):
        pass

    def testTransposeByPitchB(self):
        pass

    def testTransposeByPitchC(self):
        pass

    def testExtendTiesA(self):
        pass

    def testExtendTiesB(self):
        pass
        # sChords.show()

    def testInsertIntoNoteOrChordA(self):
        pass
        # s.show('text')

    def testInsertIntoNoteOrChordB(self):
        pass

    def testSortingAfterInsertA(self):
        pass

    def testInvertDiatonicA(self):
        # TODO: Check results

        pass

    def testMeasuresA(self):
        pass

    def testMeasuresB(self):
        pass

    def testMeasuresC(self):
        pass
        # ex.show()

    def testMeasuresSuffix(self):
        pass

    def testChordifyF(self):
        # testing chordify handling of triplets
        pass
        # pitch grouping in measure index 1 was not allocated properly
        # for c in chords.getElementsByClass(chord.Chord):
        #    self.assertEqual(len(c), 2)

    def testChordifyG(self):
        # testing a problem in triplets in makeChords
        pass

    def testMakeVoicesA(self):
        pass

        # s.show()

    def testMakeVoicesB(self):
        pass

    def testSplitAtQuarterLengthA(self):
        pass


    def testSplitAtQuarterLengthB(self):
        '''
        Test if recursive calls work over voices in a Measure
        '''
        pass
        # sPost.show()

    def testSplitAtQuarterLengthC(self):
        '''
        Test splitting a Score
        '''
        pass
        # sLeft.show()
        # sRight.show()

    def testSplitByQuarterLengths(self):
        '''
        Was not returning splitTuples before
        '''
        pass



    def testGracesInStream(self):
        '''
        testing grace notes
        '''
        pass

    def testGraceChords(self):


        pass

        # s.show()

    def testScoreShowA(self):
        # this checks the specific handling of Score.makeNotation()

        pass

    def testGetVariantsA(self):
        pass

    def testActivateVariantsA(self):
        '''
        This tests a single-measure variant
        '''
        pass

    def testActivateVariantsB(self):
        '''
        This tests two variants with different groups, each a single measure
        '''
        pass

    def testActivateVariantsC(self):
        '''
        This tests a two-measure variant
        '''
        pass

    def testActivateVariantsD(self):
        '''
        This tests a note-level variant
        '''
        pass

        # note that if the start times of each component do not match, the
        # variant part will not be matched

    def testActivateVariantsE(self):
        '''
        This tests a note-level variant with miss-matched rhythms
        '''
        pass

    def testActivateVariantsBySpanA(self):
        '''
        test replacing 1 note with a 3-note variant
        '''
        pass

        # s.show()

    def testActivateVariantsBySpanB(self):
        '''
        test replacing 2 measures by a longer single measure
        '''
        pass
        # s.show()

    def testTemplateAll(self):
        pass



    def testSetElements(self):
        pass

    def testGetElementAfterElement(self):
        pass
            # print(note1, note2, note3, note4)
            # print(note1.id, note2.id, note3.id, note4.id)
        # TEST???

    def testCoreGuardBeforeAddElement(self):
        pass

    # REMOVED: Turns out that it DOES have fermata on every note!
    # def testSchoenbergChordifyFermatas(self):
    #     '''
    #     test that after chordification, only
    #     the specific time point with a fermata has a fermata.
    #     '''
    #     schoenberg = corpus.parse('schoenberg/opus19', 6)
    #     excerpt = schoenberg.measures(10, 10)
    #     chordBefore = excerpt.parts[0].getElementsByClass(Measure)[0].notes[0]
    #     for n in chordBefore:
    #         print(n, n.expressions)
    #     return
    #     chordStream = excerpt.chordify()
    #
    #     m10 = chordStream.getElementsByClass(Measure)[0]
    #     c0 = m10.notes[0]
    #     self.assertEqual(c0.expressions, [])
    #     cLastButOne = m10.notes[-2]
    #     self.assertEqual(len(cLastButOne.expressions), 1)
    #     self.assertIn('Fermata', cLastButOne.expressions[0])
    #     cLast = m10.notes[-1]
    #     self.assertEqual(cLast.expressions, [])

    @staticmethod
    def get_beams_from_stream(srcList):
        '''
        Helper function to return beam list for all notes and rests in the stream.
        '''
        pass

    def test_makeBeams__all_quarters(self):
        '''
        Test that for a measure full of quarters, there are no beams
        '''
        pass

    def test_makeBeams__all_eighths(self):
        '''
        Test a full measure full of eighth is grouped by beams into couples
        '''
        pass

    def test_makeBeams__eighth_rests_and_eighth(self):
        '''
        Test a full measure of 8th rest followed by 8th note
        '''
        pass

    def test_makeBeams__repeated_1_e_a(self):
        '''
        Test that the pattern of "1 e a" repeated more than once has correct beams.

        Note: proper beams repr: https://share.getcloudapp.com/12uE7eBA
        '''
        pass

    def test_makeBeams__1_e_n_a(self):
        '''
        Test that 4 16th notes have proper beams across them all.
        '''
        pass

    def test_makeBeams__1_e__after_16th_note(self):
        '''
        Test that a 16th+8th notes after a 16th notes have proper beams.
        '''
        pass

    def test_makeBeams__paddingLeft_2_2(self):
        pass

    def test_makeBeams__paddingRight(self):
        pass

    def testWrite(self):
        pass

    def testOpusWrite(self):
        pass

    def testActiveSiteAfterBoolIteration(self):
        pass
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    music21.mainTest(Test, 'verbose')
