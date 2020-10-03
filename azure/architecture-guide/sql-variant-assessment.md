#### Version



| Version | Supported          |
| ------- | ------------------ |
| 1.0     | SQL-MI as recommendation based on sample questionnaire |
|         | Pricing sample based on 200+ GB memory requirement. Basic Important metrics are considered |


### Overview
 
The intent of this document is to guide in making a decision on which SQL server variant in Azure Cloud should be chosen for a business use case where on-premise transactional database like SQL or Oracle are in use and it is required to migrate the on-premise database to a SQL server in Azure.
 
The available options in Azure cloud for SQL variants are as follows:<br />
* SQL Server on Azure VM
* Azure SQL Database 
* Azure SQL Managed Instance
 
### Technology Requirements
 
Say the technology requirements are :<br />
* SQL Server to be hosted in Azure Cloud
* OS Type: Windows Server 2016+
* Database disk size: 4+ TB
* Consistent type of SQL server on non-prod and prod environments
* Support most of the existing database features
 
### Business Requirements 
 
The main business objectives are generally as follows:
* Chosen Azure SQL variant should be Cost effective 
 
### Decision: 
Based on sample real-use case technical and costs considerations, Azure SQL Managed Instance is the appropriate fit here. The key drivers that led to this 
recommendation are in follow-up sections. 
 
### Key Drivers
 
Azure SQL-DB is assessed to be not a suitable option mainly due to below reasons:<br />
a)Required database size is 4TB+. Azure SQL DB supports max 4TB in General purpose and Business Critical tiers, hence this option is not viable. 
The Hyperscale option supports up to 100 TB however the features and high costs are not viable for XChange DB requirements. <br />
b) Partitioning is a likely future requirement which is not supported by SQL-DB. <br />
 
The remaining options i.e. SQL-MI and SQL Server are assessed based on the below technical features and price comparison.
 
#### Feature Parity between SQL-VM and SQL-MI
The answers to below questions are sample answers based on a real scenario. If the answers change, then the final recommendation is subject to change

| No. |Feature Assessment Questions|Feature Availability|Sample Answers| Derived Choice|
| ----|--------------------- |----------------------|-----------------|---------------|
| 1   | Is DB size > up to 4 TB ?|SQL-DB supports only up to 4TB|Yes, ~3 TB|SQL-MI|
| 2   | Is DB size >  up to 8TB ?|SQL-MI supports only up to 8TB|No|SQL-MI|
| 3   | Is there any CDC<br/>requirement?|In SQL-Server only |No|SQL-MI|
| 4   | Does Semantic Search<br/>need to be supported? |Windows Auth is in SQL-Server only|No|SQL-MI|
| 5   | Is it Windows or SQL<br/>authentication? |Windows Auth is in SQL-Server only|Windows|SQL-MI| 
| 6   | Are file streams/ filetable s<br/>needed? |In SQL-Server only|No|SQL-MI|
| 8   | Are Distributed Transactions used? |Distributed Txs are SQL-Server only |No|SQL-MI|
| 9   | [SP, Trigger Fns](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#stored-procedures-functions-and-triggers) - Is any of<br/>these needed? |Limited in SQL-MI |No|SQL-MI|
| 10  | [Linked Server](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#linked-servers) - If needed, Does supported targets suffice?<br/>This is equivalent to "Heterogeneous Connectivity" in Oracle|Limited in SQL-MI|From Supported Targets|SQL-MI|
| 11  | Are there any cross database queries?|In SQL-Server and SQL-MI<br/>.Not supported in SQL-DB|Yes|SQL-MI|
| 12. | Is there a CLR integration to be done?|In SQL-Server and SQL-MI|None|SQL-MI|
| 13. | What kind of partitioning is applied in<br/>the existing database? Is it a distributed /horizontal partitioning?|Not yet but required in future|SQL-MI|
| 14. | Is there a time zone configuration<br/>required?|Time zone can be done only in SQL-Server and SQL-MI|Yes,EST|SQL-MI|
| 15. | Is EKM(Extensible Key management with<br/>AKV required)? for TDE|In SQL-Server,SQL-MI and SQL-DB|Yes|SQL-MI|
| 16. | Is EKM(Extensible Key management with<br/>AKV required)?<br/>for Column Level Encryption at server side|In SQL-Server only|Yes|SQ-Server or choose [Always Encrypted(client side)](https://docs.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine?view=sql-server-ver15)|

#### Size/Configuration of Source DB in Production
| No. |Pricing assessment questions|Sample Answers|
------|----------------------------|--------------|
| 1.  |Sizing - Core|8 cores|
| 2.  |Sizing - Memory|~32 GB used|
| 3.  |Throughput requirements at peak times? Is less than 750 MB/s?|Yes - 1 MB/s|
| 4.  |IOPs requirements at peak times in Prod? Is less than 6000?|Yes - 3000|
| 5.  |SQL server Required on OS|Windows Latest version|


#### Pricing - Azure Estimate
|Service type|Region|Description|Estimated monthly cost|
-------------|------|-----------|----------------------|
|Azure SQL-MI|East US|Managed Instance, General Purpose Tier, 5 GB Retention,<br/>Instance Pool, 1 64 vCore instance(s) x 730 Hours, 4398 GB Storage|$1,973.43|
|Virtual Machines|East US|1 D64as v4 (8 vCPU(s), 256 GB RAM) x 730 Hours; Windows-SQL Server; Pay as you go;<br/>1 managed OS disks – E50, 4096 GiB, 100 transaction units, SQL Enterprise License (US$1,095.00). (Standard is $292).e|$3,046.36|

SQL-Server is considerably higher the Azure SQL-MI option. This is another important reason to account while choosing the Azure SQL variant. 

#### Microsoft References:
1. [Difference between SQL server on VM and Azure SQL-MI](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server)
2. [Size Limits of Azure SQL DB and Azure SQL MI](https://docs.microsoft.com/en-us/azure/azure-sql/database/service-tiers-vcore?tabs=azure-portal)
3. [Disk Types](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/disks-types)
4. [SP, Trigger Functions](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#stored-procedures-functions-and-triggers) 
5. [Linked Server](https://docs.microsoft.com/en-us/azure/azure-sql/managed-instance/transact-sql-tsql-differences-sql-server#linked-servers)
