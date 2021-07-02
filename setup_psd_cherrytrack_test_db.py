import cherrytrack.config.test as config
import sqlalchemy

create_engine_string = config.SQLALCHEMY_DATABASE_URI

sql_engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, pool_recycle=3600)

create_db = """
CREATE DATABASE IF NOT EXISTS `psd_cherrytrack_test` /*!40100 DEFAULT CHARACTER SET latin1 */;
"""

with sql_engine.connect() as connection:
    print("*** Creating database ***")
    connection.execute(create_db)

print("Done")
