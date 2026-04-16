# ------------------------------------------------------------------------------
# Name:         layout.py
# Purpose:      Layout objects
#
# Authors:      Christopher Ariza
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2010, 2012 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
The layout.py module contains two types of objects that specify the layout on
page (or screen) for Scores and other Stream objects.  There are two main types
of Layout objects: (1) layout describing elements and (2) layout defining Streams.

(1) ScoreLayout, PageLayout, SystemLayout, and StaffLayout objects describe the size of
pages, the geometry of page and system margins, the distance between staves, etc.
The model for these layout objects is taken directly (perhaps too directly?)
from MusicXML.  These objects all inherit from a BaseLayout class, primarily
as an aid to finding all of these objects as a group.  ScoreLayouts give defaults
for each page, system, and staff.  Thus, they contain PageLayout, SystemLayout, and
currently one or more StaffLayout objects (but probably just one. MusicXML allows more than
StaffLayout object because multiple staves can be in a Part.  Music21 uses
the concept of a PartStaff for a Part that is played by the same performer as another.
e.g., the left hand of the Piano is a PartStaff paired with the right hand).

PageLayout and SystemLayout objects also have a property, 'isNew',
which, if set to `True`, signifies that a new page
or system should begin here.  In theory, one could define new dimensions for a page
or system in the middle of the system or page without setting isNew to True, in
which case these measurements would start applying on the next page.  In practice,
there's really one good place to use these Layout objects and that's in the first part
in a score at offset 0 of the first measure on a page or system
(or for ScoreLayout, at the beginning
of a piece outside any parts).  But it's not an
error to put them in other places, such as at offset 0 of the first measure of a page
or system in all the other parts.  In fact, MusicXML tends to do this, and it ends up
not being a waste if a program extracts a single part from the middle of a score.

These objects are standard :class:`~music21.base.Music21Object` types, but many
properties such as .duration, .beat, will probably not apply.

When exporting to MusicXML (which is currently the only format in which music21 can and
does preserve these markings), many MusicXML readers will ignore these tags (or worse,
add a new page or system when PageLayout and SystemLayout objects are found but also
add theme wherever they want).  In Finale, this behavior disappears if the MusicXML
document notes that it <supports> new-page and new-system markings.  Music21 will add
the appropriate <supports> tags if the containing Stream has `.definesExplicitPageBreaks`
and `.definesExplicitSystemBreaks` set to True.  When importing a score that has the
<supports> tag set, music21 will set `.definesExplicitXXXXBreaks` to True for the
outer score and the inner parts.  However, this means that if the score is manipulated
enough that the prior layout information is obsolete, programs will need to set these
properties to False or move the Layout tags accordingly.

(2) The second set of objects are Stream subclasses that can be employed when a program
needs to easily iterate around the systems and pages defined through the layout objects
just described, or to get the exact position on a page (or a graphical representation
of a page) for a particular measure or system.  (Individual notes coming soon).  Normal
Score streams can be changed into LayoutStreams by calling `divideByPages(s)` on them.
A Score that was organized: Score->Part->Measure would then become:
LayoutScore->Page->System->Staff->Measure.

The new LayoutScore has methods that enable querying what page or system a measure is in, and
specifically where on a page a measure is (or the dimensions
of every measure in the piece).  However
do not call .show() on a LayoutScore -- the normal score it's derived from will work just fine.
Nor does calling .show() on a Page or System work yet, but once the LayoutStream has been created,
code like this can be done:

     s = stream.Stream(...)
     ls = layout.divideByPages(s)
     pg2sys3 = ls.pages[1].systems[2]  # n.b.! 1, 2
     measureStart, measureEnd = pg2sys3.measureStart, pg2sys3.measureEnd
     scoreExcerpt = s.measures(measureStart, measureEnd)
     scoreExcerpt.show()  # will show page 2, system 3

Note that while the coordinates given by music21 for a musicxml score (based on margins,
staff size, etc.)
generally reflect what is actually in a musicxml producer, unfortunately, x-positions are
far less accurately
produced by most editors.  For instance, Finale scores with measure sizes that have been
manually adjusted tend to show their
unadjusted measure width and not their actual measure width in the MusicXML.

SmartScore Pro tends to produce very good MusicXML layout data.
'''
from __future__ import annotations

# may need to have an object to convert between size units
import copy
import unittest

from collections import namedtuple
import typing as t

from music21 import base
from music21.common.enums import GatherSpanners
from music21 import environment
from music21 import exceptions21
from music21 import spanner
from music21 import stream
from music21.stream.enums import StaffType

environLocal = environment.Environment('layout')


SystemSize = namedtuple('SystemSize', ['top', 'left', 'right', 'bottom'])
PageSize = namedtuple('PageSize', ['top', 'left', 'right', 'bottom', 'width', 'height'])


class LayoutBase(base.Music21Object):
    '''
    A base class for all Layout objects, defining a classSortOrder
    and also an inheritance tree.

    >>> scoreLayout = layout.ScoreLayout()
    >>> isinstance(scoreLayout, layout.LayoutBase)
    True
    '''
    classSortOrder = -10

    def _reprInternal(self):
        pass

# ------------------------------------------------------------------------------


class ScoreLayout(LayoutBase):
    '''
    Parameters for configuring a score's layout.

    PageLayout objects may be found on Measure or Part Streams.

    >>> pl = layout.PageLayout(pageNumber=4, leftMargin=234, rightMargin=124,
    ...                        pageHeight=4000, pageWidth=3000, isNew=True)
    >>> pl.pageNumber
    4
    >>> pl.rightMargin
    124
    >>> pl.leftMargin
    234
    >>> pl.isNew
    True

    This object represents both <print new-page> and <page-layout>
    elements in musicxml.  The appearance tag is handled in the `.style`
    for the stream (it was here in v7 and before, but did nothing).

    Note that the appearance and style elements are subject to change during
    and after the v8 releases.
    '''
    # TODO -- make sure that the first pageLayout and systemLayout
    #     for each page are working together.

    def __init__(self,
                 *,
                 scalingMillimeters: int|float|None = None,
                 scalingTenths: int|float|None = None,
                 musicFont: str|None = None,
                 wordFont: str|None = None,
                 pageLayout: PageLayout|None = None,
                 systemLayout: SystemLayout|None = None,
                 staffLayoutList: list[StaffLayout]|None = None,
                 **keywords):
        super().__init__(**keywords)

        self.scalingMillimeters = scalingMillimeters
        self.scalingTenths = scalingTenths
        self.pageLayout: PageLayout|None = pageLayout
        self.systemLayout: SystemLayout|None = systemLayout
        self.staffLayoutList: list[StaffLayout] = []
        self.musicFont = musicFont
        self.wordFont = wordFont

        if staffLayoutList is not None:
            self.staffLayoutList = staffLayoutList

    def tenthsToMillimeters(self, tenths: int|float) -> int|float:
        '''
        given the scalingMillimeters and scalingTenths,
        return the value in millimeters of a number of
        musicxml "tenths" where a tenth is a tenth of the distance
        from one staff line to another.

        returns 0.0 if either of scalingMillimeters or scalingTenths
        is undefined.

        >>> sl = layout.ScoreLayout(scalingMillimeters=2.0, scalingTenths=10)
        >>> sl.tenthsToMillimeters(10)
        2.0

        Numbers are rounded to a maximum of 6 digits (but because they are floats,
        there may be inaccuracies.

        >>> sl.tenthsToMillimeters(17)
        3.4
        '''
        pass


# ------------------------------------------------------------------------------
class PageLayout(LayoutBase):
    '''
    Parameters for configuring a page's layout.

    PageLayout objects may be found on Measure or Part Streams.


    >>> pl = layout.PageLayout(pageNumber=4, leftMargin=234, rightMargin=124,
    ...                        pageHeight=4000, pageWidth=3000, isNew=True)
    >>> pl.pageNumber
    4
    >>> pl.rightMargin
    124
    >>> pl.leftMargin
    234
    >>> pl.isNew
    True

    This object represents both <print new-page> and <page-layout>
    elements in musicxml.
    '''
    # TODO -- make sure that the first pageLayout and systemLayout
    #     for each page are working together.

    def __init__(self,
                 *,
                 pageNumber: int|None = None,
                 leftMargin: int|float|None = None,
                 rightMargin: int|float|None = None,
                 topMargin: int|float|None = None,
                 bottomMargin: int|float|None = None,
                 pageHeight: int|float|None = None,
                 pageWidth: int|float|None = None,
                 isNew: bool|None = None,
                 **keywords):
        super().__init__(**keywords)

        self.pageNumber = pageNumber
        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        self.topMargin = topMargin
        self.bottomMargin = bottomMargin
        self.pageHeight = pageHeight
        self.pageWidth = pageWidth

        # store if this is the start of a new page
        self.isNew = isNew


# ------------------------------------------------------------------------------


class SystemLayout(LayoutBase):
    '''
    Object that configures or alters a system's layout.

    SystemLayout objects may be found on Measure or
    Part Streams.

    Importantly, if isNew is True then this object
    indicates that a new system should start here.


    >>> sl = layout.SystemLayout(leftMargin=234, rightMargin=124, distance=3, isNew=True)
    >>> sl.distance
    3
    >>> sl.rightMargin
    124
    >>> sl.leftMargin
    234
    >>> sl.isNew
    True
    '''
    def __init__(self,
                 *,
                 leftMargin: int|float|None = None,
                 rightMargin: int|float|None = None,
                 distance: int|float|None = None,
                 topDistance: int|float|None = None,
                 isNew: bool|None = None,
                 **keywords):
        super().__init__(**keywords)

        self.leftMargin = leftMargin
        self.rightMargin = rightMargin
        # no top or bottom margins

        # this is probably the distance between adjacent systems
        self.distance = distance
        self.topDistance = topDistance

        # store if this is the start of a new system
        self.isNew = isNew


class StaffLayout(LayoutBase):
    '''
    Object that configures or alters the distance between
    one staff and another in a system.

    StaffLayout objects may be found on Measure or
    Part Streams.

    The musicxml equivalent <staff-layout> lives in
    the <defaults> and in <print> attributes.


    >>> sl = layout.StaffLayout(distance=3, staffNumber=1, staffSize=113, staffLines=5)
    >>> sl.distance
    3

    The "number" attribute refers to which staff number
    in a part group this refers to.  Thus, it's not
    necessary in music21, but we store it if it's there.
    (defaults to None)

    >>> sl.staffNumber
    1

    staffLines specifies the number of lines for a non 5-line staff.

    >>> sl.staffLines
    5

    staffSize is a percentage of the base staff size, so
    this defines a staff 13% larger than normal.  Note that it is always converted to
    a floating point number.

    >>> sl.staffSize
    113.0
    >>> sl
    <music21.layout.StaffLayout distance 3, staffNumber 1, staffSize 113.0, staffLines 5>


    StaffLayout can also specify the staffType:

    >>> sl.staffType = stream.enums.StaffType.OSSIA

    There is one other attribute, '.hidden' which has three settings:

    * None - inherit from previous StaffLayout object, or False if no object exists
    * False - not hidden -- show as a default staff
    * True - hidden -- for playback only staves, or for a hidden/optimized-out staff

    Note: (TODO: .hidden None is not working; always gives False)
    '''
    _DOC_ATTR: dict[str, str] = {
        'staffType': '''
            What kind of staff is this as a stream.enums.StaffType.

            >>> sl = layout.StaffLayout()
            >>> sl.staffType
            <StaffType.REGULAR: 'regular'>
            >>> sl.staffType = stream.enums.StaffType.CUE
            >>> sl.staffType
            <StaffType.CUE: 'cue'>
            ''',
    }
    def __init__(self,
                 *,
                 distance: int|float|None = None,
                 staffNumber: int|float|None = None,
                 staffSize: int|float|None = None,
                 staffLines: int|None = None,
                 hidden: bool|None = None,
                 staffType: StaffType = StaffType.REGULAR,
                 **keywords):
        super().__init__(**keywords)

        # this is the distance between adjacent staves
        self.distance = distance
        self.staffNumber = staffNumber
        self.staffSize: float|None = None if staffSize is None else float(staffSize)
        self.staffLines = staffLines
        self.hidden = hidden  # True = hidden; False = shown; None = inherit
        self.staffType: StaffType = staffType

    def _reprInternal(self):
        pass

# ------------------------------------------------------------------------------


class LayoutException(exceptions21.Music21Exception):
    pass


class StaffGroupException(spanner.SpannerException):
    pass


# ------------------------------------------------------------------------------
class StaffGroup(spanner.Spanner):
    '''
    A StaffGroup defines a collection of one or more
    :class:`~music21.stream.Part` objects,
    specifying that they should be shown together with a bracket,
    brace, or other symbol, and may have a common name.

    >>> p1 = stream.Part()
    >>> p2 = stream.Part()
    >>> p1.append(note.Note('C5', type='whole'))
    >>> p1.append(note.Note('D5', type='whole'))
    >>> p2.append(note.Note('C3', type='whole'))
    >>> p2.append(note.Note('D3', type='whole'))
    >>> p3 = stream.Part()
    >>> p3.append(note.Note('F#4', type='whole'))
    >>> p3.append(note.Note('G#4', type='whole'))
    >>> s = stream.Score()
    >>> s.insert(0, p1)
    >>> s.insert(0, p2)
    >>> s.insert(0, p3)
    >>> staffGroup1 = layout.StaffGroup([p1, p2],
    ...      name='Marimba', abbreviation='Mba.', symbol='brace')
    >>> staffGroup1.barTogether = 'Mensurstrich'
    >>> s.insert(0, staffGroup1)
    >>> staffGroup2 = layout.StaffGroup([p3],
    ...      name='Xylophone', abbreviation='Xyl.', symbol='bracket')
    >>> s.insert(0, staffGroup2)
    >>> #_DOCS_SHOW s.show()

    .. image:: images/layout_StaffGroup_01.*
        :width: 400
    '''
    def __init__(self,
                 *spannedElements,
                 name: str|None = None,
                 barTogether: t.Literal[True, False, None, 'Mensurstrich'] = True,
                 abbreviation: str|None = None,
                 symbol: t.Literal['bracket', 'line', 'brace', 'square']|None = None,
                 **keywords):
        super().__init__(*spannedElements, **keywords)

        self.name = name or abbreviation  # if this group has a name
        self.abbreviation = abbreviation
        self._symbol: t.Literal['bracket', 'line', 'brace', 'square']|None = None
        self.symbol = symbol
        # determines if barlines are grouped through; this is group barline
        # in musicxml
        self._barTogether = barTogether

    # --------------------------------------------------------------------------

    def _getBarTogether(self) -> t.Literal[True, False, None, 'Mensurstrich']:
        pass

    def _setBarTogether(self, value: t.Literal[True, False, None, 'Mensurstrich', 'yes', 'no']):
        pass

    barTogether = property(_getBarTogether, _setBarTogether, doc='''
        Get or set the barTogether value, with either Boolean values
        or yes or no strings.  Or the string 'Mensurstrich' which
        indicates barring between staves but not in staves.

        Currently Mensurstrich is not supported by most exporters.

        >>> sg = layout.StaffGroup()
        >>> sg.barTogether = 'yes'
        >>> sg.barTogether
        True
        >>> sg.barTogether = 'Mensurstrich'
        >>> sg.barTogether
        'Mensurstrich'
        ''')

    def _getSymbol(self) -> t.Literal['bracket', 'line', 'brace', 'square']|None:
        pass

    def _setSymbol(self, value: t.Literal['bracket', 'line', 'brace', 'square']|None):
        pass

    symbol = property(_getSymbol, _setSymbol, doc='''
        Get or set the symbol value, with either Boolean values or yes or no strings.

        >>> sg = layout.StaffGroup()
        >>> sg.symbol = 'Brace'
        >>> sg.symbol
        'brace'
        ''')


# ---------------------------------------------------------------
# Stream subclasses for layout

def divideByPages(
    scoreIn: stream.Score,
    printUpdates: bool = False,
    fastMeasures: bool = False
) -> LayoutScore:
    '''
    Divides a score into a series of smaller scores according to page
    breaks.  Only searches for PageLayout.isNew or SystemLayout.isNew
    on the first part.  Returns a new `LayoutScore` object.

    If fastMeasures is True, then the newly created System objects
    do not have Clef signs, Key Signatures, or necessarily all the
    applicable spanners in them.  On the other hand, the position
    (on the page) information will be just as correct with
    fastMeasures = True and it will run much faster on large scores
    (because our spanner gathering algorithm is currently O(n^2);
    something TODO: to fix.)


    >>> lt = corpus.parse('demos/layoutTest.xml')
    >>> len(lt.parts)
    3
    >>> len(lt.parts[0].getElementsByClass(stream.Measure))
    80


    Divide the score up into layout.Page objects

    >>> layoutScore = layout.divideByPages(lt, fastMeasures=True)
    >>> len(layoutScore.pages)
    4
    >>> lastPage = layoutScore.pages[-1]
    >>> lastPage.measureStart
    64
    >>> lastPage.measureEnd
    80

    the layoutScore is a subclass of stream.Opus:

    >>> layoutScore
    <music21.layout.LayoutScore ...>
    >>> 'Opus' in layoutScore.classes
    True

    Pages are subclasses of Opus also, since they contain Scores

    >>> lastPage
    <music21.layout.Page ...>
    >>> 'Opus' in lastPage.classes
    True


    Each page now has Systems not parts.

    >>> firstPage = layoutScore.pages[0]
    >>> len(firstPage.systems)
    4
    >>> firstSystem = firstPage.systems[0]
    >>> firstSystem.measureStart
    1
    >>> firstSystem.measureEnd
    5

    Systems are a subclass of Score:

    >>> firstSystem
    <music21.layout.System ...>
    >>> isinstance(firstSystem, stream.Score)
    True

    Each System has staves (layout.Staff objects) not parts, though Staff is a subclass of Part

    >>> secondStaff = firstSystem.staves[1]
    >>> print(len(secondStaff.getElementsByClass(stream.Measure)))
    5
    >>> secondStaff
    <music21.layout.Staff ...>
    >>> isinstance(secondStaff, stream.Part)
    True
    '''
    pass


def getPageRegionMeasureNumbers(scoreIn):
    pass


def getSystemRegionMeasureNumbers(scoreIn):
    pass


def getRegionMeasureNumbers(scoreIn, region='Page'):
    '''
    get a list where each entry is a 2-tuplet whose first number
    refers to the first measure on a page and whose second number
    is the last measure on the page.
    '''
    pass


class LayoutScore(stream.Opus):
    '''
    Designation that this Score is
    divided into Pages, Systems, Staves (=Parts),
    Measures, etc.

    Used for computing location of notes, etc.

    If the score does not change between calls to the various getPosition calls,
    it is much faster as it uses a cache.
    '''

    def __init__(self, givenElements=None, **keywords):
        super().__init__(givenElements, **keywords)
        self.scoreLayout = None
        self.measureStart = None
        self.measureEnd = None

    @property
    def pages(self):
        pass

    def show(self, fmt=None, app=None, **keywords):
        '''
        Borrows stream.Score.show

        >>> lp = layout.Page()
        >>> ls = layout.LayoutScore()
        >>> ls.append(lp)
        >>> ls.show('text')
        {0.0} <music21.layout.Page p.1>
        <BLANKLINE>
        '''
        return stream.Score.show(self, fmt=fmt, app=app, **keywords)

    def getPageAndSystemNumberFromMeasureNumber(self, measureNumber):
        '''
        Given a layoutScore from divideByPages and a measureNumber returns a tuple
        of (pageId, systemId).  Note that pageId is probably one less than the page number,
        assuming that the first page number is 1, the pageId for the first page will be 0.

        Similarly, the first systemId on each page will be 0


        >>> lt = corpus.parse('demos/layoutTest.xml')
        >>> l = layout.divideByPages(lt, fastMeasures=True)
        >>> l.getPageAndSystemNumberFromMeasureNumber(80)
        (3, 3)
        '''
        pass

    def getMarginsAndSizeForPageId(self, pageId):
        '''
        return a namedtuple of (top, left, bottom, right, width, height)
        margins for a given pageId in tenths

        Default of (100, 100, 100, 100, 850, 1100) if undefined


        >>> #_DOCS_SHOW g = corpus.parse('luca/gloria')
        >>> #_DOCS_SHOW m22 = g.parts[0].getElementsByClass(stream.Measure)[22]
        >>> #_DOCS_SHOW m22.getElementsByClass(layout.PageLayout).first().leftMargin = 204.0
        >>> #_DOCS_SHOW gl = layout.divideByPages(g)
        >>> #_DOCS_SHOW gl.getMarginsAndSizeForPageId(1)
        >>> layout.PageSize(171.0, 204.0, 171.0, 171.0, 1457.0, 1886.0) #_DOCS_HIDE
        PageSize(top=171.0, left=204.0, right=171.0, bottom=171.0, width=1457.0, height=1886.0)
        '''
        pass

    def getPositionForSystem(self, pageId: int, systemId: int) -> SystemSize:
        '''
        first systems on a page use a different positioning.

        returns a Named tuple of the (top, left, right, and bottom) where each unit is
        relative to the page margins

        N.B. right is NOT the width -- it is different.  It is the offset to the right margin.
        weird, inconsistent, but most useful.  Bottom, however, is the hard part to compute.

        >>> lt = corpus.parse('demos/layoutTestMore.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures = True)
        >>> ls.getPositionForSystem(0, 0)
        SystemSize(top=211.0, left=70.0, right=0.0, bottom=696.0)
        >>> ls.getPositionForSystem(0, 1)
        SystemSize(top=810.0, left=0.0, right=0.0, bottom=1173.0)
        >>> ls.getPositionForSystem(0, 2)
        SystemSize(top=1340.0, left=67.0, right=92.0, bottom=1610.0)
        >>> ls.getPositionForSystem(0, 3)
        SystemSize(top=1724.0, left=0.0, right=0.0, bottom=2030.0)
        >>> ls.getPositionForSystem(0, 4)
        SystemSize(top=2144.0, left=0.0, right=0.0, bottom=2583.0)
        '''
        pass

    def getPositionForStaff(self, pageId, systemId, staffId):
        '''
        return a tuple of (top, bottom) for a staff, specified by a given pageId,
        systemId, and staffId in tenths of a staff-space.

        This distance is specified with respect to the top of the system.

        Staff scaling (<staff-details> in musicxml inside an <attributes> object) is
        taken into account, but not non-five-line staves.  Thus, a normally sized staff
        is always of height 40 (4 spaces of 10-tenths each)

        >>> lt = corpus.parse('demos/layoutTest.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures=True)

        The first staff (staff 0) of each page/system always begins at height 0 and should end at
        height 40 if it is a 5-line staff (not taken into account) with no staffSize changes

        >>> ls.getPositionForStaff(0, 0, 0)
        (0.0, 40.0)
        >>> ls.getPositionForStaff(1, 0, 0)
        (0.0, 40.0)

        The second staff (staff 1) begins at the end of staff 0 (40.0) +
        the appropriate staffDistance
        and adds the height of the staff.  Staff 1 here has a size of 80 which means
        80% of the normal staff size.  40 * 0.8 = 32.0:

        >>> ls.getPositionForStaff(0, 0, 1)
        (133.0, 165.0)

        The third staff (staff 2) begins after the second staff (staff 1) but is a normal
        size staff

        >>> ls.getPositionForStaff(0, 0, 2)
        (266.0, 306.0)

        The first staff (staff 0) of the second system (system 1) also begins at 0
        and as a normally-sized staff, has height of 40:

        >>> ls.getPositionForStaff(0, 1, 0)
        (0.0, 40.0)

        The spacing between the staves has changed in the second system, but the
        staff height has not:

        >>> ls.getPositionForStaff(0, 1, 1)
        (183.0, 215.0)
        >>> ls.getPositionForStaff(0, 1, 2)
        (356.0, 396.0)

        In the third system (system 2), the staff distance reverts to the distance
        of system 0, but the staffSize is now 120 or 48 tenths (40 * 1.2 = 48)

        >>> ls.getPositionForStaff(0, 2, 1)
        (117.0, 165.0)

        Page 1 (0), System 4 (3), Staff 2 (1) is a hidden ("optimized") system.
        Thus, its staffLayout notes this:

        >>> staffLayout031 = ls.pages[0].systems[3].staves[1].staffLayout
        >>> staffLayout031
        <music21.layout.StaffLayout distance None, staffNumber None, staffSize 80, staffLines None>
        >>> staffLayout031.hidden
        True

        Thus, the position for this staff will have the same top and bottom, and the
        position for the next staff will have the same top as the previous staff:

        >>> ls.getPositionForStaff(0, 3, 0)
        (0.0, 40.0)
        >>> ls.getPositionForStaff(0, 3, 1)
        (40.0, 40.0)
        >>> ls.getPositionForStaff(0, 3, 2)
        (133.0, 173.0)


        Tests for a score with PartStaff objects:
        >>> lt = corpus.parse('demos/layoutTestMore.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures = True)
        >>> ls.getPositionForStaff(0, 0, 0)
        (0.0, 40.0)
        >>> ls.getPositionForStaff(0, 0, 1)
        (133.0, 173.0)
        >>> ls.getPositionForStaff(0, 0, 2)
        (235.0, 275.0)

        >>> ls.getPositionForStaff(0, 2, 0)
        (0.0, 40.0)
        >>> ls.getPositionForStaff(0, 2, 1)
        (40.0, 40.0)
        >>> ls.getPositionForStaff(0, 2, 2)
        (40.0, 40.0)

        System 4 has the top staff hidden, which has been causing problems:

        >>> ls.getPositionForStaff(0, 4, 0)
        (0.0, 0.0)
        >>> ls.getPositionForStaff(0, 4, 1)
        (0.0, 40.0)
        '''
        pass

    def getStaffDistanceFromPrevious(self, pageId, systemId, staffId):
        '''
        return the distance of this staff from the previous staff in the same system

        for staffId = 0, this is always 0.0

        TODO:tests, now that this is out from previous
        '''
        pass

    def getStaffSizeFromLayout(self, pageId: int, systemId: int, staffId: int) -> float:
        '''
        Get the currently active staff-size for a given pageId, systemId, and staffId.

        Note that this does not take into account the hidden state of the staff, which,
        if True, makes the effective size 0.0 -- see getStaffHiddenAttribute

        >>> lt = corpus.parse('demos/layoutTest.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures=True)
        >>> ls.getStaffSizeFromLayout(0, 0, 0)
        40.0
        >>> ls.getStaffSizeFromLayout(0, 0, 1)
        32.0
        >>> ls.getStaffSizeFromLayout(0, 0, 2)
        40.0
        >>> ls.getStaffSizeFromLayout(0, 1, 1)
        32.0
        >>> ls.getStaffSizeFromLayout(0, 2, 1)
        48.0
        >>> ls.getStaffSizeFromLayout(0, 3, 1)
        32.0
        '''
        pass

    def getStaffHiddenAttribute(self, pageId: int, systemId: int, staffId: int) -> bool:
        '''
        returns the staffLayout.hidden attribute for a staffId, or if it is not
        defined, recursively search through previous staves until one is found.


        >>> lt = corpus.parse('demos/layoutTestMore.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures = True)
        >>> ls.getStaffHiddenAttribute(0, 0, 0)
        False
        >>> ls.getStaffHiddenAttribute(0, 0, 1)
        False
        >>> ls.getStaffHiddenAttribute(0, 1, 1)
        True
        >>> ls.getStaffHiddenAttribute(0, 2, 1)
        True
        >>> ls.getStaffHiddenAttribute(0, 3, 1)
        False
        '''
        pass

    def getSystemBeforeThis(
        self,
        pageId: int,
        systemId: int
    ) -> tuple[int|None, int]:
        # noinspection PyShadowingNames
        '''
        given a pageId and systemId, get the (pageId, systemId) for the previous system.

        return (None, None) if it's the first system on the first page

        This test score has five systems on the first page,
        three on the second, and two on the third

        >>> lt = corpus.parse('demos/layoutTestMore.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures = True)
        >>> systemId = 1
        >>> pageId = 2  # last system, last page
        >>> while pageId is not None:
        ...    pageId, systemId = ls.getSystemBeforeThis(pageId, systemId)
        ...    (pageId, systemId)
        (2, 0) (1, 2) (1, 1) (1, 0) (0, 4) (0, 3) (0, 2) (0, 1) (0, 0) (None, -1)
        '''
        pass

    def getPositionForStaffMeasure(self, staffId, measureNumber, returnFormat='tenths'):
        '''
        Given a layoutScore from divideByPages, a staffId, and a measureNumber,
        returns a tuple of ((top, left), (bottom, right), pageId)
        allowing an exact position for the measure on the page.
        If returnFormat is "tenths", then it will be returned in tenths.

        If returnFormat is "float", returns each as a number from 0 to 1 where 0 is the
        top or left of the page, and 1 is the bottom or right of the page.


        >>> lt = corpus.parse('demos/layoutTest.xml')
        >>> ls = layout.divideByPages(lt, fastMeasures = True)

        The first measure of staff one begins at 336 tenths from the top (125 for the
        margin top and 211 for the top-staff-distance).  It begins 170.0 from the
        left (100 for the page-margin-left, 70 for staff-margin-left).  It ends
        40.0 below that (staffHeight) and 247.0 to the right (measure width)

        >>> ls.getPositionForStaffMeasure(0, 1)
        ((336.0, 170.0), (376.0, 417.0), 0)

        The other staves for the same measure are below this one:

        >>> ls.getPositionForStaffMeasure(1, 1)
        ((469.0, 170.0), (501.0, 417.0), 0)
        >>> ls.getPositionForStaffMeasure(2, 1)
        ((602.0, 170.0), (642.0, 417.0), 0)


        If float is requested for returning, then the numbers are the fraction of
        the distance across the page.

        >>> ls.getPositionForStaffMeasure(0, 1, returnFormat='float')
        ((0.152..., 0.0996...), (0.170..., 0.244...), 0)


        Moving over the page boundary:

        >>> ls.getPositionForStaffMeasure(0, 23)
        ((1703.0, 1345.0), (1743.0, 1606.0), 0)
        >>> ls.getPositionForStaffMeasure(1, 23)  # hidden
        ((1743.0, 1345.0), (1743.0, 1606.0), 0)
        >>> ls.getPositionForStaffMeasure(0, 24)
        ((195.0, 100.0), (235.0, 431.0), 1)
        >>> ls.getPositionForStaffMeasure(1, 24)
        ((328.0, 100.0), (360.0, 431.0), 1)
        '''
        pass
        # return self.getPositionForStaffIdSystemIdPageIdMeasure(
        #    staffId, systemId, pageId, measureNumber, returnFormat)

    def measurePositionWithinSystem(self, measureNumber, pageId=None, systemId=None):
        '''
        Given a measure number, find the start and end X positions (with respect to
        the system margins) for the measure.

        if pageId and systemId are given, then it will speed up the search. But not necessary

        no staffId is needed since (at least for now) all measures begin and end at the same
        X position


        >>> l = corpus.parse('demos/layoutTest.xml')
        >>> ls = layout.divideByPages(l, fastMeasures = True)
        >>> ls.measurePositionWithinSystem(1, 0, 0)
        (0.0, 247.0)
        >>> ls.measurePositionWithinSystem(2, 0, 0)
        (247.0, 544.0)
        >>> ls.measurePositionWithinSystem(3, 0, 0)
        (544.0, 841.0)

        Measure positions reset at the start of a new system

        >>> ls.measurePositionWithinSystem(6)
        (0.0, 331.0)
        >>> ls.measurePositionWithinSystem(7)
        (331.0, 549.0)
        '''
        pass

    def getAllMeasurePositionsInDocument(self, returnFormat='tenths', printUpdates=False):
        '''
        returns a list of dictionaries, where each dictionary gives the measure number
        and other information, etc. in the document.


        # >>> g = corpus.parse('luca/gloria')
        # >>> gl = layout.divideByPages(g)
        # >>> gl.getAllMeasurePositionsInDocument()
        '''
        pass


class Page(stream.Opus):
    '''
    Designation that all the music in this Stream
    belongs on a single notated page.
    '''

    def __init__(self, givenElements=None, **keywords):
        super().__init__(givenElements, **keywords)
        self.pageNumber = 1
        self.measureStart = None
        self.measureEnd = None
        self.systemStart = None
        self.systemEnd = None
        self.pageLayout = None

    def _reprInternal(self):
        pass

    @property
    def systems(self):
        pass

    def show(self, fmt=None, app=None, **keywords):
        '''
        Borrows stream.Score.show

        >>> ls = layout.System()
        >>> lp = layout.Page()
        >>> lp.append(ls)
        >>> lp.show('text')
        {0.0} <music21.layout.System 0: p.0, sys.0>
        <BLANKLINE>
        '''
        return stream.Score.show(self, fmt=fmt, app=app, **keywords)



class System(stream.Score):
    '''
    Designation that all the music in this Stream
    belongs on a single notated system.

    Attribute systemNumbering says at what point the numbering of
    systems resets.  It can be either "Score" (default), "Opus", or "Page".
    '''
    def __init__(self, givenElements=None, **keywords):
        super().__init__(givenElements, **keywords)
        self.systemNumber = 0

        self.pageNumber = 0
        self.pageSystemNumber = 0

        self.systemLayout = None
        self.systemNumbering = 'Score'  # or Page; when do system numbers reset?
        self.measureStart = None
        self.measureEnd = None

    def _reprInternal(self):
        pass

    @property
    def staves(self):
        pass


class Staff(stream.Part):
    '''
    Designation that all the music in this Stream
    belongs on a single Staff.
    '''

    def __init__(self, givenElements=None, **keywords):
        super().__init__(givenElements, **keywords)
        self.staffNumber = 1  # number in this system NOT GLOBAL

        self.scoreStaffNumber = 0
        self.pageNumber = 0
        self.pageSystemNumber = 0

        self.optimized = 0
        self.height = None  # None = undefined
        self.inheritedHeight = None
        self.staffLayout = None

    def _reprInternal(self):
        pass


_DOC_ORDER = [ScoreLayout, PageLayout, SystemLayout, StaffLayout, LayoutBase,
              LayoutScore, Page, System, Staff]
# ------------------------------------------------------------------------------


class Test(unittest.TestCase):

    def testBasic(self):
        pass

    def x_testGetPageMeasureNumbers(self):
        pass

    def testGetStaffLayoutFromStaff(self):
        '''
        we have had problems with attributes disappearing.
        '''
        pass


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    import music21
    music21.mainTest(Test)  # , runTest='getStaffLayoutFromStaff')
