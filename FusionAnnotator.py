#!/usr/bin/python

import sys
import argparse
from AnnotatorCore import *

def main(argv):
    if argv.help:
        print 'FusionAnnotator.py -i <input Fusion file> -o <output Fusion file> [-p previous results] [-c <input clinical file>] [-s sample list filter] [-t <default tumor type>] [-u oncokb-base-url] [-b oncokb_api_bear_token]'
        print '  Essential Fusion columns (case insensitive):'
        print '    HUGO_SYMBOL: Hugo gene symbol'
        print '    VARIANT_CLASSIFICATION: Translational effect of variant allele'
        print '    TUMOR_SAMPLE_BARCODE: sample ID'
        print '    FUSION: amino acid change, e.g. "TMPRSS2-ERG fusion"'
        print '  Essential clinical columns:'
        print '    SAMPLE_ID: sample ID'
        print '    ONCOTREE_CODE: tumor type code from oncotree (oncotree.mskcc.org)'
        print '  Cancer type will be assigned based on the following priority:'
        print '     1) ONCOTREE_CODE in clinical data file'
        print '     2) ONCOTREE_CODE exist in Fusion'
        print '     3) default tumor type (-t)'
        print '  Default OncoKB base url is http://oncokb.org'
        sys.exit()
    if argv.input_file == '' or argv.output_file == '' or argv.oncokb_api_bearer_token == '':
        print 'for help: python FusionAnnotator.py -h'
        sys.exit(2)
    if argv.sample_ids_filter:
        setsampleidsfileterfile(argv.sample_ids_filter)
    if argv.cancer_hotspots_base_url:
        setcancerhotspotsbaseurl(argv.cancer_hotspots_base_url)
    if argv.oncokb_api_url:
        setoncokbbaseurl(argv.oncokb_api_url)
    setoncokbapitoken(argv.oncokb_api_bearer_token)

    cancertypemap = {}
    if argv.input_clinical_file:
        readCancerTypes(argv.input_clinical_file, cancertypemap)

    print 'annotating %s ...' % argv.input_file
    processsv(argv.input_file, argv.output_file, argv.previous_result_file, argv.default_cancer_type,
              cancertypemap, False)

    print 'done!'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    # ArgumentParser doesn't accept "store_true" and "type=" at the same time.
    parser.add_argument('-h', dest='help', action="store_true", default=False)
    parser.add_argument('-i', dest='input_file', default='', type=str)
    parser.add_argument('-o', dest='output_file', default='', type=str)
    parser.add_argument('-p', dest='previous_result_file', default='', type=str)
    parser.add_argument('-c', dest='input_clinical_file', default='', type=str)
    parser.add_argument('-s', dest='sample_ids_filter', default=None, type=str)
    parser.add_argument('-t', dest='default_cancer_type', default='cancer', type=str)
    parser.add_argument('-u', dest='oncokb_api_url', default='', type=str)
    parser.add_argument('-v', dest='cancer_hotspots_base_url', default='', type=str)
    parser.add_argument('-b', dest='oncokb_api_bearer_token', default='', type=str)
    parser.set_defaults(func=main)

    args = parser.parse_args()
    args.func(args)
