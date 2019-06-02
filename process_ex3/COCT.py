# CO Control Table
from IONode import IONode


class COCT(IONode):
    def __init__(self, name, status=0, pcb_name=None):
        IONode.__init__(self, name, status, pcb_name)

# co = COCT("key")
# print(co)
