from pysyncobj import SyncObj, replicated


class Storage(SyncObj):
    def __init__(self, selfNode, otherNodes, lock_manager):
        super(Storage, self).__init__(selfNode, otherNodes, consumers=[lock_manager])
        self.__data = dict()

    def get(self, key):
        return self.__data.get(key, None)

    def keys(self):
        return list(self.__data.keys())

    @replicated
    def set(self, key, value):
        self.__data[key] = value

    @replicated
    def pop(self, key):
        del self.__data[key]

    @replicated
    def clear(self):
        self.__data = dict()