from binascii import a2b_hex
import copy
import io
import math
import random
import unittest

from music21 import chord
from music21 import converter
from music21 import common
from music21 import corpus
from music21 import environment
from music21 import instrument
from music21 import interval
from music21 import key
from music21 import meter
from music21.midi.base import (
    ChannelVoiceMessages,
    DeltaTime,
    MetaEvents,
    MidiTrack,
    MidiEvent,
    MidiFile,
)
from music21.midi.translate import (
    TimedNoteEvent,
    TranslateWarning,
    channelInstrumentData,
    conductorStream,
    getMetaEvents,
    midiAsciiStringToBinaryString,
    midiEventToInstrument,
    midiEventsToNote,
    midiFileToStream,
    noteToMidiEvents,
    packetStorageFromSubstreamList,
    prepareStreamForMidi,
    streamHierarchyToMidiTracks,
    streamToMidiFile,
    updatePacketStorageWithChannelInfo,
)
from music21.musicxml import testPrimitive
from music21 import note
from music21 import percussion
from music21 import scale
from music21 import stream
from music21 import tempo
from music21 import tie
from music21 import volume

environLocal = environment.Environment('midi.tests')


class Test(unittest.TestCase):

    # ------------ originally in __init__.py, now base.py --------- #

    def testWriteMThdStr(self):
        '''
        Convert bytes of Ascii midi data to binary midi bytes.
        '''
        pass

    def testBasicImport(self):
        pass

        # mf = MidiFile()
        # mf.open(fp)
        # mf.read()
        # mf.close()

    def testInternalDataModel(self):
        pass

        # first object is delta time
        # all objects are pairs of delta time, event

    def testBasicExport(self):
        pass

    def testSetPitchBend(self):
        pass

    def testWritePitchBendA(self):
        pass

    def testImportWithRunningStatus(self):
        pass

        # for n in s.parts[0].notes:
        #    print(n, n.quarterLength)
        # s.show()

    def testReadPolyphonicKeyPressure(self):
        pass

    def testReadUnknownMetaMessage(self):
        pass

    # ------------ originally in translate.py --------------------- #

    def testMidiAsciiStringToBinaryString(self):
        # noinspection PyListCreation
        pass

    def testNote(self):
        pass

    def testStripTies(self):
        # Stream without measures
        pass

    def testTimeSignature(self):
        pass

    def testKeySignature(self):
        pass

        # s.show('midi')

    def testChannelAllocation(self):
        # test instrument assignments
        pass

    def testPacketStorage(self):
        # test instrument assignments
        pass

    def testAnacrusisTiming(self):
        pass

    def testMidiProgramChangeA(self):
        pass
        # p1.show()
        # s.show('midi')

    def testMidiProgramChangeB(self):
        pass

        # s.show('midi')

    def testOverlappedEventsA(self):
        pass

    def testOverlappedEventsB(self):
        pass

        # s.plot('pianoroll')
        # s.show('midi')

    def testOverlappedEventsC(self):
        pass

        # s.show('midi')

    def testExternalMidiProgramChangeB(self):
        pass
        # s.show('midi')

    def testMicrotonalOutputA(self):
        pass

    def testMicrotonalOutputB(self):
        pass

    def testInstrumentAssignments(self):
        # test instrument assignments
        pass

    def testMicrotonalOutputD(self):
        # test instrument assignments with microtones
        pass

        # s.show('midi')

    def testMicrotonalOutputE(self):
        pass

        # post.show('midi', app='Logic Express')

    def testMicrotonalOutputF(self):
        pass

        # post.show('midi', app='Logic Express')

    def testMicrotonalOutputG(self):
        pass

        # post.show('midi')#, app='Logic Express')

    def testMidiTempoImportA(self):
        pass

    def testMidiTempoImportB(self):
        pass

    def testMidiImportMeter(self):
        pass

    def testMidiImportImplicitMeter(self):
        pass

    def testMidiExportConductorA(self):
        '''
        Export conductor data to MIDI conductor track.
        '''
        pass

        # s.show('midi')
        # s.show('midi', app='Logic Express')

    def testMidiExportConductorB(self):
        pass

    def testMidiExportConductorC(self):
        pass

    def testMidiExportConductorD(self):
        '''
        120 bpm and 4/4 are supplied by default.
        '''
        pass

    def testMidiExportConductorE(self):
        '''
        The conductor only gets the first element at an offset.
        '''
        pass

    def testMidiExportConductorF(self):
        '''
        Multiple meter changes
        '''
        pass

    def testMidiExportVelocityA(self):
        pass

    def testMidiExportVelocityB(self) -> None:
        pass
        # s.show('midi')

    def testImportTruncationProblemA(self):
        # specialized problem of not importing last notes
        pass

        # s.show('t')
        # s.show('midi')

    def testImportChordVoiceA(self):
        # looking at cases where notes appear to be chord but
        # are better seen as voices
        # specialized problem of not importing last notes

        # voice 1 -- m1 (half E G) m2 (F# B) m3 -- Chord C4C5 (zero duration?)
        # voice 2 -- m1 whole C  m2 whole D  -- m3 (not existent)
        pass

    def testImportChordsA(self):
        pass

    def testMidiEventsImported(self):
        pass

    def testMidiInstrumentToStream(self):
        pass

    def testImportZeroDurationNote(self):
        '''
        Musescore places zero duration notes in multiple voice scenarios
        to represent double stemmed notes. Avoid false positives for extra voices.
        https://github.com/cuthbertLab/music21/issues/600
        '''
        pass

    def testRepeatsExpanded(self):
        pass

    def testNullTerminatedInstrumentName(self):
        '''
        MuseScore currently writes null bytes at the end of instrument names.
        https://musescore.org/en/node/310158
        '''
        pass

    def testLousyInstrumentData(self):
        pass

    def testConductorStream(self):
        pass

    def testRestsMadeInVoice(self):
        pass

    def testRestsMadeInMeasures(self):
        pass

    def testEmptyExport(self):
        pass

    def testImportInstrumentsWithoutProgramChanges(self):
        '''
        Instrument instances are created from both program changes and
        track or sequence names. Since we have a MIDI file, we should not
        rely on default MIDI programs defined in the instrument module; we
        should just keep track of the active program number.
        https://github.com/cuthbertLab/music21/issues/1085
        '''
        pass

    def testExportUnpitched(self):
        pass

    def testMidiImportLyrics(self):
        pass

    def testMidiExportLyrics(self):
        pass


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    import music21
    music21.mainTest(Test)


