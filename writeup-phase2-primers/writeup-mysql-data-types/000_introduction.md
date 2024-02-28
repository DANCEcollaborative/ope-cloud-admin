# Introduction

START-PANEL:"info"
## Learning Objectives
* Discuss the tradeoffs of using CHAR and INT data types in MySQL across various use cases.
* Discuss the tradeoffs of using CHAR and VARCHAR data types in MySQL across use cases.
* Discuss the tradeoffs of using JSON and TEXT data types in MySQL across various use cases.
* Explain how different data types can affect the performance of database operations.
* Explain how different data types used can affect the storage cost.
* Design data types appropriately, and be able to evaluate the optimization using 4 dimensions in the rubric.
END-PANEL

## Databases and Data Types
A database is a logical framework to store organized collections of data. A database management system (DBMS) allows users to interact with the data. The data is organized in a series of tables, each table has a fixed number of columns. An example would be a table that contains customer first and last names, another table contains customer phone numbers. In each table we designate one or more columns as a primary key so that we can uniquely identify the rows of data. We also use the primary key to cross-reference data across tables, such as a customer's first and last name as well as their phone number. We update and query the data in a database using SQL. To simplify updates, data is typically split into tables where each table stores a unique portion of the data such as customer address. This approach is referred to as normalized tables. Multiple data types can be used to store data in the database. Deciding which data type to use for various use cases impacts performance, storage, usability, and maintainability among others. The purpose of this primer is to help you navigate these tradeoffs for some popular data types across various use cases.

## Data Types in MySQL
Different data types affect the performance of database operations. For example, storing integers as strings, unsurprisingly, may increase query time compared to storing integers as integers. Also, different data types affect the storage cost on disk. For instance, VARCHAR stores variable-length character strings, but CHAR uses a fixed number of bytes to store strings. In this case, VARCHAR could save space if most of the data were much smaller than the maximum size of the data type. For another instance, MySQL 5.7.8 or above versions support the JSON type, which supports storing data with JSON structure natively, which allows you to query or update JSON fields directly, and it will enhance a program’s performance without post-processing JSON data heavily. All these above are examples that choosing the correct data type is essential for an application. In the following sections, we will compare several combinations of data types across various use cases in detail.

## 4-Dimension Rubrics to Evaluate Database Performance
Managing a database is like organizing a closet - if things are not put away in an orderly manner, it becomes difficult to find what you need when you need it. In the same way, managing a database is crucial for ensuring that data is easy to find, accurate, and processed efficiently, which helps make informed decisions and operate more effectively. To evaluate the performance of a database, it is important to consider various factors that can impact its efficiency, scalability, storage usage, and maintainability.
In this primer, we use a rubric that assesses four dimensions to evaluate database performance: Data Retrieval Efficiency, Write Performance, Disk Storage, and Maintainability. By considering these dimensions, we can optimize database performance and ensure that our database is efficient, scalable, and easy to maintain over time. Let's take a closer look at each dimension and how it contributes to overall database performance.

* **Data Retrieval Efficiency**: Evaluate how quickly and efficiently the database can retrieve data and execute queries, and how optimization techniques/design in the primer can improve performance.
* **Write Performance**: Evaluate how effectively the database can handle insert, update, and delete operations, and how optimization techniques/design can affect performance.
* **Disk Storage**: Evaluate how efficiently the database uses disk storage, and how optimization techniques/design can reduce storage usage and improve performance.
* **Maintainability**: Evaluate how effectively the database design and optimization techniques enable the database to be maintained and updated over time, and how optimization techniques can simplify maintenance and prevent additional processing or complexity for developers.


In this primer, you will be learning how to choose appropriate data types to optimize database performance considering the 4 dimensions.