import pandas as pd 
import os 
import mysql.connector 
mydb = mysql.connector.connect (
    host="localhost", 
    user = "root", 
    passwd= "") 
mycursor = mydb.cursor() 
 
file_path = r"C:\\Users\\Desktop\\file\\"

for filename in os.listdir(file_path): 
    if filename.endswith('.xlsx'):
        df_name = os.path.splitext(filename)[0]
        df = pd.read_excel(os.path.join(file_path, filename))
        globals()[df_name] = df
        print (f"{df_name} is a dataframe")
        
        # Generate CREATE TABLE statement dynamically
        columns = []
        for column in df.columns:
            # Determine the SQL data type
            if pd.api.types.is_integer_dtype(df[column]):
                sql_type = 'INTEGER'
            elif pd.api.types.is_float_dtype(df[column]):
                sql_type = 'REAL'
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                sql_type = 'DATE'
            else:
                sql_type = 'TEXT'  # Default to TEXT for other types
            columns.append(f"{column} {sql_type}")
        
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {df_name} ({', '.join(columns)});\n"
        mycursor.execute("CREATE DATABASE mydatabase")
        mycursor.execute(create_table_sql) 
        print (f"{df_name} table created")
        
        #fill the table 
        # Adjusted SQL QUERY
        QUERY = f"INSERT INTO {df_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))});\n"
        df = df.where(pd.notnull(df), None)

        # Insert data
        Ldf = df.values.tolist()
        for elem in Ldf:
            x = tuple(elem)
            mycursor.execute(QUERY, x)
        print (f"{df_name} table filled ")
        
        #save changes 
        mydb.commit() 

