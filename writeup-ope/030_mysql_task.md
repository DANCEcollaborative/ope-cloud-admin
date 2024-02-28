# MySQL Tasks

Before you login to JupyterLab and start the OPE session, there is some information and instructions which are applicable to
all three OPE tasks that we would like you to know beforehand.

## The Scenario

You are hired as a group of database engineers working in a company with a large number of employees. Your team’s responsibility is to optimize a database and provide efficient queries to meet the requirements of each use case.

## Important information applicable to all three tasks

1. Optimize the database performance in each task as needed. Each teammate has expertise in different optimization techniques based on assigned primers. Collaborate with teammates to select effective strategies and apply knowledge from **multiple primers** to complete tasks successfully.
2. In the tasks, you will directly interact with the database in MySQL shell. Login to MySQL shell using the command and password we provide at the beginning of the `workspace.ipynb` notebook in the environment.
3. Due to the large dataset, use efficient queries when testing your optimization techniques.
    * Use `COUNT(*)` to check query time and row count
    * Use `SELECT` with `LIMIT` to verify output without returning excessive records
4. To evaluate query performance, use `EXPLAIN FORMAT=JSON <YOUR SQL QUERY>` to generate a detailed query execution plan in Json format. Check the `query_cost` field to assess the query's overall cost. Higher query costs may indicate optimization opportunities to improve performance. Ensure that your final query meets specified "query_cost" thresholds to pass the tasks.
5. Each task provides unoptimized SQL statements that return the desired result set. Your optimized schema and query must return the same result as the unoptimized query.

## Set up the environment


Please follow the steps to access the MySQL shell in the environment.

1. Review the instructions carefully in the `workspace.ipynb` notebook.

2. To start the task, login to MySQL Shell using the following command and password:


        mysql -u root -p -h 127.0.0.1


    When prompted with "Enter password:", enter `CloudCC@100`.
        
    Note that the password will not show on the screen as you type.

4. After you login into MySQL Shell, you can run the following queries in MySQL shell to get familiar with the databases and tables you are going to work with:

        # List all the databases
        SHOW DATABASES;

        # The database we will be working with is `employees`
        # Switch to this certain database using the command below
        USE employees;

        # List all tables in current database
        SHOW TABLES;

        # Show all columns in a table
        DESCRIBE <table_name>;

START-PANEL:"warning"
In the OPE tasks, you are expected to submit only the final `SELECT` query in the task cell before you run local autograders. Do **NOT** add any other SQL statements such as "CREATE" or "ALTER" to the cells in the notebook, or you might break the grader.

For example, only put the `SELECT` query similar to the following statement to the task cell within **double** quotes in the notebook:

**Note:** Use single quotes for string within the query.


        SELECT <column1>, <column2>, <column3>, FROM <table_name> WHERE <condition>;


END-PANEL

This diagram shows the data types of each field in each table, as well as the relationships between tables.
![database_tables_relationship](https://clouddeveloper.blob.core.windows.net/ope-phase-2/database_tables_relationship.png)
