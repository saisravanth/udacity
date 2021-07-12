from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
    User defined operator to load data into Fact table available in Redshit data warehouse.

         redshift_conn_id: Redshift ConnectionID with Airflow,
         table: Staging table name in Redshift,
         sql_query: Query to fetch data from Staging tables
    
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
    
    def execute(self, context):
        self.log.info('LoadFactOperator called !!')
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("Load data into fact table in Redshift")
        final_sql = f"""
            INSERT INTO {self.table}
            {self.sql_query}
        """
        redshift_hook.run(final_sql)