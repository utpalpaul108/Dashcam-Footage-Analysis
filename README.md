# <div align='center'>Dashcam Footage Analysis</div>

This project focuses on analyzing dashcam footage to track and count the number of vehicles and pedestrians. Utilizing YOLOv10 for object detection and ByteTrack for object tracking, this tool processes video clips to provide accurate counts and insights into traffic patterns and pedestrian movement. The project is implemented using Streamlit for the web interface, allowing users to upload and process videos with real-time progress tracking. 

## Examples

<img src="examples/example_01.png">

## Dataset

Here, I have used the pre-trained YOLOv10 model. However, you can also use your custom dataset to train the model.


## <div style="padding-top: 20px"> Steps to run </div>

<div style="padding-bottom:10px"><b>STEP 00 :</b> Clone the repository</div>

```bash
git clone git@github.com:utpalpaul108/Dashcam-Footage-Analysis.git
```
<div style="padding-top:10px"><b>STEP 01 :</b> Create a virtual environment after opening the repository and then activate the environment</div><br>

Using Anaconda Virtual Environments

```bash
cd Dashcam-Footage-Analysis
conda create -n venv python=3.10 -y
conda activate venv
```
Or for Linux operating system, you can use that

```bash
cd Dashcam-Footage-Analysis
python3.10 -m venv venv
source venv/bin/activate
```

<div style="padding-top:10px; padding-bottom:10px"><b>STEP 02 :</b> Install the requirements</div>

```bash
pip install -r requirements.txt
```

Finally, run the following command to start your application on your desired port.
```bash
streamlit run app.py --server.port 8000
```

<div style="padding-top:10px"><b>STEP 03 :</b> Run the application</div>

Now, open up your localhost with your selected port on your web browser.
```bash
http://localhost:8000
```

## <div style="padding-top: 20px">AWS CICD Deployment With Github Actions </div>


**STEP 00 :** Login to AWS console.

**STEP 01 :** Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
**STEP 02 :** Create ECR repo to store/save docker image

    - Save the URI: 211125774196.dkr.ecr.ap-southeast-2.amazonaws.com/dashcam-footage-analysis

	
**STEP 03 :** Create EC2 machine (Ubuntu) 

**STEP 04 :** Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
**STEP 05 :** Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one

**STEP 06 :** Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = ap-southeast-2

    AWS_ECR_LOGIN_URI = demo>>  211125774196.dkr.ecr.ap-southeast-2.amazonaws.com

    ECR_REPOSITORY_NAME = dashcam-footage-analysis