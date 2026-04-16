# ------------------------------------------------------------------------------
# Name:         audioSearch.transcriber.py
# Purpose:      Automatically transcribe melodies from a microphone or
#               wave file and output them as a score
#
# Authors:      Jordi Bartolome
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
from __future__ import annotations

import unittest

from music21 import environment
from music21 import scale

environLocal = environment.Environment('audioSearch.transcriber')


def runTranscribe(show=True, plot=True, useMic=True,
                  seconds=20.0, useScale=None, saveFile=True):  # pragma: no cover
    '''
    runs all the methods to record from audio for `seconds` length (default 10.0)
    and transcribe the resulting melody returning a music21.Score object

    if `show` is True, show the stream.

    if `plot` is True, then a Tk graph of the frequencies will be displayed.

    if `useMic` is True then use the microphone.  If False it will load the file of `saveFile`
    or the default temp file to run transcriptions from.

    a different scale than the chromatic scale can be specified by setting `useScale`.
    See :ref:`moduleScale` for a list of allowable scales. (or a custom one can be given).
    Microtonal scales are totally accepted, as are retuned scales where A != 440hz.

    if `saveFile` is False, then the recorded audio is saved to disk.  If
    set to `True` then `environLocal.getRootTempDir() / 'ex.wav'` is
    used as the filename.  If set to anything else then it will use that as the
    filename.
    '''
    pass


def monophonicStreamFromFile(fileName, useScale=None):
    '''
    Reads in a .wav file and returns a stream representing the transcribed, monophonic audio.

    `fileName` should be the complete path to a file on the disk.

    A different scale than the chromatic scale can be specified by setting `useScale`.
    See :ref:`moduleScale` for a list of allowable scales. (or a custom one can be given).
    Microtonal scales are totally accepted, as are retuned scales where A != 440hz.

    We demonstrate with an audio file beginning with an ascending scale.

    >>> import os #_DOCS_HIDE
    >>> taw = 'test_audio.wav' #_DOCS_HIDE
    >>> waveFile = str(common.getSourceFilePath() / 'audioSearch' / taw) #_DOCS_HIDE
    >>> #_DOCS_SHOW waveFile = 'test_audio.wav'
    >>> p = audioSearch.transcriber.monophonicStreamFromFile(waveFile)
    >>> p
    <music21.stream.Part ...>
    >>> p.show('text')
    {0.0} <music21.note.Note C>
    {0.25} <music21.note.Note C>
    {0.75} <music21.note.Note D>
    {1.75} <music21.note.Note E>
    {2.75} <music21.note.Note F>
    {4.25} <music21.note.Note G>
    {5.25} <music21.note.Note A>
    {6.25} <music21.note.Note B>
    {7.25} <music21.note.Note C>
    ...
    '''
    pass


class TestExternal(unittest.TestCase):

    def x_testRunTranscribe(self):
        pass

    def x_testTranscribePachelbel(self):
        pass
        # _myScore = runTranscribe(useMic=False, saveFile=saveFile, plot=False, show=False)
        # myScore.show()


if __name__ == '__main__':
    import music21
    music21.mainTest(TestExternal)


