# ------------------------------------------------------------------------------
# Name:         examples.py
# Purpose:      Transcribing popular music into braille music using music21.
# Authors:      Jose Cabal-Ugaz
#
# Copyright:    Copyright © 2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
The melody to the "Happy Birthday" song, in G major and 3/4 time.


>>> from music21.braille import examples
>>> hb = examples.happyBirthday()
>>> #_DOCS_SHOW hb.show('braille')
⠀⠀⠀⠀⠀⠀⠠⠃⠗⠊⠛⠓⠞⠇⠽⠲⠀⠹⠶⠼⠁⠃⠚⠀⠩⠼⠉⠲⠀⠀⠀⠀⠀⠀
⠼⠁⠀⠐⠑⠄⠵⠫⠱⠀⠳⠟⠀⠑⠄⠵⠫⠱⠀⠪⠗⠀⠑⠄⠵⠨⠱⠺⠀⠓⠄⠷⠻⠫
⠀⠀⠨⠙⠄⠽⠺⠳⠀⠪⠗⠣⠅


A piano reduction of Giuseppi Verdi's famous aria from the opera
Rigoletto, "La Donna É Mobile," in Bb major and 3/8 time.


>>> verdi = corpus.parse('verdi/laDonnaEMobile')
>>> #_DOCS_SHOW verdi.show('braille')
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⠣⠼⠉⠦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠁⠀⠨⠜⠄⠜⠁⠇⠇⠑⠛⠗⠑⠞⠞⠕⠜⠋⠄⠍⠀⠦⠨⠑⠦⠑⠦⠑⠀⠀
⠀⠀⠀⠸⠜⠘⠚⠸⠛⠼⠴⠛⠼⠴⠀⠀⠀⠀⠀⠀⠀⠀⠘⠚⠸⠛⠼⠴⠛⠼⠴
⠀⠉⠀⠨⠜⠨⠦⠨⠿⠄⠉⠏⠉⠹⠀⠀⠀⠀⠀⠀⠀⠨⠙⠙⠙⠀⠀⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠛⠬⠒⠛⠬⠒⠣⠜⠘⠻⠄⠀⠘⠛⠸⠛⠬⠒⠛⠬⠒
⠀⠑⠀⠨⠜⠨⠦⠨⠯⠄⠉⠕⠉⠺⠀⠀⠀⠀⠀⠀⠀⠦⠨⠑⠦⠙⠦⠚⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠛⠼⠴⠛⠼⠴⠣⠜⠘⠻⠄⠀⠘⠛⠸⠛⠼⠴⠛⠼⠴
⠀⠛⠀⠨⠜⠐⠾⠄⠉⠎⠪⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠙⠉⠚⠉⠓⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠛⠔⠒⠛⠔⠒⠣⠜⠘⠻⠄⠀⠘⠛⠸⠛⠔⠒⠛⠔⠒
⠀⠊⠀⠨⠜⠐⠷⠄⠉⠟⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⠋⠋⠄⠦⠨⠑⠦⠑⠦⠑
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠛⠼⠴⠛⠼⠴⠣⠜⠘⠺⠄⠀⠘⠾⠸⠛⠾⠬⠛⠾⠬⠛⠀
⠁⠁⠀⠨⠜⠨⠦⠨⠿⠄⠉⠏⠉⠹⠀⠀⠀⠀⠀⠀⠀⠀⠨⠙⠙⠙⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠍⠸⠿⠮⠔⠿⠮⠔⠿⠣⠜⠘⠻⠄⠀⠘⠿⠸⠛⠮⠔⠛⠮⠔⠛
⠁⠉⠀⠨⠜⠨⠦⠨⠯⠄⠉⠕⠉⠺⠀⠀⠀⠀⠀⠀⠀⠀⠦⠨⠑⠉⠦⠙⠉⠦⠚⠀
⠀⠀⠀⠸⠜⠄⠄⠍⠸⠿⠾⠬⠿⠾⠬⠿⠣⠜⠘⠺⠄⠀⠘⠾⠸⠛⠾⠬⠛⠾⠬⠛
⠁⠑⠀⠨⠜⠐⠾⠄⠉⠎⠪⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠙⠉⠚⠉⠓⠀⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠍⠸⠿⠮⠔⠿⠮⠔⠿⠣⠜⠘⠻⠄⠀⠘⠿⠸⠛⠮⠔⠛⠮⠔⠛
⠁⠛⠀⠨⠜⠐⠷⠄⠉⠟⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠽⠄⠉⠕⠉⠙⠙⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠍⠸⠿⠾⠬⠿⠾⠬⠿⠣⠜⠘⠺⠄⠀⠜⠍⠋⠸⠋⠓⠬⠼⠓⠬⠼
⠁⠊⠀⠨⠜⠨⠿⠴⠍⠹⠬⠔⠀⠀⠀⠀⠀⠀⠀⠨⠵⠄⠉⠏⠉⠑⠑⠀⠀⠡⠨⠷⠴⠍⠱⠬⠔⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠊⠬⠊⠬⠣⠜⠸⠻⠄⠀⠣⠸⠓⠊⠬⠼⠊⠬⠼⠀⠭⠸⠚⠬⠚⠬⠣⠜⠸⠳⠄
⠃⠃⠀⠨⠜⠨⠿⠄⠉⠗⠉⠛⠛⠀⠜⠋⠋⠨⠳⠴⠛⠀⠦⠨⠯⠦⠿⠦⠯⠵⠍⠽⠍⠀⠀
⠀⠀⠀⠸⠜⠸⠊⠙⠬⠼⠙⠬⠼⠀⠸⠺⠄⠬⠀⠀⠀⠀⠸⠯⠬⠴⠍⠿⠼⠴⠍⠿⠬⠒⠍
⠃⠑⠀⠨⠜⠐⠺⠜⠍⠋⠨⠿⠄⠉⠰⠟⠀⠰⠻⠨⠿⠄⠉⠰⠟⠣⠜⠧⠄⠀
⠀⠀⠀⠸⠜⠸⠚⠬⠚⠬⠭⠀⠀⠀⠀⠀⠀⠭⠸⠛⠬⠔⠭⠣⠜⠸⠻⠄⠬⠔
⠃⠛⠀⠨⠜⠰⠻⠨⠿⠄⠉⠰⠟⠀⠀⠀⠀⠀⠀⠰⠯⠿⠯⠦⠵⠍⠦⠽⠍⠀⠀⠀
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠚⠬⠭⠣⠜⠸⠺⠄⠬⠀⠸⠯⠬⠴⠍⠿⠼⠴⠍⠿⠬⠒⠍
⠃⠊⠀⠨⠜⠨⠺⠜⠋⠨⠿⠄⠉⠰⠟⠀⠀⠀⠰⠯⠉⠨⠮⠉⠰⠿⠉⠋⠨⠿⠄⠉⠰⠟⠣⠜⠧⠄
⠀⠀⠀⠸⠜⠘⠾⠸⠿⠼⠴⠛⠼⠴⠛⠼⠴⠀⠭⠸⠛⠬⠒⠛⠬⠒⠣⠜⠘⠻⠄⠀⠀⠀⠀⠀⠀⠀
⠉⠁⠀⠨⠜⠰⠵⠉⠨⠿⠉⠰⠿⠉⠑⠨⠿⠄⠉⠰⠟
⠀⠀⠀⠸⠜⠄⠄⠭⠸⠛⠼⠴⠛⠼⠴⠣⠜⠘⠻⠄⠀
⠉⠃⠀⠨⠜⠰⠃⠆⠰⠯⠨⠮⠰⠿⠯⠨⠮⠰⠿⠯⠨⠮⠰⠿⠀⠨⠚⠘⠆⠭⠩⠛
⠀⠀⠀⠸⠜⠘⠛⠸⠛⠔⠒⠛⠔⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠚⠬⠧⠀⠀⠀
⠉⠙⠀⠨⠜⠄⠜⠋⠋⠰⠃⠨⠦⠨⠮⠄⠗⠿⠄⠏⠵⠄⠝⠀⠐⠾⠘⠆⠍⠜⠋⠋⠋⠨⠚⠼⠴⠭⠣⠅
⠀⠀⠀⠸⠜⠄⠄⠄⠧⠸⠛⠬⠒⠣⠜⠸⠫⠄⠬⠴⠀⠀⠀⠀⠸⠾⠬⠍⠘⠚⠬⠔⠭⠣⠅⠀⠀⠀⠀⠀


The exposition to movement 1 of Mozart's K545.


>>> #_DOCS_SHOW mozart = converter.parse('mozart_k545_exposition.xml')
>>> #_DOCS_SHOW mozart.show('braille')
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠙⠲⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠁⠀⠨⠜⠄⠜⠁⠇⠇⠑⠛⠗⠕⠨⠝⠫⠳⠀⠐⠺⠄⠉⠽⠉⠵⠹⠧⠀⠨⠎⠳⠰⠹⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠸⠜⠐⠙⠓⠋⠓⠙⠓⠋⠓⠀⠀⠀⠀⠀⠐⠑⠓⠛⠓⠙⠓⠋⠓⠀⠐⠙⠐⠊⠛⠊⠐⠙⠓⠋⠓
⠀⠙⠀⠨⠜⠨⠳⠛⠉⠯⠉⠿⠫⠧⠀⠀⠐⠊⠾⠽⠵⠋⠛⠓⠮⠓⠛⠋⠵⠙⠚⠊
⠀⠀⠀⠸⠜⠸⠚⠐⠓⠑⠓⠙⠓⠋⠓⠀⠐⠻⠧⠧⠸⠻⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠋⠀⠨⠜⠐⠓⠮⠾⠽⠑⠋⠛⠷⠛⠋⠑⠽⠚⠊⠓⠀⠐⠛⠷⠮⠾⠙⠑⠋⠿⠋⠑⠙⠾⠊⠓⠛
⠀⠀⠀⠸⠜⠸⠫⠴⠧⠧⠫⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠱⠴⠧⠧⠱⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠓⠀⠨⠜⠐⠋⠿⠷⠮⠚⠙⠑⠯⠑⠙⠚⠮⠓⠛⠋⠀⠐⠑⠯⠿⠷⠊⠚⠩⠙⠵⠐⠊⠚⠙⠵⠋⠛⠓
⠀⠀⠀⠸⠜⠸⠹⠤⠧⠧⠹⠬⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠬⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠁⠚⠀⠨⠜⠨⠮⠚⠙⠚⠮⠓⠛⠋⠿⠓⠊⠓⠿⠋⠑⠙
⠀⠀⠀⠸⠜⠸⠻⠄⠓⠪⠄⠩⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠁⠁⠀⠨⠜⠐⠚⠨⠓⠋⠙⠑⠓⠋⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠱⠳⠼⠴⠐⠳⠧⠣⠅
⠀⠀⠀⠸⠜⠘⠷⠚⠑⠓⠘⠷⠸⠙⠋⠓⠘⠷⠚⠑⠓⠘⠷⠸⠙⠋⠓⠀⠘⠳⠸⠳⠘⠳⠧⠣⠅⠀




>>> print(braille.translate.objectToBraille(verdi.measures(1, 3), debug=True))
---begin grand segment---
<music21.braille.segment BrailleGrandSegment>
===
Measure 1 Right, Signature Grouping 1:
Key Signature 2 flat(s) ⠣⠣
Time Signature 3/8 ⠼⠉⠦
<BLANKLINE>
Measure 1 Left, Signature Grouping 1:
B- major
<music21.meter.TimeSignature 3/8>
====
Measure 1 Right, Note Grouping 1:
<music21.clef.TrebleClef>
Word ⠜
Text Expression Allegretto ⠁⠇⠇⠑⠛⠗⠑⠞⠞⠕
Word: ⠜
Dynamic f ⠋
Dot 3 ⠄
Rest whole ⠍
<BLANKLINE>
Measure 1 Left, Note Grouping 1:
<music21.clef.BassClef>
Octave 2 ⠘
B eighth ⠚
Ascending Chord:
Octave 3 ⠸
F eighth ⠛
Interval 4 ⠼
Interval 6 ⠴
Ascending Chord:
F eighth ⠛
Interval 4 ⠼
Interval 6 ⠴
** Grouping x 2 **
====
Measure 2 Right, Note Grouping 1:
Articulation staccato ⠦
Octave 5 ⠨
D eighth ⠑
Articulation staccato ⠦
D eighth ⠑
Articulation staccato ⠦
D eighth ⠑
<BLANKLINE>
====
Measure 3 Right, Note Grouping 1:
Articulation accent ⠨⠦
Octave 5 ⠨
F 16th ⠿
Dot ⠄
Opening single slur ⠉
E 32nd ⠏
Opening single slur ⠉
C quarter ⠹
<BLANKLINE>
Measure 3 Left, Inaccord Grouping 1:
Rest eighth ⠭
Ascending Chord:
Octave 3 ⠸
F eighth ⠛
Interval 3 ⠬
Interval 7 ⠒
Ascending Chord:
F eighth ⠛
Interval 3 ⠬
Interval 7 ⠒
full inaccord ⠣⠜
Octave 2 ⠘
F quarter ⠻
Dot ⠄
====
<BLANKLINE>
---end grand segment---
'''
from __future__ import annotations

import unittest

from music21 import key
from music21 import note
from music21 import tempo
from music21 import converter

def cp(strIn):
    pass

def happyBirthday():
    '''
    fully copyright free!
    '''
    pass

# ------------------------------------------------------------------------------
class Test(unittest.TestCase):

    def testHappyBirthdayDebug(self):
        pass

    def testVerdiDebug(self):
        # self.maxDiff = None
        pass


    def testVoices(self):
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , runTest='testVoices')

