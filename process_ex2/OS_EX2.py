import numpy as np
# from Exception import BackError
# 分页式存储管理
# 页表项
class PageItem(object):
    def __init__(self, page_num=None, chunk=-1, status=0, visit=0, address=None):
        self.page_num = page_num # 页号
        self.chunk_num = chunk # 块号
        self.status = status # 状态位
        self.visit = visit # 访问次数
        self.address = address # 地址

    def gatherAttrs(self):
        attrs = []
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return "\t\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())

    def getPage_num(self):
        return self.page_num

    def getChunk_num(self):
        return self.chunk_num

    def getStatus(self):
        return self.status

    def getVisit(self):
        return self.visit

    def getAddress(self):
        return self.address

class PagingStorage(object):
    def __init__(self, page_length=6, chunk_length=3, chunk_size=1):
        self.chunk_size = chunk_size # 块的大小
        self.lack_time = 0 # 缺页次数
        self.lack_rate = 0 # 缺页率
        self.page_table = None
        self.chunk_table = np.full(chunk_length, -1, dtype=int)
        self.bitmap = []
        self.input_list = []

    def initBitMap(self):
        np.random.seed(1)
        self.bitmap = np.random.randint(0, 2, (4, 4), dtype=int)
        self.lack_time = 0  # 缺页次数
        self.lack_rate = 0  # 缺页率
        self.page_table = np.empty(page_length, dtype=PageItem)
        self.chunk_table = np.full(chunk_length, -1, dtype=int)
        self.input_list = []
        print("初始位示图：")
        for it in self.bitmap:
            print(it)

    # 创建页表
    def creatPageTable(self):
        for i in range(len(self.page_table)):
            item = PageItem(page_num=i)
            self.page_table[i] = item

    # 访问地址
    def accessAddress(self, choose):
        flag = True
        while flag:
            try:
                addr = input("请输入逻辑地址: ").strip()
                addr = int(addr, 16)  # 将输入的字符串的16进制数转为10进制数
                chunk_size = self.chunk_size * 1024
                page_num = int(addr / chunk_size)
                if page_num >= len(self.page_table):
                    raise IndexError
                if addr == -1:
                    flag = False
                    raise ValueError
            except ValueError:
                print("返回上一级。")
            except IndexError:
                print("输入的地址越界！")
            except:
                print("请检查输入。")
            else:
                self.addressResolute(addr)
                self.input_list.append(page_num)
                if choose == 'FIFO':
                    self.FIFO(page_num)
                elif choose == 'LRU':
                    self.LRU(page_num)
            finally:
                pass

    # 获得对应页号的物理块号
    def getChunk(self):
        for i in range(len(self.bitmap)):
            # flag = 1
            for j in range(len(self.bitmap[i])):
                if 0 == self.bitmap[i,j]:
                    # self.page_table[page].chunk_num = len(self.bitmap[i])*i + j
                    # self.bitmap[i, j] = 1  # 将位示图的空位置1，表示已经被占
                    return len(self.bitmap[i])*i + j
        return -1

    # 地址解析，逻辑地址转物理地址
    def addressResolute(self, addr):
        try:
            chunk_size = self.chunk_size * 1024
            page = int(addr / chunk_size)
        except:
            print("error! 块长不能为0！")
        else:
            offset_addr = addr % chunk_size
            physical_addr = self.getChunk() * chunk_size + offset_addr
            self.page_table[page].address = hex(physical_addr)  # 转16进制
            self.page_table[page].visit += 1  # 每访问一次某页，其访问次数加1
        finally:
            pass

    # 缺页
    def missPage(self, page):
        self.page_table[page].chunk_num = self.getChunk()
        i = int(self.page_table[page].chunk_num / len(self.bitmap[0]))
        j = self.page_table[page].chunk_num % len(self.bitmap[0])
        self.bitmap[i, j] = 1
        # print("i, j", i, j)
        self.page_table[page].status = 1  # 状态位置1
        # self.page_table[page].visit += 1  # 每访问一次某页，其访问次数加1

    # 置换，修改其中的一些状态位
    def replacement(self, page):
        i = int(self.page_table[page].chunk_num/len(self.bitmap[0]))
        j = self.page_table[page].chunk_num%len(self.bitmap[0])
        self.bitmap[i,j]=0
        self.page_table[page].chunk_num = -1
        self.page_table[page].address = None  # 转16进制
        self.page_table[page].status = 0  # 状态位置1

    def FIFO(self, page_num):
        length = len(self.chunk_table)
        for i in range(length):
            # 命中
            if self.chunk_table[i] == page_num:
                break
            # 只缺页
            elif self.chunk_table[i] == -1:
                self.lack_time += 1
                self.missPage(page_num)
                self.chunk_table[i] = page_num
                break
            # 置换
            elif i == length-1 and self.chunk_table[i] != -1:
                self.replacement(self.chunk_table[0])
                for j in range(length-1):
                    self.chunk_table[j] = self.chunk_table[j+1]
                self.lack_time += 1
                self.chunk_table[length-1] = page_num
                self.missPage(page_num)
            else:
                continue
        self.show()

     # 最近最久未使用的置换
    def LRU(self, page_num):
        chunk_length = len(self.chunk_table)
        for i in range(chunk_length):
            # 状态位为0，并且内存未被占满
            if self.chunk_table[i] == -1:
                self.lack_time += 1
                self.missPage(page_num)
                self.chunk_table[i] = page_num
                break
            # 命中
            elif self.page_table[page_num].status == 1:
                for j in range(chunk_length-1):
                    if self.chunk_table[j] == page_num:
                        j2 = j
                        for j2 in range(chunk_length-1):
                            self.chunk_table[j2] = self.chunk_table[j2 + 1]
                self.chunk_table[chunk_length-1] = page_num
                break
            # 置换
            elif i == chunk_length-1:
                self.replacement(self.chunk_table[0])
                for k in range(chunk_length-1):
                    self.chunk_table[k] = self.chunk_table[k+1]
                self.lack_time += 1
                self.chunk_table[chunk_length-1] = page_num
                self.missPage(page_num)
                break
        self.show()

    # 最佳置换算法
    def OPT(self):
        self.chunk_table = np.full(chunk_length, -1, dtype=int)
        self.lack_time = 0
        record = dict() # 存取方式为 {序号:页号}
        print("self.input_list: ", self.input_list)
        # 统计各个页号的位置
        for i in range(len(self.input_list)):
            if record.get(self.input_list[i], 0) == 0:
                # temp = [i]
                record[self.input_list[i]] = [i]
            else:
                record[self.input_list[i]].append(i)

        length = len(self.chunk_table)
        for i in range(len(self.input_list)):
            for j in range(length):
                # 只缺页
                if self.chunk_table[j] == -1:
                    self.chunk_table[j] = self.input_list[i]
                    self.lack_time += 1
                    # 遇到对应的页号，则弹出列表的第一个序号
                    record[self.input_list[i]].pop(0)
                    print("缺页: self.chunk_table", self.chunk_table)
                    break
                # 命中
                elif self.chunk_table[j] == self.input_list[i]:
                    record[self.input_list[i]].pop(0)
                    print("命中: self.chunk_table", self.chunk_table)
                    break
                # 置换
                elif j == length-1:
                    record[self.input_list[i]].pop(0)
                    # 如果当前页号对应的位置列表长度大于0
                    if len(record.get(self.chunk_table[0], [])) > 0:
                        max_p = record[self.chunk_table[0]][0]
                    else:
                        max_p = len(self.input_list)
                    replace = 0
                    for k in range(1, length):
                        if len(record.get(self.chunk_table[k], [])) > 0:
                            now = record.get(self.chunk_table[k])[0]
                        else:
                            now = len(self.input_list)
                            if max_p < now:
                                replace = k
                    self.chunk_table[replace] = self.input_list[i]
                    self.lack_time += 1
                    print("置换: self.chunk_table", self.chunk_table)
                    break

        self.lack_rate = float(self.lack_time / len(self.input_list))
        print("缺页次数：", self.lack_time)
        print("缺页率：", self.lack_rate)


    def show(self):
        print("页号: 块号: 状态位: 访问次数: 物理地址: ")
        for it in self.page_table:
            print(it)
        for it in self.chunk_table:
            print(it)
        visit_sum = 0
        for it in self.page_table:
            visit_sum += it.visit
        self.lack_rate = float(self.lack_time/visit_sum)
        print("缺页次数：", self.lack_time)
        print("缺页率：", self.lack_rate)

    def help(self):
        print("FIFO  表示先进先出算法")
        print("LRU   表示最近最久未使用置换算法")
        print("OPT   表示最佳置换算法")
        print("q     表示退出")

    def make_a_test(self):
        flag = True
        while flag:
            try:
                print("if you don't know how to use it, please enter 'h'.")
                choose = input(">>").strip()

            except:
                print("请检查输入！")
            else:
                if choose == 'q':
                    flag = False
                elif choose == 'h':
                    self.help()
                elif choose == 'OPT':
                    self.OPT()
                else:
                    self.initBitMap()
                    self.creatPageTable()
                    self.accessAddress(choose)
            finally:
                pass


if __name__ == "__main__":
    try:
        page_length = int(input("请输入页表长度: "))
        chunk_length = int(input("请输入内存块长度: "))
        chunk_size = int(input("请输入内存块的大小(单位为KB): "))
    except:
        print("请检查输入！必须都为正整数。")
    else:
        page = PagingStorage()
        page.make_a_test()
    finally:
        print("Over!")

