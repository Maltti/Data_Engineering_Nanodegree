import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, select_number_rows_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()
        
def get_results(cur, conn):
    """
    Get the number of rows stored into each table
    """
    tables_rowsCount=""
    for query in select_number_rows_queries:
        print('Running ' + query)
        cur.execute(query)
        results = cur.fetchone()

        for row in results:
            print("   ", row)
             #tables_rowsCount= tables_rowsCount +str(query)+"  " +str(row) +'\n'
        #print(tables_rowsCount)
        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    print ("load_staging_tables")
    load_staging_tables(cur, conn)
    print ("")
    print ("load_insert_tables")
    insert_tables(cur, conn)
    print ("")
    get_results(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()