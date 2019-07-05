class Rank0Warpper:

    def __init__(self, inner: T):
        self._inner = inner

    def __getattr__(self, name):
        # print(f'call logger {name}')
        # return do_nothing
        return getattr(self._inner, name)
