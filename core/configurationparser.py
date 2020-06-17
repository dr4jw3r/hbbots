import configparser

def readconfig():
    cp = configparser.ConfigParser()
    cp.read("./config.ini")
    return cp