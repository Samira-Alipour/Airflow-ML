params = {
    "db_engine": "postgresql+psycopg2://airflow:airflow@postgres/airflow",
    "db_schema": "public",
    "db_experiments_table": "experiments1",
    "db_batch_table": "batch_data",
    "test_split_ratio": 0.3,
    "cv_folds": 5,
    "logreg_maxiter": 1000
}   