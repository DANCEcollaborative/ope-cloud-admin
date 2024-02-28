## Index Types
Now, let us examine and compare two types of indexes, single column index, and composite index, which is also known as multi-column index.

### Single Column Index
A single column index is an additional data structure of the table’s records sorted (typically via B-tree) only on that column. The values in B-Tree are sorted to enable binary search, which reduces the search time from `O(n)` to `O(log_2(n))`. Each record in the index also includes a pointer to the original record in the table, so that after searching values by the index, the query can find the matched records in the original table.

For Example, let's take the below table called users as an example:

    ID | first_name | last_name    | Class      | Position |  ssn |
    ---------------------------------------------------------------
    1 | Teemo      | Shroomer     | Specialist | Top      | 2345 |
    2 | Cecil      | Heimerdinger | Specialist | Mid      | 5461 |
    3 | Annie      | Hastur       | Mage       | Mid      | 8784 |
    4 | Fiora      | Laurent      | Slayer     | Top      | 7867 |
    5 | Garen      | Crownguard   | Fighter    | Top      | 4579 |
    6 | Malcolm    | Graves       | Specialist | ADC      | 4578 |
    7 | Irelia     | Lito         | Figher     | Top      | 5689 |
    8 | Janna      | Windforce    | Controller | Support  | 4580 |
    9 | Jarvan     | Lightshield  | Figher     | Top      | 4579 |
    10 | Katarina   | DuCouteau    | Assassin   | Mid      | 5608 |
    11 | Kayle      | Hex          | Specialist | Top      | 4794 |
    12 | Emilia     | LeBlanc      | Mage       | Mid      | 3468 |
    13 | Lee        | Sin          | Fighter    | Jungle   | 8085 |
    14 | Lux        | Crownguard   | Mage       | Mid      | 4567 |
    15 | Sarah      | Fortune      | Marksman   | ADC      | 6560 |
    16 | Morgana    | Hex          | Controller | Support  | 3457 |
    17 | Orianna    | Reveck       | Mage       | Mid      | 9282 |
    18 | Sona       | Buvelle      | Controller | Support  | 4722 |
    19 | Jericho    | Swain        | Mage       | Mid      | 5489 |
    20 | Shauna     | Vayne        | Marksman   | ADC      | 2352 |
    21 | Xin        | Zhao         | Fighter    | Jungle   | 6902 |
    22 | Yorick     | Mori         | Tank       | Top      | 4840 |
    23 | Wu         | Kong         | Fighter    | Jungle   | 4933 |


If we create an index on `users.first_name`, using the statement `CREATE INDEX first_name_index ON users (first_name) USING BTREE;`, it will create an additional data structure that sorts of the users by their `first_name` with a pointer mapped to their primary key, something like this:


    Annie    -> 3
    Cecil    -> 2
    Emilia   -> 12
    Fiora    -> 4
    Garen    -> 5
    Irelia   -> 7
    Janna    -> 8
    Jarvan   -> 9
    Jericho  -> 19
    Katarina -> 10
    Kayle    -> 11
    Lee      -> 13
    Lux      -> 14
    Malcolm  -> 6
    Morgana  -> 16
    Orianna  -> 17
    Sarah    -> 15
    Shauna   -> 20
    Sona     -> 18
    Teemo    -> 1
    Wu       -> 23
    Xin      -> 21
    Yorick   -> 22

With the index created, a query like `SELECT * FROM users WHERE first_name = 'Teemo';` would take only `O(log_2(n))` reads since the database can perform a binary search on this index since it is sorted by `first_name`.

#### How to create a single-column index?

The detailed syntax and options for creating a single column index can be found [here](https://dev.mysql.com/doc/refman/8.0/en/create-index.html) for MySQL 8.

Let us look at a few examples below to get an understanding of how to create single column indexes:

Using the same table as above, the following statement adds an index to the table:

`CREATE INDEX first_name_index ON users (first_name) USING BTREE;`

- The `CREATE INDEX` statement initiates the query to create an index, 
- `first_name_index` is the name of the index that will be created in the database,
- `On users (first_name)` is the `table_name(column_name)` on which the index is being created.
- `USING BTREE` is the algorithm that is being used for indexing.

The same index above can be created during the table creation using the syntax below,

    CREATE TABLE users (
        ID BIGINT NOT NULL,
        first_name varchar(100) ,
        last_name varchar(100)  ,
        class varchar(255) ,
        position varchar(255)  ,
        ssn BIGINT
        PRIMARY KEY (ID),
        INDEX first_name_index (first_name) USING BTREE
    );

To help you understand the syntax better, let us break down the above command as follows:

* `CREATE TABLE table_name command` - The `CREATE TABLE` statement is used to create a new table in a database. The `table_name` is replaced with whatever name you want to give the table, here we call it `users`.
* Inside the brackets, we have the syntax to create columns for the table. The above can be represented as, `COLUMN_NAME COLUMN_DATATYPE`.
* During the creation of a table we can also create indexes, inside the same brackets where rows are being created, the syntax for that is as this:`INDEX index_name (index_column) USING index_algorithm (BTREE | HASH)`

A single-column index can improve the performance of queries that look up by the column. However, for some queries, multi-column composite indexes will be a better choice.

### Multi-column Composite Index
A single-column index is self-explanatory which is an index that is based on one column, such as an index created with the statement `CREATE INDEX last_name_index ON employees (last_name)` that speeds up the lookup of the `last_name` field.

A composite index creates an index across multiple columns in a table. Let us take two columns for example, a composite index based on two columns will create a data structure that sorts data based on the first column, and then the second column. As a result, this index does not help a lookup by the second column. Hence, the order matters here, meaning the order of the columns in the composite index must match the order of the columns in the query otherwise there will be no benefit to the composite index.

### Single Column Index vs. Multi-column Composite Index

#### Performance benefit

Below is an example using the [datacharmer/test_db](https://github.com/datacharmer/test_db) dataset showing when multi-column composite indexes can be more effective than single column indexes, and when multi-column indexes cannot benefit queries at all.

    MySQL [employees]> DESCRIBE employees;
    +------------+---------------+------+-----+---------+-------+
    | Field      | Type          | Null | Key | Default | Extra |
    +------------+---------------+------+-----+---------+-------+
    | emp_no     | int           | NO   | PRI | NULL    |       |
    | birth_date | date          | NO   |     | NULL    |       |
    | first_name | varchar(14)   | NO   |     | NULL    |       |
    | last_name  | varchar(16)   | NO   | MUL | NULL    |       |
    | gender     | enum('M','F') | NO   |     | NULL    |       |
    | hire_date  | date          | NO   |     | NULL    |       |
    +------------+---------------+------+-----+---------+-------+
    6 rows in set (0.030 sec)

    
    MySQL [employees]> EXPLAIN ANALYZE SELECT * FROM employees WHERE `first_name` = 'Georgi' AND  `last_name` = 'Facello';
    | -> Filter: ((employees.last_name = 'Facello') and (employees.first_name = 'Georgi'))  (cost=29434.75 rows=2920) (actual time=0.199..115.096 rows=2 loops=1)
        -> Table scan on employees  (cost=29434.75 rows=292025) (actual time=0.172..91.928 rows=300024 loops=1)
    1 row in set (0.122 sec)
    

    MySQL [employees]> CREATE INDEX last_name_index ON employees (last_name);
    MySQL [employees]> EXPLAIN ANALYZE SELECT * FROM employees WHERE `first_name` = 'Georgi' AND  `last_name` = 'Facello';
    | -> Filter: (employees.first_name = 'Georgi')  (cost=48.36 rows=19) (actual time=0.555..0.988 rows=2 loops=1)
        -> Index lookup on employees using last_name_index (last_name='Facello')  (cost=48.36 rows=186) (actual time=0.538..0.949 rows=186 loops=1)
    1 row in set (0.016 sec)
     

    MySQL [employees]> CREATE INDEX name_index ON employees (last_name, first_name);
    MySQL [employees]> EXPLAIN ANALYZE SELECT * FROM employees WHERE `first_name` = 'Georgi' AND  `last_name` = 'Facello';
    | -> Index lookup on employees using name_index (last_name='Facello', first_name='Georgi')  (cost=0.70 rows=2) (actual time=0.117..0.121 rows=2 loops=1)
    1 row in set (0.008 sec)

The above example shows that the database has to scan all rows when there is no index. With a single-column index, the number of search rows reduces from 292025 to 186 and the performance improves from 0.122 sec to 0.016 sec. Multiple column indexes can further improve the data retrieval efficiency when we have to query all columns together in the WHERE clause. The previous example shows that multiple-column indexes can further reduce the number of search rows more than a single index from 186 to 2, and the performance improves from 0.016 sec to 0.008 sec.

MySQL can use multiple-column composite indexes for queries that test all the columns in the index, or queries that test only the first column, the first two columns, the first three columns, and so on. If you specify the columns in the right order in the index definition, a single composite index can speed up several kinds of queries on the same table.

Below shows one query that can benefit from the `(last_name, first_name)` index and one query that CANNOT benefit from the `(last_name, first_name)` index.


    MySQL [employees]> EXPLAIN ANALYZE SELECT * FROM employees WHERE `last_name` = 'Facello';
    
    | -> Index lookup on employees using name_index (last_name='Facello')  (cost=65.10 rows=186) (actual time=1.136..1.941 rows=186 loops=1)
    
    1 row in set (0.008 sec)

    MySQL [employees]> EXPLAIN ANALYZE SELECT * FROM employees WHERE `first_name` = 'Georgi';
    
    | -> Filter: (employees.first_name = 'Georgi')  (cost=29434.75 rows=29203) (actual time=0.465..113.504 rows=253 loops=1)
        -> Table scan on employees  (cost=29434.75 rows=292025) (actual time=0.410..92.166 rows=300024 loops=1)
    
    1 row in set (0.124 sec)

We can observe that when the condition is `last_name = 'Facello'` follows the composite index order, the select statement can use the index to retrieve results efficiently. However, if the query condition (`first_name = 'Georgi')` does not follow the composite index order, we can see that the select statement requires us to scan the table.

To help you evaluate the rule on whether a query can benefit from a composite index, we will provide some examples below.

Given an index over the `last_name` and `first_name` columns, the index can be used for lookups in queries that specify both `last_name` and `first_name` values; or queries that specify just a `last_name` value because that column is a leftmost prefix of the index.

Therefore, the `name` index is used for lookups in the following queries:

    SELECT * FROM employees WHERE last_name='Carnegie';
    
    
    SELECT * FROM employees
    WHERE last_name='Carnegie' AND first_name='Andrew';
    
    SELECT * FROM employees
    WHERE last_name='Carnegie'
    AND (first_name=''Andrew'' OR first_name='Andre');
    
    SELECT * FROM employees
    WHERE last_name='Carnegie' AND first_name >= 'M' AND first_name < 'N';
    
    # LIKE 'M%' is effectively a range query WHERE first_name >= 'M' AND first_name < 'N'.
    SELECT * FROM employees
    WHERE last_name='Carnegie' AND first_name LIKE 'M%';


However, the name index can NOT benefit the lookups in the following queries:

    SELECT * FROM employees WHERE first_name='Andrew';
    
    SELECT * FROM employees WHERE last_name='Carnegie' OR first_name='Andrew';


### Storage cost

As you may expect, a multi-column index on `(col1, col2)` uses more disk space than a single-column index on `(col1)`. Please compare the storage cost of `last_name_index` and `name_index` in the example below.

    MySQL [employees]> SELECT database_name, table_name, index_name, stat_value*@@innodb_page_size FROM mysql.innodb_index_stats WHERE stat_name='size';
    
    +---------------+--------------+--------------------+-------------------------------+
    | database_name | table_name   | index_name         | stat_value*@@innodb_page_size |
    +---------------+--------------+--------------------+-------------------------------+
    | employees     | departments  | PRIMARY            |                         16384 |
    | employees     | departments  | dept_name          |                         16384 |
    | employees     | dept_emp     | PRIMARY            |                      12075008 |
    | employees     | dept_emp     | dept_no            |                       5783552 |
    | employees     | dept_manager | PRIMARY            |                         16384 |
    | employees     | dept_manager | dept_no            |                         16384 |
    | employees     | employees    | PRIMARY            |                      15220736 |
    | employees     | employees    | last_name_index    |                       6832128 |
    | employees     | employees    | name_index         |                       8929280 |
    | employees     | salaries     | PRIMARY            |                     100270080 |
    | employees     | titles       | PRIMARY            |                      20512768 |
    | mysql         | component    | PRIMARY            |                         16384 |
    | sys           | sys_config   | PRIMARY            |                         16384 |
    +---------------+--------------+--------------------+-------------------------------+


