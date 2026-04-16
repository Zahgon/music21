# ------------------------------------------------------------------------------
# Name:         omr/evaluators.py
# Purpose:      music21 module for evaluating correcting of output from OMR software
#
# Authors:      Maura Church
#               Michael Scott Asato Cuthbert
#
# Copyright:    Copyright © 2014 Maura Church, Michael Scott Asato Cuthbert,
# License:      BSD, see license.txt
# ------------------------------------------------------------------------------
'''
This module takes two XML files and displays the number of measures that
differ between the two before and after running the combined correction models
'''
from __future__ import annotations

from music21.omr import correctors
from music21 import converter

globalDebug = False


class OmrGroundTruthPair:
    '''
    Object for making comparisons between an OMR score and the GroundTruth

    Takes in a path to the OMR and a path to the groundTruth
    (or a pair of music21.stream.Score objects).

    See below for examples.

    '''

    def __init__(self, omr=None, ground=None):
        self._overriddenDebug = None
        self.numberOfDifferences = None
        if hasattr(omr, 'filePath'):
            self.omrPath = omr.filePath
            self.omrM21Score = omr
        else:
            self.omrPath = omr
            self.omrM21Score = None

        self.omrScore = self.getOmrScore()

        if hasattr(ground, 'filePath'):
            self.groundPath = ground.filePath
            self.groundM21Score = ground
        else:
            self.groundPath = ground
            self.groundM21Score = None

        self.groundScore = self.getGroundScore()

    @property
    def debug(self):
        '''
        Returns either the debug value set for this
        evaluator, or globalDebug
        '''
        pass

    @debug.setter
    def debug(self, newDebug):
        pass

    def parseAll(self):
        '''
        Parse both scores.
        '''
        pass

    def hashAll(self):
        '''
        store the Hashes for both scores.
        '''
        pass

    def getOmrScore(self):
        '''
        Returns a ScoreCorrector object of the OMR score. does not store it anywhere

         >>> omrPath = omr.correctors.K525omrShortPath
         >>> ground = omr.correctors.K525groundTruthShortPath
         >>> omrGTP = omr.evaluators.OmrGroundTruthPair(omr=omrPath, ground=ground)
         >>> ssOMR = omrGTP.getOmrScore()
         >>> ssOMR
         <music21.omr.correctors.ScoreCorrector object at 0x...>
        '''
        pass

    def getGroundScore(self):
        '''
        Returns a ScoreCorrector object of the Ground truth score

         >>> omrPath = omr.correctors.K525omrShortPath
         >>> ground = omr.correctors.K525groundTruthShortPath
         >>> omrGTP = omr.evaluators.OmrGroundTruthPair(omr=omrPath, ground=ground)
         >>> ssGT = omrGTP.getGroundScore()
         >>> ssGT
         <music21.omr.correctors.ScoreCorrector object at 0x...>
        '''
        pass

    # def getDifferencesBetweenAlignedScores(self):
    #     '''
    #     Returns the number of differences (int) between
    #     two scores with aligned indices
    #     '''
    #     self.numberOfDifferences = 0
    #     aList = self.omrScore.getAllHashes()
    #     bList = self.groundScore.getAllHashes()
    #     for i in range(len(aList)):
    #         for j in range(min(len(aList[i]), len(bList[i]))):
    #             a = aList[i][j]
    #             b = bList[i][j]
    #             s = difflib.SequenceMatcher(None, a, b)
    #             ratio = s.ratio()
    #             measureErrors = (1-ratio) * len(a)
    #             self.numberOfDifferences += measureErrors
    #     return self.numberOfDifferences

    def substCost(self, x, y):
        '''
        define the substitution cost for x and y (2 if x and y are unequal else 0)
        '''
        pass

    def insertCost(self, x):
        '''
        define the insertion cost for x and y (1)
        '''
        pass

    def deleteCost(self, x):
        '''
        define the deletion cost for x and y (1)
        '''
        pass

    def minEditDist(self, target, source):
        '''
        Computes the min edit distance from target to source. Figure 3.25
        '''
        pass

    def getDifferences(self):
        '''
        Returns the total edit distance as an Int between
        the two scores

        This function is based on James H. Martin's minimum edit distance.

        >>> omrPath = omr.correctors.K525omrShortPath
        >>> ground = omr.correctors.K525groundTruthShortPath
        >>> omrGTP = omr.evaluators.OmrGroundTruthPair(omr=omrPath, ground=ground)
        >>> differences = omrGTP.getDifferences()
        >>> differences
        32
        '''
        pass


def evaluateCorrectingModel(omrPath, groundTruthPath, debug=None,
                            originalDifferences=None, runOnePart=False):
    # noinspection PyShadowingNames
    '''
    Get a dictionary showing the efficacy of the omr.correctors.ScoreCorrector on an OMR Score
    by comparing it to the GroundTruth.

    Set debug to True to see a lot of intermediary steps.

    >>> omrFilePath = omr.correctors.K525omrShortPath
    >>> groundTruthFilePath = omr.correctors.K525groundTruthShortPath
    >>> returnDict = omr.evaluators.evaluateCorrectingModel(omrFilePath, groundTruthFilePath)
    >>> for name in sorted(list(returnDict.keys())):
    ...     (name, returnDict[name])
    ('newEditDistance', 20)
    ('numberOfFlaggedMeasures', 13)
    ('originalEditDistance', 32)
    ('totalNumberOfMeasures', 84)
    '''
    pass


def autoCorrelationBestMeasure(inputScore):
    '''
    Essentially it's the ratio of amount of rhythmic similarity within a piece, which
    gives an upper bound on what the omr.corrector.prior measure should be able to
    achieve for the flagged measures. If a piece has low rhythmic similarity in general, then
    there's no way for a correct match to be found within the unflagged measures in the piece.

    Returns a tuple of the total number of NON-flagged measures and the total number
    of those measures that have a rhythmic match.

    Takes in a stream.Score.

    >>> c = converter.parse(omr.correctors.K525omrShortPath)  # first 21 measures
    >>> totalUnflagged, totalUnflaggedWithMatches = omr.evaluators.autoCorrelationBestMeasure(c)
    >>> (totalUnflagged, totalUnflaggedWithMatches)
    (71, 64)
    >>> print( float(totalUnflaggedWithMatches) / totalUnflagged )
    0.901...


    Schoenberg has low autoCorrelation.

    >>> c = corpus.parse('schoenberg/opus19/movement6')
    >>> totalUnflagged, totalUnflaggedWithMatches = omr.evaluators.autoCorrelationBestMeasure(c)
    >>> (totalUnflagged, totalUnflaggedWithMatches)
    (18, 6)
    >>> print( float(totalUnflaggedWithMatches) / totalUnflagged )
    0.333...

    '''
    pass


if __name__ == '__main__':
    import music21
    music21.mainTest()
