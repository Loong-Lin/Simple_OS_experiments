class PCB(object):
    def __init__(self, name='job1', size=1, arrival=0, sevice=0,
                 finished=0, runned=0):
        self.__name = name
        self.__size = size
        self.__arrival_time = arrival # 到达时刻
        self.__sevice_time = sevice # 服务时间
        self.__finished_time = finished # 完成时刻
        self.__runned_time = runned # 已运行的时间, 即对该进程执行的时间

    def gatherAttrs(self):
        attrs = []
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):

        return "{}".format(self.gatherAttrs())

    def getName(self):
        return self.__name

    def getSize(self):
        return self.__size

    def getArrivalTime(self):
        return self.__arrival_time

    def getSeviceTime(self):
        return self.__sevice_time

    def getFinishedTime(self):
        return self.__finished_time

    def setFinishedTime(self, time):
        self.__finished_time = time

    def getRunnedTime(self):
        return self.__runned_time

    def setRunnedTime(self, time):
        self.__runned_time = time

if __name__ == '__main__':
    a = PCB(arrival=2, sevice=5, finished=7, runned=5)
    print("进程名：size：提交时刻：服务时间：完成时刻：已运行时间：")
    print(a)