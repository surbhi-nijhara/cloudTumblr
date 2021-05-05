s3-change-to-s3-full.py
###This script merges the changes from cafe_refresh to cafe
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import *
from awsglue.dynamicframe import DynamicFrame

import boto3
import pandas as pd
import numpy as np

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


### create temp view of S3 cafe dynamic frame
cafeFLData = glueContext.create_dynamic_frame_from_options(
    connection_type="s3", 
    format="parquet",
    connection_options = {"paths": ["s3://cafe/cafe_FL_PoC"]}
   
    )
cafeFLData_SDF = cafeFLData.toDF()
print(" S3 cafeFLData_SDF Count: ", cafeFLData_SDF.count())
cafeFLData_SDF.createOrReplaceTempView("cafe_temp_view")

cafeRefreshData = glueContext.create_dynamic_frame_from_options(
    connection_type="s3", 
    format="parquet",
    connection_options = {"paths": ["s3://cafe_refresh"]}
   
    )
cafeRefreshData_SDF = cafeRefreshData.toDF()
cafeRefreshData_SDF.createOrReplaceTempView("cafe_refresh_temp_view")


######################  INSERTION  #######################################
#print('Starting to INSERT')
df_insert = spark.sql("""
SELECT 
a.cafeKey,
a.CustomerKey,
a.cafeName,
a.cafeDivision,
a.cafeRegion,
a.cafeshname,
a.cafeID,
a.cafeUpdateDate
FROM cafe_temp_view a

UNION

SELECT 
b.cafeKey,
b.CustomerKey,
b.cafeName,
b.cafeDivision,
b.cafeRegion,
b.cafeshname,
b.cafeID,
b.cafeUpdateDate
FROM cafe_refresh_temp_view b

WHERE b.Op = 'I'
""") 

print(" S3 cafe Count after INSERT: ", df_insert.count())

df_insert.createOrReplaceTempView("cafe_print_view")
cafe_df = spark.sql("""
SELECT 
*
From cafe_print_view as p
WHERE p.cafekey in (2642,2645,2647)

""")
cafe_df.show(truncate = False)

######################For DELETION,  Now take df_insert data frame and create a temp view #######################################
print('Starting to DELETE')
df_insert.createOrReplaceTempView("cafe_temp_view")
df_delete = spark.sql("""
SELECT 
a.cafeKey,
a.CustomerKey,
a.cafeName,
a.cafeDivision,
a.cafeRegion,
a.cafeshname,
a.cafeID,
a.cafeUpdateDate

FROM cafe_temp_view a

WHERE a.cafeKey NOT IN
(SELECT b.cafeKey FROM cafe_refresh_temp_view b WHERE b.Op ='D')
""") 
print(" S3 cafe Count after DELETE: ", df_delete.count())
df_delete.createOrReplaceTempView("cafe_print_view")
cafe_df = spark.sql("""
SELECT 
*
From cafe_print_view as p
WHERE p.cafekey in (2642,2645,2647)

""")
cafe_df.show(truncate = False)


#####################For UPDATE ############################################
print('Starting to UPDATE')
cafeRefreshData_SDF.createOrReplaceTempView("cafe_refresh_temp_view")

cafeRefreshData_8cols_SDF = spark.sql("""
SELECT 
a.cafeKey,
a.CustomerKey,
a.cafeName,
a.cafeDivision,
a.cafeRegion,
a.cafeshname,
a.cafeID,
a.cafeUpdateDate
FROM cafe_refresh_temp_view as a
WHERE a.Op = 'U'
""")

#print(" cafeRefreshData_8cols_SDF: ", cafeRefreshData_8cols_SDF.count())
#cafeRefreshData_8cols_SDF.show(truncate = False)

pandasDFcafe= df_delete.toPandas()
pandasDFRefresh = cafeRefreshData_8cols_SDF.toPandas()

### To oprevent from ints to be converetd into floats

dtypes = pandasDFRefresh.dtypes.to_dict()
#print ('\ndtypes BEFORE update:\n%s' % (dtypes))
tgt_to_src_convert_dict = {}
src_to_tgt_convert_dict = {}
for col_name, typ in dtypes.items():
    if typ == 'int32' or typ == 'int64':
        src_to_tgt_convert_dict[col_name] = object
        tgt_to_src_convert_dict[col_name] = typ

# Let's convert all ints to objects
pandasDFRefresh = pandasDFRefresh.astype(src_to_tgt_convert_dict)

#pandasDFRefresh.set_option('display.max_columns', None)
#print("pandasDFRefresh:",pandasDFRefresh)

'''
mask = pandasDFcafe['cafeKey'] == 2645
# new dataframe with selected rows
df_new = pd.DataFrame(pandasDFcafe[mask])
print("pandasDFcafe:",df_new)  

mask = pandasDFRefresh['cafeKey'] == 2645
# new dataframe with selected rows
df_new = pd.DataFrame(pandasDFRefresh[mask])
print("pandasDFRefresh",df_new)
'''
### Index is needed to update the correct record, else the 0th index onwards aka first in order records are updated.
pandasDFcafe.set_index('cafeKey',inplace=True)
pandasDFRefresh.set_index('cafeKey', inplace=True)

pandasDFcafe.update(pandasDFRefresh, overwrite=True) 

pandasDFcafe.reset_index(inplace=True)
# Let's now revert the object type back to int for all respective columns
# for which we converted to object
pandasDFcafe = pandasDFcafe.astype(tgt_to_src_convert_dict)

#print ('\ndtypes after update:\n%s\n%s' % (pandasDFcafe.dtypes, pandasDFRefresh.dtypes))
'''
mask = pandasDFcafe['cafeKey'] == 2645
# new dataframe with selected rows
df_new = pd.DataFrame(pandasDFcafe[mask])
print("pandasDFcafe after",df_new)
'''
# Create a Spark DataFrame from a pandas DataFrame using Arrow
# Enable Arrow-based spark configuration
#spark.conf.set(“spark.sql.execution.arrow.enabled”, “true”)
sdf_update = spark.createDataFrame(pandasDFcafe)
print(" S3 cafe Count after UPDATE: ", sdf_update.count())

####FINAL FRAME PRINT
sdf_update.createOrReplaceTempView("cafe_print_update_view")
cafe_df = spark.sql("""
SELECT 
*
From cafe_print_update_view as p
WHERE p.cafekey in (2642,2645,2647)

""")
cafe_df.show(truncate = False)

#append (which is not that is needed)
#cafe_final_df = DynamicFrame.fromDF(df_update.repartition(20), glueContext, "cafe_final_df" )
#s3cafeRefreshSink_df = glueContext.write_dynamic_frame.from_options(frame = cafe_final_df, connection_type = "s3", connection_options = {"path": "s3://cafe-poc/cafe"}, format = "parquet", transformation_ctx = "s3cafeRefreshSink_df")

#Overwrite
spark.conf.set('spark.sql.sources.partitionOverwriteMode','dynamic')
sdf_update=sdf_update.coalesce(20)
sdf_update.write.mode('overwrite').parquet('s3://cafe-poc/cafe_FL_PoC/')

job.commit()







    

