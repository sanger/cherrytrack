import cherrytrack.config.test as config
import sqlalchemy

create_engine_string = config.SQLALCHEMY_DATABASE_URI

sql_engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, pool_recycle=3600)

create_db = """
CREATE DATABASE IF NOT EXISTS `psd_cherrytrack_test` /*!40100 DEFAULT CHARACTER SET latin1 */;
"""

drop_table_automation_systems = """
DROP TABLE IF EXISTS `event_warehouse_test`.`automation_systems`;
"""

create_table_automation_systems = """
CREATE TABLE IF NOT EXISTS `automation_systems` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT 'unique database identifier for this row',
  `automation_system_name` VARCHAR(255) UNIQUE NOT NULL COMMENT 'the name for the workcell as used by the lab staff',
  `automation_system_manufacturer` VARCHAR(255) NOT NULL COMMENT 'used to distinguish groups of workcells supplied by different manufacturers',
  `liquid_handler_serial_number` VARCHAR(255) NOT NULL COMMENT 'the serial number of the liquid handler on the workcell',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT 'the datetime when this row was created in the database',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT 'the datetime when this row was updated in the database',
  PRIMARY KEY (`id`)
) COMMENT='This table contains one row for each automation system (or workcell).'
ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
"""

with sql_engine.connect() as connection:
    print("*** Creating database ***")
    connection.execute(create_db)

    print("*** Dropping table automation_systems ***")
    connection.execute(drop_table_automation_systems)

    print("*** Creating table automation_systems ***")
    connection.execute(create_table_automation_systems)

print("Done")
