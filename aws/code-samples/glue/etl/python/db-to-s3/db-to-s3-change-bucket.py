db-to-s3-change-bucket.py

#### This script gets the changes from SQL <table>_refresh_temp table to S3 <table>_refresh bucket
#### Assume table name as cafe
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame

import boto3


## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "cafepoc", table_name = "dbo_cafe_refresh_temp", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "cafepoc", table_name = "dbo_cafe_refresh_temp", transformation_ctx = "datasource0")


## @type: ApplyMapping
## @args: [mapping = [("cafedivision", "string", "cafedivision", "string"), ("cafekey", "int", "cafekey", "int"),("cafeupdatedate", "timestamp", "cafeupdatedate", "date"), ("cafeshname", "string", "cafeshname", "string"), ("customerkey", "int", "customerkey", "int"), ("cafeid", "int", "cafeid", "int"), ("caferegion", "string", "caferegion", "string"),  ("cafename", "string", "cafename", "string"),("Op", "varchar", "Op", "varchar")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]

#print("Count: ", datasource0.count())
#datasource0.printSchema()
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("cafedivision", "string", "cafedivision", "string"), ("cafekey", "int", "cafekey", "int"),("cafeupdatedate", "timestamp", "cafeupdatedate", "date"), ("cafeshname", "string", "cafeshname", "string"), ("customerkey", "int", "customerkey", "int"), ("cafeid", "int", "cafeid", "int"), ("caferegion", "string", "caferegion", "string"),  ("cafename", "string", "cafename", "string"),("Op", "varchar", "Op", "varchar")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]

### = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://cafe_poc/cafe_refresh"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]


cafe_df = resolvechoice2.toDF()

cafe_df.createOrReplaceTempView("cafe_temp_table")

refresh_df = spark.sql("""
SELECT 
CafeKey,
CustomerKey,
CafeName,
CafeDivision,
CafeRegion,
CafeSHName,
CafeID,
CafeUpdateDate,
Op
From cafe_temp_table
""")

print(" refresh Count: ", refresh_df.count())

final_df = DynamicFrame.fromDF(refresh_df.repartition(1), glueContext, "final_df" )

#spark_df = final_df.toDF().withColumn("changeOperation", lit("I"))
spark_df = final_df.toDF().withColumn("etlTimeStamp", current_date())
Newfinal_df = DynamicFrame.fromDF(spark_df.repartition(1), glueContext, "Newfinal_df" )


s3cafeRefreshSink_df = glueContext.write_dynamic_frame.from_options(frame = Newfinal_df, connection_type = "s3", connection_options = {"path": "s3://cafe_poc/cafe_refresh/"}, format = "parquet", transformation_ctx = "datasink4")
job.commit()


### s3 copy from refresh to full can be done as follows, if need be

'''
bucketname = "cafe-poc"
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucketname)
source = "cafe_refresh/"
target = "cafe-full"

for key in bucket.list():
    print key.name()


for obj in my_bucket.objects.filter(Prefix=source):
    source_filename = (obj.key).split('/')[-1]
    copy_source = {
        'Bucket': bucketname,
        'Key': obj.key
    }
    target_filename = "{}/{}".format(target, source_filename)
    s3.meta.client.copy(copy_source, bucketname, target_filename)

'''
job.commit()

