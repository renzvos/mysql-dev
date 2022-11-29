import os

def getvars():
    dev = False
    config = {}
    if dev:
        config["dev"] = True
        config["config_log_everysteps"]  = "true"
        config["config_datadir"] = "D:\\Works\\mysql-dev\\automation\\data"
        config["config_structuredir"] = "D:\\Works\\mysql-dev\\automation\\structure"

        config["startup_restore_structure"]  = "true"
        config["startup_restore_structure_source"]  = "dropbox"
        config["startup_restore_structure_dropbox_access"]  = "asdfsdf"
        config["startup_restore_structure_dropbox_dir"]  = "/mysqlserver-one/structure.sql"
        config["startup_restore_data"]  = "true"
        config["startup_restore_data_source"]  = "dropbox"
        config["startup_restore_data_dropbox_access"]  = "asdfasdf"
        config["startup_restore_data_dropbox_dir"]  = "/mysqlserver-one/data"
        config["backup_data_one_destination"]  = "dropbox"
        config["backup_data_one_dropbox_access"]  = "asdfasdf"
        config["backup_data_one_dropbox_dir"]  = "/mysqlserver-one/data"
        config["backup_data_interval"]  = "86400"
        config["config_log_everysteps"]  = "true"

    else:
        config["dev"] = False
        config["config_datadir"] = "/home/data"
        config["config_structuredir"] = "/home/structure"
        for item, value in os.environ.items():
            config[item] = value

    return config
