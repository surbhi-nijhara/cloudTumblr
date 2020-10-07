# CICD for Migration from Oracle to SQL


![\[Migration Architecture Diagram\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/sql-migration-arch.png?raw=true)
				
        					Migration Architecture Diagram

## Scope
The scope of DevOps for end to end migration of Oracle to SQL is to address schema, code and ADF pipeline configuration change management and strategize deployment pipelines for QA and Stage Environment.

Azure DevOps server or service be used for code change and release. The strategy and steps to effectively release the code and migrate to the oracle data is scoped to below migration entities.

* Source: Oracle DB instance hosted in on-premise environment.
* Destination: SQL Managed Instance hosted in Azure cloud.
* Migration is planned to be executed in an offline mode. 


## Environment Prerequisites:
Following is a list of the required instances to be provisioned in Azure environment.<br />
SQL Managed Instance in Azure:
* SQL MI DEV-01 :  For development of SQL DB schema and code
* SQL MI DEV-02 : For development of SQL DB code
* SQL MI DEV-03 :  For development of SQL DB schema and code<br>
    *These instances can be configured in a pool and each database will be of lesser configuration and need not be the same as SQL MI Prod instance.<br>*
    *SQL Managed instance pool for Dev<br>*
    *For example following SQL Dev size can be used.<br>*
    *SQL Managed Instance pool of 16 cores:<br>*
        *   *The pool is intended to have 3 instances split as 8 core (ADF Pipeline),<br />*
        *   **4 core (Schema Conversion),<br>*
        *   4 core (Code Conversion).  <br>*    
     *Disk Size : Standard HDD of size can be equal to Oracle Stage DB size.*

* SQL MI QA: For quality assurance of incremental migrated code and data. <br>
*This instance will be required to match the Oracle database disk size, core and memory.<br />*
*If CPU, RAM metrics are available for peak workloads, the sizing will be done accordingly. The data is awaited from RegEd.*

* SQL MI STAGE / UAT/ Prod : For end-end quality assurance of migrated code and data.<br />
This instance will be required to be of the same configuration as SQL MI QA  instance.

**Data Factory in Azure cloud:**
* ADF DEV
* ADF QA
* ADF STAGE/ UAT/Prod

**Devops Service:**
Azure Devops Server in on-premise or Azure Devops Service in Cloud.<br />
Shared Self Hosted Integration runtime in Windows instance RegEd’s on-premise.


## Code Structure
### Code Structure of SQL schema
SQL objects repository is Azure Repos Git. The repository will store SQL schema and code.

![\[SQL-Objects-Collapsed-Folders\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/SQL-Objects-Folders.png?raw=true)	
	
		SQL Objects folders - Collapsed and Expanded View(dbo.Views)

### Code Structure of ADF 
ADF entities repository is Azure Repos Git. Another repository will store ADF pipeline configuration as ARM templates. 


![\[ADF-Templates-Folders\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/ADF-folders.png?raw=true)
	
		Sample ADF folders and templates

## Change management of SQL DB schema and code
A continuous integration mechanism to deploy SQL schema including code using Azure Pipeline can be put in place. Continuous integration practice is used by the development team to simplify the building and testing of code. This helps to catch problems early in the development cycle, which makes them easier and faster to fix. 

![\[Change Mgmnt SQL Diagram\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/change-mgmnt-sql.png?raw=true)
				 
				 Oracle objects converted to SQL Objects (Schema and Code) ; Version control in Azure ReposGit 

i.Developer converts Oracle schema and Code to SQL schema and code using SSMA tool and manually. The sql schema and code are manually validated by publishing them ii.in Azure SQL MI instances provisioned in the DEV environment.<br>
iii.Developer creates a local SQL Database project on VS2019 ( if not already created) and syncs the SQL DEV changes into the local project. A DACPAC file is also generated using VS.<br>
iv.Developer commits the synced changes from local project to a cloned git Oracle2SQL repository branch. As a standard followed practice, the developer creates a development branch from the master branch of repository.<br>
v.A PR is created on master branch from Development Branch, Review and Merge PR into master branch of repository.<br>

*_Artifact_*: Tagged DACPAC file will be the artifact used to deploy schema and code.

## Change management of ADF configuration

A continuous integration mechanism to publish ARM templates to ADF resources using ADF UX Pipeline can be put in place. 
A separate data factory per environment is recoomended to be created. A Development Dev ADF integrated with Azure DevOps Git repository will be required. Here developers can author ADF entities like pipelines, datasets, and more. ADF pipeline execution for data migration will happen on SQL MI DEV. 

![\[Change Mgmnt ADF Diagram\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/change-mgmnt-adf.png?raw=true)

i.Developer creates ADF entities making use of a stable DB code build artifact. S/He can debug changes and perform test runs.<br>
ii.Developer creates a PR from the feature branch to master branch, get reviewed and merged into master branch.<br>
iii.Merged changes are published to DEV ADF using ADF UX - Publish button.<br>
*_Artifact_*: Tagged ARM templates will be the artifact used to deploy ADF configuration as code.


## Deploy Pipelines in QA
Schema, code, and ADF pipeline configuration will be deployed and certified in QA environment. The following pipelines, as needed,  are recommended to be executed in a QA environment. <br>
**Pipeline 01:** Schema/Code Deployment, from master branch, to SQL MI through the latest tagged DACPAC file. SQLPackage.exe will be used to publish the DACPAC.<br>
**Pipeline 02:** ADF code deployment from master branch, represented via ARM templates.ARM templates will be deployed with QA specific environment parameter files to QA.<br>
**Pipeline 03:** Data migration via Trigger of ADF pipelines in ADF UX. This will effectively lead to migration of all tables from Oracle to SQL. See more details in section Data Migration.<br>

![\[Pipelines Diagram\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/master/azure/diag_source/azure-db-deploy-pipelines.png?raw=true)

				  Pipelines to setup and execute data migration on QA 

QA enviornment can be used when schema conversion from Oracle copy is completed as well as data migration pipelines are ready.  As code conversion is incrementally ready, DACPAC will start including the  converted code definitions as well.
The release of the sprint N-1 (tentatively) can be targeted to be certified for promotion to Stage environment.

### Data Migration
Data Migration will be executed end-end in QA environment. 
Prerequisite: data migration will require pre-creation of below components in QA environment.
Provisioned SQL MI QA instance
Provisioned QA ADF, shared data gateway (Self Hosted Integration Runtime) to Source Oracle Stage DB.
Tagged SQL Schema release published to SQL-MI QA.
ARM templates published to QA ADF. 

#### Process for Data Migration
Drop constraints and indexes.
Trigger ADF Pipelines.
Recreates constraints and indexes.
Monitor at regular intervals. Rerun if required.
Run Sanity tests of successfully migrated data 

## Deploy Pipelines in STAGE / UAT / PROD
Deploy pipelines, similar to the pipelines created for QA environments, will be created for stage environments. The pipelines will specify the exact stable tagged artifacts for both **DACPAC** and **ARM templates**. When the stage release is successful, same artifact versions will be ready to be promoted and released for the Production environment.<br>
The stage in the release pipeline can be configured with **pre-deployment approval** for the deployment. The stage in the release pipeline can also be configured with **post-deployment gates** (like querying monitoring metrics) and **approval**for the approximate time limit required for data migration.




