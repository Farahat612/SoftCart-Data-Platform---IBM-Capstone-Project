# Apache Spark Big Data Analytics
> The team has prepared a set of data containing search terms on their e-Commerce platform. So, I was required to:
> - Download the data and run analytic queries on it using `pyspark` and `JupyterLab`.
> - Use a pretrained sales forecasting model to predict the sales for 2023.

<p align="center">
  <img width="100%" src="../Images/assignment06.png">
</p>

## Outline
In this module, I was required to analyze search terms data from the e-commerce web server,  load the sales forecast model and predict the sales for the year 2023.

## Exercise 01 : Preparing The Environment
### 1. Installing `pyspark`

```console
!pip install pyspark
!pip install findspark
```
> ```console
> Successfully installed findspark-2.0.1
> ```


## 2. Creating the Spark Session and Context

```python
import findspark
findspark.init()

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

# Creating a spark context class
sc = SparkContext()

# Creating a spark session
spark = SparkSession \
    .builder \
    .appName("Saving and Loading a SparkML Model").getOrCreate()
```
> ```console
> 23/10/26 08:43:23 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable Setting default log level to "WARN".
> To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
> ```


### 3. Downloading the source file

First I downloaded the source file that contains our search term data `searchterms.csv` from the provided url.
```console
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/searchterms.csv
```
> ```console
> --2023-10-26 08:43:29--  https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-killsNetwork/Bigdata%20and%20Spark/searchterms.csv
> Resolving cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud (cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud)... 169.63.118.104
> Connecting to cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud (cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud)|169.63.118.104|:443... connected.
> HTTP request sent, awaiting response... 200 OK
> Length: 233457 (228K) [text/csv]
> Saving to: ‘searchterms.csv’
> 
> searchterms.csv     100%[===================>] 227.99K  --.-KB/s    in 0.005s  
> 
> 2023-10-26 08:43:29 (40.7 MB/s) - ‘searchterms.csv’ saved [233457/233457]
> 
> ```


Then, I loaded it into a dataframe `seach_term_dataset`.
```python
src = 'searchterms.csv'
search_term_dataset = spark.read.csv(src)
```


Finally, I ispected the dataframe by displaying the number of rows and columns.
```python
row_count = search_term_dataset.count()
col_count = len(search_term_dataset.columns)
print(f'Row count for search_term_dataset: {row_count}')
print(f'Column count for search_term_dataset: {col_count}')
```
> ```
> Row count for search_term_dataset: 10001
> Column count for search_term_dataset: 4
> ```



## Exercise 02 : Analyzing Search Terms

### 1. Discovering The Data
First I viewed the first 5 rows of our dataset to get an overview of the data. I found 4 columns `_c0`, `_c1`, `_c2`, and `_c3` attributed to search `day`, `month`, `year`, and `searchterm` respectively.

```python
search_term_dataset.show(5)
```
> ```
> +---+-----+----+--------------+
> |_c0|  _c1| _c2|           _c3|
> +---+-----+----+--------------+
> |day|month|year|    searchterm|
> | 12|   11|2021| mobile 6 inch|
> | 12|   11|2021| mobile latest|
> | 12|   11|2021|   tablet wifi|
> | 12|   11|2021|laptop 14 inch|
> +---+-----+----+--------------+
> only showing top 5 rows
> ```


Then I displayed the datatype for the `searchterm` column.
```python
print(search_term_dataset.schema['_c3'].dataType)
```
> ```
> StringType
> ```


### 2. Analyzing the Data
1. I was required to determine to know how many times the term `gaming laptop` was searched, I accomplished that with a code that:
- Creates a Spark view from the dataframe
- Runs a simple COUNT() query with `spark.sql` where `_c3` is equal to `gaming laptop`

```python
search_term_dataset.createOrReplaceTempView('searches')
spark.sql('SELECT COUNT(*) FROM searches WHERE _c3="gaming laptop"').show()
```
> ```
> +--------+
> |count(1)|
> +--------+
> |     499|
> +--------+
> ```


2. Secondly, I was required to show the top 5 most frequently used search terms, so, Using `spark.sql` I could select the search terms and group them with a descending order by count.

```python
spark.sql('SELECT _c3, COUNT(_c3) FROM searches GROUP BY _c3 ORDER BY COUNT(_c3) DESC').show(5)
```
> ```
> +-------------+----------+
> |          _c3|count(_c3)|
> +-------------+----------+
> |mobile 6 inch|      2312|
> |    mobile 5g|      2301|
> |mobile latest|      1327|
> |       laptop|       935|
> |  tablet wifi|       896|
> +-------------+----------+
> only showing top 5 rows
> ```



## Exercise 03 : Sales Forecasting Model

### Preparing The Model
1. First I needed to download the provided pretrained `sales forecasting model` from the provided url.

```console
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/model.tar.gz
```

> ```console
> --2023-10-26 08:43:56--  https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/model.tar.gz
> Resolving cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud (cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud)... 169.63.118.104
> Connecting to cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud (cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud)|169.63.118.104|:443... connected.
> HTTP request sent, awaiting response... 200 OK
> Length: 1490 (1.5K) [application/x-tar]
> Saving to: ‘model.tar.gz’
> 
> model.tar.gz        100%[===================>]   1.46K  --.-KB/s    in 0s      
> 
> 2023-10-26 08:43:56 (9.70 MB/s) - ‘model.tar.gz’ saved [1490/1490]
> 
> ```

2. Then, I extracted the file as follows:
```console
!tar -xvzf model.tar.gz
```
> ```console
> sales_prediction.model/
> ales_prediction.model/metadata/
> sales_prediction.model/metadata/part-00000
> sales_prediction.model/metadata/.part-00000.crc
> sales_prediction.model/metadata/_SUCCESS
> sales_prediction.model/metadata/._SUCCESS.crc
> sales_prediction.model/data/
> sales_prediction.model/data/part-00000-1db9fe2f-4d93-4b1f-966b-3b09e72d664e-c000.snappy.parquet
> sales_prediction.model/data/_SUCCESS
> sales_prediction.model/data/.part-00000-1db9fe2f-4d93-4b1f-966b-3b09e72d664e-c000.snappy.parquet.crc
> sales_prediction.model/data/._SUCCESS.crc
> 
> ```


### Loading The Model
1. I created a dataframe `sales_prediction_df` from the parquet and printed the schema.

```python
sales_prediction_parquet = 'sales_prediction.model/data/part-00000-1db9fe2f-4d93-4b1f-966b-3b09e72d664e-c000.snappy.parquet'
sales_prediction_df = spark.read.parquet(sales_prediction_parquet)
sales_prediction_df.printSchema()
```

> ```console
> root
>  |-- intercept: double (nullable = true)
>  |-- coefficients: vector (nullable = true)
>  |-- scale: double (nullable = true)
> ```

2. Then, I loaded the model into `sales_prediction_model`.

```python
from pyspark.ml.regression import LinearRegressionModel
sales_prediction_model = LinearRegressionModel.load('sales_prediction.model')
```


### Using The Model
I was required to use the `sales forecast model` to predict the sales for the year of 2023 as follows:

```python
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
def predict(year):
    assembler = VectorAssembler(inputCols=["year"],outputCol="features")
    data = [[year,0]]
    columns = ["year", "sales"]
    _ = spark.createDataFrame(data, columns)
    __ = assembler.transform(_).select('features','sales')
    predictions = sales_prediction_model.transform(__)
    predictions.select('prediction').show()
predict(2023)
```

> ```
> +------------------+
> |        prediction|
> +------------------+
> |175.16564294006457|
> +------------------+
> ```



## Final Words
That was it, all the project modules, if you made it to here, I hope you got the most out of the project. Thank you.


