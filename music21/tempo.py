# ------------------------------------------------------------------------------
# Name:         tempo.py
# Purpose:      Classes and tools relating to tempo
#
# Authors:      Christopher Ariza
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2009-22 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
This module defines objects for describing tempo and changes in tempo.
'''
from __future__ import annotations

import copy
import typing as t
import unittest

from music21 import base
from music21 import common
from music21 import duration
from music21 import environment
from music21 import exceptions21
from music21 import expressions
from music21 import note
from music21 import spanner
from music21 import style

if t.TYPE_CHECKING:
    from music21.common.types import OffsetQLIn


environLocal = environment.Environment('tempo')


# all lowercase, even german, for string comparison
defaultTempoValues = {
    'larghissimo': 16,
    'largamente': 32,
    'grave': 40,
    'molto adagio': 40,
    'largo': 46,
    'lento': 52,
    'adagio': 56,
    'slow': 56,
    'langsam': 56,
    'larghetto': 60,
    'adagietto': 66,
    'andante': 72,
    'andantino': 80,
    'andante moderato': 83,  # need number
    'maestoso': 88,
    'moderato': 92,
    'moderate': 92,
    'allegretto': 108,
    'animato': 120,
    'allegro moderato': 128,  # need number
    'allegro': 132,
    'fast': 132,
    'schnell': 132,
    'allegrissimo': 140,  # need number
    'molto allegro': 144,
    'très vite': 144,
    'vivace': 160,
    'vivacissimo': 168,
    'presto': 184,
    'prestissimo': 208,
}


def convertTempoByReferent(
    numberSrc: int|float,
    quarterLengthBeatSrc: int|float,
    quarterLengthBeatDst=1.0
) -> float:
    '''
    Convert between equivalent tempi, where the speed stays the
    same but the beat referent and number change.

    60 bpm at quarter, going to half

    >>> tempo.convertTempoByReferent(60, 1, 2)
    30.0

    60 bpm at quarter, going to 16th

    >>> tempo.convertTempoByReferent(60, 1, 0.25)
    240.0

    60 at dotted quarter, get quarter

    >>> tempo.convertTempoByReferent(60, 1.5, 1)
    90.0

    60 at dotted quarter, get half

    >>> tempo.convertTempoByReferent(60, 1.5, 2)
    45.0

    60 at dotted quarter, get trip

    >>> tempo.convertTempoByReferent(60, 1.5, 1/3)
    270.0

    A Fraction instance can also be used:

    >>> tempo.convertTempoByReferent(60, 1.5, common.opFrac(1/3))
    270.0

    '''
    # find duration in seconds of quarter length
    srcDurPerBeat = 60 / numberSrc
    # convert to dur for one quarter length
    dur = srcDurPerBeat / quarterLengthBeatSrc
    # multiply dur by dst quarter
    dstDurPerBeat = dur * float(quarterLengthBeatDst)
    # environLocal.printDebug(['dur', dur, 'dstDurPerBeat', dstDurPerBeat])
    # find tempo
    return float(60 / dstDurPerBeat)


# ------------------------------------------------------------------------------
class TempoException(exceptions21.Music21Exception):
    pass


# ------------------------------------------------------------------------------
class TempoIndication(base.Music21Object):
    '''
    A generic base class for all tempo indications to inherit.
    Can be used to filter out all types of tempo indications.
    '''
    classSortOrder = 1
    _styleClass = style.TextStyle

    # def __init__(self, **keywords):
    #     super().__init__(**keywords)
    #     # self.style.justify = 'left'  # creates a style object to share.

    def getSoundingMetronomeMark(self, found=None):
        '''
        Get the appropriate MetronomeMark from any sort of TempoIndication, regardless of class.
        '''
        if found is None:
            found = self

        if isinstance(found, MetricModulation):
            return found.newMetronome
        elif isinstance(found, MetronomeMark):
            return found
        elif 'TempoText' in found.classes:
            return found.getMetronomeMark()
        else:
            raise TempoException(
                f'cannot derive a MetronomeMark from this TempoIndication: {found}')

    def getPreviousMetronomeMark(self):
        '''
        Do activeSite and context searches to try to find the last relevant
        MetronomeMark or MetricModulation object. If a MetricModulation mark is found,
        return the new MetronomeMark, or the last relevant.

        >>> s = stream.Stream()
        >>> s.insert(0, tempo.MetronomeMark(number=120))
        >>> mm1 = tempo.MetronomeMark(number=90)
        >>> s.insert(20, mm1)
        >>> mm1.getPreviousMetronomeMark()
        <music21.tempo.MetronomeMark animato Quarter=120>
        '''
        pass


# ------------------------------------------------------------------------------
class TempoText(TempoIndication):
    '''
    >>> import music21
    >>> tm = music21.tempo.TempoText('adagio')
    >>> tm
    <music21.tempo.TempoText 'adagio'>
    >>> print(tm.text)
    adagio
    '''
    def __init__(self, text=None, **keywords):
        super().__init__(**keywords)

        # store text in a TextExpression instance
        self._textExpression = None  # a stored object

        if text is not None:
            self.text = str(text)

    def _reprInternal(self):
        pass

    def _getText(self):
        '''
        Get the text used for this expression.
        '''
        pass

    def _setText(self, value):
        '''
        Set the text of this repeat expression. This is also the primary way
        that the stored TextExpression object is created.
        '''
        pass

    text = property(_getText, _setText, doc='''
        Get or set the text as a string.

        >>> import music21
        >>> tm = music21.tempo.TempoText('adagio')
        >>> tm.text
        'adagio'
        >>> tm.getTextExpression()
        <music21.expressions.TextExpression 'adagio'>
        ''')

    def getMetronomeMark(self):
        # noinspection PyShadowingNames
        '''
        Return a MetronomeMark object that is configured from this objects Text.

        >>> tt = tempo.TempoText('slow')
        >>> mm = tt.getMetronomeMark()
        >>> mm.number
        56
        '''
        mm = MetronomeMark(text=self.text)
        if self.hasStyleInformation:
            mm.style = self.style
        else:
            self.style = mm.style
        return mm

    def getTextExpression(self, numberImplicit=False):
        '''
        Return a TextExpression object for this text.

        What is this a deepcopy and not the actual one?
        '''
        pass

    def setTextExpression(self, value):
        '''
        Given a TextExpression, set it in this object.
        '''
        pass

    def applyTextFormatting(self, te=None, numberImplicit=False):
        '''
        Apply the default text formatting to the text expression version of this tempo mark
        '''
        pass

    def isCommonTempoText(self, value=None):
        '''
        Return True or False if the supplied text seems like a
        plausible Tempo indications be used for this TempoText.

        >>> tt = tempo.TempoText('adagio')
        >>> tt.isCommonTempoText()
        True

        >>> tt = tempo.TempoText('Largo e piano')
        >>> tt.isCommonTempoText()
        True

        >>> tt = tempo.TempoText('undulating')
        >>> tt.isCommonTempoText()
        False
        '''
        def stripText(s):
            # remove all spaces, punctuation, and make lower
            s = s.strip()
            s = s.replace(' ', '')
            s = s.replace('.', '')
            s = s.lower()
            return s
        # if not provided, use stored text
        if value is None:
            value = self._textExpression.content

        for candidate in defaultTempoValues:
            candidate = stripText(candidate)
            value = stripText(value)
            # simply look for membership, not a complete match
            if value in candidate or candidate in value:
                return True
        return False


# ------------------------------------------------------------------------------
class MetronomeMarkException(TempoException):
    pass


# TODO: define if tempo applies only to part
# ------------------------------------------------------------------------------
class MetronomeMark(TempoIndication):
    '''
    A way of specifying a particular tempo with a text string,
    a referent (a duration) and a number.

    The `referent` attribute is a Duration object, or a string duration type or
    a floating-point quarter-length value used to create a Duration.

    MetronomeMarks, as Music21Object subclasses, also have .duration object
    property independent of the `referent`.

    >>> a = tempo.MetronomeMark('slow', 40, note.Note(type='half'))
    >>> a.number
    40
    >>> a.referent
    <music21.duration.Duration 2.0>
    >>> a.referent.type
    'half'
    >>> print(a.text)
    slow


    Some text marks will automatically suggest a number.

    >>> mm = tempo.MetronomeMark('adagio')
    >>> mm.number
    56
    >>> mm.numberImplicit
    True

    For certain numbers, a text value can be set implicitly

    >>> tm2 = tempo.MetronomeMark(number=208)
    >>> print(tm2.text)
    prestissimo
    >>> tm2.referent
    <music21.duration.Duration 1.0>

    Unicode values work fine thanks to Python 3:

    >>> marking = 'très vite'
    >>> marking
    'très vite'
    >>> print(tempo.defaultTempoValues[marking])
    144
    >>> tm2 = tempo.MetronomeMark(marking)
    >>> tm2.text.endswith('vite')
    True
    >>> tm2.number
    144

    For playback only (no score output) set numberSounding but no number:

    >>> fast = tempo.MetronomeMark(numberSounding=168)
    >>> fast
    <music21.tempo.MetronomeMark Quarter=168 (playback only)>
    '''
    _DOC_ATTR: dict[str, str] = {
        'placement': '''
            Staff placement: 'above', 'below', or None.

            A setting of None implies that the placement will be determined
            by notation software and no particular placement is demanded.

            This is not placed in the `.style` property, since for some expressions,
            the placement above or below an object has semantic
            meaning and is not purely presentational.
            ''',
    }

    def __init__(
        self,
        text: str|int|None = None,
        number: OffsetQLIn|None = None,
        referent: OffsetQLIn|str|duration.Duration|base.Music21Object|None = None,
        *,
        parentheses: bool = False,
        playbackOnly: bool = False,
        numberSounding: OffsetQLIn|None = None,
        numberImplicit: bool|None = None,
        **keywords
    ) -> None:
        super().__init__(**keywords)

        if number is None and isinstance(text, int):
            number = text
            text = None

        self._number: int|float|None = (
            common.numToIntOrFloat(number) if number is not None else None
        )
        self.numberImplicit = None
        if numberImplicit is not None:
            self.numberImplicit = numberImplicit
        elif self._number is not None:
            self.numberImplicit = False

        self._tempoText = None  # set with property text
        self.textImplicit = None
        if text is not None:  # use property to create object if necessary
            self.text = text

        # TODO: style??
        self.parentheses: bool = parentheses
        self.placement = None

        self._referent = None  # set with property
        if referent is None:
            # if referent is None, set a default quarter note duration
            referent = duration.Duration(type='quarter')
        self.referent = referent  # use property

        # set implicit values if necessary
        self._updateNumberFromText()
        self._updateTextFromNumber()

        # need to store a sounding value for the case where
        # a sounding different is different from the number given in the MM
        self._numberSounding = numberSounding

    def _reprInternal(self):
        pass

    def _updateTextFromNumber(self):
        '''
        Update text if number is given and text is not defined
        '''
        pass

    def _updateNumberFromText(self):
        '''
        Update number if text is given and number is not defined
        '''
        pass

    # -------------------------------------------------------------------------
    def _getReferent(self):
        pass

    def _setReferent(self, value):
        pass

    referent = property(_getReferent, _setReferent, doc='''
        Get or set the referent, or the Duration object that is the
        reference for the tempo value in BPM.
        ''')

    # properties and conversions
    def _getText(self):
        pass

    def _setText(self, value, updateNumberFromText=True):
        pass

    text = property(_getText, _setText, doc='''
        Get or set a text string for this MetronomeMark. Internally implemented as a
        :class:`~music21.tempo.TempoText` object, which stores the text in
        a :class:`~music21.expression.TextExpression` object.

        >>> mm = tempo.MetronomeMark(number=123)
        >>> mm.text == None
        True
        >>> mm.text = 'medium fast'
        >>> print(mm.text)
        medium fast
        ''')

    def _getNumber(self) -> int|float|None:
        pass

    def _setNumber(self, value: int|float|None,
                   updateTextFromNumber=True):
        # do not replace with a @property since _setNumber has an
        # optional second attribute.
        pass

    number = property(_getNumber, _setNumber, doc='''
        Get and set the number, or the numerical value of the Metronome.

        >>> mm = tempo.MetronomeMark('slow')
        >>> mm.number
        56
        >>> mm.numberImplicit
        True
        >>> mm.number = 52.5
        >>> mm.number
        52.5
        >>> mm.numberImplicit
        False
        ''')

    def _getNumberSounding(self):
        pass

    def _setNumberSounding(self, value):
        pass

    numberSounding = property(_getNumberSounding, _setNumberSounding, doc='''
        Get and set the numberSounding, or the numerical value of the Metronome that
        is used for playback independent of display. If numberSounding is None, number is
        assumed to be numberSounding.

        >>> mm = tempo.MetronomeMark('slow')
        >>> mm.number
        56
        >>> mm.numberImplicit
        True
        >>> mm.numberSounding is None
        True
        >>> mm.numberSounding = 120
        >>> mm.numberSounding
        120
        ''')

    # -------------------------------------------------------------------------
    def getQuarterBPM(self, useNumberSounding=True) -> float|None:
        '''
        Get a BPM value where the beat is a quarter; must convert from the
        defined beat to a quarter beat. Will return None if no beat number is defined.

        This mostly used for generating MusicXML <sound> tags when necessary.

        >>> mm = tempo.MetronomeMark(number=60, referent='half')
        >>> mm.getQuarterBPM()
        120.0
        >>> mm.referent = 'quarter'
        >>> mm.getQuarterBPM()
        60.0
        '''
        if useNumberSounding and self.numberSounding is not None:
            return convertTempoByReferent(self.numberSounding,
                                          self.referent.quarterLength,
                                          1.0)
        if self.number is not None:
            # target quarter length is always 1.0
            return convertTempoByReferent(self.number,
                                          self.referent.quarterLength,
                                          1.0)
        return None

    def setQuarterBPM(self, value, setNumber=True):
        '''
        Given a value in BPM, use it to set the value of this MetronomeMark.
        BPM values are assumed to refer only to quarter notes; different beat values,
        if defined here, will be scaled


        >>> mm = tempo.MetronomeMark(number=60, referent='half')
        >>> mm.setQuarterBPM(240)  # set to 240 for a quarter
        >>> mm.number  # a half is half as fast
        120
        '''
        pass

    def _getDefaultNumber(self, tempoText):
        '''
        Given a tempo text expression or an TempoText, get the default number.

        >>> mm = tempo.MetronomeMark()
        >>> mm._getDefaultNumber('schnell')
        132
        >>> mm._getDefaultNumber('adagio')
        56
        >>> mm._getDefaultNumber('Largo e piano')
        46
        '''
        pass

    def _getDefaultText(self, number, spread=2):
        '''
        Given a tempo number try to get a text expression;
        presently only looks for approximate matches

        The `spread` value is a +/- shift around the default tempo
        indications defined in defaultTempoValues


        >>> mm = tempo.MetronomeMark()
        >>> mm._getDefaultText(92)
        'moderate'
        >>> mm._getDefaultText(208)
        'prestissimo'
        '''
        pass

    def getTextExpression(self, returnImplicit=False):
        '''
        If there is a TextExpression available that is not implicit, return it;
        otherwise, return None.

        >>> mm = tempo.MetronomeMark('presto')
        >>> mm.number
        184
        >>> mm.numberImplicit
        True
        >>> mm.getTextExpression()
        <music21.expressions.TextExpression 'presto'>
        >>> mm.textImplicit
        False

        >>> mm = tempo.MetronomeMark(number=90)
        >>> mm.numberImplicit
        False
        >>> mm.textImplicit
        True
        >>> mm.getTextExpression() is None
        True
        >>> mm.getTextExpression(returnImplicit=True)
        <music21.expressions.TextExpression 'maestoso'>
        '''
        pass

    # -------------------------------------------------------------------------
    def getEquivalentByReferent(self, referent):
        '''
        Return a new MetronomeMark object that has an equivalent speed but
        different number and referent values based on a supplied referent
        (given as a Duration type, quarterLength, or Duration object).


        >>> mm1 = tempo.MetronomeMark(number=60, referent=1.0)
        >>> mm1.getEquivalentByReferent(0.5)
        <music21.tempo.MetronomeMark larghetto Eighth=120>
        >>> mm1.getEquivalentByReferent(duration.Duration('half'))
        <music21.tempo.MetronomeMark larghetto Half=30>

        >>> mm1.getEquivalentByReferent('longa')
        <music21.tempo.MetronomeMark larghetto Imperfect Longa=3.75>

        '''
        pass

    # def getEquivalentByNumber(self, number):
    #     '''
    #     Return a new MetronomeMark object that has an equivalent speed but different number and
    #     referent values based on a supplied tempo number.
    #     '''
    #     pass

    def getMaintainedNumberWithReferent(self, referent):
        '''
        Return a new MetronomeMark object that has an equivalent number but a new referent.
        '''
        pass

    # --------------------------------------------------------------------------
    # real-time realization
    def secondsPerQuarter(self):
        '''
        Return the duration in seconds for each quarter length
        (not necessarily the referent) of this MetronomeMark.

        >>> mm1 = tempo.MetronomeMark(referent=1.0, number=60.0)
        >>> mm1.secondsPerQuarter()
        1.0
        >>> mm1 = tempo.MetronomeMark(referent=2.0, number=60.0)
        >>> mm1.secondsPerQuarter()
        0.5
        >>> mm1 = tempo.MetronomeMark(referent=2.0, number=30.0)
        >>> mm1.secondsPerQuarter()
        1.0
        '''
        pass

    def durationToSeconds(self, durationOrQuarterLength):
        '''
        Given a duration specified as a :class:`~music21.duration.Duration` object or a
        quarter length, return the resultant time in seconds at the tempo specified by
        this MetronomeMark.

        >>> mm1 = tempo.MetronomeMark(referent=1.0, number=60.0)
        >>> mm1.durationToSeconds(60)
        60.0
        >>> mm1.durationToSeconds(duration.Duration('16th'))
        0.25
        '''
        pass

    def secondsToDuration(self, seconds):
        '''
        Given a duration in seconds,
        return a :class:`~music21.duration.Duration` object equal to that time.

        >>> mm1 = tempo.MetronomeMark(referent=1.0, number=60.0)
        >>> mm1.secondsToDuration(0.25)
        <music21.duration.Duration 0.25>
        >>> mm1.secondsToDuration(0.5).type
        'eighth'
        >>> mm1.secondsToDuration(1)
        <music21.duration.Duration 1.0>
        '''
        pass


# ------------------------------------------------------------------------------
class MetricModulationException(TempoException):
    pass


# ------------------------------------------------------------------------------
class MetricModulation(TempoIndication):
    '''
    A class for representing the relationship between two MetronomeMarks.
    Generally this relationship is one of equality, where the number is maintained but
    the referent that number is applied to each change.

    The basic definition of a MetricModulation is given by supplying two MetronomeMarks,
    one for the oldMetronome, the other for the newMetronome. High level properties,
    oldReferent and newReferent, and convenience methods permit only setting the referent.

    The `classicalStyle` attribute determines of the first MetronomeMark describes the
    new tempo, not the old (the reverse of expected usage).

    The `maintainBeat` attribute determines if, after an equality statement,
    the beat is maintained. This is relevant for moving from 3/4 to 6/8, for example.

    >>> s = stream.Stream()
    >>> mm1 = tempo.MetronomeMark(number=60)
    >>> s.append(mm1)
    >>> s.repeatAppend(note.Note(quarterLength=1), 2)
    >>> s.repeatAppend(note.Note(quarterLength=0.5), 4)

    >>> mmod1 = tempo.MetricModulation()
    >>> mmod1.oldReferent = 0.5  # can use Duration objects
    >>> mmod1.newReferent = 'quarter'  # can use Duration objects
    >>> s.append(mmod1)
    >>> mmod1.updateByContext()  # get number from last MetronomeMark on Stream
    >>> mmod1.newMetronome
    <music21.tempo.MetronomeMark animato Quarter=120>

    >>> s.append(note.Note())
    >>> s.repeatAppend(note.Note(quarterLength=1.5), 2)

    >>> mmod2 = tempo.MetricModulation()
    >>> s.append(mmod2)  # if the obj is added to Stream, can set referents
    >>> mmod2.oldReferent = 1.5  # will get number from previous MetronomeMark
    >>> mmod2.newReferent = 'quarter'
    >>> mmod2.newMetronome
    <music21.tempo.MetronomeMark animato Quarter=80>

    Note that an initial metric modulation can set old and new referents and get None as
    tempo numbers:

    >>> mmod3 = tempo.MetricModulation()
    >>> mmod3.oldReferent = 'half'
    >>> mmod3.newReferent = '16th'
    >>> mmod3
    <music21.tempo.MetricModulation
        <music21.tempo.MetronomeMark
            Half=None>=<music21.tempo.MetronomeMark 16th=None>>

    test w/ more sane referents that either the old or the new can change without a tempo number

    >>> mmod3.oldReferent = 'quarter'
    >>> mmod3.newReferent = 'eighth'
    >>> mmod3
    <music21.tempo.MetricModulation
        <music21.tempo.MetronomeMark
            Quarter=None>=<music21.tempo.MetronomeMark Eighth=None>>
    >>> mmod3.oldMetronome
    <music21.tempo.MetronomeMark Quarter=None>
    >>> mmod3.oldMetronome.number = 60

    New number automatically updates:

    >>> mmod3
    <music21.tempo.MetricModulation
        <music21.tempo.MetronomeMark larghetto
            Quarter=60>=<music21.tempo.MetronomeMark larghetto Eighth=60>>
    '''

    def __init__(self, **keywords):
        super().__init__(**keywords)

        self.classicalStyle = False
        self.maintainBeat = False
        self.transitionSymbol = '='  # accept different symbols
        # some old formats use arrows
        self.arrowDirection = None  # can be left, right, or None

        # showing parens or not
        self.parentheses = False

        # store two MetronomeMark objects
        self._oldMetronome = None
        self._newMetronome = None

    def _reprInternal(self):
        pass

    # --------------------------------------------------------------------------
    # core properties
    def _setOldMetronome(self, value):
        pass

    def _getOldMetronome(self):
        pass

    oldMetronome = property(_getOldMetronome, _setOldMetronome, doc='''
        Get or set the left :class:`~music21.tempo.MetronomeMark` object
        for the old, or previous value.

        >>> mm1 = tempo.MetronomeMark(number=60, referent=1)
        >>> mm1
        <music21.tempo.MetronomeMark larghetto Quarter=60>
        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.oldMetronome = mm1

        Note that we do need to have a proper MetronomeMark instance to figure this out:

        >>> mmod1.oldMetronome = 'junk'
        Traceback (most recent call last):
        music21.tempo.MetricModulationException: oldMetronome property
            must be set with a MetronomeMark instance
        ''')

    def _setOldReferent(self, value):
        pass
            # raise MetricModulationException('cannot set old MetronomeMark from provided value.')

    def _getOldReferent(self):
        pass

    oldReferent = property(_getOldReferent, _setOldReferent, doc='''
        Get or set the referent of the old MetronomeMark.

        >>> mm1 = tempo.MetronomeMark(number=60, referent=1)
        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.oldMetronome = mm1
        >>> mmod1.oldMetronome
        <music21.tempo.MetronomeMark larghetto Quarter=60>
        >>> mmod1.oldReferent = 0.25
        >>> mmod1.oldMetronome
        <music21.tempo.MetronomeMark larghetto 16th=240>

        ''')

    def _setNewMetronome(self, value):
        pass

    def _getNewMetronome(self):
        # before returning the referent, see if we can update the number
        pass

    newMetronome = property(_getNewMetronome, _setNewMetronome, doc='''
        Get or set the right :class:`~music21.tempo.MetronomeMark`
        object for the new, or following value.

        >>> mm1 = tempo.MetronomeMark(number=60, referent=1)
        >>> mm1
        <music21.tempo.MetronomeMark larghetto Quarter=60>
        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.newMetronome = mm1
        >>> mmod1.newMetronome = 'junk'
        Traceback (most recent call last):
        music21.tempo.MetricModulationException: newMetronome property must be
            set with a MetronomeMark instance
        ''')

    def _setNewReferent(self, value):
        pass

    def _getNewReferent(self):
        pass

    newReferent = property(_getNewReferent, _setNewReferent, doc='''
        Get or set the referent of the new MetronomeMark.

        >>> mm1 = tempo.MetronomeMark(number=60, referent=1)
        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.newMetronome = mm1
        >>> mmod1.newMetronome
        <music21.tempo.MetronomeMark larghetto Quarter=60>
        >>> mmod1.newReferent = 0.25
        >>> mmod1.newMetronome
        <music21.tempo.MetronomeMark larghetto 16th=240>
        ''')

    @property
    def number(self):
        '''
        Get and the number of the MetricModulation, or the number
        assigned to the new MetronomeMark.

        >>> s = stream.Stream()
        >>> mm1 = tempo.MetronomeMark(number=60)
        >>> s.append(mm1)
        >>> s.repeatAppend(note.Note(quarterLength=1), 2)
        >>> s.repeatAppend(note.Note(quarterLength=0.5), 4)

        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.oldReferent = 0.5  # can use Duration objects
        >>> mmod1.newReferent = 'quarter'
        >>> s.append(mmod1)
        >>> mmod1.updateByContext()
        >>> mmod1.newMetronome
        <music21.tempo.MetronomeMark animato Quarter=120>
        >>> mmod1.number
        120
        '''
        pass

    # def _setNumber(self, value, updateTextFromNumber=True):
    #     if not common.isNum(value):
    #         raise MetricModulationException('cannot set number to a string')
    #     self._newMetronome.number = value
    #     self._oldMetronome.number = value

    # --------------------------------------------------------------------------
    # high-level configuration methods
    def updateByContext(self):
        '''
        Update this metric modulation based on the context,
        or the surrounding MetronomeMarks or MetricModulations.
        The object needs to reside in a Stream for this to be effective.
        '''
        pass

    def setEqualityByReferent(self, side=None, referent=1.0):
        '''
        Set the other side of the metric modulation to
        an equality; side can be specified, or if one side
        is None, that side will be set.

        >>> mm1 = tempo.MetronomeMark(number=60, referent=1)
        >>> mmod1 = tempo.MetricModulation()
        >>> mmod1.newMetronome = mm1
        >>> mmod1.setEqualityByReferent(None, 2)
        >>> mmod1
        <music21.tempo.MetricModulation
             <music21.tempo.MetronomeMark larghetto
                   Half=30>=<music21.tempo.MetronomeMark larghetto Quarter=60>>

        '''
        pass

    def setOtherByReferent(
        self,
        side: str|None = None,
        referent: str|int|float = 1.0
    ):
        '''
        Set the other side of the metric modulation not based on equality,
        but on a direct translation of the tempo value.

        referent can be a string type or an int/float quarter length
        '''
        pass


# ------------------------------------------------------------------------------
def interpolateElements(element1, element2, sourceStream,
                        destinationStream, autoAdd=True):
    # noinspection PyShadowingNames
    '''
    Assume that element1 and element2 are two elements in sourceStream
    and destinationStream with other elements (say eA, eB, eC) between
    them.  For instance, element1 could be the downbeat at offset 10
    in sourceStream (a Stream representing a score) and offset 20.5
    in destinationStream (which might be a Stream representing the
    timing of notes in particular recording at approximately but not
    exactly qtr = 30). Element2 could be the following downbeat in 4/4,
    at offset 14 in source but offset 25.0 in the recording:

    >>> sourceStream = stream.Stream()
    >>> destinationStream = stream.Stream()
    >>> element1 = note.Note('C4', type='quarter')
    >>> element2 = note.Note('G4', type='quarter')
    >>> sourceStream.insert(10, element1)
    >>> destinationStream.insert(20.5, element1)
    >>> sourceStream.insert(14, element2)
    >>> destinationStream.insert(25.0, element2)

    Suppose eA, eB, and eC are three quarter notes that lie
    between element1 and element2 in sourceStream
    and destinationStream, as in:

    >>> eA = note.Note('D4', type='quarter')
    >>> eB = note.Note('E4', type='quarter')
    >>> eC = note.Note('F4', type='quarter')
    >>> sourceStream.insert(11, eA)
    >>> sourceStream.insert(12, eB)
    >>> sourceStream.insert(13, eC)
    >>> destinationStream.append([eA, eB, eC])  # not needed if autoAdd were true

    then running this function will cause eA, eB, and eC
    to have offsets 21.625, 22.75, and 23.875 respectively
    in destinationStream:

    >>> tempo.interpolateElements(element1, element2,
    ...         sourceStream, destinationStream, autoAdd=False)
    >>> for el in [eA, eB, eC]:
    ...    print(el.getOffsetBySite(destinationStream))
    21.625
    22.75
    23.875

    if the elements between element1 and element2 do not yet
    appear in destinationStream, they are automatically added
    unless autoAdd is False.

    (with the default autoAdd, elements are automatically added to new streams):

    >>> destStream2 = stream.Stream()
    >>> destStream2.insert(10.1, element1)
    >>> destStream2.insert(50.5, element2)
    >>> tempo.interpolateElements(element1, element2, sourceStream, destStream2)
    >>> for el in [eA, eB, eC]:
    ...    offset = float(el.getOffsetBySite(destStream2))
    ...    print(f'{offset:.1f}')
    20.2
    30.3
    40.4

    (unless autoAdd is set to False, in which case a Tempo Exception arises:)

    >>> destStream3 = stream.Stream()
    >>> destStream3.insert(100, element1)
    >>> destStream3.insert(500, element2)
    >>> eA.id = 'blah'
    >>> tempo.interpolateElements(element1, element2, sourceStream, destStream3, autoAdd=False)
    Traceback (most recent call last):
    music21.tempo.TempoException: Could not find element <music21.note.Note D> with id ...
    '''
    pass


# ------------------------------------------------------------------------------
class TempoChangeSpanner(spanner.Spanner):
    '''
    Spanners showing tempo-change.  They do nothing right now.
    '''
    pass


class RitardandoSpanner(TempoChangeSpanner):
    '''
    Spanner representing a slowing down.
    '''
    pass


class AccelerandoSpanner(TempoChangeSpanner):
    '''
    Spanner representing a speeding up.
    '''
    pass


# ------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def testCopyAndDeepcopy(self):
        pass

    def testSetup(self):
        pass

    def testUnicode(self):
        # test with no arguments
        pass

    def testTempoTextStyle(self):
        pass

    def testMetronomeMarkA(self):
        pass

    def testMetronomeMarkB(self):
        pass

    def testMetronomeModulationA(self):
        pass

    def testGetPreviousMetronomeMarkA(self):
        pass
        # p.show()

    def testGetPreviousMetronomeMarkB(self):
        pass
        # p.show()

    def testGetPreviousMetronomeMarkC(self):
        pass

    def testSetReferentA(self):
        '''
        Test setting referents directly via context searches.
        '''
        pass
        # p.show()

    def testSetReferentB(self):
        pass

        # s.repeatAppend(note.Note(), 4)
        # s.show()

    def testSetReferentC(self):
        pass
        # s.repeatAppend(note.Note(), 4)
        # s.show()

    def testSetReferentD(self):
        pass
        # s.append(note.Note())
        # s.repeatAppend(note.Note(quarterLength=1.5), 2)

    def testSetReferentE(self):
        pass

    def testSecondsPerQuarterA(self):
        pass

    def testStylesAreShared(self):
        pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER = [MetronomeMark,
              TempoText,
              MetricModulation,
              TempoIndication,
              AccelerandoSpanner,
              RitardandoSpanner,
              TempoChangeSpanner,
              interpolateElements]


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , runTest='testStylesAreShared')
