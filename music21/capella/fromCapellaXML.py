# ------------------------------------------------------------------------------
# Name:         fromCapellaXML.py
# Purpose:      Module for importing capellaXML (.capx) files.
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
A beta version of a complete .capx to music21 converter.

Currently only handles one <voice> per <staff> and does not deal with
Slurs, Dynamics, Ornamentation, etc.

Does not handle pickup notes, which are defined simply with an early barline
(same as incomplete bars at the end).
'''
from __future__ import annotations

from io import StringIO
import typing as t
import unittest
import xml.etree.ElementTree
import zipfile

from music21 import bar
from music21 import chord
from music21 import clef
from music21 import common
from music21 import duration
from music21 import exceptions21
from music21 import layout
from music21 import key
from music21 import meter
from music21 import note
from music21 import pitch
from music21 import stream
from music21 import tie

# capellaDynamics = {'r': 'ppp',
#                   'q': 'pp',
#                   'p': 'p',
#                   'i': 'mp',
#                   'j': 'mf',
#                   'f': 'f',
#                   'g': 'ff',
#                   'h': 'fff',
#                   's': 'sf',
#                   'z': 'sfz',
#                   '{': 'fz',
#                   '|': 'fp',
#                   }
#
# isSegno1 = lambda char: char == 'y'
# isSegno2 = lambda char: char == '$'
# isSegno  = lambda char: isSegno1(char) or isSegno2(char)
# isCodaLarge = lambda char: char == 'n'
# isCodaSmall = lambda char: char == 'o'
# isCoda = lambda char: isCodaLarge(char) or isCodaSmall(char)
# isPedalStart = lambda char: char == 'a'
# isPedalStop = lambda char: char == 'b'
# isFermataAbove = lambda char: char == 'u'
# isFermataBelow = lambda char: char == 'k'
# isFermata = lambda char: isFermataAbove(char) or isFermataBelow(char)
#
# isUpbow = lambda char: char == 'Z'
# isDownbow = lambda char: char == 'Y'
#
# isTrill = lambda char: char == 't'
# isInvertedMordent = lambda char: char == 'l'
# isMordent = lambda char: char == 'x'
# isTurn = lambda char: char == 'w'
# isOrnament = lambda char: (isTrill(char) or isInvertedMordent(char) or
#        isMordent(char) or isTurn(char))


class CapellaImportException(exceptions21.Music21Exception):
    pass


class CapellaImporter:
    '''
    Object for importing .capx, CapellaXML files into music21 (from which they can be
    converted to musicxml, MIDI, lilypond, etc.)

    Note that Capella stores files closer to their printed versions -- that is to say,
    Systems enclose all the parts for that system and have new clefs etc.
    '''

    def __init__(self):
        self.xmlText = None
        self.zipFilename = None
        self.mainDom = None

    def scoreFromFile(self, filename, systemScore=False):
        '''
        main program: opens a file given by filename and returns a complete
        music21 Score from it.

        If systemScore is True then it skips the step of making Parts from Systems
        and Measures within Parts.
        '''
        self.readCapellaXMLFile(filename)
        self.parseXMLText()
        scoreObj = self.systemScoreFromScore(self.mainDom)
        if systemScore is True:
            return scoreObj
        else:
            partScore = self.partScoreFromSystemScore(scoreObj)
            return partScore

    def readCapellaXMLFile(self, filename):
        '''
        Reads in a .capx file at `filename`, stores it as self.zipFilename, unzips it,
        extracts the score.xml embedded file, sets self.xmlText to the contents.

        Returns self.xmlText
        '''
        self.zipFilename = str(filename)
        with zipfile.ZipFile(str(filename), 'r') as zipFileHandle:
            xmlText = zipFileHandle.read('score.xml')
        self.xmlText = xmlText
        return xmlText

    def parseXMLText(self, xmlText=None):
        '''
        Takes the string (or unicode string) in xmlText and parses it with `xml.etree`.
        Sets `self.mainDom` to the dom object and returns the dom object.
        '''
        if xmlText is None:
            xmlText = self.xmlText
        if not isinstance(xmlText, str):
            xmlText = xmlText.decode('utf-8')
        it = xml.etree.ElementTree.iterparse(StringIO(xmlText))
        for unused, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        self.mainDom = it.root
        return self.mainDom

    def domElementFromText(self, xmlText=None):
        '''
        Utility method, especially for the documentation examples/tests, which uses
        `xml.etree.ElementTree` to parse the string and returns its root object.

        Not used by the main parser

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> funnyTag = ci.domElementFromText(
        ...    '<funny yes="definitely"><greg/>hi<greg><ha>ha</ha>' +
        ...    '<greg type="embedded"/></greg></funny>')
        >>> funnyTag
        <Element 'funny' at 0x...>

        iter searches recursively

        >>> len(list(funnyTag.iter('greg')))
        3

        findall does not:

        >>> len(funnyTag.findall('greg'))
        2
        '''
        pass

    def partScoreFromSystemScore(self, systemScore: stream.Score) -> stream.Score:
        '''
        Take a :class:`~music21.stream.Score` object which is organized
        by Systems and return a new `Score` object which is organized by
        Parts.
        '''
        # this line is redundant currently, since all we have in systemScore
        # are Systems, but later there will be other things.
        systemStream = systemScore.getElementsByClass(layout.System)
        partDictById: dict[str|int, dict[str, t.Any]] = {}
        for thisSystem in systemStream:
            # this line is redundant currently, since all we have in
            # thisSystem are Parts, but later there will be other things.
            systemOffset = systemScore.elementOffset(thisSystem)
            partStream = thisSystem.getElementsByClass(stream.Part)
            for j, thisPart in enumerate(partStream):
                if thisPart.id not in partDictById:
                    newPart = stream.Part()
                    newPart.id = thisPart.id
                    partDictById[thisPart.id] = {'part': newPart, 'number': j}
                else:
                    newPart = partDictById[thisPart.id]['part']
                for el in thisPart:  # no need for recurse
                    newPart.coreInsert(common.opFrac(el.offset + systemOffset), el)
                newPart.coreElementsChanged()
        newScore = stream.Score()
        # ORDERED DICT
        parts: list[stream.Part|None] = [None for i in range(len(partDictById))]
        for partId in partDictById:
            partDict = partDictById[partId]
            parts[partDict['number']] = partDict['part']
        for p in parts:
            # remove redundant Clef and KeySignatures
            if p is None:
                print('part entries do not match partDict!')
                continue
            clefs = p.getElementsByClass(clef.Clef)
            keySignatures = p.getElementsByClass(key.KeySignature)
            lastClef = None
            lastKeySignature = None
            for c in clefs:
                if c == lastClef:
                    p.remove(c)
                else:
                    lastClef = c
            for ks in keySignatures:
                if ks == lastKeySignature:
                    p.remove(ks)
                else:
                    lastKeySignature = ks
            p.makeMeasures(inPlace=True)
            # for m in p.getElementsByClass(stream.Measure):
            #    barLines = m.getElementsByClass(bar.Barline)
            #    for bl in barLines:
            #        blOffset = bl.offset
            #        if blOffset == 0.0:
            #            m.remove(bl)
            #            m.leftBarline = bl
            #        elif blOffset == m.highestTime:
            #            m.remove(bl)
            #            m.rightBarline = bl  # will not yet work for double repeats!

            newScore.coreInsert(0, p)
        newScore.coreElementsChanged()
        return newScore

    def systemScoreFromScore(self, scoreElement, scoreObj=None):
        '''
        returns an :class:`~music21.stream.Score` object from a <score> tag.

        The Score object is not a standard music21 Score object which contains
        parts, then measures, then voices, but instead contains systems which
        optionally contain voices, which contain parts.  No measures have yet
        been created.
        '''
        if scoreObj is None:
            scoreObj = stream.Score()

        systemsList = scoreElement.findall('systems')
        if not systemsList:
            raise CapellaImportException(
                'Cannot find a <systems> tag in the <score> object')
        if len(systemsList) > 1:
            raise CapellaImportException(
                'Found more than one <systems> tag in the <score> object, what does this mean?')
        systemsElement = systemsList[0]

        systemList = systemsElement.findall('system')
        if not systemList:
            raise CapellaImportException(
                'Cannot find any <system> tags in the <systems> tag in the <score> object')

        for systemNumber, thisSystem in enumerate(systemList):
            systemObj = self.systemFromSystem(thisSystem)
            systemObj.systemNumber = systemNumber + 1  # 1 indexed, like musicians think
            scoreObj.coreAppend(systemObj)

        scoreObj.coreElementsChanged()
        return scoreObj

    def systemFromSystem(self, systemElement, systemObj=None):
        r'''
        returns a :class:`~music21.stream.System` object from a <system> tag.
        The System object will contain :class:`~music21.stream.Part` objects
        which will have the notes, etc. contained in it.

        TODO: Handle multiple <voices>
        '''
        if systemObj is None:
            systemObj = layout.System()

        stavesList = systemElement.findall('staves')
        if not stavesList:
            raise CapellaImportException('No <staves> tag found in this <system> element')
        if len(stavesList) > 1:
            raise CapellaImportException(
                'More than one <staves> tag found in this <system> element')
        stavesElement = stavesList[0]
        staffList = stavesElement.findall('staff')
        if not stavesList:
            raise CapellaImportException(
                'No <staff> tag found in the <staves> element for this <system> element')
        for thisStaffElement in staffList:
            # do something with defaultTime
            partId = 'UnknownPart'
            if 'layout' in thisStaffElement.attrib:
                partId = thisStaffElement.attrib['layout']
            partObj = stream.Part()
            partObj.id = partId

            voicesList = thisStaffElement.findall('voices')
            if not voicesList:
                raise CapellaImportException(
                    'No <voices> tag found in the <staff> tag for the <staves> element '
                    + 'for this <system> element')
            voicesElement = voicesList[0]
            voiceList = voicesElement.findall('voice')
            if not voiceList:
                raise CapellaImportException(
                    'No <voice> tag found in the <voices> tag for the <staff> tag for the '
                    + '<staves> element for this <system> element')
            if len(voiceList) == 1:  # single voice staff perfect!
                thisVoiceElement = voiceList[0]
                noteObjectsList = thisVoiceElement.findall('noteObjects')
                if not noteObjectsList:
                    raise CapellaImportException(
                        'No <noteObjects> tag found in the <voice> tag found in the '
                        + '<voices> tag for the <staff> tag for the <staves> element for '
                        + 'this <system> element')
                if len(noteObjectsList) > 1:
                    raise CapellaImportException(
                        'More than one <noteObjects> tag found in the <voice> tag found '
                        + 'in the <voices> tag for the <staff> tag for the <staves> element '
                        + 'for this <system> element')
                thisNoteObject = noteObjectsList[0]
                self.streamFromNoteObjects(thisNoteObject, partObj)
            systemObj.insert(0, partObj)
        return systemObj

    def streamFromNoteObjects(self, noteObjectsElement, streamObj=None):
        # noinspection PyShadowingNames
        r'''
        Converts a <noteObjects> tag into a :class:`~music21.stream.Stream` object
        which is returned.
        A Stream can be given as an optional argument, in which case the objects of this
        Stream are appended to this object.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> noteObjectsString = r"""
        ...           <noteObjects>
        ...                <clefSign clef="G2-"/>
        ...                <keySign fifths="-1"/>
        ...                <chord>
        ...                    <duration base="1/2"/>
        ...                    <lyric>
        ...                        <verse i="0">das,</verse>
        ...                        <verse i="1">scherz,</verse>
        ...                    </lyric>
        ...                    <heads>
        ...                        <head pitch="G4"/>
        ...                    </heads>
        ...                </chord>
        ...                <chord>
        ...                    <duration base="1/2"/>
        ...                    <lyric>
        ...                        <verse i="0">so</verse>
        ...                        <verse i="1">der</verse>
        ...                    </lyric>
        ...                    <heads>
        ...                        <head pitch="A4"/>
        ...                    </heads>
        ...                </chord>
        ...                <barline type="end"/>
        ...            </noteObjects>
        ...            """
        >>> noteObjectsElement = ci.domElementFromText(noteObjectsString)
        >>> streamObj = ci.streamFromNoteObjects(noteObjectsElement)
        >>> streamObj.show('text')
        {0.0} <music21.clef.Treble8vbClef>
        {0.0} <music21.key.KeySignature of 1 flat>
        {0.0} <music21.note.Note G>
        {2.0} <music21.note.Note A>
        {4.0} <music21.bar.Barline type=final>

        >>> streamObj.highestTime
        4.0
        '''
        if streamObj is None:
            s = stream.Stream()
        else:
            s = streamObj

        mapping = {'clefSign': self.clefFromClefSign,
                   'keySign': self.keySignatureFromKeySign,
                   'timeSign': self.timeSignatureFromTimeSign,
                   'rest': self.restFromRest,
                   'chord': self.chordOrNoteFromChord,
                   'barline': self.barlineListFromBarline,
                   }

        for d in noteObjectsElement:
            el = None
            dTag = d.tag
            if dTag not in mapping:
                print(f'Unknown tag type: {dTag}')
            else:
                el = mapping[dTag](d)
                if isinstance(el, list):  # barlineList returns a list
                    for elSub in el:
                        s.coreAppend(elSub)
                elif el is None:
                    pass
                else:
                    s.coreAppend(el)

        s.coreElementsChanged()
        return s

    def restFromRest(self, restElement):
        # noinspection PyShadowingNames
        '''
        Returns a :class:`~music21.rest.Rest` object from a <rest> tag.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> restElement = ci.domElementFromText('<rest><duration base="1/2"/></rest>')
        >>> r = ci.restFromRest(restElement)
        >>> r
        <music21.note.Rest half>
        >>> r.duration.type
        'half'
        '''
        pass

    def chordOrNoteFromChord(self, chordElement):
        # noinspection PyShadowingNames
        '''
        returns a :class:`~music21.note.Note` or :class:`~music21.chord.Chord`
        from a chordElement -- a `Note`
        is returned if the <chord> has one <head> element, a `Chord` is
        returned if there are multiple <head> elements.


        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> chordElement = ci.domElementFromText(
        ...     '<chord><duration base="1/1"/><heads><head pitch="G4"/></heads></chord>')
        >>> n = ci.chordOrNoteFromChord(chordElement)
        >>> n
        <music21.note.Note G>
        >>> n.duration
        <music21.duration.Duration 4.0>

        This one is an actual chord

        >>> chordElement = ci.domElementFromText(
        ...        '<chord><duration base="1/8"/>' +
        ...        '<heads><head pitch="G4"/><head pitch="A5"/></heads></chord>')
        >>> c = ci.chordOrNoteFromChord(chordElement)
        >>> c
        <music21.chord.Chord G3 A4>
        >>> c.duration
        <music21.duration.Duration 0.5>
        '''
        pass

    def notesFromHeads(self, headsElement):
        # noinspection PyShadowingNames
        '''
        returns a list of :class:`~music21.note.Note` elements for each <head> in <heads>

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> headsElement = ci.domElementFromText(
        ...    '<heads><head pitch="B7"><alter step="-1"/></head><head pitch="C2"/></heads>')
        >>> ci.notesFromHeads(headsElement)
        [<music21.note.Note B->, <music21.note.Note C>]
        '''
        pass

    def noteFromHead(self, headElement):
        # noinspection PyShadowingNames
        '''
        return a :class:`~music21.note.Note` object from a <head> element.  This will become
        part of Chord._notes if there are multiple, but in any case, it needs to be a Note
        not a Pitch for now, because it could have Tie information

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> headElement = ci.domElementFromText(
        ...      '<head pitch="B7"><alter step="-1"/><tie end="true"/></head>')
        >>> n = ci.noteFromHead(headElement)
        >>> n
        <music21.note.Note B->
        >>> n.octave  # capella octaves are one higher than written
        6
        >>> n.tie
        <music21.tie.Tie stop>
        '''
        pass

    def accidentalFromAlter(self, alterElement):
        '''
        return a :class:`~music21.pitch.Accidental` object from an <alter> tag.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> alter = ci.domElementFromText('<alter step="-1"/>')
        >>> ci.accidentalFromAlter(alter)
        <music21.pitch.Accidental flat>

        The only known display type is "suppress"

        >>> alter = ci.domElementFromText('<alter step="2" display="suppress"/>')
        >>> accidentalObject = ci.accidentalFromAlter(alter)
        >>> accidentalObject
        <music21.pitch.Accidental double-sharp>
        >>> accidentalObject.displayType
        'never'
        '''
        pass

    def tieFromTie(self, tieElement):
        '''
        returns a :class:`~music21.tie.Tie` element from a <tie> tag

        if begin == 'true' then Tie.type = start


        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> tieEl = ci.domElementFromText('<tie begin="true"/>')
        >>> ci.tieFromTie(tieEl)
        <music21.tie.Tie start>

        if end == 'true' then Tie.type = stop

        >>> tieEl = ci.domElementFromText('<tie end="true"/>')
        >>> ci.tieFromTie(tieEl)
        <music21.tie.Tie stop>

        if begin == 'true' and end == 'true' then Tie.type = continue (is this right???)

        >>> tieEl = ci.domElementFromText('<tie begin="true" end="true"/>')
        >>> ci.tieFromTie(tieEl)
        <music21.tie.Tie continue>
        '''
        pass

    def lyricListFromLyric(self, lyricElement):
        '''
        returns a list of :class:`~music21.note.Lyric` objects from a <lyric> tag


        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> lyricEl = ci.domElementFromText(
        ...      '<lyric><verse i="0" hyphen="true">di</verse>' +
        ...      '<verse i="1">man,</verse><verse i="2">frau,</verse></lyric>')
        >>> ci.lyricListFromLyric(lyricEl)
        [<music21.note.Lyric number=1 syllabic=begin text='di'>,
         <music21.note.Lyric number=2 syllabic=single text='man,'>,
         <music21.note.Lyric number=3 syllabic=single text='frau,'>]
        '''
        pass

    def lyricFromVerse(self, verse):
        # noinspection PyShadowingNames
        '''
        returns a :class:`~music21.note.Lyric` object from a <verse> tag

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> verse = ci.domElementFromText('<verse i="0" hyphen="true">di&quot;</verse>')
        >>> ci.lyricFromVerse(verse)
        <music21.note.Lyric number=1 syllabic=begin text='di"'>

        Does not yet support 'align' attribute

        if the text is empty, returns None
        '''
        pass

        # i = number - 1
        # align
        # hyphen = true

    clefMapping = {'treble': clef.TrebleClef,
                   'bass': clef.BassClef,
                   'alto': clef.AltoClef,
                   'tenor': clef.TenorClef,
                   'G2-': clef.Treble8vbClef,
                   }

    def clefFromClefSign(self, clefSign):
        # noinspection PyShadowingNames
        '''
        returns a :class:`~music21.clef.Clef` object or subclass from a <clefSign> tag.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> clefSign = ci.domElementFromText('<clefSign clef="treble"/>')
        >>> ci.clefFromClefSign(clefSign)
        <music21.clef.TrebleClef>

        >>> clefSign = ci.domElementFromText('<clefSign clef="G2-"/>')
        >>> ci.clefFromClefSign(clefSign)
        <music21.clef.Treble8vbClef>

        >>> clefSign = ci.domElementFromText('<clefSign clef="F1+"/>')
        >>> clefObject = ci.clefFromClefSign(clefSign)
        >>> clefObject
        <music21.clef.FClef>
        >>> clefObject.sign
        'F'
        >>> clefObject.line
        1
        >>> clefObject.octaveChange
        1
        '''
        pass

    def keySignatureFromKeySign(self, keySign):
        # noinspection PyShadowingNames
        '''
        Returns a :class:`~music21.key.KeySignature` object from a keySign tag.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> keySign = ci.domElementFromText('<keySign fifths="-1"/>')
        >>> ci.keySignatureFromKeySign(keySign)
        <music21.key.KeySignature of 1 flat>
        '''
        pass

    def timeSignatureFromTimeSign(self, timeSign):
        # noinspection PyShadowingNames
        '''
        Returns a :class:`~music21.meter.TimeSignature` object from a timeSign tag.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> timeSign = ci.domElementFromText('<timeSign time="4/4"/>')
        >>> ci.timeSignatureFromTimeSign(timeSign)
        <music21.meter.TimeSignature 4/4>

        >>> timeSign = ci.domElementFromText('<timeSign time="infinite"/>')
        >>> ci.timeSignatureFromTimeSign(timeSign) is None
        True
        '''
        pass

    def durationFromDuration(self, durationElement):
        '''
        Return a music21.duration.Duration element from an XML Element representing
        a duration.

        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> durationTag = ci.domElementFromText('<duration base="1/32" dots="1"/>')
        >>> durationObj = ci.durationFromDuration(durationTag)
        >>> durationObj
        <music21.duration.Duration 0.1875>
        >>> durationObj.type
        '32nd'
        >>> durationObj.dots
        1

        Here with Tuplets

        >>> durationTag2 = ci.domElementFromText(
        ...      '<duration base="1/4"><tuplet count="3"/></duration>')
        >>> d2 = ci.durationFromDuration(durationTag2)
        >>> d2
        <music21.duration.Duration 2/3>
        >>> d2.type
        'quarter'
        >>> d2.tuplets
        (<music21.duration.Tuplet 3/2>,)


        Does not handle noDuration='true', display, churchStyle on rest durations
        '''
        pass

    def tupletFromTuplet(self, tupletElement):
        '''
        Returns a :class:`~music21.duration.Tuplet` object from a <tuplet> tag.


        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> tupletTag = ci.domElementFromText('<tuplet count="3"/>')
        >>> ci.tupletFromTuplet(tupletTag)
        <music21.duration.Tuplet 3/2>

        does not handle 'tripartite' = True
        '''
        pass

    barlineMap = {'single': 'normal',
                  'double': 'double',
                  'end': 'final',
                  'repEnd': 'end',
                  'repBegin': 'start',
                  'repEndBegin': 'end-start',
                  }

    def barlineListFromBarline(self, barlineElement):
        '''
        Indication that the barline at this point should be something other than normal.

        Capella does not indicate measure breaks or barline breaks normally, so the only barlines
        that are indicated are unusual ones.

        Returns a LIST of :class:`~music21.bar.Barline` or :class:`~music21.bar.Repeat` objects
        because the `repEndBegin` type requires two `bar.Repeat` objects to encode in `music21`.


        >>> ci = capella.fromCapellaXML.CapellaImporter()
        >>> barlineTag = ci.domElementFromText('<barline type="end"/>')
        >>> ci.barlineListFromBarline(barlineTag)
        [<music21.bar.Barline type=final>]

        >>> repeatTag = ci.domElementFromText('<barline type="repEndBegin"/>')
        >>> ci.barlineListFromBarline(repeatTag)
        [<music21.bar.Repeat direction=end>, <music21.bar.Repeat direction=start>]

        '''
        pass

    def slurFromDrawObjSlur(self, drawObj):
        '''
        not implemented
        '''
        pass


class Test(unittest.TestCase):
    def testComplete(self):
        pass

class TestExternal(unittest.TestCase):
    show = True

    def testComplete(self):
        pass

    def xtestImportSorgen(self):
        pass
        # ci.walkNodes()
        # print(ci.xmlText)


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , TestExternal)
