from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """
    User defined operator to load data into Dimension tables available in Redshit data warehouse.

         redshift_conn_id: Redshift ConnectionID with Airflow,
         table: Staging table name in Redshift,
         sql_query: Query to fetch data from Staging tables
    
    """
    
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 sql_query="",
                 append_to_table = False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.append_to_table = append_to_table

    def execute(self, context):
        self.log.info('LoadDimensionOperator called !!')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.append_to_table:
            sql_temp = """
            INSERT INTO {current_table}
            {current_query}
            """
            final_sql = sql_temp.format(self.table, self.sql_query)
            
            self.log.info("Insertion of records with no truncate !!")
        else:
            sql_temp = """
            TRUNCATE TABLE {current_table};
            INSERT INTO {current_table}
            {current_query}
            """
            final_sql = sql_temp.format(current_table=self.table, current_query=self.sql_query)
            
            self.log.info("Truncated Redshift table before insertion records !!")

        redshift.run(final_sql)
