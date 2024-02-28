## Key Takeaways

Normalization and denormalization are powerful techniques that can have a great impact on your database performance and maintainability. When deciding which technique to use in your business scenarios, analyze the use cases and potential queries, evaluate the performance of the database from the 4 dimensions in the rubric, and pay attention to the priority of your application and choose the most appropriate technique accordingly. While deciding between normalization and denormalization, pay attention to certain trade-offs in each case.

In general, normalization enables easier maintenance of data integrity and is suitable when there are frequent write operations. It is also better for scalability and maintainability, as it minimizes data redundancy and requires less disk space. For example, you may choose to use normalization for an e-commerce application where transactions are frequent and have strict demand for data integrity. But it increases the number of tables, and may require complex and expensive queries that contain JOIN operations across multiple tables.

On the other hand, denormalization is used when faster read operations are more important, especially when the queries are very complex and expensive to calculate on the fly. For example, a database that allows users to search for aggregated statistics by categories or keywords. But denormalization also creates duplicate data, at the cost of increased disk space and increased difficulty and time to perform insert/delete/update operations. Denormalization also often forces the developers to implement additional code to ensure data integrity.

## References

1. [Database normalization description - Office | Microsoft Learn](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
2. [Normalization Vs Denormalization in Database Modeling](https://www.linkedin.com/pulse/normalization-vs-denormalization-rohit-prasad/)
3. [MySQL EXPLAIN ANALYZE](https://hackmysql.com/post/book-2/)