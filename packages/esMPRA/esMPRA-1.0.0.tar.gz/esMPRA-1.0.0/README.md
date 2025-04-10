# esMPRA: an easy-to-use systematic pipeline for MPRA experiment quality control and data analysis
## 
The code for pipeline implementation of "esMPRA: an easy-to-use systematic pipeline for MPRA experiment quality control and data analysis"


This pipeline is mainly based on the MPRA experiment from [Tewhey et al.](https://www.cell.com/fulltext/S0092-8674(16)30421-4), offering data processing and quality assessment for each MPRA experimental step. It can be installed with a single pip command. After code integration, all functions are accessible via a single command. This pipeline is suitable for various types of MPRA experiments, providing a highly convenient solution for efficient quality control and data processing in MPRA experiments.


## Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Mapping oligos with barcodes after plasmid construction](#step1_oligo_barcode_map)
4. [Getting plasmid abundance after inserting the reporter gene](#step2_get_plasmid_counts)
5. [Getting RNA (cDNA) abundance after reverse transcription](#step3_get_RNA_counts)
6. [Quantifying the activity of cis-regulatory elements](#step4_get_result)
7. [Assessing the reproducibility of the experiment](#step5_compare_diff_rep)
8. [Generating data for MPRAnalyze](#generate_data_for_MPRAnalyze)


## Introduction <a name="introduction">
The MPRA experiment can measure the regulatory activity of numerous cis-regulatory elements simultaneously. Its implementation involves key steps such as plasmid construction, reporter gene insertion, plasmid abundance measurement, and RNA abundance measurement. During each step, it is crucial to assess experimental quality; otherwise, accurate quantification of cis-regulatory element activity becomes difficult. This pipeline leverages prior experimental experience and available MPRA data to establish a quantitative quality control process. It enables quantitative assessment at each experimental stage, helping to identify and avoid potential risks early on. The pipeline also offers strategies for common issues, enhancing experimental success rates and reducing testing cycles. By integrating all codes into a single line command, it allows users to easily implement MPRA quality control and data processing at no cost.

<div align='center'><img align="middle" src="./ref_result/figure.png" width="80%" /><br></div>


## System Requirements <a name="system-requirements">

**Hardware requirements:** 

This package requires only a standard computer with enough RAM to support the in-memory operations.

The test files are from the ENCODE database. All runtime tests below are based on these files. After being organized, they are saved on [ZENODO](https://zenodo.org/records/15034449), and readers can download them for testing or reference.

The reference run time below are measured with CPU: Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz

**OS Requirements:** 

The package has been tested on the following system:
- Linux: CentOS 7.8

The function of this package could be achieved with any OS supporting Python.

**Env Requirements:** 

The package has been tested on the following version of env requirements:
- Python 3.8

Higher version of Python could also support the function of this package.

**Software Dependencies:** 


The pipeline may use [FLASH2](https://github.com/dstreett/FLASH2) besides Python for sequence data processing, which is optional. We recommend installing FLASH2 as it offers better performance and speed. If not installed, provide the --oligo_length parameter when using the step1_oligo_barcode_map function.



**Setup for esMPRA:** 

1. Install Python>=3.7 ref to [Download Python](https://www.python.org/downloads/) or using [Anaconda](https://www.anaconda.com/) by:

    ```
    conda create -n esMPRA python==3.8
    conda activate esMPRA
    ```


2. Install esMPRA using pip (recommended):

    ```
    pip install esMPRA
    ```

    or download this repository and run

    ```
    python setup.py sdist bdist_wheel
    pip install dist/esMPRA-1.0.0-py3-none-any.whl
    ```


3. Install flash2 (optional but suggested):

    We suggest that you install flash2 according to the “INSTALLATION” section here: https://github.com/dstreett/FLASH2. This can improve processing efficiency and quality, and better handle special cases such as particularly long oligo sequences. This step is optional, but we suggest using this tool.



4. Then all the following functions can be implemented via corresponding commands in the command line.


## Mapping oligos with barcodes after plasmid construction <a name="step1_oligo_barcode_map">
In the first step of the MPRA experiment, designed oligo sequences are mapped to random barcode sequences. After constructing the plasmid, sequencing is needed to establish the correspondence between oligo and random barcode sequences for subsequent analysis and quantification. The function of "step1_oligo_barcode_map" is to build this correspondence based on sequencing data and output relevant data for quality control.

### 1. Usage
    ```
    step1_oligo_barcode_map --ref_fa /dir/to/fasta/file/of/designed/oligos.fa --read_1 /dir/to/read1/file.fq --read_2 /dir/to/read2/file.fq --run_name name_for_this_run [options]
    ```

This step will generate a directory with suffix '_step1'

### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --ref_fa                  | True      | str   |        | the directory to the designed oligo library file in fasta format (not including the adapter sequences)     |
| --read_1                  | True      | str   |        | directory to R1 fastq file(s) (.fasta.gz format or .fasta format), sequences in this file are expected to contain the end part of the deigned oligo and the random barcode in reverse complement format; use space to separate multiple files; mitiple files will be processed as merged files     |
| --read_2                  | True      | str   |        | directory to R2 fastq file(s) (.fasta.gz format or .fasta format), sequences in this file are expected contain the start part of the deigned oligo, the order should correspond to the order in read_1; use space to separate multiple files; mitiple files will be processed as merged files    |
| --run_name                | True      | str   |        | the name of this run, allowed to include the specified path.   |
| --oligo_length            | False     | int   | 200       | (required when not using FLASH mode) the length of the designed oligo, if use the FLASH mode, this parameter will be ignored     |
| --use_flash               | False     | action  |       | use FLASH mode, this requires flash2 software installed     |
| --oligo_pre               | False     | str    | GGCCGCTTGACG       | several base paires upstrame the designed oligo, this is used to locate the oligo sequence; if using the protocol by Tewhey et al, the default values can be used directly.    |
| --oligo_after             | False     | str    | CACTGCGGCTCC       | several base paires downstrame the designed oligo, this is used to locate the oligo sequence; if using the protocol by Tewhey et al, the default values can be used directly.     |
| --barcode_pre             | False     | str    | CGAACCTCTAGA       | several base paires upstrame the random barcode, this is used to locate the random barcode; if using the protocol by Tewhey et al, the default values can be used directly.     |
| --quality_threshold       | False     | str    | 30       | quality threshold for the sequencing reads     |
| --barcode_length          | False     | int    | 20       | the length of the random barcode in the experiment     |
| --min_barcode_per_oligo   | False     | int    | 3       | an oligo was qualified only when it was assigned with more than this count of barcode    |
| --flash_read_len          | False     | int    | 250       | average read length passed to flash2     |
| --flash_frag_len          | False     | int    | 274       | fragment length passed to flash2    |
| --flash_threads           | False     | int    | 30       | number of worker threads passed to flash2     |


### 3. Quality control

The "qc_step1" function can realize quality control for this experimental step's results. Using the same run_name as in "step1_oligo_barcode_map" to automatically fetch relevant data and generate a quality control report.

    ```
    qc_step1 --run_name name_for_this_run(same as in step1_oligo_barcode_map)
    ```


The most important parameters in the quality control report are the key parameter evaluation and relevant result images on the first page. If the "Risk Level" in the evaluation is "checked OK", the parameter meets the quality control requirements. A "Medium Risk" indicates a potential quality risk, but 1 - 2 such risks are acceptable. If there are many "Medium Risk" or any "High Risk", there are obvious problems in this experimental step, and you should check and adjust the experiment according to the reference text. 
<div align='center'><img align="middle" src="./ref_result/qc1_1.jpg" width="50%" /><br></div>

Besides the evaluation results, key images also need attention. 

<div align='center'><img align="middle" src="./ref_result/qc1_2.jpg" width="40%" /><br></div>

Users should check for abnormalities according to the image descriptions and take measures to eliminate risks. 

<div align='center'><img align="middle" src="./ref_result/qc1_3.jpg" width="30%" /><br></div>


In addition, there are Additional Quality Control Metrics for auxiliary judgment and assessment of experimental effects, which users can refer to the related reference.

<div align='center'><img align="middle" src="./ref_result/qc1_4.jpg" width="50%" /><br></div>

This step will generate a file with suffix '_step1.pdf'

### 4. Examples for step1_oligo_barcode_map and quality control

We provide ready-to-run Python code for debugging and reference in the test_scripts folder. Before running the test scripts, users need to download the pre-arranged test data from ZENODO [(download data)](https://zenodo.org/records/15034449) and unzip it in the test_scripts folder. Then, run the test script using the following command:


    ```
    python run_step1.py
    ```


Reference run time for this step: 1:01:50, 235% CPU-Util. See the reference running result in the qc_report_for_step1.pdf file within the ref_result folder.

If you haven't installed flash2, you'll need to replace the "--use_flash" command in the script with "--oligo_length 200".

Reference run time for this step (not flash mode): 1:37:07, 99% CPU-Util





## Getting plasmid abundance after inserting the reporter gene <a name="step2_get_plasmid_counts">
After mapping the oligos to the random barcodes, the reporter gene needs to be inserted into the plasmid. After the reporter gene is inserted, another round of sequencing is required to quantify the abundance of the plasmid, which will be used for the quantitative analysis of the activity of cis-regulatory elements. "step2_get_plasmid_counts" quantifies the abundance of each barcode in the plasmid based on this sequencing data and outputs relevant data for quality control. This step needs to be performed based on the completion of step1_oligo_barcode_map.

### 1. Usage
    ```
    step2_get_plasmid_counts --read_1 /dir/to/read1/file.fq --run_name name_for_this_run [options]
    ```

This step will generate a directory with suffix '_step2'

### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --read_1                  | True      | str   |        | directory to R1 fastq file(s) (.fasta.gz format or .fasta format), sequences in this file are expected to contain the random barcode in reverse complement format; use space to separate multiple files; mitiple files will be processed as merged files     |
| --run_name                  | True      | str   |        | the name of this run, allowed to include the specified path     |
| --run_name_step1                  | False      | str   |   same as --run_name     | the name of used run in step1, default is the same as the run name in this step    |
| --barcode_after                  | False      | str   |   TCTAGA     | several base paires downstrame the random barcode, this is used to locate the random barcode    |
| --min_barcode_per_oligo                | False      | int   |   3     | an oligo was qualified only when it was assigned with more than this count of barcode   |
| --barcode_length            | False     | int   | 20       | the length of the random barcode in the experiment     |
| --quality_threshold            | False     | int   | 30       | quality threshold for the sequencing reads     |
| --position_mode               | False     | action  |       | use position mode, if use this mode, the barcode will be located according to the rela_position parameter     |
| --rela_position               | False     | int    | 0       | (required when using position mode) the start potision of the barcode in the read_1 file    |

### 3. Quality control

The "qc_step2" function can realize quality control for this experimental step's results. Using the same run_name as in "step2_get_plasmid_counts" to automatically fetch relevant data and generate a quality control report.

    ```
    qc_step2 --run_name name_for_this_run(same as in step2_get_plasmid_counts)
    ```


The most important parameters in the quality control report are the key parameter evaluation and relevant result images on the first page. If the "Risk Level" in the evaluation is "checked OK", the parameter meets the quality control requirements. A "Medium Risk" indicates a potential quality risk, but 1 - 2 such risks are acceptable. If there are many "Medium Risk" or any "High Risk", there are obvious problems in this experimental step, and you should check and adjust the experiment according to the reference text. 
<div align='center'><img align="middle" src="./ref_result/qc2_1.jpg" width="50%" /><br></div>

Besides the evaluation results, key images also need attention. 

<div align='center'><img align="middle" src="./ref_result/qc2_2.jpg" width="40%" /><br></div>

Users should check for abnormalities according to the image descriptions and take measures to eliminate risks. 

<div align='center'><img align="middle" src="./ref_result/qc2_3.jpg" width="30%" /><br></div>


In addition, there are Additional Quality Control Metrics for auxiliary judgment and assessment of experimental effects, which users can refer to the related reference.

<div align='center'><img align="middle" src="./ref_result/qc2_4.jpg" width="50%" /><br></div>

<div align='center'><img align="middle" src="./ref_result/qc2_5.jpg" width="50%" /><br></div>

This step will generate a file with suffix '_step2.pdf'

### 4. Examples for step2_get_plasmid_counts and quality control

We provide ready-to-run Python code for debugging and reference in the test_scripts folder. Before running the test scripts, users need to download the pre-arranged test data from ZENODO [(download data)](https://zenodo.org/records/15034449) and unzip it in the test_scripts folder. Then, run the test script using the following command:


    ```
    python run_step2.py
    ```

This script includes instructions for running step2_get_plasmid_counts and conducting the corresponding quality control. Additionally, there is a parallel experiment for subsequent reproducibility analysis.

Reference run time for this step: 44:40, 101% CPU-Util. See the reference running result in the qc_report_for_step2.pdf file within the ref_result folder.




## Getting RNA (cDNA) abundance after reverse transcription <a name="step3_get_RNA_counts">
After the insertion of the reporter gene and the determination of plasmid abundance, reverse transcription and sequencing of cDNA are required to quantify the abundance of the transcribed RNA. This RNA abundance, together with plasmid abundance, is used to calculate the activity of cis-regulatory elements. The script “step3_get_RNA_counts” quantifies the abundance of each barcode in cDNA based on the sequencing data from this step and outputs relevant data for quality control.

### 1. Usage
    ```
    step3_get_RNA_counts --read_1 /dir/to/read1/file.fq --run_name name_for_this_run [options]
    ```

This step will generate a directory with suffix '_step3'

### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --read_1                  | True      | str   |        | directory to R1 fastq file(s) (.fasta.gz format or .fasta format), sequences in this file are expected to contain the random barcode in reverse complement format; use space to separate multiple files; mitiple files will be processed as merged files     |
| --run_name                  | True      | str   |        | the name of this run, allowed to include the specified path     |
| --run_name_step1                  | False      | str   |   same as --run_name     | the name of used run in step1, default is the same as the run name in this step    |
| --barcode_after                  | False      | str   |   TCTAGA     | several base paires downstrame the random barcode, this is used to locate the random barcode    |
| --min_barcode_per_oligo                | False      | int   |   3     | an oligo was qualified only when it was assigned with more than this count of barcode   |
| --quality_threshold            | False     | int   | 20       | the length of the random barcode in the experiment     |
| --barcode_length            | False     | int   | 30       | quality threshold for the sequencing reads     |
| --position_mode               | False     | action  |       | use position mode, if use this mode, the barcode will be located according to the rela_position parameter     |
| --rela_position               | False     | int    | 0       | (required when using position mode) the start potision of the barcode in the read_1 file    |

### 3. Quality control

The "qc_step3" function can realize quality control for this experimental step's results. Using the same run_name as in "step3_get_RNA_counts" to automatically fetch relevant data and generate a quality control report.

    ```
    qc_step3 --run_name name_for_this_run(same as in step3_get_RNA_counts)
    ```


The most important parameters in the quality control report are the key parameter evaluation and relevant result images on the first page. If the "Risk Level" in the evaluation is "checked OK", the parameter meets the quality control requirements. A "Medium Risk" indicates a potential quality risk, but 1 - 2 such risks are acceptable. If there are many "Medium Risk" or any "High Risk", there are obvious problems in this experimental step, and you should check and adjust the experiment according to the reference text. 
<div align='center'><img align="middle" src="./ref_result/qc3_1.jpg" width="50%" /><br></div>

Besides the evaluation results, key images also need attention. 

<div align='center'><img align="middle" src="./ref_result/qc3_2.jpg" width="40%" /><br></div>

Users should check for abnormalities according to the image descriptions and take measures to eliminate risks. 

<div align='center'><img align="middle" src="./ref_result/qc3_3.jpg" width="30%" /><br></div>


In addition, there are Additional Quality Control Metrics for auxiliary judgment and assessment of experimental effects, which users can refer to the related reference.

<div align='center'><img align="middle" src="./ref_result/qc3_4.jpg" width="50%" /><br></div>

<div align='center'><img align="middle" src="./ref_result/qc3_5.jpg" width="50%" /><br></div>

This step will generate a file with suffix '_step3.pdf'

### 4. Examples for step3_get_RNA_counts and quality control

We provide ready-to-run Python code for debugging and reference in the test_scripts folder. Before running the test scripts, users need to download the pre-arranged test data from ZENODO [(download data)](https://zenodo.org/records/15034449) and unzip it in the test_scripts folder. Then, run the test script using the following command:


    ```
    python run_step3.py
    ```

This script includes instructions for running step3_get_RNA_counts and conducting the corresponding quality control. Additionally, there is a parallel experiment for subsequent reproducibility analysis.

Reference run time for this step: 57:41, 100% CPU-Util. See the reference running result in the qc_report_for_step3.pdf file within the ref_result folder.




## Quantifying the activity of cis-regulatory elements <a name="step4_get_result">
After completing the mapping of the correspondence between oligos and random barcodes, and the quantification of plasmid abundance and RNA abundance, the activity of cis-regulatory elements can be calculated. The "step4_get_result" script achieves the final quantification of cis-regulatory elements activity based on the results of the preceding steps and provides reference quality control metrics.This step needs to be performed based on the completion of step1_oligo_barcode_map, step2_get_plasmid_counts, and step3_get_RNA_counts.


### 1. Usage
    ```
    step4_get_result --ref_fa --run_name name_for_this_run [options]
    ```

This step will generate a directory with suffix '_step4'. The file "exp_values.tsv" in this folder represents the final quantified activity of the cis-regulatory elements.

### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --ref_fa                  | True      | str   |        | the directory to the designed oligo library file in fasta format (not including the adapter sequences)     |
| --run_name                  | True      | str   |        | the name of this run, allowed to include the specified path     |
| --run_name_step1                  | False      | str   |   same as --run_name     | the name of used run in step1, default is the same as the run name in this step    |
| --run_name_step2                  | False      | str   |   same as --run_name     | the name of used run in step2, default is the same as the run name in this step    |
| --run_name_step3                  | False      | str   |   same as --run_name     | the name of used run in step3, default is the same as the run name in this step    |
| --norm_counts                | False      | int   |   1000000  | estimated counts for normalization   |
| --thresh_for_plm           | False     | int   | 1       | threshold for min plasmid counts, only barcodes with read counts more than (or equal to) this value will be reserved     |
| --thresh_for_rna           | False     | int   | 1       | threshold for min rna counts, only barcodes with read counts more than (or equal to) this value will be reserved     |
| --thresh_for_norm           | False     | int   | 0       | threshold for min normalized counts, only oligos with total normalized counts more than this value will be reserved     |
| --min_barcode_per_oligo           | False     | int   | 3       | an oligo was qualified only when it was assigned with more than (or equal to) this count of valid barcode     |





### 3. Quality control

The "qc_step4" function can realize quality control for this experimental step's results. Using the same run_name as in "step4_get_result" to automatically fetch relevant data and generate a quality control report.

    ```
    qc_step4 --run_name name_for_this_run(same as in step4_get_result)
    ```


In this step, higher values of the first two parameters indicate better results, suggesting a greater number of effective oligos. However, the key quality control parameter is only "PCC_between_plasmid_cDNA." If this parameter is too high, it indicates that the DNA before reverse transcription has not been completely removed. 

<div align='center'><img align="middle" src="./ref_result/qc4_1.jpg" width="50%" /><br></div>

The reference figure also reflects this metric.

<div align='center'><img align="middle" src="./ref_result/qc4_2.jpg" width="40%" /><br></div>


This step will generate a file with suffix '_step4.pdf'

### 4. Examples for step4_get_result and quality control

Because this part no longer corresponds to different steps in the wet lab process compared to step 5, the example scripts for this part and the next part are combined together. We provide ready-to-run Python code for debugging and reference in the test_scripts folder. Users can run the test script using the following command:


    ```
    python run_step4_5.py
    ```

This script includes instructions for running step4_get_result and conducting the corresponding quality control. Additionally, there is a parallel experiment for subsequent reproducibility analysis.

Reference run time for this step: 2:45, 127% CPU-Util. See the reference running result in the qc_report_for_step4.pdf file within the ref_result folder.



## Assessing the reproducibility of the experiment <a name="step5_compare_diff_rep">
After completing the above steps, the activity of the cis-regulatory elements can be obtained. To assess the reproducibility of the experiment, parallel tests are usually conducted. Here, we provide the function “step5_compare_diff_rep” for parallel testing, which can test the correlation between each pair of results based on multiple parallel experiments.


### 1. Usage
    ```
    step5_compare_diff_rep --run_name name_for_this_run --run_name_step4 name_for_step4_rep1 name_for_step4_rep2 name_for_step4_rep3 ...
    ```

This step will generate a directory with suffix '_step5'. The '.png' file(s) in this folder reflects the relationship between different replications.

<div align='center'><img align="middle" src="./ref_result/example_step5.png" width="50%" /><br></div>

### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --run_name                  | True      | str   |        | the name of this run, allowed to include the specified path     |
| --run_name_step4                  | True      | str   |       | all names of runs in step4 to be compared    |


### 3. Examples for step5_compare_diff_rep


Because this part no longer corresponds to different steps in the wet lab process compared to step 4, the example scripts for this part and the previous part are combined together. We provide ready-to-run Python code for debugging and reference in the test_scripts folder. Users can run the test script using the following command:


    ```
    python run_step4_5.py
    ```

This script includes instructions for running step5_compare_diff_rep after running step4_get_result and conducting the corresponding quality control.

Reference run time for this step: 2:45, 127% CPU-Util. See the reference running result in the example_step5.png file within the ref_result folder.



## Generating data for MPRAnalyze <a name="generate_data_for_MPRAnalyze">
In addition to the aforementioned functions, we also provide interfaces for generating the data required for MPRAnalyze, so as to facilitate more in-depth statistical analysis of MPRA data.



### 1. Usage
    ```
    generate_data_for_MPRAnalyse --step1_dir /dir/to/step1 --step2_dir /dir/to/step2 --step3_dir /dir/to/step3 --run_tag tag_for_this_run
    ```

This will generate three files with prefix $tag_for_this_run. These three files are just files required for MPRAnalyze. 


### 2. Explanation for parameters

| Name                      | Required  | Type    | Default | Description |
|-----------------------|----------------------|---------|----------|--------|
| --step1_dir                  | True      | str   |        | the step1 directory where data are used for MPRAnalyze     |
| --step2_dir                  | True      | str   |        | the step2 directory where data are used for MPRAnalyze     |
| --step3_dir                  | True      | str   |        | the step3 directory where data are used for MPRAnalyze     |
| --step4_dir                  | True      | str   |        | the step4 directory where data are used for MPRAnalyze     |
| --run_tag                  | True      | str   |       | tag name used for this run    |


