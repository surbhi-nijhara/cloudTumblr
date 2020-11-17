
The purpose of this blog is to demonstrate <br />
* How to create a Windows Custom AMI for launching successfully in an ASG. <br />
* How to join EC2 launched in an Autoscaling group automatically into an existing AD(Active Directory).<br />
* Further to above, if an EC2 within ASG gets terminated, then the EC2 hostname added as AD(Active Directory) object should be removed from Active Directory.

On successul execution following is achieved: 
- New EC2 instance in ASG becomes part of the AD domain. A new hostname is added as AD Object.
- AWS SSM document retrieves the new EC2 association successfully.
- New instance in EC2 ASG gets a new hostname. 
- New instance can be accessed using the specified password as well as AD creds.
- If the instance in ASG is  terminated, the Hostname entry also gets removes from AD.

Let us first create a custom Windows AMI <br />
We will then see how to achieve this in two parts - Join EC2 with AD and Remove EC2 from AD.


### Custom Windows AMI Approach:
We will use 2 EC2 Instances outside Autoscaling Groups
1) This will be our EC2 instance created from an AWS/Base Custom Image. This will be futher custom configured or ensured if the required configuration for launching the EC2 in an AD domain is present. Let us tag this EC2 instance as **inst-golden**.
inst-original will be also used to test the goal of the PoC i.e. joining and removing the EC2, launched in ASG, in AD domain.<br />
2) Second EC2 instance, lets tag it as **inst-custom** and will be created from the image of the inst-original. This is essentially a clone of inst-original but will be sysprepped. After sysprepped, it will lose some of the configurations done in inst-original, like this instance will not be in the AD domain.

##### Steps:
   a) Create a AWS directory. Note the AD account details. An example of created directory for this blog is as follows.<br />
      ![\[Snapshot for 04-example-directoryservice:\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/ec2-windows-ad-join/aws/diag_source/04-example-directoryservice.png?raw=true)
   b) Launch an EC2 from an AWS/Base Custom Image and tag as **inst-golden**<br/> 
       - While creating the instance provide the above directory information in EC2 launch wizard.<br />
       The first time you specify a domain in the EC2 launch wizard, the wizard generates the domain’s default SSM document. <br />
       - The role to be applied needs to includes the policy **AmazonEC2RoleforSSM-ASGDomainJoin** and is created as per the details in [this]         
       (https://aws.amazon.com/blogs/security/how-to-configure-your-ec2-instances-to-automatically-join-a-microsoft-active-directory-domain/) document. Refer part 
       2 / Step 1: Create a new IAM policy, copying the AmazonEC2RoleforSSM policy. <br />
       ![\[Snapshot for 06-example-Ec2-domainjoindirectory:\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/ec2-windows-ad-join/aws/diag_source/06-example-Ec2-domainjoindirectory.png?raw=true)
   c) Remote Login into the launched Ec2 instance **inst-golden** using the RDP credentials.<br />
   d) Using 'Server Manager', select add Roles and Features, select Role-based or feature-based installation, and add following roles:<br />
      - AD Domain Services. This will enable to access Active Directory Users and Computers. <br />
   e) Change the Administrator password under User Accounts.<br/>
   f) Just Disconnect and verify if you can log into the Ec2 using below accounts<br/>
       i) Administrator and the new changed password.<br/>
      ii) AD account.<br/>
   g) When logged in with AD login, you will be able to access Active Directory Users and Computers and see OU=**glad** and under it Users and Computers.<br/>
      Under Computers, you will be able to see the hostname of **inst-golden**. <br/>
      ![\[Snapshot for 07-example-windows-ad:\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/ec2-windows-ad-join/aws/diag_source/07-example-windows-ad.png?raw=true)
   f) Login back with Administrator account<br />
   g) Ensure SSM is installed in the instance. <br />
   h) Ensure the policy: **AmazonSSMDirectoryServiceAccess** for SSM to communicate with AD, is added to the EC2 IAM role. 
      Complete steps can be seen [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-instance-profile.html)
   i) Run the following command in Windows Powershell to schedule a Windows Task that will run the User data on next boot:
      ###### Command
       C:\ProgramData\Amazon\EC2-Windows\Launch\Scripts\InitializeInstance.ps1 –Schedule
   j)Install (if not installed) and Open EC2Launch v2.<br />
      ![\[Snapshot for 05-example-EC2LaunchSettings:\]](https://github.com/surbhi-nijhara/cloudTumblr/blob/ec2-windows-ad-join/aws/diag_source/05-example-EC2LaunchSettings.png?raw=true)
      i) Ensure **Set Computer Name** is unchecked.<br /> This will enable to launch EC2 instances with unique host names.<br />
     ii) Administrator Password - Choose **Specify** and provide a password.<br />
    iii) Do a **Shutdown with Sysprep**.<br /> More details are [here](https://aws.amazon.com/premiumsupport/knowledge-center/sysprep-create-install-ec2-windows-amis/)
    After shutting down with sysprep, the EC2 instance as expected cannot be accessed using AD credentials. <br/>
         
   g) Create Image of the above Ec2 instance, say **ami-custom**<br />
   h) We will use this image **ami-custom** in AWS Launch Configuration.<br />
       Optionally, an Ec2 instance can be launched from this image, and after launch you will notice:<br />
       - Able to login with Adminstrator and the specified password.<br />
       - Not able to login using AD login.<br />
       
   
### Join Approach:
We mainly follow the steps in the doucment[here](https://aws.amazon.com/blogs/security/how-to-configure-your-ec2-instances-to-automatically-join-a-microsoft-active-directory-domain/). However, while following this document, below are more details that will help achieve the result faster.

##### Steps:
1. Under launch Configurations, Use **ami-custom**. Fill in the obvious details.
2. Under Advanced, add User data script as below with persist tag. With <persist>true</persist> added, the issue of  EC2 custom AMI not running bootstrap (user-data) can be avoided.
   #### User data script 
       <powershell>
       Set-DefaultAWSRegion -Region us-east-2
       Set-Variable -name instance_id -value (Invoke-Restmethod -uri http://169.254.169.254/latest/meta-data/instance-id)
       New-SSMAssociation -InstanceId $instance_id -Name "awsconfig_Domain_d-9a672bcc48_glad.test.com"
       </powershell>
       <persist>true</persist>
 3. Set Metadata Accessible=Enabled. 
 4. Create and Autoscaling Group from the created Launch Configuration.<br />
    Tag the instances according to your policies or as simple as **autoscale**. The ASG will launch the desired instances.
 5. Verify that the launched instances are joined to the AD.
    - Log into the instance  using
      i) Administrator and the password (specified earlier).<br/>
     ii) AD account.<br/>
    - Use following SSM commands to see that EC2 is successfully associated.
    #### Commands
        aws ssm list-associations --association-filter-list key=Name,value=awsconfig_Domain_d-9a672bcc48_glad.test.com

 
 
### Remove Approach:<br/>

1. Create the SQS queue<br/><br/>
Create a new SQS queue.   We will set the permissions in a later step, after we've created the SNS topic.<br/>
Message retention period should be configured to a value greater than the frequency of the scheduled powershell script.<br/>

2. Create the SNS topic<br/>
Create a new SNS topic and add a subscription to the SNS topic selecting 'Amazon SQS' as the endpoint, ie: arn:aws:sqs:us-east-2:{aws-account-id}:poc-removead<br/>

3. Configure providing permission to SNS to be allowed to send the Ec2 Termination message to SQS queue<br/>
In the SQS queue  created in the prior step and select the 'Access Policy' tab.  Add below policy <br/>
Modify with your SNS ARN and the SQS ARNs.<br/>

   
      {
        "Version": "2012-10-17",
        "Id": "SQSSendMessagePolicy",
        "Statement": [
        { 
          "Sid": "SQS-Access",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "SQS:SendMessage",
          "Resource": "arn:aws:sqs:us-east-2:126127892668:poc-removead",
          "Condition": {
          "ArnEquals": {
            "aws:SourceArn": "arn:aws:sns:us-east-2:126127892668:poc-removead"
          }
        }
      }
     ]
    }
       


4. Configure the notification for the Auto Scaling Group<br/>
Select your Auto Scaling Group and choose the 'Notifications' tab and then 'Create notification'.<br/>
For the notification choose the option 'terminate' and select the SNS topic created earlier.<br/>


5. Configure the IAM role<br/>
The EC2 instance that will be running our Powershell cleanup script  requires permissions to access the SQS queue.  To allow this, configure a security policy for the IAM role that is attached to the instance.  Modify the policy below for the Resource ARN to match your SQS ARN.<br/>

    "SQS-Access": {
        "Version": "2012-10-17",
        "Statement": [
            {
             "Action": [
               sqs:GetQueueAttributes,
               sqs:GetQueueUrl,
               sqs:ReceiveMessage,
               sqs:DeleteMessage
              ],
              "Resource": "arn:aws:sqs:us-east-1:123456789012:SQS-InstanceTerminations",
              "Effect": "Allow"
          }
        ]
    }




Prepare the Ec2 to run Powershell script:<br/>
1. Open Windows Powershell ISE <br/>

2. Set-AWSCredential `<br/>
                 -AccessKey {access-key} `<br/>
                 -SecretKey {secret-key} `<br/>
                 -StoreAs default<br/>
                 
 3. Save and Run below Powershell script<br/>

### Windows Powershell Script:

    #Function that logs a message to a text file
    function LogMessage
    {
        param([string]$Message)
    
       ((Get-Date).ToString() + " - " + $Message) >> $LogFile;
    }
    $LogFile = "C:PSLog.txt"#Full location of the log file

    #Delete log file if it exists
    if(Test-Path $LogFile)
    {
        Remove-Item $LogFile
    }
 
    $Message >> $LogFile;#Write the variable to the log file

    #Get the SQS queue URL
    $queueurl = Get-SQSQueueUrl -queuename poc-removead -QueueOwnerAWSAccountId <account-id> -region us-east-2

    #Get the number of SQS messages in the queue

    $messages = Get-SQSQueueAttribute -QueueUrl $queueurl -AttributeName ApproximateNumberOfMessages -Region us-east-2

    LogMessage -Message "messages:";
    $messages >> $LogFile;
    LogMessage -Message "messageCount:";
    $messageCount = $messages.ApproximateNumberOfMessages
    $messageCount >> $LogFile;

    #Loop through each message to remove the terminated server from Active Directory
    While ($messageCount -gt 0) 
    {
       $messageCount-=1
       $message = Receive-SQSMessage -QueueUrl $queueurl -Region us-east-2
       LogMessage -Message "message:";
       $message >> $LogFile;

       $jsonObj =  $($message.Body) | ConvertFrom-Json
       LogMessage -Message "jsonObj after ConvertFromJson:";
       $jsonObj >> $LogFile;

       $id=$jsonObj.EC2InstanceId
       LogMessage -Message "id after ConvertFromJson:";
       $id >> $LogFile;

       $consoleOutput = Get-EC2ConsoleOutput -InstanceId $id -Region us-east-2
       $bytes = [System.Convert]::FromBase64String($consoleOutput.Output)
       $instanceIds = (Get-EC2Instance -Filter @(@{name="platform";value="windows"})).Instances.InstanceId
       
       #Convert from Base 64 string
       $bytes = [System.Convert]::FromBase64String($consoleOutput.Output)
       $string = [System.Text.Encoding]::UTF8.GetString($bytes)

       #If the string contains RDPCERTIFICATE-SUBJECTNAME, we can extract the hostname
       if($string -match 'RDPCERTIFICATE-SUBJECTNAME: .*') {
            $windowsHostName = $matches[0] -replace 'RDPCERTIFICATE-SUBJECTNAME: '}

       Get-ADComputer -Identity $windowsHostName | Remove-ADObject -Recursive -Confirm:$False
       Remove-SQSMessage -QueueUrl $queueurl -ReceiptHandle $message.ReceiptHandle -region us-east-2 -Force
       LogMessage -Message "Done";
     }
  

 - Use following SSM commands to verify that EC2 hostname is successfully dis-associated.
    #### Commands
        aws ssm list-associations --association-filter-list key=Name,value=awsconfig_Domain_d-9a672bcc48_glad.test.com

4. Schedule Task:

[TBD]

[Reference](https://aws.amazon.com/blogs/security/how-to-configure-your-ec2-instances-to-automatically-join-a-microsoft-active-directory-domain/)
http://thesysadminswatercooler.blogspot.com/2016/01/aws-using-sqs-to-cleanup-active.html



Some Troubleshooting
Hidden files:
https://www.bitdefender.com/consumer/support/answer/1940/#:~:text=Click%20the%20Start%20button%2C%20then%20select%20Control%20Panel.&text=Click%20on%20Appearance%20and%20Personalization.&text=Select%20Folder%20Options%2C%20then%20select%20the%20View%20tab.&text=%E2%80%A2-,Under%20Advanced%20settings%2C%20select%20Show%20hidden%20files%2C%20folders%2C,and%20drives%2C%20then%20click%20Apply.

2. If the Ec2 association is not seen in SSM document, validate all teh required configuration in below article.
https://aws.amazon.com/premiumsupport/knowledge-center/systems-manager-ec2-instance-not-appear/

Password of AMI issue:
https://stackoverflow.com/questions/36496347/unable-to-get-password-for-the-instance-created-from-ami#:~:text=Password%20is%20not%20available.,the%20default%20password%20has%20changed.&text=If%20you%20have%20forgotten%20your,for%20a%20Windows%20Server%20Instance.
   
  ##### 
  
  Create Cusom Windows AMI - https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/Creating_EBSbacked_WinAMI.html#ami-create-standard
  
  #### Useful SSM Commands
        aws ssm delete-document --name awsconfig_Domain_d-9a672bcc48_glad.test.com
        aws ssm create-document --content file://<filename>.json --name awsconfig_Domain_d-9a672bcc48_glad.test.com
        aws ssm get-document --name awsconfig_Domain_d-9a672bcc48_glad.test.com




