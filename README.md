# PY_SF_SetupAuditLog
A simple pythin script to pull SF Setup Audit logs into CVS and JSON dump

Configure Connected App [todo write the how to]


Complete required filds in the audit_log_viewer.cnf MUST BE IN THE SAME DIRECTORY AS THE audit_log_viewer.cnf file
    server_url: https://....cs32.my.salesforce.com
    grant_type: password
    client_id: 
    client_secret: 
    username: 
    password: 


[Important]
The lastRunDate file is needed as it is used to fetch audit logs > greater than that date. If you do not see that file. You can create one named lastRunDate, which is a basic text file with no extension must contain a date in this format 2019-11-18T09:35:55-06:00

If you do not, the program will create one for you with the current date/time. You may want to change the date and rerun.

A CVS and JSON file is created each run with a distinct current time stamp. 

Troubleshooting

TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
check that the audit_log_viewer.cnf is there and Complete


to run:
python audit_log_viewer
