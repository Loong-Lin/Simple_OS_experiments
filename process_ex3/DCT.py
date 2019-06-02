from IONode import IONode
class DCT(IONode):
    def __init__(self, name='mouse', status=0, dtype='O', pcb_name=None): # 默认为输出设备
        IONode.__init__(self, name, status, pcb_name)
        self.__dtype = dtype # 设备类型

    def getType(self):
        return self.__dtype

    def gatherAttrs(self):
        attrs = []
        length =len(self.__dict__.keys())
        i = 0
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
            i += 1
            if i >= length-3:
                break
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.gatherAttrs())

if __name__ == '__main__':
    node = IONode("mouse1")
    d = DCT(name="mouse", dtype='I')
    print(node)
    print(d)
