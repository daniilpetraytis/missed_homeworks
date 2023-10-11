class BaseRepo:
    def add(self, entity):
        raise NotImplementedError

    def remove(self, entity):
        raise NotImplementedError

    def get_by_id(self, table, id):
        raise NotImplementedError

    def list(self, table):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError
