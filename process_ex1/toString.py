class AttrDisplay:
    def gatherAttrs(self):
        # return ",".join("{}={}"
        #                 .format(k, getattr(self, k))
        #                 for k in self.__dict__.keys())
        attrs = []
        # for k in self.__dict__.keys():
        #     item = "{}={}".format(k, getattr(self, k))
        #     attrs.append(item)
        # return attrs
        for k in self.__dict__.keys():
            attrs.append(str(self.__dict__[k]))
        return ",".join(attrs) if len(attrs) else 'no attr'

    def __str__(self):
        return "({}: {})".format(self.__class__.__name__, self.gatherAttrs())