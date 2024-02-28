## CHAR vs. INT
INT (integers) stores a number, and CHAR stores fixed-length data in the database. When storing values that only consist of characters `[0-9]`, you want to choose between INT and CHAR. In this section, we will discuss the factors to consider when making decisions.

### Storage and performance

For example, `0x12345678` is a 4-byte hex value when stored as INT type, but it will take 8 bytes if stored as CHAR type, since each single number will be counted as 1 byte when represented as a string. Also, some operations will be slower such as numbers comparison, because CHAR has to compare the number byte by byte.

An index using INT and an index using CHAR will also have a performance difference. An integer primary key will always be faster for sorting and SELECTs than an alphanumeric primary key when the data is more than 4 characters long. The chances are that for any significant number of rows, in real-world applications, an alphanumeric key is likely to be greater than 4 characters.

### Data types have mathematical implications
Efficiency is always a primary factor to consider when making decisions about databases. However, performance is not the only thing to consider. Development and maintenance of the desired functionalities of the application are also practical factors that database practitioners should consider.

Using INT implies that the numbers have mathematical meanings beyond merely a unique identifier. If data is merely a fixed-length sequence that consists of characters `[0-9]`, such as an 12-digit AWS ID, a bank account or a credit card number, using CHAR can be better. A numeric identifier sequence may contain leading 0s and storing these values as an INT can introduce unnecessary gotchas and additional work for developers. For example, if an aws_id column is stored with the data type INT, using pandas.read_sql to convert the table to a dataframe will convert a 12-digit AWS ID `012345678901` to an 11-digit integer `12345678901` which introduces risk to subsequent code.  One possible risk is as follows: when an AWS account with the ID `012345678901` is linked to a billing and the boolean value `is_linked(account_id)` is therefore expected to return True; however, the code will end up returning False unless developers add extra code such as `Series.str.zfill(12)`. All such additional issues can be avoided if the aws_id column has a data type of `CHAR(12)` and `pandas.read_sql` will read this column as the Python `str` type. Also, you will never perform mathematical operations such as addition, subtraction, aggregation for data such as AWS ID, which is another reason to store the data as a string instead of integers so that the data type clearly conveys that these values should be treated as strings instead of numbers even though they consist of numbers.

Therefore, choosing appropriate data types ensures that data is stored and manipulated in a way that is consistent with its actual nature, improving the disk storage usage, data retrieval efficiency, and ease of maintenance of the database.

### An example to demonstrate CHAR vs. INT

The following example shows how choosing the wrong data type between INT and CHAR will impact performance. The following figure shows our table schemas and the number of rows. For your information, the example is based on a popular open source dataset [datacharmer/test_db](https://github.com/datacharmer/test_db).

To demonstrate the performance difference between CHAR and INT, let us examine the tables below. The first table contains a column named `employ` with the data type `INT`, while the second table contains a column named `employ` with the data type `CHAR(128)`. The two tables contain identical data, with different data types, CHAR and INT correspondingly. Of course, normally in the real world, we rarely duplicate identical data into two tables, and the tables are merely for the sake of demonstrating the performance difference of CHAR and INT.

    MySQL [employees]> DESCRIBE salaries1;
    +-----------+-----------+------+-----+---------+-------+
    | Field     | Type      | Null | Key | Default | Extra |
    +-----------+-----------+------+-----+---------+-------+
    | salary    | int       | NO   |     | NULL    |       |
    | from_date | date      | NO   | PRI | NULL    |       |
    | to_date   | date      | NO   |     | NULL    |       |
    | employ_no   | int       | YES  |     | NULL    |       |
    +-----------+-----------+------+-----+---------+-------+
    4 rows in set (0.029 sec)
    
    MySQL [employees]> DESCRIBE salaries2;
    +-----------+-----------+------+-----+---------+-------+
    | Field     | Type      | Null | Key | Default | Extra |
    +-----------+-----------+------+-----+---------+-------+
    | salary    | int       | NO   |     | NULL    |       |
    | from_date | date      | NO   | PRI | NULL    |       |
    | to_date   | date      | NO   |     | NULL    |       |
    | employ_no   | char(128) | YES  |     | NULL    |       |
    +-----------+-----------+------+-----+---------+-------+
    4 rows in set (0.027 sec)

The following queries involve selecting data from tables based on the value of the employ_no column, which requires a comparison operation.
    
    MySQL [employees]> SELECT COUNT(*) FROM salaries1 WHERE employ_no> 10001 and employ_no< 20000;
    +----------+
    | COUNT(*) |
    +----------+
    |    94895 |
    +----------+
    1 row in set (1.699 sec)
    
    MySQL [employees]> SELECT COUNT(*) FROM salaries2 WHERE employ_no> '10001' and employ_no< '20000';
    +----------+
    | COUNT(*) |
    +----------+
    |    94895 |
    +----------+
    1 row in set (2.443 sec)

In this case, we can observe that data stored as INT achieves better data retrieval efficiency than data stored as CHAR. The reason is that it is faster to compare two integers than to compare two characters.

### Converting Data Types in existing tables

As we can learn from the above example, using inappropriate data types may negatively affect database performance. Let’s explore how we can optimize the database performance by applying the most appropriate data types on existing tables.

MySQL allows a command to alter the column definition such as name and type according to our needs. We can do this with the help of an `ALTER TABLE` statement in MySQL. The following is the syntax to change the data type of a column in MySQL:

    ALTER TABLE <table_name> MODIFY <column_name> <target_datatype>;

With this statement, we can easily modify the data types in an existing table. The following example shows how to use the `ALTER TABLE` statement to change column `employ` from `CHAR(128)` to `INT` in the above table `salaries2`.

    
    MySQL [employees]> describe salaries2;
    +-----------+-----------+------+-----+---------+-------+
    | Field     | Type      | Null | Key | Default | Extra |
    +-----------+-----------+------+-----+---------+-------+
    | salary    | int       | YES  |     | NULL    |       |
    | from_date | date      | NO   | PRI | NULL    |       |
    | to_date   | date      | NO   |     | NULL    |       |
    | employ_no   | char(128) | YES  |     | NULL    |       |
    +-----------+-----------+------+-----+---------+-------+
    5 rows in set (0.034 sec)
    
    MySQL [employees]> ALTER TABLE salaries2 MODIFY COLUMN employ_no INT;
    Query OK, 2844047 rows affected (5.358 sec)
    Records: 2844047  Duplicates: 0  Warnings: 0
    
    MySQL [employees]> DESCRIBE salaries2;
    +-----------+------+------+-----+---------+-------+
    | Field     | Type | Null | Key | Default | Extra |
    +-----------+------+------+-----+---------+-------+
    | salary    | int  | YES  |     | NULL    |       |
    | from_date | date | NO   | PRI | NULL    |       |
    | to_date   | date | NO   |     | NULL    |       |
    | employ_no   | int  | YES  |     | NULL    |       |
    +-----------+------+------+-----+---------+-------+
    5 rows in set (0.012 sec)


In conclusion, storing data in the appropriate type is essential, as using different data types will affect read/write performance. For example, if columns include alphanumeric, such as an employee’s unique ID such as `cmu-andrew-000011251835`, we can use CHAR as the data type. However, if columns only contain integers and the integers may have potential mathematical meanings such as  an employee’s salary is `20000`, the more performant choice of column type is often INT. In our example, if an integer is stored as a CHAR type instead, the query will be less efficient. Even when the number of bytes of CHAR is the same as INT, updating a CHAR will still be slower than an INT because the CPU is more efficient to process integer operations compared to the equivalent string operations. This impact is more noticeable when the data is really large or when the write operations are very frequent. On the other hand, if the length of data is larger than the maximum value allowed by INT, CHAR can be a better choice. Also, when the data has a fixed length consisting of characters `[0-9]` but has no mathematical implication, using CHAR can be a better choice for better usability and maintenance.

Therefore, we must know the performance and requirements in order to make informed decisions about data type selection.

