# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# SENTEVAL_LICENSE file in the root directory of this source tree.
#


"""
    This module contains different functions to load the test datasets
    of the SemEval's STS tasks from 2012 to 2016. This functions are based
    on those found in the SentEval toolkit.
"""


import io
import numpy as np
from utils import preprocess


def loadFile(path, datasets, preprocessing):
    """ Loads and STS file and pre-processes its sentences """
    data = {}

    for dataset in datasets:
        # Load sentences pairs
        sent1, sent2 = zip(*[l.split("\t") for l in
                            io.open(path + '/STS.input.%s.txt' % dataset,
                                    encoding='utf8').read().splitlines()])
        # Load Gold Standard files (similarity scores)
        raw_scores = np.array([x for x in
                                io.open(path + '/STS.gs.%s.txt' % dataset,
                                        encoding='utf8')
                                .read().splitlines()])
        # Consider only pairs with a score
        not_empty_idx = raw_scores != ''

        gs_scores = [float(x) for x in raw_scores[not_empty_idx]]

        # Preprocess sentences
        print("Preprocessing -{}-".format(dataset))
        sent1 = preprocess(sent1, **preprocessing)[not_empty_idx]
        sent2 = preprocess(sent2, **preprocessing)[not_empty_idx]
        print("-{}- preprocessed correctly".format(dataset))
        
        # Sort data by length to minimize padding in batcher
        sorted_data = sorted(zip(sent1, sent2, gs_scores),
                                key=lambda z: (len(z[0]), len(z[1]), z[2]))
        sent1, sent2, gs_scores = map(list, zip(*sorted_data))

        data[dataset] = (sent1, sent2, gs_scores)
        
    return data

def loadSTS12(path, preprocessing):
    """ Loads the SemEval-2012's Semantic Textual Similarity task"""
    print('\n***** TASK: STS12 *****\n')
    datasets = ['MSRpar', 'MSRvid', 'SMTeuroparl',
                        'surprise.OnWN', 'surprise.SMTnews']
    return loadFile('{}/STS12-en-test'.format(path), datasets, preprocessing)

def loadSTS13(path, preprocessing):
    """ Loads the SemEval-2013's Semantic Textual Similarity task"""
    # STS13 here does not contain the "SMT" subtask due to LICENSE issue
    print('\n***** TASK: STS13 (-SMT) ***\n\n')
    datasets = ['FNWN', 'headlines', 'OnWN']
    return loadFile('{}/STS13-en-test'.format(path), datasets, preprocessing)

def loadSTS14(path, preprocessing):
    """ Loads the SemEval-2014's Semantic Textual Similarity task"""
    print('\n***** TASK: STS14 *****\n')
    datasets = ['deft-forum', 'deft-news', 'headlines',
                        'images', 'OnWN', 'tweet-news']
    return loadFile('{}/STS14-en-test'.format(path), datasets, preprocessing)

def loadSTS15(path, preprocessing):
    """ Loads the SemEval-2015's Semantic Textual Similarity task"""
    print('\n***** TASK: STS15 *****\n')
    datasets = ['answers-forums', 'answers-students',
                        'belief', 'headlines', 'images']
    return loadFile('{}/STS15-en-test'.format(path), datasets, preprocessing)

def loadSTS16(path, preprocessing):
    """ Loads the SemEval-2016's Semantic Textual Similarity task"""
    print('\n***** TASK: STS16 *****\n')
    datasets = ['answer-answer', 'headlines', 'plagiarism',
                        'postediting', 'question-question']
    return loadFile('{}/STS16-en-test'.format(path), datasets, preprocessing)

