#### Pre-requistes 
1. Windows 10 
2. Install Ubuntu 18.04 LTS from [Microsoft](https://www.microsoft.com/en-in/p/ubuntu-1804-lts/9n9tngvndl3q?rtc=1&activetab=pivot:overviewtab) store
3. AWS Access and Secret key

#### How to Setup:
4. Download the script - glue-local-dev-setup.sh and execute. 
5. A file glue-vars.sh will be generated in the same directory from where glue-local-dev-setup.sh is execute.
6. Run source glue-vars.sh
7. Create a sample python script
8. Run aws-glue-libs/bin/gluesparksubmit <some-sript.py> --JOB_NAME <some-job-name>  


