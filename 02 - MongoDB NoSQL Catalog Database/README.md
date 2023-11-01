# MongoDB NoSQL Catalog Database
> All of SoftCart's catalog data was to be stored on a MongoDB NoSQL server, so I was required to:
> - Create the database `catalog` and import their electronics products from `catalog.json` into a collection named `electronics`.
> - Run test queries against the data and export the collection into a file named `electronics.csv` using only the `_id`, `type`, and `model` fields.

![Assignment 02](https://github.com/Farahat612/SoftCart-Data-Platform---IBM-Capstone-Project/assets/67427124/5b725139-2b0f-480f-96b7-50ac55b13688)


## Provided Scenario
You are a data engineer at an e-commerce company. Your company needs you to design a data platform that uses MongoDB as a NoSQL database. You will be using MongoDB to store the e-commerce catalog data.


## Exercise 01 : Setup the lab environment
This assignment will be using `mongoimport` and `mongoexport` commands from the **MongoDB CLI Database Tools** library. 

### Checking if it is installed
Firstly, I checked if the library is installed by running this command:

```console
mongoimport
```
> ```
> bash: mongoimport: command not found
> ```

So, the command is not recognized, meaning that it is not installed. 

### Installing the library
Now, I installed it running the following commands:

```console
wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
tar -xf mongodb-database-tools-ubuntu1804-x86_64-100.3.1.tgz
export PATH=$PATH:/home/project/mongodb-database-tools-ubuntu1804-x86_64-100.3.1/bin
echo "done"
```

> ```
> done
> ```

Then, I verified the installation by running the `mongoimport` command again:

```console
mongoimport --version
```
> ```
> 100.9.0
> ```
The command was then recognized, meaning the package had successfully been installed.


## Exercise 02 : Working with MongoDB

### Task 01 - Import `catalog.json` into mongodb server into a database named `catalog` and a collection named `electronics`

Firstly, I downloaded the `catalog.json` file from the given link as follows:

```console
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/nosql/catalog.json
```

Then, I started the `mongodb` server:

```console
start_mongo
```

Then I used `mongoimport` to perform the task using the user and password given to me as a result of the previous command as follows:

```console
mongoimport -u root -p MTY3MzYtbw9oYW1l --authenticationDatabase admin --db catalog --collection electronics --file catalog.json
```
> ```
> 2023-10-25T07:06:09.470-0400    connected to: mongodb://localhost/
> 2023-10-25T07:06:09.501-0400    438 document(s) imported successfully. 0 document(s) failed to import.
> ```


### Task 02 - List out all the databases

First, I connected to the `mongodb` server using credentials provided earlier.
Then, To display a list of all databases, I run the following command using the MongoDB CLI:

```console
> show dbs
```

>```
>  admin      0.000GB
>  catalog    0.000GB
>  config     0.000GB
>  local      0.000GB
>```

So, our database `catalog` had been successfully created. 


### Task 03 - List out all the collections in the database `catalog`

To display a list of all collections in `catalog` database, I can run the following command using the MongoDB CLI:

```console
> use catalog
```
>```
>  switched to db catalog
>```

```console
> show collections
```
>```
>  electronics
>```

So, our collection `electronics` had been successfully created. 


### Task 04 - Create an index on the field `type`

To create this index, I used the following command in the MongoDB CLI:

```console
> db.electronics.createIndex({"type" : 1})
```

>```
>  {
>          "createdCollectionAutomatically" : false,
>          "numIndexesBefore" : 1,
>          "numIndexesAfter" : 2,
>          "ok" : 1
>  }
>```

Now, our collection is indexed on the field `type`.


### Task 05 - Write a query to find the count of laptops

To query the count of `laptops` , I used the following command the MongoDB CLI:

```console
> db.electronics.find( {"type":"laptop"} ).count()
```
>```
>  389
>```

So, we have 389 records that has product type `laptop`.


### Task 06 - Write a query to find the number of `smart phones` with screen size of 6 inches

To display the record count for product type `smart phones` with screen size of `6 inches`, I used the following command:

```console
> db.electronics.find( {"type":"smart phone", "screen size":6} ).count()
```
>```
>  8
>```

So, we have 8 `smart phones` with screen size of `6 inches`.


### Task 07 - Write a query to find out the average screen size of `smart phones`

To display the average `screen size` of product type `smart phones`, I used the followign aggregration query:

```console
> db.electronics.aggregate([{$match: {"type": "smart phone"}},{$group: {_id:"$type", avg_val:{$avg:"$screen size"}}}])
```
>```
>  { "_id" : "smart phone", "avg_val" : 6 }
>```

Now, the average `screen size` is `6 inches`.


### Task 08 - Export the fields `_id`, `type`, `model`, from the `electronics` collection into a file named `electronics.csv`

To export the mentioned fields, I used `mongoexport` to perform the task using the credenials given to me as follows:

```console
mongoexport -u root -p MTY3MzYtbw9oYW1l --authenticationDatabase admin --db catalog --collection electronics --fiels _id,type,model --type=csv --out electronics.csv
```
> ```
> 2023-10-25T07:20:15.324-0400    connected to: mongodb://localhost/
> 2023-10-25T07:20:15.333-0400    438 document(s) imported successfully. 0 document(s) failed to import.
> ```


## View Third Task

These were all exercises in the second module of the project.
Visit the next module [here](https://github.com/Farahat612/SoftCart-Data-Platform---IBM-Capstone-Project/tree/main/03%20-PostgreSQL%20%26%20IBM%20DB2%20Data%20Warehouses).

