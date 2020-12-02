#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   cat_fastq.py
@Time    :   2020/12/01 12:56:33
@Author  :   liss 
@Version :   1.0
@Contact :   liss@personalbio.cn
@Desc    :   None
'''

import re
import os
import argparse

parser = argparse.ArgumentParser('样本多次测序数据进行合并，目前只给出两个目录')
parser.add_argument('-f','--barcode',metavar='FILE',type=str,help='输入barcode.txt文件')
parser.add_argument('-i1','--indir1', metavar='DIR', type=str,help='fastq目录1')
parser.add_argument('-i2','--indir2', metavar='DIR', type=str,help='fastq目录2')
parser.add_argument('-o','--outdir',metavar='DIR',type=str,help='合并后的fastq目录')
args = parser.parse_args()

fastq_name = []
with open(args.barcode,'r') as barcodeFile:
    for line in barcodeFile:
        line = line.strip()
        lst = line.split('\t')[-1]
        fastq_name.append(lst)

for barcode_name in fastq_name:
    