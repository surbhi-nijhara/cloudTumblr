#### Version



| Version | Supported          |
| ------- | ------------------ |
| 1.0     | SQL-MI is recommended |
|         | Pricing based on 210+ GB memory requirement. Basic Important metrics are considered|
|         | :white_check_mark: |
|         | Dev Sizing         |



### Overview
 
The problem statement is to make a decision on which SQL server variant in Azure Cloud should be chosen for a business use case where an on-premise transactional database like SQL, Oracle is in use is required to migrate to SQL server in Azure.
 
The available options in Azure cloud for SQL variants are as follows:
SQL Server on Azure VM
Azure SQL Database 
Azure SQL Managed Instance
 
### Technology Requirements
 
The important technology requirements are :<br />
* SQL Server to be hosted in Azure Cloud
* OS Type: Windows Server 2016+
* Database disk size: 4+ TB
* Consistent type of SQL server on non-prod and prod environments
* Partitioning 
 
### Business Requirements 
 
The main business objective of the solution that technology will resolve is as follows:
* Cost effective 
* Required Features effective
 
 
### Recommendation: 
Based on real-use case technical and costs considerations, Azure SQL Managed Instance is the appropriate fit. 
 
### Key Drivers
 
Azure SQL-DB is assessed to be not a suitable option mainly due to below reasons:<br />
a)Required database size is 4TB+. Azure SQL DB supports max 4TB in General purpose and Business Critical tiers, hence this option is not viable. 
The Hyperscale option supports upto 100 TB however the features and high costs are not viable for XChange DB requirements. <br />
b) Partitioning is a likely future requirement which is not supported by SQL-DB. <br />
 
The remaining options i.e. SQL-MI and SQL VM are assessed based on the below technical features and price comparison.
 
 
#### Feature Parity between SQL-VM and SQL-MI
The answers to below questions are sample answers based on a real scenario. If the answers change, then the final recommendation is subject to change.
 
 
 
 
 
#### Pricing
 
SQL-VM is nearly twice the Azure SQL-MI option.
 


###### Notes:
i) Instance Pool and Single Instance show the same price in Azure Price calculator.
Pricing link: https://azure.com/e/fd719f12a8554db3831bba983da6b035
 
ii)The correct sizing of SQL-MI for development, needs more inputs like existing IOPS, latency, etc. which the RegEd team is working on it to provide. 



#### Microsoft References:
1. [Difference between SQL server on VM and Azure SQL-MI](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server)
2. [Size Limits of Azure SQL DB and Azure SQL MI](https://docs.microsoft.com/en-us/azure/azure-sql/database/service-tiers-vcore?tabs=azure-portal)
3. [Disk Types](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types)
4. [SP, Trigger Functions](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#stored-procedures-functions-and-triggers) 
5. [Linked Server](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#linked-servers)
