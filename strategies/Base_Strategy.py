class BaseStrategy:

    stocks = []

    def initialize(self, context):
        pass
    

    def handle_data(self, context, data):
        # This is called every minute
        pass

    def _test_args(self):
        # Defines the start and the end date
        pass

    def analyze(self, context, perf):
        pass

