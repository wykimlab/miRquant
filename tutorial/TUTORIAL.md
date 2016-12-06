#miRquant               
Last update to README: 12/6/16

## miRquant setup
####Check out a copy of the smRNA pipeline code:
If you don’t already have a directory:

```
$ mkdir /path/to/miRquant
$ cd /path/to/miRquant
$ module load git
$ git clone https://github.com/Sethupathy-Lab/miRquant.git
```

Now you will have a miRquant directory containing all the miRquant scripts.
All of the code is run from this directory!

####Install required programs

cutadapt v1.0
bedtools v2.25.0
bowtie v1.1.0
python v2.7.6
SHRiMP v2.2.2
R v3.2.2

####Download relevant genome fasta files and generate Bowtie indexes

miRquant is currently set up to work with human, mouse and rat, with fruitfly support coming.

The specific genome releases used in miRquant are:

human - [hg19](ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/)
mouse - [mm9](ftp://hgdownload.cse.ucsc.edu/goldenPath/mm9/bigZips/)
rat - [rn4](ftp://hgdownload.cse.ucsc.edu/goldenPath/rn4/bigZips/)

Download the appropriate genomes, and the chromosome sizes (<release>.chrom.sizes) 

Change the genome fasta name to <prefix>.fa and the chromosome sizes file to <prefix>.chromSizes.  The prefixes for each species is as follows:

human - hg19
mouse - mm9
rat - rn4

Generate genome indexes.


##Running miRQuant

####Load proper modules and environmental variables:
```
$ cd /proj/seth_lab/users/ONYEN/miRquant
$ source uncENV.sh
```

####Enter run parameters into the miRquant configuration file

Copy the configuration directory to the directory containing the small RNA-seq fastqs.
```
cp -r /path/to/miRquant/configuration /path/to/fastq_containing_directory
```
The configuration directory contains two configuration files;
1. conf_miRquant.yml
 - Configuration that will be edited for each project to fit the parameters
2. conf_system.yml
 - Configuration file for the cluster you are working on, currently filled out for lsf job scheduler.

The miRquant configuration file (conf_miRquant.yml) is as follows:
```
# Directory locations
paths:
    genome:
        /proj/seth_lab/projects/genome/ 
    mirquant:
        /proj/seth_lab/users/Matt/sm_RNA_pipeline_code/dev/pipeline/   <- location of miRquant
    output:
        /proj/seth_lab/users/Matt/sm_RNA_pipeline_code/dev/mirquant_output/   <- location for the output files
    resources:
        /proj/seth_lab/users/Matt/sm_RNA_pipeline_code/dev/pipeline/bin/resources/   <- location of the resource files

# Location of necessary files
parameters:
    genome_release:
        mm9  <- genome release, must match genome file name (eg: mm9.fa)
    species:
        mmu  <- species, currently set up for hsa, mmu, rno, cast
    Minimum Read Length:
        14   <- minimum length of reads included in 
# Load in options for cutAdapt
cutadapt:
    adapter:
        'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACXXXXXXATCTCGTATGCCGTCTTCTGCTTG'  <- adapter sequence, XXX's will be replaced with sample specific barcode
    overlap:
        10   <- Extent of overlap needed to trim
    error:
        1    <- Number of errors allowed
    Minimum_Read_Length:
        14   <- Minimum length of read following adapter trimming
# Load in options for bowtie
bowtie:
    quality:
        33  <- quality requirement for bowtie alignment
# Load in options for SHRiMP
shrimp:
    path:
        /proj/.test/roach/miRNA/SHRiMP_2_2_2/   <- location of SHRiMP
    dependencies:
        python:
            /proj/.test/roach/miRNA/lib/python/ <- location of python version necessary to run SHRiMP
    quality:
        33   <- quality requirement for SHRiMP alignment
```

####Run the chain submission script:
From the miRquant directory:
```
$ cd /proj/seth_lab/users/ONYEN/miRquant

$ python miRquant.py path/to/MY_PROJECT_NAME/*.fastq

```

Check that your jobs are running
`$ bjobs`

####Once all jobs have finished ( “No unfinished jobs” message):
This might take awhile depending on the number of samples run.
Once the chain submission has finished, you can see if there were any errors in your log files.  The log files will be located in the output folder specified in the configuration file in a directory of the sample name, in a logs directory.

In your MY_PROJECT_NAME directory, there will be a directory for each FILENAME.fastq (called FILENAME.)

In that directory, there will be an IntermediateFiles subdirectory and a FILENAME.stats file.

To get an idea of how the trimming and aligning is looking, type:
```
$ cat /proj/seth_lab/projects/smallRNA/MY_PROJECT_NAME/*/*.stats

file:/proj/seth_lab/projects/smallRNA/MY_PROJECT_NAME/FILENAME.fastq
TotReads:21189608.00000000000000000000
TrimmReads:17621310.00000000000000000000
ShortReads:2500007.00000000000000000000
EMhits:10710591
EMmiss:6910719

TotReads = Total number of reads for this file
TrimmReads = # of reads successfully trimmed of 3’ adapter
ShortReads = # of reads too short after trimming (< 13 )
EMhits =  # of reads with an exact alignment to the genome
EMmiss = # of reads that fail to exactly align to genome
```

####Run the next stage to collect results:
From your pipeline directory (/proj/seth_lab/users/ONYEN/miRquant):
```
$ python runC.py path/to/MY_PROJECT_NAME/
```

Once all of those jobs have finished running, run:
```
$ python post_runC.py path/to/MY_PROJECT_NAME/
```

####Run the next stage to generate TAB separated files:
```
$ bsub python process_summary_to_tab.py path/to/MY_PROJECT_NAME/
```
After run finishes, you should see:
```
$ cd path/to/MY_PROJECT_NAME/
$ cat */*.stats

file:path/to/MY_PROJECT_NAME/FILE.fastq
TotReads:6149484.00000000000000000000
TrimmReads:3730081.00000000000000000000
ShortReads:1938220.00000000000000000000
EMhits:2509867
EMmiss:1220214
Mapped: 2881057.09082651
miRMapped: 1104952.30513136
```

Mapped and miRMapped indicate the number of reads mapped to the genome and to miRNAs respectively.

The log file above will also contain a table that you can use to put together the mapping stats for your project.

Outputs:
For each Sample:
  TAB_3p_summary.txt       -   3'-end differences
  TAB_3p_summary_miR.txt   -   3'-end differences (miRNA loci only)
  TAB_ed_summary.txt       -   central differences
  TAB_lenDist_summary.txt  -   length differences
  Shrimp_results.bed       -   bed file containing all results

##Final processing
Run the muliple final analyses.
```
$ module load python/2.7.6
$ module load R
$ python final_processing.py path/to/MY_PROJECT_NAME/
```
This will produce the mapping statistics, read length distribution, reads per million mapped, reads per million miRs mapped, and the Eucledian distances between the samples.

These final outputs will be in the output folder specified in the configuration file, in a directory named year_month_day_miRquant_num, where the year, month, and day refer to the date and the num will correspond to how many times miRquant had been run on that day.

The final processing scripts create single sheets to be assembled for the final excel report.

The final tab is done manually in excel to get the fold-change and p-value between sample groups.