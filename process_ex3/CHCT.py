# Channel Control Table
from IONode import IONode
class CHCT(IONode):
    def __init__(self, name, status=0, pcb_name=None):
        IONode.__init__(self, name, status, pcb_name)


# co = CHCT("key")
# print(co)