from __future__ import unicode_literals

from labkey.utils import create_server_context
from labkey.exceptions import RequestError, QueryNotFoundError, ServerContextError, ServerNotFoundError
from labkey.query import select_rows, update_rows, Pagination, QueryFilter, insert_rows, delete_rows, execute_sql
from requests.exceptions import Timeout
import sys 
import copy
import argparse
import os.path
import os
import glob
import re
import urllib3

#Macros used in each checking function
LABKEY_SERVER = 'isentry.bii.virginia.edu'
CONTEXT_PATH = 'labkey'
SCHEMA = 'lists'

#Environment setup for each checking function
def setup():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    os.environ["CURL_CA_BUNDLE"] = "" # turn off authentication

#Checks if 'check_bacteria' is an entry in the Bacteria_Sample table
def get_bacteria_sample_keys():
    setup()
    project_name = 'Development'
    table = "Bacteria_Sample"
    context_bs = create_server_context(LABKEY_SERVER,project_name,CONTEXT_PATH,use_ssl=True)
    try:
        bs_result = select_rows(context_bs,SCHEMA,table)
        bs_keys = []
        if bs_result is not None: 
            for bs in bs_result['rows']:
                bs_keys.append(bs['B_ID'])
            return bs_keys
        else:
            print("Failed to retrieve rows from Bacteria_Sample table")
            return None
    except ServerContextError:
        print('Failed to create server context with Bacteria_Sample table')

def get_assay_keys():
    setup()
    project_name = 'Development'
    table = "Assay"
    context_assay = create_server_context(LABKEY_SERVER,project_name,CONTEXT_PATH,use_ssl=True)
    try:
        assay_result = select_rows(context_assay,SCHEMA,table)
        assay_keys = []
        if assay_result is not None:
            for ar in assay_result['rows']:
                assay_keys.append(ar['Assay'])
            return assay_keys
        else:
            print("Failed to retrieve rows from Assay table")
            return None
    except ServerContextError:
        print('Failed to create server context with Assay table')
        return None

def get_experiment_keys():
    setup()
    project_name = 'Development'
    table = "Experiment"
    context_experiment = create_server_context(LABKEY_SERVER,project_name,CONTEXT_PATH,use_ssl=True)
    try:
        experiment_result = select_rows(context_experiment,SCHEMA,table)
        experiment_keys = []
        if experiment_result is not None:
            for er in experiment_result['rows']:
                experiment_keys.append(er['Experiment'])
            return experiment_keys
        else:
            print("Failed to retrieve rows from Experiment table")
            return None
    except ServerContextError:
        print('Failed to create server context with Experiment table')
        return None
