# ------------------------------------------------------------------------------
# Name:         lily/objects.py
# Purpose:      python objects representing lilypond
#
# Authors:      Michael Scott Asato Cuthbert
#               Jeremy Teitelbaum (Lilypond 2.24 adaptations)
#
# Copyright:    Copyright © 2007-2025 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
music21 translates to Lilypond format and if Lilypond is installed on the
local computer, can automatically generate .pdf, .png, and .svg versions
of musical files using Lilypond.

The Grammar for Lilypond comes from
http://lilypond.org/doc/v2.14/Documentation/notation/lilypond-grammar
'''
from __future__ import annotations

import typing as t
import unittest

from music21 import common
from music21 import exceptions21
from music21 import prebase


class LilyObjectsException(exceptions21.Music21Exception):
    pass


class LyObject(prebase.ProtoM21Object):
    r'''
    LyObject is the base class of all other Lily Objects

    >>> lyo = lily.lilyObjects.LyObject()
    >>> lyo.stringOutput()
    ''

    '''
    supportedClasses: list[object] = []  # ordered list of classes to support
    m21toLy: dict[str, dict] = {}
    defaultAttributes: dict[str, t.Any] = {}
    backslash = '\\'

    def __init__(self):
        # self.context = context
        self.lilyAttributes = {}
        self._parent = None
        self.thisIndent = 0
        self.markupTop = None
        self.lyricMarkupOrIdentifier = None
        self.markupListOrIdentifier = None
        self.markupTopOrIdentifier = None
        # self.setLilyAttributes(inObject, context, **keywords)

    def __setattr__(self, name, value):
        if isinstance(value, LyObject):
            value.setParent(self)
        elif common.isIterable(value):
            for v in value:
                if isinstance(v, LyObject):
                    if v._parent is None:
                        v.setParent(self)

        object.__setattr__(self, name, value)

    def getParent(self):
        pass

    def setParent(self, parentObject):
        self._parent = common.wrapWeakref(parentObject)

    def ancestorList(self):
        r'''
        returns a list of all unwrapped parent objects for the current object
        '''
        pass

    def getAncestorByClass(self, classObj, getAncestorNumber=1):
        pass

    @property
    def newlineIndent(self):
        # totalIndents = self.thisIndent
        pass

    def setAttributes(self, m21Object):
        r'''
        Returns a dictionary and sets self.lilyAttributes to that dictionary, for a m21Object
        of class classLookup using the mapping of self.m21toLy[classLookup]

        >>> class Mock(base.Music21Object):
        ...     pass
        >>> m = Mock()
        >>> m.mockAttribute = 32
        >>> m.mockAttribute2 = None

        >>> lm = lily.lilyObjects.LyMock()

        LyMock (our test class) defines mappings for two classes:
        to LyMock.lilyAttributes:

        >>> print(lm.supportedClasses)
        [...'Mock', ...'Mocker']

        Thus, we can get attributes from the Mock class (see `setAttributesFromClassObject`):

        >>> lilyAttributes = lm.setAttributes(m)
        >>> for x in sorted(lilyAttributes.keys()):
        ...    print(f'{x}: {lilyAttributes[x]}')
        mock-attribute: 32
        mock-attribute-2: None

        >>> lilyAttributes is lm.lilyAttributes
        True
        '''
        pass

    def setAttributesFromClassObject(self, classLookup, m21Object):
        r'''
        Returns a dictionary and sets self.lilyAttributes to that dictionary, for a m21Object
        of class classLookup using the mapping of self.m21toLy[classLookup]


        >>> class Mock(base.Music21Object): pass
        >>> m = Mock()
        >>> lm = lily.lilyObjects.LyMock()

        LyMock (our test class) defines certain mappings from the m21 Mock class
        to LyMock.lilyAttributes:

        >>> for x in sorted(lm.m21toLy['Mock'].keys()):
        ...    print(f"{x}: {lm.m21toLy['Mock'][x]}")
        mockAttribute: mock-attribute
        mockAttribute2: mock-attribute-2


        Some of these attributes have defaults:

        >>> for x in sorted(lm.defaultAttributes.keys()):
        ...    print(f'{x}: {lm.defaultAttributes[x]}')
        mockAttribute2: 7


        >>> m.mockAttribute = 'hello'
        >>> lilyAttributes = lm.setAttributesFromClassObject('Mock', m)
        >>> for x in sorted(lilyAttributes.keys()):
        ...    print(f'{x}: {lilyAttributes[x]}')
        mock-attribute: hello
        mock-attribute-2: 7

        >>> lilyAttributes is lm.lilyAttributes
        True
        '''
        pass

    def _reprInternal(self) -> str:
        pass

    def __str__(self):
        so = self.stringOutput()
        so = so.replace('\n\n', '\n')
        return so

    def stringOutput(self):
        pass

    def getFirstNonNoneAttribute(self, attributeList):
        pass

    def newlineSeparateStringOutputIfNotNone(self, contents):
        pass

    def encloseCurly(self, arg):
        pass

    def quoteString(self, stringIn):
        r'''
        returns a string that is quoted with
        internal quotation marks backslash'd out
        and an extra space at the end.

        >>> m = lily.lilyObjects.LyObject()
        >>> print(m.quoteString(r'Hello "there"!'))
        "Hello \"there\"!"
        '''
        stringNew = stringIn.replace('"', r'\"')
        return '"' + stringNew + '" '

    def comment(self, stringIn: str) -> str:
        r'''
        returns a comment that is %{ stringIn.strip() %}

        (Don't put %} etc. in comments -- it will break the system.)
        '''
        return ' %{ ' + stringIn.strip() + ' %} '


class LyMock(LyObject):
    r'''
    A test object for trying various music21 to Lily conversions

    '''
    supportedClasses = ['Mock', 'Mocker']
    m21toLy = {'Mock': {'mockAttribute': 'mock-attribute',
                         'mockAttribute2': 'mock-attribute-2',
                        },
               'Mocker': {'mockerAttribute': 'mock-attribute',
                          'greg': 'mock-attribute-2', },
               }
    defaultAttributes = {'mockAttribute2': 7,
                         }

# ----------Grammar------------------#


class LyLilypondTop(LyObject):
    r'''
    corresponds to the highest level lilypond object in Appendix C:

    ::

      `lilypond: /* empty */
             | lilypond toplevel_expression
             | lilypond assignment
             | lilypond error
             | lilypond "\invalid"`


    error and \invalid are not defined by music21
    '''
    canContain = [None, 'TopLevelExpression', 'Assignment']

    def __init__(self, contents=None):
        if contents is None:
            contents = []
        super().__init__()
        self.contents = contents

    def stringOutput(self):
        pass


class LyTopLevelExpression(LyObject):
    r'''
    can contain one of:

      lilypondHeader
      bookBlock
      bookPartBlock
      scoreBlock
      compositeMusic
      fullMarkup
      fullMarkupList
      outputDef

    >>> bookBlock = lily.lilyObjects.LyBookBlock()
    >>> lyTopLevel = lily.lilyObjects.LyTopLevelExpression(bookBlock=bookBlock)
    >>> str(lyTopLevel)
    '\\book  { } '
    '''

    def __init__(self, lilypondHeader=None, bookBlock=None,
                 bookPartBlock=None, scoreBlock=None, compositeMusic=None,
                 fullMarkup=None, fullMarkupList=None, outputDef=None
                 ):
        super().__init__()
        self.lilypondHeader = lilypondHeader
        self.bookBlock = bookBlock
        self.bookPartBlock = bookPartBlock
        self.scoreBlock = scoreBlock
        self.compositeMusic = compositeMusic
        self.fullMarkup = fullMarkup
        self.fullMarkupList = fullMarkupList
        self.outputDef = outputDef

    def stringOutput(self):
        pass


class LyLilypondHeader(LyObject):
    r'''
    A header object with a LyHeaderBody

    >>> lyh = lily.lilyObjects.LyLilypondHeader()
    >>> str(lyh)
    '\\header { } '
    '''

    def __init__(self, lilypondHeaderBody=None):
        super().__init__()
        self.lilypondHeaderBody = lilypondHeaderBody

    def stringOutput(self):
        pass


class LyEmbeddedScm(LyObject):
    r'''
    represents Scheme embedded in Lilypond code.

    Can be either an SCM_TOKEN (Scheme Token) or SCM_IDENTIFIER String stored in self.content

    Note that if any LyEmbeddedScm is found in an output then the output SHOULD be marked as unsafe.
    But a lot of standard lilypond functions are actually embedded scheme.
    For instance, \clef, which
    as http://lilypond.org/doc/v2.12/input/lsr/lilypond-snippets/Pitches#Tweaking-clef-properties
    shows is a macro to run a lot of \set commands.

    >>> lyScheme = lily.lilyObjects.LyEmbeddedScm('##t')
    >>> str(lyScheme)
    '##t'
    '''

    def __init__(self, content=None):
        super().__init__()
        self.content = content

    def stringOutput(self):
        pass


class LyLilypondHeaderBody(LyObject):
    def __init__(self, assignments=None):
        if assignments is None:
            assignments = []
        super().__init__()
        self.assignments = assignments

    def stringOutput(self):
        pass


class LyAssignmentId(LyObject):
    '''
    >>> lyAssignmentId = lily.lilyObjects.LyAssignmentId('title', isLyricString=False)
    >>> str(lyAssignmentId)
    'title'
    '''

    def __init__(self, content=None, isLyricString=False):
        super().__init__()
        self.content = content
        self.isLyricString = isLyricString

    def stringOutput(self):
        pass


class LyAssignment(LyObject):
    r'''
    one of three forms of assignment:

      assignment_id '=' identifier_init
      assignment_id property_path '=' identifier_init
      embedded_scm

    if self.embeddedScm is not None, uses type 3
    if self.propertyPath is not None, uses type 2
    else uses type 1 or raises an exception.

    >>> lyIdInit = lily.lilyObjects.LyIdentifierInit(string='hi')
    >>> lya = lily.lilyObjects.LyAssignment(assignmentId='title', identifierInit=lyIdInit)
    >>> print(lya)
    title = "hi"

    Note that you could also pass assignmentId a LyAssignmentId object,
    but that's overkill for a lot of things.
    '''

    def __init__(self, assignmentId=None, identifierInit=None,
                 propertyPath=None, embeddedScm=None):
        super().__init__()
        self.assignmentId = assignmentId
        self.identifierInit = identifierInit
        self.propertyPath = propertyPath
        self.embeddedScm = embeddedScm

    def stringOutput(self):
        pass


class LyIdentifierInit(LyObject):
    r'''

    >>> lyIdInit = lily.lilyObjects.LyIdentifierInit(string='hello')
    >>> print(lyIdInit)
    "hello"
    '''

    def __init__(self,
                 scoreBlock=None,
                 bookBlock=None,
                 bookPartBlock=None,
                 outputDef=None,
                 contextDefSpecBlock=None,
                 music=None, postEvent=None, numberExpression=None,
                 string=None, embeddedScm=None, fullMarkup=None, fullMarkupList=None,
                 digit=None, contextModification=None):
        super().__init__()
        self.scoreBlock = scoreBlock
        self.bookBlock = bookBlock
        self.bookPartBlock = bookPartBlock
        self.outputDef = outputDef
        self.contextDefSpecBlock = contextDefSpecBlock
        self.music = music
        self.postEvent = postEvent
        self.numberExpression = numberExpression
        self.string = string
        self.embeddedScm = embeddedScm
        self.fullMarkup = fullMarkup
        self.fullMarkupList = fullMarkupList
        self.digit = digit
        self.contextModification = contextModification

    def stringOutput(self):
        pass


class LyContextDefSpecBlock(LyObject):
    def __init__(self, contextDefSpecBody=None):
        super().__init__()
        self.contextDefSpecBody = contextDefSpecBody

    def stringOutput(self):
        pass


class LyContextDefSpecBody(LyObject):
    r'''
    None or one of four forms:

       CONTEXT_DEF_IDENTIFIER
       context_def_spec_body "\grobdescriptions" embedded_scm
       context_def_spec_body context_mod
       context_def_spec_body context_modification

    >>> lyContextBody = lily.lilyObjects.LyContextDefSpecBody(contextDefIdentifier='cdi')
    >>> lyContextBody.stringOutput()
    'cdi'


    >>> embedScm = lily.lilyObjects.LyEmbeddedScm('#t')
    >>> lyContextBody = lily.lilyObjects.LyContextDefSpecBody(
    ...                 contextDefSpecBody='body', embeddedScm=embedScm)
    >>> lyContextBody.stringOutput()
    'body \\grobdescriptions #t'
    '''

    def __init__(self, contextDefIdentifier=None, contextDefSpecBody=None,
                          embeddedScm=None, contextMod=None, contextModification=None):
        super().__init__()
        self.contextDefIdentifier = contextDefIdentifier
        self.contextDefSpecBody = contextDefSpecBody
        self.embeddedScm = embeddedScm
        self.contextMod = contextMod
        self.contextModification = contextModification

    def stringOutput(self):
        pass


class LyBookBlock(LyObject):
    def __init__(self, bookBody=None):
        super().__init__()
        self.bookBody = bookBody

    def stringOutput(self):
        pass


class LyBookBody(LyObject):
    r'''
    Contains None, bookIdentifier (string?) or one or more of the following:

       paperBlock
       bookPartBlock
       scoreBlock
       compositeMusic
       fullMarkup
       fullMarkupList
       lilypondHeader
       error

    >>> lyBookBody = lily.lilyObjects.LyBookBody(bookIdentifier='bookId')
    >>> lyBookBody.stringOutput()
    'bookId'

    >>> lyBookBody = lily.lilyObjects.LyBookBody()
    >>> lyBookBody.stringOutput() is None
    True

    >>> lyBookBody = lily.lilyObjects.LyBookBody(contents=['a', 'b', 'c'])
    >>> print(lyBookBody.stringOutput())
    a
    b
    c
    '''

    def __init__(self, contents=None, bookIdentifier=None):
        if contents is None:
            contents = []
        super().__init__()
        self.contents = contents
        self.bookIdentifier = bookIdentifier

    def stringOutput(self):
        pass


class LyBookpartBlock(LyObject):
    r'''
    >>> lbb = lily.lilyObjects.LyBookpartBlock()
    >>> lbb.stringOutput()
    '\\bookpart  { \n\n } \n'
    '''

    def __init__(self, bookpartBody=None):
        super().__init__()
        self.bookpartBody = bookpartBody

    def stringOutput(self):
        pass


class LyBookpartBody(LyObject):
    r'''
    Contains None, bookIdentifier (string?) or one or more of the following:

       paperBlock
       scoreBlock
       compositeMusic
       fullMarkup
       fullMarkupList
       lilypondHeader
       error


    >>> lyBookpartBody = lily.lilyObjects.LyBookpartBody(bookIdentifier='bookId')
    >>> lyBookpartBody.stringOutput()
    'bookId'

    >>> lyBookpartBody = lily.lilyObjects.LyBookpartBody()
    >>> lyBookpartBody.stringOutput() is None
    True

    >>> lyBookpartBody = lily.lilyObjects.LyBookpartBody(contents=['a', 'b', 'c'])
    >>> print(lyBookpartBody.stringOutput())
    a
    b
    c
    '''

    def __init__(self, contents=None, bookIdentifier=None):
        if contents is None:
            contents = []
        super().__init__()
        self.contents = contents
        self.bookIdentifier = bookIdentifier

    def stringOutput(self):
        pass


class LyScoreBlock(LyObject):
    r'''
    represents the container for a score ( \score { ... } )

    with all the real stuff being in self.scoreBody

    >>> lyScoreBlock = lily.lilyObjects.LyScoreBlock(scoreBody='hello')
    >>> print(lyScoreBlock)
    \score { hello }
    '''

    def __init__(self, scoreBody=None):
        super().__init__()
        self.scoreBody = scoreBody

    def stringOutput(self):
        pass


class LyScoreBody(LyObject):
    r'''
    represents the contents of a \score { contents }
    block

    can take one of the following attributes:
    music, scoreIdentifier, scoreBody, lilypondHeader, outputDef, error

    >>> lsb = lily.lilyObjects.LyScoreBody(scoreIdentifier='score')
    >>> str(lsb)
    'score'
    '''

    def __init__(self, music=None, scoreIdentifier=None, scoreBody=None, lilypondHeader=None,
                 outputDef=None, error=None):
        super().__init__()
        self.music = music
        self.scoreIdentifier = scoreIdentifier
        self.scoreBody = scoreBody
        self.lilypondHeader = lilypondHeader
        self.outputDef = outputDef
        self.error = error

    def stringOutput(self):
        pass


class LyPaperBlock(LyObject):

    def __init__(self, outputDef=None):
        super().__init__()
        self.outputDef = outputDef

    def stringOutput(self):
        pass

class LyLayout(LyObject):
    def stringOutput(self):
        pass


class LyOutputDef(LyObject):
    r'''
    This is an ugly grammar, since it does not close the curly bracket.
    '''

    def __init__(self, outputDefBody=None):
        super().__init__()
        self.outputDefBody = outputDefBody

    def stringOutput(self):
        pass


class LyOutputDefHead(LyObject):
    r'''
    defType can be paper, midi, or layout.

    >>> lyODH = lily.lilyObjects.LyOutputDefHead()
    >>> lyODH.defType = 'midi'
    >>> print(lyODH.stringOutput())
    \midi

    According to Appendix C, is the same as LyOutputDefHeadWithModeSwitch
    '''

    def __init__(self, defType=None):
        super().__init__()
        self.defType = defType

    def stringOutput(self):
        pass


class LyOutputDefBody(LyObject):
    r'''

    output_def_body: output_def_head_with_mode_switch '{'
                    | output_def_head_with_mode_switch
                         '{'
                         OUTPUT_DEF_IDENTIFIER
                    | output_def_body assignment
                    | output_def_body context_def_spec_block
                    | output_def_body error
    '''

    def __init__(self, outputDefHead=None, outputDefIdentifier=None, outputDefBody=None,
                 assignment=None, contextDefSpecBlock=None, error=None):
        super().__init__()
        self.outputDefHead = outputDefHead
        self.outputDefIdentifier = outputDefIdentifier
        self.outputDefBody = outputDefBody
        self.assignment = assignment
        self.contextDefSpecBlock = contextDefSpecBlock
        self.error = error

    def stringOutput(self):
        pass


class LyTempoEvent(LyObject):
    r'''
    tempo_event: "\tempo" steno_duration '=' tempo_range
               | "\tempo" scalar steno_duration '=' tempo_range
               | "\tempo" scalar


    >>> lte = lily.lilyObjects.LyTempoEvent(scalar='40')
    >>> str(lte)
    '\\tempo 40'

    More complex:

    >>> steno = lily.lilyObjects.LyStenoDuration('quarter')
    >>> tempoRange = lily.lilyObjects.LyTempoRange(70, 100)
    >>> lte = lily.lilyObjects.LyTempoEvent(tempoRange=tempoRange, stenoDuration=steno)
    >>> str(lte)
    '\\tempo quarter  = 70~100 '

    >>> lte.scalar = 85
    >>> str(lte)
    '\\tempo 85 quarter  = 70~100 '
    '''

    def __init__(self, tempoRange=None, stenoDuration=None, scalar=None):
        super().__init__()
        self.tempoRange = tempoRange
        self.stenoDuration = stenoDuration
        self.scalar = scalar

    def stringOutput(self):
        pass


class LyMusicList(LyObject):
    r'''
    can take any number of LyMusic, LyEmbeddedScm, or LyError objects
    '''

    def __init__(self, contents=None):
        super().__init__()
        if contents is None:
            contents = []
        self.contents = contents

    def stringOutput(self):
        pass


class LyMusic(LyObject):

    def __init__(self, simpleMusic=None, compositeMusic=None):
        super().__init__()
        self.simpleMusic = simpleMusic
        self.compositeMusic = compositeMusic

    def stringOutput(self):
        pass


class LyAlternativeMusic(LyObject):

    def __init__(self, musicList=None):
        super().__init__()
        self.musicList = musicList

    def stringOutput(self):
        pass


class LyRepeatedMusic(LyObject):

    def __init__(self, simpleString=None, unsignedNumber=None, music=None, alternativeMusic=None):
        super().__init__()
        self.simpleString = simpleString
        self.unsignedNumber = unsignedNumber
        self.music = music
        self.alternativeMusic = alternativeMusic

    def stringOutput(self):
        pass


class LySequentialMusic(LyObject):
    r'''
    represents sequential music.

    Can be explicitly tagged with "\sequential" if displayTag is True
    '''

    def __init__(self, musicList=None, displayTag=False, beforeMatter=None):
        super().__init__()
        self.musicList = musicList
        self.displayTag = displayTag
        self.beforeMatter = beforeMatter

    def stringOutput(self):
        pass
        # + self.encloseCurly(musicListSO)


class LyOssiaMusic(LyObject):
    r'''
    represents ossia music.

    Can be tagged with \startStaff and \stopStaff if startstop is True
    '''

    def __init__(self, musicList=None, startstop=True):
        super().__init__()
        self.musicList = musicList
        self.startstop = startstop

    def stringOutput(self):
        pass


class LySimultaneousMusic(LyObject):
    r'''
    represents simultaneous music.

    Can be explicitly tagged with '\simultaneous' if displayTag is True
    otherwise encloses in double angle brackets
    '''

    def __init__(self, musicList=None, displayTag=False):
        super().__init__()
        self.musicList = musicList
        self.displayTag = displayTag

    def stringOutput(self):
        pass


class LySimpleMusic(LyObject):

    def __init__(self, eventChord=None, musicIdentifier=None,
                 musicPropertyDef=None, contextChange=None):
        super().__init__()
        self.eventChord = eventChord
        self.musicIdentifier = musicIdentifier
        self.musicPropertyDef = musicPropertyDef
        self.contextChange = contextChange

    def stringOutput(self):
        pass


class LyContextModification(LyObject):
    r'''
    represents both context_modification and optional_context_mod

    but not context_mod!!!!!
    '''

    def __init__(self, contextModList=None, contextModIdentifier=None, displayWith=True):
        super().__init__()
        self.contextModList = contextModList
        self.contextModIdentifier = contextModIdentifier  # String?
        self.displayWith = displayWith  # optional, but not supported without so far

    def stringOutput(self):
        pass


class LyContextModList(LyObject):
    r'''
    contains zero or more LyContextMod objects and an optional contextModIdentifier
    '''

    def __init__(self, contents=None, contextModIdentifier=None):
        if contents is None:
            contents = []
        super().__init__()
        self.contents = contents
        self.contextModIdentifier = contextModIdentifier  # STRING

    def stringOutput(self):
        pass


class LyCompositeMusic(LyObject):
    r'''
    one of LyPrefixCompositeMusic or LyGroupedMusicList stored in self.contents
    '''

    def __init__(self, prefixCompositeMusic=None, groupedMusicList=None, newLyrics=None):
        super().__init__()
        self.prefixCompositeMusic = prefixCompositeMusic
        self.groupedMusicList = groupedMusicList
        self.newLyrics = newLyrics

    @property
    def contents(self):
        pass

    def stringOutput(self):
        pass


class LyGroupedMusicList(LyObject):
    r'''
    one of LySimultaneousMusic or LySequentialMusic
    '''

    def __init__(self, simultaneousMusic=None, sequentialMusic=None):
        super().__init__()
        self.simultaneousMusic = simultaneousMusic
        self.sequentialMusic = sequentialMusic

    def stringOutput(self):
        pass


class LySchemeFunction(LyObject):
    r'''
    Unsupported for now, represents all of::

        function_scm_argument: embedded_scm
          116                      | simple_string

          117 function_arglist_music_last: EXPECT_MUSIC function_arglist music

          118 function_arglist_nonmusic_last: EXPECT_MARKUP
                                                function_arglist
                                                full_markup
          119                               | EXPECT_MARKUP
                                                function_arglist
                                                simple_string
          120                               | EXPECT_SCM
                                                function_arglist
                                                function_scm_argument

          121 function_arglist_nonmusic: EXPECT_NO_MORE_ARGS
          122                          | EXPECT_MARKUP
                                           function_arglist_nonmusic
                                           full_markup
          123                          | EXPECT_MARKUP
                                           function_arglist_nonmusic
                                           simple_string
          124                          | EXPECT_SCM
                                           function_arglist_nonmusic
                                           function_scm_argument

          125 function_arglist: EXPECT_NO_MORE_ARGS
          126                 | function_arglist_music_last
          127                 | function_arglist_nonmusic_last

          128 generic_prefix_music_scm: MUSIC_FUNCTION function_arglist

    We have usually been using LyEmbeddedScm for this
    '''

    def __init__(self, content=None):
        super().__init__()
        self.content = content

    def stringOutput(self):
        pass


class LyOptionalId(LyObject):
    r'''
    an optional id setting
    '''

    def __init__(self, content=None):
        super().__init__()
        self.content = content

    def stringOutput(self):
        pass


class LyPrefixCompositeMusic(LyObject):
    r'''
    type must be specified.  Should be one of:

    scheme, context, new, times, repeated, transpose,
    modeChanging, modeChangingWith, relative,
    rhythmed

    prefix_composite_music: generic_prefix_music_scm
                       | "\context"
                                simple_string
                                optional_id
                                optional_context_mod
                                music
                       | "\new"
                                simple_string
                                optional_id
                                optional_context_mod
                                music
                       | "\times" fraction music
                       | repeated_music
                       | "\transpose"
                                pitch_also_in_chords
                                pitch_also_in_chords
                                music
                       | mode_changing_head grouped_music_list
                       | mode_changing_head_with_context
                                optional_context_mod
                                grouped_music_list
                       | relative_music
                       | re_rhythmed_music
    '''
    # pylint: disable=redefined-builtin
    def __init__(self, type=None, genericPrefixMusicScm=None,
                 simpleString=None, optionalId=None, optionalContextMod=None,
                 music=None, fraction=None, repeatedMusic=None,
                 pitchAlsoInChords1=None, pitchAlsoInChords2=None,
                 modeChangingHead=None, groupedMusicList=None,
                 modeChangingHeadWithContext=None, relativeMusic=None,
                 reRhythmedMusic=None
                 ):
        super().__init__()
        self.type = type
        self.genericPrefixMusicScm = genericPrefixMusicScm
        self.simpleString = simpleString
        self.optionalId = optionalId
        self.optionalContextMod = optionalContextMod
        self.music = music
        self.fraction = fraction
        self.repeatedMusic = repeatedMusic
        self.pitchAlsoInChords1 = pitchAlsoInChords1
        self.pitchAlsoInChords2 = pitchAlsoInChords2
        self.modeChangingHead = modeChangingHead
        self.groupedMusicList = groupedMusicList
        self.modeChangingHeadWithContext = modeChangingHeadWithContext
        self.relativeMusic = relativeMusic
        self.reRhythmedMusic = reRhythmedMusic

    def stringOutput(self):
        pass


class LyModeChangingHead(LyObject):
    r'''
    represents both mode_changing_head and mode_changing_head_with_context

    .hasContext = False
    .mode = ['note', 'drum', 'figure', 'chord', 'lyric']

    >>> l = lily.lilyObjects.LyModeChangingHead(hasContext=True, mode='drum')
    >>> print(l.stringOutput())
    \drummode
    >>> l2 = lily.lilyObjects.LyModeChangingHead(hasContext=False, mode='chord')
    >>> print(l2.stringOutput())
    \chords

    '''
    allowableModes = ['note', 'drum', 'figure', 'chord', 'lyric']

    def __init__(self, hasContext=False, mode=None):
        super().__init__()
        self.hasContext = hasContext
        self.mode = mode

    def stringOutput(self):
        pass


class LyRelativeMusic(LyObject):
    r'''
    relative music
    '''

    def __init__(self, content=None):
        super().__init__()
        self.content = content

    def stringOutput(self):
        pass


class LyNewLyrics(LyObject):
    r'''
    contains a list of LyGroupedMusicList objects or identifiers
    '''

    def __init__(self, groupedMusicLists=None):
        if groupedMusicLists is None:
            groupedMusicLists = []
        super().__init__()
        self.groupedMusicLists = groupedMusicLists

    def stringOutput(self):
        pass


class LyReRhythmedMusic(LyObject):
    def __init__(self, groupedMusic=None, newLyrics=None):
        super().__init__()
        self.groupedMusic = groupedMusic
        self.newLyrics = newLyrics

    def stringOutput(self):
        pass


class LyContextChange(LyObject):
    r'''
    >>> lcc = lily.lilyObjects.LyContextChange('x', 'y')
    >>> str(lcc)
    '\\change x = y '
    '''

    def __init__(self, before=None, after=None):
        super().__init__()
        self.before = before
        self.after = after

    def stringOutput(self):
        pass


class LyPropertyPath(LyObject):
    r'''
    represents both property_path and property_path_revved

    has one or more of LyEmbeddedScm objects
    '''

    def __init__(self, embeddedScheme=None):
        if embeddedScheme is None:
            embeddedScheme = []

        super().__init__()
        self.embeddedScheme = embeddedScheme

    def stringOutput(self):
        pass


class LyPropertyOperation(LyObject):
    r'''
    Represents:

       property_operation: STRING '=' scalar
                       | "\unset" simple_string
                       | "\override" simple_string property_path '=' scalar
                       | "\revert" simple_string embedded_scm

    mandatory mode in ['set', 'unset', 'override', 'revert']


    also represents simple_music_property_def which has the same forms


    >>> lpo = lily.lilyObjects.LyPropertyOperation('unset', 'simple')
    >>> str(lpo)
    '\\unset simple '

    >>> lpo = lily.lilyObjects.LyPropertyOperation('override', 'simple', 'x', 'y')
    >>> str(lpo)
    '\\override simple.x = y '

    >>> lpo = lily.lilyObjects.LyPropertyOperation('revert', 'x', 'y')
    >>> str(lpo)
    '\\revert x.y '

    TODO: should \set be given?
    '''

    def __init__(self, mode=None, value1=None, value2=None, value3=None):
        super().__init__()
        self.mode = mode
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3

    def stringOutput(self):
        pass


class LyContextDefMod(LyObject):
    r'''
    one of consists, remove, accepts, defaultchild, denies, alias, type, description, name
    '''

    def __init__(self, contextDef=None):
        super().__init__()
        self.contextDef = contextDef

    def stringOutput(self):
        pass


class LyContextMod(LyObject):
    def __init__(self, contextDefOrProperty=None, scalar=None):
        super().__init__()
        self.contextDefOrProperty = contextDefOrProperty
        self.scalar = scalar

    def stringOutput(self):
        pass

# no need for context_prop_spec -- just strings
# see LyPropertyOperation for simple_music_property_def


class LyMusicPropertyDef(LyObject):

    def __init__(self, isOnce=False, propertyDef=None):
        super().__init__()
        self.isOnce = isOnce
        self.propertyDef = propertyDef

    def stringOutput(self):
        pass

# string, simple_string, scalar, etc. not needed


class LyEventChord(LyObject):
    r'''
    takes all the parts as a list of up to three elements::

        event_chord: simple_chord_elements post_events
               | CHORD_REPETITION optional_notemode_duration post_events
               | MULTI_MEASURE_REST optional_notemode_duration post_events
               | command_element
               | note_chord_element

    simple_chord_elements can be a LySimpleElement object.  Or it can be a
    LyNewChord or LyFigureSpec + Duration
    once that is done.  But there is no LySimpleChordElements object yet.
    '''

    def __init__(self, simpleChordElements=None, postEvents=None, chordRepetition=None,
                 multiMeasureRest=None, duration=None, commandElement=None, noteChordElement=None):
        super().__init__()
        self.simpleChordElements = simpleChordElements
        self.postEvents = postEvents
        self.chordRepetition = chordRepetition
        self.multiMeasureRest = multiMeasureRest
        self.duration = duration
        self.commandElement = commandElement
        self.noteChordElement = noteChordElement

    def stringOutput(self):
        pass


class LyNoteChordElement(LyObject):
    def __init__(self, chordBody=None, optionalNoteModeDuration=None, postEvents=None):
        if postEvents is None:
            postEvents = []
        super().__init__()
        self.chordBody = chordBody
        self.optionalNoteModeDuration = optionalNoteModeDuration
        self.postEvents = postEvents

    def stringOutput(self):
        pass


class LyChordBody(LyObject):

    def __init__(self, chordBodyElements=None):
        if chordBodyElements is None:
            chordBodyElements = []

        super().__init__()
        self.chordBodyElements = chordBodyElements

    def stringOutput(self):
        pass


class LyChordBodyElement(LyObject):
    r'''
    Contains a note or a drum pitch or a music function::

      chord_body_element: pitch
                            exclamations (a string of zero or more ! marks)
                            questions (a string of zero or more ? marks)
                            octave_check
                            post_events
                       | DRUM_PITCH post_events
                       | music_function_chord_body

    TODO: only the first form is currently supported in creation
    '''

    def __init__(self, parts=None):
        if parts is None:
            parts = []
        super().__init__()
        self.parts = parts

    def stringOutput(self):
        pass

# music_function_identifier_musicless_prefix: MUSIC_FUNCTION

# NOT Supported
#  217 music_function_chord_body: music_function_identifier_musicless_prefix
#                                   EXPECT_MUSIC
#                                   function_arglist_nonmusic
#                                   chord_body_element
#  218                          | music_function_identifier_musicless_prefix
#                                   function_arglist_nonmusic
#
#  219 music_function_event: music_function_identifier_musicless_prefix
#                              EXPECT_MUSIC
#                              function_arglist_nonmusic
#                              post_event
#  220                     | music_function_identifier_musicless_prefix
#                              function_arglist_nonmusic


class LyCommandElement(LyObject):
    def __init__(self, commandType=None, argument=None):
        super().__init__()
        self.commandType = commandType
        self.argument = argument

    def stringOutput(self):
        pass


class LyCommandEvent(LyObject):
    def __init__(self, commandType=None, argument1=None, argument2=None):
        super().__init__()
        self.commandType = commandType
        self.argument1 = argument1
        self.argument2 = argument2

    def stringOutput(self):
        pass


class LyPostEvents(LyObject):
    def __init__(self, eventList=None):
        if eventList is None:
            eventList = []
        super().__init__()
        self.eventList = eventList

    def stringOutput(self):
        pass


class LyPostEvent(LyObject):

    def __init__(self, arg1=None, arg2=None):
        super().__init__()
        self.arg1 = arg1
        self.arg2 = arg2

    def stringOutput(self):
        pass


class LyDirectionLessEvent(LyObject):
    r'''
    represents ['[', ']', '~', '(', ')', '\!', '\(', '\)', '\>', '\<']
    or an EVENT_IDENTIFIER or a tremolo_type
    '''

    def __init__(self, event=None):
        super().__init__()
        self.event = event

    def stringOutput(self):
        pass


# noinspection SpellCheckingInspection
class LyDirectionReqdEvent(LyObject):
    def __init__(self, event=None):
        super().__init__()
        self.event = event

    def stringOutput(self):
        pass


class LyOctaveCheck(LyObject):

    def __init__(self, equalOrQuotesOrNone=None):
        super().__init__()
        self.equalOrQuotesOrNone = equalOrQuotesOrNone

    def stringOutput(self):
        pass


class LyPitch(LyObject):
    r'''
    represents a pitch name and zero or more sup or sub quotes
    also used for steno_pitch and steno_tonic_pitch
    '''

    def __init__(self, noteNamePitch=None, quotes=None):
        super().__init__()
        self.noteNamePitch = noteNamePitch
        self.quotes = quotes

    def stringOutput(self):
        pass

# no need for pitch_also_in_chords


class LyGenTextDef(LyObject):
    r'''
    holds either full_markup, string, or DIGIT
    '''

    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def stringOutput(self):
        pass


class LyScriptAbbreviation(LyObject):
    r'''
    Holds a script abbreviation (for articulations etc.), one of::

        ^ + - | > . _

    '''

    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def stringOutput(self):
        pass


class LyScriptDir(LyObject):
    r'''
    Holds a script direction abbreviation (above below etc), one of::

        _ ^ -

    '''

    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def stringOutput(self):
        pass

# no need for absolute_pitch
# no need for optional_notemode_duration -- we can use LyMultipliedDuration or None


class LyStenoDuration(LyObject):
    r'''
    the main thing that we think of as non-tuplet duration.

    a duration number followed by one or more dots


    >>> lsd = lily.lilyObjects.LyStenoDuration('2', 2)
    >>> print(lsd)
    2..

    '''

    def __init__(self, durationNumber=None, numDots=0):
        super().__init__()
        self.durationNumber = durationNumber
        self.numDots = numDots

    def stringOutput(self):
        pass


class LyMultipliedDuration(LyObject):
    r'''
    represents either a simple LyStenoDuration or a list of things that
    the steno duration should be multiplied by.

    if stenoDur is None then output is None -- thus also represents
    optional_notemode_duration
    '''

    def __init__(self, stenoDur=None, multiply=None):
        if multiply is None:
            multiply = []
        super().__init__()
        self.stenoDur = stenoDur
        self.multiply = multiply

    def stringOutput(self):
        pass


class LyTremoloType(LyObject):

    def __init__(self, tremTypeOrNone=None):
        super().__init__()
        self.tremTypeOrNone = tremTypeOrNone

    def stringOutput(self):
        pass

# SKIPPING figured bass objects (lines 305 - 325) for now


class LyOptionalRest(LyObject):
    def __init__(self, rest=False):
        super().__init__()
        self.rest = rest

    def stringOutput(self):
        pass


class LySimpleElement(LyObject):
    r'''
    A single note, lyric element, drum pitch or hidden rest::

        simple_element: pitch
                        exclamations (a string of zero or more ! marks)
                        questions (a string of zero or more ? marks)
                        octave_check
                        optional_notemode_duration
                        optional_rest
                    | DRUM_PITCH optional_notemode_duration
                    | RESTNAME optional_notemode_duration
                    | lyric_element optional_notemode_duration
    '''

    def __init__(self, parts=None):
        if parts is None:
            parts = []
        super().__init__()
        self.parts = parts

    def stringOutput(self):
        pass

# SKIPPING ALL ChordSymbol Markup for now


class LyLyricElement(LyObject):
    r'''
    Object represents a single Lyric in lilypond.


    >>> lle = lily.lilyObjects.LyLyricElement('hel_')
    >>> lle
    <music21.lily.lilyObjects.LyLyricElement hel_>
    >>> print(lle)
    hel_
    '''

    def __init__(self, lyMarkupOrString=None):
        super().__init__()
        self.lyMarkupOrString = lyMarkupOrString

    def stringOutput(self):
        pass


class LyTempoRange(LyObject):
    r'''
    defines either a single tempo or a range
    '''

    def __init__(self, lowestOrOnlyTempo=None, highestTempoOrNone=None):
        super().__init__()
        self.lowestOrOnlyTempo = lowestOrOnlyTempo
        self.highestTempoOrNone = highestTempoOrNone

    def stringOutput(self):
        pass


class LyNumberExpression(LyObject):
    r'''
    any list of numbers or LyNumberTerms separated by '+' or '-' objects.
    '''

    def __init__(self, numberAndSepList=None):
        if numberAndSepList is None:
            numberAndSepList = []
        super().__init__()
        self.numberAndSepList = numberAndSepList

    def stringOutput(self):
        pass


class LyNumberTerm(LyObject):
    r'''
    any list of numbers separated by '*' or '/' strings.
    '''

    def __init__(self, numberAndSepList=None):
        if numberAndSepList is None:
            numberAndSepList = []
        super().__init__()
        self.numberAndSepList = numberAndSepList

    def stringOutput(self):
        pass


class LyLyricMarkup(LyObject):
    def __init__(self, lyricMarkupOrIdentifier=None, markupTop=None):
        super().__init__()
        self.lyricMarkupOrIdentifier = lyricMarkupOrIdentifier
        self.markupTop = markupTop

    def stringOutput(self):
        pass


class LyFullMarkupList(LyObject):
    def __init__(self, markupListOrIdentifier=None):
        super().__init__()
        self.markupListOrIdentifier = markupListOrIdentifier

    def stringOutput(self):
        pass


class LyFullMarkup(LyObject):
    def __init__(self, markupTopOrIdentifier=None):
        super().__init__()
        self.markupTopOrIdentifier = markupTopOrIdentifier

    def stringOutput(self):
        pass


class LyMarkupTop(LyObject):
    def __init__(self, argument1=None, argument2=None):
        super().__init__()
        self.argument1 = argument1
        self.argument2 = argument2

    def stringOutput(self):
        pass


class LyMarkupList(LyObject):
    def __init__(self, markupIdentifierOrList=None):
        super().__init__()
        self.markupIdentifierOrList = markupIdentifierOrList

    def stringOutput(self):
        pass


class LyMarkupComposedList(LyObject):
    def __init__(self, markupHeadList=None, markupBracedList=None):
        super().__init__()
        self.markupHeadList = markupHeadList
        self.markupBracedList = markupBracedList

    def stringOutput(self):
        pass


class LyMarkupBracedList(LyObject):
    def __init__(self, listBody=None):
        super().__init__()
        self.listBody = listBody

    def stringOutput(self):
        pass


class LyMarkupBracedListBody(LyObject):
    def __init__(self, markupOrMarkupList=None):
        if markupOrMarkupList is None:
            markupOrMarkupList = []

        super().__init__()
        self.markupOrMarkupList = markupOrMarkupList

    def stringOutput(self):
        pass

# skip markup_command_list and arguments for now
# skip markup_head_1_item
# skip markup_head_1_list

# simple_markup can be string or more complex


class LySimpleMarkup(LyObject):
    r'''
    simpleType can be 'string' (or markup identifier or lyric markup identifier, etc.) or
    'score-body' or 'markup-function'

    takes 1 required arg, 2nd for markup_function
    '''

    def __init__(self, simpleType='string', argument1=None, argument2=None):
        super().__init__()
        self.simpleType = simpleType
        self.argument1 = argument1
        self.argument2 = argument2

    def stringOutput(self):
        pass


class LyMarkup(LyObject):
    def __init__(self, simpleMarkup=None, optionalMarkupHeadList=None):
        super().__init__()
        self.simpleMarkup = simpleMarkup
        self.optionalMarkupHeadList = optionalMarkupHeadList

    def stringOutput(self):
        pass


# ------------older-------------
#
# class LyNote(LyObject):
#    pass
#
# class LyDuration(LyObject):
#    pass
#
# class LyLyricGroup(LyObject):
#    pass
#
# ## --------Layout----------##
#
# class LyPaper(LyObject):
#    m21toLy = {'PageLayout': {'pageWidth': 'paper-width',
#                               'pageHeight': 'paper-height',
#                               'topMargin': 'top-margin',
#                               'bottomMargin': 'bottom-margin',
#                               'leftMargin': 'left-margin',
#                               'rightMargin': 'right-margin',
#                               },
#                }
#
#    defaultAttributes = {'pageWidth': None,
#                 'pageHeight': None,
#                 'topMargin': None,
#                 'bottomMargin': None,
#                 'leftMargin': None,
#                 'rightMargin': None,
#                 }
#
#
# class LyLayout(LyObject):
#    pass
#
#
# ## -------Tools-----------##
# class LyCodePrinter:
#    pass
#
#    def __init__(self):
#        currentIndent = 0
#        bracketNesting = 0
#        angleBracketNest = 0

# # ------Tests------------##

class Test(unittest.TestCase):

    def testOneNoteTheHardWay(self):
        r'''
        make a dotted-half note c.
        '''
        pass


if __name__ == '__main__':
    import music21
    music21.mainTest(Test)

