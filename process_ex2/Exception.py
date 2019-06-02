class BackError(Exception):
    def __init__(self,backInfo):
        super().__init__(self) #初始化父类
        self.backinfo=backInfo
    def __str__(self):
        return "返回上一级 " + self.backrinfo