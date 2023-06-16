# Model deployment for Bangkit's Capstone Project "Hair Fit"
# Environment that this project use
- Python (`python:3.8.10`)
# Depedencies
In the `requirement.txt` maybe it looks many, but it is included the library depedencies. The actual that we install :
- fastapi 
- numpy==1.23.5 
- uvicorn 
- image 
- pydantic 
- tensorflow 
- python-multipart 
- matplotlib 
- google-cloud-storage 
- python-dotenv
# Setup
It is up to you to run it on local or cloud
1. git clone this repository into cloud shell or local repository
2. Configure your environment variable by declare it on your shell or make the .env file that located here or `./.env` or just `.env`. Below is the env variable that needed.
```bash
BACKEND="backend endpoint"
MODEL_URL="link model for download that are in GCP Bucket"
GCP_PROJECT="your gcp project id"
```
3. Get the [Model](https://github.com/Hair-Fit/Model) by running the notebook on google collab and download it. For running this prediction service on the cloud, you should upload the model in the GCS Bucket.
4. Get your service account json key and make sure your service account have permission "Storage Object Admin". Make that file located here or `/.serviceaccount.json` or `serviceaccount.json`


# Deployment

After setup, you are good to go for deployment

## Local development with installed python 
recommended do this with venv or other python virtual env

1. Install the depedencies

```shell
pip install -r requirement.txt
```

2. Init the model (if you already have or download the model, you can skip this)
```shell
python3 init-model.py
```
3. Run the service
```
uvicorn main:app --reload 
```

## Local development with docker
1. Inside current repository or directory build :
```bash
docker build -t your_user/image_name:tag_version .
```
2. After build the image run it with declared variable
```bash
docker run -p 8080:8080 \
-e BACKEND="backend endpoint" \
-e MODEL_URL="link model for download that are in GCP Bucket" \
-e GCP_PROJECT="your gcp project id" \
your_user/image_name:tag_version
```

## Run it on GCP
1. enable all the necessary gcp api :
  - Cloud Run Admin API
  - Artifact Registry API
2. Give the authorization, run it on cloud shell (the example is using asia-southeast1)
```shell
gcloud auth configure-docker asia-southeast1.pkg.dev
```
```shell
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```
3. Make the artifact repository, remember the name of it
4. Build the image on cloud shell
```shell
docker build -t asia-southeast1-docker.pkg.dev/project-id/artifact-repository/image-name:tag .
```
5. Push the image on cloud shell
```shell
docker push asia-southeast1-docker.pkg.dev/project-id/artifact-repository/image-name:tag
```
6. Create and configure service in GCP cloud run page 
  - Make sure the region is same like artifact repository 
  - Add the environment variable
  ```bash
BACKEND="backend endpoint"
MODEL_URL="link model for download that are in GCP Bucket"
GCP_PROJECT="your gcp project id"
```
7. Done <br>
the endpoint for predict would be kinda like this :
```shell
https://your-cloud-run-url/predict
```
## To test
### Using POST request method
The request header couldbe : <br>
`Conten-Type = multipart/form-data` <br>
The request body would be like  :
```json
{
  "file":your-file
}
```
### Using postman
You just need submit the image using form-data with value type as file <br>
`file : value-type-as-a-file`