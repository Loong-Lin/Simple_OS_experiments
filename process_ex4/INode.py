class FileName(object):
    def __init__(self, name=None):
        self.__name = name
        self.next = None # 指向该文件对应的i结点盘块的指针

    def getName(self):
        return self.__name

    def gatherAttrs(self):
        attrs = []

        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())


class INode(object):
    def __init__(self, date=None, ftype=2, size=0, extended_name=None, index_block=None):
        self.__date = date  # 文件最近的存取、修改时间
        self.__ftype = ftype # 文件类型, 1为文件，2位目录，0位已删除的目录项
        self.__size = size # 文件大小
        self.__extended_name = extended_name # 扩展名，目录没有扩展名
        self.__index_block = index_block  # 索引块号

    def gatherAttrs(self):
        attrs = []

        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))

        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())

    def getFtype(self):
        return self.__ftype

    def setFtype(self, ftype):
        self.__ftype = ftype

    def getIndexBlock(self):
        return self.__index_block

    def getSize(self):
        return self.__size

    def getDate(self):
        return self.__date

    def getExtendedName(self):
        return self.__extended_name

if __name__ == '__main__':
    a = FileName('A')
    b = INode()
    print(a,"\t", b)