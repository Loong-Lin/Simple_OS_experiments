from DCT import DCT
from COCT import COCT
from CHCT import CHCT


class IOManagemnet(object):
    def __init__(self):
        self.device_table = ['keyboard', 'mouse', 'displayer', 'printer']  # 设备名称表
        self.system_device_table = []  # 系统设备表，存放DCT对象
        self.CO_control_table = [COCT('CO1'), COCT('CO2'), COCT('CO3')]  # 控制器控制表
        self.CH_control_table = [CHCT('CH1'), CHCT('CH2')]  # 通道控制表
        self.CH_table = ['CH1', 'CH2']  # 通道名
        self.CO_table = ['CO1', 'CO2', 'CO3']  # 控制器名
        self.process = []  # 所有的进程

    # 设备初始化
    def init(self):
        length = len(self.device_table)
        for i in range(length):
            # sdt = SDT(name=self.device_table[i])
            if i <= 1:
                # sdt.dct = DCT(name=self.device_table[i], dtype='I', pcb_name='job3')
                dct = DCT(name=self.device_table[i], dtype='I')
                # sdt.dct = dct
            else:
                dct = DCT(name=self.device_table[i])
                # sdt.dct = dct
            self.system_device_table.append(dct)

        self.system_device_table[0].parent = self.CO_control_table[0]
        self.system_device_table[1].parent = self.CO_control_table[0]
        self.CO_control_table[0].parent = self.CH_control_table[0]

        self.system_device_table[2].parent = self.CO_control_table[1]
        self.CO_control_table[1].parent = self.CH_control_table[1]

        self.system_device_table[3].parent = self.CO_control_table[2]
        self.CO_control_table[2].parent = self.CH_control_table[1]
        # chct = self.CH_control_table[1]
        # chct.pcb.setName("aaaa")
        # dct = self.system_device_table[3]
        # dct.pcb.setName("aaaa")

    # 添加设备
    def addDevice(self):
        try:
            device_info = input("Please Input Device name and Device type: ").strip().split(" ")
            types = ['i', 'I', 'o', 'O']
            # print(device_info)
            print("1.选择已有控制器; 2.创建新控制器")
            choose = int(input(">>"))
            if len(device_info) != 2:
                raise ValueError
            if device_info[1] not in types:
                raise ValueError
            if device_info[0] in self.device_table:
                raise NameError
        except ValueError:
            print("请检查输入！")
        except NameError:
            print("已存在同名设备，请重新输入设备名。")
        except:
            print("请检查输入")
        else:
            self.device_table.append(device_info[0])
            # sdt = SDT(name=device_info[0])
            dct = DCT(name=device_info[0], dtype=device_info[1])
            self.system_device_table.append(dct)  # 首先将新设备加入系统设备表
            # print("1.选择已有控制器; 2.创建新控制器")
            # choose = int(input(">>"))
            if choose == 1:
                co_name = input("输入控制器名: ")
                for i in range(len(self.CO_control_table)):
                    if self.CO_control_table[i].getName() == co_name:
                        dct.parent = self.CO_control_table[i]
                print("last_co: ", dct.parent)
            elif choose == 2:
                flag = True
                while flag:
                    co_name = input("输入新控制器名: ")
                    ch_name = input("输入选择的通道名称：")
                    if ch_name not in self.CH_table:
                        print("通道名输入错误，请重新输入！")
                    else:
                        flag = False
                new_co = COCT(name=co_name)
                dct.parent = new_co  # 新设备指向新的节点
                self.CO_control_table.append(new_co)  # 加入通道控制表
                for i in range(2):
                    if ch_name == self.CH_control_table[i].getName():
                        new_co.parent = self.CH_control_table[i]
        finally:
            pass

    def deleteDevice(self):
        length = len(self.device_table)
        if length <= 4:
            print("无可删除设备！初始化设备不可删除")
        else:
            new_devices = self.device_table[4:length]
            device_name = input("请输入想删除的设备名称：")
            if device_name in new_devices:
                dev_index = self.device_table.index(device_name)  # 获取其在列表的位置
                self.device_table.remove(device_name)  # 在设备名称表上移除
                del_device = self.system_device_table.pop(dev_index)  # 弹出系统控制表上对应位置的设备
                print("del_device: ", del_device)
                del_co = del_device.parent
                print("del_co: ", del_co)
                co_index = self.CO_control_table.index(del_co)
                print("co_index: ", co_index)
                print("delete successfully.")
                # 如果是新增的控制器则删除，否则不删
                if co_index > 2:
                    self.CO_control_table.pop(co_index)
            elif device_name in self.device_table[:5]:
                print("初始设备不允许删除！")
            else:
                print("无此设备名！")

    # 进程申请设备
    def applyDevice(self):
        try:
            print(self.device_table)
            process_name = input("请输入进程名: ")
            device_name = input("请输入需要申请的设备名：")
            if process_name not in self.process and device_name in self.device_table:
                self.process.append(process_name)
            else:
                raise NameError
        except NameError:
            print("请检查输入！")
        else:
            # 获取设备在系统设备控制表中的位置
            dev_index = self.device_table.index(device_name)
            dct = self.system_device_table[dev_index]  # 对应的设备
            if dct.getStatus() == 0:  # 设备dct处于空闲状态
                dct.setStatus(1)  # 状态位设为忙等
                dct.pcb.setName(process_name)  # 更改当前占用的进程名
                coct = dct.parent  # 去COCT看
                coct.next = dct  # 往回指，为了回收方便
                if coct.getStatus() == 0:
                    coct.setStatus(1)
                    coct.pcb.setName(process_name)
                    chct = coct.parent  # 去CHCT
                    chct.next = coct  # 往回指，为了回收方便
                    if chct.getStatus() == 0:
                        chct.setStatus(1)
                        chct.pcb.setName(process_name)
                    else:
                        # 如果处于忙等，则加入等待队列
                        chct.waiting_list.append(process_name)
                else:
                    coct.waiting_list.append(process_name)
            else:
                dct.waiting_list.append(process_name)
            p = dct.parent
            print("设备名: 状态: 进程: 等待队列: 类型:")
            print(dct, '\t' + dct.getType())
            while p:
                print(p)
                p = p.parent
        finally:
            pass

    def judgeProcess(self, pcb_name):
        # 获取设备在系统设备控制表中的位置
        pass

    def recycleDevice(self):
        try:
            pcb_name = input("请输入进程名：")
            device_name = input("请输入设备名：")
            if pcb_name not in self.process:
                raise NameError
            elif device_name not in self.device_table:
                raise NameError
        except NameError:
            print("进程名或设备名输入错误！")
        else:
            self.judgePcbDevice(pcb_name, device_name)
        finally:
            pass

    def judgePcbDevice(self, pcb_name, device_name):
        dev_index = self.device_table.index(device_name)
        begin_dct = self.system_device_table[dev_index]
        chct = begin_dct.parent.parent  # 从CH往开始查，从后往前查
        if pcb_name == chct.getPCBName():
            if len(chct.waiting_list) > 0:
                # 如果等待队列不为空，则弹出队首进程占有通道
                chct.pcb.setName(chct.waiting_list.pop(0))
            else:  # 查COCT
                coct = chct.next
                if len(coct.waiting_list) > 0:
                    pop_pcb = coct.waiting_list.pop(0)
                    coct.pcb.setName(pop_pcb)
                    chct.pcb.setName(pop_pcb)
                    if len(begin_dct.waiting_list) > 0:
                        begin_dct.pcb.setName(begin_dct.waiting_list.pop(0))
                    else:
                        begin_dct.pcb.setName(None)
                        begin_dct.setStatus(0)

                else:  # 查DCT
                    dct = coct.next
                    if len(dct.waiting_list) > 0:
                        pop_pcb = dct.waiting_list.pop(0)
                        dct.pcb.setName(pop_pcb)
                        coct = dct.parent
                        coct.pcb.setName(pop_pcb)
                        chct = coct.parent
                        chct.pcb.setName(pop_pcb)
                    # 整个通道线路上只有一个进程时
                    else:
                        dct.pcb.setName(None)
                        dct.setStatus(0)
                        coct = dct.parent
                        coct.pcb.setName(None)
                        coct.setStatus(0)
                        chct = coct.parent
                        chct.pcb.setName(None)
                        chct.setStatus(0)
        else:
            print("无正在占用通道的设备")

    def makeATest(self):
        # flag = True
        funcs = {'add': self.addDevice,
                 'del': self.deleteDevice,
                 'p': self.applyDevice,
                 'r': self.recycleDevice,
                 's': self.show,
                 'h': self.help,
                 'q': self.quit}
        print("if you need help, you can input 'h'.")
        while True:
            key = input("$").strip(', ')
            if key not in funcs.keys():
                print("wrong command!")
            else:
                func = funcs.get(key, "no this function.")
                func()

    def help(self):
        tips = {'add': 'add device',
                'del': 'delete device',
                'p': 'process apply device',
                'r': 'over process and recycle Device',
                's': 'show',
                'h': 'help',
                'q': 'exit'}
        for it in tips.items():
            print(it)

    def quit(self):
        print("Game Over!")
        exit(0)

    # 输出函数
    def show(self):
        length = len(self.system_device_table)
        print("设备名: 状态: 进程: 等待队列: 类型:")
        for i in range(length):
            p = self.system_device_table[i].parent
            print(self.system_device_table[i], '\t' + self.system_device_table[i].getType())
            while p:
                print(p)
                p = p.parent


if __name__ == '__main__':
    io = IOManagemnet()
    io.init()
    io.makeATest()
