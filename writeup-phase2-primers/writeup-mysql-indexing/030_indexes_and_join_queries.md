## Indexes and JOIN Queries
As demonstrated with the examples above, indexes speed up lookup as it reduces a full table scan to binary search. Indexes also speed up JOIN queries that query data from two or more related tables, as an index on the inner table is helpful to allow the matching rows to be efficiently found and thus avoiding having to scan all entries for each row from the outer table. MySQL executes joins between tables using a nested-loop algorithm or variations on it.

Without indexes, joining two tables will use the following algorithm:

    algorithm nested_loop_join is
        for each record record_t1 in table1 do
            for each record record_t2 in table2 do
                if record_t1 and record_t2 satisfy the join condition then
                    yield tuple <record_t1,record_t2>


If the inner relation has an index on the attributes used in the join, then the naive nest loop join can be replaced with an index join.
    
    algorithm index_join is
        for each record record_t1 in table1 do
            for each record record_t2 in table2 in the index lookup do
                yield tuple <record_t1,record_t2>


The time complexity improves from  `O(size of table1 * size of table2)` to `O(size of table1 * log (size of table2))`.
