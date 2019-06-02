import numpy as np

class Node(object):
    def __init__(self, index_name=0):
        self.index_name = index_name
        self.index_list = []

    def gatherAttrs(self):
        attrs = []

        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return "\t".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "{}".format(self.gatherAttrs())



class FNode(object):
    def __init__(self, size=0, extended_name=None):
        self.size = size  # 文件大小
        self.__extended_name = extended_name  # 扩展名，目录没有扩展名
        self.direct_index = []
        self.single_index = Node()
        self.double_index = Node()
        self.tri_index = Node()


# 磁盘管理
class FileManagement(object):
    def __init__(self, block_size=32):
        self.__block_size = block_size # 磁盘块大小，单位为B,
        self.super_blocks = []
        self.fnode_blocks = []
        self.bitmap = None

    def getBlockSize(self):
        return self.__block_size

    # 初始化位示图
    def initBitMap(self):
        np.random.seed(1)
        self.bitmap = np.random.randint(0, 2, (32, 32), dtype=int)
        k = 0
        '''for i in range(len(self.bitmap)):
            for j in range(len(self.bitmap[i])):
                if self.bitmap[i, j] == 0:
                    k += 1
        print("zero: ", k)'''

    # 获得对应的物理块号
    def getChunk(self):
        for i in range(len(self.bitmap)):
            # flag = 1
            for j in range(len(self.bitmap[i])):
                if 0 == self.bitmap[i,j]:
                    self.bitmap[i, j] = 1  # 将位示图的空位置1，表示已经被占
                    return len(self.bitmap[i])*i + j
        return -1

    # 直接索引
    def directBlock(self, length):
        # fnode = FNode()
        direct_index = []
        for i in range(length):
            direct_index.append(self.getChunk())
            if direct_index[i] == -1:
                print("direct_index:磁盘块不足！")
                break
        return direct_index

     # 第一层
    def firstLayer(self, length):
        # fnode = FNode(size=file_size)
        node = Node(index_name=self.getChunk())
        for i in range(length):
            addr_block = self.getChunk()
            if addr_block == -1:
                print("single_index:磁盘块不足！")
                break
            node.index_list.append(addr_block)
        #fnode.single_index = node
        return node

    # 第二层
    def secondLayer(self, length):
        node1 = Node(index_name=self.getChunk())
        # block_num-direct_len-A_a， A_a为一个盘块可以容纳的索引号数量
        A_a = int(self.getBlockSize()/4)
        node2 = Node(index_name=self.getChunk())
        # rows = int(length/A_a)
        for i in range(length):
            addr_block = self.getChunk()
            node2.index_list.append(addr_block)
            if addr_block == -1:
                print("double_index:磁盘块不足！")
                break
            if len(node2.index_list) == A_a and i != length-1:
                node1.index_list.append(node2)
                node2 = Node(index_name=self.getChunk())
            elif i == length-1:
                node1.index_list.append(node2)
        return node1

    def thirdLayer(self, length):
        A_a = int(self.getBlockSize() / 4)
        third = int(length / (A_a * A_a)) + 1
        length2 = length % (A_a * A_a)
        # print("length2:", length2)
        if length%(A_a*A_a) == 0:
            third = third - 1
            length2 = A_a * A_a
        node3 = Node(index_name=self.getChunk())
        for i in range(third):
            node2 = Node(index_name=self.getChunk())
            if i == 0:
                node1 = Node(index_name=self.getChunk())
            for j in range(A_a*A_a):
                addr_block = self.getChunk()
                if addr_block == -1:
                    print("double_index:磁盘块不足！")
                    break

                node1.index_list.append(addr_block)
                if len(node1.index_list) == A_a:
                    node2.index_list.append(node1)
                    node1 = Node(index_name=self.getChunk())
                elif i == third - 1 and j == length2-1:
                    node2.index_list.append(node1)
                    break
            node3.index_list.append(node2)
        return node3

    # 检查文件大小是否能存下
    def checkFileSize(self, file_size):
        A_a = int(self.getBlockSize() / 4)
        filesize1 = 10 * self.getBlockSize() + A_a * self.getBlockSize()
        filesize2 = filesize1 + pow(A_a, 2) * self.getBlockSize()
        filesize3 = filesize2 + pow(A_a, 3) * self.getBlockSize()
        if file_size > filesize3:
            # print("sorry, 您的文件过大，超过了所能存储的极限。")
            return False
        elif file_size < 0:
            # print("文件大小必须为正数。")
            return False
        return True

    # 为文件分配磁盘块, 文件大小的单位为B
    def fileAllocation(self, fnode):
        file_size = fnode.size
        # 得到所需要的存储文件的磁盘块数
        if file_size%self.getBlockSize() == 0:
            block_num = int(file_size/self.getBlockSize())
        else:
            block_num = int(file_size / self.getBlockSize()) + 1
        print("block_num: ", block_num)
        A_a = int(self.getBlockSize() / 4)
        filesize1 = 10 * self.getBlockSize() + A_a * self.getBlockSize()
        filesize2 = filesize1 + pow(A_a, 2) * self.getBlockSize()
        filesize3 = filesize2 + pow(A_a, 3) * self.getBlockSize()
        print("direct_index:", 10 * self.getBlockSize(),  "filesize1:",
              filesize1, " filesize2:", filesize2, " filesize3:", filesize3)
        direct_len = 10
        # fnode = FNode(size=file_size)

        if file_size <= 10 * self.getBlockSize():
            direct_list = self.directBlock(block_num)
            fnode.direct_index = direct_list
        elif file_size <= filesize1:
            direct_list = self.directBlock(direct_len)
            fnode.direct_index = direct_list
            # 开始第一层
            node = self.firstLayer(block_num-direct_len)
            fnode.single_index = node

        elif file_size <= filesize2:
            direct_list = self.directBlock(direct_len)
            fnode.direct_index = direct_list
            # 开始第一层
            node = self.firstLayer(A_a)
            fnode.single_index = node
            # 开始第二层
            node1 = self.secondLayer(block_num-direct_len-A_a)
            fnode.double_index = node1

        elif file_size <= filesize3:
            direct_list = self.directBlock(direct_len)
            fnode.direct_index = direct_list
            # 开始第一层
            node = self.firstLayer(A_a)
            fnode.single_index = node
            # 开始第二层
            node1 = self.secondLayer(A_a * A_a)
            fnode.double_index = node1
            # 开始第三层
            node3 = self.thirdLayer(block_num-direct_len-A_a-A_a*A_a)
            fnode.tri_index = node3
        elif file_size < 0:
            print("文件大小必须为正整数。")
        else:
            print("盘块号不够，无法存储！")

        if 0 <= file_size <=filesize3:
            fnode.size = file_size
            self.fnode_blocks.append(fnode)
            self.showFnode(fnode)

    def showFnode(self, fnode):
        print("Direct: ", fnode.direct_index)
        print("Single: ", fnode.single_index)
        print("double_index: ", )
        if len(fnode.double_index.index_list) > 0:
            print(fnode.double_index.index_name)
            for item in fnode.double_index.index_list:
                print(item)
        print("tri_index: ", )
        if len(fnode.tri_index.index_list) > 0:
            print("node3 index_name", fnode.tri_index.index_name)
            for item in fnode.tri_index.index_list:
                print("second index_name: ", item.index_name)
                if len(item.index_list) > 0:
                  for it in item.index_list:
                      print("last layer", it)

    # 回收内存块
    def recyleBlock(self, fnode):
        file_size = fnode.size
        # print(fnode.direct_index)
        # print("file_size: ", fnode.size)
        # 得到所需要的磁盘块数
        if file_size % self.getBlockSize() == 0:
            block_num = int(file_size / self.getBlockSize())
        else:
            block_num = int(file_size / self.getBlockSize()) + 1

        A_a = int(self.getBlockSize() / 4)
        filesize1 = 10 * self.getBlockSize() + self.getBlockSize() * A_a
        filesize2 = filesize1 + pow(A_a, 2) * self.getBlockSize()
        filesize3 = filesize2 + pow(A_a, 3) * self.getBlockSize()
        direct_len = len(fnode.direct_index)
        if file_size <= 10 * self.getBlockSize():
            for i in range(block_num):
                self.setBlock(fnode.direct_index[i])
            print("磁盘块回收成功！")
        elif file_size <= filesize1:
            for i in range(direct_len):
                self.setBlock(fnode.direct_index[i])
            # 第一层
            self.setBlock(fnode.single_index.index_name)
            for i in range(block_num-direct_len):
                self.setBlock(fnode.single_index.index_list[i])
            print("磁盘块回收成功！")
        elif file_size < filesize2:
            for i in range(direct_len):
                self.setBlock(fnode.direct_index[i])
            # 第一层
            self.setBlock(fnode.single_index.index_name)
            for i in range(A_a):
                self.setBlock(fnode.single_index.index_list[i])
            # 第二层
            self.setBlock(fnode.double_index.index_name)
            rows = len(fnode.double_index.index_list)
            for i in range(rows):
                index_name = fnode.double_index.index_list[i].index_name
                self.setBlock(index_name)
                double_length = len(fnode.double_index.index_list[i].index_list)
                for j in range(double_length):
                    self.setBlock(fnode.double_index.index_list[i].index_list[j])
            print("磁盘块回收成功！")
        elif file_size <= filesize3:
            for i in range(direct_len):
                self.setBlock(fnode.direct_index[i])
                # 第一层
            self.setBlock(fnode.single_index.index_name)
            for i in range(A_a):
                self.setBlock(fnode.single_index.index_list[i])
            # fnode.single_index = Node()
            # 第二层
            self.setBlock(fnode.double_index.index_name)
            rows = len(fnode.double_index.index_list)
            for i in range(rows):
                index_name = fnode.double_index.index_list[i].index_name
                self.setBlock(index_name)
                double_length = len(fnode.double_index.index_list[i].index_list)
                for j in range(double_length):
                    self.setBlock(fnode.double_index.index_list[i].index_list[j])
            # 第三层
            self.setBlock(fnode.tri_index.index_name)
            rows = len(fnode.tri_index.index_list)
            for i in range(rows):
                index_name1 = fnode.tri_index.index_list[i].index_name
                self.setBlock(index_name1)
                second = len(fnode.tri_index.index_list[i].index_list)
                for j in range(second):
                    node3 = fnode.tri_index.index_list[i].index_list[j]
                    self.setBlock(node3.index_name)
                    third = len(node3.index_list)
                    for k in range(third):
                        self.setBlock(node3.index_list[k])
            print("磁盘块回收成功！")
        else:
            print("该文件不在磁盘块中！")
        # 因为FNode为复合类型，传入的参数为地址，所以可以这样删除
        self.fnode_blocks.remove(fnode)

    # 将位示图的被占位置置为0
    def setBlock(self, chunk_num):
        i = int(chunk_num / len(self.bitmap[0]))
        j = chunk_num % len(self.bitmap[0])
        self.bitmap[i, j] = 0


    def show(self):
       for fnode in self.fnode_blocks:
           self.showFnode(fnode)



if __name__ == '__main__':
    a = FileManagement()
    a.initBitMap()
    # file_size =100, 500,  1000, 6000,
    fnode = FNode(size=5000)
    a.fileAllocation(fnode)
    a.recyleBlock(a.fnode_blocks[0])
    a.show()








