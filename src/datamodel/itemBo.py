from src.database import items

class itemcls(object):
    def __init__(self):
        self.categoryid = None
        self.itemid = None
        self.qty = None
        self.imagename = None
        self.price = None
        self.itemname = None

    def setObjFromOrMObj(self, ormitem: items):
        self.itemid = ormitem.itemid
        self.categoryid = ormitem.categoryid
        self.qty = ormitem.qty
        self.imagename = ormitem.imagename
        self.price = ormitem.price
        self.itemname = ormitem.itemname


