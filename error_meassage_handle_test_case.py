def clean_up_spark_logs(error_logs):
    # Define common error patterns
    error_patterns = {
        # General Python Errors
        "IndentationError": r"IndentationError:.*",
        "SyntaxError": r"SyntaxError:.*",
        "TypeError": r"TypeError:.*",
        "ValueError": r"ValueError:.*",
        "KeyError": r"KeyError:.*",
        "AttributeError": r"AttributeError:.*",
        "IndexError": r"IndexError:.*",
        "ModuleNotFoundError": r"ModuleNotFoundError:.*",
        "ImportError": r"ImportError:.*",
        "TimeoutError": r"TimeoutError:.*",
        "IOError": r"IOError:.*|OSError:.*",
        "DataTypeMismatchError": r"cannot resolve.*due to data type mismatch.*",

        # PySpark Errors
        "PySpark Task Failure": r"Task \d+ in stage \d+\.\d+ failed.*",
        "PySpark OutOfMemoryError": r"OutOfMemoryError.*",
        "PySpark GC Overhead": r"GC overhead limit exceeded.*",
        "PySpark Serialization Error": r"NotSerializableException.*|SerializationException.*",
        "PySpark Data Skew": r"Task \d+ took too long.*",
        "PySpark Stage Failure": r"Stage \d+ failed.*",
        "PySpark File System Error": r"(FileNotFoundException|AccessDeniedException).*",
        "PySpark Iceberg Error": r"org\.apache\.iceberg\.exceptions\..*",
        "PySpark Resource Allocation Error": r"Error while allocating resources.*",
        "PySpark Missing Columns": r"cannot resolve.*given input columns.*",

        # Boto3/AWS Errors
        "Boto3 NoCredentialsError": r"NoCredentialsError:.*",
        "Boto3 PartialCredentialsError": r"PartialCredentialsError:.*",
        "Boto3 ClientError": r"botocore\.exceptions\.ClientError:.*",
        "Boto3 EndpointConnectionError": r"EndpointConnectionError:.*",
        "AWS Access Denied": r"AccessDenied:.*",
        "AWS Resource Not Found": r"ResourceNotFoundException:.*",
        "AWS ThrottlingException": r"ThrottlingException:.*",
        "AWS Internal Server Error": r"InternalServerError:.*",

        # Airflow Errors (MWAA)
        "Airflow DAG Import Error": r"airflow\.exceptions\.DagImportException:.*",
        "Airflow Task Timeout": r"Task timed out.*",
        "Airflow Execution Error": r"airflow\.exceptions\.AirflowException:.*",
        "Airflow Dependency Failed": r"Upstream task.*failed.*",
        "Airflow Operator Error": r"airflow\.exceptions\.AirflowSkipException:.*",
        "Airflow Connection Error": r"airflow\.exceptions\.AirflowConnectionException:.*",

        # PyMySQL Errors
        "PyMySQL OperationalError": r"pymysql\.err\.OperationalError:.*",
        "PyMySQL IntegrityError": r"pymysql\.err\.IntegrityError:.*",
        "PyMySQL ProgrammingError": r"pymysql\.err\.ProgrammingError:.*",
        "PyMySQL Connection Error": r"pymysql\.err\.InterfaceError:.*",

        # datetime Errors
        "Datetime ValueError": r"ValueError: invalid datetime format.*",
        "Datetime OverflowError": r"OverflowError:.*",

        # SparkSession Errors
        "SparkSession Resource Error": r"Resource allocation failed.*",
        "SparkSession Initialization Error": r"Failed to initialize SparkSession.*",
        "SparkSession Missing Config": r"KeyError:.*",

        # Miscellaneous Patterns
        "JSON Parse Error": r"JSONDecodeError:.*",
        "File Read Error": r"FileNotFoundError:.*",
        "Permission Error": r"PermissionError:.*",
        "SQL Syntax Error": r"pymysql\.err\.ProgrammingError:.*syntax error.*",
        "NUM_COLUMNS_MISMATCH": r"\[NUM_COLUMNS_MISMATCH\].*",

        # EMR and Distributed System Errors
        "EMR Cluster Termination": r"Cluster termination initiated.*",
        "HDFS Disk Error": r"org\.apache\.hadoop\.fs\.DiskCheckerException.*",
        "EMR Job Failure": r"Job failed with exit code.*",
        "YARN OutOfMemory": r"Container killed by YARN for exceeding memory limits.*",
        "YARN Resource Manager Error": r"YARN ResourceManager.*",
        "Shuffle Read/Write Error": r"Failed to allocate shuffle buffer.*",
        "Driver Container Failure": r"Driver container exited with.*",

        # Java and JVM Errors
        "Java Class Not Found": r"java\.lang\.ClassNotFoundException:.*",
        "JVM OutOfMemoryError": r"java\.lang\.OutOfMemoryError:.*",
        "JVM StackOverflowError": r"java\.lang\.StackOverflowError:.*",
        "JVM Fatal Error": r"Java HotSpot.*fatal.*",
    }

    results = ''
    matched = False

    # Process each error pattern
    for error_type, pattern in error_patterns.items():
        matches = re.findall(pattern, error_logs, re.MULTILINE)
        if matches:
            matched = True
            cleaned_messages = [
                re.sub(r"Caused by: [^:]+:\s*", "", match).strip()
                if "Caused by:" in match
                else match.strip()
                for match in matches
            ]
            results = cleaned_messages[0]

    # Handle unmatched logs
    if not matched:
        # If no matches were found, capture all log messages
        logs_lines = error_logs.splitlines()
        unmatched_logs = [line.strip() for line in logs_lines if line.strip()]

        results = unmatched_logs[0] or ["No recognizable error patterns found."]

    return results