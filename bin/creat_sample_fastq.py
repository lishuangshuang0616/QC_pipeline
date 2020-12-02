#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   creat_sample_fastq.py
@Time    :   2020/12/01 12:45:17
@Author  :   liss 
@Version :   1.0
@Contact :   liss@personalbio.cn
@Desc    :   将fastq和样本sample对应
'''

import re
import os
import argparse

parser = argparse.ArgumentParser('将fastq和样本sample对应')
parser.add_argument('-i1','--barcode', metavar='FILE', type=str,help='输入barcode.txt文件')
parser.add_argument('-i2','--fastq', metavar='FILE', type=str,help='输入fastq的list文件')
parser.add_argument('-o','--outfile',metavar='FILE',type=str,help='输出样本对应fastq文件')
args = parser.parse_args()


result = open(args.outfile, 'w')
d1 = {}
with open(args.barcode,'r') as lst:
    for l1 in lst:
        l1 = l1.strip()
        k1 = l1.split('\t')[0]
        d1[k1] = l1.split('\t')[1]

d2 = {}
with open(args.fastq,'r') as mat:
    for l2 in mat:
        l2= l2.strip()
        k2 =re.split('_|/',l2)[-3]
        d2.setdefault(k2,[]).append(l2)
        
d3 = {}
for k1,v1 in d1.items():
    for k2,v2 in d2.items():
        if v1 == k2:
            d3[k1] = v2
            a = ",".join(v2)
            result.write(f'{k1}\t{a}'+'\n')
