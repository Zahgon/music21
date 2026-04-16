# ------------------------------------------------------------------------------
# Name:         alpha/analysis/hasher.py
# Purpose:      Hash musical notation
#
# Authors:      Emily Zhang
#
# Copyright:    Copyright © 2015 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import collections
import difflib
import unittest

from music21 import chord
from music21 import key
from music21 import interval
from music21 import note
from music21 import stream


class Hasher:
    '''
    This is a modular hashing object that can hash notes, chords, and rests, and some of their
    properties. Steps to using and calling the hasher:

    1) Initialize a hasher object

    2) Set the properties that you want to hash. There are 4 main groups of properties/settings::

        a) self.validTypes should be some combination of notes, chords, rests

        b) general hashing settings include self.includeReference. if
           self.includeReference is True, a reference to the original note/rest/chord is created
           and kept track of during the hashing process.

        c) note properties are things like pitch, duration, offset, and some slightly fancier
           properties

        d) self.stateVars is a dictionary of things you might want to hash that require some memory
           e.g. current key signature, interval from the last note

    3) call the hashStream() function on the stream you want to hash.

    This is what the Hasher object does the in background once hashStream() is called:

    1) It runs self.setupValidTypesAndStateVars() and sets up properties from (a) and (d) from
    above based on your settings

    2) It runs self.preprocessStream() and based on settings from (d)

    3) It determines which objects in the passed-in stream should be hashed

    4) It runs self.setupTupleList() and sets up self.tupleList, self.hashingFunctions
    and self.tupleClass, all related to each other. self.tupleList is a list of all the
    properties that are hashed. self.hashingFunctions is a dictionary of which hashing function
    should be used for each property (there are multiple ways of hashing a note's pitch, for
    example, by MIDI number, or by a string representation). self.tupleClass is a NamedTuple
    that is constructed ad hoc based on which properties are to be hashed.

    5) For all the elements from the stream that are to be hashed, the hasher hashes every one of
    its properties that are to be hashed using the hashing function listed in
    self.hashingFunctions. It creates a single NamedTuple called a NoteHash for each element
    from the stream. However, if self.includeReference is set to True, a NoteHashWithReference
    tuple is created instead.
    '''

    def __init__(self):
        '''
        The Hasher object is initialized with defaults of what objects should be hashed, and
        what properties of those objects should be hashed.
        '''

        # --- begin general types of things to hash ---
        self.validTypes = [note.Note, note.Rest, chord.Chord]
        # --- end general types of things to hash ---

        # --- begin general hashing settings ---
        self.includeReference = False
        # --- end general hashing settings ---

        # --- begin note properties to hash ---
        self.hashPitch = True
        # hashMIDI = True => 58 instead of 'C--'
        self.hashMIDI = True
        # hashNoteNameOctave = False => 'C4' instead of 'C'
        self.hashNoteNameOctave = False
        self.hashOctave = False
        self.hashDuration = True
        self.roundDurationAndOffset = True
        self.hashOffset = True
        # self.roundOffset = True
        self.granularity = 32
        self.hashIntervalFromLastNote = False
        self.hashIsAccidental = False
        self.hashIsTied = False
        # --- end note properties to hash ---

        # --- begin chord properties to hash ---  #
        # chords can be hashed as chords or by their note constituents
        self.hashChordsAsNotes = True
        self.hashChordsAsChords = False
        self.hashNormalOrderString = False
        self.hashPrimeFormString = False
        # --- end chord properties to hash ---  #

        self.tupleList = []
        self.tupleClass = None
        # stateVars are variables that are kept track of through multiple hashes
        # e.g. interval from the previous note, key signature
        self.stateVars = {}
        self.hashingFunctions = {}

    def setupValidTypesAndStateVars(self):
        '''
        Sets up the self.stateVars dictionary depending on how the flags for
        self.hashIntervalFromLastNote and self.hashIsAccidental are set.

        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.hashIntervalFromLastNote = True
        >>> h.setupValidTypesAndStateVars()
        >>> h.stateVars
        {'IntervalFromLastNote': None}

        >>> h2 = alpha.analysis.hasher.Hasher()
        >>> h2.hashIsAccidental = True
        >>> h2.setupValidTypesAndStateVars()
        >>> h2.stateVars
        {'KeySignature': None}

        >>> key.KeySignature in h2.validTypes
        True
        '''
        pass

        # -- Begin Individual Hashing Functions of Properties---
    def _hashDuration(self, e, thisChord=None):
        '''
        returns the duration of a chord object passed in, otherwise the duration of a note
        object passed in.

        >>> h = alpha.analysis.hasher.Hasher()
        >>> n = note.Note('A-', quarterLength=2.5)
        >>> h._hashDuration(n)
        2.5

        >>> d = duration.Duration(2.0)
        >>> c = chord.Chord('A-4 C#5 E5', duration=d)
        >>> h._hashDuration(n, thisChord=c)
        2.0
        '''
        pass

    def _hashRoundedDuration(self, e, thisChord=None):
        '''
        TODO: Check if this is working
        '''
        pass

    def _hashMIDIPitchName(self, e, thisChord=None):
        '''
        returns midi pitch value (21-108) of a note
        returns 0 if rest
        returns 1 if not hashing individual notes of a chord

        >>> n = note.Note(72)
        >>> c = chord.Chord('A-4 C#5 E5')
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.hashChordsAsChords = True
        >>> h._hashMIDIPitchName(n, thisChord=c)
        1
        >>> h.hashChordsAsChords = False
        >>> h._hashMIDIPitchName(n, thisChord=c)
        72
        >>> r = note.Rest()
        >>> h._hashMIDIPitchName(r, thisChord=c)
        0

        '''
        pass

    def _hashPitchName(self, e, thisChord=None):
        '''
        returns string representation of a note e.g. 'F##4'
        returns 'r' if rest
        returns 'z' if not hashing individual notes of a chord (i.e. hashing chords as chords)

        >>> n = note.Note(72)
        >>> c = chord.Chord('A-4 C#5 E5')
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.hashChordsAsChords = True
        >>> h._hashPitchName(n, thisChord=c)
        'z'
        >>> h.hashChordsAsChords = False
        >>> h._hashPitchName(n, thisChord=c)
        'C5'
        >>> r = note.Rest()
        >>> h._hashPitchName(r, thisChord=c)
        'r'
        '''
        pass

    def _hashPitchNameNoOctave(self, e, thisChord=None):
        '''
        returns string representation of a note without the octave e.g. 'F##'
        returns 'r' if rest
        returns 'z' if not hashing individual notes of a chord

        >>> n = note.Note(72)
        >>> c = chord.Chord('A-4 C#5 E5')
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.hashChordsAsChords = True
        >>> h._hashPitchNameNoOctave(n, thisChord=c)
        'z'
        >>> h.hashChordsAsChords = False
        >>> h._hashPitchNameNoOctave(n, thisChord=c)
        'C'
        >>> r = note.Rest()
        >>> h._hashPitchNameNoOctave(r, thisChord=c)
        'r'
        '''
        pass

    def _hashOctave(self, e, thisChord=None):
        '''
        returns octave number of a note
        returns -1 if rest or not hashing individual notes of a chord

        >>> n = note.Note(72)
        >>> c = chord.Chord('A-4 C#5 E5')
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.hashChordsAsChords = True
        >>> h._hashOctave(c, thisChord=c)
        -1
        >>> h.hashChordsAsChords = False
        >>> h._hashOctave(n, thisChord=c)
        5
        >>> r = note.Rest()
        >>> h._hashOctave(r, thisChord=c)
        -1
        '''
        pass

    def _hashIsAccidental(self, e, thisChord=None):
        # TODO: figure out how to tell if note is accidental based on key sig
        pass

    def _hashRoundedOffset(self, e, thisChord=None):
        '''
        Returns offset rounded to the nearest subdivided beat.
        The subdivided beat is indicated with self.granularity.
        By default, the granularity is set to 32, or 32nd notes
        '''
        pass

    def _hashOffset(self, e, thisChord=None):
        '''
        returns an unrounded floating point representation of a note's offset
        '''
        pass

    def _hashIntervalFromLastNote(self, e, thisChord=None):
        '''
        returns the interval between last note and current note, if extant
        known issues with first note of every measure in transposed pieces
        returns 0 if things don't work
        '''
        pass

    def _hashPrimeFormString(self, e, thisChord=None):
        '''
        returns prime form of a chord as a string e.g. '<037>'
        returns '<>' otherwise
        '''
        pass

    def _hashChordNormalOrderString(self, e, thisChord=None):
        '''
        returns normal order of a chord as a string e.g. '<047>'
        returns '<>' otherwise
        '''
        pass

    # --- End Individual Hashing Functions

    def setupTupleList(self):
        '''
        Sets up self.hashingFunctions, a dictionary of which properties of self.validTypes should
        be hashed and which hashing functions should be used for those properties. Creates a
        tupleList of all the properties that are hashed and uses that to create a named tuple
        NoteHash with those properties. This is how we can generate a malleable named tuple
        NoteHash that is different depending upon which properties a particular instance of
        Hasher object hashes.
        '''
        pass

    def hashMeasures(self, s):
        '''
        lightweight hasher. only hashes number of notes, first and last pitch
        '''

    def hashStream(self, s):
        '''
        This method is the meat of the program. It goes through all the elements that are left
        to be hashed and individually hashes them by looking up which hashing functions ought
        to be used on each element and passing off the element to the method
        self.addSingleNoteHashToFinalHash, which creates the appropriate hash for that element
        and adds it to self.finalHash
        '''
        pass

    def addHashToFinalHash(self, singleNoteHash, finalHash, reference):
        pass

    def addNoteHashWithReferenceToFinalHash(self, finalHash, tupleHash, reference):
        # noinspection PyShadowingNames
        '''
        creates a NoteHashWithReference object from tupleHash and with the reference pass in
        and adds the NoteHashWithReference object to the end of finalHash

        >>> from collections import namedtuple
        >>> n = note.Note('C4')
        >>> NoteHash = namedtuple('NoteHash', ['Pitch', 'Duration'])
        >>> nh = NoteHash(n.pitch, n.duration)
        >>> finalHash = []
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.addNoteHashWithReferenceToFinalHash(finalHash, nh, n)
        >>> finalHash
        [NoteHashWithReference(Pitch=C4, Duration=<music21.duration.Duration 1.0>)]

        >>> finalHash[0].reference.id == n.id
        True
        '''
        pass

    def addNoteHashToFinalHash(self, finalHash, tupleHash):
        # noinspection PyShadowingNames
        '''
        creates a NoteHash object from tupleHash and adds the NoteHash
        object to the end of finalHash

        >>> from collections import namedtuple
        >>> n = note.Note('C4')
        >>> NoteHash = namedtuple('NoteHash', ['Pitch', 'Duration'])
        >>> nh = NoteHash(n.pitch, n.duration)
        >>> finalHash = []
        >>> h = alpha.analysis.hasher.Hasher()
        >>> h.addNoteHashToFinalHash(finalHash, nh)
        >>> finalHash
        [(<music21.pitch.Pitch C4>, <music21.duration.Duration 1.0>)]
        '''
        pass

#     def addSingleNoteHashToFinalHash(self, singleNoteHash, finalHash, reference=None):
#         # TODO: use the linter, reference DOESN'T have to be passed in
#         # what is reference? it's a hashable music21 elt, write documentation
#         tupleHash = (self.tupleClass._make(singleNoteHash))
#         if self.includeReference:
#             nhwr = NoteHashWithReference(tupleHash)
#             if reference.derivation.rootDerivation is not None:
#                 nhwr.reference = reference.derivation.rootDerivation
#             else:
#                 nhwr.reference = reference
#             finalHash.append(nhwr)
#         else:
#             nh = NoteHash(tupleHash)
#             finalHash.append(nh)

    # --- Begin Rounding Helper Functions ---

    def _getApproxDurOrOffset(self, durOrOffset):
        pass

    def _approximatelyEqual(self, a, b, sig_fig=4):
        '''
        use to look at whether beat lengths are close, within a certain range
        probably can use for other things that are approx. equal
        '''
        pass

    # --- End Rounding Helper Functions ---


class NoteHashWithReference:
    # noinspection PyShadowingNames
    '''
    returns tuple with reference to original note or chord or rest

    >>> from collections import namedtuple
    >>> NoteHash = namedtuple('NoteHash', ['Pitch', 'Duration'])
    >>> nh = NoteHash(60, 4)
    >>> nhwr = alpha.analysis.hasher.NoteHashWithReference(nh)
    >>> nhwr.reference = note.Note('C4')
    >>> nhwr
    NoteHashWithReference(Pitch=60, Duration=4)

    >>> nhwr.Pitch
    60
    >>> nhwr.Duration
    4

    >>> nhwr.hashItemsKeys
    ('Pitch', 'Duration')

    >>> for val in nhwr:
    ...     print(val)
    60
    4

    >>> nhwr.reference
    <music21.note.Note C>
    '''

    def __init__(self, hashItemsNT):
        self.reference = None
        hashItemsDict = hashItemsNT._asdict()
        for x in hashItemsDict:
            setattr(self, x, hashItemsDict[x])
        self.hashItemsKeys = tuple(hashItemsDict.keys())

    def __iter__(self):
        for keyName in self.hashItemsKeys:
            yield getattr(self, keyName)

    def __repr__(self):
        nhStrAll = 'NoteHashWithReference('

        vals = []
        for x in self.hashItemsKeys:
            nhStr = x
            nhStr += '='
            nhStr += str(getattr(self, x))
            vals.append(nhStr)
        nhStrAll += ', '.join(vals)
        nhStrAll += ')'
        return nhStrAll


class NoteHash(tuple):
    '''
    >>> note1 = note.Note('C4')
    >>> nh = alpha.analysis.hasher.NoteHash((1, 2))
    >>> nh
    (1, 2)
    >>> a, b = nh
    >>> a
    1
    >>> b
    2
    >>> nh.__class__
    <... 'music21.alpha.analysis.hasher.NoteHash'>
    '''
    def __new__(cls, tupEls):
        return super(NoteHash, cls).__new__(cls, tuple(tupEls))


class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def _approximatelyEqual(self, a, b, sig_fig=2):
        '''
        use to look at whether beat lengths are close, within a certain range
        probably can use for other things that are approx. equal
        '''
        pass

    def testBasicHash(self):
        '''
        test for hasher with basic settings: pitch, rounded duration, offset
        with notes, chord, and rest
        '''
        pass

    def testHashChordsAsChordsPrimeFormString(self):
        '''
        test to make sure that hashing works when trying to hash chord as chord
        '''
        pass

    def testHashChordsAsChordsNormalOrder(self):
        pass

    def testHashUnroundedDuration(self):
        pass

    def testHashRoundedDuration(self):
        pass

    def testReferences(self):
        pass

    def testIntervals(self):
        pass


class TestExternal(unittest.TestCase):
    show = True

    # def testBasicHash(self):
    #     # from pprint import pprint as pp
    #     from music21 import corpus
    #     s1 = corpus.parse('schoenberg', 6).parts[0]
    #     h = Hasher()
    #     # h.hashPitch = True
    #     # h.hashDuration = True
    #     # h.hashOffset = True
    #     # h.hashMIDI = False
    #     # h.hashChords = False
    #     # h.hashChordsAsNotes = False
    #     # h.validTypes = [note.Note, note.Rest]
    #     # h.hashMIDI = False  # otherwise, hash string 'C-- instead of 58'
    #     # h.hashOctave = False
    #     # h.hashDuration = True
    #     # h.roundDurationAndOffset = False
    #     # h.roundOffset = False
    #     # h.hashChordsAsNotes = False
    #     # h.hashChordsAsChords = True
    #     # h.hashOctave = True
    #     # h.hashPrimeFormString = True
    #     h.hashIntervalFromLastNote = True
    #     # pp(h.hashStream(s1.recurse()))
    #     # hashes1 = h.hashStream(s1.recurse())
    #     s2 = corpus.parse('schoenberg', 2).parts[0]
    #     # hashes2 = h.hashStream(s2.recurse())
    #     s3 = corpus.parse('bwv66.6').parts[0]
    #     hashes3 = h.hashStream(s3)
    #     # s4 = corpus.parse('bwv66.6').parts[0].transpose('M2')
    #     # s4 = s5.parts[0].transpose('M2')
    #     s4.show()
    #     # pp(s4.recurse())

    #     hashes4 = h.hashStream(s4)
    #     print(hashes3)
    #     print('    ')
    #     print(hashes4)

    #     pp(difflib.SequenceMatcher(a=hashes1, b=hashes2).ratio())
    #     pp(difflib.SequenceMatcher(a=hashes1, b=hashes3).ratio())
    #     pp(difflib.SequenceMatcher(a=hashes2, b=hashes3).ratio())
    #     # pp(difflib.SequenceMatcher(a=hashes3, b=hashes4).ratio())

    # def testFolk(self):
    #     from music21 import corpus
    #     h = Hasher()

    #     s1 = corpus.parse('ryansMammoth/MyLoveIsInAmericaReel.abc').parts[0]
    #     s2 = corpus.parse('ryansMammoth/MyLoveIsFarAwayReel.abc').parts[0]

    #     s2.show()

    #     hashes1 = h.hashStream(s1)
    #     hashes2 = h.hashStream(s2)

    #     print(difflib.SequenceMatcher(a=hashes1, b=hashes2).ratio())

    #     h.hashPitch = False

    #     hashes1 = h.hashStream(s1)
    #     hashes2 = h.hashStream(s2)

    #     print(difflib.SequenceMatcher(a=hashes1, b=hashes2).ratio())

    def testBvSvS(self):
        pass

    def testInterval(self):
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
