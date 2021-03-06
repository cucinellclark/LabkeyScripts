from __future__ import unicode_literals

from labkey.utils import create_server_context
from labkey.exceptions import RequestError, QueryNotFoundError, ServerContextError, ServerNotFoundError
from labkey.query import select_rows, update_rows, Pagination, QueryFilter, insert_rows, delete_rows, execute_sql
from requests.exceptions import Timeout
import check_labkey_tables as clt
import sys, humanfriendly
import copy
import argparse
import os.path
import os
import glob
import re
import urllib3

table_headers = ["File","Assay","Bacteria_Sample","Experiment","Filesize","Metadata","Date"]

def validate_table(table,delim):
    missing_headers = []
    valid_table = True
    with open(table,"r") as t:
        header = next(t)
        header = header.strip().split(delim)
        if len(header) != len(table_headers):
            print("Table header lengths do not match, required headers in order: %s"%"\t".join(table_headers))
            print("Input table headers w/ length %s: %s"%(len(header),"\t".join(header)))
            return False
    for i,h in enumerate(table_headers):
        if not h == header[i]:
            valid_table = False
            missing_headers.append(h)
    if len(missing_headers) > 0:
        print("Missing table headers: %s"%"\t".join(missing_headers))
    return valid_table

def translate_filesizes(table):
    new_table = []
    for row_tuple in table:
        filesize = humanfriendly.format_size(int(row_tuple[4]),binary=True)
        new_row = tuple(list(row_tuple[0:4])+[filesize]+list(row_tuple[5:]))
        new_table.append(new_row)
    return new_table

parser = argparse.ArgumentParser()
parser.add_argument('-t','--table',required=True,help="File with data to be uploaded to the Data_Files table")
parser.add_argument('-d','--delim',default="\t",help="Table delimeter")
parser.add_argument('-c','--columns',default=False,action='store_true',help="Prints the required column headers for a table being submitted through this script")
parser.add_argument('-f','--filesize',default=False,action='store_true',help="translate filesize from bytes to corresponding KB/MB/GB")

args = parser.parse_args()

if args.columns:
    print("Required table headers are (in order): %s"%"\t".join(table_headers))
    sys.exit()

#Validate table
if not validate_table(args.table,args.delim):
    print("Invalid table: exiting")
    sys.exit()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = "" # turn off authentication

labkey_server = 'isentry.bii.virginia.edu'
#TODO: change project name to correct Folder once out of Development
project_name = 'Development'
context_path = 'labkey'
schema = 'lists'
table = 'Data_Files'
context_data_files_table = create_server_context(labkey_server, project_name, context_path, use_ssl=True)

#load table into memory
table_list = []
with open(args.table,"r") as t:
    next(t)
    for line in t:
        line = line.strip().split(args.delim)
        table_list.append(tuple(line))    

#translate file sizes if flagged
if args.filesize: 
    table_list = translate_filesizes(table_list)

#valid table keys
bs_keys = clt.get_bacteria_sample_keys()
assay_keys = clt.get_assay_keys()
experiment_keys = clt.get_experiment_keys()

#upload each line
for table_row in table_list:
    next_row = {} 
    next_row["File"] = table_row[0] 
    next_row["Assay"] = table_row[1]
    if table_row[1] not in assay_keys:
        print("%s not in Assay table: exiting"%table_row[1])
        sys.exit()
    next_row["Bacteria_Sample"] = table_row[2]
    if table_row[2] not in bs_keys:
        print("%s not in Bacteria_Sample table: exiting"%table_row[2])
        sys.exit()
    next_row["Experiment"] = table_row[3]
    if table_row[3] not in experiment_keys:
        print("%s not in Experiment table: exiting"%table_row[3])
        sys.exit()
    next_row["Filesize"] = table_row[4]
    next_row["Metadata"] = table_row[5]
    next_row["Date"] = table_row[6]
    insertResult = insert_rows(context_data_files_table,schema,table,[next_row])
