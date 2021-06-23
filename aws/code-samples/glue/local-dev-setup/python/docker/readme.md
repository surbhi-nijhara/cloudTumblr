#### Prerequisites:
1. Install docker
2. Install aws-cli


Steps:
1. Pull the required image <br>
Run : docker pull amazon/aws-glue-libs:glue_libs_1.0.0_image_01<br>

2. Mount aws credentials and working directory containing etl scripts to docker shell<br>
### Windows
Run :  docker run -itd -v C:\Users\surbhi.nijhara\.aws:/root/.aws:ro -v C:\surbhi-repo:/home/snijhara/project/ --name glue_without_notebook amazon/aws-glue-libs:glue_libs_1.0.0_image_01y

### Mac
Run: docker run -itd --name glue_without_notebook amazon/aws-glue-libs:glue_libs_1.0.0_image_01

### Linux (Ubuntu)
docker run -itd -v ~/.aws:/root/.aws:ro -v /home/snijhara/project/:/home/snijhara/project/ --name glue_without_notebook amazon/aws-glue-libs:glue_libs_1.0.0_image_01

3. Enter the Docker shell<br>
Run : docker exec -it glue_without_notebook bash

4. Go to home directory <br>
   Run : cd /home
   
5. Run : aws-glue-libs/bin/gluesparksubmit /home/snijhara/project/{path-to-python-files} --JOB_NAME  {job-name} 
