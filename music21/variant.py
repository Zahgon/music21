# ------------------------------------------------------------------------------
# Name:         variant.py
# Purpose:      Ossia and other variant reading tools
#
# Authors:      Christopher Ariza
#               Evan Lynch
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
# currently the tinyNotation demos use alignment to show variation, making this necessary.

# pylint: disable=line-too-long
# all other lines are linted.
'''
Contains :class:`~music21.variant.Variant` and its subclasses, as well as functions for merging
and showing different variant streams. These functions and the variant class should only be
used when variants of a score are the same length and contain the same measure structure at
this time.
'''
from __future__ import annotations

from collections.abc import Sequence
import copy
import difflib
import unittest

from music21 import base
from music21 import clef
from music21 import common
from music21 import environment
from music21 import exceptions21
from music21 import meter
from music21 import note
from music21 import search
from music21 import stream
from music21.stream.enums import GivenElementsBehavior

environLocal = environment.Environment('variant')


# ------------------------------------------------------------------------------
# classes


class VariantException(exceptions21.Music21Exception):
    pass


class Variant(base.Music21Object):
    '''
    A Music21Object that stores elements like a Stream, but does not
    represent itself externally to a Stream; i.e., the contents of a Variant are not flattened.

    This is accomplished not by subclassing, but by object composition: similar to the Spanner,
    the Variant contains a Stream as a private attribute. Calls to this Stream, for the Variant,
    are automatically delegated by use of the __getattr__ method. Special cases are overridden
    or managed as necessary: e.g., the Duration of a Variant is generally always zero.

    To use Variants from a Stream, see the :func:`~music21.stream.Stream.activateVariants` method.

    >>> v = variant.Variant()
    >>> v.repeatAppend(note.Note(), 8)
    >>> len(v.notes)
    8
    >>> v.highestTime
    0.0
    >>> v.containedHighestTime
    8.0

    >>> v.duration  # handled by Music21Object
    <music21.duration.Duration 0.0>
    >>> v.isStream
    False

    >>> s = stream.Stream()
    >>> s.append(v)
    >>> s.append(note.Note())
    >>> s.highestTime
    1.0
    >>> s.show('t')
    {0.0} <music21.variant.Variant object of length 8.0>
    {0.0} <music21.note.Note C>
    >>> s.flatten().show('t')
    {0.0} <music21.variant.Variant object of length 8.0>
    {0.0} <music21.note.Note C>
    '''

    classSortOrder = stream.Stream.classSortOrder - 2  # variants should always come first?

    # this copies the init of Streams
    def __init__(
        self,
        givenElements: (
            None
            | base.Music21Object
            | Sequence[base.Music21Object]
        ) = None,
        name: str|None = None,
        givenElementsBehavior: GivenElementsBehavior = GivenElementsBehavior.OFFSETS,
        **music21ObjectKeywords,
    ):
        super().__init__(**music21ObjectKeywords)
        self.exposeTime = False
        self._stream = stream.VariantStorage(givenElements=givenElements,
                                             givenElementsBehavior=givenElementsBehavior)

        self._replacementDuration = None

        if name is not None:
            self.groups.append(name)

    # --------------------------------------------------------------------------
    # as _stream is a private Stream, unwrap/wrap methods need to override
    # Music21Object to get at these objects
    # this is the same as with Spanners

    def purgeOrphans(self, excludeStorageStreams=True):
        pass

    def purgeLocations(self, rescanIsDead=False):
        # must override Music21Object to purge locations from the contained
        self._stream.purgeLocations(rescanIsDead=rescanIsDead)
        base.Music21Object.purgeLocations(self, rescanIsDead=rescanIsDead)

    def _reprInternal(self):
        pass

    def __getattr__(self, attr):
        '''
        This defers all calls not defined in this Class to calls on the privately contained Stream.
        '''
        # environLocal.printDebug(['relaying unmatched attribute request '
        #               + attr + ' to private Stream'])

        # must mask pitches so as not to recurse
        # TODO: check tt recurse does not go into this
        if attr in ['flat', 'pitches']:
            raise AttributeError

        # needed for unpickling where ._stream doesn't exist until later
        if attr != '_stream' and hasattr(self, '_stream'):
            return getattr(self._stream, attr)
        else:
            raise AttributeError

    def __getitem__(self, key):
        return self._stream.__getitem__(key)

    def __len__(self):
        return len(self._stream)

    def __iter__(self):
        return self._stream.__iter__()

    def getElementIds(self):
        pass

    def replaceElement(self, old, new):
        '''
        When copying a Variant, we need to update the Variant with new
        references for copied elements. Given the old element,
        this method will replace the old with the new.

        The `old` parameter can be either an object or object id.

        This method is very similar to the replaceSpannedElement method on Spanner.
        '''
        pass

    # --------------------------------------------------------------------------
    # Stream  simulation/overrides
    @property
    def highestTime(self):
        '''
        This property masks calls to Stream.highestTime. Assuming `exposeTime`
        is False, this always returns zero, making the Variant always take zero time.

        >>> v = variant.Variant()
        >>> v.append(note.Note(quarterLength=4))
        >>> v.highestTime
        0.0
        '''
        pass

    @property
    def highestOffset(self):
        '''
        This property masks calls to Stream.highestOffset. Assuming `exposeTime`
        is False, this always returns zero, making the Variant always take zero time.

        >>> v = variant.Variant()
        >>> v.append(note.Note(quarterLength=4))
        >>> v.highestOffset
        0.0
        '''
        pass

    def show(self, fmt=None, app=None):
        '''
        Call show() on the Stream contained by this Variant.

        This method must be overridden, otherwise Music21Object.show() is called.


        >>> v = variant.Variant()
        >>> v.repeatAppend(note.Note(quarterLength=0.25), 8)
        >>> v.show('t')
        {0.0} <music21.note.Note C>
        {0.25} <music21.note.Note C>
        {0.5} <music21.note.Note C>
        {0.75} <music21.note.Note C>
        {1.0} <music21.note.Note C>
        {1.25} <music21.note.Note C>
        {1.5} <music21.note.Note C>
        {1.75} <music21.note.Note C>
        '''
        self._stream.show(fmt=fmt, app=app)

    # --------------------------------------------------------------------------
    # properties particular to this class

    @property
    def containedHighestTime(self):
        '''
        This property calls the contained Stream.highestTime.

        >>> v = variant.Variant()
        >>> v.append(note.Note(quarterLength=4))
        >>> v.containedHighestTime
        4.0
        '''
        pass

    @property
    def containedHighestOffset(self):
        '''
        This property calls the contained Stream.highestOffset.

        >>> v = variant.Variant()
        >>> v.append(note.Note(quarterLength=4))
        >>> v.append(note.Note())
        >>> v.containedHighestOffset
        4.0
        '''
        pass

    @property
    def containedSite(self):
        '''
        Return the Stream contained in this Variant.
        '''
        pass

    def _getReplacementDuration(self):
        pass

    def _setReplacementDuration(self, value):
        pass

    replacementDuration = property(_getReplacementDuration, _setReplacementDuration, doc='''
        Set or Return the quarterLength duration in the main stream which this variant
        object replaces in the variant version of the stream. If replacementDuration is
        not set, it is assumed to be the same length as the variant. If, it is set to 0,
        the variant should be interpreted as an insertion. Setting replacementDuration
        to None will return the value to the default which is the duration of the variant
        itself.
        ''')

    @property
    def lengthType(self):
        '''
        Returns 'deletion' if variant is shorter than the region it replaces, 'elongation'
        if the variant is longer than the region it replaces, and 'replacement' if it is
        the same length.
        '''
        pass

    def replacedElements(self, contextStream=None, classList=None,
                         keepOriginalOffsets=False, includeSpacers=False):
        # noinspection PyShadowingNames
        '''
        Returns a Stream containing the elements which this variant replaces in a
        given context stream.
        This Stream will have length self.replacementDuration.

        In regions that are strictly replaced, only elements that share a class with
        an element in the variant
        are captured. Elsewhere, all elements are captured.

        >>> s = converter.parse("tinynotation: 4/4 d4 e4 f4 g4   a2 b-4 a4    g4 a8 g8 f4 e4    d2 a2                  d4 e4 f4 g4    a2 b-4 a4    g4 a8 b-8 c'4 c4    f1", makeNotation=False)
        >>> s.makeMeasures(inPlace=True)
        >>> v1stream = converter.parse("tinynotation: 4/4        a2. b-8 a8", makeNotation=False)
        >>> v2stream1 = converter.parse("tinynotation: 4/4                                       d4 f4 a2", makeNotation=False)
        >>> v2stream2 = converter.parse("tinynotation: 4/4                                                  d4 f4 AA2", makeNotation=False)

        >>> v1 = variant.Variant()
        >>> v1measure = stream.Measure()
        >>> v1.insert(0.0, v1measure)
        >>> for e in v1stream.notesAndRests:
        ...    v1measure.insert(e.offset, e)

        >>> v2 = variant.Variant()
        >>> v2measure1 = stream.Measure()
        >>> v2measure2 = stream.Measure()
        >>> v2.insert(0.0, v2measure1)
        >>> v2.insert(4.0, v2measure2)
        >>> for e in v2stream1.notesAndRests:
        ...    v2measure1.insert(e.offset, e)
        >>> for e in v2stream2.notesAndRests:
        ...    v2measure2.insert(e.offset, e)

        >>> v3 = variant.Variant()
        >>> v2.replacementDuration = 4.0
        >>> v3.replacementDuration = 4.0

        >>> s.insert(4.0, v1)    # replacement variant
        >>> s.insert(12.0, v2)  # insertion variant (2 bars replace 1 bar)
        >>> s.insert(20.0, v3)  # deletion variant (0 bars replace 1 bar)

        >>> v1.replacedElements(s).show('text')
        {0.0} <music21.stream.Measure 2 offset=0.0>
            {0.0} <music21.note.Note A>
            {2.0} <music21.note.Note B->
            {3.0} <music21.note.Note A>

        >>> v2.replacedElements(s).show('text')
        {0.0} <music21.stream.Measure 4 offset=0.0>
            {0.0} <music21.note.Note D>
            {2.0} <music21.note.Note A>

        >>> v3.replacedElements(s).show('text')
        {0.0} <music21.stream.Measure 6 offset=0.0>
            {0.0} <music21.note.Note A>
            {2.0} <music21.note.Note B->
            {3.0} <music21.note.Note A>

        >>> v3.replacedElements(s, keepOriginalOffsets=True).show('text')
        {20.0} <music21.stream.Measure 6 offset=20.0>
            {0.0} <music21.note.Note A>
            {2.0} <music21.note.Note B->
            {3.0} <music21.note.Note A>


        A second example:


        >>> v = variant.Variant()
        >>> variantDataM1 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
        ...                  ('a', 'quarter'),('b', 'quarter')]
        >>> variantDataM2 = [('c', 'quarter'), ('d', 'quarter'),
        ...                  ('e', 'quarter'), ('e', 'quarter')]
        >>> variantData = [variantDataM1, variantDataM2]
        >>> for d in variantData:
        ...    m = stream.Measure()
        ...    for pitchName, durType in d:
        ...        n = note.Note(pitchName)
        ...        n.duration.type = durType
        ...        m.append(n)
        ...    v.append(m)
        >>> v.groups = ['paris']
        >>> v.replacementDuration = 4.0

        >>> s = stream.Stream()
        >>> streamDataM1 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter')]
        >>> streamDataM2 = [('b', 'eighth'), ('c', 'quarter'),
        ...                 ('a', 'eighth'), ('a', 'quarter'), ('b', 'quarter')]
        >>> streamDataM3 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
        >>> streamDataM4 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
        >>> streamData = [streamDataM1, streamDataM2, streamDataM3, streamDataM4]
        >>> for d in streamData:
        ...    m = stream.Measure()
        ...    for pitchName, durType in d:
        ...        n = note.Note(pitchName)
        ...        n.duration.type = durType
        ...        m.append(n)
        ...    s.append(m)
        >>> s.insert(4.0, v)

        >>> v.replacedElements(s).show('t')
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.note.Note B>
            {0.5} <music21.note.Note C>
            {1.5} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note B>
        '''
        spacerFilter = lambda r: r.hasStyleInformation and r.style.hideObjectOnPrint

        if contextStream is None:
            contextStream = self.activeSite
            if contextStream is None:
                environLocal.printDebug(
                    'No contextStream or activeSite, finding most recently added site (dangerous)')
                contextStream = self.getContextByClass('Stream')
                if contextStream is None:
                    raise VariantException('Cannot find a Stream context for this object.')

        if self not in contextStream.getElementsByClass(self.__class__):
            raise VariantException(f'Variant not found in stream {contextStream}')

        vStart = self.getOffsetBySite(contextStream)

        if includeSpacers is True:
            spacerDuration = (self
                              .getElementsByClass(note.Rest)
                              .addFilter(spacerFilter)
                              .first().duration.quarterLength)
        else:
            spacerDuration = 0.0


        if self.lengthType in ('replacement', 'elongation'):
            vEnd = vStart + self.replacementDuration + spacerDuration
            classes = []
            for e in self.elements:
                classes.append(e.classes[0])
            if classList is not None:
                classes.extend(classList)
            returnStream = contextStream.getElementsByOffset(vStart, vEnd,
                includeEndBoundary=False,
                mustFinishInSpan=False,
                mustBeginInSpan=True,
                classList=classes).stream()

        elif self.lengthType == 'deletion':
            vMiddle = vStart + self.containedHighestTime
            vEnd = vStart + self.replacementDuration
            classes = []  # collect all classes found in this variant
            for e in self.elements:
                classes.append(e.classes[0])
            if classList is not None:
                classes.extend(classList)
            returnPart1 = contextStream.getElementsByOffset(vStart, vMiddle,
                includeEndBoundary=False,
                mustFinishInSpan=False,
                mustBeginInSpan=True,
                classList=classes).stream()
            returnPart2 = contextStream.getElementsByOffset(vMiddle, vEnd,
                includeEndBoundary=False,
                mustFinishInSpan=False,
                mustBeginInSpan=True).stream()

            returnStream = returnPart1
            for e in returnPart2.elements:
                oInPart = e.getOffsetBySite(returnPart2)
                returnStream.insert(vMiddle - vStart + oInPart, e)
        else:
            raise VariantException('lengthType must be replacement, elongation, or deletion')

        if self in returnStream:
            returnStream.remove(self)

        # This probably makes sense to do, but activateVariants
        #    for example only uses the offset in the original.
        #    Also, we are not changing measure numbers and should
        #    not as that will cause activateVariants to fail.
        if keepOriginalOffsets is False:
            for e in returnStream:
                e.setOffsetBySite(returnStream, e.getOffsetBySite(returnStream) - vStart)

        return returnStream

    def removeReplacedElementsFromStream(self, referenceStream=None, classList=None):
        '''
        remove replaced elements from a referenceStream or activeSite


        >>> v = variant.Variant()
        >>> variantDataM1 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
        ...                  ('a', 'quarter'),('b', 'quarter')]
        >>> variantDataM2 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
        >>> variantData = [variantDataM1, variantDataM2]
        >>> for d in variantData:
        ...    m = stream.Measure()
        ...    for pitchName, durType in d:
        ...        n = note.Note(pitchName)
        ...        n.duration.type = durType
        ...        m.append(n)
        ...    v.append(m)
        >>> v.groups = ['paris']
        >>> v.replacementDuration = 4.0

        >>> s = stream.Stream()
        >>> streamDataM1 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter')]
        >>> streamDataM2 = [('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'),
        ...                 ('a', 'quarter'), ('b', 'quarter')]
        >>> streamDataM3 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
        >>> streamDataM4 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
        >>> streamData = [streamDataM1, streamDataM2, streamDataM3, streamDataM4]
        >>> for d in streamData:
        ...    m = stream.Measure()
        ...    for pitchName, durType in d:
        ...        n = note.Note(pitchName)
        ...        n.duration.type = durType
        ...        m.append(n)
        ...    s.append(m)
        >>> s.insert(4.0, v)

        >>> v.removeReplacedElementsFromStream(s)
        >>> s.show('t')
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note G>
        {4.0} <music21.variant.Variant object of length 8.0>
        {8.0} <music21.stream.Measure 0 offset=8.0>
            {0.0} <music21.note.Note C>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note A>
        {12.0} <music21.stream.Measure 0 offset=12.0>
            {0.0} <music21.note.Note C>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note A>
        '''
        pass



# ------Public Merge Functions
def mergeVariants(streamX, streamY, variantName='variant', *, inPlace=False):
    # noinspection PyShadowingNames
    '''
    Takes two streams objects or their derivatives (Score, Part, Measure, etc.) which
    should be variant versions of the same stream,
    and merges them (determines differences and stores those differences as variant objects
    in streamX) via the appropriate merge
    function for their type. This will not know how to deal with scores meant for
    mergePartAsOssia(). If this is the intention, use
    that function instead.

    >>> streamX = converter.parse('tinynotation: 4/4 a4 b  c d', makeNotation=False)
    >>> streamY = converter.parse('tinynotation: 4/4 a4 b- c e', makeNotation=False)

    >>> mergedStream = variant.mergeVariants(streamX, streamY,
    ...                                      variantName='docVariant', inPlace=False)
    >>> mergedStream.show('text')
    {0.0} <music21.meter.TimeSignature 4/4>
    {0.0} <music21.note.Note A>
    {1.0} <music21.variant.Variant object of length 1.0>
    {1.0} <music21.note.Note B>
    {2.0} <music21.note.Note C>
    {3.0} <music21.variant.Variant object of length 1.0>
    {3.0} <music21.note.Note D>

    >>> v0 = mergedStream.getElementsByClass(variant.Variant).first()
    >>> v0
    <music21.variant.Variant object of length 1.0>
    >>> v0.first()
    <music21.note.Note B->

    >>> streamZ = converter.parse('tinynotation: 4/4 a4 b c d e f g a', makeNotation=False)
    >>> variant.mergeVariants(streamX, streamZ, variantName='docVariant', inPlace=False)
    Traceback (most recent call last):
    music21.variant.VariantException: Could not determine what merging method to use.
            Try using a more specific merging function.


    Example: Create a main score (aScore) and a variant score (vScore), each with
    two parts (ap1/vp1
    and ap2/vp2) and some small variants between ap1/vp1 and ap2/vp2, marked with * below.

    >>> aScore = stream.Score()
    >>> vScore = stream.Score()

    >>> #                                                 *
    >>> ap1 = converter.parse('tinynotation: 4/4   a4 b c d    e2 f   g2 f4 g ')
    >>> vp1 = converter.parse('tinynotation: 4/4   a4 b c e    e2 f   g2 f4 a ')

    >>> #                                                         *    *    *
    >>> ap2 = converter.parse('tinynotation: 4/4   a4 g f e    f2 e   d2 g4 f ')
    >>> vp2 = converter.parse('tinynotation: 4/4   a4 g f e    f2 g   f2 g4 d ')

    >>> ap1.id = 'aPart1'
    >>> ap2.id = 'aPart2'

    >>> aScore.insert(0.0, ap1)
    >>> aScore.insert(0.0, ap2)
    >>> vScore.insert(0.0, vp1)
    >>> vScore.insert(0.0, vp2)

    Create one merged score where everything different in vScore from aScore is called a variant.

    >>> mergedScore = variant.mergeVariants(aScore, vScore, variantName='docVariant', inPlace=False)
    >>> mergedScore.show('text')
    {0.0} <music21.stream.Part aPart1>
        {0.0} <music21.variant.Variant object of length 4.0>
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note C>
            {3.0} <music21.note.Note D>
        {4.0} <music21.stream.Measure 2 offset=4.0>
            {0.0} <music21.note.Note E>
            {2.0} <music21.note.Note F>
        {8.0} <music21.variant.Variant object of length 4.0>
        {8.0} <music21.stream.Measure 3 offset=8.0>
            {0.0} <music21.note.Note G>
            {2.0} <music21.note.Note F>
            {3.0} <music21.note.Note G>
            {4.0} <music21.bar.Barline type=final>
    {0.0} <music21.stream.Part aPart2>
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note G>
            {2.0} <music21.note.Note F>
            {3.0} <music21.note.Note E>
        {4.0} <music21.variant.Variant object of length 8.0>
        {4.0} <music21.stream.Measure 2 offset=4.0>
            {0.0} <music21.note.Note F>
            {2.0} <music21.note.Note E>
        {8.0} <music21.stream.Measure 3 offset=8.0>
            {0.0} <music21.note.Note D>
            {2.0} <music21.note.Note G>
            {3.0} <music21.note.Note F>
            {4.0} <music21.bar.Barline type=final>


    >>> mergedPart = variant.mergeVariants(ap2, vp2, variantName='docVariant', inPlace=False)
    >>> mergedPart.show('text')
    {0.0} <music21.stream.Measure 1 offset=0.0>
    ...
    {4.0} <music21.variant.Variant object of length 8.0>
    {4.0} <music21.stream.Measure 2 offset=4.0>
    ...
        {4.0} <music21.bar.Barline type=final>
    '''
    pass


def mergeVariantScores(aScore, vScore, variantName='variant', *, inPlace=False):
    # noinspection PyShadowingNames
    '''
    Takes two scores and merges them with mergeVariantMeasureStreams, part-by-part.

    >>> aScore, vScore = stream.Score(), stream.Score()

    >>> ap1 = converter.parse('tinynotation: 4/4   a4 b c d    e2 f2   g2 f4 g4 ')
    >>> vp1 = converter.parse('tinynotation: 4/4   a4 b c e    e2 f2   g2 f4 a4 ')

    >>> ap2 = converter.parse('tinynotation: 4/4   a4 g f e    f2 e2   d2 g4 f4 ')
    >>> vp2 = converter.parse('tinynotation: 4/4   a4 g f e    f2 g2   f2 g4 d4 ')

    >>> aScore.insert(0.0, ap1)
    >>> aScore.insert(0.0, ap2)
    >>> vScore.insert(0.0, vp1)
    >>> vScore.insert(0.0, vp2)

    >>> mergedScores = variant.mergeVariantScores(aScore, vScore,
    ...                                           variantName='docVariant', inPlace=False)
    >>> mergedScores.show('text')
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.variant.Variant object of length 4.0>
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note C>
            {3.0} <music21.note.Note D>
        {4.0} <music21.stream.Measure 2 offset=4.0>
            {0.0} <music21.note.Note E>
            {2.0} <music21.note.Note F>
        {8.0} <music21.variant.Variant object of length 4.0>
        {8.0} <music21.stream.Measure 3 offset=8.0>
            {0.0} <music21.note.Note G>
            {2.0} <music21.note.Note F>
            {3.0} <music21.note.Note G>
            {4.0} <music21.bar.Barline type=final>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.stream.Measure 1 offset=0.0>
            {0.0} <music21.clef.TrebleClef>
            {0.0} <music21.meter.TimeSignature 4/4>
            {0.0} <music21.note.Note A>
            {1.0} <music21.note.Note G>
            {2.0} <music21.note.Note F>
            {3.0} <music21.note.Note E>
        {4.0} <music21.variant.Variant object of length 8.0>
        {4.0} <music21.stream.Measure 2 offset=4.0>
            {0.0} <music21.note.Note F>
            {2.0} <music21.note.Note E>
        {8.0} <music21.stream.Measure 3 offset=8.0>
            {0.0} <music21.note.Note D>
            {2.0} <music21.note.Note G>
            {3.0} <music21.note.Note F>
            {4.0} <music21.bar.Barline type=final>
    '''
    pass


def mergeVariantMeasureStreams(streamX, streamY, variantName='variant', *, inPlace=False):
    '''
    Takes two streams of measures and returns a stream (new if inPlace is False) with the second
    merged with the first as variants. This function differs from mergeVariantsEqualDuration by
    dealing with streams that are of different length. This function matches measures that are
    exactly equal and creates variant objects for regions of measures that differ at all. If more
    refined variants are sought (with variation within the bar considered and related but different
    bars associated with each other), use variant.refineVariant().

    In this example, the second bar has been deleted in the second version,
    a new bar has been inserted between the
    original third and fourth bars, and two bars have been added at the end.


    >>> data1M1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...            ('a', 'quarter'), ('a', 'quarter')]
    >>> data1M2 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
    ...            ('a', 'quarter'),('b', 'quarter')]
    >>> data1M3 = [('c', 'quarter'), ('d', 'quarter'),
    ...            ('e', 'quarter'), ('e', 'quarter')]
    >>> data1M4 = [('d', 'quarter'), ('g', 'eighth'), ('g', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]

    >>> data2M1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...            ('a', 'quarter'), ('a', 'quarter')]
    >>> data2M2 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
    >>> data2M3 = [('e', 'quarter'), ('g', 'eighth'), ('g', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> data2M4 = [('d', 'quarter'), ('g', 'eighth'), ('g', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> data2M5 = [('f', 'eighth'), ('c', 'quarter'), ('a', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> data2M6 = [('g', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]

    >>> data1 = [data1M1, data1M2, data1M3, data1M4]
    >>> data2 = [data2M1, data2M2, data2M3, data2M4, data2M5, data2M6]
    >>> stream1 = stream.Stream()
    >>> stream2 = stream.Stream()
    >>> mNumber = 1
    >>> for d in data1:
    ...    m = stream.Measure()
    ...    m.number = mNumber
    ...    mNumber += 1
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    stream1.append(m)
    >>> mNumber = 1
    >>> for d in data2:
    ...    m = stream.Measure()
    ...    m.number = mNumber
    ...    mNumber += 1
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    stream2.append(m)
    >>> #_DOCS_SHOW stream1.show()


    .. image:: images/variant_measuresStreamMergeStream1.*
        :width: 600

    >>> #_DOCS_SHOW stream2.show()


    .. image:: images/variant_measuresStreamMergeStream2.*
        :width: 600

    >>> mergedStream = variant.mergeVariantMeasureStreams(stream1, stream2, 'paris', inPlace=False)
    >>> mergedStream.show('text')
    {0.0} <music21.stream.Measure 1 offset=0.0>
        {0.0} <music21.note.Note A>
        {1.0} <music21.note.Note B>
        {1.5} <music21.note.Note C>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note A>
    {4.0} <music21.variant.Variant object of length 0.0>
    {4.0} <music21.stream.Measure 2 offset=4.0>
        {0.0} <music21.note.Note B>
        {0.5} <music21.note.Note C>
        {1.0} <music21.note.Note A>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {8.0} <music21.stream.Measure 3 offset=8.0>
        {0.0} <music21.note.Note C>
        {1.0} <music21.note.Note D>
        {2.0} <music21.note.Note E>
        {3.0} <music21.note.Note E>
    {12.0} <music21.variant.Variant object of length 4.0>
    {12.0} <music21.stream.Measure 4 offset=12.0>
        {0.0} <music21.note.Note D>
        {1.0} <music21.note.Note G>
        {1.5} <music21.note.Note G>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {16.0} <music21.variant.Variant object of length 8.0>

    >>> mergedStream[variant.Variant][0].replacementDuration
    4.0
    >>> mergedStream[variant.Variant][1].replacementDuration
    0.0

    >>> parisStream = mergedStream.activateVariants('paris', inPlace=False)
    >>> parisStream.show('text')
    {0.0} <music21.stream.Measure 1 offset=0.0>
        {0.0} <music21.note.Note A>
        {1.0} <music21.note.Note B>
        {1.5} <music21.note.Note C>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note A>
    {4.0} <music21.variant.Variant object of length 4.0>
    {4.0} <music21.stream.Measure 2 offset=4.0>
        {0.0} <music21.note.Note C>
        {1.0} <music21.note.Note D>
        {2.0} <music21.note.Note E>
        {3.0} <music21.note.Note E>
    {8.0} <music21.variant.Variant object of length 0.0>
    {8.0} <music21.stream.Measure 3 offset=8.0>
        {0.0} <music21.note.Note E>
        {1.0} <music21.note.Note G>
        {1.5} <music21.note.Note G>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {12.0} <music21.stream.Measure 4 offset=12.0>
        {0.0} <music21.note.Note D>
        {1.0} <music21.note.Note G>
        {1.5} <music21.note.Note G>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {16.0} <music21.variant.Variant object of length 0.0>
    {16.0} <music21.stream.Measure 5 offset=16.0>
        {0.0} <music21.note.Note F>
        {0.5} <music21.note.Note C>
        {1.5} <music21.note.Note A>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {20.0} <music21.stream.Measure 6 offset=20.0>
        {0.0} <music21.note.Note G>
        {1.0} <music21.note.Note D>
        {2.0} <music21.note.Note E>
        {3.0} <music21.note.Note E>

    >>> parisStream[variant.Variant][0].replacementDuration
    0.0
    >>> parisStream[variant.Variant][1].replacementDuration
    4.0
    >>> parisStream[variant.Variant][2].replacementDuration
    8.0
    '''
    pass


def mergeVariantsEqualDuration(streams, variantNames, *, inPlace=False):
    '''
    Pass this function a list of streams (they must be of the same
    length or a VariantException will be raised).
    It will return a stream which merges the differences between the
    streams into variant objects keeping the
    first stream in the list as the default. If inPlace is True, the
    first stream in the list will be modified,
    otherwise a new stream will be returned. Pass a list of names to
    associate variants with their sources, if this list
    does not contain an entry for each non-default variant,
    naming may not behave properly. Variants that have the
    same differences from the default will be saved as separate
    variant objects (i.e. more than once under different names).
    Also, note that a streams with bars of differing lengths will not behave properly.


    >>> stream1 = stream.Stream()
    >>> stream2paris = stream.Stream()
    >>> stream3london = stream.Stream()
    >>> data1 = [('a', 'quarter'), ('b', 'eighth'),
    ...    ('c', 'eighth'), ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'quarter'), ('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter')]
    >>> data2 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'), ('a', 'quarter'),
    ...    ('b', 'quarter'), ('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter')]
    >>> data3 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...    ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'), ('a', 'quarter'),
    ...    ('c', 'quarter'), ('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter')]
    >>> for pitchName, durType in data1:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    stream1.append(n)
    >>> for pitchName, durType in data2:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    stream2paris.append(n)
    >>> for pitchName, durType in data3:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    stream3london.append(n)
    >>> mergedStreams = variant.mergeVariantsEqualDuration(
    ...       [stream1, stream2paris, stream3london], ['paris', 'london'])
    >>> mergedStreams.show('t')
    {0.0} <music21.note.Note A>
    {1.0} <music21.variant.Variant object of length 1.0>
    {1.0} <music21.note.Note B>
    {1.5} <music21.note.Note C>
    {2.0} <music21.note.Note A>
    {3.0} <music21.variant.Variant object of length 1.0>
    {3.0} <music21.note.Note A>
    {4.0} <music21.note.Note B>
    {4.5} <music21.variant.Variant object of length 1.5>
    {4.5} <music21.note.Note C>
    {5.0} <music21.note.Note A>
    {6.0} <music21.note.Note A>
    {7.0} <music21.variant.Variant object of length 1.0>
    {7.0} <music21.note.Note B>
    {8.0} <music21.note.Note C>
    {9.0} <music21.variant.Variant object of length 2.0>
    {9.0} <music21.note.Note D>
    {10.0} <music21.note.Note E>

    >>> mergedStreams.activateVariants('london').show('t')
    {0.0} <music21.note.Note A>
    {1.0} <music21.variant.Variant object of length 1.0>
    {1.0} <music21.note.Note B>
    {1.5} <music21.note.Note C>
    {2.0} <music21.note.Note A>
    {3.0} <music21.variant.Variant object of length 1.0>
    {3.0} <music21.note.Note A>
    {4.0} <music21.note.Note B>
    {4.5} <music21.variant.Variant object of length 1.5>
    {4.5} <music21.note.Note C>
    {5.0} <music21.note.Note A>
    {6.0} <music21.note.Note A>
    {7.0} <music21.variant.Variant object of length 1.0>
    {7.0} <music21.note.Note C>
    {8.0} <music21.note.Note C>
    {9.0} <music21.variant.Variant object of length 2.0>
    {9.0} <music21.note.Note D>
    {10.0} <music21.note.Note E>

    If the streams contain parts and measures, the merge function will iterate
    through them and determine
    and store variant differences within each measure/part.

    >>> stream1 = stream.Stream()
    >>> stream2 = stream.Stream()
    >>> data1M1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...            ('a', 'quarter'), ('a', 'quarter')]
    >>> data1M2 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
    ...            ('a', 'quarter'),('b', 'quarter')]
    >>> data1M3 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
    >>> data2M1 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter')]
    >>> data2M2 = [('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> data2M3 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
    >>> data1 = [data1M1, data1M2, data1M3]
    >>> data2 = [data2M1, data2M2, data2M3]
    >>> tempPart = stream.Part()
    >>> for d in data1:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    tempPart.append(m)
    >>> stream1.append(tempPart)
    >>> tempPart = stream.Part()
    >>> for d in data2:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    tempPart.append(m)
    >>> stream2.append(tempPart)
    >>> mergedStreams = variant.mergeVariantsEqualDuration([stream1, stream2], ['paris'])
    >>> mergedStreams.show('t')
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.note.Note A>
            {1.0} <music21.variant.Variant object of length 1.0>
            {1.0} <music21.note.Note B>
            {1.5} <music21.note.Note C>
            {2.0} <music21.note.Note A>
            {3.0} <music21.variant.Variant object of length 1.0>
            {3.0} <music21.note.Note A>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note B>
            {0.5} <music21.variant.Variant object of length 1.5>
            {0.5} <music21.note.Note C>
            {1.0} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note B>
        {8.0} <music21.stream.Measure 0 offset=8.0>
            {0.0} <music21.note.Note C>
            {1.0} <music21.variant.Variant object of length 3.0>
            {1.0} <music21.note.Note D>
            {2.0} <music21.note.Note E>
            {3.0} <music21.note.Note E>
    >>> #_DOCS_SHOW mergedStreams.show()


    .. image:: images/variant_measuresAndParts.*
        :width: 600


    >>> for p in mergedStreams.getElementsByClass(stream.Part):
    ...    for m in p.getElementsByClass(stream.Measure):
    ...        m.activateVariants('paris', inPlace=True)
    >>> mergedStreams.show('t')
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.stream.Measure 0 offset=0.0>
            {0.0} <music21.note.Note A>
            {1.0} <music21.variant.Variant object of length 1.0>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note A>
            {3.0} <music21.variant.Variant object of length 1.0>
            {3.0} <music21.note.Note G>
        {4.0} <music21.stream.Measure 0 offset=4.0>
            {0.0} <music21.note.Note B>
            {0.5} <music21.variant.Variant object of length 1.5>
            {0.5} <music21.note.Note C>
            {1.5} <music21.note.Note A>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note B>
        {8.0} <music21.stream.Measure 0 offset=8.0>
            {0.0} <music21.note.Note C>
            {1.0} <music21.variant.Variant object of length 3.0>
            {1.0} <music21.note.Note B>
            {2.0} <music21.note.Note A>
            {3.0} <music21.note.Note A>
    >>> #_DOCS_SHOW mergedStreams.show()


    .. image:: images/variant_measuresAndParts2.*
        :width: 600

    If barlines do not match up, an exception will be thrown. Here two streams that are identical
    are merged, except one is in 3/4, the other in 4/4. This throws an exception.

    >>> streamDifferentMeasures = stream.Stream()
    >>> dataDiffM1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter')]
    >>> dataDiffM2 = [ ('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter')]
    >>> dataDiffM3 = [('a', 'quarter'), ('b', 'quarter'), ('c', 'quarter')]
    >>> dataDiffM4 = [('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
    >>> dataDiff = [dataDiffM1, dataDiffM2, dataDiffM3, dataDiffM4]
    >>> streamDifferentMeasures.insert(0.0, meter.TimeSignature('3/4'))
    >>> tempPart = stream.Part()
    >>> for d in dataDiff:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    tempPart.append(m)
    >>> streamDifferentMeasures.append(tempPart)
    >>> mergedStreams = variant.mergeVariantsEqualDuration(
    ...                 [stream1, streamDifferentMeasures], ['paris'])
    Traceback (most recent call last):
    music21.variant.VariantException: _mergeVariants cannot merge streams
        which are of different lengths
    '''
    pass


def mergePartAsOssia(mainPart, ossiaPart, ossiaName,
                     inPlace=False, compareByMeasureNumber=False, recurseInMeasures=False):
    # noinspection PyShadowingNames
    '''
    Some MusicXML files are generated with full parts that have only a few non-rest measures
    instead of ossia parts, such as those
    created by Sibelius 7. This function
    takes two streams (mainPart and ossiaPart), the second interpreted as an ossia.
    It outputs a stream with the ossia part merged into the stream as a
    group of variants.

    If compareByMeasureNumber is True, then the ossia measures will be paired with the
    measures in the mainPart that have the
    same measure.number. Otherwise, they will be paired by offset. In most cases
    these should have the same result.

    Note that this method has no way of knowing if a variant is supposed to be a
    different duration than the segment of stream which it replaces
    because that information is not contained in the format of score this method is
    designed to deal with.


    >>> mainStream = converter.parse('tinynotation: 4/4   A4 B4 C4 D4   E1    F2 E2     E8 F8 F4 G2   G2 G4 F4   F4 F4 F4 F4   G1      ')
    >>> ossiaStream = converter.parse('tinynotation: 4/4  r1            r1    r1        E4 E4 F4 G4   r1         F2    F2      r1      ')
    >>> mainStream.makeMeasures(inPlace=True)
    >>> ossiaStream.makeMeasures(inPlace=True)

    >>> mainPart = stream.Part()
    >>> for m in mainStream:
    ...    mainPart.insert(m.offset, m)
    >>> ossiaPart = stream.Part()
    >>> for m in ossiaStream:
    ...    ossiaPart.insert(m.offset, m)

    >>> s = stream.Stream()
    >>> s.insert(0.0, ossiaPart)
    >>> s.insert(0.0, mainPart)
    >>> #_DOCS_SHOW s.show()

    >>> mainPartWithOssiaVariantsFT = variant.mergePartAsOssia(mainPart, ossiaPart,
    ...                                                            ossiaName='Parisian_Variant',
    ...                                                            inPlace=False,
    ...                                                            compareByMeasureNumber=False,
    ...                                                            recurseInMeasures=True)
    >>> mainPartWithOssiaVariantsTT = variant.mergePartAsOssia(mainPart, ossiaPart,
    ...                                                            ossiaName='Parisian_Variant',
    ...                                                            inPlace=False,
    ...                                                            compareByMeasureNumber=True,
    ...                                                            recurseInMeasures=True)
    >>> mainPartWithOssiaVariantsFF = variant.mergePartAsOssia(mainPart, ossiaPart,
    ...                                                            ossiaName='Parisian_Variant',
    ...                                                            inPlace=False,
    ...                                                            compareByMeasureNumber=False,
    ...                                                            recurseInMeasures=False)
    >>> mainPartWithOssiaVariantsTF = variant.mergePartAsOssia(mainPart, ossiaPart,
    ...                                                            ossiaName='Parisian_Variant',
    ...                                                            inPlace=False,
    ...                                                            compareByMeasureNumber=True,
    ...                                                            recurseInMeasures=False)

    >>> mainPartWithOssiaVariantsFT.show('text') == mainPartWithOssiaVariantsTT.show('text')
    {0.0} <music21.stream.Measure ...
    True

    >>> mainPartWithOssiaVariantsFF.show('text') == mainPartWithOssiaVariantsFT.show('text')
    {0.0} <music21.stream.Measure ...
    True

    >>> mainPartWithOssiaVariantsFT.show('text')
    {0.0} <music21.stream.Measure 1 offset=0.0>
    ...
    {12.0} <music21.stream.Measure 4 offset=12.0>
        {0.0} <music21.variant.Variant object of length 3.0>
        {0.0} <music21.note.Note E>
        {0.5} <music21.note.Note F>
        {1.0} <music21.note.Note F>
        {2.0} <music21.note.Note G>
    {16.0} <music21.stream.Measure 5 offset=16.0>
    ...
    {20.0} <music21.stream.Measure 6 offset=20.0>
        {0.0} <music21.variant.Variant object of length 4.0>
        {0.0} <music21.note.Note F>
        {1.0} <music21.note.Note F>
        {2.0} <music21.note.Note F>
        {3.0} <music21.note.Note F>
    ...

    >>> mainPartWithOssiaVariantsFF.activateVariants('Parisian_Variant').show('text')
    {0.0} <music21.stream.Measure 1 offset=0.0>
    ...
    {12.0} <music21.variant.Variant object of length 4.0>
    {12.0} <music21.stream.Measure 4 offset=12.0>
        {0.0} <music21.note.Note E>
        {1.0} <music21.note.Note E>
        {2.0} <music21.note.Note F>
        {3.0} <music21.note.Note G>
    {16.0} <music21.stream.Measure 5 offset=16.0>
    ...
    {20.0} <music21.variant.Variant object of length 4.0>
    {20.0} <music21.stream.Measure 6 offset=20.0>
        {0.0} <music21.note.Note F>
        {2.0} <music21.note.Note F>
    ...

    '''
    pass


# ------ Public Helper Functions

def addVariant(
    s: stream.Stream,
    startOffset: int|float,
    sVariant: stream.Stream|Variant,
    variantName=None,
    variantGroups=None,
    replacementDuration=None
):
    # noinspection PyShadowingNames
    '''
    Takes a stream, the location of the variant to be added to
    that stream (startOffset), the content of the
    variant to be added (sVariant), and the duration of the section of the stream which the variant
    replaces (replacementDuration).

    If replacementDuration is 0,
    this is an insertion. If sVariant is
    None, this is a deletion.


    >>> data1M1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...            ('a', 'quarter'), ('a', 'quarter')]
    >>> data1M3 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
    >>> data1M2 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
    ...            ('a', 'quarter'),('b', 'quarter')]
    >>> data1 = [data1M1, data1M2, data1M3]
    >>> tempPart = stream.Part()
    >>> stream1 = stream.Stream()
    >>> for d in data1:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    stream1.append(m)

    >>> data2M2 = [('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> stream2 = stream.Stream()
    >>> m = stream.Measure()
    >>> for pitchName, durType in data2M2:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    m.append(n)
    >>> stream2.append(m)
    >>> variant.addVariant(stream1, 4.0, stream2,
    ...                    variantName='rhythmic_switch', replacementDuration=4.0)
    >>> stream1.show('text')
    {0.0} <music21.stream.Measure 0 offset=0.0>
        {0.0} <music21.note.Note A>
        {1.0} <music21.note.Note B>
        {1.5} <music21.note.Note C>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note A>
    {4.0} <music21.variant.Variant object of length 4.0>
    {4.0} <music21.stream.Measure 0 offset=4.0>
        {0.0} <music21.note.Note B>
        {0.5} <music21.note.Note C>
        {1.0} <music21.note.Note A>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {8.0} <music21.stream.Measure 0 offset=8.0>
        {0.0} <music21.note.Note C>
        {1.0} <music21.note.Note D>
        {2.0} <music21.note.Note E>
        {3.0} <music21.note.Note E>

    >>> stream1 = stream.Stream()
    >>> stream1.repeatAppend(note.Note('e'), 6)
    >>> variant1 = variant.Variant()
    >>> variant1.repeatAppend(note.Note('f'), 3)
    >>> startOffset = 3.0
    >>> variant.addVariant(stream1, startOffset, variant1,
    ...                    variantName='paris', replacementDuration=3.0)
    >>> stream1.show('text')
    {0.0} <music21.note.Note E>
    {1.0} <music21.note.Note E>
    {2.0} <music21.note.Note E>
    {3.0} <music21.variant.Variant object of length 6.0>
    {3.0} <music21.note.Note E>
    {4.0} <music21.note.Note E>
    {5.0} <music21.note.Note E>
    '''
    pass



def refineVariant(s, sVariant, *, inPlace=False):
    # noinspection PyShadowingNames
    '''
    Given a stream and variant contained in that stream, returns a
    stream with that variant 'refined.'

    It is refined in the sense that, (with the best estimates) measures which have been determined
    to be related are merged within the measure.

    Suppose a four-bar phrase in a piece is a slightly
    different five-bar phrase in a variant. In the variant, every F# has been replaced by an F,
    and the last bar is repeated. Given these streams, mergeVariantMeasureStreams would return
    the first stream with a single variant object containing the entire 5 bars of the variant.
    Calling refineVariant on this stream and that variant object would result in a variant object
    in the measures for each F#/F pair, and a variant object containing the added bar at the end.
    For a more detailed explanation of how similar measures are properly associated with each other
    look at the documentation for _getBestListAndScore

    Note that this code does not work properly yet.


    >>> v = variant.Variant()
    >>> variantDataM1 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
    ...                  ('a', 'quarter'),('b', 'quarter')]
    >>> variantDataM2 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]
    >>> variantData = [variantDataM1, variantDataM2]
    >>> for d in variantData:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    v.append(m)
    >>> v.groups = ['paris']
    >>> v.replacementDuration = 8.0

    >>> s = stream.Stream()
    >>> streamDataM1 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter')]
    >>> streamDataM2 = [('b', 'eighth'), ('c', 'quarter'),
    ...                 ('a', 'eighth'), ('a', 'quarter'), ('b', 'quarter')]
    >>> streamDataM3 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
    >>> streamDataM4 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
    >>> streamData = [streamDataM1, streamDataM2, streamDataM3, streamDataM4]
    >>> for d in streamData:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    s.append(m)
    >>> s.insert(4.0, v)

    >>> variant.refineVariant(s, v, inPlace=True)
    >>> s.show('text')
    {0.0} <music21.stream.Measure 0 offset=0.0>
        {0.0} <music21.note.Note A>
        {1.0} <music21.note.Note B>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note G>
    {4.0} <music21.stream.Measure 0 offset=4.0>
        {0.0} <music21.note.Note B>
        {0.5} <music21.variant.Variant object of length 1.5>
        {0.5} <music21.note.Note C>
        {1.5} <music21.note.Note A>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note B>
    {8.0} <music21.stream.Measure 0 offset=8.0>
        {0.0} <music21.note.Note C>
        {1.0} <music21.variant.Variant object of length 3.0>
        {1.0} <music21.note.Note B>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note A>
    {12.0} <music21.stream.Measure 0 offset=12.0>
        {0.0} <music21.note.Note C>
        {1.0} <music21.note.Note B>
        {2.0} <music21.note.Note A>
        {3.0} <music21.note.Note A>

    '''
    pass


def _mergeVariantMeasureStreamsCarefully(streamX, streamY, variantName, *, inPlace=False):
    '''
    There seem to be some problems with this function, and it isn't well tested.
    It is not recommended to use it at this time.

    '''
    pass


def getMeasureHashes(s):
    # noinspection PyShadowingNames
    '''
    Takes in a stream containing measures and returns a list of hashes,
    one for each measure. This is currently implemented
    with search.translateStreamToString()

    >>> s = converter.parse("tinynotation: 2/4 c4 d8. e16 FF4 a'4 b-2")
    >>> sm = s.makeMeasures()
    >>> hashes = variant.getMeasureHashes(sm)
    >>> hashes
    ['<P>K@<', ')PQP', 'FZ']
    '''
    pass


# ----- Private Helper Functions
def _getBestListAndScore(streamX, streamY, badnessDict, listDict,
                         isNone=False, streamXIndex=-1, streamYIndex=-1):
    # noinspection PyShadowingNames
    '''
    This is a recursive function which makes a map between two related streams of measures.
    It is designed for streams of measures that contain few if any measures that are actually
    identical and that have a different number of measures (within reason). For example,
    if one stream has 10 bars of eighth notes and the second stream has the same ten bars
    of eighth notes except with some dotted rhythms mixed in and the fifth bar is repeated.
    The first, streamX, is the reference stream. This function returns a list of
    integers with length len(streamY) which maps each measure of StreamY to the measure
    in streamX it is most likely associated with. For example, if the returned list is
    [0, 2, 3, 'addedBar', 4]. This indicates that streamY is most similar to streamX
    after the second bar of streamX has been removed and a new bar inserted between
    bars 4 and 5. Note that this list has measures 0-indexed. This function generates this map by
    minimizing the difference or 'badness' for the sequence of measures on the whole as determined
    by the helper function _simScore which compares measures for similarity. 'addedBar' appears
    in the list where this function has determined that the bar appearing
    in streamY does not have a counterpart in streamX anywhere and is an insertion.


    >>> badnessDict = {}
    >>> listDict = {}
    >>> stream1 = stream.Stream()
    >>> stream2 = stream.Stream()

    >>> data1M1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...            ('a', 'quarter'), ('a', 'quarter')]
    >>> data1M2 = [('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'),
    ...            ('a', 'quarter'),('b', 'quarter')]
    >>> data1M3 = [('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter'), ('e', 'quarter')]

    >>> data2M1 = [('a', 'quarter'), ('b', 'quarter'), ('c', 'quarter'), ('g#', 'quarter')]
    >>> data2M2 = [('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'),
    ...            ('a', 'quarter'), ('b', 'quarter')]
    >>> data2M3 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
    >>> data2M4 = [('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('a', 'quarter')]
    >>> data1 = [data1M1, data1M2, data1M3]
    >>> data2 = [data2M1, data2M2, data2M3, data2M4]
    >>> for d in data1:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    stream1.append(m)
    >>> for d in data2:
    ...    m = stream.Measure()
    ...    for pitchName, durType in d:
    ...        n = note.Note(pitchName)
    ...        n.duration.type = durType
    ...        m.append(n)
    ...    stream2.append(m)
    >>> kList, kBadness = variant._getBestListAndScore(stream1, stream2,
    ...                                                badnessDict, listDict, isNone=False)
    >>> kList
    [0, 1, 2, 'addedBar']
    '''
    pass


def _diffScore(measureX, measureY):
    '''
    Helper function for _getBestListAndScore which compares two measures and returns a value
    associated with their similarity. The higher the normalized (0, 1) value the poorer the match.
    This should be calibrated such that the value that appears in _getBestListAndScore for
    isNone is true (i.e. testing when a bar does not associate with any existing bars the reference
    stream), is well-matched with the similarity scores generated by this function.


    >>> m1 = stream.Measure()
    >>> m2 = stream.Measure()
    >>> m1.append([note.Note('e'), note.Note('f'), note.Note('g'), note.Note('a')])
    >>> m2.append([note.Note('e'), note.Note('f'), note.Note('g#'), note.Note('a')])
    >>> variant._diffScore(m1, m2)
    0.4...

    '''
    pass


def _getRegionsFromStreams(streamX, streamY):
    # noinspection PyShadowingNames
    '''
    Takes in two streams, returns a list of 5-tuples via difflib.get_opcodes()
    working on measure differences.


    >>> s1 = converter.parse("tinynotation: 2/4 d4 e8. f16 GG4 b'4 b-2 c4 d8. e16 FF4 a'4 b-2")

                                                *0:Eq  *1:Rep        * *3:Eq             *6:In

    >>> s2 = converter.parse("tinynotation: 2/4 d4 e8. f16 FF4 b'4 c4 d8. e16 FF4 a'4 b-2 b-2")
    >>> s1m = s1.makeMeasures()
    >>> s2m = s2.makeMeasures()
    >>> regions = variant._getRegionsFromStreams(s1m, s2m)
    >>> regions
    [('equal', 0, 1, 0, 1),
     ('replace', 1, 3, 1, 2),
     ('equal', 3, 6, 2, 5),
     ('insert', 6, 6, 5, 6)]

    '''
    pass


def _mergeVariants(streamA, streamB, *, variantName=None, inPlace=False):
    '''
    This is a helper function for mergeVariantsEqualDuration which takes two streams
    (which cannot contain container
    streams like measures and parts) and merges the second into the first via variant objects.
    If the first already contains variant objects, containsVariants should be set to true and the
    function will compare streamB to the streamA as well as the
    variant streams contained in streamA.
    Note that variant streams in streamB will be ignored and lost.


    >>> stream1 = stream.Stream()
    >>> stream2 = stream.Stream()
    >>> data1 = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...    ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'quarter'), ('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter')]
    >>> data2 = [('a', 'quarter'), ('b', 'quarter'), ('a', 'quarter'), ('g', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'quarter'), ('a', 'eighth'), ('a', 'quarter'),
    ...    ('b', 'quarter'), ('c', 'quarter'), ('b', 'quarter'), ('a', 'quarter')]
    >>> for pitchName, durType in data1:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    stream1.append(n)
    >>> for pitchName, durType in data2:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    stream2.append(n)
    >>> mergedStreams = variant._mergeVariants(stream1, stream2, variantName='paris')
    >>> mergedStreams.show('t')
    {0.0} <music21.note.Note A>
    {1.0} <music21.variant.Variant object of length 1.0>
    {1.0} <music21.note.Note B>
    {1.5} <music21.note.Note C>
    {2.0} <music21.note.Note A>
    {3.0} <music21.variant.Variant object of length 1.0>
    {3.0} <music21.note.Note A>
    {4.0} <music21.note.Note B>
    {4.5} <music21.variant.Variant object of length 1.5>
    {4.5} <music21.note.Note C>
    {5.0} <music21.note.Note A>
    {6.0} <music21.note.Note A>
    {7.0} <music21.note.Note B>
    {8.0} <music21.note.Note C>
    {9.0} <music21.variant.Variant object of length 2.0>
    {9.0} <music21.note.Note D>
    {10.0} <music21.note.Note E>

    >>> mergedStreams.activateVariants('paris').show('t')
    {0.0} <music21.note.Note A>
    {1.0} <music21.variant.Variant object of length 1.0>
    {1.0} <music21.note.Note B>
    {2.0} <music21.note.Note A>
    {3.0} <music21.variant.Variant object of length 1.0>
    {3.0} <music21.note.Note G>
    {4.0} <music21.note.Note B>
    {4.5} <music21.variant.Variant object of length 1.5>
    {4.5} <music21.note.Note C>
    {5.5} <music21.note.Note A>
    {6.0} <music21.note.Note A>
    {7.0} <music21.note.Note B>
    {8.0} <music21.note.Note C>
    {9.0} <music21.variant.Variant object of length 2.0>
    {9.0} <music21.note.Note B>
    {10.0} <music21.note.Note A>

    >>> stream1.append(note.Note('e'))
    >>> mergedStreams = variant._mergeVariants(stream1, stream2, variantName=['paris'])
    Traceback (most recent call last):
    music21.variant.VariantException: _mergeVariants cannot merge streams
        which are of different lengths
    '''
    pass


def _generateVariant(noteList, originStream, start, variantName=None):
    # noinspection PyShadowingNames
    '''
    Helper function for mergeVariantsEqualDuration which takes a list of
    consecutive notes from a stream and returns
    a variant object containing the notes from the list at the offsets
    derived from their original context.

    >>> originStream = stream.Stream()
    >>> data = [('a', 'quarter'), ('b', 'eighth'), ('c', 'eighth'),
    ...    ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'eighth'), ('c', 'eighth'), ('a', 'quarter'), ('a', 'quarter'),
    ...    ('b', 'quarter'), ('c', 'quarter'), ('d', 'quarter'), ('e', 'quarter')]
    >>> for pitchName, durType in data:
    ...    n = note.Note(pitchName)
    ...    n.duration.type = durType
    ...    originStream.append(n)
    >>> noteList = []
    >>> for n in originStream.notes[2:5]:
    ...    noteList.append(n)
    >>> start = originStream.notes[2].offset
    >>> variantName='paris'
    >>> v = variant._generateVariant(noteList, originStream, start, variantName)
    >>> v.show('text')
    {0.0} <music21.note.Note C>
    {0.5} <music21.note.Note A>
    {1.5} <music21.note.Note A>

    >>> v.groups
    ['paris']

    '''
    pass


# ------- Variant Manipulation Methods
def makeAllVariantsReplacements(streamWithVariants,
                                variantNames=None,
                                inPlace=False,
                                recurse=False):
    # noinspection PyShadowingNames,GrazieInspection
    '''
    This function takes a stream and a list of variantNames
    (default works on all variants), and changes all insertion
    (elongations with replacementDuration 0)
    and deletion variants (with containedHighestTime 0) into variants with non-zero
    replacementDuration and non-null elements
    by adding measures on the front of insertions and measures on the end
    of deletions. This is designed to make it possible to format all variants in a
    readable way as a graphical ossia (via lilypond). If inPlace is True
    it will perform this action on the stream itself; otherwise it will return a
    modified copy. If recurse is True, this
    method will work on variants within container objects within the stream (like parts).

    >>> #                                                          *                                            *                                *
    >>> s = converter.parse("tinynotation: 4/4       d4 e4 f4 g4   a2 b-4 a4    g4 a8 g8 f4 e4    d2 a2                        d4 e4 f4 g4    a2 b-4 a4    g4 a8 b-8 c'4 c4    f1")
    >>> s2 = converter.parse("tinynotation: 4/4      d4 e4 f4 g4   a2. b-8 a8   g4 a8 g8 f4 e4    d2 a2   d4 f4 a2  d4 f4 AA2  d4 e4 f4 g4                 g4 a8 b-8 c'4 c4    f1")
    >>> #                                                          replacement                            insertion                            deletion
    >>> s.makeMeasures(inPlace=True)
    >>> s2.makeMeasures(inPlace=True)
    >>> variant.mergeVariants(s, s2, variantName='london', inPlace=True)

    >>> newStream = stream.Score(s)

    >>> returnStream = variant.makeAllVariantsReplacements(newStream, recurse=False)
    >>> for v in returnStream.parts[0][variant.Variant]:
    ...     (v.offset, v.lengthType, v.replacementDuration)
    (4.0, 'replacement', 4.0)
    (16.0, 'elongation', 0.0)
    (20.0, 'deletion', 4.0)

    >>> returnStream = variant.makeAllVariantsReplacements(
    ...                            newStream, variantNames=['france'], recurse=True)
    >>> for v in returnStream.parts[0][variant.Variant]:
    ...     (v.offset, v.lengthType, v.replacementDuration)
    (4.0, 'replacement', 4.0)
    (16.0, 'elongation', 0.0)
    (20.0, 'deletion', 4.0)

    >>> variant.makeAllVariantsReplacements(newStream, recurse=True, inPlace=True)
    >>> for v in newStream.parts[0][variant.Variant]:
    ...     (v.offset, v.lengthType, v.replacementDuration, v.containedHighestTime)
    (4.0, 'replacement', 4.0, 4.0)
    (12.0, 'elongation', 4.0, 12.0)
    (20.0, 'deletion', 8.0, 4.0)

    '''

    if inPlace is True:
        returnStream = streamWithVariants
    else:
        returnStream = copy.deepcopy(streamWithVariants)

    if recurse is True:
        for s in returnStream.recurse(streamsOnly=True):
            _doVariantFixingOnStream(s, variantNames=variantNames)
    else:
        _doVariantFixingOnStream(returnStream, variantNames=variantNames)


    if inPlace is True:
        return
    else:
        return returnStream


def _doVariantFixingOnStream(s, variantNames=None):
    # noinspection PyShadowingNames,GrazieInspection
    '''
    This is a helper function for makeAllVariantsReplacements.
    It iterates through the appropriate variants
    and performs the variant changing operation to eliminate strict deletion and insertion variants.

    >>> #                                           *                           *                                            *                                *                           *
    >>> s = converter.parse("tinynotation: 4/4                    d4 e4 f4 g4   a2 b-4 a4    g4 a8 g8 f4 e4    d2 a2                        d4 e4 f4 g4    a2 b-4 a4    g4 a8 b-8 c'4 c4    f1    ", makeNotation=False)
    >>> s2 = converter.parse("tinynotation: 4/4      a4 b c d     d4 e4 f4 g4   a2. b-8 a8   g4 a8 g8 f4 e4    d2 a2   d4 f4 a2  d4 f4 AA2  d4 e4 f4 g4                 g4 a8 b-8 c'4 c4          ", makeNotation=False)
    >>> #                                        initial insertion              replacement                            insertion                            deletion                        final deletion
    >>> s.makeMeasures(inPlace=True)
    >>> s2.makeMeasures(inPlace=True)
    >>> variant.mergeVariants(s, s2, variantName='london', inPlace=True)

    >>> variant._doVariantFixingOnStream(s, 'london')
    >>> s.show('text')
    {0.0} <music21.variant.Variant object of length 8.0>
    {0.0} <music21.stream.Measure 1 offset=0.0>
    ...
    {4.0} <music21.variant.Variant object of length 4.0>
    {4.0} <music21.stream.Measure 2 offset=4.0>
    ...
    {12.0} <music21.variant.Variant object of length 12.0>
    {12.0} <music21.stream.Measure 4 offset=12.0>
    ...
    {20.0} <music21.variant.Variant object of length 4.0>
    {20.0} <music21.stream.Measure 6 offset=20.0>
    ...
    {24.0} <music21.variant.Variant object of length 4.0>
    {24.0} <music21.stream.Measure 7 offset=24.0>
    ...

    >>> for v in s[variant.Variant]:
    ...     (v.offset, v.lengthType, v.replacementDuration)
    (0.0, 'elongation', 4.0)
    (4.0, 'replacement', 4.0)
    (12.0, 'elongation', 4.0)
    (20.0, 'deletion', 8.0)
    (24.0, 'deletion', 8.0)


    This also works on streams with variants that contain notes and rests rather than measures.

    >>> s = converter.parse('tinyNotation: 4/4                     e4 b b b   f4 f f f   g4 a a a       ', makeNotation=False)
    >>> v1Stream = converter.parse('tinyNotation: 4/4   a4 a a a                                       ', makeNotation=False)
    >>> #                                               initial insertion     deletion
    >>> v1 = variant.Variant(v1Stream.notes)
    >>> v1.replacementDuration = 0.0
    >>> v1.groups = ['london']
    >>> s.insert(0.0, v1)

    >>> v2 = variant.Variant()
    >>> v2.replacementDuration = 4.0
    >>> v2.groups = ['london']
    >>> s.insert(4.0, v2)

    >>> variant._doVariantFixingOnStream(s, 'london')
    >>> for v in s[variant.Variant]:
    ...     (v.offset, v.lengthType, v.replacementDuration, v.containedHighestTime)
    (0.0, 'elongation', 1.0, 5.0)
    (4.0, 'deletion', 5.0, 1.0)
    '''

    for v in s.getElementsByClass(Variant):
        if isinstance(variantNames, list):  # If variantNames are controlled
            if set(v.groups) and not set(variantNames):
                # and if this variant is not in the controlled list
                continue  # then skip it
            else:
                continue  # huh????
        lengthType = v.lengthType
        replacementDuration = v.replacementDuration
        highestTime = v.containedHighestTime

        if lengthType == 'elongation' and replacementDuration == 0.0:
            variantType = 'insertion'
        elif lengthType == 'deletion' and highestTime == 0.0:
            variantType = 'deletion'
        else:
            continue

        if v.getOffsetBySite(s) == 0.0:
            isInitial = True
            isFinal = False
        elif v.getOffsetBySite(s) + v.replacementDuration == s.duration.quarterLength:
            isInitial = False
            isFinal = True
        else:
            isInitial = False
            isFinal = False

        # If a non-final deletion or an INITIAL insertion,
        #  add the next element after the variant.
        if ((variantType == 'insertion' and (isInitial is True))
                or (variantType == 'deletion' and (isFinal is False))):
            targetElement = _getNextElements(s, v)

            # Delete initial clefs, etc. from initial insertion targetElement if it exists
            if isinstance(targetElement, stream.Stream):
                # Must use .elements, because of removal of elements
                for e in targetElement.elements:
                    if isinstance(e, (clef.Clef, meter.TimeSignature)):
                        targetElement.remove(e)

            v.append(copy.deepcopy(targetElement))  # Appends a copy

        # If a non-initial insertion or a FINAL deletion,
        #     add the previous element after the variant.
        # #elif ((variantType == 'deletion' and (isFinal is True)) or
        #         (type == 'insertion' and (isInitial is False))):
        else:
            targetElement = _getPreviousElement(s, v)
            newVariantOffset = targetElement.getOffsetBySite(s)
            # Need to shift elements to make way for new element at front
            offsetShift = targetElement.duration.quarterLength
            for e in v.containedSite:
                oldOffset = e.getOffsetBySite(v.containedSite)
                e.setOffsetBySite(v.containedSite, oldOffset + offsetShift)
            v.insert(0.0, copy.deepcopy(targetElement))
            s.remove(v)
            s.insert(newVariantOffset, v)

            # Give it a new replacementDuration including the added element
        oldReplacementDuration = v.replacementDuration
        v.replacementDuration = oldReplacementDuration + targetElement.duration.quarterLength


def _getNextElements(s, v, numberOfElements=1):
    # noinspection PyShadowingNames, GrazieInspection
    '''
    This is a helper function for makeAllVariantsReplacements() which returns the next element in s
    of the type of elements found in the variant v so that it can be added to v.


    >>> #                                                   *                       *
    >>> s1 = converter.parse('tinyNotation: 4/4             b4 c d e    f4 g a b   d4 e f g   ', makeNotation=False)
    >>> s2 = converter.parse('tinyNotation: 4/4 e4 f g a    b4 c d e               d4 e f g   ', makeNotation=False)
    >>> #                                       insertion               deletion
    >>> s1.makeMeasures(inPlace=True)
    >>> s2.makeMeasures(inPlace=True)
    >>> mergedStream = variant.mergeVariants(s1, s2, 'london')
    >>> for v in mergedStream.getElementsByClass(variant.Variant):
    ...     returnElement = variant._getNextElements(mergedStream, v)
    ...     print(returnElement)
    <music21.stream.Measure 1 offset=0.0>
    <music21.stream.Measure 3 offset=8.0>

    This also works on streams with variants that contain notes and rests rather than measures.

    >>> s = converter.parse('tinyNotation: 4/4                     e4 b b b   f4 f f f   g4 a a a       ', makeNotation=False)
    >>> v1Stream = converter.parse('tinyNotation: 4/4   a4 a a a                                       ', makeNotation=False)
    >>> #                                               initial insertion
    >>> v1 = variant.Variant(v1Stream.notes)
    >>> v1.replacementDuration = 0.0
    >>> v1.groups = ['london']
    >>> s.insert(0.0, v1)

    >>> v2 = variant.Variant()
    >>> v2.replacementDuration = 4.0
    >>> v2.groups = ['london']
    >>> s.insert(4.0, v2)
    >>> for v in s[variant.Variant]:
    ...     returnElement = variant._getNextElements(s, v)
    ...     print(returnElement)
    <music21.note.Note E>
    <music21.note.Note G>
    '''
    replacedElements = v.replacedElements(s)
    lengthType = v.lengthType
    # Get class of elements in variant or replaced Region
    if lengthType == 'elongation':
        vClass = type(v.getElementsByClass(['Measure', 'Note', 'Rest']).first())
        if isinstance(vClass, note.GeneralNote):
            vClass = note.GeneralNote
    else:
        vClass = type(replacedElements.getElementsByClass(['Measure', 'Note', 'Rest']).first())
        if isinstance(vClass, note.GeneralNote):
            vClass = note.GeneralNote

    # Get next element in s after v which is of type vClass
    if lengthType == 'elongation':
        variantOffset = v.getOffsetBySite(s)
        potentialTargets = s.getElementsByOffset(variantOffset,
                                                  offsetEnd=s.highestTime,
                                                  includeEndBoundary=True,
                                                  mustFinishInSpan=False,
                                                  mustBeginInSpan=True,
                                                  classList=[vClass])
        returnElement = potentialTargets.first()

    else:
        replacementDuration = v.replacementDuration
        variantOffset = v.getOffsetBySite(s)
        potentialTargets = s.getElementsByOffset(variantOffset + replacementDuration,
                                                  offsetEnd=s.highestTime,
                                                  includeEndBoundary=True,
                                                  mustFinishInSpan=False,
                                                  mustBeginInSpan=True,
                                                  classList=[vClass])
        returnElement = potentialTargets.first()


    return returnElement


def _getPreviousElement(s, v):
    # noinspection PyShadowingNames,GrazieInspection
    '''
    This is a helper function for makeAllVariantsReplacements() which returns
    the previous element in s
    of the type of elements found in the variant v so that it can be added to v.


    >>> #                                                   *                       *
    >>> s1 = converter.parse('tinyNotation: 4/4 a4 b c d                b4 c d e    f4 g a b    ')
    >>> s2 = converter.parse('tinyNotation: 4/4 a4 b c d    e4 f g a    b4 c d e                ')
    >>> #                                                   insertion               deletion
    >>> s1.makeMeasures(inPlace=True)
    >>> s2.makeMeasures(inPlace=True)
    >>> mergedStream = variant.mergeVariants(s1, s2, 'london')
    >>> for v in mergedStream[variant.Variant]:
    ...     returnElement = variant._getPreviousElement(mergedStream, v)
    ...     print(returnElement)
    <music21.stream.Measure 1 offset=0.0>
    <music21.stream.Measure 2 offset=4.0>

    This also works on streams with variants that contain notes and rests rather than measures.

    >>> s = converter.parse('tinyNotation: 4/4         b4 b b a            e4 b b b      g4 e e e       ', makeNotation=False)
    >>> v1Stream = converter.parse('tinyNotation: 4/4           f4 f f f                                ', makeNotation=False)
    >>> #                                                       insertion                final deletion
    >>> v1 = variant.Variant(v1Stream.notes)
    >>> v1.replacementDuration = 0.0
    >>> v1.groups = ['london']
    >>> s.insert(4.0, v1)

    >>> v2 = variant.Variant()
    >>> v2.replacementDuration = 4.0
    >>> v2.groups = ['london']
    >>> s.insert(8.0, v2)
    >>> for v in s[variant.Variant]:
    ...     returnElement = variant._getPreviousElement(s, v)
    ...     print(returnElement)
    <music21.note.Note A>
    <music21.note.Note B>
    '''

    replacedElements = v.replacedElements(s)
    lengthType = v.lengthType
    # Get class of elements in variant or replaced Region
    foundStream = None
    if lengthType == 'elongation':
        foundStream = v.getElementsByClass(['Measure', 'Note', 'Rest'])
    else:
        foundStream = replacedElements.getElementsByClass(['Measure', 'Note', 'Rest'])

    if not foundStream:
        raise VariantException('Cannot find any Measures, Notes, or Rests in variant')
    vClass = type(foundStream[0])
    if isinstance(vClass, note.GeneralNote):
        vClass = note.GeneralNote

    # Get next element in s after v which is of type vClass
    variantOffset = v.getOffsetBySite(s)
    potentialTargets = s.getElementsByOffset(
        0.0,
        offsetEnd=variantOffset,
        includeEndBoundary=False,
        mustFinishInSpan=False,
        mustBeginInSpan=True,
    ).getElementsByClass(vClass)
    returnElement = potentialTargets.last()

    return returnElement


def makeVariantBlocks(s):
    '''
    Unknown and undocumented.  Used only in lily/translate -- for musicdiff.
    '''
    from music21 import variant
    variantsToBeDone = s.getElementsByClass(variant.Variant)

    for v in variantsToBeDone:
        startOffset = s.elementOffset(v)
        endOffset = v.replacementDuration + startOffset
        conflictingVariants = s.getElementsByOffset(offsetStart=startOffset,
                                                    offsetEnd=endOffset,
                                                    includeEndBoundary=False,
                                                    mustFinishInSpan=False,
                                                    mustBeginInSpan=True,
                                                    classList=[variant.Variant])
        for cV in conflictingVariants:
            oldReplacementDuration = cV.replacementDuration
            if s.elementOffset(cV) == startOffset:
                continue  # do nothing
            else:
                shiftOffset = s.elementOffset(cV) - startOffset
                r = note.Rest()
                r.duration.quarterLength = shiftOffset
                r.style.hideObjectOnPrint = True
                for el in cV._stream:
                    oldOffset = el.getOffsetBySite(cV._stream)
                    cV._stream.coreSetElementOffset(el, oldOffset + shiftOffset)
                cV.coreElementsChanged()
                cV.insert(0.0, r)
                cV.replacementDuration = oldReplacementDuration
                s.remove(cV)
                s.insert(startOffset, cV)
                variantsToBeDone.append(cV)


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def pitchOut(self, listIn):
        pass

    def testBasicA(self):
        pass


    def testBasicB(self):
        '''
        Testing relaying attributes requests to private Stream with __getattr__
        '''
        pass


    def testVariantGroupA(self):
        '''
        Variant groups are used to distinguish
        '''
        pass


    def testVariantClassA(self):
        pass

    def testDeepCopyVariantA(self):
        pass

    def testDeepCopyVariantB(self):
        pass


class TestExternal(unittest.TestCase):
    show = True

    def testMergeJacopoVariants(self):
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , TestExternal)
