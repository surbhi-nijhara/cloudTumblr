Prerequisites:
Install docker
Install aws-cli


Windows:

docker run -itd -v C:\Users\surbhi.nijhara\.aws:/root/.aws:ro -v C:\surbhi-repo:/home/snijhara/project/ --name glue_without_notebook amazon/aws-glue-libs:glue_libs_1.0.0_image_01y

docker exec -it glue_without_notebook bash
