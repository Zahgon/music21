# ------------------------------------------------------------------------------
# Name:         corpus/chorales.py
# Purpose:      Access to the chorale collection
#
# Authors:      Michael Scott Asato Cuthbert
#               Evan Lynch
#
# Copyright:    Copyright © 2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
This file makes it easier to access Bach's chorales through various
numbering schemes and filters and includes the corpus.chorales.Iterator()
class for easily iterating through the chorale collection.
'''
from __future__ import annotations

import copy
import unittest

from music21 import common
from music21 import environment
from music21 import exceptions21
from music21 import metadata

environLocal = environment.Environment('corpus.chorales')


class ChoraleList:
    # noinspection SpellCheckingInspection
    '''
    A searchable list of Bach's chorales by various numbering systems:

    Note that multiple chorales share the same title, so it's best to
    iterate over one of the other lists to get them all.

    The list of chorales comes from
    https://en.wikipedia.org/wiki/List_of_chorale_harmonisations_by_Johann_Sebastian_Bach
    which does not have all chorales in the Bärenreitter-Kirnberger or Riemenschneider
    numberings since it only includes BWV 250-438.

    >>> bcl = corpus.chorales.ChoraleList()
    >>> info358 = bcl.byBudapest[358]
    >>> for key in sorted(list(info358)):
    ...   print(f'{key} {info358[key]}')
    baerenreiter 68
    budapest 358
    bwv 431
    kalmus 358
    notes None
    riemenschneider 68
    title Wenn wir in höchsten Nöten sein
    >>> #_DOCS_SHOW c = corpus.parse('bach/bwv' + str(info358['bwv']))
    >>> #_DOCS_SHOW c.show()  # shows Bach BWV431

    More fully:

    >>> b = corpus.parse('bwv' + str(corpus.chorales.ChoraleList().byRiemenschneider[2]['bwv']))
    >>> b
    <music21.stream.Score ...>
    '''

    def __init__(self):
        self.byTitle = {}
        self.byBWV = {}
        self.byKalmus = {}
        self.byBaerenreiter = {}
        self.byBudapest = {}
        self.byRiemenschneider = {}

        self.prepareList()

    # noinspection SpellCheckingInspection
    def prepareList(self):
        '''
        puts a list of Bach Chorales into dicts of dicts called

        self.byBudapest
        self.byBWV
        self.byRiemenschneider

        etc.
        '''
        pass


class ChoraleListRKBWV:
    # noinspection SpellCheckingInspection
    '''
    A searchable list of Bach's chorales by various numbering systems:

    Note that multiple chorales share the same title, so it's best to
    iterate over one of the other lists to get them all.

    The list of chorales comes from Margaret Greentree (formerly at
    jsbchorales.net) who compiled
    all chorales in the corpus, but only had numbers for the `kalmus`,
    `riemenschneider`, and `bwv` numbering systems.

    >>> bcl = corpus.chorales.ChoraleListRKBWV()
    >>> info155 = bcl.byRiemenschneider[155]
    >>> for key in sorted(list(info155)):
    ...   print(f'{key} {info155[key]}')
    bwv 344
    kalmus 173
    riemenschneider 155
    title Hilf, Herr Jesu, laß gelingen
    >>> #_DOCS_SHOW c = corpus.parse('bach/bwv' + str(info155['bwv']))
    >>> #_DOCS_SHOW c.show()  # shows Bach BWV344

    More fully:

    >>> theNumber = corpus.chorales.ChoraleListRKBWV().byRiemenschneider[2]['bwv']
    >>> b = corpus.parse('bwv' + str(theNumber))
    >>> b
    <music21.stream.Score ...>
    '''

    def __init__(self):
        self.byTitle = {}
        self.byBWV = {}
        self.byKalmus = {}
        self.byRiemenschneider = {}
        self.prepareList()

    # noinspection SpellCheckingInspection
    def prepareList(self):
        '''
        puts a list of Bach Chorales into dicts of dicts called

        self.byKalmus
        self.byBWV
        self.byRiemenschneider
        self.byTitle
        '''
        pass


class Iterator:
    # noinspection SpellCheckingInspection
    '''
    This is a class for iterating over many Bach Chorales. It is designed
    to make it easier to use
    one of music21's most accessible datasets. It will parse each chorale
    in the selected
    range in a lazy fashion so that a list of chorales need not be parsed up front. To select a
    range of chorales, first select a .numberingSystem
    ('riemenschneider', 'bwv', 'kalmus', 'budapest',
    'baerenreiter', or 'title'). Then, set .currentNumber to the lowest
    number in the range and
    .highestNumber to the highest in the range. This can either be done by catalogue number
    (iterationType = 'number') or by index (iterationType = 'index').

    Note that these numbers are 1-indexed (as most catalogues are) and
    unlike Python's range feature, the final number is included.

    Changing the numberingSystem will reset the iterator and
    change the range values to span the entire numberList.
    The iterator can be initialized with three parameters
    (currentNumber, highestNumber, numberingSystem). For example
    corpus.chorales.Iterator(1, 26,'riemenschneider') iterates
    through the riemenschneider numbered chorales from 1 to 26.
    Additionally, the following keywords can be set:

    * `returnType` = either 'stream' (default) or 'filename'
    * `iterationType` = either 'number' or 'index'
    * `titleList` = [list, of, titles]
    * `numberList` = [list, of, numbers]

    >>> for chorale in corpus.chorales.Iterator(1, 4, returnType='filename'):
    ...    print(chorale)
    bach/bwv269
    bach/bwv347
    bach/bwv153.1
    bach/bwv86.6

    >>> BCI = corpus.chorales.Iterator()
    >>> BCI.numberingSystem
    'riemenschneider'

    >>> BCI.currentNumber
    1

    >>> BCI.highestNumber
    371

    An Exception will be raised if the number set is not in the
    numbering system selected, or if the numbering system selected is not valid.

    >>> BCI.currentNumber = 377
    Traceback (most recent call last):
    ...
    music21.corpus.chorales.BachException: 377 does not correspond to a
        chorale in the riemenschneider numbering system

    >>> BCI.numberingSystem = 'not a numbering system'
    Traceback (most recent call last):
    ...
    music21.corpus.chorales.BachException: not a numbering system is not a valid
        numbering system for Bach Chorales.

    If the numberingSystem 'title' is selected, the iterator must be
    initialized with a list of titles.
    It will iterate through the titles in the order of the list.

    >>> BCI.numberingSystem = 'title'
    >>> BCI.returnType = 'filename'
    >>> BCI.titleList = ['Jesu, meine Freude',
    ...                  'Gott hat das Evangelium',
    ...                  'Not a Chorale']
    'Not a Chorale' will be skipped because it is not a recognized title.

    >>> for chorale in BCI:
    ...    print(chorale)
    bach/bwv358
    bach/bwv319

    The numberList, which, by default, includes all chorales in the chosen numberingSystem,
    can be set like the titleList. In the following example,
    note that the first chorale in the given
    numberList will not be part of the iteration because the
    first currentNumber is set to 2 at the
    start by the first argument. (If `iterationType=='index'`,
    setting the currentNumber to 1 and the highestNumber to 7
    would have the same effect as the given example.

    >>> BCI = corpus.chorales.Iterator(2, 371, numberingSystem='riemenschneider',
    ...                                numberList=[1, 2, 3, 4, 6, 190, 371, 500],
    ...                                returnType='filename')
    500 will be skipped because it is not in the numberingSystem riemenschneider

    >>> for chorale in BCI:
    ...    print(chorale)
    bach/bwv347
    bach/bwv153.1
    bach/bwv86.6
    bach/bwv281
    bach/bwv337
    bach/bwv278

    Elements in the iterator can be accessed by index as well as slice.

    >>> for chorale in corpus.chorales.Iterator(returnType='filename')[4:10]:
    ...    print(chorale)
    bach/bwv86.6
    bach/bwv267
    bach/bwv281
    bach/bwv17.7
    bach/bwv40.8
    bach/bwv248.12-2
    bach/bwv38.6

    >>> print(corpus.chorales.Iterator(returnType='filename')[55])
    bach/bwv121.6

    For the first 20 chorales in the Riemenschneider numbering system, there are professionally
    annotated roman numeral analyses in romanText format, courtesy of Dmitri Tymoczko of Princeton
    University.  To get them as an additional part to the score set returnType to "stream", and
    add a keyword "analysis = True":

    If chorales are accessed through the Iterator(), the metadata.title attribute will have the
    correct German title. This is different from the metadata returned by the parser which does
    not give the German title but rather the BWV number.

    >>> corpus.chorales.Iterator(returnType='stream')[1].metadata.title
    'Ich dank’ dir, lieber Herre'
    '''
    _DOC_ORDER = ['numberingSystem', 'currentNumber', 'highestNumber',
                  'titleList', 'numberList', 'returnType', 'iterationType']

    def __init__(self,
                 currentNumber: int|None = None,
                 highestNumber: int|None = None,
                 *,
                 numberingSystem: str = 'riemenschneider',
                 returnType: str = 'stream',
                 iterationType: str = 'number',
                 analysis: bool = False,
                 numberList: list[int]|None = None,
                 titleList: list[str]|None = None,
                 ):
        '''
        By default: numberingSystem = 'riemenschneider', currentNumber = 1,
        highestNumber = 371, iterationType = 'number',
        and returnType = 'stream'

        Notes:

        Two ChoraleList objects are created. These should probably
        be consolidated, but they contain
        different information at this time. Also, there are problems
        with entries in ChoraleListRKBWV
        that need to be addressed. Namely, chorales that share the
        same key (and thus overwrite each other)
        and chorales that do not appear to be in the corpus at all.
        '''
        self._currentIndex = None
        self._highestIndex = None
        self._titleList: list[str] = []
        self._numberList = None
        self._numberingSystem = None
        self._returnType = 'stream'
        self._iterationType = 'number'
        self.analysis = analysis

        self._choraleList1 = ChoraleList()  # For budapest, baerenreiter
        self._choraleList2 = ChoraleListRKBWV()  # for kalmus, riemenschneider, title, and bwv

        self.numberingSystem = numberingSystem  # This assignment must come before the keywords

        self.returnType = returnType
        self.iterationType = iterationType

        if numberList is not None:
            # TODO: overly complex order of setting
            self.numberList = numberList

        if titleList is not None:
            # TODO: overly complex order of setting
            self.titleList = titleList

        # These assignments must come after .iterationType

        self.currentNumber = currentNumber
        self.highestNumber = highestNumber

    def __iter__(self):
        return self

    def __len__(self):
        if self.numberingSystem is None:
            raise BachException('NumberingSystem not set. Cannot find a length.')
        if self.numberingSystem == 'title':
            return len(self.titleList)
        else:
            return len(self.numberList)

    def __getitem__(self, key):
        if isinstance(key, slice):
            returnObj = copy.deepcopy(self)
            returnObj.currentNumber = key.start
            returnObj.highestNumber = key.stop
            return returnObj
        else:
            if self.numberingSystem is None:
                raise BachException('NumberingSystem not set. Cannot find index.')

            if self.numberingSystem == 'title':
                if key in range(len(self.titleList)):
                    return self._returnChorale(key)
                else:
                    raise IndexError(f'{key} is not in the range of the titleList.')

            elif self.iterationType == 'index' or self.numberingSystem == 'bwv':
                if key in range(len(self.numberList)):
                    return self._returnChorale(key)
                else:
                    raise IndexError(f'{key} is not in the range of the numberList.')
            elif self.iterationType == 'number':
                if key in self.numberList:
                    return self._returnChorale(key)
                else:
                    raise IndexError(f'{key} is not in the numberList')

    def __next__(self):
        '''
        At each iteration, the _currentIndex is incremented, and the
        next chorale is parsed based upon its bwv number which is queried via
        whatever the current numberingSystem is set to. If the
        _currentIndex becomes higher than the _highestIndex, the iteration stops.
        '''
        if self._currentIndex > self._highestIndex:
            raise StopIteration()
        nextChorale = self._returnChorale()
        self._currentIndex += 1
        return nextChorale

    # ### Private Methods

    def _returnChorale(self, choraleIndex=None):
        # noinspection SpellCheckingInspection
        '''
        This returns a chorale based upon the _currentIndex
        and the numberingSystem. The numberList is the list
        of valid numbers in the selected numbering system.
        The _currentIndex is the location in the numberList
        of the current iteration. If the numberingSystem == 'title',
        the chorale is instead queried by Title
        from the titleList and the numberList is ignored.

        >>> BCI = corpus.chorales.Iterator()
        >>> riemenschneider1 = BCI._returnChorale()
        >>> riemenschneider1.metadata.title
        'Aus meines Herzens Grunde'

        >>> BCI.currentNumber = BCI.highestNumber
        >>> riemenschneider371 = BCI._returnChorale()
        >>> riemenschneider371.metadata.title
        'Christ lag in Todesbanden'


        >>> BCI.numberingSystem = 'title'
        >>> BCI._returnChorale()
        Traceback (most recent call last):
        ...
        music21.corpus.chorales.BachException: Cannot parse Chorales because no titles to parse.

        >>> BCI.titleList = ['Christ lag in Todesbanden', 'Aus meines Herzens Grunde']
        >>> christlag = BCI._returnChorale()
        >>> christlag.show('text')
        {0.0} <music21.text.TextBox 'PDF © 2004...'>
        {0.0} <music21.text.TextBox 'BWV 278'>
        {0.0} <music21.metadata.Metadata object at ...>
        {0.0} <music21.stream.Part Soprano>
            {0.0} <music21.instrument.Instrument 'P1: Soprano: '>
            {0.0} <music21.stream.Measure 0 offset=0.0>
                {0.0} <music21.layout.SystemLayout>
                {0.0} <music21.clef.TrebleClef>
                {0.0} <music21.key.Key of e minor>
                {0.0} <music21.meter.TimeSignature 4/4>
                {0.0} <music21.note.Note B>
        ...

        >>> christlag.metadata.title
        'Christ lag in Todesbanden'

        >>> BCI.currentNumber += 1
        >>> ausMeines = BCI._returnChorale()
        >>> ausMeines.metadata.title
        'Aus meines Herzens Grunde'

        >>> BCI.numberingSystem = 'kalmus'
        >>> BCI.returnType = 'filename'
        >>> BCI._returnChorale()
        'bach/bwv253'

        >>> BCI._returnChorale(3)
        'bach/bwv48.3'
        '''
        pass

    @staticmethod
    def _bwvSort(bwv: str) -> float:
        '''
        This takes a string such as '69.6-a' and returns a float for sorting.
        '''
        pass

    def _initializeNumberList(self):
        '''
        This creates the _numberList which the iterator iterates through.
        It is called each time the numberingSystem
        changes and also whenever the titleList is set. The numbers are
        drawn from the chorale search objects,
        so any mistakes should be corrected there. Additionally, the
        initial values of currentNumber and highestNumber
        are set to the lowest and highest numbers in the selected list.
        If the numberingSystem == 'title', the _numberList
        is set to None, and the currentNumber and highestNumber are set
        to the lowest and highest indices in the titleList.

        >>> BCI = corpus.chorales.Iterator()
        >>> BCI.numberingSystem = 'riemenschneider'
        >>> (BCI._numberList[0], BCI._numberList[40], BCI._numberList[-1])
        (1, 41, 371)

        >>> BCI.numberingSystem = 'kalmus'
        >>> (BCI._numberList[0], BCI._numberList[40], BCI._numberList[-1])
        (1, 48, 389)

        >>> BCI.numberingSystem = 'bwv'
        >>> (BCI._numberList[14], BCI._numberList[96], BCI._numberList[-1])
        ('18.5-w', '145-a', '438')

        >>> BCI.numberingSystem = 'budapest'
        >>> (BCI._numberList[0], BCI._numberList[40], BCI._numberList[-1])
        (0, 68, 388)

        >>> BCI.numberingSystem = 'baerenreiter'
        >>> (BCI._numberList[0], BCI._numberList[40], BCI._numberList[-1])
        (1, 134, 370)

        >>> BCI.numberingSystem = 'title'
        >>> BCI._numberList
        '''
        pass

    # ---Properties
    # - Numbering System
    def _getNumberingSystem(self):
        pass

    def _setNumberingSystem(self, value):
        pass

    numberingSystem = property(_getNumberingSystem, _setNumberingSystem,
                               doc='''
                                    This property determines which numbering
                                    system to iterate through chorales with.
                                    It can be set to 'bwv', 'kalmus', 'baerenreiter',
                                    'budapest', or 'riemenschneider'.
                                    It can also be set to 'title' in which case the
                                    iterator needs to be given a list
                                    of chorale titles in .titleList. At this time,
                                    the titles need to be exactly as they
                                    appear in the dictionary it queries.''')

    # - Title List

    @property
    def titleList(self) -> list[str]:
        '''
        A list of titles to iterate over
        if `.numberingSystem` is set to 'title'.
        '''
        pass

    @titleList.setter
    def titleList(self, value: list[str]):
        pass

    # - Number List

    @property
    def numberList(self):
        '''
        Allows access to the catalogue numbers
        (or indices if iterationType == 'index')
        that will be iterated over. This can be
        set to a specific list of numbers.
        The list will be sorted.
        '''
        pass

    @numberList.setter
    def numberList(self, value):
        pass

    # - Current Number

    @property
    def currentNumber(self):
        '''
        The currentNumber is the number of the
        chorale (in the set numberingSystem) for the
        next chorale to be parsed by the iterator.
        It is initially the first chorale in whatever
        numberingSystem is set, but it can be changed
        to any other number in the numberingSystem
        as desired as long as it does not go above
        the highestNumber which is the boundary
        of the iteration.
        '''
        pass

    @currentNumber.setter
    def currentNumber(self, value):
        pass

    # - Highest Number

    @property
    def highestNumber(self):
        '''
        The highestNumber is the number of the chorale
        (in the set numberingSystem) for the
        last chorale to be parsed by the iterator.
        It is initially the highest numbered chorale in whatever
        numberingSystem is set, but it can be changed
        to any other number in the numberingSystem
        as desired as long as it does not go below
        the currentNumber of the iteration.
        '''
        pass

    @highestNumber.setter
    def highestNumber(self, value):
        pass

    # - Return Type
    @property
    def returnType(self):
        '''
        This property determines what the iterator
        returns; 'stream' is the default and causes the iterator to parse
        each chorale. If this is set to 'filename', the
        iterator will return the filename of each chorale but not
        parse it.
        '''
        pass

    @returnType.setter
    def returnType(self, value):
        pass

    # - Iteration Type
    @property
    def iterationType(self):
        '''
        This property determines how boundary numbers are
        interpreted, as indices or as catalogue numbers.
        '''
        pass

    @iterationType.setter
    def iterationType(self, value):
        pass


def getByTitle(title):
    # noinspection SpellCheckingInspection
    '''
    Return a Chorale by title (or title fragment) or None

    >>> germanTitle = "Sach' Gott heimgestellt"
    >>> c = corpus.chorales.getByTitle(germanTitle)
    >>> c.metadata.title
    "Ich hab' mein' Sach' Gott heimgestellt"
    '''
    pass


class BachException(exceptions21.Music21Exception):
    pass


class TestExternal(unittest.TestCase):
    show = True

    def testGetRiemenschneider1(self):
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest()  # External)
