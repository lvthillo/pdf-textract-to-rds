# PDF Textract to RDS
This demo project will deploy a Textract Demo Project. Textract will read a multipage invoice PDF from S3 and write the data to an RDS Postgres database. This makes PDF data queryable in SQL.

![draw](https://user-images.githubusercontent.com/14105387/71366582-a7e5b400-25a2-11ea-9f77-bbcfc7acf9ed.png)


### Steps to deploy the demo project

1) Deploy RDS Postgres database.
```
$ aws cloudformation create-stack --stack-name db --template-body file://db/postgres.yml --parameters ParameterKey=Username,ParameterValue=lvthillo ParameterKey=Password,ParameterValue=notsupersecret
```

2) Execute initial SQL script to create table and demo-user. Replace the connection URL.
```
$ psql -h xxx.xxx.rds.amazonaws.com -p 5432 -U lvthillo -d InvoiceDB  -W -a -f db/setup.sql
```

3) Deploy SAM stack. Replace with your bucket.
```
$ sam build
$ sam deploy --template-file .aws-sam/build/template.yaml --parameter-overrides DemoUser=demouser TableName=invoices --stack-name textract --capabilities CAPABILITY_IAM --s3-bucket demo-lvthillo-bucket
```

More details can be found [here](https://medium.com/@lvthillo/write-pdf-data-to-a-relational-database-using-amazon-textract-3b0e6bc3a390?sk=25c02c34e16f401f608d0e6ebb2b9673).
