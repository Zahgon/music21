# ------------------------------------------------------------------------------
# Name:         search.py
# Purpose:      Tools for searching analysis
#
# Authors:      Christopher Ariza
#
# Copyright:    Copyright © 2011 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import unittest

from music21 import chord
from music21 import environment
from music21 import exceptions21
from music21 import note
from music21 import pitch
from music21 import scale
from music21 import stream

environLocal = environment.Environment('alpha.analysis.search')


class SearchModuleException(exceptions21.Music21Exception):
    pass


def findConsecutiveScale(source, targetScale, degreesRequired=5,
                         stepSize=1, comparisonAttribute='name',
                         repeatsAllowed=True, restsAllowed=False):
    '''
    Given a pitch source and a concrete scale, return references to all
    elements found that represent consecutive scale segments in one direction.

    The `targetScale` is a concrete scale instance.

    The `degreesRequired` specifies how many consecutive scale degrees
    are required for grouping. Note that if more are found, they will
    continue to be gathered until a break is found.

    The `stepSize` determines what scale step size is examined

    The `comparisonAttribute` is the Pitch class attribute used
    for all pitch comparisons; this can be used to force enharmonic
    comparison ('name'), pitch space comparison ('nameWithOctave') or
    permit pitch class matching ('pitchClass').

    If `repeatsAllowed` is True, repeated Pitches will be counted as
    part of the consecutive segment.

    If `restsAllowed` is True, rests will not interrupt a consecutive segment.
    '''
    pass


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def testFindConsecutiveScaleA(self):
        pass

    def xtestFindConsecutiveScaleB(self):
        pass

        # s.show()

        # ex = stream.Score()
        # for sub in post:
        #     m = stream.Measure()
        #     for e in sub:
        #         m.append(e)
        #     ex.append(m)
        # ex.show()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
