#!/PERSONALBIO/Work/Mg/Mg03/software/miniconda3/bin/python3.7
# -*- coding: utf-8 -*-

import os, sys

if len(sys.argv) == 0 or len(sys.argv) == 1 or sys.argv[0] in ['-h', '--help'] or sys.argv[1] in ['-h', '--help']:
	print('\n用于统计结果文件，在与样本名称同级的目录下运行\npython3 report_stat.py <sample_list>\n')
	exit()

##预设置 / 读取
#定义函数控制整数千分位、小数位数
def report_num(n, f = 4):
	if isinstance(n, str):
		try:
			n = int(n)
		except ValueError:
			n = float(n)
	if isinstance(n, int):
		n = format(n, ',')
	elif isinstance(n, float):
		if f == 0:
			n = format(int(n), ',')
		elif n == 0:
			n = int(n)
		else:
			n = f'%.{f}f'%n
	return(n)

#工作路径（默认当前路径，若有需要请自行修改）
work_dir = list(os.popen('pwd'))[0].strip()
os.chdir(work_dir)

#读取样本名称列表，几列无所谓，但是第一列一定要为为样本名称
sample_all = []
with open(sys.argv[1], 'r') as sample_file:
	for line in sample_file:
		sample_all.append(line.split('\t')[0].strip())

sample_file.close()

##检查文件
print('\n检查文件，若 Error 请到相应路经检查！')
error = []

for sample_name in sample_all:
	if not os.path.exists(f'{sample_name}/1_RawData/{sample_name}.summary') or not os.path.exists(f'{sample_name}/2_HQData/{sample_name}.summary') or not os.path.exists(f'{sample_all[0]}/1_RawData/fastQC/{sample_all[0]}.R1_fastqc.zip') or not os.path.exists(f'{sample_all[0]}/1_RawData/fastQC/{sample_all[0]}.R2_fastqc.zip'):
		error.append(f'Error：样本 {sample_name} 文件不完整，请检查结果路径')

if error:
	for i in error:
		print(i)
	print('统计终止，请确认文件无误后再运行！\n')
	exit()

##依次统计，生成统计结果文件，用于report
print('\n检查无误，整合统计结果')
os.system('mkdir -p report_stat')

#表2 测序数据统计
table2 = open('report_stat/table2-rawdata_summary.xls', 'w')
print('Sample_Name\tRead_Num\tTotal_base\tN_rate\tGC_Content\tQ20_rate\tQ30_rate', file = table2)
raw_reads = {}

for sample_name in sample_all:
	line = os.popen(f'cat {sample_name}/1_RawData/{sample_name}.summary').readlines()[1].strip().split('\t')
	print(f'{sample_name}\t{report_num(line[1])}\t{report_num(line[2])}\t{report_num(line[3])}\t{report_num(line[4], 2)}\t{report_num(line[5], 2)}\t{report_num(line[6], 2)}', file = table2)
	raw_reads[sample_name] = [int(line[1]), int(line[2])]

table2.close()
print(f'表2 测序数据统计（table2-rawdata_summary.xls），统计完毕')

#表3 数据过滤统计
table3 = open('report_stat/table3-cleandata_summary.xls', 'w')
print('Sample\tHQ Reads\tHQ Reads %\tHQ Data (bp)\tHQ Data %', file = table3)

for sample_name in sample_all:
	hq_msg = os.popen(f'cat {sample_name}/2_HQData/{sample_name}.summary').readlines()[1].strip().split('\t')
	hq_reads_rate = 100 * int(hq_msg[1])/raw_reads[sample_name][0]
	hq_base_rate = 100 * int(hq_msg[2])/raw_reads[sample_name][1]
	print(f'{sample_name}\t{report_num(hq_msg[1])}\t{report_num(hq_reads_rate, 2)}\t{report_num(hq_msg[2])}\t{report_num(hq_base_rate, 2)}', file = table3)

table3.close()
print(f'表3 数据过滤统计（table3-cleandata_summary.xls），统计完毕')

#图2-图5 fastqc质量评估图
os.system(f'unzip -q {sample_all[0]}/1_RawData/fastQC/{sample_all[0]}.R1_fastqc.zip -d report_stat/')
os.system(f'mv report_stat/{sample_all[0]}.R1_fastqc/Images/per_base_quality.png report_stat/figure2-per_base_quality.png')
os.system(f'mv report_stat/{sample_all[0]}.R1_fastqc/Images/per_base_sequence_content.png report_stat/figure3-per_base_sequence_content.png')
os.system(f'mv report_stat/{sample_all[0]}.R1_fastqc/Images/per_sequence_gc_content.png report_stat/figure4-per_sequence_gc_content.png')
os.system(f'mv report_stat/{sample_all[0]}.R1_fastqc/Images/per_sequence_quality.png report_stat/figure5-per_sequence_quality.png')
os.system(f'rm -rf report_stat/{sample_all[0]}_PE400_R1_fastqc')

print(f'图2-图5 fastqc质量评估图，处理完毕')
