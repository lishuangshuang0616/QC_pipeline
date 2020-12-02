python3 ~/work/pipeline/QC/bin/creat_sample_fastq.py -i1 barcode.txt -i2 raw -o sample.txt
python3 ~/work/pipeline/QC/bin/QC_pipeline.py --ini QC.ini --outdir ~/work/pipeline/QC/test
