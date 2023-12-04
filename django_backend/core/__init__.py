from pathlib import Path
import pymysql


pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent