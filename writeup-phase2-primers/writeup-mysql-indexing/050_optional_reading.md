## (Optional Reading) Partial Index

Indexes trade space for performance. Indexes, however, occupy a lot of disk space. A table with 2 billion rows and a column last_name that is 8 bytes long, indexes use roughly 16 GB of disk space. To save space, instead of indexing the entire column, we can use a partial index and we can only index the first 4 bytes.

    CREATE INDEX last_name_index on users (last_name(4));


By creating partial indexes,  we reduce disk space for the data portion of the index by roughly half. However, the trade-off is that the database cannot eliminate as many rows using partial indexes. For instance,

    SELECT * FROM table WHERE last_name = ‘Smith’;

In this case, the database will retrieve all fields beginning with Smit, including Smith, Smitty, and so on. Therefore, the query has to discard irrelevant results such as Smitty.

A multi-column index can also make use of a partial index. Please compare the storage cost of `last_name_index`, `name_index`, and `partial_name_index` in the example below.

    
    MySQL [employees]> create index name_index on employees (last_name(4), first_name(4));
    MySQL [employees]> select database_name, table_name, index_name, stat_value*@@innodb_page_size from mysql.innodb_index_stats where stat_name='size';
    
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
    | employees     | employees    | partial_name_index |                       6832128 |
    | employees     | salaries     | PRIMARY            |                     100270080 |
    | employees     | titles       | PRIMARY            |                      20512768 |
    | mysql         | component    | PRIMARY            |                         16384 |
    | sys           | sys_config   | PRIMARY            |                         16384 |
    +---------------+--------------+--------------------+-------------------------------+

## (Optional Reading) Clustered Index
Clustered indexes are indexes whose order of the rows in the data pages corresponds to the order of the rows in the index. This order is why only one clustered index can exist in any table, whereas many non-clustered indexes can exist in a table. The columns that make up a clustered index should form a unique primary key, or any combination where values are increased for each new entry. As clustered indexes sort the records based on the value, using a column already ordered ascending, such as an identifier column, is a good choice.
In Relational Database Management System (RDBMS), usually, the primary key allows you to create a clustered index based on that specific column. Here is an example to demonstrate clustered index. At the beginning, we have a very simple table PhoneBook with three columns: LastName, FirstName and PhoneNumber.

    mysql> DESCRIBE PhoneBook;
    +-------------+-------------+------+-----+---------+-------+
    | Field       | Type        | Null | Key | Default | Extra |
    +-------------+-------------+------+-----+---------+-------+
    | LastName    | varchar(50) | NO   |     | NULL    |       |
    | FirstName   | varchar(50) | NO   |     | NULL    |       |
    | PhoneNumber | varchar(50) | NO   |     | NULL    |       |
    +-------------+-------------+------+-----+---------+-------+

We store information unorderly in the table and it is very inefficient to search for certain information. Say we are going to search a person whose LastName is Logan and FirstName is Todd, the database will search every single row until the end, because it doesn’t know where to stop – even if we found a match, we wouldn’t know if there will be more matches later on.

![Unordered data](https://clouddeveloper.blob.core.windows.net/mysql-indexing/unordered_data.png)


That led to the use of indexes. In the phonebook, the information is sorted by last names from A-Z, and if there’s any duplicates of last name, the information is further sorted by first names from A-Z. In this case, the index key is an ordered list of columns and their associated sort directions.
![Ordered data](https://clouddeveloper.blob.core.windows.net/mysql-indexing/ordered_data.png)

This makes the searching much easier, since the database knows where to stop searching because of the ordered index, and it doesn’t need to scan the whole table.
After the table data is put into physical order, SQL server builds up a set of index pages that allows queries to navigate directly to the data they’re interested in.

![Clustered index](https://clouddeveloper.blob.core.windows.net/mysql-indexing/clustered_index.png)
This entire structure, including the base table data, is called a clustered index.
When a query navigates through the index tree to the base table data, this is called a clustered index seek.
([Reference](https://www.youtube.com/watch?v=ITcOiLSfVJQ))


A column whose value changes frequently should not be used for a clustered index. The reason is that each change of the column used for the clustered index requires the records to be reordered. This reordering can easily be avoided by using a column that is updated less frequently, or ideally, not updated at all.

In the above example, it is better for us to use LastName combined with FirstName as the clustered index, because they are not likely to be changed compared with Phone Numbers. Imagine that if we use Phone Number as the clustered index ordered from 0-9, when a person changes his phone number, which is normal in real life, each level of the index should be changed. This is certainly an inefficient action that we should avoid in business scenarios.

Likewise, columns that store large data, such as `BLOB` columns (text, nvarchar(max), image, etc.), and `GUID` columns are not ideal for clustered indexes. This is because sorting large values is highly inefficient, and in the case of `GUID` and image columns, doesn't make much sense.