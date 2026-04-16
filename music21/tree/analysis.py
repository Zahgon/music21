# -----------------------------------------------------------------------------
# Name:         tree/analysis.py
# Purpose:      horizontal analysis tools on timespan trees
#
# Authors:      Joséphine Wolf Oberholtzer
#
# Copyright:    Copyright © 2013-2014 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
'''
Tools for performing voice-leading analysis with trees.
'''
from __future__ import annotations

import collections.abc
import unittest

from music21 import environment
from music21 import exceptions21

environLocal = environment.Environment('tree.analysis')


class HorizontalityException(exceptions21.TreeException):
    pass


# -----------------------------------------------------------------------------


class Horizontality(collections.abc.Sequence):
    r'''
    A horizontality of consecutive PitchedTimespan objects.

    It must be initiated with a list or tuple of Timespan objects.
    '''

    # CLASS VARIABLES #

    __slots__ = (
        'timespans',
    )

    # INITIALIZER #

    def __init__(self, timespans=None):
        if not isinstance(timespans, collections.abc.Sequence):
            raise HorizontalityException(f'timespans must be a sequence, not {timespans!r}')
        if not timespans:
            raise HorizontalityException(
                'there must be at least one timespan in the timespans list')
        if not all(hasattr(x, 'offset') and hasattr(x, 'endTime') for x in timespans):
            raise HorizontalityException('only Timespan objects can be added to a horizontality')
        self.timespans = tuple(timespans)

    # SPECIAL METHODS #

    def __getitem__(self, item):
        return self.timespans[item]

    def __len__(self):
        return len(self.timespans)

    def __repr__(self):
        pitchStrings = []
        for x in self:
            joinedPitches = ', '.join(y.nameWithOctave for y in x.pitches)
            out = f'({joinedPitches},)'
            pitchStrings.append(out)
        pitchStr = ' '.join(pitchStrings)
        return f'<{type(self).__name__}: {pitchStr}>'

    # PROPERTIES #

    @property
    def hasPassingTone(self):
        r'''
        Is true if the Horizontality contains a passing tone; currently defined as three tones in
        one direction.

        (TODO: better check)
        '''
        pass

    @property
    def hasNeighborTone(self):
        r'''
        Is true if the Horizontality contains a neighbor tone.
        '''
        pass

    @property
    def hasNoMotion(self):
        r'''
        Is true if the Horizontality contains no motion (including enharmonic restatements)
        '''
        pass


# -----------------------------------------------------------------------------


class Test(unittest.TestCase):
    pass


# -----------------------------------------------------------------------------


_DOC_ORDER = ()


# -----------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
