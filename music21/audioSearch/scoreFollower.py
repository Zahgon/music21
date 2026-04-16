# -----------------------------------------------------------------------------
# Name:         audioSearch.scoreFollower.py
# Purpose:      Detection of the position in the score in real time
#
#
# Authors:      Jordi Bartolome
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
from __future__ import annotations

import math
from time import time
import unittest

from music21 import environment
from music21 import scale
from music21 import search
from music21 import stream

environLocal = environment.Environment('audioSearch.scoreFollower')


class ScoreFollower:
    def __init__(self, scoreStream=None):
        self.scoreStream = scoreStream
        if scoreStream is not None:
            self.scoreNotesOnly = scoreStream.flatten().notesAndRests.stream()
        else:
            self.scoreNotesOnly = None
        self.waveFile = str(environLocal.getRootTempDir() / 'scoreFollowerTemp.wav')
        self.lastNotePosition = 0
        self.currentSample = 0
        self.totalFile = 0
        self.lastNotePosition = 0
        self.startSearchAtSlot = 0
        self.predictedNotePosition = 0
        self.countdown = 0
        self.END_OF_SCORE = False
        self.qle = None
        self.firstNotePage = None
        self.lastNotePage = None
        self.firstSlot = 1
        self.silencePeriodCounter = 0
        self.notesCounter = 0
        self.begins = True

        self.useScale = None
        self.silencePeriod = None
        self.result = None
        self.useMic = None
        self.processing_time = None
        self.seconds_recording = None

    def runScoreFollower(
        self,
        plot=False,
        useMic=False,
        seconds=15.0,
        useScale=None,
    ):
        '''
        The main program. It runs the 'repeatTranscription' until the
        performance ends.

        If `useScale` is none, then it uses a scale.ChromaticScale
        '''
        pass

    def repeatTranscription(self):
        '''
        First, it records from the microphone (or from a file if is used for
        test). Later, it processes the signal to detect the pitches.
        It converts them into music21 objects and compares them with the score.
        It finds the best matching position of the recorded signal with the
        score, and decides, depending on matching accuracy, the last note
        predicted and some other parameters, in which position the recorded
        signal is.

        It returns a value that is False if the song has not finished, or true
        if there has been a problem like some consecutive bad matches or the
        score has finished.

        >>> from music21.audioSearch import scoreFollower
        >>> scoreNotes = ' '.join(['c4', 'd', 'e', 'f', 'g', 'a', 'b', "c'", 'c', 'e',
        ...     'g', "c'", 'a', 'f', 'd', 'c#', 'd#', 'f#', 'c', 'e', 'g', "c'",
        ...     'a', 'f', 'd', 'c#', 'd#', 'f#'])
        >>> scNotes = converter.parse('tinynotation: 4/4 ' + scoreNotes, makeNotation=False)
        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.useMic = False
        >>> import os #_DOCS_HIDE
        >>> ScF.waveFile = str(common.getSourceFilePath() #_DOCS_HIDE
        ...                 / 'audioSearch' / 'test_audio.wav') #_DOCS_HIDE
        >>> #_DOCS_SHOW ScF.waveFile = 'test_audio.wav'
        >>> ScF.seconds_recording = 10
        >>> ScF.useScale = scale.ChromaticScale('C4')
        >>> ScF.currentSample = 0
        >>> exitType = ScF.repeatTranscription()
        >>> print(exitType)
        False
        >>> print(ScF.lastNotePosition)
        10

        '''
        pass

    def silencePeriodDetection(self, notesList):
        '''
        Detection of consecutive periods of silence.
        Useful if the musician has some consecutive measures of silence.

        >>> from music21.audioSearch import scoreFollower
        >>> scNotes = corpus.parse('luca/gloria').parts[0].flatten().notes.stream()
        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> notesList = []
        >>> notesList.append(note.Rest())
        >>> ScF.notesCounter = 3
        >>> ScF.silencePeriodCounter = 0
        >>> ScF.silencePeriodDetection(notesList)
        >>> ScF.notesCounter
        0
        >>> ScF.silencePeriodCounter
        1


        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> notesList = []
        >>> notesList.append(note.Rest())
        >>> notesList.append(note.Note())
        >>> ScF.notesCounter = 1
        >>> ScF.silencePeriodCounter = 3
        >>> ScF.silencePeriodDetection(notesList)
        >>> ScF.notesCounter
        2
        >>> ScF.silencePeriodCounter
        0
        '''
        pass

    def updatePosition(self, prob, totalLengthPeriod, time_start):
        '''
        It updates the position in which the scoreFollower starts to search at,
        and the predicted position in which the new fragment of the score
        should start.  It updates these positions taking into account the value
        of the "countdown", and if is the beginning of the song or not.

        It returns the exitType, which determines whether the scoreFollower has
        to stop (and why) or not.

        See example of a bad prediction at the beginning of the song:

        >>> from time import time
        >>> from music21.audioSearch import scoreFollower
        >>> scNotes = corpus.parse('luca/gloria').parts[0].flatten().notes.stream()
        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.begins = True
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.countdown = 0
        >>> prob = 0.5  # bad prediction
        >>> totalLengthPeriod = 15
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(ScF.startSearchAtSlot)
        0

        Different examples for different countdowns:

        Countdown = 0:

        The last matching was good, so it calculates the position in which it
        starts to search at, and the position in which the music should start.

        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.scoreNotesOnly = scNotes.flatten().notesAndRests
        >>> ScF.begins = False
        >>> ScF.countdown = 0
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.lastNotePosition = 38
        >>> ScF.predictedNotePosition = 19
        >>> ScF.seconds_recording = 10
        >>> prob = 0.8
        >>> totalLengthPeriod = 25
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(ScF.startSearchAtSlot)
        38

        >>> ScF.predictedNotePosition >=38
        True

        Countdown = 1:

        Now it doesn't change the slot in which it starts to search at.
        It also predicts the position in which the music should start.

        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.begins = False
        >>> ScF.countdown = 1
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.lastNotePosition = 15
        >>> ScF.predictedNotePosition = 19
        >>> ScF.seconds_recording = 10
        >>> prob = 0.8
        >>> totalLengthPeriod = 25
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(ScF.startSearchAtSlot)
        15

        >>> ScF.predictedNotePosition > 15
        True

        Countdown = 2:

        Now it starts searching at the beginning of the page of the screen.
        The note prediction is also the beginning of the page.

        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.begins = False
        >>> ScF.countdown = 2
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.lastNotePosition = 15
        >>> ScF.predictedNotePosition = 19
        >>> ScF.seconds_recording = 10
        >>> prob = 0.8
        >>> totalLengthPeriod = 25
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(ScF.startSearchAtSlot)
        15

        >>> print(ScF.predictedNotePosition)
        39

        Countdown = 4:

        Now it starts searching at the beginning of the page of the screen.
        The note prediction is also the beginning of the page.

        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.begins = False
        >>> ScF.countdown = 4
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.lastNotePosition = 15
        >>> ScF.predictedNotePosition = 19
        >>> ScF.seconds_recording = 10
        >>> prob = 0.8
        >>> totalLengthPeriod = 25
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(ScF.startSearchAtSlot)
        0

        >>> print(ScF.predictedNotePosition)
        0

        Countdown = 5:

        Now it stops the program.

        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.begins = False
        >>> ScF.countdown = 5
        >>> ScF.startSearchAtSlot = 15
        >>> ScF.lastNotePosition = 15
        >>> ScF.predictedNotePosition = 19
        >>> ScF.seconds_recording = 10
        >>> prob = 0.8
        >>> totalLengthPeriod = 25
        >>> time_start = time()
        >>> exitType = ScF.updatePosition(prob, totalLengthPeriod, time_start)
        >>> print(exitType)
        countdownExceeded

        '''
        pass

    def getFirstSlotOnScreen(self):
        '''
        Returns the index of the first element on the screen right now.

        Doesn't work. (maybe it's not necessary)
        '''
        pass

    def predictNextNotePosition(self, totalLengthPeriod, totalSeconds):
        '''
        It predicts the position in which the first note of the following
        recording note should start, taking into account the processing time of
        the computer.  It has two inputs: totalLengthPeriod, that is the number
        of pulses or beats in the recorded audio, and totalSeconds, that is the
        length in seconds of the processing time.

        It returns a number with the position of the predicted note in the
        score.

        >>> from time import time
        >>> from music21.audioSearch import scoreFollower
        >>> scNotes = corpus.parse('luca/gloria').parts[0].flatten().notes.stream()
        >>> ScF = scoreFollower.ScoreFollower(scoreStream=scNotes)
        >>> ScF.scoreNotesOnly = ScF.scoreStream.flatten().notesAndRests
        >>> ScF.lastNotePosition = 14
        >>> ScF.seconds_recording = 10.0
        >>> totalLengthPeriod = 8
        >>> totalSeconds = 2.0
        >>> predictedStartPosition = ScF.predictNextNotePosition(
        ...     totalLengthPeriod, totalSeconds)
        >>> print(predictedStartPosition)
        18

        '''
        pass

    def matchingNotes(
        self,
        scoreStream,
        transcribedScore,
        notePrediction,
        lastNotePosition,
    ):
        pass


# -----------------------------------------------------------------------------


class TestExternal(unittest.TestCase):

    def xtestRunScoreFollower(self):
        pass


# -----------------------------------------------------------------------------


if __name__ == '__main__':
    import music21
    music21.mainTest(TestExternal)


