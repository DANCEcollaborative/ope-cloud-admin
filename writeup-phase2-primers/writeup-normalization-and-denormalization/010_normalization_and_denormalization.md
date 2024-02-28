# Normalization vs. Denormalization

## A summary of normalization vs. denormalization

[table]
  [tr]
   [td]Normalization
   [/td]
   [td]Denormalization
   [/td]
  [/tr]
  [tr]
   [td]Normalization is used in systems where the emphasis is on making general-purpose operations (insert, delete, and update) faster. This is because the entire data is properly structured in separate tables.
   [/td]
   [td]Denormalization is used in systems where the emphasis is on making the search and analysis of a particular query or data faster. This is because the tables are designed around the query.
   [/td]
  [/tr]
  [tr]
   [td]It is useful when both read and write operations need to be optimized. This is because the data in each table can be independently modified.
   [/td]
   [td]It is useful when the read operation through a particular query is the primary use case, as the data required by the query is pre-computed and stored, and can improve data retrieval efficiency.
   [/td]
  [/tr]
  [tr]
   [td]Redundant data is eliminated as normalization leads to the creation of several atomic tables.
   [/td]
   [td]Redundant data is increased because the tables which are joined together can have a many-to-many relationship and with denormalization the same data will be replicated many times. Having redundant data will result in the challenge to maintain data integrity and the cost of more disk storage.
   [/td]
  [/tr]
  [tr]
   [td]Normalization increases the number of tables, and complex queries will require expensive join operations across multiple tables.
   [/td]
   [td]Denormalization decreases the number of tables, and queries may require fewer join operations since the data has been pre-computed during denormalization.
   [/td]
  [/tr]
[/table]


## Examples to demonstrate the pros and cons of normalization vs. denormalization

Now let’s go over some use case scenarios while we discuss some differences and go over advantages and disadvantages of normalization and denormalization. To do this, we will experiment with normalization and denormalization using Yelp's [public dataset](https://www.yelp.com/dataset). We will run some queries on both normalization and denormalization tables to help you better understand their advantages and disadvantages, so you can consider the tradeoffs for various scenarios.


### Database setup

In this primer, you will experiment with normalization and denormalization using Yelp's [public dataset](https://www.yelp.com/dataset).
To run the experiments, we will use EC2 instances on AWS. Follow the steps on anywhere (local machine, AWS Cloud Shell, etc.) to provision an EC2 instance, install MySQL 8 and download datasets on the EC2 instance you provisioned.

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


Currently, you have two tables present in your Yelp Database: Reviews and Businesses. Run the following queries to review the information of these two tables.


    mysql> DESCRIBE businesses;
    mysql> DESCRIBE reviews;


### Read Operation with Normalization

Let's start with normalization. Currently, we have separate `businesses` and `reviews` tables, there’s no redundant data stored in the database, and the relationship between these two tables is through the `business_id` column. In this case, the database provides good performance for write operations such as insert,update and delete, since we do not need to synchronously update redundant data.

However, when it comes to read operation, especially complex SELECT statements that require data from multiple related tables, normalization can be ineffective, as we have to JOIN the tables and scan multiple tables.

Let’s consider the following example scenario. Say the application we are running is a website that provides information about businesses. We want to build a recommendation panel which presents businesses with the highest average star reviews. The up-to-date recommendation panel will be visited once our website is clicked, which has relatively high frequency. Let’s try to perform this read operation with normalized tables using the following query:



    SELECT b.name, t.avg_stars FROM businesses b INNER JOIN (select business_id, avg(stars) avg_stars FROM reviews GROUP BY business_id) t ON b.business_id=t.business_id WHERE avg_stars = 5;

    +-------------------------------------------+-----------+
    | name                                      | avg_stars |
    +-------------------------------------------+-----------+
    | Montallegro Barber Shop                   |    5.0000 |
    | Rio Salado Electric                       |    5.0000 |
    | Perfect Nails By Teresa                   |    5.0000 |
    | Pro Nails And Spa By Tina                 |    5.0000 |
    | Better Health Solutions                   |    5.0000 |
    …
    | ASAP Bee Removal                          |    5.0000 |
    | Paul Kitching 21212                       |    5.0000 |
    | Kip's Ice Cream                           |    5.0000 |
    | Mr Antenna USA                            |    5.0000 |
    | Escape Adventures Bike Tours & Rentals    |    5.0000 |
    | Vazkez Roofing and Repair                 |    5.0000 |
    | Mail & More                               |    5.0000 |
    +-------------------------------------------+-----------+
    19344 rows in set (2.06 sec)


Obviously, the query statement is lengthy and thus error-prone in business scenarios. Besides, it takes a significant amount of time for this single query with high querying frequency. In this case, normalization tables would provide lower performance.


### Read Operation with Denormalization

Under the same circumstance, let’s experiment how denormalization would address this scenario for complex read operations.

Denormalization is a strategy to increase performance. It is the implementation of controlled redundancy into the database, or precomputed data, to speed up the operation on it. We can use extra attributes in an existing table, add new tables, or even create instances of existing tables. Here we will go through an example that creates a precomputed table.

First of all, we will need to create a precomputed table business_star_reviews (business_id, name, average_stars) using the following command:
    
    CREATE TABLE business_star_reviews AS 
        (SELECT b.business_id, b.name, t.avg_stars FROM businesses b 
         INNER JOIN (SELECT business_id, avg(stars) avg_stars FROM reviews GROUP BY business_id) t 
         ON b.business_id = t.business_id
    );

    Query OK, 59033 rows affected (3.00 sec)
    Records: 59033  Duplicates: 0  Warnings: 0



We have created a precomputed table that stores the business name and the average star views. It becomes quite efficient if we want to query the recommendation panel! Try the following query and observe the querying time:

    SELECT name, avg_stars FROM business_star_reviews WHERE avg_stars = 5;
    
    +-------------------------------------------+----------------+
    | name                                      |     avg_stars  |
    +-------------------------------------------+----------------+
    | Montallegro Barber Shop                   |         5.0000 |
    | Pro Nails And Spa By Tina                 |         5.0000 |
    | Knight Smoke & Gift Shop                  |         5.0000 |
    | Better Health Solutions                   |         5.0000 |
    | Mt. Charleston Lodge                      |         5.0000 |
    | SimonMed Imaging                          |         5.0000 |
    | All Bar One                               |         5.0000 |
    …
    | Phoenix BJJ & MMA Academy                 |         5.0000 |
    | Las Vegas Sliding Door Repair             |         5.0000 |
    | Dairy King                                |         5.0000 |
    | Treewise                                  |         5.0000 |
    | Biz Xpress                                |         5.0000 |
    | Cotswold Medical Clinic                   |         5.0000 |
    +------------------------------------------------+-----------+
    19344 rows in set (0.04 sec)


In this scenario, you can observe that the performance has improved significantly from 2.06 sec to 0.04 sec using the denormalization technique. Also, the query statement is much simpler, which makes it easier to read and maintain for developers.


### Analysis of Read Operations with Normalization vs. Denormalization

Before we discuss other advantages and disadvantages about the two techniques, let’s analyze why the performance of read operation differs so significantly. Here we use the [EXPLAIN ANALYZE](https://dev.mysql.com/blog-archive/mysql-explain-analyze/#:~:text=EXPLAIN%20ANALYZE%20is%20a%20profiling,points%20in%20the%20execution%20plan.) query to analyze the two queries of normalization and denormalization. Note that MySQL 5.7 and MariaDB may not support `EXPLAIN ANALYZE`, so make sure you are using MySQL 8.0.18+ in this primer in order to run the statement.


    EXPLAIN ANALYZE SELECT b.name, t.avg_stars FROM businesses b INNER JOIN (select business_id, avg(stars) avg_stars FROM reviews GROUP BY business_id) t ON b.business_id=t.business_id WHERE avg_stars = 5;
    -> Nested loop inner join  (cost=199093.70 rows=138333) (actual time=1223.248..1454.490 rows=19344 loops=1)
        -> Table scan on t  (cost=0.01..1731.66 rows=138333) (actual time=1223.162..1226.939 rows=19344 loops=1)
            -> Materialize  (cost=47249.51..48981.16 rows=138333) (actual time=1223.159..1223.159 rows=19344 loops=1)
                -> Filter: (avg(reviews.stars) = 5)  (cost=33416.20 rows=138333) (actual time=1.103..1213.477 rows=19344 loops=1)
                    -> Group aggregate: avg(reviews.stars)  (cost=33416.20 rows=138333) (actual time=1.097..1201.496 rows=59033 loops=1)
                        -> Index scan on reviews using business_id  (cost=19582.90 rows=138333) (actual time=1.088..1149.513 rows=153187 loops=1)
        -> Single-row index lookup on b using PRIMARY (business_id=t.business_id)  (cost=0.99 rows=1) (actual time=0.012..0.012 rows=1 loops=19344)


    EXPLAIN ANALYZE SELECT name, avg_stars FROM business_star_reviews WHERE avg_stars = 5;
    -> Filter: (business_star_reviews.avg_stars = 5.0000)  (cost=5970.55 rows=5898) (actual time=0.029..37.620 rows=19344 loops=1)
        -> Table scan on business_star_reviews  (cost=5970.55 rows=58983) (actual time=0.026..31.517 rows=59033 loops=1)


Here is the interpretation of the two `EXPLAIN ANALYZE` statements above about the execution process of the queries with normalization versus denormalization. As counterintuitive as the `EXPLAIN ANALYZE` output format can be, note that the step with the MAX indentation level is the step that runs the first.


* Query on normalized tables consists the following steps:
    * (`Index scan on reviews using business_id`) MySQL scanned the reviews table,
    * (`Group aggregate: avg(reviews.stars)`) The `reviews` table was aggregated and a temporary table was created.
    * (`Filter: (avg(reviews.stars) = 5)`) Filter the aggregated reviews table based on WHERE clause.
    * (`Materialize` and then `Table scan on t`) The filtered, aggregated tabled was materialized and scanned.
    * (`Single-row index lookup on b`) Executed in parallel with the `Table scan on t` step, MySQL also scans the business table based on the index.
    * (`Nested loop inner join`) MySQL used a nested loop to perform an INNER JOIN on the `businesses` table and filtered aggregated reviews table to generate the final output.
* Query on the denormalized table consists of the following steps:
    * (`Table scan on business_star_reviews`) MySQL scanned the single table.
    * (`Filter`) MySQL applied a filter to fetch the required rows based on the WHERE clause and generate the final output.

With denormalization, MySQL does not need to perform the aggregation (`Group aggregate: avg(reviews.stars)`) and join (`Nested loop inner join`) as both the steps were pre-computed and the result of those steps was already stored in our denormalized table.


### Write operations with Normalization vs. Denormalization

Although denormalization provides improved reading speed in this scenario, we should analyze each technique from different aspects. As we mentioned before, one pronounced limitation of denormalization is the increased difficulty of writing and updating data, since we will have to ensure that the redundant data stays up-to-date and intact. Let’s explore further in this section.

Back to our recommendation panel example, it is fast whenever we need to select the businesses with the highest average stars with denormalization. However, in the table where we have data redundancy due to the database denormalization, updating the data may be an issue. Whenever there is any change to the reviews or businesses, for example the business name has changed, or a new review with stars is inserted, we not only need to update `businesses` and `reviews` tables, but we also need to recalculate values in the `business_star_reviews` table.


#### Write operations in Normalization

Let’s experiment with a simple example of write and update operations with normalized tables first.


    UPDATE businesses SET name = "a_new_business_name" WHERE business_id = "__3I-DDkqM9XjLH1cJl3VA";
    
    Query OK, 1 row affected (0.01 sec)
    
    Rows matched: 1  Changed: 1  Warnings: 0

For the `reviews` table, we do not need to change anything because there’s NO redundant data in normalization and the  `businesses` and `reviews` tables are bound by `business_id`.


#### Write operations in Denormalization

Let’s discuss why write operations become more complicated when using denormalization. Remember that we have created a precomputed table `business_star_reviews` which also contains `name` field. Therefore, besides updating the name in the businesses table, we will need to update the  `business_star_reviews` table as well. Otherwise, the `business_star_reviews` table will contain outdated data. Let’s look at an example to see why this will require additional data integrity risk for developers to manage.

    UPDATE business_star_reviews SET name = "a_new_business_name" WHERE business_id = "__3I-DDkqM9XjLH1cJl3VA";
    
    Query OK, 1 row affected (0.07 sec)
    
    Rows matched: 1  Changed: 1  Warnings: 0


In this simple scenario we only need one more update operation. Consider a more complex scenario where a new review is inserted and the average star of the reviews needs to get updated because of the new review. In this case, besides the insert operation, we will also need to recalculate the average star reviews and update the value in the `business_star_reviews` table.

It is complex and error-prone for developers to drop/recreate/recalculate data with denormalization. The worst case is when the data changes significantly and we have to recreate the whole precomputed table in order to store up-to-date data. When the table is large, deleting and recreating the table may introduce a prolonged delay until the table gets recreated, which maybe perceived as an outage.


    # Drop the precomputed table
    mysql> DROP TABLE business_star_reviews;

    Query OK, 0 rows affected (0.06 sec)
    
    # Recreate the precomputed table with up-to-date data
    CREATE TABLE business_star_reviews AS 
        (SELECT b.business_id, b.name, t.avg_stars FROM businesses b 
         INNER JOIN (SELECT business_id, avg(stars) avg_stars FROM reviews GROUP BY business_id) t 
         ON b.business_id = t.business_id
    );

    Query OK, 59033 rows affected (3.07 sec)
    Records: 59033  Duplicates: 0  Warnings: 0

Is it necessary to recreate the table every time a new write/update/delete operation takes place? Can we only update the rows that have been affected in the operation? Although it is technically feasible, this will still have a negative performance impact when there is any data update, and will bring technical difficulties for developers to implement and manage. Below is an example to update a single row when the average star review of a certain business changes.


    mysql> UPDATE business_star_reviews SET avg_stars = (SELECT avg(stars) avg_stars FROM reviews WHERE business_id = "__3I-DDkqM9XjLH1cJl3VA") WHERE business_id = "__3I-DDkqM9XjLH1cJl3VA";
    
    Query OK, 1 row affected (0.06 sec)
    
    Rows matched: 1  Changed: 1  Warnings: 0


Using normalized tables will save developers from writing and managing such queries.

Let’s briefly discuss another scenario to further demonstrate the performance inefficiency and potential maintenance challenges when updating data with denormalization due to data redundancy. With denormalization, redundant data is stored in the table, which uses more disk space and can make it more challenging to maintain the database. Suppose we have two normalized tables, `businesses` and `reviews`, and a denormalized table named `business_reviews` that joins these two tables. If we need to update the `business_name` given a `business_id`, we would just need to update one row in the business table. But with the denormalized `business_reviews` table that duplicates data, the rows to update can be more. Let's assume that there are 100 businesses and each business has 1000 reviews. There will be a total of 100 x 1000 = 100,000 rows in the denormalized `business_reviews` table. If we need to modify a `business_name` given a `business_id`, we have to modify all the 1000 rows of that business, since the same `business_name` value has been redundantly stored 1000 times for that particular business in the `business_reviews` table, making maintenance of the database more complex and time-consuming.

START-PANEL:"info"

A friendly reminder to terminate any cloud resources that you provisioned when completing the hands-on experiment in this primer.

END-PANEL
