CREATE USER  demouser WITH LOGIN; 
GRANT rds_iam TO demouser;
CREATE TABLE invoices (
    DATE date,
    DESCRIPTION varchar(255),
    RATE decimal(4,2),
    HOURS decimal(3,2),
    AMOUNT decimal(5,2)
);
GRANT ALL PRIVILEGES ON TABLE invoices TO demouser;