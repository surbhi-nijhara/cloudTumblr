The purpose of this blog is to demonstrate 
a) how to join EC2 launched in an Autoscaling group automatically into an existing AD(Active Directory.).
b) Further to above, if an EC2 within ASG gets terminated, then the EC2 hostname added as AD(Active Directory) object should be removed from Active Directory.

### Join Approach:
The approach is to use AWS SSM.
1. Follow [this](https://aws.amazon.com/blogs/security/how-to-configure-your-ec2-instances-to-automatically-join-a-microsoft-active-directory-domain/) document.
2. Prerequistes:<br/>
   a) Create a AWS directory. <br/>
   b) Create an EC2 from an AWS provided Windows Server Image.<br/> 
      While creating the instance provide the directory information in EC2 launch wizard. 
   c) On the created Ec2 instance -<br/>
   Add Roles 
   AD - This will enable to use Active Directory Users and Computers. <br/>
   We can also see the OU=glad and under the same use Users and Computers.<br/>
 
   d) Also change the Administrator password.<br/>
   e) Just disconnect and check if you can log into the Ec2 using<br/>
       i) User Administrator and new changed password.<br/>
      ii) User AD domain and its password.<br/>
   f) Use EC2Launch v2.<br/>
      i) Ensure is unchecked.<br/>
     ii) Password - Specify<br/>
    iii) Do a Shutdown with SysPrep using EC2Launch Settings.<br/>
         After shutting down with sysprep, the EC2 instance as expected cannot be accessed using AD credentials. <br/>
      

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
  



4. Schedule Task:

[TBD]

[Reference](https://aws.amazon.com/blogs/security/how-to-configure-your-ec2-instances-to-automatically-join-a-microsoft-active-directory-domain/)
http://thesysadminswatercooler.blogspot.com/2016/01/aws-using-sqs-to-cleanup-active.html
