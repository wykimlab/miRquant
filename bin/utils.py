#!/usr/bin/python2

usage='''
  Assembly of multiple functions used throughout the pipeline, including:
    1. Logging
    2. Importing configuration file
    3. Checking input arguments and printing usage
    4. Define location of resource_paths
'''

import yaml
import os
import sys
import logging


def remove_if_exists(path_):
    '''
    Check whether a file or directory exists, and if so, remove it
    '''
    if os.path.exists(path_):
        os.system('rm -r {}'.format(path_))
    

def check_input():
    '''
    Check whether there were arguments supplied to the script, otherwise
    print the usage and exit
    '''
    if len(sys.argv) < 2:
        print usage
        sys.exit()


def return_sample_results_directories(dir_):
    '''
    List content of directory and return directories ending in period (sample 
    directories).
    '''
    return ['{}/{}'.format(dir_, d) for d in os.listdir(dir_) if d[-1] == '.']


def check_logging_level(level):
    '''
    Check to see how verbose the logging should be.
    '''
    if level == 'v':
        return 'logging.WARNING'
    elif level == 'vv':
        return 'logging.INFO'
    elif level == 'vvv':
        return 'logging.DEBUG'
    else:
        print 'ERROR: Logging level not recognized'
        print 'Use v for low ouput, vv for mid output, and vvv for high output'
    sys.exit()


def initiate_logging(log_path = './', log_name = 'log.txt', log_l = 'vvv'):
    '''
    Creates a logging file for standard out
    '''
    log_l = check_logging_level(log_l)
    log_fi = '{}{}'.format(log_path, log_name)
    logging.basicConfig(filename = log_fi, 
                        format = '%(message)s',
                        level=logging.DEBUG)


def load_mirquant_config_file(config_path = './configuration/'):
    '''
    Load miRquant configuration file, which contains the various arguments,
    paths, and executable parameters supplied by the user.  File is in yaml
    format.
    '''
    with open('{}/conf_miRquant.yml'.format(config_path), 'r') as config_f:
        cfg = yaml.load(config_f)
    return cfg


def load_sys_config_file(config_path = './configuration/'):
    '''
    Load miRquant configuration file, which contains the various arguments,
    paths, and executable parameters supplied by the user.  File is in yaml
    format.
    '''
    try:
        with open('{}/conf_system.yml'.format(config_path), 'r') as config_f:
            return yaml.load(config_f)
    except IOError:
        return {'job' : {}}


def build_job(di):
    '''
    Builds job command line from system configuration yaml di
    '''
    cmd = ''
    for job in di:
        cmd += '{} '.format(job)
        for k, v in di[job].iteritems():
            cmd += '{} {} '.format(k, v)
    return cmd


def sample_output_paths(out_path, sample):
    '''
    Sets up the output directories for the sample.
    '''
    out_dir = '{}{}'.format(out_path, sample)
    return {l: '{}/{}/'.format(out_dir, l) for l in ['output', 'log', 'temp']}


def resource_paths(species, paths, para):
    '''
    Load the paths to all the resource files for a species.  Check if the file
    exists, otherwise raise error and exit.
    '''
    g_dir = paths['genome']
    r_dir = paths['resources']
    g_ver = para['genome_release']
        
    genome = '{}{}.fa'.format(g_dir, g_ver)
    table = '{}{}_table.txt'.format(r_dir, species)
    tableL = '{}{}_tableL.bed'.format(r_dir, species)
    tRNAlib = '{}{}_mature_tRNA_LIB.fa'.format(r_dir, g_ver)
    tRNAbed = '{}{}_tRNA.bed'.format(r_dir, g_ver)
    tRNAbed12 = '{}{}_tRNA12.bed'.format(r_dir, g_ver)
    refAnn = '{}{}_ref.bed'.format(r_dir, g_ver)
    genBase = '{}{}'.format(g_dir, g_ver)

    for file in [genome, table, tableL, tRNAlib, tRNAbed, tRNAbed12, refAnn]:
        if not os.path.isfile(file):
            log.ERROR('ERROR: {} does not exist!'.format(file))
            log.ERROR('Generate this resource file before running miRquant')
            sys.exit()
    return [genome, table, tableL, tRNAlib, tRNAbed, tRNAbed12, refAnn, genBase]


def ftoi(x):
    '''
    Checks if number is whole, and if so, apply int() to number.
    '''
    try:
        return int(x) if int(x) / x == 1 else float(x)
    except ZeroDivisionError:
        return 0
