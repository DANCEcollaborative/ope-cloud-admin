# Proof of Completion
In this section, you will experiment with data type conversion using Yelp's [public dataset](https://www.yelp.com/dataset).
To run the experiments and complete the Proof of Completion exercises, we will use EC2 instances on AWS. Follow the steps on anywhere (local machine, AWS Cloud Shell, etc.) to provision an EC2 instance, install MySQL 8 and download datasets on the EC2 instance you provisioned.

START-PANEL:"info"

Note that the Proof of Completion exercise is MANDATORY in order to complete your OPE tasks. If any member of the team fails to complete this exercise, your team's OPE score will be 0, regardless of whether you achieve a perfect score on the OPE.

END-PANEL

### Database setup

1. Download and extract the Terraform configuration files using the following commands.


        $ mkdir terraform && cd terraform
        $ wget https://clouddeveloper.blob.core.windows.net/ope-phase-2/terraform/ope-proof-of-completion.tgz
        $ tar -xvzf ope-proof-of-completion.tgz


2. Make sure `awscli` is installed and run the following command to configure awscli with your AWS credentials.


        $ aws configure

    To find your credentials, navigate to the [IAM security credentials console](https://us-east-1.console.aws.amazon.com/iamv2/home#/security_credentials) in the AWS Management Console, and scroll down to locate the access keys  section. If you have not yet created an access key, generate one now by clicking the "Create New Access Key" button. Make sure that you are using the AWS credentials for your team project to avoid penalties for unauthorized usage.



3. Create a file named `terraform.tfvars` and set the values of the variables defined at `variables.tf`. A sample of `terraform.tfvars` is as the following:


        key_name="<put your pem key name here>" # NOTE: DO NOT include the ".pem" file extension.
        project_tag="twitter-phase-2"
        ami_id="ami-09cd747c78a9add63"

4. Then run the following commands to provision the EC2 instance.


        $ terraform init
        $ terraform apply


5. After the instance is running, SSH into the VM (you may SSH into the VM as user "ubuntu", or connect through AWS Console) and install MySQL 8 on the VM by running the bash script using the following command. Note that the following command is the combination of downloading and running the script.


        $ wget https://s3.amazonaws.com/cmucc-instance-launcher/ope/install_mysql8.sh && yes | sh install_mysql8.sh


6. Now you have installed and configured MySQL 8 on the VM. Follow the steps to download the dataset:


        $ declare -a data_files=(businesses checkin review tip user)
    
        $ for data_file in "${data_files[@]}"; do
        wget https://clouddeveloper.blob.core.windows.net/datasets/cloud-storage/yelp_academic_dataset_"$data_file".tsv
        done


    You can validate the TSV files with `wc -l *.tsv` and the expected output is as follows:



         174568 yelp_academic_dataset_businesses.tsv
         146351 yelp_academic_dataset_checkin.tsv
         153190 yelp_academic_dataset_review.tsv
         643783 yelp_academic_dataset_tip.tsv
         357182 yelp_academic_dataset_user.tsv
        1475074 total


7. Download the script that will create and load the database:


        $ wget https://clouddeveloper.blob.core.windows.net/datasets/cloud-storage/create_yelp_database.sql -O create_yelp_database.sql


8. You can load the data files into the database with the following command. Please note that running this command may take several tens of minutes, and there will be no visible output during the loading process. Please wait patiently until the loading is completed.


        $ mysql -u root -ppassword --local-infile=1 < create_yelp_database.sql




9. After the command has been completed successfully and the tables have been created, you can login as root user, inspect and verify the schemas with the following commands:


        $ mysql -u root -ppassword

        # set the working database
        mysql> USE yelp_db;
        # list the tables
        mysql> SHOW TABLES;
        # show the schema of a table
        mysql> DESCRIBE businesses;


10. To verify whether the data has been successfully loaded into the database, you can list the first 10 records of the table using the SELECT command:


        mysql> SELECT * FROM businesses LIMIT 10;



### MySQL Query Cost

In this exercise and in the coming OPE, we will use an evaluable criteria to assess the performance of queries and database design – the cost of executing a query based on MySQL optimizer's estimated execution plan. By running the `EXPLAIN FORMAT=JSON` command on a SQL query, the `query_cost` attribute of the JSON formatted output provides an estimate of the cost of executing the query, based on the MySQL optimizer's estimated execution plan.
The query_cost value is a decimal number that represents the estimated number of resources (such as CPU cycles or disk I/O operations) that will be required to execute the query. A lower query_cost value indicates that the query is likely to be more efficient and execute faster, although there are many other factors that can affect query performance, such as table size, available memory, and server configuration. As a result, it is important to use `query_cost` as one of many metrics for evaluating query performance, rather than relying on it exclusively.


START-FORM1FAIpQLSfcQ7pUfgAVmsxxS7ozx2b0hdVOm2hW8DTkBErzD40rGk1SDgEND-FORM


START-PANEL:"warning"

A friendly reminder to terminate the cloud resources that you provisioned when completing the hands-on experiment and Proof of Completion in this primer.

Run `terraform destroy` to delete the resources created by Terraform.

END-PANEL
