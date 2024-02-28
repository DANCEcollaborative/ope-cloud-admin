## JSON vs. TEXT

### A Brief Introduction to JSON

JSON (JavaScript Object Notation) is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of key–value pairs and arrays.

Below is an example JSON object that contains the fields (also known as keys): "followers",
"profile" and "name".

    {
        "followers":[
            {
                "profile":"https://farm4.staticflickr.com/3733/10498671606_caba28c5a6_m.jpg",
                "name":"Fortanono"
            },
            {
                "profile":"https://farm6.staticflickr.com/5779/20996394095_e3a527d780_m.jpg",
                "name":"That_Zeffia_guy"
            }
        ],
        "profile":"https://farm2.staticflickr.com/1519/26254768136_09c360b4c1_m.jpg",
        "name":"Branibor"
    }


To store JSON objects, one option to consider is surely to use document stores such as MongoDB which stores data in a JSON-like format natively. How should we store JSON objects if we are using SQL databases?

### Options to store JSON in MySQL: TEXT, flatted columns, and native JSON

If there were no native JSON data type, there are two options to store JSON objects. The first one is using a TEXT column to store JSON data directly. For example, one value stored in a column named `json_data` could be a completed JSON object as plain text:

    {"followers":[{"profile":"https://farm4.staticflickr.com/3733/10498671606_caba28c5a6_m.jpg","name":"Fortanono"},{"profile":"https://farm6.staticflickr.com/5779/20996394095_e3a527d780_m.jpg","name":"That_Zeffia_guy"}],"profile":"https://farm2.staticflickr.com/1519/26254768136_09c360b4c1_m.jpg","name":"Branibor"}


However, as you can see, when further processing is needed, storing the data as text makes it difficult for querying some specific fields inside a JSON object. How do you search JSON objects by the `name` field without scanning and processing all the records?

Another option is flattening the JSON keys to multiple columns, for example, one column named `followers`, a second column named `profile`, and a third column named `name`.

However, flattening JSON into multiple columns will have limitations when some columns can be optional and the values will be stored as NULL. Also, it can be difficult to update the schema if more fields are needed as the business evolves.

Fortunately, MySQL 5.7.8 or above supports a native JSON data type, enabling efficient access to JSON data. With the native support of the JSON structure, MySQL will automatically validate the JSON objects when writing to a column with JSON data type, which is a major advantage compared to storing the data as TEXT. On the other hand, when reading JSON values stored in the database, it can retrieve JSON data without post-processing.

Do note a nuance that creating indexes for specific keys from JSON objects is more complex than usual data types and it will use extra disk storage to store extra generated columns. JSON data cannot be indexed directly, and in order to create an index that references a field of JSON, you can define a generated column that extracts the information that should be indexed. Then you can create an index on the generated column, such indexes defined on a virtual column are known as **[virtual indexes](https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html)**. Below is an example to create an index on the `id` field of JSON:


    mysql> CREATE TABLE json_example_table (
    ->     json_data JSON,
    ->     generated_column INT GENERATED ALWAYS AS (json_data->"$.id"),
    ->     INDEX i (generated_column)
    -> );


As you may expect, virtual indexes have additional write costs due to computation performed when materializing virtual column values. Therefore, if all the JSON objects share a consistent schema that will not change in future, flattening JSON to store in a database may be a good option.

### An example to demonstrate JSON vs. TEXT

The following example shows an example of accessing JSON objects in MySQL. In this example, we store Bitcoin ticker data from Binance as JSON data in table exchange1 and TEXT data in table exchange2.


    MySQL [Exchanges]> SHOW TABLES;
    +---------------------+
    | Tables_in_Exchanges |
    +---------------------+
    | exchange1           |
    | exchange2           |
    +---------------------+
    
    MySQL [Exchanges]> DESCRIBE exchange1;
    +--------+------+------+-----+---------+-------+
    | Field  | Type | Null | Key | Default | Extra |
    +--------+------+------+-----+---------+-------+
    | ticker | json | YES  |     | NULL    |       |
    +--------+------+------+-----+---------+-------+
    1 row in set (0.024 sec)
    
    MySQL [Exchanges]> DESCRIBE exchange2;
    +--------+----------+------+-----+---------+-------+
    | Field  | Type     | Null | Key | Default | Extra |
    +--------+----------+------+-----+---------+-------+
    | ticker | longtext | YES  |     | NULL    |       |
    +--------+----------+------+-----+---------+-------+
    1 row in set (0.004 sec)
 

The following snippet shows how to select JSON objects by querying a specific JSON field.

    MySQL [Exchanges]> SELECT JSON_EXTRACT(`ticker`, "$[0]")
        -> FROM `exchange1`
        -> WHERE `ticker`-> '$[0].symbol' = "ETHBTC" LIMIT 3;
    +---------------------------------------------+
    | JSON_EXTRACT(`ticker`, "$[0]")              |
    +---------------------------------------------+
    | {"price": "0.06744200", "symbol": "ETHBTC"} |
    | {"price": "0.06744200", "symbol": "ETHBTC"} |
    | {"price": "0.06744200", "symbol": "ETHBTC"} |
    +---------------------------------------------+
    3 rows in set (0.004 sec)

However, if data is stored as TEXT, we have to scan all the data from the database and process each record in a program in order. For instance, the following Python snippet shows an example of querying JSON records from table exchange2 and finding the records whose value of the `symbol` field equals `ETHBTC`. Besides the complex Python code to implement, you can observe that the Python script takes 4 seconds, which is significantly slower than using the native JSON data type in MySQL.


    import json
    import time
    import requests
    import mysql.connector
    
    db = mysql.connector.connect(
        host="192.168.1.179",
        user="root",
        password="password",
        database="Exchanges"
    )
    
    cursor = db.cursor()
    x = []
    s = time.time()
    cursor.execute("SELECT ticker FROM exchange2")
    for r in cursor.fetchall():
        j = json.loads(r[0])
        if j[0] != "ETHBTC":
            continue
        x.append(j)
        if len(x) == 3:
            break
    e = time.time()
    print(f"cost: {e - s}")
    
    # Elapsed Time: 4.430235147476196

