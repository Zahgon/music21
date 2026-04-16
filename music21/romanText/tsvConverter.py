# ------------------------------------------------------------------------------
# Name:         romanText/tsvConverter.py
# Purpose:      Converter for the DCMLab's tabular format for representing harmonic analysis.
#
# Authors:      Mark Gotham
#
# Copyright:    Copyright © 2019 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Converter for parsing the tabular representations of harmonic analysis such as the
DCMLab's Annotated Beethoven Corpus (Neuwirth et al. 2018).
'''
from __future__ import annotations

import csv
import fractions
import pathlib
import re
import string
import types
import typing as t
import unittest

from music21 import chord
from music21 import common
from music21 import environment
from music21 import harmony
from music21 import key
from music21 import metadata
from music21 import meter
from music21 import roman
from music21 import spanner
from music21 import stream

environLocal = environment.Environment()

# ------------------------------------------------------------------------------
# V1_HEADERS and V2_HEADERS specify the columns that we process from the DCML
# files, together with the type that the columns should be coerced to (usually
# str)

V1_HEADERS = types.MappingProxyType({
    'chord': str,
    'altchord': str,
    'measure': int,
    'beat': float,
    'totbeat': str,
    'timesig': str,
    'length': float,
    'global_key': str,
    'local_key': str,
    'pedal': str,
    'numeral': str,
    'form': str,
    'figbass': str,
    'changes': str,
    'relativeroot': str,
    'phraseend': str,
})

MN_ONSET_REGEX = re.compile(
    r'(?P<numer>\d+(?:\.\d+)?)/(?P<denom>\d+(?:\.\d+)?)'
)

def _float_or_frac(value):
    # mn_onset in V2 is sometimes notated as a fraction like '1/2'; we need
    # to handle such cases
    pass


V2_HEADERS = types.MappingProxyType({
    'chord': str,
    'mn': int,
    'mn_onset': _float_or_frac,
    'timesig': str,
    'volta': str,
    'globalkey': str,
    'localkey': str,
    'pedal': str,
    'numeral': str,
    'form': str,
    'figbass': str,
    'changes': str,
    'relativeroot': str,
    'phraseend': str,
    'label': str,
})

HEADERS = {1: V1_HEADERS, 2: V2_HEADERS}

# Headers for Digital and Cognitive Musicology Lab Standard v1 as in the ABC
# corpus at
# https://github.com/DCMLab/ABC/tree/2e8a01398f8ad694d3a7af57bed8b14ac57120b7
DCML_V1_HEADERS = (
    'chord',
    'altchord',
    'measure',
    'beat',
    'totbeat',
    'timesig',
    'op',
    'no',
    'mov',
    'length',
    'global_key',
    'local_key',
    'pedal',
    'numeral',
    'form',
    'figbass',
    'changes',
    'relativeroot',
    'phraseend',
)

# Headers for Digital and Cognitive Musicology Lab Standard v2 as in the ABC
# corpus at
# https://github.com/DCMLab/ABC/tree/65c831a559c47180d74e2679fea49aa117fd3dbb
DCML_V2_HEADERS = (
    'mc',
    'mn',
    'mc_onset',
    'mn_onset',
    'timesig',
    'staff',
    'voice',
    'volta',
    'label',
    'globalkey',
    'localkey',
    'pedal',
    'chord',
    'special',
    'numeral',
    'form',
    'figbass',
    'changes',
    'relativeroot',
    'cadence',
    'phraseend',
    'chord_type',
    'globalkey_is_minor',
    'localkey_is_minor',
    'chord_tones',
    'added_tones',
    'root',
    'bass_note',
)

DCML_HEADERS = {1: DCML_V1_HEADERS, 2: DCML_V2_HEADERS}

class TabChordBase():
    '''
    Abstract base class for intermediate representation format for moving
    between tabular data and music21 chords.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.numeral: str = ''
        self.relativeroot: str|None = None
        self.representationType: str|None = None  # Added (not in DCML)
        self.extra: dict[str, str] = {}
        self.dcml_version = -1

        # shared between DCML v1 and v2
        self.chord: str = ''
        self.timesig: str = ''
        self.pedal: str|None = None
        self.form: str|None = None
        self.figbass: str|None = None
        self.changes: str|None = None
        self.phraseend: str|None = None

        # the following attributes are overwritten by properties in TabChordV2
        # because of changed column names in DCML v2
        self.local_key: str = ''
        self.global_key: str = ''
        self.beat: float = 1.0
        self.measure: int = 1

    @property
    def combinedChord(self) -> str:
        '''
        For easier interoperability with the DCML standards, we now use the
        column name 'chord' from the DCML file. But to preserve backwards-
        compatibility, we add this property, which is an alias for 'chord'.

        >>> tabCd = romanText.tsvConverter.TabChord()
        >>> tabCd.chord = 'viio7'
        >>> tabCd.combinedChord
        'viio7'
        >>> tabCd.combinedChord = 'IV+'
        >>> tabCd.chord
        'IV+'
        '''
        pass

    @combinedChord.setter
    def combinedChord(self, value: str):
        pass

    def _changeRepresentation(self) -> None:
        '''
        Converts the representationType of a TabChordBase subclass between the
        music21 and DCML conventions.

        To demonstrate, let's set up a dummy TabChordV2().

        >>> tabCd = romanText.tsvConverter.TabChordV2()
        >>> tabCd.global_key = 'F'
        >>> tabCd.local_key = 'vi'
        >>> tabCd.numeral = 'ii'
        >>> tabCd.chord = 'ii%7(6)'
        >>> tabCd.representationType = 'DCML'

        >>> tabCd.representationType
        'DCML'

        >>> tabCd.chord
        'ii%7(6)'

        >>> tabCd._changeRepresentation()
        >>> tabCd.representationType
        'm21'

        >>> tabCd.chord
        'iiø7[no5][add6]'
        '''
        pass

    def tabToM21(self) -> harmony.Harmony:
        '''
        Creates and returns a music21.roman.RomanNumeral() object
        from a TabChord with all shared attributes.
        NB: call changeRepresentation() first if .representationType is not 'm21'
        but you plan to process it with m21 (e.g. moving it into a stream).

        >>> tabCd = romanText.tsvConverter.TabChord()
        >>> tabCd.numeral = 'vii'
        >>> tabCd.global_key = 'F'
        >>> tabCd.local_key = 'V'
        >>> tabCd.representationType = 'm21'
        >>> m21Ch = tabCd.tabToM21()

        Now we can check it's a music21 RomanNumeral():

        >>> m21Ch.figure
        'vii'
        '''
        pass

    def populateFromRow(
        self,
        row: list[str],
        headIndices: dict[str, tuple[int, type]],
        extraIndices: dict[int, str]
    ) -> None:
        # To implement without calling setattr we would need to repeat lines
        #   similar to the following three lines for every attribute (with
        #   attributes specific to subclasses in their own methods that would
        #   then call __super__()).
        pass

class TabChord(TabChordBase):
    '''
    An intermediate representation format for moving between tabular data in
    DCML v1 and music21 chords.
    '''
    def __init__(self) -> None:
        # self.numeral and self.relativeroot defined in super().__init__()
        super().__init__()
        self.altchord: str|None = None
        self.totbeat: str|None = None
        self.length: fractions.Fraction|float|None = None
        self.dcml_version: int = 1

class TabChordV2(TabChordBase):
    '''
    An intermediate representation format for moving between tabular data in
    DCML v2 and music21 chords.
    '''
    def __init__(self) -> None:
        # self.numeral and self.relativeroot defined in super().__init__()
        super().__init__()
        self.mn: int = 0
        self.mn_onset: float = 0.0
        self.volta: str = ''
        self.globalkey: str = ''
        self.localkey: str = ''
        self.dcml_version: int = 2

    @property
    def beat(self) -> float:
        '''
        'beat' has been removed from DCML v2 in favor of 'mn_onset' and
        'mc_onset'. 'mn_onset' is equivalent to 'beat', except that 'mn_onset'
        is zero-indexed where 'beat' was 1-indexed, and 'mn_onset' is in
        fractions of a whole-note rather than in quarter notes.

        >>> tabCd = romanText.tsvConverter.TabChordV2()
        >>> tabCd.mn_onset = 0.0
        >>> tabCd.beat
        1.0

        >>> tabCd.mn_onset = 0.5
        >>> tabCd.beat
        3.0

        >>> tabCd.beat = 1.5
        >>> tabCd.beat
        1.5
        '''
        pass

    @beat.setter
    def beat(self, beat: float):
        pass

    @property
    def measure(self) -> int:
        '''
        'measure' has been removed from DCML v2 in favor of 'mn' and 'mc'. 'mn'
        is equivalent to 'measure', so this property is provided as an alias.
        '''
        return int(self.mn)

    @measure.setter
    def measure(self, measure: int):
        self.mn = int(measure) if measure is not None else None

    @property
    def local_key(self) -> str:
        '''
        'local_key' has been renamed 'localkey' in DCML v2. This property is
        provided as an alias for 'localkey' so that TabChord and TabChordV2 can
        be used in the same way.
        '''
        pass

    @local_key.setter
    def local_key(self, k: str):
        pass

    @property
    def global_key(self) -> str:
        '''
        'global_key' has been renamed 'globalkey' in DCML v2. This property is
        provided as an alias for 'globalkey' so that TabChord and TabChordV2 can
        be used in the same way.
        '''
        pass

    @global_key.setter
    def global_key(self, k: str):
        pass

# ------------------------------------------------------------------------------


class TsvHandler:
    '''
    Conversion starting with a TSV file.

    First we need to get a score. (Don't worry about this bit.)

    >>> name = 'tsvEg_v1.tsv'
    >>> path = common.getSourceFilePath() / 'romanText' / name
    >>> handler = romanText.tsvConverter.TsvHandler(path)
    >>> handler.tsvToChords()

    These should be TabChords now.

    >>> testTabChord1 = handler.chordList[0]
    >>> testTabChord1.combinedChord
    '.C.I6'

    Good. We can make them into music21 Roman-numerals.

    >>> m21Chord1 = testTabChord1.tabToM21()
    >>> m21Chord1.figure
    'I'

    And for our last trick, we can put the whole collection in a music21 stream.

    >>> out_stream = handler.toM21Stream()
    >>> out_stream.parts[0].measure(1)[roman.RomanNumeral][0].figure
    'I'

    '''
    def __init__(self, tsvFile: str|pathlib.Path, dcml_version: int = 1):
        if dcml_version == 1:
            self.heading_names = HEADERS[1]
            self._tab_chord_cls: type[TabChordBase] = TabChord
        elif dcml_version == 2:
            self.heading_names = HEADERS[2]
            self._tab_chord_cls = TabChordV2
        else:
            raise ValueError(f'dcml_version {dcml_version} is not in (1, 2)')
        self.tsvFileName = tsvFile
        self.chordList: list[TabChordBase] = []
        self.m21stream: stream.Score|None = None
        self._head_indices: dict[str, tuple[int, type|t.Any]] = {}
        self._extra_indices: dict[int, str] = {}
        self.dcml_version = dcml_version
        self.tsvData = self._importTsv()  # converted to private

    def _get_heading_indices(self, header_row: list[str]) -> None:
        '''
        Private method to get column name/column index correspondences.

        Expected column indices (those in HEADERS, which correspond to TabChord
        attributes) are stored in self._head_indices. Others go in
        self._extra_indices.
        '''
        pass

    def _importTsv(self) -> list[list[str]]:
        '''
        Imports TSV file data for further processing.
        '''
        pass

    def _makeTabChord(self, row: list[str]) -> TabChordBase:
        '''
        Makes a TabChord out of a list imported from TSV data
        (a row of the original tabular format -- see TsvHandler.importTsv()).
        '''
        pass

    def tsvToChords(self) -> None:
        '''
        Converts a list of lists (of the type imported by importTsv)
        into TabChords (i.e. a list of TabChords).
        '''
        pass

    def toM21Stream(self) -> stream.Score:
        '''
        Takes a list of TabChords (self.chordList, prepared by .tsvToChords()),
        converts those TabChords in RomanNumerals
        (converting to the music21 representation format as necessary),
        creates a suitable music21 stream (by running .prepStream() using data from the TabChords),
        and populates that stream with the new RomanNumerals.
        '''
        pass

    def prepStream(self) -> stream.Score:
        '''
        Prepares a music21 stream for the harmonic analysis to go into.
        Specifically: creates the score, part, and measure streams,
        as well as some (the available) metadata based on the original TSV data.
        Works like the .template() method,
        except that we don't have a score to base the template on as such.
        '''
        pass


# ------------------------------------------------------------------------------
class M21toTSV:
    '''
    Conversion starting with a music21 stream.
    Exports to tabular data format and (optionally) writes the file.

    >>> bachHarmony = corpus.parse('bach/choraleAnalyses/riemenschneider001.rntxt')
    >>> bachHarmony.parts[0].measure(1)[0].figure
    'I'

    The initialization includes the preparation of a list of lists, so

    >>> initial = romanText.tsvConverter.M21toTSV(bachHarmony, dcml_version=2)
    >>> tsvData = initial.tsvData
    >>> from music21.romanText.tsvConverter import DCML_V2_HEADERS
    >>> tsvData[1][DCML_V2_HEADERS.index('chord')]
    'I'
    '''
    def __init__(self, m21Stream: stream.Score, dcml_version: int = 2):
        self.version = dcml_version
        self.m21Stream = m21Stream
        if dcml_version == 1:
            self.dcml_headers = DCML_HEADERS[1]
        elif dcml_version == 2:
            self.dcml_headers = DCML_HEADERS[2]
        else:
            raise ValueError(f'dcml_version {dcml_version} is not in (1, 2)')
        self.tsvData = self.m21ToTsv()

    def m21ToTsv(self) -> list[list[str]]:
        '''
        Converts a list of music21 chords to a list of lists
        which can then be written to a tsv file with toTsv(), or processed another way.
        '''
        pass

    def _m21ToTsv_v1(self) -> list[list[str]]:
        pass

    def _m21ToTsv_v2(self) -> list[list[str]]:
        pass

    def write(self, filePathAndName: str|pathlib.Path):
        '''
        Writes a list of lists (e.g. from m21ToTsv()) to a tsv file.
        '''
        with open(filePathAndName, 'a', newline='', encoding='utf-8') as csvFile:
            csvOut = csv.writer(csvFile,
                                delimiter='\t',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            csvOut.writerow(self.dcml_headers)

            for thisEntry in self.tsvData:
                csvOut.writerow(thisEntry)

# ------------------------------------------------------------------------------

def getForm(rn: roman.RomanNumeral) -> str:
    '''
    Takes a music21.roman.RomanNumeral object and returns the string indicating
    'form' expected by the DCML standard.

    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('V'))
    ''
    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('viio7'))
    'o'
    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('IVM7'))
    'M'
    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('III+'))
    '+'
    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('IV+M7'))
    '+M'
    >>> romanText.tsvConverter.getForm(roman.RomanNumeral('viiø7'))
    '%'
    '''
    pass


def handleAddedTones(dcmlChord: str) -> str:
    '''
    Converts DCML added-tone syntax to music21.

    >>> romanText.tsvConverter.handleAddedTones('V(64)')
    'Cad64'

    >>> romanText.tsvConverter.handleAddedTones('i(4+2)')
    'i[no3][add4][add2]'

    >>> romanText.tsvConverter.handleAddedTones('Viio7(b4-5)/V')
    'Viio7[no3][no5][addb4]/V'

    When in root position, 7 does not replace 8:

    >>> romanText.tsvConverter.handleAddedTones('vi(#74)')
    'vi[no3][add#7][add4]'

    When not in root position, 7 does replace 8:

    >>> romanText.tsvConverter.handleAddedTones('ii6(11#7b6)')
    'ii6[no8][no5][add11][add#7][addb6]'

    '0' can be used to indicate root-replacement by 7 in a root-position chord.
    We need to change '0' to '7' because music21 changes the 0 to 'o' (i.e.,
    a diminished chord).

    >>> romanText.tsvConverter.handleAddedTones('i(#0)')
    'i[no1][add#7]'
    '''
    pass


def localKeyAsRn(local_key: key.Key, global_key: key.Key) -> str:
    '''
    Takes two music21.key.Key objects and returns the roman numeral for
    `local_key` relative to `global_key`.

    >>> k1 = key.Key('C')
    >>> k2 = key.Key('e')
    >>> romanText.tsvConverter.localKeyAsRn(k1, k2)
    'VI'
    >>> k3 = key.Key('C#')
    >>> romanText.tsvConverter.localKeyAsRn(k3, k2)
    '#VI'
    >>> romanText.tsvConverter.localKeyAsRn(k2, k1)
    'iii'
    '''
    pass

def isMinor(test_key: str) -> bool:
    '''
    Checks whether a key is minor or not simply by upper vs lower case.

    >>> romanText.tsvConverter.isMinor('F')
    False

    >>> romanText.tsvConverter.isMinor('f')
    True
    '''
    pass


def characterSwaps(preString: str, minor: bool = True, direction: str = 'm21-DCML') -> str:
    '''
    Character swap function to coordinate between the two notational versions, for instance
    swapping between '%' and '/o' for the notation of half diminished (for example).

    >>> testStr = 'ii%'
    >>> romanText.tsvConverter.characterSwaps(testStr, minor=False, direction='DCML-m21')
    'iiø'
    '''
    pass


def getLocalKey(local_key: str, global_key: str, convertDCMLToM21: bool = False) -> str:
    '''
    Re-casts comparative local key (e.g. 'V of G major') in its own terms ('D').

    >>> romanText.tsvConverter.getLocalKey('V', 'G')
    'D'

    >>> romanText.tsvConverter.getLocalKey('ii', 'C')
    'd'

    >>> romanText.tsvConverter.getLocalKey('i', 'C')
    'c'

    By default, assumes an m21 input, and operates as such:

    >>> romanText.tsvConverter.getLocalKey('#vii', 'a')
    'g#'

    Set convert=True to convert from DCML to m21 formats. Hence;

    >>> romanText.tsvConverter.getLocalKey('vii', 'a', convertDCMLToM21=True)
    'g'

    '''
    pass


def getSecondaryKey(rn: str, local_key: str) -> str:
    '''
    Separates comparative Roman-numeral for tonicizations like 'V/vi' into the component parts of
    a Roman-numeral (V) and
    a (very) local key (vi)
    and expresses that very local key in relation to the local key also called (DCML column 11).

    While .getLocalKey() work on the figure and key pair:

    >>> romanText.tsvConverter.getLocalKey('vi', 'C')
    'a'

    With .getSecondaryKey(), we're interested in the relative root of a secondaryRomanNumeral:

    >>> romanText.tsvConverter.getSecondaryKey('V/vi', 'C')
    'a'
    '''
    pass

# ------------------------------------------------------------------------------


class Test(unittest.TestCase):

    def testTsvHandler(self):
        pass

    def testM21ToTsv(self):
        pass

    def testIsMinor(self):
        pass

    def testOfCharacter(self):
        pass


    def testGetLocalKey(self):
        pass

    def testGetSecondaryKey(self):
        pass

    def testRepeats(self):
        pass

# ------------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
