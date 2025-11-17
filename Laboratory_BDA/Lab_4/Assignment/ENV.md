# BDA Lab 4 — Environment & Configuration

## System Information
- Python: 3.10.19
- Spark: 4.0.1
- PySpark: 4.0.1
- Java: openjdk version "21.0.8" 2025-07-15 LTS
- OS: Windows-10-10.0.26100-SP0
- Machine: Remi

## Spark Configuration
- spark.app.id = local-1762707962294
- spark.app.name = BDA-Lab04
- spark.app.startTime = 1762707961498
- spark.app.submitTime = 1762707960963
- spark.driver.extraJavaOptions = -Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true
- spark.driver.host = Remi.mshome.net
- spark.driver.port = 59742
- spark.executor.extraJavaOptions = -Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true
- spark.executor.id = driver
- spark.hadoop.fs.s3a.vectored.read.max.merged.size = 2M
- spark.hadoop.fs.s3a.vectored.read.min.seek.size = 128K
- spark.master = local[*]
- spark.rdd.compress = True
- spark.serializer.objectStreamReset = 100
- spark.sql.artifact.isolation.enabled = false
- spark.sql.session.timeZone = UTC
- spark.sql.shuffle.partitions = 4
- spark.sql.warehouse.dir = file:/C:/Users/rerel/OneDrive/Bureau/Esiee/Esiee/E5/BDA/Lab_4/Assignment/spark-warehouse
- spark.submit.deployMode = client
- spark.submit.pyFiles = 
- spark.ui.showConsoleProgress = true

## Data Paths
- BASE_DIR: C:\Users\rerel\OneDrive\Bureau\Esiee\Esiee\E5\BDA\Lab_4\Assignment
- DATA_ROOT: C:\Users\rerel\OneDrive\Bureau\Esiee\Esiee\E5\BDA\Lab_4\Assignment\data
- OUTPUT_ROOT: C:\Users\rerel\OneDrive\Bureau\Esiee\Esiee\E5\BDA\Lab_4\Assignment\outputs
- TAXI_DATA_PATH: C:\Users\rerel\OneDrive\Bureau\Esiee\Esiee\E5\BDA\Lab_4\Assignment\data\taxi-data

## Reproducibility Notes
- All queries use deterministic data sources (Parquet, CSV with fixed schema)
- Timezone: UTC (hardcoded in SparkSession)
- Shuffle partitions: 4 (hardcoded for consistency)
- Output format: CSV with headers (deterministic column order)
