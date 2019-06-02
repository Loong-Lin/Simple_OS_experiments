from PCB import PCB


class IONode(object):
    def __init__(self, name, status=0, pcb_name=None):
        self.__name = name  # 表示设备名
        self.__status = status  # 表示设备状态，0位空闲，1为忙等
        self.pcb = PCB(pcb_name)  # 占用该节点的进程
        self.waiting_list = list()  # 等待该节点的进程队列等待该节点的进程队列
        self.parent = None  # 指向父节点
        self.next = None  # 指向下一个节点


    def gatherAttrs(self):
        attrs = []
        length =len(self.__dict__.keys())
        i = 0
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
            i += 1
            if i >= length-2:
                break
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())

    def getName(self):
        return self.__name

    def getPCBName(self):
        return self.pcb.getName()

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status

if __name__ == '__main__':
    pcb = PCB("job3")
    a = IONode(name="mouse", status=0)
    # a.pcb = pcb
    print(a)
    print(a.getName())
    print(a.getPCBName())
