# ------------------------------------------------------------------------------
# Name:         examples.py
# Purpose:      Figured bass test cases
# Authors:      Jose Cabal-Ugaz
#
# Copyright:    Copyright © 2010-2011 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Each of the example methods in this module provides a figured bass line as a
:class:`~music21.figuredBass.realizer.FiguredBassLine` instance.
These can be realized by calling
:meth:`~music21.figuredBass.realizer.FiguredBassLine.realize`, which takes in an
optional :class:`~music21.figuredBass.rules.Rules` object.
The result is a :class:`~music21.figuredBass.realizer.Realization`
object which can generate realizations as instances of
:class:`~music21.stream.Score`. These realizations can then be displayed
in external software such as MuseScore or Finale by
calling :meth:`~music21.base.Music21Object.show`.
'''
from __future__ import annotations

import copy
import unittest

from music21.figuredBass import realizer
from music21.figuredBass import rules

# ------------------------------------------------------------------------------


def exampleA():
    '''
    This example was a homework assignment for 21M.302: Harmony & Counterpoint II
    at MIT in the fall of 2010, taught by Charles Shadle of the MIT Music Program.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.exampleA()
    >>> #_DOCS_SHOW fbLine.generateBassLine().show()

    .. image:: images/figuredBass/fbExamples_bassLineA.*
            :width: 700

    The following is a realization of fbLine in four parts using the default rules set.
    The soprano part is limited to stepwise motion, and the alto and tenor parts are
    limited to motions within a perfect octave.


    >>> from music21.figuredBass import rules
    >>> fbRules = rules.Rules()
    >>> fbRules.partMovementLimits = [(1, 2), (2, 12), (3, 12)]
    >>> fbRealization1 = fbLine.realize(fbRules)
    >>> fbRealization1.getNumSolutions()
    360
    >>> #_DOCS_SHOW fbRealization1.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol1A.*
            :width: 700


    Now, the restriction on upper parts being within a perfect octave of each other is
    removed, and fbLine is realized again.


    >>> fbRules.upperPartsMaxSemitoneSeparation = None
    >>> fbRealization2 = fbLine.realize(fbRules)
    >>> fbRealization2.keyboardStyleOutput = False
    >>> fbRealization2.getNumSolutions()
    3564440
    >>> #_DOCS_SHOW fbRealization2.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol2A.*
        :width: 700
    '''
    pass


def exampleD():
    '''
    This example was a homework assignment for 21M.302: Harmony & Counterpoint II
    at MIT in the fall of 2010, taught by Charles Shadle of the MIT Music Program.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.exampleD()
    >>> #_DOCS_SHOW fbLine.generateBassLine().show()

    .. image:: images/figuredBass/fbExamples_bassLineD.*
            :width: 700

    The following is a realization of fbLine in four parts using the default rules set.
    The soprano part is limited to stepwise motion, and the alto and tenor parts are
    limited to motions within a perfect octave.

    >>> from music21.figuredBass import rules
    >>> fbRules = rules.Rules()
    >>> fbRules.partMovementLimits = [(1, 2), (2, 12), (3, 12)]
    >>> fbRealization1 = fbLine.realize(fbRules)
    >>> fbRealization1.getNumSolutions()
    1560
    >>> #_DOCS_SHOW fbRealization1.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol1D.*
            :width: 700

    Now, the restriction on voice overlap is lifted, which is common in keyboard-style
    figured bass, and fbLine is realized again. Voice overlap can be seen in the fourth
    measure.

    >>> fbRules.forbidVoiceOverlap = False
    >>> fbRealization2 = fbLine.realize(fbRules)
    >>> fbRealization2.getNumSolutions()
    109006
    >>> #_DOCS_SHOW fbRealization2.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol2D.*
            :width: 700

    Now, the restriction on voice overlap is reset, but the restriction on the upper parts
    being within a perfect octave of each other is removed. fbLine is realized again.

    >>> fbRules.forbidVoiceOverlap = True
    >>> fbRules.upperPartsMaxSemitoneSeparation = None
    >>> fbRealization3 = fbLine.realize(fbRules)
    >>> fbRealization3.getNumSolutions()
    27445876
    >>> fbRealization3.keyboardStyleOutput = False
    >>> #_DOCS_SHOW fbRealization3.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol3D.*
            :width: 700
    '''
    pass


def exampleB():
    '''
    This example was retrieved from page 114 of *The Music Theory Handbook* by Marjorie Merryman.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.exampleB()
    >>> #_DOCS_SHOW fbLine.generateBassLine().show()

    .. image:: images/figuredBass/fbExamples_bassLineB.*
        :width: 700

    First, fbLine is realized with the default rules set.


    >>> fbRealization1 = fbLine.realize()
    >>> fbRealization1.getNumSolutions()
    422
    >>> #_DOCS_SHOW fbRealization1.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol1B.*
        :width: 700


    Now, a Rules object is created, and the restriction that the chords
    need to be complete is lifted. fbLine is realized once again.


    >>> from music21.figuredBass import rules
    >>> fbRules = rules.Rules()
    >>> fbRules.forbidIncompletePossibilities = False
    >>> fbRealization2 = fbLine.realize(fbRules)
    >>> fbRealization2.getNumSolutions()
    159373
    >>> #_DOCS_SHOW fbRealization2.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol2B.*
        :width: 700
    '''
    pass


def exampleC():
    '''
    This example was retrieved from page 114 of *The Music Theory Handbook* by Marjorie Merryman.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.exampleC()
    >>> #_DOCS_SHOW fbLine.generateBassLine().show()

    .. image:: images/figuredBass/fbExamples_bassLineC.*
        :width: 700

    First, fbLine is realized with the default rules set.

    >>> fbRealization1 = fbLine.realize()
    >>> fbRealization1.getNumSolutions()
    833
    >>> #_DOCS_SHOW fbRealization1.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol1C.*
        :width: 700


    Now, parallel fifths are allowed in realizations. The image below
    shows one of them. There is a parallel fifth between the bass and
    alto parts going from the half-diminished 6,5 (B,F#) to the dominant
    seventh (C#,G#) in the second measure.

    >>> from music21.figuredBass import rules
    >>> fbRules = rules.Rules()
    >>> fbRules.forbidParallelFifths = False
    >>> fbRealization2 = fbLine.realize(fbRules)
    >>> fbRealization2.getNumSolutions()
    2427
    >>> #_DOCS_SHOW fbRealization2.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_sol2C.*
        :width: 700
    '''
    pass


def V43ResolutionExample():
    '''
    The dominant 4,3 can resolve to either the tonic 5,3 or tonic 6,3. The proper resolution
    is dependent on the bass note of the tonic, and is determined in context, as shown in the
    following figured bass realization.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.V43ResolutionExample()
    >>> fbRealization = fbLine.realize()
    >>> #_DOCS_SHOW fbRealization.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_V43.*
        :width: 350
    '''
    pass


def viio65ResolutionExample():
    '''
    For a fully diminished seventh chord resolving to the tonic, the resolution chord
    can contain either a doubled third (standard resolution) or a doubled tonic (alternate
    resolution), depending on whether the third of the diminished chord rises or falls.
    The user can control this in a Rules object by modifying
    :attr:`~music21.figuredBass.rules.Rules.doubledRootInDim7`.
    However, when resolving a diminished 6,5, the third is found in the bass and the
    proper resolution is determined in context, regardless of user preference.


    The following shows both cases involving a diminished 6,5. The resolution of the
    first diminished chord has a doubled D, while that of the second has a doubled F#.
    Notice that the resolution of the first involves a diminished fifth (E, Bb) going
    to a perfect fifth (D, A).

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.viio65ResolutionExample()
    >>> fbRealization = fbLine.realize()
    >>> #_DOCS_SHOW fbRealization.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_vii65.*
        :width: 700
    '''
    pass


def augmentedSixthResolutionExample():
    '''
    This example was retrieved from page 61 of *The Music Theory Handbook* by Marjorie Merryman.

    Italian (8,#6,3), French (#6,4,3), German (#6,5,3), and Swiss (#6,#4,3)
    augmented sixth resolutions to
    either the major dominant or the major/minor tonic 6,4 are supported.
    The first four bars show the
    resolutions to the dominant in the order above, while the last bar
    shows the German augmented sixth
    resolving to the tonic.

    >>> from music21.figuredBass import examples
    >>> fbLine = examples.augmentedSixthResolutionExample()
    >>> fbRealization = fbLine.realize()
    >>> #_DOCS_SHOW fbRealization.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_a6.*
        :width: 700
    '''
    pass


def italianA6ResolutionExample():
    '''
    The Italian augmented sixth chord (It+6) is the only
    augmented sixth chord to consist of only three
    pitch names, and when represented in four parts, the
    tonic is doubled. The tonic can resolve up, down or
    stay the same, and in four parts, the two tonics always
    resolve differently, resulting in two equally
    acceptable resolutions. An alternate approach to resolving
    the It+6 chord was taken, such that an It+6
    chord could map internally to two different resolutions.
    Every other special resolution in fbRealizer
    consists of a 1:1 mapping of special chords to resolutions.


    Here, the It+6 chord is resolving to the dominant, minor tonic,
    and major tonic, respectively. In the
    dominant resolution shown, the tonics (D) are resolving inward,
    but they can resolve outward as well. In
    the minor tonic resolution, the higher tonic is resolving up to F,
    and the lower tonic remains the same.
    In the major tonic resolution, the higher tonic remains the same,
    while the lower tonic resolves up to the F#.

    >>> from music21.figuredBass import examples
    >>> from music21.figuredBass import rules
    >>> fbLine = examples.italianA6ResolutionExample()
    >>> fbRules = rules.Rules()
    >>> fbRules.upperPartsMaxSemitoneSeparation = None
    >>> fbRules.partMovementLimits.append([1, 4])
    >>> fbRealization = fbLine.realize(fbRules)
    >>> fbRealization.keyboardStyleOutput = False
    >>> #_DOCS_SHOW fbRealization.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_it+6.*
        :width: 700
    '''
    pass


def twelveBarBlues():
    '''
    This is a progression in Bb major based on the twelve bar blues. The progression used is:

        I  |  IV  |  I  |  I7
        IV |  IV  |  I  |  I7
        V7 |  IV6 |  I  |  I

    >>> from music21.figuredBass import examples
    >>> from music21.figuredBass import rules
    >>> bluesLine = examples.twelveBarBlues()
    >>> #_DOCS_SHOW bluesLine.generateBassLine().show()

    .. image:: images/figuredBass/fbExamples_bluesBassLine.*
        :width: 700

    >>> fbRules = rules.Rules()
    >>> fbRules.partMovementLimits = [(1, 4), (2, 12), (3, 12)]
    >>> fbRules.forbidVoiceOverlap = False
    >>> blRealization = bluesLine.realize(fbRules)
    >>> blRealization.getNumSolutions()
    2224978
    >>> #_DOCS_SHOW blRealization.generateRandomRealization().show()

    .. image:: images/figuredBass/fbExamples_twelveBarBlues.*
        :width: 700
    '''
    pass

# -----------------------------------------------------------------
# Functions that generate Boogie/Blues vamps.


def generateBoogieVamp(blRealization=None, numRepeats=5):
    '''
    Turns whole notes in twelve bar blues bass line to blues boogie woogie bass line. Takes
    in numRepeats, which is the number of times to repeat the bass line. Also, takes in a
    realization of :meth:`~music21.figuredBass.examples.twelveBarBlues`. If none is provided,
    a default realization with :attr:`~music21.figuredBass.rules.Rules.forbidVoiceOverlap`
    set to False and :attr:`~music21.figuredBass.rules.Rules.partMovementLimits` set to
    [(1, 4), (2, 12), (3, 12)] is used.

    >>> from music21.figuredBass import examples
    >>> #_DOCS_SHOW examples.generateBoogieVamp(numRepeats=1).show()

    .. image:: images/figuredBass/fbExamples_boogieVamp.*
        :width: 700
    '''
    pass


def generateTripletBlues(blRealization=None, numRepeats=5):  # 12/8
    '''
    Turns whole notes in twelve bar blues bass line to triplet blues bass line. Takes
    in numRepeats, which is the number of times to repeat the bass line. Also, takes in a
    realization of :meth:`~music21.figuredBass.examples.twelveBarBlues`. If none is provided,
    a default realization with :attr:`~music21.figuredBass.rules.Rules.forbidVoiceOverlap`
    set to False and :attr:`~music21.figuredBass.rules.Rules.partMovementLimits` set to
    [(1, 4), (2, 12), (3, 12)] is used.

    >>> from music21.figuredBass import examples
    >>> #_DOCS_SHOW examples.generateTripletBlues(numRepeats=1).show()

    .. image:: images/figuredBass/fbExamples_tripletBlues.*
        :width: 700
    '''
    pass


_DOC_ORDER = [exampleA, exampleB, exampleC, exampleD, V43ResolutionExample,
              viio65ResolutionExample,
              augmentedSixthResolutionExample, italianA6ResolutionExample, twelveBarBlues,
              generateBoogieVamp, generateTripletBlues]

# ------------------------------------------------------------------------------


class Test(unittest.TestCase):
    pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

