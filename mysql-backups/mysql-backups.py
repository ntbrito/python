#!/usr/bin/python

import json
import sys
import os
import re
import getopt
from datetime import date

today = date.today()
## working_dir = os.path.dirname(os.path.abspath(__file__))
working_dir = os.getcwd()
logs_file = working_dir + '/log/mysql-backups.log'

## Functions ##

## Write logs
def write_log(database_name):
    file_log = open(logs_file, 'a')
    file_log.write('============================ \n')
    file_log.write('Backup for the day %s \n' % str(today))
    file_log.write('Database to backup: %s \n\n' % database_name)
    file_log.close()


## Connect and upload files to the S3 bucket
def connect_s3(sql_file):
    import boto
    from boto.s3.key import Key
    from boto.s3.connection import S3Connection

    ## Info on the bucket from the json file
    access_key = sites_list['s3_bucket']['aws_access_key']
    secret_key = sites_list['s3_bucket']['aws_secret_key']
    path = sites_list['s3_bucket']['path']
    bucket_name = sites_list['s3_bucket']['bucket_name']

    ## Connect to the bucket
    connection = boto.connect_s3(
                  aws_access_key_id = access_key,
                  aws_secret_access_key = secret_key
                  )

    bucket = connection.get_bucket(bucket_name)
    file_name = sql_file
    full_key_name = os.path.join(path, file_name)
    key = bucket.new_key(full_key_name)
    key.set_contents_from_filename(file_name)


## Backup a specifc site on a given json file
def cloudsite_backup(sites_list, site_to_backup):

    for site in sites_list['sites']:
        site_name = site['site_name']


        if (site_name == site_to_backup):
            site_database = site['database']['database_name']
            site_user = site['database']['database_user']
            site_ip = site['database']['database_ip']
            site_passwd = site['database']['database_passwd']

            write_log(site_database)
            dump_database = 'mysqldump' ' -h' + site_ip + ' -u' + site_user + ' -p' + site_passwd + ' ' + site_database + ' > ' + working_dir + '/' + site_name + '-' + str(today) + '.sql'

            os.system(dump_database)
            sql_file = site_name + '-' + str(today) + '.sql'
            connect_s3(sql_file)

## Backup all sites from a given json file (we hope)
def cloudsite_backupall(sites_list):

    for site in sites_list['sites']:
        site_name = site['site_name']

        if re.search( 'not backup', site['comment'] ):
            print "Do not backup database for: ", site_name
        else:
            site_database = site['database']['database_name']
            site_user = site['database']['database_user']
            site_ip = site['database']['database_ip']
            site_passwd = site['database']['database_passwd']

            write_log(site_database)
            dump_database = 'mysqldump' ' -h' + site_ip + ' -u' + site_user + ' -p' + site_passwd + ' ' + site_database + ' > ' + working_dir + '/' + site_name + '-' + str(today) + '.sql'

            os.system(dump_database)
            sql_file = site_name + '-' + str(today) + '.sql'
            connect_s3(sql_file)

def usage():
	print "Error in usage: \n\
	%s </path/to/json_file> <name_of_site> " % sys.argv[0]


## This is the main function, maybe call it 'main' would be a better idea
def validate_input(argv):
    global sites_list
    ## global site_to_backup

    opts, args = getopt.getopt(argv, "hj:s:")

    if (args or args == '-h'):
        usage()
        exit(1)

    for opt, arg in opts:
        if (opt == '-j'):
            json_file = arg
        if (opt == '-s'):
            site_to_backup = arg

    try:
        json_data = open(json_file)
    except:
        print "File not found"
        usage()
        exit(1)
    else:
        sites_list = json.load(json_data)

    try:
        site_to_backup
    except:
        print "Backup all sites defined in the json file"
        cloudsite_backupall(sites_list)
    else:
        print "Create backup for the site: ", site_to_backup
        cloudsite_backup(sites_list, site_to_backup)

    json_data.close()


validate_input(sys.argv[1:])
