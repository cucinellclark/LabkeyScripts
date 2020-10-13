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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = "" # turn off authentication

#Query assay table to make sure a valid assay is present
def validate_assay():
    return True

#Query experiment table to make sure a valid experiment is present
def valid_experiment():
    return True

parser = argparse.ArgumentParser()
parser.add_argument('-t','--table',required=True)


args = parser.parse_args()

labkey_server = 'isentry.bii.virginia.edu'
project_name = 'Development'
context_path = 'labkey'
schema = 'lists'
table = 'Sample-Assay'
context_sample_assay_table = create_server_context(labkey_server, project_name, context_path, use_ssl=True)
