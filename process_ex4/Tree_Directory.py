# 树形目录管理
import datetime as dt
from INode import FileName
from INode import INode
from OS_EX4 import FileManagement
from OS_EX4 import FNode


class DirItem(object):
    def __init__(self, ab_name):
        self.__absolute_name = ab_name
        self.dir_item = []
        self.inode = []
        self.dir_num = 0
        # self.nextnode = None

    def getAbsoluteName(self):
        return self.__absolute_name


class TreeDirectory(object):
    def __init__(self):
        self.current_dir = ''  # 当前所处目录的名字
        self.dir_count = 0  # 文件或目录的总数
        self.tree = []  # 用于存放树形结构的目录
        self.tree_str = ''
        self.filemanagement = FileManagement(block_size=32)

    def init(self):
        dir_item = DirItem('User')
        date = dt.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        inode1 = INode(index_block=0, date=date)
        dir_item.inode.append(inode1)
        dir_item.inode.append(inode1)

        dir_item.dir_item.append(FileName(name='.')) # 第一个表示当前目录
        dir_item.dir_item.append(FileName(name='..')) # 第二个表示父目录
        # dir_item.dir_item[0].next = dir_item.inode[0]
        # dir_item.dir_item[1].next = dir_item.inode[1]
        dir_item.dir_num = 2
        self.current_dir = 'User'
        self.tree.append(dir_item)
        self.dir_count += 1

    def initDirItem(self, parent_index, dirname):
        # dir_item.setDate(date)
        dir_item = DirItem(dirname)  # 创建了DirItem对象
        date = dt.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        inode0 = INode(index_block=self.dir_count, date=date)
        inode1 = INode(index_block=parent_index, date=date)
        dir_item.inode.append(inode0)
        dir_item.inode.append(inode1)

        dir_item.dir_item.append(FileName(name='.'))  # 第一个表示当前目录
        dir_item.dir_item.append(FileName(name='..'))  # 第二个表示父目录
        # dir_item.dir_item[0].next = dir_item.inode[0]
        # dir_item.dir_item[1].next = dir_item.inode[1]
        dir_item.dir_num = 2
        self.tree.append(dir_item)  # 家里树目录列表中
        self.dir_count += 1

    # 获得当前目录的所在self.tree 的位置
    def getDirIndex(self, dir_name=None):
        tree_length = len(self.tree)
        if dir_name == None:
            dir_name = self.current_dir

        for i in range(tree_length):
            nowdir = self.tree[i].getAbsoluteName()
            if dir_name == nowdir:
                return i
        return -1

    # 检查目录重名
    def checkName(self, dirname):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            dir_length = self.tree[i].dir_num
            for j in range(dir_length):
                if self.tree[i].inode[j].getFtype() == 2 and\
                        dirname == self.tree[i].dir_item[j].getName():
                    return False
        return True

    # 创建目录
    def makeDirectory(self, dir_name=None):
        try:
            value = self.checkName(dir_name)
            if value == False:
                raise NameError
            if dir_name == None:
                raise TypeError
        except NameError:
            print("已有同名文件夹！")
        except TypeError:
            print("缺少一个参数，请检查输入")
        else:
            if -1 != self.getDirIndex():
                i = self.getDirIndex()
                ab_name = self.current_dir + '/' + dir_name
                # parent_index = self.tree[i].inode[0] # 当前目录索引即为新目录的父索引
                self.initDirItem(i, ab_name)
                # 将新创建的目录加入到父目录下
                date = dt.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
                inode = INode(index_block=self.dir_count - 1, date=date)
                self.tree[i].inode.append(inode)
                self.tree[i].dir_item.append(FileName(dir_name))
                # self.tree[i].dir_item[self.tree[i].dir_num].next = inode
                self.tree[i].dir_num += 1
                print(inode, '\t', dir_name)
            else:
                print("当前路径异常！")
        finally:
            pass

    # 创建文件
    def makeFile(self, filename, size=None):
        try:
            size = int(size)
            if -1 != self.getDirIndex():
                i = self.getDirIndex()
            else:
                raise ValueError

            if not self.checkFileName(filename):
                raise NameError
        except TypeError:
            print("请检查输入。")
        except NameError:
            print("已存在重名文件！")
        except ValueError:
            print("当前路径异常！")
        else:
            if self.filemanagement.checkFileSize(size): # 文件大小合理
                date = dt.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
                inode = INode(date=date, ftype=1, size=size, index_block=self.dir_count)
                self.tree[i].inode.append(inode)
                self.tree[i].dir_item.append(FileName(filename))
                fnode = FNode(size=size)
                self.tree[i].dir_item[self.tree[i].dir_num].next = fnode
                # 对文件进行磁盘块分配
                self.filemanagement.fileAllocation(fnode=fnode)
                self.tree[i].dir_num += 1
                self.dir_count += 1
            else:
                print("文件大小不合理，不予以分配磁盘块。")
        finally:
            pass

    def checkFileName(self, filename):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            dir_length = self.tree[i].dir_num
            for j in range(dir_length):
                if self.tree[i].inode[j].getFtype() == 1 and\
                        filename == self.tree[i].dir_item[j].getName():
                    return False
        return True

    # 删除文件，并且回收磁盘块
    def delFile(self, file_name):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()

            dir_length = self.tree[i].dir_num
            # print(self.tree[i].getAbsoluteName())
            for j in range(2, dir_length):
                if file_name == self.tree[i].dir_item[j].getName():

                    fnode = self.tree[i].dir_item[j].next
                    self.filemanagement.recyleBlock(fnode)
                    self.tree[i].inode.pop(j)
                    self.tree[i].dir_item.pop(j)
                    self.tree[i].dir_num -= 1
                    break
                elif j == dir_length - 1:
                    print("无此文件！")

    # 改变当前工作目录
    def changeDirectory(self, dir_name=None):
        try:

            if -1 != self.getDirIndex():
                i = self.getDirIndex()
            if dir_name == None:
                raise TypeError
        except TypeError:
            print("缺少一个路径参数。")
        else:
            dir_length = self.tree[i].dir_num
            for j in range(2, dir_length):
                if dir_name == self.tree[i].dir_item[j].getName() and \
                        self.tree[i].inode[j].getFtype() != 0:
                    self.current_dir += '/' + dir_name
                    print(self.current_dir)
                    break
                elif j == dir_length - 1:
                    print("不存在此路径！")


    # 返回上一层目录
    def backLastDirectory(self):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            # if 0 != i:
            name_str = self.tree[i].getAbsoluteName()
            name_list = name_str.split('/')
            if len(name_list) >= 2:
                name_list.pop()
                self.current_dir = '/'.join(name_list)
                # parent_index = self.tree[i].inode[1].getIndexBlock()
                # parent_dir = self.tree[parent_index].getAbsoluteName()
                # self.current_dir = parent_dir

    # 移除空目录，若此目录下还有其他目录，则不能移除
    def removeDirectory(self, dir_name):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            dir_length = self.tree[i].dir_num
            print(self.tree[i].getAbsoluteName())
            for j in range(2, dir_length):
                if dir_name == self.tree[i].dir_item[j].getName():
                    # 获得要删除目录的绝对路径名
                    ab_name = self.current_dir + '/' + dir_name
                    index_dir = self.getDirIndex(ab_name)
                    # pop_dir = self.tree.pop(index_dir)
                    if self.tree[index_dir].dir_num == 2:
                        self.tree.pop(index_dir)
                        self.tree[i].inode.pop(j)
                        self.tree[i].dir_item.pop(j)
                        self.tree[i].dir_num -= 1
                        # 文件类型置为0，表示已被删除
                        # self.tree[i].inode[j].setFtype(0)
                        print(ab_name, "已删除")
                    else:
                        print("当前目录不为空，不可删除！")
                    break
                elif j == dir_length - 1:
                    print("无此目录！")

    # 输出树目录，即命令tree
    def showTreeDir(self):
        self.tree_str = ''
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            # dir_length = self.tree[i].dir_num
            dir_length = len(self.tree[i].dir_item)
            for j in range(2, dir_length):
                if self.tree[i].inode[j].getFtype() == 2:
                    pathname = self.tree[i].dir_item[j].getName()
                    ab_name = self.tree[i].getAbsoluteName() + '/' + pathname
                    dir_index = self.getDirIndex(ab_name)
                    # dir_index = self.tree[i].inode[j].getIndexBlock()
                    self.TreeDir(dir_index, pathname)
            print(self.tree_str)

    def TreeDir(self, i, pathname, n=1):
        if self.tree[i].dir_num == 2:
            self.tree_str += '    |' * n + '-' * 4 + pathname + '\n'
        elif self.tree[i].dir_num > 2:
            dir_length = self.tree[i].dir_num
            self.tree_str += '    |' * n + '-' * 4 + pathname + '\n'
            # i = self.getDirIndex(self.tree[i].getAbsoluteName())
            # print(self.tree[i].getAbsoluteName(), " : ", i)
            if -1 != i:
                for j in range(2, dir_length):
                    if self.tree[i].inode[j].getFtype() == 2:
                        # dir_index = self.tree[i].inode[j].getIndexBlock()
                        pathname = self.tree[i].dir_item[j].getName()
                        ab_name = self.tree[i].getAbsoluteName() + '/' + pathname
                        print("ab_name: ", ab_name)
                        dir_index = self.getDirIndex(ab_name)
                        self.TreeDir(dir_index, pathname, n+1)


    # 输出当前目录下的目录, dir
    def showCurrentDir(self):
        if -1 != self.getDirIndex():
            i = self.getDirIndex()
            dir_length = self.tree[i].dir_num
            print("目录：", self.tree[i].getAbsoluteName())
            for j in range(dir_length):
                if self.tree[i].inode[j].getFtype() != 0:
                    print(self.tree[i].inode[j], '\t', self.tree[i].dir_item[j].getName())

    def showDirItem(self):
        for it in self.tree:
            if it.dir_num >= 2:
                print(it.getAbsoluteName())
                for i in range(it.dir_num):
                    if it.inode[i].getFtype() != 0:
                        print(it.inode[i], '\t', it.dir_item[i].getName())

    def help(self):
        tips = {'mk': "makeFile",
                'md': "makeDirectory",
                'cd':"changeDirectory",
                'rd': "removeDirectory",
                'del': "delFile",
                'cd..': "backLastDirectory",
                'dir': "showCurrentDir",
                'ls': "showCurrentDir",
                'tree': "showTreeDir",
                'show': "showDirItem",
                'help': "help",
                'exit': "exit"}
        for it in tips.items():
            print(it)

    def exit(self):
        print("OVER...")
        exit(0)

    def makeATest(self):
        func = {'mk': self.makeFile,
                'md': self.makeDirectory,
                'cd': self.changeDirectory,
                'rd': self.removeDirectory,
                'del': self.delFile,
                'cd..': self.backLastDirectory,
                'dir': self.showCurrentDir,
                'ls': self.showCurrentDir,
                'tree': self.showTreeDir,
                'show': self.showDirItem,
                'help': self.help,
                'exit': self.exit}

        while True:
            commend = input(self.current_dir + " >> ").strip().split()
            # print(commend)
            if len(commend) == 3:
                fun = func.get(commend[0], 0)
                if 0 != fun:
                    fun(commend[1], commend[2])
            elif len(commend) == 2:
                fun = func.get(commend[0], 0)
                if 0 != fun:
                    fun(commend[1])
            elif len(commend) == 1:
                fun = func.get(commend[0], 0)
                if 0 != fun:
                    fun()
                else:
                    print("Wrong Commend!")


if __name__ == '__main__':
    a = TreeDirectory()
    a.init()
    a.filemanagement.initBitMap()
    a.makeATest()
