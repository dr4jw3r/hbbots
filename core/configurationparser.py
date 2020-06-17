import configparser

def readconfig():
    cp = configparser.ConfigParser()
    cp.read("./sample_config.ini")
    return cp