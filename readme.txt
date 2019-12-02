Complete required filds in the audit_log_viewer.cnf MUST BE IN THE SAME DIRECTORY AS THE audit_log_viewer.cnf file
    server_url: https://fsa--FPACDev43.cs32.my.salesforce.com
    grant_type: password
    client_id: 
    client_secret: 
    username: 
    password: 


The lastRunDate file is needed as it is used to fetch audit logs > greater than that date. If you do not see that file. You can create one
basic text editor with no extension must contain a date in this format 2019-11-18T09:35:55-06:00

If you do not, the program will create one for you with the current date/time. You may want to change the date and rerun.

filename=lastRunDate 

A CVS and JSON file is created each run with a distinct current time stamp. 


Troubleshooting
this
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
check that the audit_log_viewer.cnf is there and Complete


to run:
python audit_log_viewer

