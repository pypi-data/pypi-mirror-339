#=============================================================#
###  CREATED AT     : 29 FEBRUARI 2024                      ###
###  UPDATED AT     : 09 APRIL 2025                         ###
###  COPYRIGHT      : ANDRI ARIYANTO                        ###
###  DESCRIPTION    : Module untuk pembuatan spark session  ###
#=============================================================#

import os
import sys
import contextlib

@contextlib.contextmanager
def suppress_native_output():
  with open(os.devnull, 'w') as devnull:
    old_stdout_fd = os.dup(1)
    old_stderr_fd = os.dup(2)
    os.dup2(devnull.fileno(), 1)
    os.dup2(devnull.fileno(), 2)
    try:
      yield
    finally:
      os.dup2(old_stdout_fd, 1)
      os.dup2(old_stderr_fd, 2)

#=============================================================#
      
from pyspark.sql import SparkSession

def sparkSession(
  appname="Bribrain Packages SparkSession", 
  executor="small", 
  instances=2, 
  cores=2, 
  memory=4, 
  overhead=2, 
  verbose=False,
  extra_configs=None):
  """Membuat spark session yang dapat digunakan untuk proses data engineering

  Args:
      appname (str): Nama dari spark session
          (default is Bribrain Packages SparkSession)
      executor (str): Standard resource yang dapat dipilih untuk spark session 
          (optional is small, medium, high, custom)
          (default is small)
          (notes is small (2,2,4,2), medium (4,4,6,2), high (6,6,8,4))
      instances (int): Config untuk menentukan instance spark session
          (default is 2)
      cores (int): Config untuk menentukan cores spark session
          (default is 2)
      memory (int): Config untuk menentukan memory spark session
          (default is 4)
      overhead (int): Config untuk menentukan overhead spark session
          (default is 2)
      verbose (bool): Config untuk menampilkan console progress
          (default is False)
      extra_configs (dict): Config untuk menambahkan additional spark config
          (default is None)
          
  Returns:
      pyspark.sql.session.SparkSession: Spark session untuk proses data engineering
  """
  
  # Define resource configuration
  if   executor=="small":
    config = [2, 2, 4, 2]
  elif executor=="medium":
    config = [4, 4, 6, 2]
  elif executor=="high":
    config = [6, 6, 8, 4]
  elif executor=="custom":
    config = [instances, cores, memory, overhead]
  else:
    raise ValueError(f"Unknown executor type: {executor}")

  executor_instances, executor_cores, executor_memory, memory_overhead = config
  verbose_str = "true" if verbose else "false"

  # Start building SparkSession
  builder = (
    SparkSession.builder
    .appName(appname)
    .config("spark.sql.crossJoin.enabled", "true")
    .config("spark.dynamicAllocation.enabled", "false")
    .config("spark.executor.instances", f"{executor_instances}")
    .config("spark.executor.cores", f"{executor_cores}")
    .config("spark.executor.memory", f"{executor_memory}g")
    .config("spark.yarn.executor.memoryOverhead", f"{memory_overhead}g")
    .config("spark.sql.broadcastTimeout", "36000")
    .config("spark.ui.showConsoleProgress", verbose_str)
    .config("spark.network.timeout", "300s")
  )
  
  # Add extra configs if provided
  if extra_configs:
    for key, value in extra_configs.items():
      builder = builder.config(key, value)

  with suppress_native_output():
    # Enable Hive and create session
    spark = builder.enableHiveSupport().getOrCreate()

    
  return spark


#=============================================================#

import zipfile

def template():
  """Membuat template foldering yang digunakan untuk proses data engineering

  Args:
      -
    
  Returns:
      -
  """
  
  res = os.system("hdfs dfs -get /tmp/production/bribrain/template.zip")

  with zipfile.ZipFile("/home/cdsw/template.zip", 'r') as zip_ref:
      zip_ref.extractall("/home/cdsw")

  os.remove("/home/cdsw/template.zip")
