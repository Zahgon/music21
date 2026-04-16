# ------------------------------------------------------------------------------
# Name:         dynamics.py
# Purpose:      Module for dealing with dynamics changes.
#
# Authors:      Michael Scott Asato Cuthbert
#               Christopher Ariza
#
# Copyright:    Copyright © 2009-2023 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Classes and functions for creating and manipulating dynamic symbols. Rather than
subclasses, the :class:`~music21.dynamics.Dynamic` object is often specialized by parameters.
'''
from __future__ import annotations

import unittest

from music21 import base
from music21 import common
from music21 import environment
from music21 import exceptions21
from music21 import spanner
from music21 import style

environLocal = environment.Environment('dynamics')


shortNames = ['pppppp', 'ppppp', 'pppp', 'ppp', 'pp', 'p', 'mp',
                  'mf', 'f', 'fp', 'sf', 'ff', 'fff', 'ffff', 'fffff', 'ffffff']
longNames = {'ppp': 'pianississimo',
              'pp': 'pianissimo',
              'p': 'piano',
              'mp': 'mezzopiano',
              'mf': 'mezzoforte',
              'f': 'forte',
              'fp': 'fortepiano',
              'sf': 'sforzando',
              'ff': 'fortissimo',
              'fff': 'fortississimo'}

# could be really useful for automatic description of musical events
englishNames = {'ppp': 'extremely soft',
                 'pp': 'very soft',
                 'p': 'soft',
                 'mp': 'moderately soft',
                 'mf': 'moderately loud',
                 'f': 'loud',
                 'ff': 'very loud',
                 'fff': 'extremely loud'}


def dynamicStrFromDecimal(n):
    '''
    Given a decimal from 0 to 1, return a string representing a dynamic
    with 0 being the softest (0.01 = 'ppp') and 1 being the loudest (0.9+ = 'fff')
    0 returns "n" (niente), while ppp and fff are the loudest dynamics used.


    >>> dynamics.dynamicStrFromDecimal(0.25)
    'pp'
    >>> dynamics.dynamicStrFromDecimal(1)
    'fff'
    '''
    pass


# defaults used for volume scalar
dynamicStrToScalar = {
    None: 0.5,  # default value
    'n': 0.0,
    'pppp': 0.1,
    'ppp': 0.15,
    'pp': 0.25,
    'p': 0.35,
    'mp': 0.45,
    'mf': 0.55,
    'f': 0.7,
    'fp': 0.75,
    'sf': 0.85,
    'ff': 0.85,
    'fff': 0.9,
    'ffff': 0.95,
}


# ------------------------------------------------------------------------------
class DynamicException(exceptions21.Music21Exception):
    pass


# ------------------------------------------------------------------------------
class Dynamic(base.Music21Object):
    '''
    Object representation of Dynamics.

    >>> pp1 = dynamics.Dynamic('pp')
    >>> pp1.value
    'pp'
    >>> pp1.longName
    'pianissimo'
    >>> pp1.englishName
    'very soft'

    Dynamics can also be specified on a 0 to 1 scale with 1 being the
    loudest (see dynamicStrFromDecimal() above)

    >>> ppp = dynamics.Dynamic(0.15)  # on 0 to 1 scale
    >>> ppp.value
    'ppp'
    >>> print(f'{ppp.volumeScalar:.2f}')
    0.15

    Note that we got lucky last time because the dynamic 0.15 exactly corresponds
    to what we've considered the default for 'ppp'.  Here we assign 0.98 which
    is close to the 0.9 that is the default for 'fff' -- but the 0.98 will
    be retained in the .volumeScalar

    >>> loud = dynamics.Dynamic(0.98)  # on 0 to 1 scale
    >>> loud.value
    'fff'
    >>> print(f'{loud.volumeScalar:.2f}')
    0.98

    Transferring the .value ('fff') to a new Dynamic object will set the volumeScalar
    back to 0.9

    >>> loud2 = dynamics.Dynamic(loud.value)
    >>> loud2.value
    'fff'
    >>> print(f'{loud2.volumeScalar:.2f}')
    0.90

    Custom dynamics are possible:

    >>> myDyn = dynamics.Dynamic('rfzsfmp')
    >>> myDyn.value
    'rfzsfmp'
    >>> print(myDyn.volumeScalar)
    0.5
    >>> myDyn.volumeScalar = 0.87
    >>> myDyn.volumeScalar
    0.87

    Dynamics can be placed anywhere in a stream.


    >>> s = stream.Stream()
    >>> s.insert(0, note.Note('E-4', type='half'))
    >>> s.insert(2, note.Note('F#5', type='half'))
    >>> s.insert(0, dynamics.Dynamic('pp'))
    >>> s.insert(1, dynamics.Dynamic('mf'))
    >>> s.insert(3, dynamics.Dynamic('fff'))
    >>> #_DOCS_SHOW s.show()

    .. image:: images/dynamics_simple.*
        :width: 344

    '''
    classSortOrder = 10
    _styleClass = style.TextStyle

    _DOC_ORDER = ['longName', 'englishName']
    _DOC_ATTR: dict[str, str] = {
        'longName': r'''
            the name of this dynamic in Italian.


            >>> d = dynamics.Dynamic('pp')
            >>> d.longName
            'pianissimo'
            ''',
        'englishName': r'''
            the name of this dynamic in English.


            >>> d = dynamics.Dynamic('pp')
            >>> d.englishName
            'very soft'
            ''',
        'placement': '''
            Staff placement: 'above', 'below', or None.

            A setting of None implies that the placement will be determined
            by notation software and no particular placement is demanded.

            This is not placed in the `.style` property, since for some dynamics,
            the placement above or below an object has semantic
            meaning and is not purely presentational.  For instance, a dynamic
            placed between two staves in a piano part implies that it applies
            to both hands, while one placed below the lower staff would apply
            only to the left hand.
            ''',
    }
    def __init__(self, value=None, **keywords):
        super().__init__(**keywords)

        # the scalar is used to calculate the final output of a note
        # under this dynamic. if this property is set, it will override
        # use of a default.
        self._volumeScalar = None
        self.longName = None
        self.englishName = None
        self._value = None

        if not isinstance(value, str):
            # assume it is a number, try to convert
            self._volumeScalar = value
            self.value = dynamicStrFromDecimal(value)
        else:
            self.value = value  # will use property

        # for position, as musicxml, all units are in tenths of interline space
        # position is needed as default positions are often incorrect
        self.style.absoluteX = -36
        self.style.absoluteY = -80  # below top line
        # this value provides good 16th note alignment
        self.placement = None

    def _reprInternal(self):
        pass

    def _getValue(self):
        pass

    def _setValue(self, value):
        pass

    value = property(_getValue, _setValue,
                     doc='''
        Get or set the value of this dynamic, which sets the long and
        English names of this Dynamic. The value is a string specification.

        >>> p = dynamics.Dynamic('p')
        >>> p.value
        'p'
        >>> p.englishName
        'soft'
        >>> p.longName
        'piano'

        >>> p.value = 'f'
        >>> p.value
        'f'
        >>> p.englishName
        'loud'
        >>> p.longName
        'forte'
        ''')

    def _getVolumeScalar(self):
        pass

    def _setVolumeScalar(self, value):
        # we can manually set this to be anything, overriding defaults
        pass

    volumeScalar = property(_getVolumeScalar, _setVolumeScalar, doc=r'''
        Get or set the volume scalar for this dynamic. If not explicitly set, a
        default volume scalar will be provided. Any number between 0 and 1 can be
        used to set the volume scalar, overriding the expected behavior.

        As mezzo is at 0.5, the unit interval range is doubled for
        generating final output. The default output is 0.5.


        >>> d = dynamics.Dynamic('mf')
        >>> d.volumeScalar
        0.55...

        >>> d.volumeScalar = 0.1
        >>> d.volumeScalar
        0.1
        >>> d.value
        'mf'


        int(volumeScalar \* 127) gives the MusicXML <sound dynamics="x"/> tag

        >>> xmlOut = musicxml.m21ToXml.GeneralObjectExporter().parse(d).decode('utf-8')
        >>> print(xmlOut)
        <?xml...
        <direction>
            <direction-type>
              <dynamics default-x="-36" default-y="-80">
                <mf />
              </dynamics>
            </direction-type>
            <sound dynamics="12" />
        </direction>...
        ''')


# ------------------------------------------------------------------------------
class DynamicWedge(spanner.Spanner):
    '''
    Common base-class for Crescendo and Diminuendo.
    '''

    def __init__(self, *spannedElements, **keywords):
        super().__init__(*spannedElements, **keywords)

        # from music21 import note
        # self.fillElementTypes = [note.GeneralNote]

        self.type = None  # crescendo or diminuendo
        self.placement = 'below'  # can above or below, after musicxml
        self.spread = 15  # this unit is in tenths
        self.niente = False


class Crescendo(DynamicWedge):
    '''
    A spanner crescendo wedge.

    >>> d = dynamics.Crescendo()
    >>> d.spread
    15
    >>> d.spread = 20
    >>> d.spread
    20
    >>> d.type
    'crescendo'
    '''

    def __init__(self, *spannedElements, **keywords):
        super().__init__(*spannedElements, **keywords)
        self.type = 'crescendo'


class Diminuendo(DynamicWedge):
    '''
    A spanner diminuendo wedge.

    >>> d = dynamics.Diminuendo()
    >>> d.spread = 20
    >>> d.spread
    20
    '''

    def __init__(self, *spannedElements, **keywords):
        super().__init__(*spannedElements, **keywords)
        self.type = 'diminuendo'

# ------------------------------------------------------------------------------


class TestExternal(unittest.TestCase):
    show = True

    def testSingle(self):
        pass

    def testBasic(self):
        '''
        present each dynamic in a single measure
        '''
        pass


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testCopyAndDeepcopy(self):
        pass

    def testBasic(self):
        pass

    def testCorpusDynamicsWedge(self):
        pass

    def testMusicxmlOutput(self):
        # test direct rendering of musicxml
        pass

    def testDynamicsPositionA(self):
        pass
        # s.show()

    def testDynamicsPositionB(self):
        pass
        # s.show()


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER = [Dynamic, dynamicStrFromDecimal]

if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
