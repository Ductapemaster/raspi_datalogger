sql_username = "<username>"
sql_password = "<password>"
sql_database_server = "localhost"
sql_database_name = "datalogger"

sql_database_url = "mysql://{}:{}@{}/{}".format(sql_username, sql_password, sql_database_server, sql_database_name)

influx_username = sql_username
influx_password = sql_password
influx_database_server = "localhost"
influx_database_port = 8086
