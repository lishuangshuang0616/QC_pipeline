#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stat_fast.py
@Time    :   2020/12/01 16:44:44
@Author  :   liss 
@Version :   1.0
@Contact :   liss@personalbio.cn
@Desc    :   None
'''

import argparse
import os,glob
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-i','--indir', metavar='DIR', type=str,help='Required')
args = parser.parse_args()


def stat_fastq(i):
    R1 = glob.glob(os.path.join(i, "*R1.*.gz"))[0]
    R2 = glob.glob(os.path.join(i, "*R2.*.gz"))[0]
    code1 = subprocess.run(f"/YZGROUP3/home-new/G02/work/pipeline/QC/bin/fastq_stat {R1}", shell=True, stdout=subprocess.PIPE, check=True)
    code2 = subprocess.run(f"/YZGROUP3/home-new/G02/work/pipeline/QC/bin/fastq_stat {R2}", shell=True, stdout=subprocess.PIPE, check=True)
    read1_num,read1_base,read1_q20,read1_q30,read1_GC,read1_N = code1.stdout.decode('utf-8').strip().split('\t')
    read2_num,read2_base,read2_q20,read2_q30,read2_GC,read2_N = code2.stdout.decode('utf-8').strip().split('\t')

    read_name = i.split('/')[-2]
    read_num = int(read1_num) + int(read2_num)
    total_base = int(read1_base) + int(read2_base)
    Average_Read_Length = float('%.2f' %((int(total_base)/int(read_num) *100)/100))
    total_base_M = format(int(total_base/1000000), ',')
    N_num = int(read1_N)+int(read2_N)
    GC_Num = int(read1_GC) + int(read2_GC)
    Q20_Num = int(read1_q20) + int(read2_q20)
    Q30_Num = int(read1_q30) + int(read2_q30)
    read_q20_rate = float('%.2f' %(((int(read1_q20) + int(read2_q20))*100)/total_base))
    read_q30_rate = float("%.2f" %(((int(read1_q30) + int(read2_q30))*100)/total_base))
    read_GC_rate = float("%.2f" %(((int(read1_GC) + int(read2_GC))*100)/total_base))
    read_N_rate = float("%.4f" %(((int(read1_N)+int(read2_N))*100)/total_base))
    
    with open(os.path.join(i,'%s.summary')%read_name,'w+') as raw:
        raw.write("Sample Name\tRead_Num\tTotal_base\tN_rate\tGC_Content\tQ20_rate\tQ30_rate\tAverage_Read_Length\tN_num\tGC_Num\tQ20_Num\tQ30_Num\n")
        raw.write(f'{read_name}\t{read_num}\t{total_base}\t{read_N_rate}\t{read_GC_rate}\t{read_q20_rate}\t{read_q30_rate}\t{Average_Read_Length}\t{N_num}\t{GC_Num}\t{Q20_Num}\t{Q30_Num}')

if __name__ == "__main__":
    rawdata = os.path.join(args.indir,'1_RawData')
    cleandata = os.path.join(args.indir,'2_HQData')
    stat_fastq(rawdata)
    stat_fastq(cleandata)