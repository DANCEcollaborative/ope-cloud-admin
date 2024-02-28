## Key Takeaways
INT uses less disk space and achieves better performance than CHAR because INT uses fewer bytes to store data and processes fewer bytes faster. However, CHAR will be a good option for data such as Bank Account ID, which is a sequence of numbers but has no mathematical meaning, since INT may introduce unnecessary gotchas and additional work for developers, and lead to poor database maintenance.

Also, compared with CHAR, using VARCHAR can save disk space and improve data retrieval efficiency and write performance if the lengths of the values in a column significantly vary. However, if all the values in a column have the same length, using CHAR is a better choice because it does not cost extra space to store data length.

Finally, if data is not structured and does not need further processing, we can store the data as TEXT type. However, storing data in JSON type can help applications query specific JSON fields without scanning all the rows. Note that flattening JSON may be a good solution if all the JSON objects share a consistent and unchangeable schema, since there will be no additional space and computation cost compared to inserting and updating virtual columns when using virtual indexes with JSON type. Therefore, choosing the correct data is essential because it impacts the overall performance of database operations including both read and write, disk space utilization and the maintenance of databases.

## Reference
1. [Other MySQL Documentation](https://dev.mysql.com/doc/index-other.html)
2. [11.3.2 The CHAR and VARCHAR Types](https://dev.mysql.com/doc/refman/8.0/en/char.html)
3. [11.5 The JSON Data Type](https://dev.mysql.com/doc/refman/8.0/en/json.html)
4. [A Practical Guide to MySQL JSON Data Type By Example](https://www.mysqltutorial.org/mysql-json/)
5. [2018 of MySQL (InnoDB) CHAR vs VARCHAR](https://dba.stackexchange.com/questions/226502/2018-of-mysql-innodb-char-vs-varchar)
6. [MySQL Performance - CHAR(64) vs VARCHAR(64) [closed]](https://stackoverflow.com/questions/26558094/mysql-performance-char64-vs-varchar64)
7. [Advanced JSON to MySQL indexing](https://www.percona.com/blog/2015/03/10/advanced-json-to-mysql-indexing-aggregation-highly-complex-json-documents/)
8. [13.1.20.9 Secondary Indexes and Generated Columns](https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html)
9. [MySQL forum - Re: Primary key performance int vs. char](https://forums.mysql.com/read.php?21,36252,36263)
10. [JSON](https://www.json.org/json-en.html)