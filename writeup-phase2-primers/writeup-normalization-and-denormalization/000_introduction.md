# Introduction

START-PANEL:"info"
## Learning Objectives

* Describe the concept of normalization and denormalization of tables in databases.
* Describe the benefits and tradeoffs of using normalization and denormalization in databases.
* Identify use cases where denormalized or normalized tables would be preferred.
* Compare the performance of queries when using normalized vs. denormalized tables.
* Evaluate and compare the complexity of updating data in normalized and denormalized tables.
* Apply database normalization & denormalization appropriately, and be able to evaluate the optimization using 4 dimensions in the rubric.
END-PANEL

## Databases and Tables

A database is a logical framework to store organized collections of data. A database management system (DBMS) allows users to interact with the data. In relational databases, the data is organized in a series of tables, each table has a fixed number of columns. The structure of a database is typically referred to as a schema.  For example, we have a customer table that has the schema of their first names, last names, and phone numbers; another table is the order table that contains orders of various customers. The schemas of tables are fixed and each of them indicates a certain collection of related data.

Although different related data is separated in various tables, in some scenarios, there might be relations between the tables that we care about, for example, we might want to match customers with the orders they made. In this case, we could use the primary key to cross-reference data across tables.

There are different types of databases that are designed for certain use cases. A good example of these is OLTP and OLAP database systems. Online transaction processing (OLTP) systems typically capture, store, and process data using transactions. Use cases include databases used in an e-commerce application. Meanwhile, online analytical processing (OLAP) systems run complex queries against aggregated historical data from OLTP systems to extract useful insights that inform decisions. Examples include creating a sales report on the most popular sold items from yesterday's sales data of an e-commerce site.

## Normalization and Denormalization

While designing a schema for the relational database, it is important to analyze the use cases and identify how data must be stored in the tables. Normalization and denormalization are two techniques that can have a significant impact on the performance, cost, usability, and maintenance of your application. Hence, choosing the correct strategy is critical to meet your requirements. 

### Normalization

Normalization is an approach to divide the data in a database into multiple tables to reduce redundancy and improve data integrity. This includes creating tables and establishing relations between those tables according to rules designed both to ensure data integrity and to make the database more flexible by eliminating redundancy and inconsistent dependency.

### Denormalization

Denormalization is the inverse process of normalization, where multiple tables are combined into a single table. Denormalization can make data retrieval faster but at the cost of having redundant data which results in increased cost when updating data and increased risk of data integrity. This allows tables to be built and optimized for a specific set of queries but suffer from the lack the flexibility and efficiency compared to normalized schema.


## 4-Dimension Rubrics to Evaluate Database Performance

Managing a database is like organizing a closet - if things are not put away in an orderly manner, it becomes difficult to find what you need when you need it. In the same way, managing a database is crucial for ensuring that data is easy to find, accurate, and processed efficiently, which helps make informed decisions and operate more effectively. To evaluate the performance of a database, it is important to consider various factors that can impact its efficiency, scalability, storage usage, and maintainability.
In this primer, we use a rubric that assesses four dimensions to evaluate database performance: Data Retrieval Efficiency, Write Performance, Disk Storage, and Maintainability. By considering these dimensions, we can optimize database performance and ensure that our database is efficient, scalable, and easy to maintain over time. Let's take a closer look at each dimension and how it contributes to overall database performance.

* **Data Retrieval Efficiency**: Evaluate how quickly and efficiently the database can retrieve data and execute queries, and how optimization techniques/design in the primer can improve performance.
* **Write Performance**: Evaluate how effectively the database can handle insert, update, and delete operations, and how optimization techniques/design can affect performance.
* **Disk Storage**: Evaluate how efficiently the database uses disk storage, and how optimization techniques/design can reduce storage usage and improve performance.
* **Maintainability**: Evaluate how effectively the database design and optimization techniques enable the database to be maintained and updated over time, and how optimization techniques can simplify maintenance and prevent additional processing or complexity for developers.

In this primer, you will be learning how to appropriately apply normalization and denormalization to optimize database performance considering the 4 dimensions. 
