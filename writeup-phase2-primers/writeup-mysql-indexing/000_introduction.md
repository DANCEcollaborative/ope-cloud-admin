# Introduction

START-PANEL:"info"
## Learning Objectives

* Define and describe the purpose of indexes in relational databases.
* Explain how indexes impact the performance of both read and write operations.
* Discuss the tradeoffs of creating an index
* Discuss the tradeoffs of using single-column and multi-column composite indexes in MySQL across various use cases.
* Apply indexes appropriately, and be able to evaluate the indexing optimization using 4 dimensions in the rubric.
END-PANEL

## Databases and indexes
A database is a logical framework to store organized collections of data. A database management system (DBMS) allows users to interact with the data. The data is organized in a series of tables; each has a fixed number of columns. An example would be a table that contains customers' first and last names; another table contains customer phone numbers and a customer may have multiple phone numbers. In each table, we designate one or more columns as a unique identifier of the rows of data, known as a primary key. We also use the primary key to cross-reference data across tables, for example, to get a customer's first and last name from one table and phone number from another. We update and query the data in a database using SQL. To simplify updates and reduce data redundancy, data is typically split into tables where each table stores a unique portion of the data, such as customer address. This approach is referred to as normalized tables.  Also, multiple data types can be used to store data in the database.

One very popular operation in databases is finding data you're interested in. For example, finding the customers in a table whose first name is Alex, or to find the customers in a table who have Forbes Avenue in their address or 15213 as their zip code. To do this, you will have to visit every record in the table and check whether the first name column contains "Alex"  or whether the address column contains "Forbes Avenue" or whether the zip code column equals "15213". As you can imagine, scanning every row in a table can be an expensive operation that takes a long time to complete. We need a technique to make these types of search operations faster.

A simple analogy is that when you are looking to read a specific topic in a text book, it would be inefficient and time consuming to read every page in the textbook to find your topic of interest. To solve this problem, we dedicate a few extra pages in the textbook to create an ordered index of topics and page numbers. That way, you can search the ordered index for the topic of interest to find the page number. Then, you can quickly go to the page number to read about the topic of interest. Similarly, in database tables, we can create an index to quickly locate a row in the table without having to search every row in the table.
A database index is a data structure that we create about the data stored in the tables so that we can speed the retrieval of data in the table. Just like the text book example, we need to dedicate extra resources to create the ordered index. When the data in a table in the database is updated, the index also has to be updated. Indexes speed up locating data but they slow down updating data.

### What are indexes?
Simply put, indexes are a powerful tool used in the background of a database to avoid a complete table scan, therefore speed up queries. Indexes speed up queries because finding data in an ordered list is faster than scanning all rows, which improves the lookup time for the requested data. Although indexes speed up locating data, we are going to learn how they slow down updating data.

#### Why are Indexes needed?
Let's take a look at the following scenario. You walk into the CMU library to find the book called “A brief history of time” - by Stephen Hawking, but you are overwhelmed by the infinite number of rows and floors of books. If you now find row by row, checking each book, you will spend a lot of time finding the book. If there were a way just to know on which exact floor and row does the book reside, your search would become comparatively much faster. Indexes do precisely that; for data that is queried more often, an index on that column improves the query time.

Given a table with multiple columns, such as `first_name`, `last_name`, and `record_id`, when you create an index you need to specify which of the three columns you want to create an ordered data structure for. With that token, searches will be sped up only if they are on the column(s) for which you created the index. If you create an index on `last_name`, searches on `first_name` will not be sped up because you still need to scan the entire table. You can create more than one single column index, however, be mindful of the added cost.

Since an index provides a data structure with ordered column values, it can speed up a lookup from being a full table scan to a binary search. This reduces the complexity from  `O(size of table)` to `O(log(size of table))`.

## 4-Dimension Rubrics to Evaluate Database Performance
Managing a database is like organizing a closet - if things are not put away in an orderly manner, it becomes difficult to find what you need when you need it. In the same way, managing a database is crucial for ensuring that data is easy to find, accurate, and processed efficiently, which helps make informed decisions and operate more effectively. To evaluate the performance of a database, it is important to consider various factors that can impact its efficiency, scalability, storage usage, and maintainability.
In this primer, we use a rubric that assesses four dimensions to evaluate database performance: Data Retrieval Efficiency, Write Performance, Disk Storage, and Maintainability. By considering these dimensions, we can optimize database performance and ensure that our database is efficient, scalable, and easy to maintain over time. Let's take a closer look at each dimension and how it contributes to overall database performance.

* **Data Retrieval Efficiency**: Evaluate how quickly and efficiently the database can retrieve data and execute queries, and how optimization techniques/design in the primer can improve performance.
* **Write Performance**: Evaluate how effectively the database can handle insert, update, and delete operations, and how optimization techniques/design can affect performance.
* **Disk Storage**: Evaluate how efficiently the database uses disk storage, and how optimization techniques/design can reduce storage usage and improve performance.
* **Maintainability**: Evaluate how effectively the database design and optimization techniques enable the database to be maintained and updated over time, and how optimization techniques can simplify maintenance and prevent additional processing or complexity for developers.

In this primer, you will be learning how to appropriately create indexes to optimize database performance considering the 4 dimensions. 
