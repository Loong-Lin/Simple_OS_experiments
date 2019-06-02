class NameError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return "There is already exited " + self.errorinfo

# if __name__ == '__main__':
#     try:
#         raise CustomError('客户异常')
#     except CustomError as e:
#         print(e)