Python scripts
==

== open_session
- The script open_session.py returns a session using Multi Factor Authentication. The function accepts 2 parameters a profile (as defined on the aws credentials file) and the MFA token.
- For this to work all you need is to define a list of mfa devices per account/profile in the file mfa.json and the credentials for each profile on the file aws.py. The function uses the credentials from this file, so there is no need to have an aws credentials file of credentials defined as environment variables.

== mysql-backups
- The script mysql-backups.py reads the file ".json" and backups all the databases configured on this file.
- It can accept the database name as an argument to the script or it can create a dump of all the entries if no database is specified on the command line.

== rds-monitoring
- The script rds-stats.py collects metrics from AWS CloudWatch and publishes them using the zabbix template zbx_rds_template.xml
- The script must be placed under the "Zabbix external scripts" directory (see Zabbix documentation) and it should be invoqued by the template with the command

-- rds-stats.py[-i,{HOST.HOST},-m,CPUUtilization,-r,{$REGION}]

- For that an item must be created per metric (example above is for CPU Utilization) and a MACRO is defined per Database Instance to set the AWS region: {$REGION} = fra
(fra - for Frankfurt; dub for Dublin, etc)

- The region names and MACROS can be defined on the lines:

if (region == 'fra'):
        aws_region = 'eu-central-1'
        my_account = 'serviced'

(Or even better, a dictionary can be created for this.)

-- Also note the 'my_account' variable must be changed to the corresponding AWS account name
