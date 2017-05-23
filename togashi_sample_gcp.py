#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----------------
# Imports
import os, sys, uuid, time
import datetime
import inspect, pprint
import ConfigParser
import subprocess
from google.cloud import bigquery

# ----------------
# Configs
inifile = ConfigParser.SafeConfigParser()
inifile.read("./togashi-config.ini")

project_name	= inifile.get('General', 'project_name')
source_dataset	= inifile.get('General', 'source_dataset')
source_table	= inifile.get('General', 'source_table')
source_query_target	= ("%s.%s.%s" %( project_name, source_dataset, source_table ) )
dest_dataset	= inifile.get('General', 'dest_dataset')
dest_table	= inifile.get('General', 'dest_table')
dest_query_target	= ("%s.%s.%s" %( project_name, dest_dataset, dest_table ) )

nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


# ----------------
# Functions
def async_query(query, dest_dataset, dest_table):
    # Set Configuration
    client = bigquery.Client()
    dataset = client.dataset( dest_dataset )
    table = dataset.table( name = dest_table )
    query_job = client.run_async_query( str(uuid.uuid4()), str(query) )
    query_job.use_legacy_sql = False
    query_job.destination = table
    query_job.write_disposition	= 'WRITE_APPEND'

    # Run asynchronous query & Insert to dest_dataset.dest_table
    query_job.begin()
    #print("---- Debug start ----")
    #pprint.pprint( inspect.getmembers(query_job) )
    #print("---- Debug end ----")

    # Wait for job
    wait_for_job(query_job)

    # Drain the query results by requesting a page at a time.
    query_results = query_job.results()
    page_token = None

    while True:
        rows, total_rows, page_token = query_results.fetch_data(
        max_results=10,
        page_token=page_token)

        for row in rows:
            print(row)

        if not page_token:
            break

def wait_for_job(job):
    while True:
        job.reload()  # Refreshes the state via a GET request.
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError(job.errors)
            return
        time.sleep(1)

# ----------------
# Main Contents

# Set query
exec_query	= "SELECT host,ident,message,time FROM `" + str(source_query_target) + "` ORDER BY time ASC LIMIT 5;"
print("[Exec Query]\t:\t%s" %( exec_query ) )

# Execute
print("[Exec Time]\t:\t%s" %( nowtime ) )
async_query( exec_query, dest_dataset, dest_table )

sys.exit(0)
