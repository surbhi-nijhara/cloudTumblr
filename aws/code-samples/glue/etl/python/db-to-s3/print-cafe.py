print-cafe.py
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

### Print the changed records
cafePrintData = glueContext.create_dynamic_frame_from_options(
    connection_type="s3", 
    format="parquet",
    connection_options = {"paths": ["s3://cafe-poc/cafe_FL_PoC/"]}
   
    )
cafePrintData_SDF = dimcafePrintData.toDF()
cafePrintData_SDF.createOrReplaceTempView("cafe_new_view")
cafe_df = spark.sql("""
SELECT 
*
From cafe_new_view as p
WHERE p.cafeKey IN (2642,2645,2647)

""")
#-WHERE p.cafeKey in (2642,2644,2645,2646)


print(" S3 cafe Count: ", dimcafe_df.count())
cafe_df.show(truncate = False)