from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    User defined operator to check data quality in tables available in Redshit data warehouse.

         redshift_conn_id: Redshift ConnectionID with Airflow,
         sql_query: The query to run on table in Redshift data warehouse
         expectedResult: Expected result of the query
    """
    
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 dq_checks = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.dq_checks = dq_checks

    def execute(self, context):
        self.log.info('DataQualityOperator called !!')
        
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for dq_check in self.dq_checks:
            check_sql = dq_check["check_sql"] 
            expected_result = dq_check["expected_result"]
            records = redshift_hook.get_records(check_sql)
            
            if records[0][0] == expected_result:
                self.log.info("Data quality succeeded for query: " + check_sql)
            else:
                raise ValueError("Null values observed in data for query: " + check_sql)