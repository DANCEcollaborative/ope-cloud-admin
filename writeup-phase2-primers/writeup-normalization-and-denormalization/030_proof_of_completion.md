# Proof of Completion
In this section, you will experiment with MySQL indexing using Yelp's [public dataset](https://www.yelp.com/dataset).
To complete the Proof of Completion exercises, follow the steps in the `Database setup` section in the primer to provision an EC2 instance, install MySQL 8 and download datasets, to run the experiments and complete the Proof of Completion exercises.

START-PANEL:"info"

Note that the Proof of Completion exercise is MANDATORY in order to complete your OPE tasks. If any member of the team fails to complete this exercise, your team's OPE score will be 0, regardless of whether you achieve a perfect score on the OPE.

END-PANEL

### MySQL Query Cost

In this exercise and in the coming OPE, we will use an evaluable criteria to assess the performance of queries and database design – the cost of executing a query based on MySQL optimizer's estimated execution plan. By running the `EXPLAIN FORMAT=JSON` command on a SQL query, the `query_cost` attribute of the JSON formatted output provides an estimate of the cost of executing the query, based on the MySQL optimizer's estimated execution plan.
The query_cost value is a decimal number that represents the estimated number of resources (such as CPU cycles or disk I/O operations) that will be required to execute the query. A lower query_cost value indicates that the query is likely to be more efficient and execute faster, although there are many other factors that can affect query performance, such as table size, available memory, and server configuration. As a result, it is important to use `query_cost` as one of many metrics for evaluating query performance, rather than relying on it exclusively.


START-FORM1FAIpQLSeN9q7t1K9fp0xcPoyfgtbe-jOM7MhQ8Z21N69AFdu4FyVpTQEND-FORM


START-PANEL:"warning"

A friendly reminder to terminate the cloud resources that you provisioned when completing the hands-on experiment and Proof of Completion in this primer.

Run `terraform destroy` to delete the resources created by Terraform.

END-PANEL
