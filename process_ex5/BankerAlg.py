import io
# 银行家算法
class Process(object):
    def __init__(self, name=None):
        self.name = name
        self.max = [] # 该进程所需要的最大资源
        self.allocation = [] # 已分配的资源，即已得到的资源
        self.need = [] # 还需要的资源数
        self.safe = False

    def gatherAttrs(self):
        attrs = []
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())

class BankerAlgorithm(object):
    def __init__(self):
        self.all_source =[]
        self.processes = []
        self.safe_queue = [] # 安全队列
        self.work = []

    def initProcesses(self):
        self.all_source = [6, 9, 13, 3]
        data_path = "banker_data.txt"
        with io.open(data_path, 'r') as f:
            data_lines = [it.strip().split(' ') for it in f.readlines()]
        for it in data_lines:
            process = Process(name=it[0])
            length = len(it)
            list1 = []
            for i in range(1, length):
                list1.append(int(it[i]))
            x1 = int(length/3)
            process.max = list1[0:x1]
            process.allocation = list1[x1:2*x1]
            process.need = list1[2*x1:length]
            self.processes.append(process)
        alloca = [0, 0, 0, 0]
        for it in self.processes:
            alloca[0] += it.allocation[0]
            alloca[1] += it.allocation[1]
            alloca[2] += it.allocation[2]
            alloca[3] += it.allocation[3]
        for i in range(len(self.all_source)):
            self.work.append(self.all_source[i] - alloca[i])

    def findSafeProcess(self):
        for it in self.processes:
            if not it.safe:
                flag = True
                for j in range(len(it.need)):
                    if it.need[j] > self.work[j]:
                        flag = False
                        break
                if flag == True:
                    # it.safe = True
                    return it
        return -1

    def requestSource(self):
        length = len(self.processes)
        for i in range(length):
            process = self.findSafeProcess()
            if process != -1:
                alloca = process.allocation
                print("before:", self.work)
                for i in range(len(self.work)):
                    self.work[i] = self.work[i] + alloca[i]
                process.safe = True
                print(process, " ", self.work)
                self.safe_queue.append(process)
        if len(self.safe_queue) == length:
            print("存在安全序列！")
            print("safe queue: ")
            for it in self.safe_queue:
                print(it.name)
        else:
            print("不存在安全序列！")


    def show(self):
        for it in self.processes:
            print(it)
        print(self.work)

if __name__ == '__main__':
    a = BankerAlgorithm()
    a.initProcesses()
    a.show()
    a.requestSource()



