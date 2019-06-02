from PCB import PCB
import io

class ProcessScheduling(object):
    def __init__(self):
        self.ready = []  # 就绪态队列
        self.execute = []  # 执行态队列
        self.block = []  # 阻塞态队列
        self.finish = []  # 是已运行完进程的队列，用于统计各项数据
        self.turnover_time = []  # 周转时间 turnaround time
        self.power_time = []  # 带权周转时间 turnover_time_right
        self.round_robin_time = 0 # 时间片轮转的总时间

    # 初始化到文件中
    def initToFile(self):
        self.ready = []
        self.finish = []
        self.turnover_time = []
        self.power_time = []
        self.round_robin_time = 0
        data_path = "process_data.txt"
        with io.open(data_path, 'r') as f:
            data_lines = [it.strip().split() for it in f.readlines()]
        print("name: arrival_time: sevice_time:")
        for it in data_lines:
            arr_time = int(it[1])
            sev_time = int(it[2])
            pcb = PCB(name=it[0], arrival=arr_time, sevice=sev_time)
            self.ready.append(pcb)
            print(' '+it[0] + '\t\t\t' + it[1] + '\t\t\t' + it[2])

    def create(self):
        flag = True
        while flag:
            try:
                input_data = input("请输入进程名称、提交时刻、和服务时间：").strip().split(' ')
                if len(input_data) == 1 and input_data[0] == 'ok':
                    print("创建进程结束！")
                    break
                elif len(input_data) == 3:
                    name = input_data[0]
                    if self.checkName(name):
                        raise NameError
                    arrival_time = int(input_data[1])
                    length = len(self.ready)
                    if length > 0 and self.ready[length - 1].getArrivalTime() > arrival_time:
                        print("此次的提交时刻不得小于上一个进程的提交时刻。")
                        continue
                    service_time = int(input_data[2])
                    pcb = PCB(name=name, arrival=arrival_time, sevice=service_time)

                else:
                    raise TypeError

            except NameError:
                print("已存在同名的进程！。")
            except TypeError:
                print("请检查输入，必须输入三个参数！")
            else:
                print(pcb)
                self.ready.append(pcb)
                # pass
            finally:
                pass

        # 检查是否存在重名进程

    def checkName(self, pcb_name):
        for it in self.ready:
            if pcb_name == it.getName():
                # print("已存在名字为" + it.getName() + "的进程。")
                return True
        for it in self.execute:
            if pcb_name == it.getName():
                # print("已存在名字为" + it.getName() + "的进程。")
                return True
        for it in self.finish:
            if pcb_name == it.getName():
                # print("已存在名字为" + it.getName() + "的进程。")
                return True
        return False

    # 将就绪态的进程调到执行态中
    def readyToExecute(self):
        if len(self.execute) == 0 and len(self.ready) > 0:
            job1 = self.ready.pop(0)  # 把就绪态的进程弹出
            self.execute.append(job1)

    # 时间片轮转
    def round_robin(self, q):
        if len(self.execute) > 0:
            round_out = self.execute.pop()
            run_time = round_out.getRunnedTime() + q
            if run_time == round_out.getSeviceTime():
                self.round_robin_time += q
                round_out.setRunnedTime(run_time)
                round_out.setFinishedTime(self.round_robin_time)
                self.finish.append(round_out)
            elif run_time > round_out.getSeviceTime():
                q = round_out.getSeviceTime() - round_out.getRunnedTime()
                self.round_robin_time += q
                run_time = round_out.getSeviceTime()
                round_out.setFinishedTime(self.round_robin_time)
                round_out.setRunnedTime(run_time)
                self.finish.append(round_out)

            elif run_time < round_out.getSeviceTime():
                self.round_robin_time += q
                round_out.setRunnedTime(run_time)
                round_out.setFinishedTime(self.round_robin_time)
                self.ready.append(round_out)
            # if round_out.getArrivalTime() > self.round_robin_time:
            #     pass
            self.readyToExecute()

    # first come first served
    def FCFS(self):
        ready_length = len(self.ready)
        for i in range(ready_length):
            pcb = self.ready.pop(0)
            sevice_time = pcb.getSeviceTime()
            start_time = pcb.getArrivalTime()
            if len(self.finish) > 0:
                last_pcb = self.finish[len(self.finish) - 1]
                if last_pcb.getFinishedTime() > start_time:
                    start_time = last_pcb.getFinishedTime()
            turn_time = start_time + sevice_time - pcb.getArrivalTime()
            right_time = float(turn_time) / sevice_time
            pcb.setFinishedTime(start_time + sevice_time)
            pcb.setRunnedTime(sevice_time)
            self.turnover_time.append(turn_time)
            self.power_time.append(right_time)
            self.finish.append(pcb)
        self.showResult()

    # 短进程优先
    def shortProcessFirst(self):
        ready_length = len(self.ready)
        for i in range(ready_length):
            first_pcb = self.ready[i]
            short_job = first_pcb.getSeviceTime()
            if len(self.finish) == 0:
                start_time = first_pcb.getArrivalTime()
            elif len(self.finish) > 0:
                start_time = self.finish[len(self.finish) - 1].getFinishedTime()
            k = i
            for j in range(i + 1, len(self.ready)):
                if start_time >= self.ready[j].getArrivalTime() and \
                        short_job > self.ready[j].getSeviceTime():
                    k = j
                    short_job = self.ready[j].getSeviceTime()
            self.ready[i] = self.ready[k]
            self.ready[k] = first_pcb

            pcb = self.ready[i]

            sevice_time = pcb.getSeviceTime()
            turn_time = start_time + sevice_time - pcb.getArrivalTime()
            right_time = float(turn_time) / sevice_time
            pcb.setFinishedTime(start_time + sevice_time)
            pcb.setRunnedTime(sevice_time)
            self.turnover_time.append(turn_time)
            self.power_time.append(right_time)
            self.finish.append(pcb)

        self.showResult()

    # 时间片轮转调度算法，RR
    def roundRobin(self):
        q = int(input("Please input an integer, q: "))
        self.readyToExecute()
        while True:
            # print("length", length)
            if len(self.ready) == 0 and len(self.execute) == 0:
                break
            self.round_robin(q) # 时间片轮转
            self.showList()
        for it in self.finish:
            turn_time = it.getFinishedTime() - it.getArrivalTime() # 周转时间
            power_time = float(turn_time)/it.getSeviceTime()
            self.turnover_time.append(turn_time)
            self.power_time.append(power_time)
        self.showResult()


    def firstComeFistSevice(self, round_out, q):
        # if len(queue) > 0:
        # round_out = self.execute.pop()
        run_time = round_out.getRunnedTime() + q
        if run_time == round_out.getSeviceTime():
            self.round_robin_time += q
            round_out.setRunnedTime(run_time)
            round_out.setFinishedTime(self.round_robin_time)
            self.finish.append(round_out)
            return True
        elif run_time > round_out.getSeviceTime():
            q = round_out.getSeviceTime() - round_out.getRunnedTime()
            self.round_robin_time += q
            run_time = round_out.getSeviceTime()
            round_out.setFinishedTime(self.round_robin_time)
            round_out.setRunnedTime(run_time)
            self.finish.append(round_out)
            return True
        else:
            self.round_robin_time += q
            round_out.setRunnedTime(run_time)
            round_out.setFinishedTime(self.round_robin_time)
            # self.ready.append(round_out)
            return round_out


    # multileved feedback queue, 多级反馈队列调度算法
    def multilevedQueue(self):
        # first_queue = [] # 第一级队列，q=1
        second_queue = [] # 第二级队列，q=2
        third_queue = [] # 第三级队列，q=4
        first_queue = self.ready
        length = len(first_queue)
        for i in range(length):
            pcb = self.firstComeFistSevice(first_queue.pop(0), 1)
            if True != pcb:
                print("pcb: ", pcb)
                second_queue.append(pcb)
            # first_queue.pop(0)
            # first_queue.pop(first_queue.index(it))

        for i in range(len(second_queue)):
            # second_queue.remove(sec)
            pcb2 = self.firstComeFistSevice(second_queue.pop(0), 2)
            if True != pcb2:
                print("pcb2:", pcb2)
                third_queue.append(pcb2)

        third_length = len(third_queue)
        for i in range(third_length):
            pcb3 = self.firstComeFistSevice(third_queue.pop(0), 4)
            if True != pcb3:
                print("pcb3: ", pcb3)
                third_queue.append(pcb3)

        while True:
            if len(third_queue) == 0:
                break
            third_length = len(third_queue)
            for i in range(third_length):
                pcb3 = self.firstComeFistSevice(third_queue.pop(0), 4)
                if True != pcb3:
                    print("pcb33:", pcb3)
                    third_queue.append(pcb3)

        for it in self.finish:
            turn_time = it.getFinishedTime() - it.getArrivalTime()  # 周转时间
            power_time = float(turn_time) / it.getSeviceTime()
            self.turnover_time.append(turn_time)
            self.power_time.append(power_time)



    def showResult(self):
        print("进程名:   ", end='')
        for it in self.finish:
            print(it.getName(), end=' ')
        print()

        print("提交时刻：", end='')
        for it in self.finish:
            print(it.getArrivalTime(), end=' ')
        print()
        print("服务时间：", end='')
        for it in self.finish:
            print(it.getSeviceTime(), end=' ')
        print()
        print("已运行时间：", end='')
        for it in self.finish:
            print(it.getRunnedTime(), end=' ')
        print()
        print("完成时刻：", end='')
        for it in self.finish:
            print(it.getFinishedTime(), end=' ')
        print()
        print("周转T：", end='')
        sum_time = 0
        for it in self.turnover_time:
            sum_time += it
            print(it, end=' ')
        print()
        ave = float(sum_time)/len(self.finish)
        print("平均周转时间：%.2f" % ave)
        print("带权周转时间：", end='')
        sum_time = 0
        for it in self.power_time:
            sum_time += it
            print("%.2f" % it, end=' ')
        print()
        ave = float(sum_time) / len(self.finish)
        print("平均带权周转时间：%.2f" %  ave)


    def showList(self):
        print("就绪队列：")
        for it in self.ready:
            print(it)
        print("执行队列：")
        for it in self.execute:
            print(it)
        print("完成队列：")
        for it in self.finish:
            print(it)

    def help(self):
        tips = {
            'c': '通过文件创建进程',
            's1': '输出结果',
            's2': '输出各个状态的队列',
            'fcfs': '先来先服务算法',
            'spf': '短进程优先',
            'sjf': '短进程优先',
            'rr': '时间片轮转',
            'mfq': '多级反馈队列',
            'h': '帮助'
        }
        for item in tips.items():
            print(item)

    def makeATest(self):
        functions = {
            'c': self.initToFile,
            's1': self.showResult,
            's2': self.showList,
            'fcfs': self.FCFS,
            'spf': self.shortProcessFirst,
            'sjf': self.shortProcessFirst,
            'rr': self.roundRobin,
            'mfq': self.multilevedQueue,
            'h': self.help
        }
        print("if you need help, you can input 'h'.")
        flag = True
        while flag:
            key = input("$").strip(', ')
            if key == 'q':
                flag = False
            elif key not in functions.keys():
                print("wrong command!")
            else:
                func = functions.get(key, "no this function.")
                func()
        # self.create()
        # self.FCFS()


if __name__ == '__main__':
    a = ProcessScheduling()
    a.makeATest()
