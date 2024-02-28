## Key takeaways

When it comes to index design, you must analyze the queries that you have in order to decide which indexes to create. You cannot discuss indexes without knowing the concrete business use cases and the queries.

Indexing trade write operation performance for read operation performance. An index can largely improve data retrieval efficiency for the columns that the index is created upon; however, when data it comes to write operations such as insert, update or delete, the index has to be refreshed to handle the new record, and thus negatively affect write operations. Single column indexes generally have a lower impact on write performance compared to composite indexes because they require fewer updates when data is modified, only affecting their associated column. In addition, indexes require additional disk storage, and lead to extra database maintenance overhead for developers

Based on the queries that you need, you may want to choose between single column indexes and multiple column composite indexes. A multiple column index can better speed up a query if the query is based on the multiple columns compared to a single column index. However, multiple-column indexes for queries can only improve queries that look up the columns in the index in order, the first column, the first two columns in order, the first three columns in order, and so on. Multi-column indexes cannot benefit queries based on other combinations or ordering such as the second and third columns, or the second and first columns.

## References

1. [MySQL Composite Index - Leveraging multiple-column indexes to Speed up Queries](https://www.mysqltutorial.org/mysql-index/mysql-composite-index/)
2. [Advantages and Disadvantages of Indexing in SQL - Scaler Topics](https://www.scaler.com/topics/sql/advantages-and-disadvantages-of-indexing-in-sql/)
3. [The Downside of Database Indexing](https://www.navicat.com/en/company/aboutus/blog/1764-the-downside-of-database-indexing#:~:text=The%20downside%20to%20adding%20indexes,considered%20to%20be%20poor%20indexing)
4. [Nested loop join - Wikipedia](https://en.wikipedia.org/wiki/Nested_loop_join)
5. [MySQL 8.0 Reference Manual :: 8.3.6 Multiple-Column Indexes](https://dev.mysql.com/doc/refman/8.0/en/multiple-column-indexes.html)
6. [Chapter 4. Indexes](https://www.oreilly.com/library/view/high-performance-mysql/0596003064/ch04.html)
