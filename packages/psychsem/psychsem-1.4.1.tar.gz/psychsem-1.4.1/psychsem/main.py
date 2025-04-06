def psych10():
    print("Psych thats a wrong number...again...dammm")
    
def psych():
    print("well,well,well....Here we are .... my friend")

def HSREAD():
    print('''from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('read data eg').getOrCreate()
df = spark.read.option("Header",True).csv('employee.csv')
df.show()
df.show(5)
df.printSchema()
df.select("Salary").show()
df.select("Salary").show(3)
df.filter(df["Salary"]>15000).show()
pandas_df = df.toPandas()
print(pandas_df.head())
print(pandas_df.tail())
spark.stop()''')
    
def HSUNION():
    print('''from pyspark.sql import SparkSession
from pyspark.sql.functions import col
spark = SparkSession.builder.appName('Combined DataFrame').getOrCreate()
data1 = [(1,"maz",50),(2,"ram",21),(3,"aaa",5)]
data2 = [(4,"aasxdqd",22),(5,"aaeeas",25),(6,"sem",24)]
column = ["ID","Name","Age"]
df1 = spark.createDataFrame(data1,column)
df2 = spark.createDataFrame(data2,column)
df1.show()
df2.show()
#union
Combined_df = df1.union(df2)
Combined_df.show()
df3=df2.select("ID","Name","Age")
Combined_df.show()
# Using joins [merging dataframe on a column]
data4 = [(1,"Mumbai"),(2,"Bangalore"),(3,"Delhi"),(4,"Amritsar"),(5,"Kolkata"),(6,"Chennai")]
column2 = ["ID","City"]
df4 = spark.createDataFrame(data4,column2)
df4.show()
join_df = df1.join(df4,on="ID",how="inner")
join_df.show()
df1 = df1.withColumn("Country",col("Name"))
df1.show()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('read data eg').getOrCreate()
df1 = spark.read.option("Header",True).csv('dept.csv')
df1.show()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('read data eg').getOrCreate()
df2 = spark.read.option("Header",True).csv('employee.csv')
df2.show()
df_merge=df1.join(df2,on="dept_id",how="inner")
df_merge.show()''')
    
def HSRDD():
    print('''from pyspark.sql import  SparkSession
from pyspark.sql.functions import col
spark = SparkSession.builder.appName('read data eg').getOrCreate()
data = [(1,"Laptop",1000,"Electronics"),
        (2,"Shoes",50,"Fashion"),
        (3, "Shirt", 25, "Fashion"),
        (4, "Headphones", 150, "Electronics"),
        (5, "Pants", 40, "Fashion")]
column = ["prod_id","product","price","category"]
df = spark.createDataFrame(data,column)
print(" -D037")
df.show()
collected_data=df.collect()
for row in collected_data :
  print(row)
  df.filter(df["price"]>100).show()

from pyspark.sql import SparkSession
# Initialize Spark Session
spark = SparkSession.builder.appName("SalesTotal").getOrCreate()
sc = spark.sparkContext  # Get the SparkContext
# Sample sales data (Product, Price)
sales_data = [
    ("Laptop", 1000),
    ("Mobile", 500),
    ("Laptop", 1200),
    ("Tablet", 700),
    ("Mobile", 450),
    ("Tablet", 650),
    ("Laptop", 1100),
    ("Mobile", 520),
]
# Create an RDD
rdd = sc.parallelize(sales_data)
# Map Step: Convert each entry to (Product, Price)
mapped_rdd = rdd.map(lambda x: (x[0], x[1]))
# Reduce Step: Sum up sales for each product
total_sales_rdd = mapped_rdd.reduceByKey(lambda a, b: a + b)
print("**********************************")
print("Sales Data Analysis : Map reduce")
print("**********************************")
# Collect and print results
result = total_sales_rdd.collect()
for product, total in result:
    print(f"{product}: ${total}")

# Stop Spark session
spark.stop()''')
    
def HSUDF():
    print('''from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark =  SparkSession.builder.appName("udf examle").getOrCreate()

data = [("alex",65),("max",15),("ray",45),]
columns = ["Name","Age"]
df  = spark.createDataFrame(data,columns)
df.show()
def age_group(age):
  if age < 18:
    return "Minor"
  elif age >= 18 and age < 60:
    return "Adult"
  else:
    return "Senior"
age_group_udf = udf(age_group,StringType())

df_with_group = df.withColumn("Age_Group",age_group_udf(df["Age"]))
df_with_group.show()
age_count = df_with_group.groupBy("Age_Group").count()
age_count.show()''')
    

def HSRMSE():
    print('''from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
spark.stop()
spark =  SparkSession.builder.appName("udf examle").getOrCreate()
data =[(1,100),(2,110),(3,120),(4,130),(5,105)]
columns=["Feature","Target"]
df  = spark.createDataFrame(data,columns)
df.show()
Assembler = VectorAssembler(inputCols=["Feature"],outputCol="Features")
Assemebled_df = Assembler.transform(df).select("Features","Target")
Assemebled_df.show()
LR = LinearRegression(featuresCol="Features",labelCol="Target")
LR_model = LR.fit(Assemebled_df)
print(LR_model.coefficients)
print(LR_model.intercept)
training_summary = LR_model.summary
RMSE = training_summary.rootMeanSquaredError
print("RMSE,",RMSE)
print(" - ")
print("***********************************")
prediction = LR_model.transform(Assemebled_df)
print(prediction.show())''')
    
def HSKMEANS():
    print('''from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
spark = SparkSession.builder.appName("KMeans").getOrCreate()
data = [(1.0,2.0),(1.5,1.8),(5.0,8.0),(8.0,8.0),(1.0,0.6),(9.0,11.0)]
columns = ['Sub1','Sub2']
df = spark.createDataFrame(data,columns)
print(" -037")
df.show()
assembler = VectorAssembler(inputCols=['Sub1','Sub2'],outputCol='features')
assembler1=assembler.transform(df)
assembler1.show()
Kmeans = KMeans(k=2,seed=1)
model = Kmeans.fit(assembler1)
prediction = model.transform(assembler1)
prediction.show()
print(" - ")
print("***********************************")
for center in model.clusterCenters():
  print(center)''')
    
def HSLR():
    print('''from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import CountVectorizer,IDF,Tokenizer
spark = SparkSession.builder.appName("Logistic Regresion").getOrCreate()
#sample email data
data = [ (1,"win a free iphone") ,(1,"congratulation you won a lottery"),
 (0,"lets meet for lunch"),(0,"don't forget to complete the assignment")]
columns = ['label','text']
df = spark.createDataFrame(data,columns)
print(" - ")
df.show()
#preprocess
tokenizer = Tokenizer(inputCol='text',outputCol='tokens')
df = tokenizer.transform(df)
df.show()
vectorizer = CountVectorizer(inputCol='tokens',outputCol='rawfeature')
vector_model = vectorizer.fit(df)
df = vector_model.transform(df)
df.show()
print(" -  ")
print("***********************************")
df = df.select('label','rawfeature') # Change 'features1' to 'rawfeature'
df = df.withColumnRenamed("rawfeature","features1") # Rename the column to 'features1' if necessary for Logistic Regression

LR = LogisticRegression(featuresCol='features1',labelCol='label') # LR is used as the variable for LogisticRegression
lr_model = LR.fit(df)

prediction = lr_model.transform(df)
prediction.show()''')
    
def HSNB():
    print('''from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

print("")
print("***********************************")

# Initialize SparkSession.
# When running on a Hadoop cluster, SparkSession will automatically connect to your Hadoop/HDFS environment.
spark = SparkSession.builder \
    .appName("NaiveBayesInPySpark") \
    .getOrCreate()

# -------------------------------------------------------------------------------
# If your data resides in HDFS, uncomment and modify the following line:
# df = spark.read.format("csv").option("header", "true").load("hdfs:///path/to/your/data.csv")
# -------------------------------------------------------------------------------

# For demonstration, we create a small sample dataset.
data = [
    (0, "spark is great and fast", "positive"),
    (1, "hadoop is reliable but slow", "negative"),
    (2, "spark and hadoop are big data technologies", "positive"),
    (3, "I dislike hadoop performance", "negative"),
    (4, "spark offers ease of development", "positive"),
    (5, "I am frustrated by hadoop complexities", "negative")
]
columns = ["id", "text", "label"]
df = spark.createDataFrame(data, columns)

# Convert string labels to numeric indices using StringIndexer.
labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel")

# Tokenize the text column: this splits sentences into words.
tokenizer = Tokenizer(inputCol="text", outputCol="words")

# Convert tokens to feature vectors using HashingTF.
hashingTF = HashingTF(inputCol="words", outputCol="features", numFeatures=1000)

# Create the Naive Bayes classifier.
# "multinomial" modelType is typically used for text classification.
nb = NaiveBayes(labelCol="indexedLabel", featuresCol="features", modelType="multinomial")

# Build the Pipeline that chains the preprocessing and model stages.
pipeline = Pipeline(stages=[labelIndexer, tokenizer, hashingTF, nb])

# Split the dataset into training and testing sets.
(trainingData, testData) = df.randomSplit([0.7, 0.3], seed=1234)

# Train the model using the pipeline.
model = pipeline.fit(trainingData)

# Use the trained model to make predictions on the test data.
predictions = model.transform(testData)
predictions.select("id", "text", "label", "indexedLabel", "prediction").show()

# Evaluate the accuracy of the model.
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy"
)
accuracy = evaluator.evaluate(predictions)
print(f"Test set accuracy: {accuracy}")

# Stop the SparkSession once done.
spark.stop()
''')
    
def HSWCST():
    print('''
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext  # Get the SparkContext

# Sample text data (simulating a small dataset)
data = [
    "hello world",
    "hello pyspark",
    "pyspark map reduce example",
    "reduce and map are powerful",
]

# Create an RDD (Resilient Distributed Dataset)
rdd = sc.parallelize(data)

# Map Step: Split sentences into words and assign count 1 to each
mapped_rdd = rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1))

# Reduce Step: Sum up occurrences of each word
word_counts = mapped_rdd.reduceByKey(lambda a, b: a + b)

print("")
print("**********************************************")
print("Real-Time Word Count with PySpark Streaming")
print("**********************************************")

# Collect and print results
result = word_counts.collect()
for word, count in result:
    print(f"{word}: {count}")

# Stop Spark session
spark.stop()''')

def HSWORDCOUNT():
    print('''#word count
from pyspark.sql import SparkSession
from pyspark.sql.functions import split,explode,col

spark = SparkSession.builder.appName("Word Count").getOrCreate()

# load the sample text
data = [("hello world",),("Hello how are you",),("Im fine",)]
df = spark.createDataFrame(data,["text"])
df.show()
word_df = df.withColumn("words",explode(split(col("text")," ")))
word_df.show()
print(" - ")
print("**************************")
word_count = word_df.groupBy("words").count().orderBy(col("count").desc())
word_count.show()''')