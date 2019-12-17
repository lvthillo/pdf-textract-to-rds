import json
import boto3
import os
import pg8000
from trp import Document

def getJobResults(jobId):

    pages = []

    textract = boto3.client('textract')
    response = textract.get_document_analysis(JobId=jobId)
    
    pages.append(response)

    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):

        response = textract.get_document_analysis(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages

def convert_row_to_list(row):
    list_of_cells = [cell.text.strip() for cell in row.cells]
    return list_of_cells

def get_connection():
    """
        Method to establish the connection.
    """
    try:
        print ("Connecting to database")
        # Create a low-level client with the service name for rds
        client = boto3.client("rds")
        # Read the environment variables to get DB EndPoint
        DBEndPoint = os.environ.get("DBEndPoint")
        # Read the environment variables to get the Database name
        DatabaseName = os.environ.get("DatabaseName")
        # Read the environment variables to get the Database username which has access to database.
        DBUserName = os.environ.get("DBUserName")
        # Generates an auth token used to connect to a db with IAM credentials.
        password = client.generate_db_auth_token(
            DBHostname=DBEndPoint, Port=5432, DBUsername=DBUserName
        )
        # Establishes the connection with the server using the token generated as password
        conn = pg8000.connect(
            host=DBEndPoint,
            user=DBUserName,
            database=DatabaseName,
            password=password,
            ssl={"sslmode": "verify-full", "sslrootcert": "rds-ca-2015-root.pem"},
        )
        print ("Succesful connection!")
        return conn
    except Exception as e:
        print ("While connecting failed due to :{0}".format(str(e)))
        return None

def write_dict_to_db(mydict, connection):
    #check if connected
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(mydict))
    columns = ', '.join(mydict.keys())
    # fix hardcoded db
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('invoices', columns, placeholders)
    print(sql, mydict.values())
    cursor.execute(sql, list(mydict.values()))
    connection.commit()
    cursor.close()

def lambda_handler(event, context):
    notificationMessage = json.loads(json.dumps(event))['Records'][0]['Sns']['Message']
    
    pdfTextExtractionStatus = json.loads(notificationMessage)['Status']
    pdfTextExtractionJobTag = json.loads(notificationMessage)['JobTag']
    pdfTextExtractionJobId = json.loads(notificationMessage)['JobId']
    
    print(pdfTextExtractionJobTag + ' : ' + pdfTextExtractionStatus)
    
    if(pdfTextExtractionStatus == 'SUCCEEDED'):
        response = getJobResults(pdfTextExtractionJobId)
        doc = Document(response)

    all_values = []

    for page in doc.pages:
        for table in page.tables:
            for i, row in enumerate(table.rows):
                if i == 0:
                    keys = convert_row_to_list(table.rows[0])
                else:
                    values = convert_row_to_list(row)
                    all_values.append(dict(zip(keys, values)))

    connection = get_connection()       
    for dictionary in all_values:
        write_dict_to_db(dictionary, connection)