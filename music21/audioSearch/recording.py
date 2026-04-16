# ------------------------------------------------------------------------------
# Name:         audioSearch.recording.py
# Purpose:      routines for making recordings from microphone input
#
# Authors:      Jordi Bartolome
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2011-25 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
modules for audio searching that directly record from the microphone.

Requires PyAudio and portaudio to be installed (https://www.portaudio.com/download.html)

Windows users will get pyaudio and portaudio with `pip install pyaudio`

macOS users should have Homebrew installed and run `brew install portaudio`
before running `pip install pyaudio`

There is no official support for Linux/BSD etc. in music21, but package managers like `apt`
tend to have libraries like `portaudio19` and `python3-pyaudio`.
'''
from __future__ import annotations

from importlib.util import find_spec
import unittest
import wave

from music21.common.types import DocOrder
from music21 import environment
from music21 import exceptions21

environLocal = environment.Environment('audioSearch.recording')

default_recordChannels = 1
default_recordSampleRate = 44100
default_recordChunkLength = 1024


def samplesFromRecording(seconds=10.0, storeFile=True,
                         recordFormat=None,
                         recordChannels=default_recordChannels,
                         recordSampleRate=default_recordSampleRate,
                         recordChunkLength=default_recordChunkLength):  # pragma: no cover
    '''
    records `seconds` length of sound in the given format (default Wave)
    and optionally stores it to disk using the filename of `storeFile`

    Returns a list of samples.
    '''
    pass


class RecordingException(exceptions21.Music21Exception):
    pass


# -----------------------------------------
class Test(unittest.TestCase):
    pass

class TestExternal(unittest.TestCase):  # pragma: no cover
    loader = find_spec('pyaudio')
    if loader is not None:  # pragma: no cover
        pyaudio_installed = True
    else:
        pyaudio_installed = False

    @unittest.skipUnless(pyaudio_installed, 'pyaudio must be installed')
    def testRecording(self):
        '''
        record one second of data and print 10 records
        '''
        pass


# ------------------------------------------------------------------------------
# define presented order in documentation
_DOC_ORDER: DocOrder = []


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)
