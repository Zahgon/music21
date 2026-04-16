# -----------------------------------------------------------------------------
# Name:         audioSearch.py
# Purpose:      base subroutines for all audioSearching and score following
#               routines
#
# Authors:      Jordi Bartolome
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011-2020 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
'''
Base routines used throughout audioSearching and score-following.

Requires numpy and matplotlib.  Installing scipy makes the process faster
and more accurate using FFT convolve.
'''
from __future__ import annotations

__all__ = [
    'AudioSearchException',
    'autocorrelationFunction',
    'decisionProcess',
    'detectPitchFrequencies',
    'getFrequenciesFromAudioFile',
    'getFrequenciesFromMicrophone',
    'getFrequenciesFromPartialAudioFile',
    'histogram',
    'interpolation',
    'joinConsecutiveIdenticalPitches',
    'normalizeInputFrequency',
    'notesAndDurationsToStream',
    'pitchFrequenciesToObjects',
    'prepareThresholds',
    'quantizeDuration',
    'quarterLengthEstimation',
    'recording',
    'scoreFollower',
    'smoothFrequencies',
    'transcriber',
]

import copy
import math
import pathlib
import wave
import warnings
import unittest

from typing import cast

# cannot call this base, because when audioSearch.__init__.py
# imports * from base, it overwrites audioSearch!
from music21 import base
from music21 import environment
from music21 import exceptions21
from music21 import features
from music21 import metadata
from music21 import note
from music21 import pitch
from music21 import scale
from music21 import stream

from music21.audioSearch import recording
from music21.audioSearch import transcriber

environLocal = environment.Environment('audioSearch')

audioChunkLength = 1024
recordSampleRate = 44100


def histogram(data, bins):
    # noinspection PyShadowingNames
    '''
    Partition the list in `data` into a number of bins defined by `bins`
    and return the number of elements in each bin and a set of `bins` + 1
    elements where the first element (0) is the start of the first bin,
    the last element (-1) is the end of the last bin, and every remaining element (i)
    is the dividing point between one bin and another.

    >>> data = [1, 1, 4, 5, 6, 0, 8, 8, 8, 8, 8]
    >>> outputData, bins = audioSearch.histogram(data, 8)
    >>> print(outputData)
    [3, 0, 0, 1, 1, 1, 0, 5]
    >>> bins
    [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    >>> print([int(b) for b in bins])
    [0, 1, 2, 3, 4, 5, 6, 7, 8]

    >>> outputData, bins = audioSearch.histogram(data, 4)
    >>> print(outputData)
    [3, 1, 2, 5]
    >>> print([int(b) for b in bins])
    [0, 2, 4, 6, 8]
    '''
    pass


def autocorrelationFunction(recordedSignal, recordSampleRateIn):
    # noinspection PyShadowingNames
    '''
    Converts the temporal domain into a frequency domain. To do that, it
    uses the autocorrelation function, which finds periodicities in the signal
    in the temporal domain and, consequently, finds the frequency in each instant
    of time.

    >>> import wave
    >>> import numpy  # you need to have numpy, scipy, and matplotlib installed to use this

    >>> wv = wave.open(str(common.getSourceFilePath() /
    ...                     'audioSearch' / 'test_audio.wav'), 'r')
    >>> data = wv.readframes(1024)
    >>> samples = numpy.frombuffer(data, dtype=numpy.int16)
    >>> finalResult = audioSearch.autocorrelationFunction(samples, 44100)
    >>> wv.close()
    >>> print(finalResult)
    143.6276...
    '''
    pass


def prepareThresholds(useScale=None):
    # noinspection PyShadowingNames
    '''
    returns two elements.  The first is a list of threshold values
    for one octave of a given scale, `useScale`,
    (including the octave repetition) (Default is a ChromaticScale).
    The second is the pitches of the scale.

    A threshold value is the fractional part of the log-base-2 value of the
    frequency.

    For instance if A = 440 and B-flat = 460, then the threshold between
    A and B-flat will be 450.  Notes below 450 should be considered As and those
    above 450 should be considered B-flats.

    Thus, the list returned has one less element than the number of notes in the
    scale + octave repetition.  If useScale is a ChromaticScale, `prepareThresholds`
    will return a 12-element list.  If it's a diatonic scale, it'll have 7 elements.


    >>> pitchThresholds, pitches = audioSearch.prepareThresholds(scale.MajorScale('A3'))
    >>> for i in range(len(pitchThresholds)):
    ...    print(f'{pitches[i]} < {pitchThresholds[i]:.2f} < {pitches[i + 1]}')
    A3 < 0.86 < B3
    B3 < 0.53 < C#4
    C#4 < 0.16 < D4
    D4 < 0.28 < E4
    E4 < 0.45 < F#4
    F#4 < 0.61 < G#4
    G#4 < 1.24 < A4
    '''
    pass


def interpolation(correlation, peak):
    # noinspection PyShadowingNames
    '''
    Interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.

    Correlation is a vector and peak is an index for that vector.

    Returns the x coordinate of the vertex of that parabola.

    >>> import numpy
    >>> f = [2, 3, 1, 6, 4, 2, 3, 1]
    >>> peak = int(numpy.argmax(f))
    >>> peak  # f[3] is 6, which is the max.
    3
    >>> audioSearch.interpolation(f, peak)
    3.21428571...
    '''
    pass


def normalizeInputFrequency(inputPitchFrequency, thresholds=None, pitches=None):
    # noinspection PyShadowingNames
    '''
    Takes in an inputFrequency, a set of threshold values, and a set of allowable pitches
    (given by prepareThresholds) and returns a tuple of the normalized frequency and the
    pitch detected (as a :class:`~music21.pitch.Pitch` object)

    It will convert the frequency to be within the range of the default frequencies
    (usually C4 to C5), but the pitch object will have the correct octave.

    >>> audioSearch.normalizeInputFrequency(441.72)
    (440.0, <music21.pitch.Pitch A4>)

    If you will be doing this often, it's best to cache your thresholds and
    pitches by running `prepareThresholds` once first:

    >>> thresholds, pitches = audioSearch.prepareThresholds(scale.ChromaticScale('C4'))
    >>> for fq in [450, 510, 550, 600]:
    ...      print(audioSearch.normalizeInputFrequency(fq, thresholds, pitches))
    (440.0, <music21.pitch.Pitch A4>)
    (523.25113..., <music21.pitch.Pitch C5>)
    (277.18263..., <music21.pitch.Pitch C#5>)
    (293.66476..., <music21.pitch.Pitch D5>)
    '''
    pass


def pitchFrequenciesToObjects(detectedPitchesFreq, useScale=None):
    # noinspection PyShadowingNames
    '''
    Takes in a list of detected pitch frequencies and returns a tuple where the first element
    is a list of :class:~`music21.pitch.Pitch` objects that best match these frequencies
    and the second element is a list of the frequencies of those objects that can
    be plotted for matplotlib

    TODO: only return the former.  The latter can be generated in other ways.

    >>> readPath = common.getSourceFilePath() / 'audioSearch' / 'test_audio.wav'
    >>> freqFromAQList = audioSearch.getFrequenciesFromAudioFile(waveFilename=readPath)

    >>> detectedPitchesFreq = audioSearch.detectPitchFrequencies(
    ...   freqFromAQList, useScale=scale.ChromaticScale('C4'))
    >>> detectedPitchesFreq = audioSearch.smoothFrequencies(detectedPitchesFreq)
    >>> (detectedPitchObjects, listPlot) = audioSearch.pitchFrequenciesToObjects(
    ...   detectedPitchesFreq, useScale=scale.ChromaticScale('C4'))
    >>> [str(p) for p in detectedPitchObjects]
    ['A5', 'A5', 'A6', 'D6', 'D4', 'B4', 'A4', 'F4', 'E-4', 'C#3', 'B3', 'B3', 'B3', 'A3', 'G3',...]
    '''
    pass


def getFrequenciesFromMicrophone(length=10.0, storeWaveFilename=None):
    '''
    records for length (=seconds) a set of frequencies from the microphone.

    If storeWaveFilename is not None, then it will store the recording on disk
    in a wave file.

    Returns a list of frequencies detected.

    TODO -- find a way to test or at least demo
    '''
    pass


def getFrequenciesFromAudioFile(waveFilename='xmas.wav'):
    '''
    gets a list of frequencies from a complete audio file.

    Each sample is a window of audioSearch.audioChunkLength long.

    >>> audioSearch.audioChunkLength
    1024

    >>> readPath = common.getSourceFilePath() / 'audioSearch' / 'test_audio.wav'
    >>> freq = audioSearch.getFrequenciesFromAudioFile(waveFilename=readPath)
    >>> print(freq)
    [143.627..., 99.083..., 211.004..., 4700.313..., ...]
    '''
    pass


def getFrequenciesFromPartialAudioFile(waveFilenameOrHandle='temp', length=10.0, startSample=0):
    '''
    It calculates the fundamental frequency at every instant of time of an audio signal
    extracted either from the microphone or from an already recorded song.
    It uses a period of time defined by the variable "length" in seconds.

    It returns a list with the frequencies, a variable with the file descriptor,
    and the end sample position.

    >>> #_DOCS_SHOW readFile = 'pachelbel.wav'
    >>> sp = common.getSourceFilePath() #_DOCS_HIDE
    >>> readFile = sp / 'audioSearch' / 'test_audio.wav' #_DOCS_HIDE
    >>> fTup  = audioSearch.getFrequenciesFromPartialAudioFile(readFile, length=1.0)
    >>> frequencyList, pachelbelFileHandle, currentSample = fTup
    >>> for frequencyIndex in range(5):
    ...     print(frequencyList[frequencyIndex])
    143.627...
    99.083...
    211.004...
    4700.313...
    767.827...
    >>> print(currentSample)  # should be near 44100, but probably not exact
    44032

    Now read the next 1 second:

    >>> fTup = audioSearch.getFrequenciesFromPartialAudioFile(pachelbelFileHandle, length=1.0,
    ...                                                       startSample=currentSample)
    >>> frequencyList, pachelbelFileHandle, currentSample = fTup
    >>> for frequencyIndex in range(5):
    ...     print(frequencyList[frequencyIndex])
    187.798...
    238.263...
    409.700...
    149.958...
    101.989...
    >>> print(currentSample)  # should be exactly double the previous
    88064
    '''
    pass


def detectPitchFrequencies(freqFromAQList, useScale=None):
    # noinspection PyShadowingNames
    '''
    Detects the pitches of the notes from a list of frequencies, using thresholds which
    depend on the useScale option. If useScale is None,
    the default value is the Major Scale beginning C4.

    Returns the frequency of each pitch after normalizing them.

    >>> freqFromAQList=[143.627689055, 99.0835452019, 211.004784689, 4700.31347962, 2197.9431119]
    >>> cMaj = scale.MajorScale('C4')
    >>> pitchesList = audioSearch.detectPitchFrequencies(freqFromAQList, useScale=cMaj)
    >>> for i in range(5):
    ...     print(int(round(pitchesList[i])))
    147
    98
    220
    4699
    2093
    '''
    pass


def smoothFrequencies(
    frequencyList: list[int|float],
    *,
    smoothLevels=7,
    inPlace=False
) -> list[int]|None:
    '''
    Smooths the shape of the signal to avoid false detections in the fundamental
    frequency.  Takes in a list of ints or floats.

    The second pitch below is certainly too low.  It will be smoothed out:

    >>> inputPitches = [440, 220, 440, 440, 442, 443, 441, 470, 440, 441, 440,
    ...                 442, 440, 440, 440, 397, 440, 440, 440, 442, 443, 441,
    ...                 440, 440, 440, 440, 440, 442, 443, 441, 440, 440]
    >>> result = audioSearch.smoothFrequencies(inputPitches)
    >>> result
    [409, 409, 409, 428, 435, 438, 442, 444, 441, 441, 441,
     441, 434, 433, 432, 431, 437, 438, 439, 440, 440, 440,
     440, 440, 440, 441, 441, 441, 440, 440, 440, 440]

    Original list is unchanged:

    >>> inputPitches[1]
    220

    Different levels of smoothing have different effects.  At smoothLevel=2,
    the isolated 220hz sample is pulling down the surrounding samples:

    >>> audioSearch.smoothFrequencies(inputPitches, smoothLevels=2)[:5]
    [330, 275, 358, 399, 420]

    Doing this enough times will smooth out a lot of inconsistencies.

    >>> audioSearch.smoothFrequencies(inputPitches, smoothLevels=28)[:5]
    [432, 432, 432, 432, 432]


    If inPlace is True then the list is modified in place and nothing is returned:

    >>> audioSearch.smoothFrequencies(inputPitches, inPlace=True)
    >>> inputPitches[:5]
    [409, 409, 409, 428, 435]

    Note that `smoothLevels=1` is the baseline that does nothing:

    >>> audioSearch.smoothFrequencies(inputPitches, smoothLevels=1) == inputPitches
    True

    And less than 1 raises a ValueError:

    >>> audioSearch.smoothFrequencies(inputPitches, smoothLevels=0)
    Traceback (most recent call last):
    ValueError: smoothLevels must be >= 1

    There cannot be more smoothLevels than input frequencies:

    >>> audioSearch.smoothFrequencies(inputPitches, smoothLevels=40)
    Traceback (most recent call last):
    ValueError: There cannot be more smoothLevels (40) than inputPitches (32)

    Note that the system runs on O(smoothLevels * len(frequenciesList)),
    so additional smoothLevels can be costly on a large set.

    This function always returns a list of ints -- rounding to the nearest
    hertz (you did want it smoothed right?)

    * Changed in v6: inPlace defaults to False (like other music21
      functions) and if done in Place, returns nothing.  smoothLevels and inPlace
      became keyword only.
    '''
    pass


# ------------------------------------------------------
# Duration related routines


def joinConsecutiveIdenticalPitches(detectedPitchObjects):
    # noinspection PyShadowingNames
    '''
    takes a list of equally spaced :class:`~music21.pitch.Pitch` objects
    and returns a tuple of two lists, the first a list of
    :class:`~music21.note.Note`
    or :class:`~music21.note.Rest` objects (each of quarterLength 1.0)
    and a list of how many were joined together to make that object.

    N.B. the returned list is NOT a :class:`~music21.stream.Stream`.

    >>> readPath = common.getSourceFilePath() / 'audioSearch' / 'test_audio.wav'
    >>> freqFromAQList = audioSearch.getFrequenciesFromAudioFile(waveFilename=readPath)
    >>> chrome = scale.ChromaticScale('C4')
    >>> detectedPitchesFreq = audioSearch.detectPitchFrequencies(freqFromAQList, useScale=chrome)
    >>> detectedPitchesFreq = audioSearch.smoothFrequencies(detectedPitchesFreq)
    >>> (detectedPitches, listPlot) = audioSearch.pitchFrequenciesToObjects(
    ...        detectedPitchesFreq, useScale=chrome)
    >>> len(detectedPitches)
    861
    >>> notesList, durationList = audioSearch.joinConsecutiveIdenticalPitches(detectedPitches)
    >>> len(notesList)
    24
    >>> print(notesList)
    [<music21.note.Rest quarter>, <music21.note.Note C>, <music21.note.Note C>,
     <music21.note.Note D>, <music21.note.Note E>, <music21.note.Note F>,
     <music21.note.Note G>, <music21.note.Note A>, <music21.note.Note B>,
     <music21.note.Note C>, ...]
    >>> print(durationList)
    [71, 6, 14, 23, 34, 40, 27, 36, 35, 15, 17, 15, 6, 33, 22, 13, 16, 39, 35, 38, 27, 27, 26, 8]
    '''
    pass


def quantizeDuration(length):
    '''
    round an approximately transcribed quarterLength to a better one in
    music21.

    Should be replaced by a full-featured routine in midi or stream.

    See :meth:`~music21.stream.Stream.quantize` for more information
    on the standard music21 methodology.

    >>> audioSearch.quantizeDuration(1.01)
    1.0
    >>> audioSearch.quantizeDuration(1.70)
    1.5
    '''
    pass


def quarterLengthEstimation(durationList, mostRepeatedQuarterLength=1.0):
    # noinspection PyShadowingNames
    '''
    takes a list of lengths of notes (measured in
    audio samples) and tries to estimate what the length of a
    quarter note should be in this list.

    If mostRepeatedQuarterLength is another number, it still returns the
    estimated length of a quarter note, but chooses it so that the most
    common note in durationList will be the other note.  See example 2:

    Returns a float -- and not an int.

    >>> durationList = [20, 19, 10, 30, 6, 21]
    >>> audioSearch.quarterLengthEstimation(durationList)
    20.625

    Example 2: suppose these are the inputted durations for a
    score where most of the notes are half notes.  Show how long
    a quarter note should be:

    >>> audioSearch.quarterLengthEstimation(durationList, mostRepeatedQuarterLength=2.0)
    10.3125
    '''
    pass


def notesAndDurationsToStream(
    notesList,
    durationList,
    scNotes=None,
    removeRestsAtBeginning=True,
    qle=None
):
    # noinspection PyShadowingNames
    '''
    take a list of :class:`~music21.note.Note` objects or rests
    and an equally long list of how long
    each one lasts in terms of samples and returns a
    Stream using the information from quarterLengthEstimation
    and quantizeDurations.

    returns a :class:`~music21.stream.Score` object, containing
    a metadata object and a single :class:`~music21.stream.Part` object, which in turn
    contains the notes, etc.  Does not run :meth:`~music21.stream.base.Stream.makeNotation`
    on the Score.


    >>> durationList = [20, 19, 10, 30, 6, 21]
    >>> n = note.Note
    >>> noteList = [n('C#4'), n('D5'), n('B4'), n('F#5'), n('C5'), note.Rest()]
    >>> s,lengthPart = audioSearch.notesAndDurationsToStream(noteList, durationList)
    >>> s.show('text')
    {0.0} <music21.metadata.Metadata object at ...>
    {0.0} <music21.stream.Part ...>
        {0.0} <music21.note.Note C#>
        {1.0} <music21.note.Note D>
        {2.0} <music21.note.Note B>
        {2.5} <music21.note.Note F#>
        {4.0} <music21.note.Note C>
        {4.25} <music21.note.Rest quarter>
    '''
    pass


def decisionProcess(
    partsList,
    notePrediction,
    beginningData,
    lastNotePosition,
    countdown,
    firstNotePage=None,
    lastNotePage=None
):
    # noinspection PyShadowingNames
    '''
    Decides which of the given parts of the score has the best match with
    the recorded part of the song.
    If there is not a part of the score with a high probability to be the correct part,
    it starts a "countdown" in order stop the score following if the bad matching persists.
    In this case, it does not match the recorded part of the song with any part of the score.

    Inputs: partsList, contains all the possible parts of the score, sorted from the
    higher probability to be the best matching at the beginning to the lowest probability.
    notePrediction is the position of the score in which the next note should start.
    beginningData is a list with all the beginnings of the used fragments of the score to find
    the best matching.
    lastNotePosition is the position of the score in which the last matched fragment of the
    score finishes.
    Countdown is a counter of consecutive errors in the matching process.

    Outputs: Returns the beginning of the best matching fragment of
    score and the countdown.

    >>> scNotes = corpus.parse('luca/gloria').parts[0].flatten().notes.stream()
    >>> scoreStream = scNotes
    >>> sfp = common.getSourceFilePath() #_DOCS_HIDE
    >>> readPath = sfp / 'audioSearch' / 'test_audio.wav' #_DOCS_HIDE
    >>> freqFromAQList = audioSearch.getFrequenciesFromAudioFile(waveFilename=readPath) #_DOCS_HIDE

    >>> tf = 'test_audio.wav'
    >>> #_DOCS_SHOW freqFromAQList = audioSearch.getFrequenciesFromAudioFile(waveFilename=tf)
    >>> chrome = scale.ChromaticScale('C4')
    >>> detectedPitchesFreq = audioSearch.detectPitchFrequencies(freqFromAQList, useScale=chrome)
    >>> detectedPitchesFreq = audioSearch.smoothFrequencies(detectedPitchesFreq)
    >>> (detectedPitches, listPlot) = audioSearch.pitchFrequenciesToObjects(
    ...                                             detectedPitchesFreq, useScale=chrome)
    >>> (notesList, durationList) = audioSearch.joinConsecutiveIdenticalPitches(detectedPitches)
    >>> transcribedScore, qle = audioSearch.notesAndDurationsToStream(notesList, durationList,
    ...                                             scNotes=scNotes, qle=None)
    >>> hop = 6
    >>> tn_recording = 24
    >>> totScores = []
    >>> beginningData = []
    >>> lengthData = []
    >>> for i in range(4):
    ...     excerpt = scoreStream[i * hop + 1:i * hop + tn_recording + 1]
    ...     scNotes = stream.Part(excerpt)
    ...     name = str(i)
    ...     beginningData.append(i * hop + 1)
    ...     lengthData.append(tn_recording)
    ...     scNotes.id = name
    ...     totScores.append(scNotes)
    >>> listOfParts = search.approximateNoteSearch(transcribedScore.flatten().notes.stream(),
    ...                                            totScores)
    >>> notePrediction = 0
    >>> lastNotePosition = 0
    >>> countdown = 0
    >>> positionInList, countdown = audioSearch.decisionProcess(
    ...          listOfParts, notePrediction, beginningData, lastNotePosition, countdown)
    >>> print(positionInList)
    0

    The countdown result is 1 because the song used is completely different from the score!!

    >>> print(countdown)
    1
    '''
    pass


class AudioSearchException(exceptions21.Music21Exception):
    pass

# -----------------------------------------


class Test(unittest.TestCase):
    pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER: list[type] = []


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

