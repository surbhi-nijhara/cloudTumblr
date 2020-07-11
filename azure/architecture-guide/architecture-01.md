# Overview
The problem statement is to provide a high level architectural view for deploying microservices in Microsoft Azure Cloud Platform. 
The architecture diagram represented is a blueprint with an intent to understand an overall need of different Azure platform services.
 
# Technology Requirements
 
The important technology requirements are :
Azure Cloud Platform with PaaS capabilities
 
# Business Requirements 
The main business objective of the solution is to create a catalogue of the services in Azure cloud platform.
Please see the out-of-scope section
 
# Recommendation of Azure Architecture : 



Key Components:

* Azure API Gateway 
* Azure API Management
* Azure AD 
* Azure Kubernetes Service 
* Azure SQL / CosmosDB
* Azure Monitor, Azure Monitor Logs 
* Azure Redis Cache
* Azure Service Bus
* Azure Blob Storage
* Azure Key Vault
* Azure Express Route
* Azure DNS


# Details:
### Azure API Gateway :
API Gateway will provide a single entry point for all external access to the platform applications. It acts as a reverse proxy and also provides WAF controls and SSL Termination. API Gateway will be deployed in its own subnet inside a custom VNet.

### Azure API Management
APIM will be used to manage publishing of APIs, exposed from microservices, both for external and internal customers/applications. It also is needed for integration with Active directory.
It can also help with IP white listing and rate limiting of the incoming requests. APIM will be deployed in its own subnet inside a custom VNet.
 
External access requests from web client will access API GW
Internal Access: Any request from an on-prem application, like the APIs exposed from service layer(API) to access Azure cache or Azure Service Broker, will route through APIM.
 
 
 
### Ingress Controller
NGinx Ingress controller (or likewise) will enable Kubernetes services to be accessible from the external network.
Kubernetes has a built-in configuration for HTTP load balancing, called Ingress, that defines rules for external connectivity to Kubernetes services. 
An Ingress resource that defines rules, including the URI path, backing service name, and other information will be configured and created. 
The Ingress controller will then automatically program a load balancer to enable Ingress configuration. 

### Azure AD
Active directory will provide OAuth capabilities and act as Azure authorization server for authentication and authorization of the users of hosted microservices.

### Azure Kubernetes Service
AKS will be the managed container platform for deploying containerized microservices.

### AzureSQL / Cosmos 
Azure SQL / Cosmos will be a Azure managed datastore exhibiting enterprise grade scalablibilty and resilieny.

### Azure Monitor, Azure Monitor Logs, Application Insights
Azure Monitor will be used for Monitoring and Logging.  
Application Insights will be used for tracing capabilities.

### Azure Redis Cache
Managed Redis cache can be used for distributed and scalable caching.

Cache can be used for use cases like replicating session information of an user, in case user session is created on-prem in an hybrid architecture. The session information can then be used for validation during authentication in Azure cloud.

### Azure Service Bus
Service bus will serve as a Messaging Broker for event driven business workflows.

Service bus can be used during synchronization/ captuirng data change (CDC)  between on-prem database server and cloud hosted database. 
When the on-premise application will add, update, delete a resource/record in on-premise server, it will also publish an event to Azure Service bus topic. The synch job will be subscribed to the same topic for receiving and handling the event.

# Azure Blob Storage
Blob storage will provide us with storage of Blob.
Blob storage can be used to store documents, file objects, media objects, etc..

### Azure Key Vault
Key vault will be used for storing encryption keys.

Key vault will store CMK and data keys to be used for encryption of fields at client side as well as encryption of data at server side.

### Azure Express Route
Express route will be used for dedicated private connection between Azure cloud and  on-premise environment via ISP.
The microservices in the cloud can access on-premise database server with its internal/private IP. 
 
### Azure DNS
Azure DNS will be used for hosting services for DNS domains that provide name resolution by using Azure infrastructure. 
DNS records will be managed by using the same credentials, APIs, tools, and billing as other Azure services.

### Azure Repos and Devops Pipelines
Alternatively Github/Bitbucket repo with Jenkins can also be hosted in Azure.
Jenkins tool as a CICD orchestrator can be used for the microservices pipeline. 

### Azure Resource Manager with Terraform for IaC (Deployment Automation) 


##### Notes:
Management subnet with management/ bastion instance is not shown in diagram however will be needed.


