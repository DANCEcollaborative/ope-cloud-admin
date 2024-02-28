## What are the trade-offs?

Despite the performance benefits for read operations, indexes are not without cost. When you create an index, a data structure is created and it has to be updated with every write. , resulting in the cost of more disk storage and adding complexity and additional maintenance overhead for developers. One needs to carefully consider if there is a net gain in creating an index and that the index will be used for popular queries that are executed frequently. The downside to adding indexes to a table is that they affect write performance because each index needs to be modified during writes (`INSERT`, `UPDATE`, `DELETE`). Single column indexes tend to have a lower impact on write performance because they are associated with a single column and require fewer updates when data is modified. In contrast, composite indexes may have a higher impact on write performance due to the need to update the index whenever any of the indexed columns are modified. Also, each index takes extra storage space on the disk. Before creating an index, one has to carefully examine a specific query or a set of queries to decide how an index will benefit these queries.

Moreover, it is a common misconception that extraneous indexes only negatively impact writes but not reads. Actually, excessive indexing can even negatively affect data retrieval efficiency. To understand how indexes can potentially hurt read performance, we should first understand the concept of a query optimizer. A query optimizer is a critical database management system (DBMS) component that analyzes SQL queries and determines efficient execution mechanisms. Given a query, a query optimizer will generate one or more query plans for each query and then choose the most efficient query plan to run the query. If you create indexes which might seem relevant for a query, but turn out to be unuseable, the query optimizer will waste time evaluating whether and how to use all the candidate indexes. In extreme cases with very complicated indexes, the query optimizer might end up choosing a suboptimal query plan because of the indexes. Any table configuration where performance suffers due to excessive, improper, or missing indexes can be considered a poor index design.

A poor index can be an index created on a column that does not benefit the target query that you want to optimize. Take the following query as an example with the dataset [datacharmer/test_db](https://github.com/datacharmer/test_db), creating an index on the `birth_date` column does not improve the performance of the query with the condition `where extract(YEAR FROM birth_date) = 1989` and actually slightly hurts performance.

    MySQL [employees]> EXPLAIN ANALYZE SELECT COUNT(*) FROM employees WHERE extract(YEAR FROM birth_date) = 1989
    
    | -> Aggregate: count(0)  (cost=58637.25 rows=1) (actual time=60.927..60.927 rows=1 loops=1)
        -> Filter: (extract(year from employees.birth_date) = 1989)  (cost=29434.75 rows=292025) (actual time=60.915..60.915 rows=0 loops=1)
            -> Table scan on employees  (cost=29434.75 rows=292025) (actual time=0.088..44.978 rows=300024 loops=1)
    1 row in set (0.067 sec)
    
    
    MySQL [employees]> CREATE INDEX date ON employees (birth_date);
    MySQL [employees]> EXPLAIN ANALYZE SELECT COUNT(*) FROM employees WHERE extract(YEAR FROM birth_date) = 1989;
    | -> Aggregate: count(0)  (cost=58637.25 rows=1) (actual time=61.435..61.435 rows=1 loops=1)
        -> Filter: (extract(year from employees.birth_date) = 1989)  (cost=29434.75 rows=292025) (actual time=61.431..61.431 rows=0 loops=1)
            -> Covering index scan on employees using date  (cost=29434.75 rows=292025) (actual time=0.593..44.131 rows=300024 loops=1)
    1 row in set (0.068 sec)

Another example of an unnecessary index that cannot benefit any operations but only hurt performance is an index as follows:

    # this index can help on queries that based on (Col1),  (Col1, Col2) and (Col1, Col2, Col3)
    CREATE INDEX existing_index ON SomeTable(Col1, Col2, Col3); 
    
    # given the existing index on (Col1, Col2, Col3), creating this additional index is unnecessary and will only hurt performance
    CREATE INDEX unnecessary_index ON SomeTable(Col1, Col2); 
