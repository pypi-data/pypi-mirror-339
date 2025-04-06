import os
import sys
import pandas as pd
import numpy as np
import re
from dateutil.parser import parse as date_parse


def infer_sql_type_from_value(value:str):
    if value == "":     return "EMPTY"
    if value == None:   return "EMPTY"
    if value == np.nan: return "EMPTY"
    if value is pd.NaT: return "EMPTY"

    # Regular expressions for different data types
    int_regex           = re.compile(r'^-?\d+$')
    int_comma_regex     = re.compile(r'^-?\d+(,\d+)+$')
    double_regex        = re.compile(r'^-?\d*\.\d+$')
    double_comma_regex  = re.compile(r'^-?\d+(,\d+)+\.\d+$')
    bool_regex          = re.compile(r'^(True|False|true|false)$')

    # Check for each data type
    if int_regex.match(value):              return "INTEGER"
    elif int_comma_regex.match(value):      return "INTEGER"
    elif double_regex.match(value):         return "DOUBLE"
    elif double_comma_regex.match(value):   return "DOUBLE"
    elif bool_regex.match(value):           return "BOOLEAN"

    try:
        parsed = date_parse(value)
        # Decide DATE or DATETIME based on presence of time
        if parsed.time().hour == 0 and parsed.time().minute == 0 and parsed.time().second == 0:
            return "DATE"
        else:
            return "DATETIME"
    except (ValueError, OverflowError):
        pass
    
    try:
        value.encode('ascii')  # Try encoding as ASCII
    except UnicodeEncodeError:
        return "NVARCHAR"  # If it fails, it's a Unicode string
    
    return "VARCHAR"    # Default to VARCHAR

def determine_final_type(types:list[str], column_name:str=None):
    if "NVARCHAR" in types: return "NVARCHAR"
    if "VARCHAR" in types:  return "VARCHAR"
    if "DATETIME" in types: return "DATETIME"
    if "DATE" in types:     return "DATE"
    if "DOUBLE" in types:    return "DOUBLE"
    if "INTEGER" in types:  return "INTEGER"
    if "BOOLEAN" in types:  return "BOOLEAN"
    return "VARCHAR"  # Default if no types are identified

def clean_value_with_type(value, column_type:str="VARCHAR", pd_np_nulls:list[object]=[None, np.nan, pd.NaT, "NULL", "None", "nan", "NaN"]):
    # Returns values with the quotes also for easy insert use

    if value in pd_np_nulls:
        return f"NULL"
    if value is pd.NaT: 
        return f"NULL"

    if column_type in ["NVARCHAR", "VARCHAR"]:
        value = str(value).replace("'", "''")
        return f"'{value}'"

    if column_type in ["DOUBLE", "INTEGER"]:
        value = str(value).replace(",", "").replace("'", "").replace('"', "")
        return f"{value}"
                
    if column_type in ["DATETIME", "DATE"]:
        return f"'{value}'"
        
    if column_type == "BOOLEAN":
        if value == True or str(value).upper() == "TRUE":
            return f"TRUE"
        if value == False or str(value).upper() == "FALSE":
            return f"FALSE"
    
    return f"NULL"


