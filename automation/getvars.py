import os

def getvars():
    dev = False
    config = {}
    if dev:
        config["config_log_everysteps"]  = "true"
        config["config_datadir"] = "D:\\Works\\mysql-dev\\automation\\data"
    else:
        config["config_datadir"] = "/home/data"
        for item, value in os.environ.items():
            config[item] = value

    return config
