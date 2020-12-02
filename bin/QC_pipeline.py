#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   QC_pipeline.py
@Time    :   2020/12/01 15:49:38
@Author  :   liss 
@Version :   1.0
@Contact :   liss@personalbio.cn
@Desc    :   None
'''

import os
import configparser
import argparse
import pathlib
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--ini', metavar='FILE', type=str,help='Required')
parser.add_argument('--outdir', metavar='FILE', type=str,default=os.getcwd())
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.ini)
outdir = args.outdir

sampleDict = {}
with open(config['Sample']['samplelist'],'r') as f:
    for line in f:
        line = line.strip()
        lst = line.split('\t')
        sampleDict[lst[0]] = lst[1]

output = os.path.join(outdir)
output = pathlib.Path(output)

shell_list = []

############################   QC   ########################################
for sample in sampleDict.keys():
    sampledir = os.path.join(output,sample)
    pathlib.Path(sampledir).mkdir(parents=True, exist_ok=True)
    rawdata = os.path.join(sampledir,'1_RawData')
    cleandata = os.path.join(sampledir,'2_HQData')
    pathlib.Path(rawdata).mkdir(parents=True, exist_ok=True)
    pathlib.Path(cleandata).mkdir(parents=True, exist_ok=True)
    fq1 = sampleDict[sample].split(',')[0]
    fq2 = sampleDict[sample].split(',')[1]

    shell_list.append('bsub -q psn -n 1 -J %s -o %s.o -e %s.e "sh %s/%s.qc.sh"'%(sample,sample,sample,sampledir,sample))
    
    with open(sampledir + '/%s.qc.sh'%sample,'w') as QC_sh:
        QC_commands = []
        QC_commands.append('ln -s %s %s/%s.R1.fastq.gz'%(fq1,rawdata,sample))
        QC_commands.append('ln -s %s %s/%s.R2.fastq.gz'%(fq2,rawdata,sample))
        QC_commands.append('mkdir -p %s/fastQC'%(rawdata))
        QC_commands.append('%s/fastqc %s/%s.R1.fastq.gz -t 2 -o %s/fastQC'%(config['Bin']['Bin'],rawdata,sample,rawdata))
        QC_commands.append('%s/fastqc %s/%s.R2.fastq.gz -t 2 -o %s/fastQC'%(config['Bin']['Bin'],rawdata,sample,rawdata))
        QC_commands.append('%s/fastp -i %s/%s.R1.fastq.gz -o %s/%s_HQ_R1.fq.gz -I %s/%s.R2.fastq.gz -O %s/%s_HQ_R2.fq.gz --compression=4 --adapter_sequence=%s --adapter_sequence_r2=%s --length_required=50 --average_qual=20 -n 3 -w 10'%(config['Bin']['Bin'],rawdata,sample,cleandata,sample,rawdata,sample,cleandata,sample,config['Adapter']['Adapter1'],config['Adapter']['Adapter2']))
        QC_commands.append('python3 %s/stat_fastq.py -i %s'%(config['Bin']['Bin'],sampledir))  
        QC_sh.write('\n'.join(QC_commands))

with open(output/'qsub.sh','w') as shelllist:
    shelllist.write('\n'.join(shell_list))

cmd = 'cut -f1 %s/barcode.txt > %s/sample_list'%(output,output)
os.system(cmd)

with open(output/'report.sh','w') as reportlist:
    reportlist.write('python3 %s/report_stat.py sample_list'%config['Bin']['Bin'] +'\n')
    reportlist.write('python3 %s/report_web.py sample_list project.txt report_stat'%config['Bin']['Bin']+'\n')