# ------------------------------------------------------------------------------
# Name:         reduction.py
# Purpose:      Tools for creating a score reduction.
#
# Authors:      Christopher Ariza
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011-2013 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
Tools for generation reduction displays, showing a score and or a chord reduction,
and one or more reductive representation lines.

Used by graph.PlotHorizontalBarWeighted()
'''
from __future__ import annotations

import copy
import re
import typing as t
import unittest

from music21 import exceptions21

from music21 import chord
from music21 import common
from music21.common.types import DocOrder
from music21 import environment
from music21 import expressions
from music21 import instrument
from music21 import note
from music21 import pitch
from music21 import prebase
from music21 import stream

environLocal = environment.Environment('analysis.reduction')


# ------------------------------------------------------------------------------
class ReductiveEventException(exceptions21.Music21Exception):
    pass


# as lyric, or as parameter
#
# ::/p:g#/o:5/nh:f/ns:n/l:1/g:ursatz/v:1


class ReductiveNote(prebase.ProtoM21Object):
    '''
    The extraction of an event from a score and specification of where
    and how it should be presented in a reductive score.

    A specification string, as well as Note, must be provided for parsing.

    A specification must be created when access the Measure that the source note
    is found in. Storing the measure and index position provides significant
    performance optimization, as we do no have to search
    every note when generated the reduction.

    The `measureIndex` is the index of measure where this is found, not
    the measure number. The `measureOffset` is the position in the measure
    specified by the index.
    '''
    _delimitValue = ':'  # store the delimiter string, must start with 2
    _delimitArg = '/'
    # map the abbreviation to the data key
    _parameterKeys = {
        'p': 'pitch',
        'o': 'octave',
        'nf': 'noteheadFill',
        'sd': 'stemDirection',
        'g': 'group',
        'v': 'voice',
        'ta': 'textAbove',  # text annotation
        'tb': 'textBelow',  # text annotation
    }
    _defaultParameters = {
        'pitch': None,  # use notes, or if a chord take highest
        'octave': None,  # use notes
        'noteheadFill': None,  # use notes
        'stemDirection': 'noStem',
        'group': None,
        'voice': None,
    }

    def __init__(self, specification, inputNote, measureIndex, measureOffset):
        self._specification = specification

        self._note = None  # store a reference to the note this is attached to
        self._parameters = {}
        # do parsing if possible
        self._isParsed = False
        self._parseSpecification(self._specification)
        self._note = inputNote  # keep a reference
        self.measureIndex = measureIndex
        self.measureOffset = measureOffset

    def _reprInternal(self):
        pass

    def __getitem__(self, key):
        return self._parameters[key]

    def _parseSpecification(self, spec: str):
        # start with the defaults
        pass

    def isParsed(self) -> bool:
        pass

    def getNoteAndTextExpression(self):
        '''
        Produce a new note, a deep copy of the supplied note
        and with the specified modifications.
        '''
        pass


# ------------------------------------------------------------------------------
class ScoreReductionException(exceptions21.Music21Exception):
    pass


class ScoreReduction:
    '''
    An object to reduce a score.
    '''
    def __init__(self, **keywords):
        # store a list of one or more reductions
        self._reductiveNotes = {}
        self._reductiveVoices = []
        self._reductiveGroups = []

        # store the source score
        self._score = None
        self._chordReduction = None  # store a chordal reduction of available


    def _setScore(self, value):
        pass

    def _getScore(self):
        pass

    score = property(_getScore, _setScore, doc='''
        Get or set the Score. Setting the score set a deepcopy of the score; the score
        set here will not be altered.

        >>> s = corpus.parse('bwv66.6')
        >>> sr = analysis.reduction.ScoreReduction()
        >>> sr.score = s
        ''')


    def _setChordReduction(self, value):
        pass

    def _getChordReduction(self):
        pass

    chordReduction = property(_getChordReduction, _setChordReduction, doc='''
        Get or set a Chord reduction as a Stream or Score. Setting the this values
        set a deepcopy of the reduction; the reduction set here will not be altered.
        ''')



    def _extractReductionEvents(self, score, removeAfterParsing=True):
        '''
        Remove and store all reductive events
        Store in a dictionary where obj id is obj key
        '''
        pass

    def _extractNoteReductiveEvent(self, n, infoDict=None, removeAfterParsing=True):
        pass


    def _parseReductiveNotes(self):
        pass


    def _createReduction(self):
        pass

    def reduce(self):
        '''
        Given a score, populate this Score reduction
        '''
        pass



# ------------------------------------------------------------------------------
class PartReductionException(exceptions21.Music21Exception):
    pass

# ------------------------------------------------------------------------------
class PartReduction:
    '''
    A part reduction reduces a Score into one or more parts.
    Parts are combined based on a part group dictionary.
    Each resulting part is then segmented by an object.
    This object is assigned as floating-point value.

    This reduction is designed to work with the GraphHorizontalBarWeighted and related Plot
    subclasses.

    If the `fillByMeasure` parameter is True, and if measures are available,
    each part will segment by Measure divisions, and look for the target activity only
    once per Measure.

    If more than one target is found in the Measure, values will be averaged.

    If `fillByMeasure` is False, the part will be segmented by each Note.

    The `segmentByTarget` parameter is True, segments, which may be Notes or Measures,
    will be divided if necessary to show changes that occur over the duration of the
    segment by a target object.

    If the `normalizeByPart` parameter is True, each part will be normalized within
    the range only of that part. If False, all parts will be normalized by the max
    of all parts. The default is True.

    If the `normalize` parameter is False, no normalization will take place. The default is True.

    '''
    def __init__(self,
                 srcScore=None,
                 *,
                 partGroups: list[dict[str, t.Any]]|None = None,
                 fillByMeasure: bool = True,
                 segmentByTarget: bool = True,
                 normalize: bool = True,
                 normalizeByPart: bool = False,
                 **keywords):
        if srcScore is None:
            return
        if not isinstance(srcScore, stream.Score):
            raise PartReductionException('provided Stream must be Score')
        self._score = srcScore
        # an ordered list of dictionaries for
        # part id, part color, and a list of Part objs
        # TODO: typed dict
        self._partBundles: list[dict[str, t.Any]] = []
        # a dictionary of part id to a list of events
        self._eventSpans: dict[str|int, list[t.Any]] = {}

        # define how parts are grouped
        # a list of dictionaries, with keys for name, color, and a match list
        self._partGroups = partGroups

        self._fillByMeasure = fillByMeasure

        # We re-partition if the spans change
        self._segmentByTarget = segmentByTarget
        self._normalizeByPart = normalizeByPart  # norm by all parts is default
        self._normalizeToggle = normalize

        # check that there are measures
        for p in self._score.parts:
            if not p.hasMeasures():
                self._fillByMeasure = False
                # environLocal.printDebug(['overriding fillByMeasure as no measures are defined'])
                break

    def _createPartBundles(self):
        '''
        Fill the _partBundles list with dictionaries,
        each dictionary defining a name (part id or supplied), a color, and list
        of Parts that match.
        '''
        self._partBundles = []
        if self._partGroups:
            for d in self._partGroups:  # a list of dictionaries
                name, pColor, matches = d['name'], d['color'], d['match']
                sub = []
                for p in self._score.parts:
                    # environLocal.printDebug(['_createPartBundles: part.id', p.id])
                    # if matches is None, use group name
                    if matches is None:
                        matches = [name]
                    pId = str(p.id).lower()
                    for m in matches:  # strings or instruments
                        if (isinstance(m, str)
                                and pId.find(m.lower()) >= 0):
                            sub.append(p)
                            break
                        elif re.match(m.lower(), pId):
                            sub.append(p)
                        # TODO: match if m is Instrument class
                if not sub:
                    continue
                data = {
                    'pGroupId': name,
                    'color': pColor,
                    'parts': sub,
                }
                self._partBundles.append(data)
        else:  # manually creates
            for p in self._score.parts:
                # store one or more Parts associated with an id
                data = {'pGroupId': p.id, 'color': '#666666', 'parts': [p]}
                self._partBundles.append(data)

        # create flat representation of all parts in a bundle
        for partBundle in self._partBundles:
            if len(partBundle['parts']) == 1:
                partBundle['parts.flat'] = partBundle['parts'][0].flatten()
            else:
                # align all parts and flatten
                # this takes a flat presentation of all parts
                s = stream.Stream()
                for p in partBundle['parts']:
                    s.insert(0, p)
                partBundle['parts.flat'] = s.flatten()


    def _createEventSpans(self):
        # for each part group id key, store a list of events
        self._eventSpans = {}

        for partBundle in self._partBundles:
            pGroupId = partBundle['pGroupId']
            pColor = partBundle['color']
            parts = partBundle['parts']
            # print(pGroupId)
            dataEvents = []
            # combine multiple streams into a single
            eStart = None
            eEnd = None
            eLast = None

            # segmenting by measure if that measure contains notes.
            # Note that measures are not elided of activity is contiguous
            if self._fillByMeasure:
                partMeasures = []
                for p in parts:
                    partMeasures.append(p.getElementsByClass(stream.Measure).stream())
                # environLocal.printDebug(['partMeasures', partMeasures])
                # assuming that all parts have same the number of measures
                # iterate over each measure
                # iLast = len(partMeasures[0]) - 1
                for i in range(len(partMeasures[0])):
                    active = False
                    # check for activity in any part in the part group
                    for p in partMeasures:  # iter of parts containing measures
                        # print(p, i, p[i], len(p[i].flatten().notes))
                        if p[i].iter().notes:
                            active = True
                            break
                    # environLocal.printDebug([i, 'active', active])
                    if not active:
                        continue
                    # get offset, or start, of this measure
                    e = partMeasures[0][i]
                    eStart = e.getOffsetBySite(partMeasures[0])
                    # use duration, not barDuration.quarterLength
                    # as want filled duration?
                    eEnd = (eStart + e.barDuration.quarterLength)
                    ds = {'eStart': eStart,
                          'span': eEnd - eStart,
                          'weight': None,
                          'color': pColor,
                          }
                    dataEvents.append(ds)

                    # if eStart is None and active:
                    #     eStart = partMeasures[0][i].getOffsetBySite(
                    #              partMeasures[0])
                    # elif (eStart is not None and not active) or i >= iLast:
                    #     if eStart is None:  # nothing to do; just the last
                    #         continue
                    #     # if this is the last measure, and it is active
                    #     if (i >= iLast and active):
                    #         eLast = partMeasures[0][i]
                    #     # use duration, not barDuration.quarterLength
                    #     # as want filled duration?
                    #     eEnd = (eLast.getOffsetBySite(
                    #             partMeasures[0]) +
                    #             eLast.barDuration.quarterLength)
                    #     ds = {'eStart':eStart, 'span':eEnd-eStart,
                    #           'weight':None, 'color':pColor}
                    #     dataEvents.append(ds)
                    #     eStart = None
#                    eLast = partMeasures[0][i]

            # fill by alternative approach, based on activity of notes
            # creates region for each contiguous span of notes
            # this is useful as it will handle overlaps and similar arrangements
            # TODO: this needs further testing
            else:
                # this takes a flat presentation of all parts, and then
                # finds any gaps in consecutive notes
                eSrc = partBundle['parts.flat']
                # a li=st, not a stream
                # a None in the resulting list designates a rest
                noteSrc = eSrc.findConsecutiveNotes()
                for i, e in enumerate(noteSrc):
                    # environLocal.printDebug(['i, e', i, e])
                    # if this event is a rest, e is None
                    if e is None:
                        if eStart is None:  # the first event is a rest
                            continue
                        else:
                            eEnd = eLast.getOffsetBySite(eSrc) + eLast.quarterLength
                        # create a temporary weight
                        ds = {'eStart': eStart,
                              'span': eEnd - eStart,
                              'weight': None,
                              'color': pColor,
                              }
                        dataEvents.append(ds)
                        eStart = None
                    elif i >= len(noteSrc) - 1:  # this is the last
                        if eStart is None:  # the last event was a rest
                            # this the start is the start of this event
                            eStart = e.getOffsetBySite(eSrc)
                        eEnd = e.getOffsetBySite(eSrc) + e.quarterLength
                        # create a temporary weight
                        ds = {'eStart': eStart,
                              'span': eEnd - eStart,
                              'weight': None,
                              'color': pColor,
                              }
                        dataEvents.append(ds)
                        eStart = None
                    else:
                        if eStart is None:
                            eStart = e.getOffsetBySite(eSrc)
                        eLast = e
            # environLocal.printDebug(['dataEvents', dataEvents])
            self._eventSpans[pGroupId] = dataEvents


    def _getValueForSpan(
        self,
        target='Dynamic',
        splitSpans=True,
        targetToWeight=None
    ):
        '''
        For each span, determine the measured parameter value. This is translated
        as the height of the bar graph.

        If `splitSpans` is True, a span will be split of the target changes over the span.
        Otherwise, Spans will be averaged. This is the `segmentByTarget` parameter.

        The `targetToWeight` parameter is a function that takes a list or Stream of objects
        (of the class specified by `target`) and returns a single floating-point value.
        '''
        # this temporary function only works with dynamics
        def _dynamicToWeight(targets):
            # permit a stream
            pass

        # supply function to convert one or more targets to number
        if targetToWeight is None:
            targetToWeight = _dynamicToWeight

        if not splitSpans:  # this is segmentByTarget
            for partBundle in self._partBundles:
                flatRef = partBundle['parts.flat']
                for ds in self._eventSpans[partBundle['pGroupId']]:
                    # for each event span, find the targeted object
                    offsetStart = ds['eStart']
                    offsetEnd = offsetStart + ds['span']
                    match = flatRef.getElementsByOffset(
                        offsetStart,
                        offsetEnd,
                        includeEndBoundary=False,
                        mustFinishInSpan=False,
                        mustBeginInSpan=True
                    ).getElementsByClass(target).stream()
                    if not match:
                        w = None
                    else:
                        w = targetToWeight(match)
                    # environLocal.printDebug(['segment weight', w])
                    ds['weight'] = w
        else:
            for partBundle in self._partBundles:
                finalBundle = []
                flatRef = partBundle['parts.flat']
                # get each span
                for ds in self._eventSpans[partBundle['pGroupId']]:
                    offsetStart = ds['eStart']
                    offsetEnd = offsetStart + ds['span']
                    # get all targets within the contiguous region
                    # e.g., Dynamics objects
                    match = flatRef.getElementsByOffset(offsetStart, offsetEnd,
                        includeEndBoundary=True, mustFinishInSpan=False,
                        mustBeginInSpan=True).getElementsByClass(target).stream()
                    # environLocal.printDebug(['matched elements', target, match])
                    # extend duration of all found dynamics
                    match.extendDuration(target, inPlace=True)
                    # match.show('t')
                    dsFirst = copy.deepcopy(ds)
                    if not match:
                        # weight is not known
                        finalBundle.append(dsFirst)
                        continue
                    # create new spans for each target in this segment
                    for i, tar in enumerate(match):
                        targetStart = tar.getOffsetBySite(flatRef)
                        # can use extended duration
                        targetSpan = tar.duration.quarterLength
                        # if dur of target is greater tn this span
                        # end at this span
                        if targetStart + targetSpan > offsetEnd:
                            targetSpan = offsetEnd - targetStart
                        # if we have the last matched target, it will
                        # have zero duration, as there is no following
                        # thus, span needs to be distance to end of regions
                        if targetSpan <= 0.001:
                            targetSpan = offsetEnd - targetStart
                        # environLocal.printDebug([t, 'targetSpan', targetSpan,
                        #  'offsetEnd', offsetEnd, "ds['span']", ds['span']])

                        if i == 0 and ds['eStart'] == targetStart:
                            # the target start at the same position
                            # as the start of this existing span
                            # dsFirst['eStart'] = targetStart
                            dsFirst['span'] = targetSpan
                            dsFirst['weight'] = targetToWeight(tar)
                            finalBundle.append(dsFirst)
                        elif t == 0 and ds['eStart'] != targetStart:
                            # add two, one for the empty region, one for target
                            # adjust span of first; weight is not known
                            # (hangs over from last)
                            dsFirst['span'] = targetStart - offsetStart
                            finalBundle.append(dsFirst)
                            dsNext = copy.deepcopy(ds)
                            dsNext['eStart'] = targetStart
                            dsNext['span'] = targetSpan
                            dsNext['weight'] = targetToWeight(tar)
                            finalBundle.append(dsNext)
                        else:  # for all other cases, create segment for each
                            dsNext = copy.deepcopy(ds)
                            dsNext['eStart'] = targetStart
                            dsNext['span'] = targetSpan
                            dsNext['weight'] = targetToWeight(tar)
                            finalBundle.append(dsNext)
                # after iterating all ds spans, reassign
                self._eventSpans[partBundle['pGroupId']] = finalBundle

    def _extendSpans(self):
        '''
        Extend the value of a target parameter to the next boundary.
        An undefined boundary will wave as its weight None.
        '''
        # environLocal.printDebug(['_extendSpans: pre'])
        # for partBundle in self._partBundles:
        #     for i, ds in enumerate(self._eventSpans[partBundle['pGroupId']]):
        #         print(ds)

        minValue = 0.01  # for error conditions
        for partBundle in self._partBundles:
            lastWeight = None
            for i, ds in enumerate(self._eventSpans[partBundle['pGroupId']]):
                if i == 0:  # cannot extend first
                    if ds['weight'] is None:  # this is an error in the rep
                        ds['weight'] = minValue
                        # environLocal.printDebug([
                        #  'cannot extend a weight: no previous weight defined'])
                    else:
                        lastWeight = ds['weight']
                else:  # not first
                    if ds['weight']:
                        lastWeight = ds['weight']
                    elif lastWeight:  # its None, use last
                        ds['weight'] = lastWeight
                    # do not have a list; mist set to min
                    elif ds['weight'] is None and lastWeight is None:
                        ds['weight'] = minValue
                        # environLocal.printDebug([
                        #  'cannot extend a weight: no previous weight defined'])
#         environLocal.printDebug(['_extendSpans: post'])
#         for partBundle in self._partBundles:
#             for i, ds in enumerate(self._eventSpans[partBundle['pGroupId']]):
#                 print(ds)

    def _normalize(self, byPart=False):
        '''
        Normalize, either within each Part, or for all parts
        '''
        partMaxRef = {}
        for partBundle in self._partBundles:
            partMax = 0
            for ds in self._eventSpans[partBundle['pGroupId']]:
                if ds['weight'] > partMax:
                    partMax = ds['weight']
            partMaxRef[partBundle['pGroupId']] = partMax

        try:
            maxOfMax = max(partMaxRef.values())
        except ValueError:  # empty part?
            maxOfMax = 0

        for partBundle in self._partBundles:
            for ds in self._eventSpans[partBundle['pGroupId']]:
                # weight is now fraction of the max for that part
                if byPart:
                    bestMax = partMaxRef[partBundle['pGroupId']]
                else:
                    bestMax = maxOfMax
                if bestMax != 0:
                    ds['weight'] = (ds['weight'] / bestMax)
                else:
                    ds['weight'] = 1  # error?

    def process(self):
        '''
        Core processing routines.
        '''
        self._createPartBundles()
        self._createEventSpans()
        self._getValueForSpan(splitSpans=self._segmentByTarget)
        self._extendSpans()
        if self._normalizeToggle:
            self._normalize(byPart=self._normalizeByPart)



    def getGraphHorizontalBarWeightedData(self):
        '''
        Get all data organized into bar span specifications.
        '''
        # data =  [
        #  ('Violins',  [(3, 5, 1, '#fff000'), (1, 12, 0.2, '#3ff203', 0.1, 1)]  ),
        #  ('Celli',    [(2, 7, 0.2, '#0ff302'), (10, 3, 0.6, '#ff0000', 1)]  ),
        #  ]
        data = []
        # iterate over part bundles to get order
        for partBundle in self._partBundles:
            # print(partBundle)
            dataList = []
            groupSpans = partBundle['pGroupId']
            for ds in self._eventSpans[groupSpans]:
                # data format here is set by the graphing routine
                dataList.append([ds['eStart'], ds['span'], ds['weight'], ds['color']])
            data.append((partBundle['pGroupId'], dataList))
        return data

# ------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def testExtractionA(self):
        pass


    def testExtractionB(self):
        pass
        # post.show()

    # def testExtractionC(self):
    #     from music21 import analysis
    #     from music21 import corpus
    #     # http://solomonsmusic.net/schenker.htm
    #     # shows extracting an Ursatz line
    #
    #     # BACH pre;ide !, WTC
    #
    #     src = corpus.parse('bwv846')
    #     import warnings
    #     with warnings.catch_warnings():  # catch deprecation warning
    #         warnings.simplefilter('ignore', category=exceptions21.Music21DeprecationWarning)
    #         chords = src.flatten().makeChords(minimumWindowSize=4,  # make chords is gone
    #                                     makeRests=False)
    #     for c in chords.flatten().notes:
    #         c.quarterLength = 4
    #     for m in chords.getElementsByClass(stream.Measure):
    #         m.clef = clef.bestClef(m, recurse=True)
    #
    #     chords.measure(1).notes[0].addLyric('::/p:e/o:5/nf:no/ta:3/g:Ursatz')
    #     chords.measure(1).notes[0].addLyric('::/p:c/o:4/nf:no/tb:I')
    #
    #     chords.measure(24).notes[0].addLyric('::/p:d/o:5/nf:no/ta:2')
    #     chords.measure(24).notes[0].addLyric('::/p:g/o:3/nf:no/tb:V')
    #
    #     chords.measure(30).notes[0].addLyric('::/p:f/o:4/tb:7')
    #
    #     chords.measure(34).notes[0].addLyric('::/p:c/o:5/nf:no/v:1/ta:1')
    #     chords.measure(34).notes[0].addLyric('::/p:g/o:4/nf:no/v:2')
    #     chords.measure(34).notes[0].addLyric('::/p:c/o:4/nf:no/v:1/tb:I')
    #
    #     sr = analysis.reduction.ScoreReduction()
    #     sr.chordReduction = chords
    #     # sr.score = src
    #     unused_post = sr.reduce()
    #     # unused_post.show()


    def testExtractionD(self):
        # this shows a score, extracting a single pitch
        pass
        # post.show()

    def testExtractionD2(self):
        # this shows a score, extracting a single pitch
        pass
        # post.show()

    def testExtractionE(self):
        pass
        # post.show()

    def testPartReductionA(self):
        pass


    def _matchWeightedData(self, match, target):
        '''
        Utility function to compare known data but not compare floating point weights.
        '''
        pass

    def testPartReductionB(self, show=False):
        '''
        Artificially create test cases.
        '''
        pass


    def testPartReductionC(self):
        '''
        Artificially create test cases.
        '''
        pass


    def testPartReductionD(self):
        '''
        Artificially create test cases. Here, uses rests.
        '''
        pass
        # p = graph.PlotDolan(s, title='Dynamics')
        # p.process()


    def testPartReductionE(self):
        '''
        Artificially create test cases.
        '''
        pass
        # p = graph.PlotDolan(s, title='Dynamics', fillByMeasure=False,
        #                     segmentByTarget=True, normalizeByPart=False)
        # p.process()

    def xtestPartReductionSchoenberg(self):
        pass


class TestExternal(unittest.TestCase):
    show = True

    def testPartReductionB(self):
        pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER: DocOrder = []


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , runTest='testPartReductionSchoenberg')
