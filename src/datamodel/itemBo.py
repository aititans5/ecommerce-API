from src.database import items

class itemcls(object):
    def __init__(self):
        self.categoryid = None
        self.itemid = None
        self.qty = None
        self.imagename = None
        self.price = None
        self.itemname = None

    def __init__(self,categoryid, itemid, qty, imagename, price, itemname):
        self.categoryid = categoryid
        self.itemid = itemid
        self.qty = qty
        self.imagename = imagename
        self.price = price
        self.itemname = itemname

    def setObjFromOrMObj(self, ormitem: items):
        self.itemid = ormitem.itemid
        self.categoryid = ormitem.categoryid
        self.qty = ormitem.qty
        self.imagename = ormitem.imagename
        self.price = ormitem.price
        self.itemname = ormitem.itemname


