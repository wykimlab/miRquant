#miRquant 2.0  

1. Introduction
2. Installation
  1. Requirements
  2. Setup
3. Steps
  1. Adapter trimming
  2. Alignment
    1. Bowtie alignment
    2. Genomic window construction
    3. SHRiMP alignment
  3. Annotation
  4. Final analysis
4. Output

##miRquant introduction  
miRquant 2.0 is a bioinformatic strategy for accurate detection of miRNAs from smRNA-seq data, with an emphasis on separately annotating and quantifying functionally-distinct isoforms of canonical miRNAs, termed isomiRs. In addition to the quantification of miRNA and isomiR expression level, we now provide additional detailed information on the quality of the sequencing data, genome mapping statistics, abundance of other types of small RNAs such as tDRs and yDRs, prevalence of post-transcriptional modifications such as A-to-I edits and 3’ non-templated nucleotide additions, and correlation in miRNA profiles across multiple samples.  Furthermore, miRquant 2.0 is now equipped to handle smRNA-seq data from human, mouse, and rat, and is currently being expanded to fruitfly.  We make publicly available both the tool and a detailed tutorial for users to learn how to run the program and interpret the results.  Below we provide an overview of the miRquant algorithm and the diverse capabilities of the tool.

##miRquant Installation  
###Requirements
#####Software
miRquant 2.0 can be downloaded as a zip file or cloned from the [miRquant GitHub page](https://github.com/Sethupathy-Lab/miRquant).  

In addition to these scripts, miRquant 2.0 requires the following software for various steps of the pipeline.

* cutadapt v1.1.2  
* bedtools v2.25.0  
* bowtie v1.1.0  
* python v2.7.6  
* SHRiMP v2.2.2  
* R v3.2.2 

Install these programs and add their locations to the system path.

#####Resources

miRquant is currently set up to work with human, mouse and rat, with fruitfly support coming.

The specific genome releases used in miRquant are:

human - [hg19](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/)  
mouse - [mm9](http://hgdownload.cse.ucsc.edu/goldenPath/mm9/bigZips/)  
rat - [rn4](http://hgdownload.cse.ucsc.edu/goldenPath/rn4/bigZips/)  

Download the appropriate genomes and the chromosome sizes for that genome release (\<release\>.chrom.sizes) 

###Setup

Once python/2.7.6 and pip are installed, change to the miRquant directory and type:

```
pip install -r requirements.txt
```

Change the genome fasta name to \<prefix\>.fa and the chromosome sizes file to \<prefix\>.chromSizes.  The prefixes for each species is as follows:

human - hg19  
mouse - mm9  
rat - rn4  

Store the genomes and the chromosome size files *in the same location*.

Build Bowtie genome indexes for each genome.  Information on this can be found in the [Bowtie tutorial](http://bowtie-bio.sourceforge.net/tutorial.shtml).

To test that everything was installed correctly, follow the tutorial.

##miRquant steps
![mirquant](https://github.com/Sethupathy-Lab/miRquant/blob/master/.imgs/miRquant_scheme.png "miRquant")
###Adapter trimming

###Alignment
In smRNA-seq, the number of sequenced bases (generally ~50 on the HiSeq 2000 and more recent platforms) exceeds the length of the target RNA fragment.  Therefore, part of the 3’ adapter is sequenced and requires removal prior to genome alignment.  To accomplish this, miRquant 2.0 utilizes the adapter trimming program Cutadapt (version 1.12).  Specifically, miRquant 2.0 requires at minimum a ten-nucleotide overlap between the adapter sequence and the 3’-end of the sequencing read with less than 10% errors in the alignment.  Those reads that do not meet this criterion, or are \<14 nucleotides in length following trimming, are discarded.  Those reads that meet this criterion are subject to trimming and included for further analysis.
#####Bowtie alignment
Alignment of reads to the reference genome is accomplished by a two-tier process.  In the first-tier, Bowtie (version 1.1.0) is used to align only those reads that match perfectly to the genome.  If a read aligns equally well to multiple genomic loci, those reads are proportionally assigned to each of the loci.
#####Genomic window construction
Following this mapping step, miRquant 2.0 assembles contigs or ‘genomic windows’ that contain \>=1 perfectly mapped reads.  If genomic windows are within 65 nucleotides of each other, these windows are merged into larger ‘super genomic windows.’  This step is intended to ensure that all reads potentially related to a single pre-miRNA (roughly 65 to 110 nucleotides in length) are contained within the same window.
#####SHRiMP alignment
In the second-tier, the SHRiMP aligner (version 2.2.2) is used to align reads, with mismatches allowed, only to the genomic windows generated in tier 1.  The types, locations, and number of mismatches allowed are defined in accordance with known patterns of post-transcriptional editing of miRNAs, most notably, A-to-I editing and 3’ non-templated nucleotide addition.  For example, the number of mismatches allowed at the 3’-end of a miRNA-related read ranges from 0 to 3, depending on the length of the read (0 if read length either 14 or 15 nucleotides; 1 if 16 <= read length <= 19; 2 if 20 <= read length <= 23; and 3 if read length > 23).  Similar to the Bowtie step, reads aligning equally well to multiple locations are proportionally assigned to each of those loci.
###Annotation
All reads aligned by the two-tier process outlined above are evaluated for overlap with annotation libraries for miRNAs, tRNAs, and Y-RNAs, which are derived from miRBase, GtRNAdb, and GENCODE, respectively.  For miRNAs, each read overlapping a known miRNA locus is compared to the start position of the reference miRNA listed in miRBase.  If the start position of the read is identical to that of the reference miRNA, the read contributes one count toward the reference miRNA.  If the start position of the read differs from the reference start location, the read contributes one count to an isomiR that is named to represent that offset (e.g., if the read start position is 2 nucleotides upstream of the reported start position for miR-25-3p, the read would be called miR-25-3p_+_2).

For tRNAs, each read overlapping a known tRNA locus in GtRNAdb is named to include the chromosome of origin, amino acid with which it associates, location within the tRNA to which the read maps, total length of the tRNA, and strand (chr#:tRNA#:amino acid and codon:start position in tRNA:end position in tRNA:tRNA length:strand).  More detailed annotation and quantification of tDRs is available through other programs, such as tDRmapper or MINTbase.  The same naming scheme is used for yDRs (Y-RNA loci are defined according to GENCODE annotations).  Reads for which no overlap occurs with miRNA, tRNA, or Y-RNA loci are named according to the genomic location of the start position and the strand (chr#:location#:strand).
###Final analysis

##miRquant output
A hallmark feature of miRquant 2.0 is the extensive information provided on each miRNA, isomiR, or other small RNA detected in the smRNA-seq data.  This information is reported in separate files and these are summarized below.
#####miRquant output on a sample-by-sample basis include (eg SampleA):
```
SampleA/
`-- output
    |-- SampleA.stats                      <- Statistics on various miRquant steps
    |-- Shrimp_results.bed                 <- Full counts from both Bowtie and SHRiMP alignments in bed format
    |-- TAB_3p_summary.txt                 <- Summary of 3' nontemplated nucleotide additions for each locus
    |-- TAB_3p_summary_miR.txt             <- Summary of 3' nontemplated nucleotide additions for each miRNA locus
    |-- TAB_3p_summary_tRNA.txt            <- Summary of 3' nontemplated nucleotide additions for each tDR locus
    |-- TAB_3p_summary_yRNA.txt            <- Summary of 3' nontemplated nucleotide additions for each yDR locus
    |-- TAB_ed_summary.txt                 <- Summary of internal nucleotide substitutions for each locus
    |-- TAB_lenDist_summary.txt            <- Summary of read length distribution for each locus
    `-- read_length_histo_SampleA.txt      <- Summary of read length distribution for all loci combined
```
Example of TAB_3p_summary.txt:
```
Name	tRNA	miRbaseOffset	Seed	Percent	Count	EM	T	A	E	AT	AA	C	TT	AG	G	AAT	TAT	TA	CT	AC	TAA	GC	CA	AGT	AGA	GA	ATT	CTT	AAA	AAAT	TC	TTT	GT	ACT	AATT	TGT	TG	TAAT
	GCT	AAGA	AGAT	TTAT	TATT	ATC	ACCA	AAAA	AAGT	AAAG	TGA	GAG	TTA	AGC	TAC	TTTT	TAAG	TAAA	TCATCT	GGT
Total					66988.6025507	51050.9430268	7366.33333333	4275.16666666	3246.12619048	255.833333333	158.0	104.5	102.
5	60.5	44.5	41.0	39.0	33.5	33.5	18.2	17.0	14.0	12.0	10.0	8.0	7.5	7.0	6.0	6.0	6.0	6.0	5.55.5	5.0	5.0	4.0	4.0	4.0	3.0	2.0	2.0	2.0	2.0	1.0	1.0	1.0	1.0	1.0	1.0	1.0	1.0	1.01.0	1.0	1.0	1.0	1.0	1.0	0.5
mmu-mir-486-5p	Ank1	0	CCTGTAC	0.988499271758	11990.1666667	6707.5	3032	1668.33333333	332.833333333	47.5	49	24	27	4.50.5	10.5	19.5	12	11.5	3	8.5	0	4	2.5	3	0.5	1	0	2.5	3	2	0.5	0	0	1.5	1.5	0	2	0	0	1	1	1	0	0	0.5	0	0.5	0.5	0.5	0.5	0	0.5	0	0.5	0	0.5	0.5	0.5
mmu-mir-486-5p_+_2	Ank1	2	TGTACTG	0.011500728242	139.5	79	26	18	8.5	3	0.5	0	3	0	0	0	00	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0.5	0	0	00	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	0	0	0	0	0
```
where:
  * Name: Name of genomic loci
  * tRNA: Annotation of loci

#####miRquant output for all project samples include:
```
2016_12_7_miRquant_1/
|-- Mapping_Statistics.csv                 <- Statistics on various miRquant steps
|-- RPMMM_all.csv                          <- Reads per million mapped to miRNAs (RPMMM)
|-- RPMMM_mirs_over_50.csv                 <- RPMMMs over 50 for at least one sample
|-- RPMM_all.csv                           <- Reads per million mapped (RPMM)
|-- RPMM_mirs_over_100.csv                 <- RPMM over 100 for at least one sample
|-- length_distribution.csv                <- Read length distribution for samples as table
|-- length_distribution.png                <- Read length distribution for samples as bar graph
|-- sample_correlation_heatmap.png         <- Sample pair-wise Pearson correlation values as heatmap with hierarchical clustering
`-- sample_correlation_values.csv          <- Sample pair-wise Pearson correlation table
```

####Mapping statistics
![MapStats](https://github.com/Sethupathy-Lab/miRquant/blob/master/.imgs/mapping_statistics.png "Mapping Statistics")
From the mapping statistics, users can determine the number of total reads generated, as well as the number and percentage of total reads that were successfully trimmed, trimmed reads that were mapped by Bowtie and SHRiMP, mapped reads that pertain to miRNAs, tRNAs, or Y-RNAs.  These data inform the user of potential quality issues with the sample (RNA degradation, adapter dimerization during library prep, poor sequencing) as well as the relative abundance of different types of small RNAs represented in the data.

####Length distribution
![LenDist](https://github.com/Sethupathy-Lab/miRquant/blob/master/.imgs/length_histogram.png "Length distribution")
For each sample, miRquant reports the length distributions of all trimmed reads.  A peak at ~18-24 nucleotides likely represents mature miRNAs, a subclass of tDRs known as tRNA fragments (tRFs), and possibly yDRs.  A peak at ~30-33 nucleotides likely represents a subclass of tDRs referred to as tRNA halves (tRHs), and possibly yDRs.  Elevated signal at other read sizes could indicate other known or novel small RNAs, but could also be suggestive of degradation.

####Cross-sample comparisons
![ExpHM](https://github.com/Sethupathy-Lab/miRquant/blob/master/.imgs/expression_heatmap.png "Expression correlation heatmap")
miRquant computes pair-wise Pearson correlations of miRNA expression profiles across all samples and carries out hierarchical clustering to plot the expression correlation heatmap.  Only miRNAs above a specified expression threshold are included in the correlation analysis.  An example is provided, in which miRNA profiles are being compared across two different conditions, with three replicates each.  The color in each of the squares in the heatmap corresponds to the extent of miRNA expression correlation between two particular samples.  In this example, the heatmap and dendogram show that the replicates are grouped appropriately by condition, and that the two conditions cluster separately.

####Normalized expression
![RPMM](https://github.com/Sethupathy-Lab/miRquant/blob/master/.imgs/normalized_reads_table.png "Normalized reads")  
Read count normalization is performed in two ways.  For a given miRNA/isomiR/tDR/yDR in a sample, the number of corresponding reads is divided by the total number of mapped reads and multiplied by 1 million.  This is referred to as the reads per million mapped (RPMM).  For miRNAs/isomiRs, an alternative method of normalization is employed.  Specifically, the number of corresponding reads is divided by the total number of reads mapped to all miRNA/isomiR loci and multiplied by 1 million.  This is referred to as reads per million mapped to miRNAs (RPMMM).  The latter approach is generally favored for miRNAs.  Notably, the types, locations, and frequency of potential post-transcriptional editing events are reported for every annotated miRNA/isomiR/tDR/yDR in the sample.  Edits are separated into two groups: internal edits and 3’ non-templated additions.
