# -*- coding: utf-8 -*-

from toString import AttrDisplay
from exception import NameError


class PCB(AttrDisplay):

    def __init__(self, name, size):
        self.__name = name
        self.__size = size

    def getName(self):
        return self.__name

    def getSize(self):
        return self.__size


class Process(object):
    def __init__(self, s=0, e=100):
        # self.__start = s
        # self.__end = e
        self.free_space = [(s, e)]  # 存放空闲空间的起始地址和结束地址
        self.pcb_dict = dict()  # 存放进程名和进程起始地址，name : (start_ad, pcb.size)
        self.ready = []  # 就绪态
        self.execute = []  # 执行态
        self.block = []  # 阻塞态



    def create(self):
        try:
            name, size = input("Please Enter new job's name and memory's size: ").split(' ')
            pcb = PCB(str(name), int(size))
            na = self.checkName(name)
            if na == 1:
                raise NameError(name)
        except NameError as e:
            print(e)
        except:
            print("请检查输入。")
            # flag = True
            # while flag:
            #     if size.isdigit() and len(str(name)) < 8:
            #         if int(size) > 0:
            #             flag = False
            #     else:
            #         print("Input is illegal.")
            #         name, size = input("Please Enter new job's name and memory's size: ").split(' ')
            # pcb = PCB(str(name), int(size))
        else:
            self.processAddManage(pcb)
            print("Create a new job: " + str(pcb.getName()))
            # self.readyProcess(pcb)
        finally:
            pass

    def readyProcess(self, pcb):
        self.ready.append(pcb)
        if len(self.execute) == 0:
            job1 = self.ready.pop(0)  # 把先创建的任务弹出
            self.execute.append(job1)

    # 阻塞正在执行中的进程
    def blockProcess(self):
        if 0 == len(self.execute):
            print("没有进程在被执行，无需block。")
        else:
            b = self.execute.pop()
            self.block.append(b)
            print(b.getName() + " is blocked!")
            if len(self.execute) == 0 and len(self.ready) > 0:
                self.execute.append(self.ready.pop(0))

    def wakeup(self):
        if 0 == len(self.block):
            print("没有进程被阻塞，无需wakeup。")
        else:
            wake = self.block.pop(0)  # 弹出被阻塞队列中的第一个
            print(wake.getName() + " is waked up.")
            # self.ready.append(wake) # 将弹出的pcb加入就绪态
            self.readyProcess(wake)

    # 结束进程
    def terminate(self):
        if 0 == len(self.execute):
            print("没有可以结束的进程。")
        else:
            ter = self.execute.pop()
            self.processEndManage(ter)  # 结束进程，释放内存，从字典中删除这个进程
            print(ter.getName() + " is terminated.")
            if len(self.ready) > 0:
                new = self.ready.pop(0)
                self.execute.append(new)

    # 时间片轮转
    def round_robin(self):
        if 0 == len(self.ready) and 0 == len(self.execute):
            print("There is no pcb in Ready and Execute, so can't round_robing.")
        elif len(self.execute) > 0 and len(self.ready) == 0:
            pass
        else:
            round_out = self.execute.pop()
            print(round_out.getName() + " is round-robin.")
            round_in = self.ready.pop(0)
            self.execute.append(round_in)
            self.ready.append(round_out)

    # 进程增加管理
    def processAddManage(self, pcb):
        if len(self.free_space) == 0:
            self.free_space.append((self.getStart(), self.getEnd()))
        size = pcb.getSize()
        space_length = len(self.free_space)
        for i in range(space_length):
            (start, end) = self.free_space[i]
            if size <= (end - start):
                if (end - start) <= size + 2:
                    # pass
                    self.pcb_dict[pcb.getName()] = (start, end-start)
                    del self.free_space[i]
                    self.readyProcess(pcb)
                else:
                    self.pcb_dict[pcb.getName()] = (start, pcb.getSize())
                    self.free_space[i] = (start + size, end)
                    self.readyProcess(pcb)
                break
            elif i == space_length-1:
                print("内存空间不足")
                break


     # 进程结束管理
    def processEndManage(self, pcb):
        if self.pcb_dict.get(pcb.getName()) is not None:
            (start, size) = self.pcb_dict[pcb.getName()]
            for i in range(len(self.free_space)):
                (s, e) = self.free_space[i]
                if start + size == s:
                    self.free_space[i] = (start, e) # 将释放的内存空间加到空闲区
                    break
                else:
                    self.free_space.append((start, start + size))
                    break
            del self.pcb_dict[pcb.getName()]

            if len(self.free_space) == 0:
                self.free_space.append((start, start + size))
        else:
            print("不存在进程" + pcb.getName())
        # 合并相连的空闲区
        new_space = []
        if len(self.free_space) >= 2:
            self.free_space.sort()
            list_length = len(self.free_space)
            (s, e) = self.free_space[0]
            for j in range(1, list_length):
                (s1, e1) = self.free_space[j]
                if e == s1:
                    e = e1
                    # new_space.append((s, e1))
                else:
                    new_space.append((s, e))
                    s = s1
                    e = e1
            new_space.append((s, e))
            self.free_space = new_space


    # 检查是否存在重名进程
    def checkName(self, pcb_name):
        for it in self.ready:
            if pcb_name == it.getName():
                print("已存在名字为" + it.getName() + "的进程。")
                return 1
        for it in self.execute:
            if pcb_name == it.getName():
                print("已存在名字为" + it.getName() + "的进程。")
                return 1
        for it in self.block:
            if pcb_name == it.getName():
                print("已存在名字为" + it.getName() + "的进程。")
                return 1
        return 0

    def show(self):
        print("Ready:", end=' ')
        for it in self.ready:
            print(it.getName(), self.pcb_dict[it.getName()], end=', ')
        print()
        print("Execute:", end=' ')
        for it in self.execute:
            print(it.getName(), self.pcb_dict[it.getName()], end=', ')
        print()
        print("Block: ", end=' ')
        for it in self.block:
            print(it.getName(), self.pcb_dict[it.getName()], end=', ')
        print()
        # print("self_pcb.dict", self.pcb_dict)
        print("free_space: ", self.free_space)

    def help(self):
        functions = {
            'c': "create",
            'b': "blockProcess",
            'w': "wakeup",
            'o': "terminal",
            't': "round_robin",
            's': "show",
            'h': "help",
            'v': "version"
        }
        for it in functions.items():
            print(it)

    def version(self):
        print("Version 1.0 OS Process Control.")
        print("made by Lin Yangqing.")

    def quit(self):
        print("欢迎您再次光顾！ #_#")
        exit(0)

    def make_a_test(self):
        functions = {
            'c': self.create,
            'b': self.blockProcess,
            'w': self.wakeup,
            'o': self.terminate,
            't': self.round_robin,
            's': self.show,
            'h': self.help,
            'v': self.version,
            'q': self.quit
        }
        print("if you need help, you can input 'h'.")
        while True:
            key = input("$").strip(', ')
            if key not in functions.keys():
                print("wrong command!")
            else:
                func = functions.get(key, "no this function.")
                func()


if __name__ == "__main__":
    try:
        start, end = input("请输入内存的起始地址和结束地址：").strip().split()
        a = Process(int(start), int(end))
    except:
        print("请检查您的输入是否为整数，且以空格分隔")
    else:
        a.make_a_test()
    finally:
        print("OK")