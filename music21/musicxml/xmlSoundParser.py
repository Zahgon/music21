# ------------------------------------------------------------------------------
# Name:         musicxml/xmlSoundParser.py
# Purpose:      Translate the <sound> tag to music21
#
# Authors:      Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2016-22 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Functions that convert <sound> tag to the many music21
objects that this tag might represent.

Pulled out because xmlToM21 is getting way too big.
'''
from __future__ import annotations

import typing as t
import xml.etree.ElementTree as ET
import warnings

from music21 import common
from music21 import duration
from music21 import tempo

from music21.musicxml import helpers

if t.TYPE_CHECKING:
    from music21.musicxml.xmlToM21 import MeasureParser


class SoundTagMixin:
    '''
    This Mixin is applied to MeasureParser -- it is moved
    out from there because there is still a lot to write
    here and xmlToM21.py is getting too big.
    '''
    def xmlSound(self, mxSound: ET.Element) -> None:
        '''
        Convert a <sound> tag to one or more relevant objects
        (presently just MetronomeMark),
        and add it or them to the core and staffReference.
        '''
        pass

    def setSound(
        self,
        mxSound: ET.Element,
        mxDir: ET.Element|None,
        staffKey: int,
        totalOffset: float
    ) -> None:
        '''
        Takes a <sound> tag and creates objects from it.
        Presently only handles <sound tempo='x'> events and inserts them as MetronomeMarks.
        If the <sound> tag is a child of a <direction> tag, the direction information
        is used to set the placement of the MetronomeMark.
        '''
        pass


    def setSoundTempo(
        self,
        mxSound: ET.Element,
        mxDir: ET.Element|None,
        staffKey: int,
        totalOffset: float
    ) -> None:
        '''
        Add a metronome mark from the tempo attribute of a <sound> tag.
        '''
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest()  # doctests only
