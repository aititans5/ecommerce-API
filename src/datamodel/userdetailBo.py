from src.database import userdetail


class userdetailcls(object):
    def __init__(self):
        pass


    def setObjFromOrMObj(self, ormuserdetail: userdetail):
        self.userid = ormuserdetail.userid
        self.name = ormuserdetail.name
        self.username = ormuserdetail.username
        self.email = ormuserdetail.email
        self.password = None
        self.activeuser = ormuserdetail.activeuser
        self.created_at = ormuserdetail.created_at
        self.updated_at = ormuserdetail.updated_at

