docker-compose up --remove-orphans --build --scale app=1 --scale app_s3=1 --scale app_google_drive=1 --scale app_ipfs=1
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.PIDs}}"

You need to create .env file like this:
AWS_ACCESS_KEY = #AWS_CREDENTIALS
AWS_SECRET_KEY = #AWS_CREDENTIALS

GCP_PROJECT_ID = #GOOGLE_CLOUD_CREDENTIALS
GCP_PRIVATE_KEY_ID = #GOOGLE_CLOUD_CREDENTIALS
GCP_PRIVATE_KEY = #GOOGLE_CLOUD_CREDENTIALS
GCP_CLIENT_EMAIL = #GOOGLE_CLOUD_CREDENTIALS
GCP_CLIENT_ID = #GOOGLE_CLOUD_CREDENTIALS
GCP_CLIENT_X509_CERT_URL = #GOOGLE_CLOUD_CREDENTIALS