#!/bin/env python 
import datetime
import sys
import os
import boto3

working_dir = os.path.dirname(os.path.abspath(__file__))
## working_dir = os.getcwd()


## Connect to cloudwatch
def cloudwatch_connect(region):
    import json

    my_region = region

    cred_file = working_dir+'/credentials.json'
    json_data = open(cred_file)
    accounts = json.load(json_data)

    if (region == 'fra'):
        aws_region = 'eu-central-1'
        my_account = 'serviced'

    if (region == 'dub'):
        aws_region = 'eu-west-1'
        my_account = 'serviced'

    if (region == 'nva'):
        aws_region = 'us-east-1'
        my_account = 'serviced'

    if (region == 'lon'):
        aws_region = 'eu-west-2'
        my_account = 'serviced'

    if (region == 'int'):
        aws_region = 'eu-west-1'
        my_account = 'internal'


    ## Info on the bucket from the json file
    access_key = accounts['account'][my_account]['aws_access_key']
    secret_key = accounts['account'][my_account]['aws_secret_key']


    ## Connect to CloudWatch
    connection = boto3.client('cloudwatch',
                           region_name = aws_region,
                           aws_access_key_id = access_key,
                           aws_secret_access_key = secret_key
                           )

    return (connection)

def collect_metric(metric, db_instanceid, region):
    my_metric = metric
    my_dbinstance = db_instanceid
    my_region = region

    session = cloudwatch_connect(my_region)

    validmetrics = ["CPUUtilization", "ReadLatency", "WriteLatency", "DatabaseConnections", "FreeStorageSpace"]

    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=4)

    ## Validate metric
    if my_metric not in validmetrics:
        print "Metric %s not supported! \n" % my_metric
        exit(1)

    response = session.get_metric_statistics(
                            Namespace = 'AWS/RDS',
                            MetricName = my_metric,
                            Dimensions = [{ 'Name': 'DBInstanceIdentifier', 'Value': my_dbinstance }],
                            StartTime = start,
                            EndTime = end,
                            Period = 60,
                            Statistics = ['Average']
                            )

    if ( response['ResponseMetadata']['HTTPStatusCode'] == 200 ):
        ## print "%s \n" % response
        ## metric_unit = response['Datapoints'][0]['Unit']

        my_result = response['Datapoints'][0]['Average']

        if (my_metric == 'FreeStorageSpace') or (my_metric == 'DatabaseConnections'):
            ## my_result = my_result / 1024 ** 2
            my_result = int(my_result)

        print "%s" % my_result


def main():
    from optparse import OptionParser

    ### Arguments
    parser = OptionParser()
    parser.add_option("-i", "--instance-id", dest="instance_id",
                help="DBInstanceIdentifier")
    parser.add_option("-m", "--metric", dest="metric",
                help="RDS cloudwatch metric")
    parser.add_option("-r", "--region", dest="region",
                help="AWS region [dub | lon | fra | nva | int]")

    (options, args) = parser.parse_args()

    ## Verify args
    if (options.instance_id == None):
        parser.error("-i DBInstanceIdentifier is required")
    if (options.metric == None):
        parser.error("-m RDS cloudwatch metric is required")
    if (options.region == None):
        parser.error("-r AWS region is required")

    db_instanceid = options.instance_id
    metric = options.metric
    region = options.region


    ## cloudwatch_connect(account)
    collect_metric(metric, db_instanceid, region)


if __name__ == '__main__':
    sys.exit(main())
