class Metric:
    def __init__(self, compute_fn):
        self.compute_fn = compute_fn

    def update(self, output, target):
        pass

    def compute(self):
        pass
