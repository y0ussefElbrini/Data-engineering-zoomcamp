from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.common.time import Duration


def create_session_aggregated_sink(t_env):
    table_name = 'longest_trip_streak'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            pickup_location INT,
            dropoff_location INT,
            trip_count BIGINT,
            PRIMARY KEY (pickup_location, dropoff_location) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name


def create_green_trips_source_kafka(t_env):
    table_name = "green_trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime TIMESTAMP(3),
            lpep_dropoff_datetime TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            WATERMARK FOR lpep_dropoff_datetime AS lpep_dropoff_datetime - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name


def session_window_aggregation():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(3)

    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = TableEnvironment.create(environment_settings=settings)

    try:
        # Create Kafka source table
        source_table = create_green_trips_source_kafka(t_env)
        aggregated_table = create_session_aggregated_sink(t_env)

        # Perform session window aggregation
        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            PULocationID AS pickup_location,
            DOLocationID AS dropoff_location,
            COUNT(*) AS trip_count
        FROM TABLE(
            SESSION(
                TABLE {source_table},
                DESCRIPTOR(lpep_dropoff_datetime),
                INTERVAL '5' MINUTE
            )
        )
        GROUP BY PULocationID, DOLocationID;
        """).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))


if __name__ == '__main__':
    session_window_aggregation()
