## CHAR vs. VARCHAR

### Storage

The length of CHAR columns is fixed, and the length can be any value from 0 to 255. On the other hand, values in VARCHAR columns are variable-length, and the maximum size is 65,535. Also, the VARCHAR data type uses 1 or 2 more bytes to store the same value compared to CHAR. There is a 1-byte or 2-byte length prefix before the actual data and the length prefix indicates the number of bytes in the value. A column uses one length byte if values require no more than 255 bytes, two length bytes if values may require more than 255 bytes.

The following example shows the number of bytes of VARCHAR and CHAR stored in a database. We can observe that VARCHAR(4) uses an additional 1 byte to store string length. Therefore, when our data is fixed-length such as md5 string, using CHAR is better than using VARCHAR because there are no additional bytes for storing the data length. On the other hand, storing variable-length data as a CHAR can waste disk space and also undermine performance because more bytes are required to process if the data size is less than the maximum length.
    
    | String    | CHAR(4)   |    size   | VARCHAR(4)|   Size    |
    |:----------|:----------|:----------|:----------|:----------|
    | ""        | ''        | 4 bytes   | ''        | 1 bytes   | 
    | "ab"      | 'ab'      | 4 bytes   | 'ab'      | 3 bytes   |
    | "abcd"    | 'abcd'    | 4 bytes   | 'abcd'    | 5 bytes   |
    | "abcdefg" | 'abcd'    | 4 bytes   | 'abcd'    | 5 bytes    |


### Data may get truncated if the data exceeds the max length when using CHAR and VARCHAR

When you use CHAR or VARCHAR, you need to declare a maximum length. Note that data may get truncated if the data exceeds the declared max length when using CHAR and VARCHAR. (As a side note, enabling "strict SQL mode" can alter the behavior when data exceeds the max length, but it is beyond the scope of this primer.)

Storing data that is much shorter than the declared length using CHAR will waste a lot of space. Developers will want to declare a smallest maximum length when using CHAR to save space, e.g., using CHAR(32) instead of CHAR(255), assuming that the values will never exceed 32 characters; on the other hand, VARCHAR does not waste extra storage when storing shorter strings, developers can safely declare VARCHAR with a large enough maximum length such as VARCHAR(255), which reduces the probability that the data got accidentally truncated. Suppose there is a column that stores email addresses, CHAR(32) might seem reasonable, but  `one.surprisingly.long.unique.user.id.11251835@gmail.com` and `one.surprisingly.long.unique.user.identifier.08111919@gmail.com` are both valid email addresses that will end up both getting stored as `one.surprisingly.long.unique.user.id`; if the developers choose VARCHAR instead of CHAR with a large maximum length will help developers avoid such pitfalls.

### An example to demonstrate CHAR vs. VARCHAR

The following snippet shows an experiment of the different table size of using CHAR and
VARCHAR with two tables that have the same number of rows. Note that the data was generated from a script:

    MySQL [Employees]> SELECT COUNT(*) FROM employees1;
    +----------+
    | COUNT(*) |
    +----------+
    |  2052600 |
    +----------+
    1 row in set (0.369 sec)
    
    MySQL [Employees]> SELECT COUNT(*) FROM employees2;
    +----------+
    | COUNT(*) |
    +----------+
    |  2052600 |
    +----------+
    1 row in set (0.490 sec)

One table uses VARCHAR while the other uses CHAR.

    MySQL [Employees]> DESCRIBE employees1;
    +-------+--------------+------+-----+---------+-------+
    | Field | Type         | Null | Key | Default | Extra |
    +-------+--------------+------+-----+---------+-------+
    | id    | varchar(64)  | YES  |     | NULL    |       |
    | name  | varchar(128) | YES  |     | NULL    |       |
    +-------+--------------+------+-----+---------+-------+
    2 rows in set (0.013 sec)
    
    MySQL [Employees]> DESCRIBE employees2;
    +-------+-----------+------+-----+---------+-------+
    | Field | Type      | Null | Key | Default | Extra |
    +-------+-----------+------+-----+---------+-------+
    | id    | char(64)  | YES  |     | NULL    |       |
    | name  | char(128) | YES  |     | NULL    |       |
    +-------+-----------+------+-----+---------+-------+
    2 rows in set (0.007 sec)


The queries below calculate the storage each table takes to effectively store identical data. We can observe that VARCHAR can save disk space when most of the row data is smaller than the maximum size.

    MySQL [Employees]> SELECT table_name, round(((data_length + index_length) / 1024 / 1024), 2)
        -> as SIZE_MB FROM information_schema.TABLES 
        ->  WHERE table_schema = DATABASE() ORDER BY SIZE_MB DESC;
    +------------+---------+
    | TABLE_NAME | SIZE_MB |
    +------------+---------+
    | employees2 |  466.00 |
    | employees1 |  270.81 |
    +------------+---------+
    2 rows in set (0.006 sec)

Also, when most row data are smaller than maximum size, we can observe that operations such as indexing VARCHAR are faster than CHAR because CHAR processes more bytes than VARCHAR.


    MySQL [Employees]> SELECT * FROM employees1 WHERE name = 'fnntbtvmhjvfroghcqvfhnwwzhhznvfyeidxsndzmyhwketfrtxdwbieadatjimd';
    +--------------------------------------+------------------------------------------------------------------+
    | id                                   | name                                                             |
    +--------------------------------------+------------------------------------------------------------------+
    | 242f803c-4dd1-11ed-afac-0242ac110002 | fnntbtvmhjvfroghcqvfhnwwzhhznvfyeidxsndzmyhwketfrtxdwbieadatjimd |
    +--------------------------------------+------------------------------------------------------------------+
    1 row in set (0.770 sec)
    
    MySQL [Employees]> SELECT * FROM employees2 WHERE name = 'fnntbtvmhjvfroghcqvfhnwwzhhznvfyeidxsndzmyhwketfrtxdwbieadatjimd';
    +--------------------------------------+------------------------------------------------------------------+
    | id                                   | name                                                             |
    +--------------------------------------+------------------------------------------------------------------+
    | 242fa0a5-4dd1-11ed-afac-0242ac110002 | fnntbtvmhjvfroghcqvfhnwwzhhznvfyeidxsndzmyhwketfrtxdwbieadatjimd |
    +--------------------------------------+------------------------------------------------------------------+
    1 row in set (1.190 sec)
    
    MySQL [Employees]> CREATE INDEX uindex1 ON employees1(id);
    Query OK, 0 rows affected (4.919 sec)
    Records: 0  Duplicates: 0  Warnings: 0
    
    MySQL [Employees]> CREATE INDEX uindex2 ON employees2(id);
    Query OK, 0 rows affected (6.708 sec)
    Records: 0  Duplicates: 0  Warnings: 0


However, if all data are fixed length, such as MD5 strings that are 128-bit hash values used by scenarios such as verifying data integrity, we can observe that VARCHAR uses more disk space than CHAR because VARCHAR uses additional bytes to store the information of the string length.

    MySQL [Employees]> DESCRIBE employees1;
    +-------+-------------+------+-----+---------+-------+
    | Field | Type        | Null | Key | Default | Extra |
    +-------+-------------+------+-----+---------+-------+
    | id    | varchar(36) | YES  | MUL | NULL    |       |
    | name  | varchar(64) | YES  |     | NULL    |       |
    +-------+-------------+------+-----+---------+-------+
    2 rows in set (0.007 sec)
    
    MySQL [Employees]> DESCRIBE employees2;
    +-------+----------+------+-----+---------+-------+
    | Field | Type     | Null | Key | Default | Extra |
    +-------+----------+------+-----+---------+-------+
    | id    | char(36) | YES  | MUL | NULL    |       |
    | name  | char(64) | YES  |     | NULL    |       |
    +-------+----------+------+-----+---------+-------+
    2 rows in set (0.004 sec)
    
    MySQL [Employees]> SELECT table_name, round(((data_length + index_length) / 1024 / 1024), 2) AS SIZE_MB FROM information_schema.TABLES  WHERE table_schema = DATABASE() ORDER BY SIZE_MB DESC;
    +------------+---------+
    | TABLE_NAME | SIZE_MB |
    +------------+---------+
    | employees1 |  446.81 |
    | employees2 |  445.81 |
    +------------+---------+
    2 rows in set (0.008 sec)

In conclusion, when the data size is fixed such as MD5 hash, CHAR is a better choice than VARCHAR because we can save more disk space. However, if the length of the data varies significantly, using VARCHAR can not only save storage but also improve performance.