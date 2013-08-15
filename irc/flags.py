user_modes = "CDFGNRSUWXabcdfgijklnopqrsuwxyz"
channel_modes = "BIMNORSabcehiklmnopqstvz"

import config, re


class FlagList: # 
    _list = None
    _type = "b"
    _useRegex = False
    def __init__(self, type, useRegex=False):
        self._list = []
        self._type = type
        self._useRegex = useRegex
    def add(self, item):
        if len(self._list) >= 250:
            return False
        else:
            if self._useRegex:
                self._list.append((item, re.compile(item.replace(".", "\\.").replace("*", ".*"))))
            else:
                self._list.append(item)
            return True
    def remove(self, item):
        try:
            if self._useRegex:
                i = 0
                for litem in self._list:
                    if litem[0] == item:
                        self._list.pop(i)
                        return True
                    i = i + 1
                return False
            else:
                self._list.remove(item)
            return True
        except:
            return False

    def match(self, subject):
        if not self._useRegex:
            try:
                self._list.index(subject)
                return True
            except:
                return False
        else:
            for litem in self._list:
                if litem[1].match(subject) != None:
                    return True
            return False

