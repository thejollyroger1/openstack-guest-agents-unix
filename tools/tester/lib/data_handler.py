#

import shelve

#
class DataShelve:
  def load_history(self, path):
    return shelve.open(path)

  def save_history(self, db):
    db.sync()
    db.close()
