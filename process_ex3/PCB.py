class PCB(object):
    def __init__(self, name='job'):
        self.__name = name # 进程名
        # self.__size = size

    def gatherAttrs(self):
        attrs = []
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return " ".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())

    def getName(self):
        return self.__name

    def setName(self, pcb_name):
        self.__name = pcb_name
