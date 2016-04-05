import MySQLdb

CONFIG_FILE="/var/www/monitor/config.py"

class database(object):
  def __init__(self):
    config = {}
    execfile(CONFIG_FILE,config)
    while not self._connect(config): print("Retrying database connection")

  def _connect(self,config):
    try:
      self.db = MySQLdb.connect(config["host"],config["user"],config["password"],config["database"])
      self.db.autocommit(True)
      return True
    except:
      print("Cannot connect to MYSQL")
      return False

  def insert(self,txt):
    dbc = self.db.cursor()
    try:
      dbc.execute("insert into " + txt)
      dbc.close()
      self.db.commit()
    except Exception as e:
      print(e)
      return False
    return True
  
  def update(self,txt):
    dbc = self.db.cursor()
    try:
      dbc.execute("update from " + txt)
      dbc.close()
      self.db.commit()
    except Exception as e:
      print(e)
      return False
    return True
   
  def select(self,txt):
    dbc = self.db.cursor()
    try:
      dbc.execute("select " + txt)
      result = dbc.fetchall()
    except Exception as e:
      print(e)
      result = None
    dbc.close()
    return result
