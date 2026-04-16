# ------------------------------------------------------------------------------
# Name:         metrical.py
# Purpose:      Tools for metrical analysis
#
# Authors:      Christopher Ariza
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2009-2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Various tools and utilities for doing metrical or rhythmic analysis.

See the chapter :ref:`User's Guide Chapter 14: Time Signatures <usersGuide_14_timeSignatures>`
for more information on defining
metrical structures in music21.
'''
from __future__ import annotations

import copy
import unittest

from music21 import environment
from music21 import stream

environLocal = environment.Environment('analysis.metrical')


def labelBeatDepth(streamIn):
    # noinspection PyShadowingNames
    r'''
    Modify a Stream in place by annotating metrical analysis symbols.

    This assumes that the Stream is already partitioned into Measures.

    >>> s = stream.Stream()
    >>> ts = meter.TimeSignature('4/4')
    >>> s.insert(0, ts)
    >>> n = note.Note(type='eighth')
    >>> s.repeatAppend(n, 8)
    >>> s.makeMeasures(inPlace=True)
    >>> post = analysis.metrical.labelBeatDepth(s)
    >>> sOut = []
    >>> for n in s.flatten().notes:
    ...     stars = "".join([l.text for l in n.lyrics])
    ...     sOut.append(f'{n.beatStr:8s} {stars}')
    >>> print("\n".join(sOut))
    1        ****
    1 1/2    *
    2        **
    2 1/2    *
    3        ***
    3 1/2    *
    4        **
    4 1/2    *
    '''
    pass

def thomassenMelodicAccent(streamIn: stream.Stream):
    # noinspection PyShadowingNames
    '''
    Adds an attribute, 'melodicAccent' to each note's `.editorial`
    within a :class:`~music21.stream.Stream` object
    according to the method postulated in Joseph M. Thomassen, "Melodic accent: Experiments and
    a tentative model," ''Journal of the Acoustical Society of America'', Vol. 71, No. 6 (1982) pp.
    1598-1605; with, Erratum, ''Journal of the Acoustical Society of America'', Vol. 73,
    No. 1 (1983) p.373, and in David Huron and Matthew Royal,
    "What is melodic accent? Converging evidence
    from musical practice." ''Music Perception'', Vol. 13, No. 4 (1996) pp. 489-516.

    Similar to the humdrum melac_ tool.

    .. _melac: https://www.humdrum.org/Humdrum/commands/melac.html

    Takes in a Stream of :class:`~music21.note.Note` objects (use `.flatten().notes` to get it, or
    better `.flatten().getElementsByClass(note.Note)` to filter out chords)
    and adds the attribute to
    each.  Note that Huron and Royal's work suggests that melodic accent has a correlation
    with metrical accent only for solo works/passages; even treble passages do not have a
    strong correlation. (Gregorian chants were found to have a strong ''negative'' correlation
    between melodic accent and syllable onsets)

    Following Huron's lead, we assign a `melodicAccent` of 1.0 to the first note in a piece
    and take the accent marker of the first interval alone to the second note and
    of the last interval alone to be the accent of the last note.

    Example from Thomassen, figure 5:

    >>> s = converter.parse('tinynotation: 7/4 c4 c c d e d d')
    >>> analysis.metrical.thomassenMelodicAccent(s.flatten().notes)
    >>> for n in s.flatten().notes:
    ...    (n.pitch.nameWithOctave, n.editorial.melodicAccent)
    ('C4', 1.0)
    ('C4', 0.0)
    ('C4', 0.0)
    ('D4', 0.33)
    ('E4', 0.5561)
    ('D4', 0.17)
    ('D4', 0.0)

    '''
    pass




# ------------------------------------------------------------------------------
class TestExternal(unittest.TestCase):
    show = True

    def testSingle(self):
        '''
        Need to test direct meter creation w/o stream
        '''
        pass


class Test(unittest.TestCase):
    pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER = [labelBeatDepth]

if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , TestExternal)


