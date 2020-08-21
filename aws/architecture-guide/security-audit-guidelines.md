## Security Audit Recommendations
This section provides recommendations on the measures to be taken for auditing the security controls and the procedures to be in place to respond to a security incident if it occurs.
To audit and detect the security violations, a robust logging, monitoring and alert mechanisms should be configured leveraging a multitude of managed and proven capabilities available in Amazon cloud platform. These services will provide detective controls which will help to notify for appropriate responses to the incidents.
 
### Detective Security Controls
Capture Logs: Ensure **Amazon CloudWatch**, the managed and scalable monitoring solution captures all the logs and are visible in AWS Console.

#### Audit AWS resource changes:
Configure **Amazon Config** for recording any configuration changes to the AWS resources and setup rules to evaluate if the changes are as per the guidelines, compliances or required best practices. It serves as a compliance framework for resource configurations across AWS accounts. Amazon config reports the changes to the resources with detailed snapshots. <br>
It is further recommended to integrate **AWS Config with Cloudwatch** to notify any deviation of the set rules.

#### Audit User Activity: 
**Amazon CloudTrail** is a governance tool enabling compliance, operational and risk auditing of the AWS account. While **AWS config** reports the changes done on the AWS resources, Cloudtrail helps identify the events, API calls that led to those changes. Identity of the caller, the time of the API call, the request parameters, and the response elements are reported as part of the activity results.<br>
Cloud trail is enabled by default and the trails are visible in console and stored in S3. The access to Cloud trail console and S3 should be restricted only be provided to the auditing team.
**AWS Cloud Trail** should be enabled in each account and each supported region. Setup CloudWatch events and alarms to act when security anomalies are detected.

#### Monitor AWS accounts: 
Configure **Amazon GuardDuty** which is a smart threat detection service that will enable continuous monitoring for malicious activity and unauthorized behavior to protect the configured AWS accounts and workloads. Guard Duty analyzes VPC Flow logs, CloudTrail logs and DNS logs. Amazon GuardDuty provides alerts via Amazon CloudWatch so that an action can be taken when required. The alert can be through an email for a human action however preferably an automated response should be set up, for example, by leveraging Amazon Lambda.

### Responsive Controls to Security Incidents
#### Preparation:<br>
* **Create staff**: Identify and train a team of SREs (site reliability engineers) to handle and respond to the security incidents. 
 
* **Build Runbooks and Response Plans**: Create runbooks and governance plans to include common scenarios and the resolutions or mitigation solutions. This will improve the response time to the incident.
Escalation mechanism should be clearly defined including both internal and external stakeholders. 
 
* **Automate containment**: Automating containment capability will reduce exposure from the vulnerabilities by automatically implementing temporary (or permanent) compensating controls via security groups and network ACLs. This in turn will enable applying remediations compensating controls more expediently.
 
#### On Detection
* **Severity Classification**: On receiving the notifications or alerts, captured logs, trails and audit snapshots should be assessed and the incident should be classified for a severity level. Amazon support should be contacted depending on the severity.
* **Containment**: Enable containment via the pre-identified tool like AWS CLI and stash the current security group to isolate the identified host using restrictive ingress and egress security group rules.
* **Investigation**: After containment, investigate the threat, correlation, and the required response time. It should be ensured to restore the security group.
* **Follow-up**: Cross-validate with Amazon Support, and report findings and response actions. 
