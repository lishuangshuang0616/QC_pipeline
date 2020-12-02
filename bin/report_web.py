#!/PERSONALBIO/Work/Mg/Mg03/software/miniconda3/bin/python3.7
# -*- coding: utf-8 -*-

import os, sys

##定于函数，用于将表格/图片读入 html
#用于将表格写入 html
def table_write(table, out, id, indent = 3):
	div = f'''{indent*'    '}<div align="center" style="padding-bottom:15px">\n{(indent+1)*'    '}<table id="{id}">\n'''
	
	with open(table, 'r') as table:
		line = table.readline().strip().split('\t')
		div += f'''{(indent+2)*'    '}<thead>\n{(indent+3)*'    '}<tr>'''
		for i in line:
			div += f'''<th>{i}</th>'''
		div += f'''</tr>\n{(indent+2)*'    '}</thead>\n'''
		div += f'''{(indent+2)*'    '}<tbody>\n'''
		
		for line in table:
			div += f'''{(indent+3)*'    '}<tr>'''
			line = line.strip().split('\t')
			for i in line:
				div += f'''<td align="center">{i}</td>'''
			div += '''</tr>\n'''
		div += f'''{(indent+2)*'    '}</tbody>\n{(indent+1)*'    '}</table>\n{indent*'    '}</div>'''
	
	print(div, file = out)

#用于将图片写入 html
def figure_write(figure, out, indent = 3):
	print(f'''{indent*'    '}<br><a href="{figure}" target="_blank"><center><img src="{figure}" height="60%" width="60%" /></center></a><br>''', file = out)

##执行操作
#工作路径（默认当前路径，若有需要请自行修改）
work_dir = list(os.popen('pwd'))[0].strip()
os.chdir(work_dir)

#读取样本名称列表，几列无所谓，但是第一列一定要为为样本名称
sample_all = []
sample_file = open(sys.argv[1], 'r')
for line in sample_file:
	sample_all.append(line.split('\t')[0].strip())

sample_file.close()

#移动报告模板、统计文件至工作路径
os.system('mkdir -p report')
if os.path.exists('report/src'):
	os.system(f'rm -rf report/src')
	os.system('cp -r /YZGROUP4/STORAGE/personalbio/Work/Genome/G04/software/YZ_zhiguolv_Mg/report_template/src ./report')
else:
	os.system('cp -r /YZGROUP4/STORAGE/personalbio/Work/Genome/G04/software/YZ_zhiguolv_Mg/report_template/src ./report')

if os.path.exists('report/report_stat'):
	os.system(f'rm -rf report/report_stat')
	os.system(f'cp -r {sys.argv[3]} ./report/report_stat')
else:
	os.system(f'cp -r {sys.argv[3]} ./report/report_stat')

#读取手动配置文件
project = open(sys.argv[2], 'r')

for line in project:
	line = line.strip()
	if line and line[0] != '#':
		var_name = line.split('=')[0].strip()
		var_value = line.split('=')[1].strip()
		exec(var_name + " = var_value")

project.close()

#生成客户/公司信息
indent = 4
illumina = illumina.split('_')

title = f'''{indent*'    '}<tr><td align="center" colspan="4">项目信息</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">项目编号</td><td align="center" width="500px" colspan="3">{项目编号}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">开题单号</td><td align="center" width="500px" colspan="3">{开题单号}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">项目类型</td><td align="center" width="500px" colspan="3">{项目类型}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">样品个数</td><td align="center" width="500px" colspan="3">{样品个数}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">测序平台</td><td align="center" width="500px" colspan="3">Illumina {illumina[0]}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">分析类型</td><td align="center" width="500px" colspan="3">{分析类型}</td></tr>
	{indent*'    '}<tr><td align="center" colspan="4">客户信息</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">单位名称</td><td align="center" width="500px" colspan="3">{单位名称}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">单位地址</td><td align="center" width="500px" colspan="3">{单位地址}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">课题组负责人</td><td align="center" width="100px" colspan="3">{课题组负责人}</td></tr>
	{indent*'    '}<tr><td align="center" width="200px">项目联系人</td><td align="center" width="100px" colspan="3">{项目联系人}</td></tr>
	{indent*'    '}<tr><td align="center" colspan="4">派森诺联系人</td></tr>
	{indent*'    '}<tr><td align="center" width="200px" rowspan="2">技术支持</td><td align="center" width="100px" rowspan="2">{技术支持}</td><td align="center" width="100px">电话</td><td align="center" width="300px">021-64502808-8085</td></tr>
	{indent*'    '}<tr><td align="center" width="100px">邮箱</td><td align="center" width="300px">microsupport@personalbio.cn</td></tr>

#生成 table1
table1 = open('./report/report_stat/table1-sample.xls', 'w')
print('Sample\tLib. Name\tLib. Insert Size\tSequencing platform\tSequencing Mode', file = table1)

for sample_name in sample_all:
	print(f"{sample_name}\tPE\t400 bp\tIllumina {illumina[0]}\tPaired-end, 2×{illumina[1].split('PE')[1]}bp", file = table1)

table1.close()

#套用报告模板，添加内容
os.chdir('report')
report_test = open(f'{开题单号}.html', 'w')

with open('/YZGROUP4/STORAGE/personalbio/Work/Genome/G04/software/YZ_zhiguolv_Mg/report_template/report_temp.html', 'r') as temp:
	for line in temp:
		
		#title
		if '@@title@@' in line:
			print(title, file = report_test)
		elif '@@单位名称@@' in line:
			line = line.strip('\n').split('@@单位名称@@')
			print(f'{line[0]}{单位名称}{line[1]}', file = report_test)
		elif '@@制定日期@@' in line:
			line = line.strip('\n').split('@@制定日期@@')
			print(f'{line[0]}{制定日期}{line[1]}', file = report_test)
		elif '@@项目类型@@' in line:
			line = line.strip('\n').split('@@项目类型@@')
			print(f'{line[0]}{项目类型}{line[1]}', file = report_test)
        
		#样品信息
		elif '@@PE@@' in line and '@@sample_number@@' in line:
			line = line.strip('\n').split('@@PE@@')
			line = f'{line[0]}{illumina[0]}{line[1]}'
			line = line.split('@@sample_number@@')
			line = f'{line[0]}{样品个数}{line[1]}'
			print(line, file = report_test)
		
		#表格
		elif '@@table1@@' in line:
			table_write('./report_stat/table1-sample.xls', out = report_test, id = 'table1', indent = 3)
		elif '@@table2@@' in line:
			table_write('./report_stat/table2-rawdata_summary.xls', out = report_test, id = 'table2', indent = 3)
		elif '@@table3@@' in line:
			table_write('./report_stat/table3-cleandata_summary.xls', out = report_test, id = 'table3', indent = 3)
		
		#图片
		elif '@@figure2@@' in line:
			figure_write('./report_stat/figure2-per_base_quality.png', out = report_test, indent = 3)
		elif '@@figure3@@' in line:
			figure_write('./report_stat/figure3-per_base_sequence_content.png', out = report_test, indent = 3)
		elif '@@figure4@@' in line:
			figure_write('./report_stat/figure4-per_sequence_gc_content.png', out = report_test, indent = 3)
		elif '@@figure5@@' in line:
			figure_write('./report_stat/figure5-per_sequence_quality.png', out = report_test, indent = 3)
		
		#示例样本
		elif '@@sample_example@@' in line:
			line = line.strip('\n').split('@@sample_example@@')
			print(f'{line[0]}{sample_all[0]}{line[1]}', file = report_test)
		
		#模板其余部分直接使用
		else:
			print(line.strip('\n'), file = report_test)

temp.close()
report_test.close()
