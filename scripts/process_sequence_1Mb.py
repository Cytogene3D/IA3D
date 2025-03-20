#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import textwrap
import pickle
import numpy as np
from pyfaidx import Fasta

import orca_predict
from orca_predict import *
from orca_utils import genomeplot
from selene_sdk.sequences import Genome

H1_ESC = 0
HFF = 1
Cell_Types = {"H1-ESC": H1_ESC, "HFF": HFF}


def pred_1Mb(seq, model):
    pred = model(seq.transpose(1, 2))
    return pred


def main(chrom, start, output_prefix, use_cuda=True):
    """
    """
    orca_predict.load_resources(models=['1M'], use_cuda=use_cuda)
    from orca_predict import *

    encoded_sequence = hg38.get_encoding_from_coords(chrom, start, start + 1000000)[None, :, :]
    prediction = pred_1Mb(torch.FloatTensor(encoded_sequence).cpu(), hff_1m)



def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                     Run glint alignment of query on subject region
                                     '''))
    parser.add_argument('--fasta',
                        required=True, help='fasta file')
    parser.add_argument('--chrom',
                        required=True, help='chrom name')
    parser.add_argument('--start', type=int,
                        required=True, help='chrom name')
    parser.add_argument('--nocuda',
                        action="store_true", help='Switching to cpu (default: False)')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()

    use_cuda = not args.nocuda
    main(args.fasta, args.chrom, use_cuda)
