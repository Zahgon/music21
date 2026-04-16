# ------------------------------------------------------------------------------
# Name:         noteworthy/binaryTranslate.py
# Purpose:      parses .nwc binary files, compressed and uncompressed
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2006-2013 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Attempts at reading pure .nwc files in music21

First will solve uncompressed .nwc then compressed .nwc

Thanks to Juria90 and the nwc2xml project for solving so many of the documentation problems.
No part of this code is taken from that project, but this project would have been impossible
without his work.

Translates .nwc into .nwctxt and then uses Jordi Guillen's .nwctxt translator to go from
there to music21.

BETA -- does not work for many file elements and is untested.

Demo, showing the extent of problems.  The measure numbers are not set.  Lyrics are missing.
Drum is still poorly handled.
This is very beta.  Much better would be to convert the file into .xml or .nwctxt first.

::

    >>> #_DOCS_SHOW c = converter.parse('/Users/Hildegard/Desktop/test1.nwc')
    >>> p = common.getSourceFilePath() / 'noteworthy' / 'cuthbert_test1_v175.nwc' #_DOCS_HIDE
    >>> c = converter.parse(p) #_DOCS_HIDE
    >>> c.show('text')
    {0.0} <music21.metadata.Metadata object at ...>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.instrument.Violin 'Violin'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.tempo.MetronomeMark animato Quarter=120>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note G>
            {1.0} <music21.note.Note C>
            {2.0} <music21.note.Note C>
            {3.0} <music21.note.Note B>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note C>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.instrument.Violin 'Violin'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note G>
            {1.0} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.5} <music21.note.Note G>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note G>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.instrument.Viola 'Viola'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.clef.AltoClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note D>
            {2.0} <music21.note.Note C#>
            {2.6667} <music21.note.Note D>
            {3.3333} <music21.note.Note E>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note E>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.instrument.Violoncello 'Violoncello'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.clef.BassClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note G>
            {1.0} <music21.note.Note F>
            {2.0} <music21.note.Note E>
            {3.0} <music21.note.Note G>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note C>

    >>> #_DOCS_SHOW c = converter.parse('/Users/Hildegard/Desktop/jingle1.nwc')
    >>> p = common.getSourceFilePath() / 'noteworthy' / 'jingle_v175.nwc' #_DOCS_HIDE
    >>> c = converter.parse(p) #_DOCS_HIDE
    >>> c.show('text')
    {0.0} <music21.metadata.Metadata object at 0x7fe8c0a5ffa0>
    {0.0} <music21.stream.Part 0x7fe8c0920100>
        {0.0} <music21.instrument.Piano 'Piano'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.expressions.TextExpression 'Lively'>
            {0.0} <music21.expressions.TextExpression 'F'>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.tempo.MetronomeMark animato Quarter=120>
            {0.0} <music21.key.KeySignature of 1 flat>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Rest quarter>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Rest quarter>
        {8.0} <music21.stream.Measure 1 offset=8.0>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note C>
            {2.0} <music21.note.Note F>
            {3.5} <music21.note.Note G>
        {12.0} <music21.stream.Measure 2 offset=12.0>
            {0.0} <music21.note.Note A>
            {3.0} <music21.note.Rest quarter>
        {16.0} <music21.stream.Measure 3 offset=16.0>
            {0.0} <music21.expressions.TextExpression 'Bb'>
            {0.0} <music21.note.Note B->
            {1.0} <music21.note.Note B->
            {2.0} <music21.note.Note B->
            {3.5} <music21.note.Note B->
        {20.0} <music21.stream.Measure 4 offset=20.0>
            {0.0} <music21.expressions.TextExpression 'F'>
            {0.0} <music21.note.Note B->
            {1.0} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note A>
            {3.5} <music21.note.Note A>
        {24.0} <music21.stream.Measure 5 offset=24.0>
            {0.0} <music21.expressions.TextExpression 'G'>
            {0.0} <music21.bar.Barline type=regular>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note G>
            {2.0} <music21.note.Note G>
            {3.0} <music21.note.Note A>
        {28.0} <music21.stream.Measure 6 offset=28.0>
            {0.0} <music21.expressions.TextExpression 'C7'>
            {0.0} <music21.note.Note G>
            {2.0} <music21.note.Note C>
            {4.0} <music21.bar.Repeat direction=end>
        {28.0} <music21.spanner.RepeatBracket 1
                <music21.stream.Measure 5 offset=24.0><music21.stream.Measure 6 offset=28.0>>
        {32.0} <music21.stream.Measure 7 offset=32.0>
            {0.0} <music21.expressions.TextExpression 'C7'>
            {0.0} <music21.bar.Barline type=regular>
            {0.0} <music21.note.Note C>
            {1.0} <music21.note.Note C>
            {2.0} <music21.note.Note B->
            {3.0} <music21.note.Note G>
        {36.0} <music21.stream.Measure 8 offset=36.0>
            {0.0} <music21.expressions.TextExpression 'F'>
            {0.0} <music21.note.Note F>
            {3.0} <music21.note.Rest quarter>
    {0.0} <music21.stream.Part 0x7fe8c0921660>
        {0.0} <music21.instrument.Piano 'Piano'>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.clef.BassClef>
            {0.0} <music21.key.KeySignature of 1 flat>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.chord.Chord F3 A3 C4>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.chord.Chord F3 A3 C4>
        {8.0} <music21.stream.Measure 1 offset=8.0>
            {0.0} <music21.chord.Chord F3 A3 C4>
        {12.0} <music21.stream.Measure 2 offset=12.0>
            {0.0} <music21.chord.Chord F3 A3 C4>
            {1.0} <music21.note.Rest quarter>
            {2.0} <music21.chord.Chord F3 A3 C4>
            {3.0} <music21.note.Rest quarter>
        {16.0} <music21.stream.Measure 3 offset=16.0>
            {0.0} <music21.chord.Chord F3 B-3 D4>
        {20.0} <music21.stream.Measure 4 offset=20.0>
            {0.0} <music21.chord.Chord F3 A3 C4>
            {1.0} <music21.note.Rest quarter>
            {2.0} <music21.note.Rest half>
        {24.0} <music21.stream.Measure 5 offset=24.0>
            {0.0} <music21.bar.Barline type=regular>
            {0.0} <music21.chord.Chord G3 B3>
            {2.0} <music21.note.Rest half>
        {28.0} <music21.stream.Measure 6 offset=28.0>
            {0.0} <music21.chord.Chord E3 B-3 C4>
            {4.0} <music21.bar.Repeat direction=end>
        {28.0} <music21.spanner.RepeatBracket 1
                 <music21.stream.Measure 5 offset=24.0><music21.stream.Measure 6 offset=28.0>>
        {32.0} <music21.stream.Measure 7 offset=32.0>
            {0.0} <music21.bar.Barline type=regular>
            {0.0} <music21.chord.Chord E3 B-3 C4>
            {1.0} <music21.note.Rest quarter>
            {2.0} <music21.note.Rest half>
        {36.0} <music21.stream.Measure 8 offset=36.0>
            {0.0} <music21.chord.Chord F3 A3 C4>
            {3.0} <music21.note.Rest quarter>


'''
from __future__ import annotations

import pathlib
import struct
import typing as t
from typing import TypedDict

from music21 import environment
from music21 import exceptions21

from music21.noteworthy import constants

environLocal = environment.Environment('noteworthy.translate')


class FontDict(TypedDict):
    name: bytes
    size: int
    style: int
    charset: int


class NoteworthyBinaryTranslateException(exceptions21.Music21Exception):
    pass


class NWCConverter:
    '''
    A converter object for binary .nwc files.  Do not normally use directly; use converter.parse.

    >>> nwcc = noteworthy.binaryTranslate.NWCConverter()
    >>> nwcc
    <music21.noteworthy.binaryTranslate.NWCConverter object at 0x...>
    >>> nwcc.fileContents
    b''
    >>> nwcc.parsePosition
    0
    >>> nwcc.version  # version of nwc file to be parsed
    200
    >>> nwcc.numberOfStaves
    0
    >>> nwcc.staves
    []
    '''
    def __init__(self, **keywords) -> None:
        self.fileContents: bytes = b''
        self.parsePosition = 0
        self.version = 200
        self.numberOfStaves = 0
        self.titlePageInfo = 0
        self.pageNumberStart = 0
        self.staves: list[NWCStaff] = []
        self.comment: bytes = b''
        self.fonts: list[FontDict] = []
        self.lyricist: bytes = b''
        self.groupVisibility: bytes = b''
        self.allowLayering: int = 1
        self.margins: bytes = b''
        self.notationTypeface: bytes = b'Maestro'
        self.extendLastSystem = None
        self.copyright1: bytes = b''
        self.copyright2: bytes = b''
        self.increaseNoteSpacing = None
        self.author: bytes = b''
        self.title: bytes = b''
        self.measureStart = None
        self.measureNumbers = None
        self.mirrorMargins = None
        self.staffLabels = None
        self.sins = None
        self.user: bytes = b''
        self.staffHeight = 0
        self.currentAlterations: dict[int, str] = {}

    # noinspection SpellCheckingInspection
    def parseFile(self, fp: pathlib.Path|str):
        # noinspection PyShadowingNames
        r'''
        Parse a file (calls .toStream)

        >>> #_DOCS_SHOW fp = '/Users/cuthbert/desktop/cuthbert_test1.nwc'
        >>> fp = str(common.getSourceFilePath()/'noteworthy'/'cuthbert_test1.nwc') #_DOCS_HIDE
        >>> nwcc = noteworthy.binaryTranslate.NWCConverter()
        >>> nwcc.fileContents
        b''
        >>> streamObj = nwcc.parseFile(fp)
        >>> len(nwcc.fileContents)  # binary
        1139
        >>> nwcc.fileContents[0:80]
        b'[NoteWorthy ArtWare]\x00\x00\x00[NoteWorthy
                 Composer]\x00\x01\x02\x02\x00\x00\x00N/A\x000_JldRQMSKq6M5a3FQqK_g\x00\x00\x00'
        >>> streamObj
        <music21.stream.Score ...>
        '''
        with open(fp, 'rb') as f:
            self.fileContents = f.read()
        self.parse()
        return self.toStream()

    def parseString(self, bytesIn: bytes = b''):
        '''
        same as parseFile but takes a string (in Py3, bytes) of binary data instead.
        '''
        self.fileContents = bytesIn
        self.parse()
        return self.toStream()

    def readLEShort(self, updateParsePosition=True):
        '''
        Helper module: read a little-endian short value to an integer

        >>> nwcc = noteworthy.binaryTranslate.NWCConverter()
        >>> nwcc.fileContents = b'\x02\x01\x03\x01'
        >>> nwcc.parsePosition
        0
        >>> nwcc.readLEShort()
        258
        >>> nwcc.parsePosition
        2
        >>> nwcc.readLEShort()
        259
        >>> nwcc.parsePosition
        4

        Or to not update the parsePosition, send False:
        >>> nwcc.parsePosition = 0
        >>> nwcc.readLEShort(False)
        258
        >>> nwcc.readLEShort(False)
        258
        >>> nwcc.parsePosition
        0
        '''
        fc = self.fileContents
        pp = self.parsePosition
        value = struct.unpack('<h', fc[pp:pp + 2])[0]

        if updateParsePosition is True:
            self.parsePosition = pp + 2
        return value

    def byteToInt(self, updateParsePosition=True):
        '''
        changes a byte into an unsigned int
        (i.e., if the byte is > 127 then it's subtracted from 256)
        '''
        fc = self.fileContents
        pp = self.parsePosition
        value = ord(fc[pp:pp + 1])
        # print(value)
        if updateParsePosition is True:
            self.parsePosition = pp + 1
        return value

    def byteToSignedInt(self, updateParsePosition=True):
        '''
        changes a byte into a signed int
        (i.e., if the byte is > 127 then it's subtracted from 256)
        '''
        val = self.byteToInt(updateParsePosition)
        if val > 127:
            val = val - 256
        return val

    def readBytes(self, bytesToRead=1, updateParsePosition=True) -> bytes:
        '''
        reads the next bytesToRead bytes and then (optionally) updates self.parsePosition
        '''
        fc = self.fileContents
        pp = self.parsePosition
        value = fc[pp:pp + bytesToRead]
        if updateParsePosition is True:
            self.parsePosition = pp + bytesToRead
        return value

    def readToNUL(self, updateParsePosition=True) -> bytes:
        r'''
        reads self.fileContents up to, but not including, the next position of \x00.

        updates the parsePosition unless updateParsePosition is False
        '''
        fc = self.fileContents
        try:
            nulPosition = fc.index(0, self.parsePosition)
        except ValueError:
            nulPosition = -1
            # raise NoteworthyBinaryTranslateException(fc[self.parsePosition:],
            #             self.parsePosition)
        # print(self.parsePosition, nulPosition)
        ret: bytes
        if nulPosition == -1:
            ret = fc[self.parsePosition:]
        else:
            ret = fc[self.parsePosition:nulPosition]
        if updateParsePosition is True:
            self.parsePosition = nulPosition + 1
        return ret

    def isValidNWCFile(self, updateParsePosition=True) -> bool:
        storedPP = self.parsePosition
        self.parsePosition = 0
        header1 = self.readToNUL()
        if header1 != b'[NoteWorthy ArtWare]':
            return False
        junk = self.readToNUL()
        junk = self.readToNUL()
        header2 = self.readToNUL()
        if header2 != '[NoteWorthy Composer]':
            return False
        if updateParsePosition is False and storedPP != 0:
            self.parsePosition = storedPP
        return True

    # thanks to Juria90 for figuring these out! and so much more!
    versionFromHex = {0x0114: 120,
                      0x011E: 130,
                      0x0132: 150,
                      0x0137: 155,
                      0x0146: 170,
                      0x014B: 175,
                      0x0200: 200,
                      0x0201: 201,
                      }

    def fileVersion(self, updateParsePosition=True):
        storedPP = self.parsePosition
        self.parsePosition = 45
        fileVersionRaw = self.readLEShort(updateParsePosition)
        if updateParsePosition is False:
            self.parsePosition = storedPP
        if fileVersionRaw in self.versionFromHex:
            self.version = self.versionFromHex[fileVersionRaw]
        else:
            print('No Version Found! Most likely a newer version.  Using 2.01')
            self.version = 201  # most likely a newer version

        return self.version

    def skipBytes(self, numBytes=1):
        self.parsePosition += numBytes

    def advanceToNotNUL(self, nul: bytes = b'\x00'):
        pp = self.parsePosition
        fc = self.fileContents
        # the slice Notation [pp:pp + 1] is needed to avoid Py3 conversion to bytes
        while fc[pp:pp + 1] == nul:
            pp += 1
        self.parsePosition = pp

    def parse(self):
        '''
        the main parse routine called by parseFile() or parseString()
        '''
        if self.fileContents[0:6] == b'[NWZ]\x00':
            import zlib
            fcNew = zlib.decompress(self.fileContents[6:])
            self.fileContents = fcNew

        self.parsePosition = 0
        self.parseHeader()
        self.staves = []
        # print(self.numberOfStaves)

        for i in range(self.numberOfStaves):
            thisStaff = NWCStaff(parent=self)
            thisStaff.parse()
            self.staves.append(thisStaff)

    def parseHeader(self) -> None:
        '''
        Sets a ton of information from the header, and advances the parse position.
        '''
        self.isValidNWCFile()
        self.fileVersion()

        # print(self.version)
        # print(self.parsePosition)
        self.skipBytes(4)  # skipping registered vs. unregistered
        # print(self.parsePosition)
        self.user = self.readToNUL()
        # print(self.user)
        unused_unknown = self.readToNUL()
        # print(unused_unknown)
        self.skipBytes(10)
        self.title = self.readToNUL()
        self.author = self.readToNUL()
        if self.version >= 200:
            self.lyricist = self.readToNUL()
        self.copyright1 = self.readToNUL()
        self.copyright2 = self.readToNUL()
        self.comment = self.readToNUL()

        self.extendLastSystem = self.byteToInt()
        self.increaseNoteSpacing = self.byteToInt()
        unused = self.readBytes(5)
        self.measureNumbers = self.byteToInt()

        unused = self.readBytes(1)
        self.measureStart = self.readLEShort()
        if self.version >= 130:
            self.margins = self.readToNUL()
        else:
            self.margins = b'0.0 0.0 0.0 0.0'

        unused = self.byteToInt()
        unused = self.readBytes(2)
        if self.version >= 130:
            self.groupVisibility = self.readBytes(32)
            self.allowLayering = self.byteToInt()

        if self.version >= 200:
            self.notationTypeface = self.readToNUL()
        self.staffHeight = self.readLEShort()

        if self.version > 170:
            fontCount = 12
        elif self.version > 130:
            fontCount = 10  # some 170 have 12 font info.  See Juria90's code for workaround.
        else:
            fontCount = 0
        self.advanceToNotNUL()  # should not be needed, but some parse errors
        self.skipBytes(2)
        self.fonts = []
        for i in range(fontCount):
            fontDict: FontDict = {
                'name': self.readToNUL(),
                'style': self.byteToInt(),  # regular; 1 = bold; 2 = italic; 3 = bold italic???
                'size': self.byteToInt(),
                'charset': 0,
            }
            unused = self.byteToInt()
            fontDict['charset'] = self.byteToInt()
            if fontDict['name'] == b'':
                fontDict['name'] = b'Times New Roman'
            if fontDict['size'] == 0:
                fontDict['size'] = 12
            self.fonts.append(fontDict)
            # ansi charset is default; but we don't use
        # print(self.fonts)
        self.titlePageInfo = self.byteToInt()

        # index of [None, First Systems, Top Systems, All Systems]
        self.staffLabels = self.byteToInt()
        self.pageNumberStart = self.readLEShort()
        if self.version >= 200:
            self.skipBytes(1)
        self.numberOfStaves = self.byteToInt()
        # print('StaffCount', self.numberOfStaves)
        self.skipBytes(1)

    def dumpToNWCText(self) -> list[str]:
        infos = ''
        if self.title:
            infos += '|SongInfo|Title:' + self.title.decode('latin_1')
        if self.author:
            infos += '|Author:' + self.author.decode('latin_1')
        dumpObjects = [infos]
        for s in self.staves:
            staffDumpObjects = s.dump()
            for sdo in staffDumpObjects:
                dumpObjects.append(sdo)

        return dumpObjects

    def toStream(self):
        from music21.noteworthy import translate
        nwt = translate.NoteworthyTranslator()
        s = nwt.parseList(self.dumpToNWCText())
        return s


class NWCStaff:
    '''
    A NWCStaff is a list of NWCObjects (see :meth:`parseObjects`) associated to metadata
    (see :meth:`parseHeader`). It may also contain some lyrics (see :meth:`parseLyrics`).
    It defines a :meth:`dump` method that return a list of string containing the
    nwctxt-formatted content of each object of the staff.
    '''
    def __init__(self, parent: NWCConverter) -> None:
        self.parent: NWCConverter = parent
        self.lyrics: list[list[bytes]] = []
        self.objects: list[NWCObject] = []
        self.instrumentName: bytes = b''
        self.group = None
        self.layerWithNextStaff = None
        self.transposition = None
        self.partVolume = None
        self.stereoPan = None
        self.color = 0
        self.alignSyllable = None
        self.numberOfLyrics = 0
        self.numberOfObjects = 0
        self.lines = 0
        self.name = None
        self.staffOffset = 0
        self.label: bytes = b''
        self.lyricAlignment = 0

    def parse(self):
        # environLocal.warn([self.parent.parsePosition, self.objects])
        self.parseHeader()
        # environLocal.warn(['header done', self.parent.parsePosition, self.objects])
        self.parseLyrics()
        # environLocal.warn(['lyrics done', self.parent.parsePosition, self.objects])
        self.parseObjects()
        # environLocal.warn([self.parent.parsePosition, self.objects])

    def dump(self) -> list[str]:
        dumpObjects = []

        # default to first midi instrument
        instruName = (self.instrumentName.decode('latin_1')
                      if self.instrumentName
                      else 'Acoustic Grand Piano')
        label = self.label.decode('latin_1') if self.label else instruName

        staffString = '|AddStaff|Name:' + label
        dumpObjects.append(staffString)

        staffInstruString = '|StaffInstrument|Name:' + instruName
        if instruName in constants.MidiInstruments:
            staffInstruString += '|Patch:'
            staffInstruString += str(constants.MidiInstruments.index(instruName))

        staffInstruString += '|Trans:' + str(self.transposition)

        dumpObjects.append(staffInstruString)

        for o in self.objects:
            dm = o.dumpMethod
            d = dm(o)
            if d != '':
                dumpObjects.append(d)

        return dumpObjects

    def parseHeader(self):
        p = self.parent
        # p = NWCConverter()
        self.name = p.readToNUL()
        # print('staff name:', self.name)
        if p.version >= 200:
            self.label = p.readToNUL()
            # print('label:', self.label)
            self.instrumentName = p.readToNUL()
            # print('instrument name:', self.instrumentName)
        self.group = p.readToNUL()
        # print('group: ', self.group)

        if p.version >= 200:
            # self.endingBar = p.byteToInt()
            # self.muted = p.byteToInt()
            # junk = p.byteToInt()
            # self.channel = p.byteToInt()
            # junk = p.byteToInt()
            # self.playbackDevice = p.byteToInt()
            # junk = p.byteToInt()
            # self.patchBank = p.byteToInt()
            # junk = p.byteToInt()
            # self.patchName = p.byteToInt()
            # junk = p.byteToInt()
            # self.defaultVelocity = p.byteToInt()
            # self.style = p.readLEShort()
            # self.verticalSizeUpper = p.readLEShort()
            # self.verticalSizeLower = p.readLEShort()

            p.skipBytes(27)
            self.lines = p.byteToInt()
            # print('lines:', self.lines)
            # print('position:', p.parsePosition)
            self.layerWithNextStaff = p.readLEShort()
            self.transposition = p.readLEShort()
            self.partVolume = p.readLEShort()
            self.stereoPan = p.readLEShort()
            self.color = p.byteToInt()
            self.alignSyllable = p.readLEShort()
            self.numberOfLyrics = p.readLEShort()

        elif p.version == 175:
            p.skipBytes(11)
            instruPatch = p.byteToInt()
            index = instruPatch - 1 if 0 < instruPatch < len(constants.MidiInstruments) else 0
            self.instrumentName = constants.MidiInstruments[index].encode('latin_1')
            p.skipBytes(10)
            self.transposition = p.byteToSignedInt()
            p.skipBytes(6)
            self.alignSyllable = p.readLEShort()
            self.numberOfLyrics = p.readLEShort()

        if self.numberOfLyrics > 0:
            self.lyricAlignment = p.readLEShort()
            self.staffOffset = p.readLEShort()
        else:
            self.lyricAlignment = 0
            self.staffOffset = 0
        # print('Number of lyrics:', self.numberOfLyrics)

    def parseLyrics(self):

        p = self.parent
        lyrics = []

        for i in range(self.numberOfLyrics):
            syllables = []
            try:
                lyricBlockSize = p.readLEShort()
            except struct.error:
                lyricBlockSize = 0
                environLocal.warn('Could not read lyrics. Trying with zero length.')
            # print('lyric block size: ', lyricBlockSize)

            if lyricBlockSize > 0:
                unused_lyricSize = p.readLEShort()
                parsePositionStart = p.parsePosition

                # print('lyric Size: ', lyricSize)
                junk = p.readLEShort()
                continueIt = True
                maxRead = 1000
                while continueIt is True and maxRead > 0:
                    syllable = p.readToNUL()
                    # environLocal.warn([p.parsePosition, syllable, 'syllable'])
                    maxRead -= 1
                    # print('syllable: ', syllable)
                    if syllable == b'':
                        continueIt = False
                    else:
                        syllables.append(syllable)
                p.parsePosition = parsePositionStart + lyricBlockSize
                lyrics.append(syllables)
            # print(syllables)
        # print(lyrics)
        if self.numberOfLyrics > 0:
            junk = p.readLEShort()
        junk_2 = p.readLEShort()
        # print(p.parsePosition)
        self.lyrics = lyrics
        return lyrics

    def parseObjects(self):
        p = self.parent
        objects = []
        self.numberOfObjects = p.readLEShort()
        if p.version > 150:
            self.numberOfObjects -= 2

        # print('Number of objects: ', self.numberOfObjects)
        for i in range(self.numberOfObjects):
            thisObject = NWCObject(staffParent=self, parserParent=p)
            thisObject.parse()
            objects.append(thisObject)
        self.objects = objects
        # print(objects)
        return objects


class NWCObject:
    '''
    NWCObject class is a union that can be used for each type of object contained in a staff.

    An object binary blob starts with its type.
    The parse() method calls the appropriate method depending on the object type.
    Each parsing method should set up the 'dumpMethod' method that return the nwctxt version
    of the object.
    '''
    def __init__(self, staffParent: NWCStaff, parserParent: NWCConverter):
        self.staffParent: NWCStaff = staffParent
        self.parserParent: NWCConverter = parserParent
        self.type = None
        self.placement = 0
        self.pos = 0
        self.style = 0
        self.localRepeatCount = 0
        self.data = 0
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.delay = 0
        self.clefType = 0
        self.offset = 0
        self.visible = 0
        self.duration = 0
        self.durationStr = None
        self.font = 0
        self.sharps = 0
        self.octaveShift = 0
        self.octaveShiftName = None
        self.clefName = None
        self.attribute1 = None
        self.attribute2 = 0
        self.stemLength = 0
        self.dots = 0
        self.bits = 0
        self.denominator = 0
        self.tieInfo = ''
        self.volume = 0
        self.base = 0
        self.velocity = 0
        self.count = 0
        self.name = None
        self.value = 0
        self.flats = 0
        self.keyString = ''
        self.numerator = 0
        self.alterationStr = ''
        self.dotAttribute = None
        self.text = None

        def genericDumpMethod(inner_self) -> str:
            pass

        self.dumpMethod = genericDumpMethod

    def parse(self):
        '''
        determine what type of object I am, and set things accordingly
        '''
        p = self.parserParent
        objectType = p.readLEShort()  # a number -- an index in the objMethods list
        if objectType >= len(self.objMethods) or objectType < 0:
            raise NoteworthyBinaryTranslateException(
                f'Cannot translate objectType: {objectType}; max is {len(self.objMethods)}')
        if p.version >= 170:
            self.visible = p.byteToInt()
        else:
            self.visible = 0

        objectMethod = self.objMethods[objectType]

        objectMethod(self)

    # Start parsing specific objects
    # =================================

    def clef(self):
        '''
        clef info,
        4 bytes
        '''
        p = self.parserParent
        # print('Clef at: ', p.parsePosition)
        self.type = 'Clef'
        self.clefType = p.readLEShort()
        self.octaveShift = p.readLEShort()

        if self.clefType < len(constants.ClefNames):
            self.clefName = constants.ClefNames[self.clefType]
        if self.octaveShift < len(constants.OctaveShiftNames):
            self.octaveShiftName = constants.OctaveShiftNames[self.octaveShift]

        # print('now at: ', p.parsePosition)
        def dump(inner_self):
            build = '|Clef|'
            if inner_self.clefName:
                build += 'Type:' + inner_self.clefName + '|'
            if inner_self.octaveShiftName:
                build += 'OctaveShift:' + inner_self.octaveShiftName + '|'
            return build

        self.dumpMethod = dump

    def keySig(self):
        '''
        Key signature
        10 bytes
        '''
        pass

    def barline(self):
        '''
        Bar line
        2 bytes
        '''
        pass

    def ending(self):
        '''
        Endings
        2 bytes
        '''
        pass

    def instrument(self):
        '''
        Instrument
        8 bytes
        '''
        p = self.parserParent
        self.type = 'Instrument'
        # self.name = p.readToNUL()
        # p.skipBytes(1)
        p.skipBytes(8)  # velocity

    def timeSig(self):
        '''
        Time signature
        6 bytes
        '''
        pass

    def tempo(self):
        '''
        Tempo indications
        5 bytes + null terminated string
        '''
        p = self.parserParent
        self.type = 'Tempo'
        self.pos = p.byteToInt()
        self.placement = p.byteToInt()
        self.value = p.readLEShort()
        self.base = p.byteToInt()
        if p.version < 170:
            junk = p.readLEShort()
        self.text = p.readToNUL()

        def dump(inner_self):
            return f'|Tempo|Tempo:{inner_self.value}'

        self.dumpMethod = dump


    def dynamic(self):
        '''
        dynamics
        7 bytes
        '''
        pass

    def setDurationForObject(self):
        '''
        get duration string for note or rest
        '''

        durStr = constants.DurationValues[self.duration]

        grace = 0
        triplet = False
        if self.type == 'Note':
            self.dotAttribute = self.attribute1[0]
            grace = self.attribute1[1] & 0x20
        else:
            self.dotAttribute = self.data2[3]

        # start 0101, middle 1010, end 1111
        triplet = self.data2[1] & 0x0c

        ordDot = self.dotAttribute

        if (ordDot & 0x01) > 0:
            self.dots = 2
        elif (ordDot & 0x04) > 0:
            self.dots = 1
        else:
            self.dots = 0

        if self.dots == 1:
            durStr += ',Dotted'
        elif self.dots == 2:
            durStr += ',DblDotted'

        if grace > 0:
            durStr += ',Grace'

        if triplet:
            durStr += ',Triplet'

        return durStr

    def note(self):
        '''
        Note
        8 bytes
        '''
        p = self.parserParent
        self.type = 'Note'
        # print('Note at parse position: ', p.parsePosition)
        if p.version < 170:
            print('Cannot yet handle versions before 170')
        else:
            self.duration = p.byteToInt()
            self.data2 = p.readBytes(3)  # ??
            self.attribute1 = p.readBytes(2)
            # print(hex(ord(self.attribute1[0])))
            self.pos = p.byteToSignedInt()
            self.pos = -1 * self.pos
            self.attribute2 = p.byteToInt()
            if p.version <= 170:
                self.data3 = p.readBytes(2)
            else:
                self.data3 = None
            if p.version >= 200:
                if (self.attribute2 & 0x40) != 0:
                    # print('have stemLength info!')
                    self.stemLength = p.byteToInt()
                else:
                    # print('attribute 2:', hex(self.attribute2))
                    self.stemLength = 7
            else:
                self.stemLength = 7
            # if p.version >= 200 and (self.attribute2 & 0x40) != 0:
            #    self.stemLength = p.byteToInt()
            # else:
            #    self.stemLength = 7
        # uh oh!!!
        # p.skipBytes(2)
        # print('Now at: ', p.parsePosition)
        # print('Duration: ', self.duration)
        # print('Data2: ',)
        # for i in self.data2:
        #     print(hex(ord(i)),)
        # print('...')

        self.durationStr = self.setDurationForObject()

        alterationIndex = self.attribute2 & 0x07
        if alterationIndex < len(constants.AlterationTexts):
            self.alterationStr = constants.AlterationTexts[alterationIndex]
        else:
            self.alterationStr = ''


        # in NWC, alteration is not specified for other octave
        if self.alterationStr == '':
            self.alterationStr = self.parserParent.currentAlterations.get(self.pos % 7, '')
        if self.alterationStr is None:
            self.alterationStr = ''
        self.parserParent.currentAlterations[self.pos % 7] = self.alterationStr

        self.tieInfo = ''
        ordAtt1 = self.attribute1[0]
        if (ordAtt1 & 0x10) > 0:
            self.tieInfo = '^'

        def dump(inner_self):
            build = '|Note|Dur:' + inner_self.durationStr + '|'

            build += ('Pos:'
                      + inner_self.alterationStr
                      + str(inner_self.pos)
                      + inner_self.tieInfo + '|')
            return build

        self.dumpMethod = dump

    def rest(self):
        '''
        Rest
        8 bytes
        '''
        pass

    def noteChordMember(self):
        '''
        Chord member
        8 bytes + n Note objects
        '''
        pass



    def pedal(self):
        '''
        Pedal
        3 bytes
        '''
        pass

    def flowDir(self):
        '''
        Flow
        4 bytes
        '''
        pass

    def mpc(self):
        '''
        Midi Instructions
        34 bytes
        '''
        pass

    def tempoVariation(self):
        '''
        Tempo variation
        4 bytes
        '''
        pass

    def dynamicVariation(self):
        '''
        Dynamic variation
        3 bytes
        '''
        pass

    def performance(self):
        '''
        Performance
        3 bytes
        '''
        pass

    def textObj(self):
        '''
        Text
        3 bytes + null terminated string
        '''
        pass


    def restChordMember(self):
        '''
        Rest chord
        10 bytes
        '''
        pass

    # list of methods to parse specific object. The index in the list
    # is the ID of the object to parse.
    # see NWCObject.parse
    objMethods = [clef,              # 0
                  keySig,            # 1
                  barline,           # 2
                  ending,            # 3
                  instrument,        # 4
                  timeSig,           # 5
                  tempo,             # 6
                  dynamic,           # 7
                  note,              # 8
                  rest,              # 9
                  noteChordMember,   # 10
                  pedal,             # 11
                  flowDir,           # 12
                  mpc,               # 13
                  tempoVariation,    # 14
                  dynamicVariation,  # 15
                  performance,       # 16
                  textObj,           # 17
                  restChordMember    # 18
                  ]


if __name__ == '__main__':
    import music21
    music21.mainTest()
    # fp = '/Users/cuthbert/Desktop/395.nwc'
    # fp = 'http://www.cpdl.org/brianrussell/358.nwc'
    # from music21 import converter
    # s = converter.parse(fp)
    # s.show()

    # nwc = NWCConverter()
    # s = nwc.parseFile(fp)
    # s.show()
    # print(nwc.dumpToNWCText())
    # print(nwc.isValidNWCFile())
    # print(nwc.fileVersion())
