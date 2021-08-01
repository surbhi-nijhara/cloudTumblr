#!/bin/bash

# Make sure the script is running as root.
#if [ "$UID" -ne "0" ]; then
#	    echo "You must be root to run $0. Try following"
#	    echo "sudo $0"
 #           exit 9
	    
#fi
usage() { echo "Usage: $0 [-a <"AWS_ACCESS_KEY_ID">] [-s <"AWS_SECRET_KEY">]" 1>&2; exit 1; }
# accept AWS access and secret key
while getopts ":a:s:" flag
do
    case "${flag}" in
	a) YOUR_ACCESS_KEY_ID=${OPTARG};;
        s) YOUR_SECRET_ACCESS_KEY=${OPTARG};;
	*) usage ;; 
    esac
done
shift $((OPTIND-1))
if [ -z "${YOUR_ACCESS_KEY_ID}" ] || [ -z "${YOUR_SECRET_ACCESS_KEY}" ]; then
	    usage
fi
echo "Access-Key: $YOUR_ACCESS_KEY_ID";
echo "Secret-Key: $YOUR_SECRET_ACCESS_KEY";


rm glue-vars.sh
touch glue-vars.sh
chmod +x glue-vars.sh;

#install zip
if (which zip | grep "/usr/bin/zip") then
	echo "----> Zip is already installed"
else 
	echo "****** Installing zip *********"
	sudo apt install zip
fi


#install Java
if ( java -version 2>&1 >/dev/null | grep "java version\|openjdk version")  then
	  echo "----> Java installed already"
else
	  echo "----> Java NOT installed!"
	  echo "***** Installing Java *******"
          default_java_dir="/usr/lib/jvm"
          sudo apt update
          sudo apt install openjdk-8-jdk
	  echo $(java -version) 
	  echo "----> Java is installed"
fi 

JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
echo export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64 >> ./glue-vars.sh

#install maven

if ( mvn -v 2>&1 | grep "Apache Maven")  then
	echo "----> Maven installed already"
else	
       echo "----> Maven NOT Installed"
       sudo apt install maven
       echo export MAVEN_CONFIG=/home/.m2 >> ./glue-vars.sh
       echo export M2_HOME=/usr/share/maven >> ./glue-vars.sh
       echo "----> Maven is now Installed"
fi
#set env variables
echo export PATH=~/.local/bin:$JAVA_HOME/bin:/usr/local/bin/python3:$PATH >> ./glue-vars.sh
cd;
rm -rf local-dev-aws
mkdir local-dev-aws;
cd local-dev-aws;
pwd=`pwd`
USER_HOME=$pwd
echo export USER_HOME=$USER_HOME >> ../glue-vars.sh

#download spark lib
if [ -d "$USER_HOME/spark-2.4.3-bin-spark-2.4.3-bin-hadoop2.8" ]; then
   echo "********** SPARK Library is already installed ************"
else
   echo "********** Now Installing SPARK Libray ************"
   wget https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-1.0/spark-2.4.3-bin-hadoop2.8.tgz;
   tar -xvf spark-2.4.3-bin-hadoop2.8.tgz --warning=no-unknown-keyword;
   rm spark-2.4.3-bin-hadoop2.8.tgz;
fi

#download aws-glue-libs
if [ -d "$USER_HOME/aws-glue-libs" ]; then
    echo "******** AWS-GLUE-LIB 1.0 is already installed *********"
else
    echo "******** Now Downloading AWS-GLUE-LIB 1.0 *********"
    curl -L -o glue.zip https://github.com/awslabs/aws-glue-libs/archive/glue-1.0.zip;
    unzip glue.zip;
    mv aws-glue-libs-glue-1.0 aws-glue-libs;
    rm glue.zip;
    rm -rf aws-glue-libs-glue-1.0;
fi


# Set the environment variavles
echo "******** Setting Env variables *********";
SPARK_HOME=$USER_HOME/spark-2.4.3-bin-spark-2.4.3-bin-hadoop2.8 
echo $SPARK_HOME
echo export SPARK_HOME=$USER_HOME/spark-2.4.3-bin-spark-2.4.3-bin-hadoop2.8 >> ../glue-vars.sh
PYSPARK_PYTHON=python3.6  
echo export PYSPARK_PYTHON=python3.6 >> ../glue-vars.sh

echo export MAVEN_CONFIG=/home/.m2 >> ../glue-vars.sh
echo export M2_HOME=/usr/share/maven >> ../glue-vars.sh

echo export PYTHONPATH=$SPARK_HOME/python/lib:$USER_HOME/aws-glue-libs/awsglue:$SPARK_HOME/python/lib/pyspark.zip:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$SPARK_HOME/python:$USER_HOME/aws-glue-libs/PyGlue.zip:$USER_HOME/aws-glue-libs/PyGlue.zip/awsglue:/usr/lib/python3/dist-packages/ >> ../glue-vars.sh

#rm -rf aws-glue-libs/jarsv1/netty* 
#sed -i /^mvn/s/^/#/ aws-glue-libs/bin/glue-setup.sh
sed -i '/^mvn/ a rm -rf $ROOT_DIR/jarsv1/netty*' aws-glue-libs/bin/glue-setup.sh

#install boto3
#python -m pip install boto3

# install aws-cli
if (aws --version | grep "aws-cli") then
	echo "--> AWS is already configured"
else

	echo "********* Now Installing awscli ********"
	pip3 install awscli;
	# aws configure
	echo "******Configuring aws********"
	aws configure set aws_access_key_id $YOUR_ACCESS_KEY_ID; 
	aws configure set aws_secret_access_key $YOUR_SECRET_ACCESS_KEY; 
	aws configure set default.region "us-east-1"
fi
        #sudo apt remove python3-botocore; 
	#pip3 install botocore;
# install python local lambda
pip3 install python-lambda-local
# --> How to run: Ref: https://pypi.org/project/python-lambda-local/
echo "********Done! You are all set!*********"
