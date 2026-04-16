# -----------------------------------------------------------------------------
# Name:         corpora.py
# Purpose:      corpus classes
#
# Authors:      Joséphine Wolf Oberholtzer
#
# Copyright:    Copyright © 2009-2012, 2014 Michael Scott Asato Cuthbert
# License:      BSD, see license.txt
# -----------------------------------------------------------------------------
from __future__ import annotations

import abc
from collections.abc import Collection, Sequence, Iterable
import pathlib
import typing as t

from music21 import common
from music21.corpus import work
from music21 import environment
from music21.exceptions21 import CorpusException
from music21 import prebase

if t.TYPE_CHECKING:
    from music21.metadata import bundles

environLocal = environment.Environment(__file__)


# -----------------------------------------------------------------------------


class Corpus(prebase.ProtoM21Object):
    r'''
    Abstract base class of all corpora subclasses.
    '''

    # CLASS VARIABLES #

    __metaclass__ = abc.ABCMeta

    # TODO: this is volatile -- should be elsewhere
    _acceptableExtensions: list[str] = [
        'abc', 'capella', 'midi', 'musicxml', 'musedata',
        'humdrum', 'romantext', 'noteworthytext', 'noteworthy'
    ]

    # TODO: this should be wiped if a SubConverter is registered or deregistered.
    # mypy online (but not local) having a problem determining type of findInputExtension
    # https://github.com/python/mypy/issues/1032
    _allExtensions: tuple[str, ...] = tuple(  # type: ignore
        common.flattenList(
            [common.formats.findInputExtension(x)  # type: ignore
             for x in _acceptableExtensions]
        )
    )

    _pathsCache: dict[tuple[str, tuple[str, ...]], list[pathlib.Path]] = {}

    _directoryInformation: tuple[()]|Sequence[tuple[str, str, bool]] = ()

    parseUsingCorpus = True

    # SPECIAL METHODS #
    def _reprInternal(self):
        pass

    # PRIVATE METHODS #

    def _removeNameFromCache(self, name):
        pass

    def _findPaths(
        self,
        rootDirectoryPath: pathlib.Path,
        *,
        fileExtensions: Iterable[str],
    ) -> list[pathlib.Path]:
        '''
        Given a root filePath file path, recursively search all contained paths
        for files in `rootFilePath` matching any of the file extensions in
        `fileExtensions`.

        The `fileExtensions` is an Iterable of file extensions.

        NB: we've tried optimizing with `fnmatch` but it does not save any
        time.

        Generally cached.
        '''
        rdp = common.cleanpath(rootDirectoryPath, returnPathlib=True)
        matched = []

        for filename in sorted(rdp.rglob('*')):
            if filename.name.startswith('__'):
                continue
            if filename.name.startswith('.'):
                continue
            for extension in fileExtensions:
                if filename.suffix.endswith(extension):
                    matched.append(filename)
                    break

        # this is actually twice as slow
        # for extension in fileExtensions:
        #     for filename in rdp.rglob('*' + extension):
        #           ... etc ...
        return matched

    @staticmethod
    def translateExtensions(
        fileExtensions: Iterable[str] = (),
        *,
        expandExtensions: bool = True,
    ) -> tuple[str, ...]:
        # noinspection PyShadowingNames
        '''
        Utility to get default extensions, or, optionally, expand extensions to
        all known formats.

        >>> coreCorpus = corpus.corpora.CoreCorpus()
        >>> for extension in coreCorpus.translateExtensions():
        ...     extension
        ...
        '.abc'
        '.capx'
        '.mid'
        '.midi'
        '.xml'
        '.mxl'
        '.musicxml'
        '.md'
        '.musedata'
        '.zip'
        '.krn'
        '.rntxt'
        '.rntext'
        '.romantext'
        '.rtxt'
        '.nwctxt'
        '.nwc'

        >>> coreCorpus.translateExtensions(('.mid',), expandExtensions=False)
        ('.mid',)

        >>> coreCorpus.translateExtensions(('.mid',), expandExtensions=True)
        ('.mid', '.midi')

        It does not matter if you choose a canonical name or not, the output is the same:

        >>> coreCorpus.translateExtensions(('.musicxml',), expandExtensions=True)
        ('.xml', '.mxl', '.musicxml')

        >>> coreCorpus.translateExtensions(('.xml',), expandExtensions=True)
        ('.xml', '.mxl', '.musicxml')

        Leading dots don't matter:

        >>> coreCorpus.translateExtensions(('xml',))
        ('.xml', '.mxl', '.musicxml')


        # With multiple extensions:

        >>> coreCorpus.translateExtensions(('.mid', '.musicxml'), expandExtensions=False)
        ('.mid', '.musicxml')
        >>> coreCorpus.translateExtensions(('.mid', '.musicxml'))
        ('.mid', '.midi', '.xml', '.mxl', '.musicxml')

        * Changed in v9: returns a tuple, not a list.  first element must be an Iterable of strings

        TODO: unify with tools in common.formats
        '''
        if not fileExtensions:
            return Corpus._allExtensions
        elif expandExtensions:
            expandedExtensions: list[str] = []
            for extension in fileExtensions:
                allInputExtensions = common.formats.findInputExtension(extension)
                if allInputExtensions:
                    # inefficient, but very few loops.
                    expandedExtensions += allInputExtensions
            return tuple(expandedExtensions)
        else:
            return tuple(fileExtensions)

    # PRIVATE PROPERTIES #

    @property
    @abc.abstractmethod
    def cacheFilePath(self) -> pathlib.Path:
        raise NotImplementedError

    # PUBLIC METHODS #
    def rebuildMetadataCache(self, useMultiprocessing=True, verbose=True):
        r'''
        Rebuild a named bundle from scratch.

        If a bundle is associated with one of music21's corpora, delete any
        metadata cache on disk, clear the bundle's contents and reload in all
        files from that associated corpus.

        Return the rebuilt metadata bundle.
        '''
        pass

    def cacheMetadata(self, useMultiprocessing=True, verbose=True, timer=None):
        '''
        Cache the metadata for a single corpus.
        '''
        def update(message):
            if verbose is True:
                environLocal.warn(message)
            else:
                environLocal.printDebug(message)

        if timer is None:
            timer = common.Timer()
            timer.start()

        metadataBundle = self.metadataBundle
        paths = self.getPaths()

        update(f'{self.name} metadata cache: starting processing of paths: {len(paths)}')
        update(f'cache: filename: {metadataBundle.filePath}')

        failingFilePaths = metadataBundle.addFromPaths(
            paths,
            parseUsingCorpus=self.parseUsingCorpus,
            useMultiprocessing=useMultiprocessing,
            verbose=verbose
        )

        update(f'cache: writing time: {timer} md items: {len(metadataBundle)}\n')

        update(f'cache: filename: {metadataBundle.filePath}')

        del metadataBundle
        return failingFilePaths

    @abc.abstractmethod
    def getPaths(
        self,
        *,
        fileExtensions: Iterable[str] = (),
        expandExtensions: bool = True
    ) -> list[pathlib.Path]:
        r'''
        The paths of the files in a given corpus.
        '''
        raise NotImplementedError

    def getWorkList(
        self,
        workName: str|pathlib.Path,
        movementNumber: int|Collection[int]|None = None,
        *,
        fileExtensions: Iterable[str] = (),
    ):
        r'''
        Search the corpus and return a list of filenames of works, always in a
        list.

        If no matches are found, an empty list is returned.

        >>> coreCorpus = corpus.corpora.CoreCorpus()

        This returns 1 even though there is a '.mus' file, which cannot be read:

        >>> len(coreCorpus.getWorkList('cpebach/h186'))
        1
        >>> len(coreCorpus.getWorkList('cpebach/h186', None, fileExtensions=['.xml']))
        1

        >>> len(coreCorpus.getWorkList('schumann_clara/opus17', 3))
        1
        >>> len(coreCorpus.getWorkList('schumann_clara/opus17', 2))
        0

        Note that 'verdi' just gets the single Verdi piece and not the
        Monteverdi pieces:

        >>> len(coreCorpus.getWorkList('verdi'))
        1

        '''
        if str(workName).startswith('schumann/'):  # pragma: no cover
            # no default schumanns, but older examples showed this.
            workName = str(workName).replace('schumann/', 'schumann_robert/')

        paths = self.getPaths(fileExtensions=fileExtensions)
        results = []

        workPath = pathlib.PurePath(workName)
        workPosix = workPath.as_posix().lower()
        # find all matches for the work name
        # TODO: this should match by path component, not just
        # substring
        for path in paths:
            if workPosix in path.as_posix().lower():
                results.append(path)

        if results:
            # more than one matched, so use more stringent criterion:
            # must have a slash before the name
            previousResults = results
            results = []
            for path in previousResults:
                if '/' + workPosix in path.as_posix().lower():
                    results.append(path)
            if not results:
                results = previousResults

        movementResults = []
        if movementNumber is not None and results:
            # store one or more possible mappings of movement number
            movementStrList = []
            # see if this is a pair
            if common.holdsType(movementNumber, int):
                movementStrList.append(
                    ''.join(str(x) for x in movementNumber))
                movementStrList.append(
                    '-'.join(str(x) for x in movementNumber))
                movementStrList.append('movement'
                                       + '-'.join(str(x) for x in movementNumber))
                movementStrList.append('movement'
                                       + '-0'.join(str(x) for x in movementNumber))
            else:
                movementStrList += [
                    f'0{movementNumber}',
                    str(movementNumber),
                    f'movement{movementNumber}',
                ]
            for filePath in sorted(results):
                filename = filePath.name
                if filePath.suffix:
                    filenameWithoutExtension = filePath.stem
                else:
                    filenameWithoutExtension = None
                searchPartialMatch = True
                if filenameWithoutExtension is not None:
                    # look for direct matches first
                    for movementStr in movementStrList:
                        # if movementStr.lower() in filePath.lower():
                        if filenameWithoutExtension.lower() == movementStr.lower():
                            movementResults.append(filePath)
                            searchPartialMatch = False
                # if we have one direct match, all other matches must
                # be direct. this will match multiple files with different
                # file extensions
                if movementResults:
                    continue
                if searchPartialMatch:
                    for movementStr in movementStrList:
                        if filename.startswith(movementStr.lower()):
                            movementResults.append(filePath)
            if not movementResults:
                pass
        else:
            movementResults = results
        return sorted(set(movementResults))

    def search(
        self,
        query: str,
        field: str|None = None,
        *,
        fileExtensions: Iterable[str] = (),
        **keywords
    ):
        r'''
        Search this corpus for metadata entries, returning a metadataBundle

        >>> corpus.corpora.CoreCorpus().search('3/4')
        <music21.metadata.bundles.MetadataBundle {1875 entries}>

        >>> corpus.corpora.CoreCorpus().search(
        ...      'bach',
        ...      field='composer',
        ...      )
        <music21.metadata.bundles.MetadataBundle {363 entries}>

        >>> predicate = lambda noteCount: noteCount < 20
        >>> corpus.corpora.CoreCorpus().search(
        ...     predicate,
        ...     field='noteCount',
        ...     )
        <music21.metadata.bundles.MetadataBundle {134 entries}>

        '''
        return self.metadataBundle.search(
            query,
            field=field,
            fileExtensions=fileExtensions,
            **keywords
        )

    # PUBLIC PROPERTIES #

    @property
    def directoryInformation(self) -> tuple[work.DirectoryInformation, ...]:
        '''
        Returns a tuple of DirectoryInformation objects for
        each directory in self._directoryInformation.

        >>> core = corpus.corpora.CoreCorpus()
        >>> diBrief = core.directoryInformation[0:5]
        >>> diBrief
        (<music21.corpus.work.DirectoryInformation airdsAirs>,
         <music21.corpus.work.DirectoryInformation bach>,
         <music21.corpus.work.DirectoryInformation beach>,
         <music21.corpus.work.DirectoryInformation beethoven>,
         <music21.corpus.work.DirectoryInformation chopin>)
        >>> diBrief[2].directoryTitle
        'Amy Beach'
        '''
        pass

    @property
    @abc.abstractmethod
    def name(self):
        r'''
        The name of a given corpus.
        '''
        raise NotImplementedError

    @property
    def metadataBundle(self) -> bundles.MetadataBundle:
        r'''
        The metadata bundle for a corpus:

        >>> corpus.corpora.CoreCorpus().metadataBundle
        <music21.metadata.bundles.MetadataBundle 'core': {151... entries}>

        As a technical aside, the metadata bundle for a corpus is actually
        stored in corpus.manager, in order to cache most effectively over
        multiple calls. There might be good reasons to eventually move them
        to each Corpus object, so long as its cached across instances of the
        class.
        '''
        pass

    def all(self) -> bundles.MetadataBundle:
        '''
        This is a synonym for the metadataBundle property, but easier to understand
        what it does.

        >>> corpus.corpora.CoreCorpus().all()
        <music21.metadata.bundles.MetadataBundle 'core': {151... entries}>
        '''
        pass

    def getComposer(
        self,
        composerName,
        *,
        fileExtensions: Iterable[str] = (),
    ):
        '''
        Return all filenames in the corpus that match a composer's or a
        collection's name. A `fileExtensions`, if provided, defines which
        extensions are returned. A `fileExtensions` of `()`, (default) returns
        all extensions.

        Note that xml and mxl are treated equivalently.

        >>> coreCorpus = corpus.corpora.CoreCorpus()
        >>> a = coreCorpus.getComposer('bach')
        >>> len(a) > 100
        True

        >>> a = coreCorpus.getComposer('bach', fileExtensions=['krn'])
        >>> len(a) < 10
        True

        >>> a = coreCorpus.getComposer('bach', fileExtensions=('xml',))
        >>> len(a) > 10
        True
        '''
        pass

    def getWorkReferences(self):
        '''
        Return a data dictionary for all works in this corpus
        Returns a list of corpus.work.DirectoryInformation objects, one
        for each directory. A 'works' dictionary for each composer
        provides references to dictionaries for all associated works.

        This is used in the generation of corpus documentation

        >>> workRefs = corpus.corpora.CoreCorpus().getWorkReferences()
        >>> workRefs[1:3]
        [<music21.corpus.work.DirectoryInformation bach>,
         <music21.corpus.work.DirectoryInformation beach>]
                 '''
        pass

# -----------------------------------------------------------------------------


class CoreCorpus(Corpus):
    r'''
    A model of the *core* corpus.

    >>> coreCorpus = corpus.corpora.CoreCorpus()
    '''

    # CLASS VARIABLES #

    # noinspection SpellCheckingInspection
    _directoryInformation = (  # filepath, composer/collection name, isComposer
        ('airdsAirs', "Aird's Airs", False),
        ('bach', 'Johann Sebastian Bach', True),
        ('beach', 'Amy Beach', True),
        ('beethoven', 'Ludwig van Beethoven', True),
        ('chopin', 'Frederic Chopin', True),
        ('ciconia', 'Johannes Ciconia', True),
        ('corelli', 'Arcangelo Corelli', True),
        ('cpebach', 'C.P.E. Bach', True),
        ('demos', 'Demonstration Files', False),
        ('essenFolksong', 'Essen Folksong Collection', False),
        ('handel', 'George Frideric Handel', True),
        ('haydn', 'Joseph Haydn', True),
        ('joplin', 'Scott Joplin', True),
        ('johnson_j_r', 'J. Rosamund Johnson', True),
        ('josquin', 'Josquin des Prez', True),
        ('leadSheet', 'Leadsheet demos', False),
        ('liliuokalani', 'Queen Liliʻuokalani', True),
        ('luca', 'D. Luca', True),
        ('lusitano', 'Vicente Lusitano', True),
        ('miscFolk', 'Miscellaneous Folk', False),
        ('monteverdi', 'Claudio Monteverdi', True),
        ('mozart', 'Wolfgang Amadeus Mozart', True),
        ('nottingham-dataset', 'Nottingham Music Database (partial)', False),
        ('oneills1850', "Oneill's 1850 Collection", False),
        ('palestrina', 'Giovanni Palestrina', True),
        ('ryansMammoth', "Ryan's Mammoth Collection", False),
        ('schoenberg', 'Arnold Schoenberg', True),
        ('schubert', 'Franz Schubert', True),
        ('schumann_robert', 'Robert Schumann', True),
        ('schumann_clara', 'Clara Schumann', True),
        ('theoryExercises', 'Theory Exercises', False),
        ('trecento', 'Fourteenth-Century Italian Music', False),
        ('verdi', 'Giuseppe Verdi', True),
        ('weber', 'Carl Maria von Weber', True),
        ('webern', 'Anton Webern', True),
    )

    _noCorpus = False

    name = 'core'

    # PRIVATE PROPERTIES #

    @property
    def cacheFilePath(self) -> pathlib.Path:
        pass

    # PUBLIC METHODS #

    def getPaths(
        self,
        fileExtensions: Iterable[str] = (),
        *,
        expandExtensions=True,
    ) -> list[pathlib.Path]:
        '''
        Get all paths in the core corpus that match a known extension, or an
        extension provided by an argument.

        If `expandExtensions` is True, a format for an extension, and related
        extensions, will be replaced by all known input extensions.

        This is convenient when an input format might match for multiple
        extensions.

        >>> coreCorpus = corpus.corpora.CoreCorpus()
        >>> corpusFilePaths = coreCorpus.getPaths()
        >>> 3000 < len(corpusFilePaths) < 4000
        True

        >>> kernFilePaths = coreCorpus.getPaths(['krn'])
        >>> len(kernFilePaths) >= 500
        True

        >>> abcFilePaths = coreCorpus.getPaths(['abc'])
        >>> len(abcFilePaths) >= 100
        True
        '''
        fileExtensions_out = self.translateExtensions(
            fileExtensions=fileExtensions,
            expandExtensions=expandExtensions,
        )
        cacheKey = ('core', tuple(fileExtensions_out))
        # not cached, fetch and reset
        if cacheKey not in Corpus._pathsCache:
            basePath = common.getCorpusFilePath()
            Corpus._pathsCache[cacheKey] = self._findPaths(
                basePath,
                fileExtensions=fileExtensions_out,
            )
        return Corpus._pathsCache[cacheKey]

    # PUBLIC PROPERTIES #

    @property
    def manualCoreCorpusPath(self):
        r'''
        Set music21's core corpus to a directory, and save that information in
        the user settings.

        This is specifically for use with "no corpus" music21 packages, where
        the core corpus was not included with the rest of the package
        functionality, and had to be installed separately.

        Set it to a directory:

        >>> coreCorpus = corpus.corpora.CoreCorpus()
        >>> #_DOCS_SHOW coreCorpus.manualCoreCorpusPath = '~/Desktop'

        Unset it:

        >>> #_DOCS_SHOW coreCorpus.manualCoreCorpusPath = None
        >>> #_DOCS_SHOW coreCorpus.manualCoreCorpusPath is None
        >>> True  #_DOCS_HIDE
        True

        '''
        pass

    @manualCoreCorpusPath.setter
    def manualCoreCorpusPath(self, expr):  # pragma: no cover
        pass

    @property
    def noCorpus(self):
        '''
        Return True or False if this is a `corpus` or `noCorpus` distribution.

        >>> corpus.corpora.CoreCorpus().noCorpus
        False
        '''
        pass


# -----------------------------------------------------------------------------


class LocalCorpus(Corpus):
    r'''
    A model of a *local* corpus.

    >>> localCorpus = corpus.corpora.LocalCorpus()

    The default local corpus is unnamed (or called "local" or None), but an arbitrary number of
    independent, named local corpora can be defined and persisted:

    >>> namedLocalCorpus = corpus.corpora.LocalCorpus('funk')

    Illegal local corpus name ('core' or 'virtual')

    >>> corpus.corpora.LocalCorpus('core')
    Traceback (most recent call last):
    music21.exceptions21.CorpusException: The name 'core' is reserved.
    '''
    # CLASS VARIABLES #
    _temporaryLocalPaths: dict[str, set[pathlib.Path]] = {}
    parseUsingCorpus: bool = False

    # INITIALIZER #

    def __init__(self, name: str|None = None):
        if not isinstance(name, (str, type(None))):
            raise CorpusException('Name must be a string or None')

        if name is not None and not name:
            raise CorpusException('Name cannot be blank')

        if name == 'local':
            self._name = None
        elif name in ('core', 'virtual'):
            raise CorpusException(f'The name {name!r} is reserved.')
        else:
            self._name = name

    # SPECIAL METHODS #

    def _reprInternal(self):
        pass

    # PRIVATE METHODS #

    def _getSettings(self):
        pass

    # PRIVATE PROPERTIES #

    @property
    def cacheFilePath(self) -> pathlib.Path:
        '''
        Get the path to the file path that stores the .json file.

        returns a pathlib.Path
        '''
        pass

    @cacheFilePath.setter
    def cacheFilePath(self, value):
        '''
        Set the path to the file path that stores the .json file.
        '''
        pass

    # PUBLIC METHODS #

    def addPath(self, directoryPath):
        r'''
        Add a directory path to a local corpus:

        >>> localCorpus = corpus.corpora.LocalCorpus('a new corpus')
        >>> localCorpus.addPath('~/Desktop')

        Paths added in this way will not be persisted from session to session
        unless explicitly saved by a call to ``LocalCorpus.save()``.
        '''
        pass

    def delete(self):
        r'''
        Delete a non-default local corpus from the user settings.
        '''
        pass

    def getPaths(
        self,
        *,
        fileExtensions: Iterable[str] = (),
        expandExtensions=True,
    ) -> list[pathlib.Path]:
        '''
        Access files in additional directories supplied by the user and defined
        in environment settings in the 'localCorpusSettings' list.

        If additional paths are added on a per-session basis with the
        :func:`~music21.corpus.addPath` function, these paths are also returned
        with this method.
        '''
        fileExtensions_trans: tuple[str, ...] = self.translateExtensions(
            fileExtensions=fileExtensions,
            expandExtensions=expandExtensions,
        )
        cacheKey = (self.name, fileExtensions_trans)
        # not cached, fetch and reset
        # if cacheKey not in Corpus._pathsCache:
        # check paths before trying to search
        validPaths = []
        for directoryPath in self.directoryPaths:
            if not directoryPath.is_dir():
                environLocal.warn(
                    f'invalid path set as localCorpusSetting: {directoryPath}')
            else:
                validPaths.append(directoryPath)
        # append successive matches into one list
        matches = []
        for directoryPath in validPaths:
            matches.extend(self._findPaths(directoryPath, fileExtensions=fileExtensions_trans))
        Corpus._pathsCache[cacheKey] = matches

        return Corpus._pathsCache[cacheKey]

    def removePath(self, directoryPath: str|pathlib.Path) -> None:
        r'''
        Remove a directory path from a local corpus.

        If that path is included in the list of persisted paths for the given
        corpus, it will be removed permanently.

        >>> testCorpus = corpus.corpora.LocalCorpus(name='test')
        >>> testCorpus.addPath('~/Desktop')
        >>> len(testCorpus.directoryPaths)
        1
        >>> testCorpus.removePath('~/Desktop')
        >>> testCorpus.directoryPaths
        ()

        TODO: test for corpus persisted to disk without actually reindexing
        files on user's Desktop.
        '''
        pass

    def save(self):
        r'''
        Save the current list of directory paths in use by a given corpus in
        the user settings.  And reindex.
        '''
        userSettings = environment.UserSettings()
        lcs = environment.LocalCorpusSettings(self.directoryPaths)
        if self.name != 'local':
            lcs.name = self.name
        lcs.cacheFilePath = self.cacheFilePath

        if self.name == 'local':
            userSettings['localCorpusSettings'] = lcs
        else:
            userSettings['localCorporaSettings'][self.name] = lcs
        environment.Environment().write()
        self.cacheMetadata()

    # PUBLIC PROPERTIES #

    @property
    def directoryPaths(self):
        r'''
        The directory paths in use by a given local corpus.
        '''
        pass

    @property
    def existsInSettings(self):
        r'''
        True if this local corpus has a corresponding entry in music21's user
        settings, otherwise false.
        '''
        pass

    @property
    def name(self):
        r'''
        The name of a given local corpus.  Either 'local' for the unnamed corpus
        or a name for a named corpus

        >>> corpus.corpora.LocalCorpus().name
        'local'

        >>> corpus.corpora.LocalCorpus('funkCorpus').name
        'funkCorpus'

        '''
        pass


# -----------------------------------------------------------------------------


# class VirtualCorpus(Corpus):
#     r'''
#     A model of the *virtual* corpus. that stays online.
#
#     >>> virtualCorpus = corpus.corpora.VirtualCorpus()
#
#     '''
#
#     # CLASS VARIABLES #
#
#     _virtualWorks = []
#
#     name = 'virtual'
#
#     corpusName = None
#     for corpusName in dir(virtual):
#         className = getattr(virtual, corpusName)
#         if callable(className):
#             obj = className()
#             if isinstance(obj, virtual.VirtualWork):
#                 if obj.corpusPath is not None:
#                     _virtualWorks.append(obj)
#     del corpusName
#     del className
#     del obj
#     # PRIVATE PROPERTIES #
#
#     @property
#     def cacheFilePath(self):
#         filePath = common.getMetadataCacheFilePath() / 'virtual.p.gz'
#         return filePath
#
#     # PUBLIC METHODS #
#
#     def getPaths(
#         self,
#         fileExtensions=None,
#         expandExtensions=True,
#         ):
#         '''
#         Get all paths in the virtual corpus that match a known extension.
#
#         An extension of None will return all known extensions.
#
#         >>> len(corpus.corpora.VirtualCorpus().getPaths()) > 6
#         True
#
#         '''
#         fileExtensions = self.translateExtensions(
#             fileExtensions=fileExtensions,
#             expandExtensions=expandExtensions,
#             )
#         paths = []
#         for obj in self._virtualWorks:
#             if obj.corpusPath is not None:
#                 for fileExtension in fileExtensions:
#                     results = obj.getUrlByExt(fileExtension)
#                     for result in results:
#                         if result not in paths:
#                             paths.append(result)
#         return paths
#
#     def getWorkList(
#         self,
#         workName,
#         movementNumber=None,
#         fileExtensions=None,
#         ):
#         '''
#         Given a work name, search all virtual works and return a list of URLs
#         for any matches.
#
#         >>> virtualCorpus = corpus.corpora.VirtualCorpus()
#         >>> virtualCorpus.getWorkList('bach/bwv1007/prelude')
#         ['https://kern.ccarh.org/cgi-bin/ksdata?l=cc/bach/cello&file=bwv1007-01.krn&f=xml']
#
#         >>> virtualCorpus.getWorkList('junk')
#         []
#
#         '''
#         if not common.isListLike(fileExtensions):
#             fileExtensions = [fileExtensions]
#         for obj in VirtualCorpus._virtualWorks:
#             if obj.corpusPath is not None and workName.lower() in obj.corpusPath.lower():
#                 return obj.getUrlByExt(fileExtensions)
#         return []
#
#


__all__ = (
    'Corpus',
    'CoreCorpus',
    'LocalCorpus',
    # 'VirtualCorpus',
)

_DOC_ORDER = (
    Corpus,
    CoreCorpus,
    LocalCorpus,
    # VirtualCorpus,
)

if __name__ == '__main__':
    import music21
    music21.mainTest()
