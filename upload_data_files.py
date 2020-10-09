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

parser = argparse.ArgumentParser()
parser.add_argument('-t','--table',required=True,help="File with data to be uploaded to the Data_Files table")
parser.add_argument('-d','--delim',default="\t",help="Table delimeter")
parser.add_argument('-c','--columns')
parser.add_argument('-f','--filesize',help="translate filesize from bytes to corresponding KB/MB/GB")

args = parser.parse_args()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = "" # turn off authentication

labkey_server = 'isentry.bii.virginia.edu'
#TODO: change project name to correct Folder once out of Development
project_name = 'Development'
context_path = 'labkey'
schema = 'lists'
table = 'Data_Files'
context_data_files_table = create_server_context(labkey_server, project_name, context_path, use_ssl=True)

with open(args.table,"r") as table:
    for line in table:
        next_row = {} 
        line = line.strip().split(args.delim)
        next_row["File"] = line[0] 
        next_row["Assay"] = line[1]
        next_row["Bacteria_Sample"] = line[2]
        next_row["Experiment"] = line[3]
        next_row["Filesize"] = line[4]
        next_row["Metadata"] = line[5]
        next_row["Date"] = line[6]
