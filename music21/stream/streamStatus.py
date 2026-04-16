# -----------------------------------------------------------------------------
# Name:         streamStatus.py
# Purpose:      Functionality for reporting on the notational status of streams
#
# Authors:      Joséphine Wolf Oberholtzer
#
# Copyright:    Copyright © 2013 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
from __future__ import annotations

import unittest

from music21 import environment
from music21.common.misc import defaultDeepcopy
from music21.common.objects import SlottedObjectMixin

environLocal = environment.Environment(__file__)


# -----------------------------------------------------------------------------


class StreamStatus(SlottedObjectMixin):
    '''
    An object that stores the current notation state for the client stream.

    Separates out tasks such as whether notation has been made, etc.

    >>> s = stream.Stream()
    >>> ss = s.streamStatus
    >>> ss
    <music21.stream.streamStatus.StreamStatus object at 0x...>
    >>> s.streamStatus.client is s
    True

    Copying of StreamStatus and surrounding Streams

    >>> import copy
    >>> ss2 = copy.deepcopy(ss)
    >>> ss2.client is None
    True

    >>> s2 = copy.deepcopy(s)
    >>> s2.streamStatus
    <music21.stream.streamStatus.StreamStatus object at 0x...>
    >>> s2.streamStatus is ss
    False
    >>> s2.streamStatus.client is s2
    True
    '''

    # CLASS VARIABLES #

    __slots__ = (
        '_accidentals',
        '_beams',
        '_concertPitch',
        '_dirty',
        '_enharmonics',
        '_measures',
        '_ornaments',
        '_rests',
        '_ties',
        '_tuplets',
        'client',
    )

    # INITIALIZER #

    def __init__(self, client=None):
        self._accidentals = None
        self._beams = None
        self._concertPitch = None
        self._dirty = None
        self._enharmonics = None
        self._measures = None
        self._ornaments = None
        self._rests = None
        self._ties = None
        self._tuplets = None
        self.client = client

    # SPECIAL METHODS #

    def __deepcopy__(self, memo=None):
        '''
        Manage deepcopying by creating a new reference to the same object.
        leaving out the client
        '''
        return defaultDeepcopy(self, memo, ignoreAttributes={'client'})

    # PUBLIC METHODS #

    def haveAccidentalsBeenMade(self):
        '''
        If Accidentals.displayStatus is None for all contained pitches, it as
        assumed that accidentals have not been set for display and/or
        makeAccidentals has not been run. If any Accidental has displayStatus
        other than None, this method returns True, regardless of if
        makeAccidentals has actually been run.
        '''
        for p in self.client.pitches:
            if p.accidental is not None:
                if p.accidental.displayStatus is not None:
                    return True
        return False

    def haveBeamsBeenMade(self):
        '''
        If any Note in this Stream has .beams defined, it as assumed that Beams
        have not been set and/or makeBeams has not been run. If any Beams
        exist, this method returns True, regardless of if makeBeams has
        actually been run.
        '''
        pass

    def haveTupletBracketsBeenMade(self):
        '''
        If any GeneralNote in this Stream is a tuplet, then check to
        see if any of them have a first Tuplet with type besides None
        return True. Otherwise, return False if there is a tuplet. Return None if
        no Tuplets.

        >>> s = stream.Stream()
        >>> s.streamStatus.haveTupletBracketsBeenMade() is None
        True
        >>> s.append(note.Note())
        >>> s.streamStatus.haveTupletBracketsBeenMade() is None
        True
        >>> nTuplet = note.Note(quarterLength=1/3)
        >>> s.append(nTuplet)
        >>> s.streamStatus.haveTupletBracketsBeenMade()
        False
        >>> nTuplet.duration.tuplets[0].type = 'start'
        >>> s.streamStatus.haveTupletBracketsBeenMade()
        True

        '''
        pass

    # PUBLIC PROPERTIES #

    @property
    def accidentals(self):
        pass

    @accidentals.setter
    def accidentals(self, expr):
        pass

    @property
    def beams(self):
        pass

    @beams.setter
    def beams(self, expr):
        pass

    @property
    def tuplets(self):
        pass

    @tuplets.setter
    def tuplets(self, expr):
        pass


# -----------------------------------------------------------------------------


class Test(unittest.TestCase):
    '''
    Note: most Stream tests are found in stream.tests
    '''

    def testHaveBeamsBeenMadeAfterDeepcopy(self):
        pass
        # m.show()


# -----------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
