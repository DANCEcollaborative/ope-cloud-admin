AZURE_STORAGE_ACCOUNT=clouddeveloper
PROJECT_ID=mysql-indexing

all: upload

upload:
	az storage container create --name ${PROJECT_ID} --account-name ${AZURE_STORAGE_ACCOUNT} --public-access blob --subscription 4171bf4b-8249-4372-a624-0728a3edb99b
	az storage blob upload-batch --destination ${PROJECT_ID}  --source ./ --account-name ${AZURE_STORAGE_ACCOUNT} --pattern '*.png*'
	az storage blob upload-batch --destination ${PROJECT_ID}  --source ./ --account-name ${AZURE_STORAGE_ACCOUNT} --pattern '*.jpg*'