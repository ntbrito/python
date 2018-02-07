#!/usr/bin/env python

import json
import os
import boto3
import aws


CWD = os.path.dirname(os.path.abspath(__file__))

def create_session(profile, token):

    myprofile = profile
    mytoken = token

    mfa_file = os.path.join(CWD, "mfa.json")
    mfa_data = open(mfa_file)
    mfa = json.load(mfa_data)
    snumber = mfa['mfadevice'][myprofile]

    tempsession = boto3.Session(
        aws_access_key_id=aws.AWS[myprofile]['aws_access_key_id'],
        aws_secret_access_key=aws.AWS[myprofile]['aws_secret_access_key'],
        profile_name=myprofile
    )

    sts = tempsession.client('sts')

    validation = sts.get_session_token(
        SerialNumber=snumber,
        TokenCode=mytoken,
    )

    session = boto3.Session(
        aws_access_key_id=validation['Credentials']['AccessKeyId'],
        aws_secret_access_key=validation['Credentials']['SecretAccessKey'],
        aws_session_token=validation['Credentials']['SessionToken']
    )

    return (session)
