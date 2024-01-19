import Observable

class ObservableList(Observable):
    def __init__(self):
        super().__init__()
        self._data = []

    def set_data(self, new_data):
        self._data = new_data
        self.notify_observers(self._data)

    def get_data(self):
        return self._data


