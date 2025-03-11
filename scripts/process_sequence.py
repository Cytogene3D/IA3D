#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import textwrap
import pickle
import numpy as np
from pyfaidx import Fasta

import orca_predict
from orca_utils import genomeplot
from selene_sdk.sequences import Genome

H1_ESC = 0
HFF = 1
Cell_Types = {"H1-ESC": H1_ESC, "HFF": HFF}


def set_mpos(mpos):
    if mpos == -1:
        mpos = 16_000_000
    return mpos


def get_sequence(fasta, chrom):
    """ Using pysam Fasta to retrieve the sequence"""
    genome = Fasta(fasta)
    sequence = str(genome[chrom][:])
    # Check that the sequence is a 32Mb sequence
    if len(sequence) != 32_000_000:
        print("The fasta sequence must be exactly of size 32000000. Exiting...")
        exit(1)
    return sequence


def dump_target_matrix(predict, output_prefix, mpos, wpos, mutation, chromlen):

    resolutions = ["%dMb" % r for r in [32, 16, 8, 4, 2, 1]]

    # Hff is the second prediction hence 1 in 0-based
    hff_predictions = predict['predictions'][1]
    starts = predict['start_coords']
    ends = predict['end_coords']
    for pred, resol, start, end in zip(hff_predictions, resolutions, starts, ends):
        output = "%s_predictions_%s.txt" % (output_prefix, resol)
        header = ("# Orca=predictions resol=%s mpos=%d wpos=%d start=%d end=%d "
                  "nbins=250 width=%d chromlen=%d mutation=%s" %
                  (resol, mpos, wpos,  start, end, end-start, chromlen, mutation))
        np.savetxt(output, pred, delimiter='\t', header=header, comments='')
    hff_normmats = predict['normmats'][1]
    for pred, resol, start, end in zip(hff_normmats, resolutions, starts, ends):
        output = "%s_normmats_%s.txt" % (output_prefix, resol)
        header = ("# Orca=normmats resol=%s mpos=%s wpos=%d start=%d end=%d "
                  "nbins=250 width=%d chromlen=%d mutation=%s" %
                  (resol, mpos, wpos, start, end, end-start, chromlen, mutation))
        np.savetxt(output, pred, delimiter='\t', header=header, comments='')

    outputlog = "%s.log" % output_prefix
    with open(outputlog, "w") as fout:
        fout.write("# Coordinates of the different matrix in descending order\n")
        fout.write("%d\t%d\n" % (start, end))


def main(fasta, chrom, output_prefix, mutation, mpos=-1):
    """
    """
    sequence = get_sequence(fasta, chrom)

    orca_predict.load_resources(models=['32M', '256M'], use_cuda=True)

    mpos = set_mpos(mpos)
    midpoint = int(len(sequence) / 2)
    wpos = midpoint
    encoded_sequence = Genome.sequence_to_encoding(sequence)[None, :, :]
    outputs_ref = orca_predict.genomepredict(encoded_sequence, chrom,
                                             mpos=mpos, wpos=midpoint,
                                             use_cuda=True)

    output_pkl = "%s.pkl" % output_prefix
    file = open(output_pkl, 'wb')
    pickle.dump(outputs_ref, file)
    chromlen = 158534110
    dump_target_matrix(outputs_ref, output_prefix, mpos, wpos, mutation, chromlen)

    model_labels = ["H1-ESC", "HFF"]
    genomeplot(
        outputs_ref,
        show_genes=False,
        show_tracks=False,
        show_coordinates=True,
        model_labels=model_labels,
        file=output_prefix + ".pdf",
        )


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                     Run glint alignment of query on subject region
                                     '''))
    parser.add_argument('--fasta',
                        required=True, help='fasta file')
    parser.add_argument('--chrom',
                        required=True, help='chrom name')
    parser.add_argument('--outprefix',
                        required=True, help='the output prefix')
    parser.add_argument('--mpos',
                        required=False, help='The coordinate to zoom into for multiscale prediction.',
                        default=-1,  type=int)
    parser.add_argument('--mutation',
                        required=False, help='The coordinate of the mutated bin.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()

    main(args.fasta, args.chrom, args.outprefix, args.mutation, args.mpos)
