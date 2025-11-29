class StatesReq:

    def __init__(self):
        self.ctx_data = {}

class StatesResp:

    def __init__(self):
        self.states = []
        self.row_count = 0
        self.status = "Success"
        self.ctx_data = {}

    def add_response_time(self, ctx_name, resp_time):
        if "response_times" not in self.ctx_data:
            self.ctx_data["response_times"] = []
        self.ctx_data["response_times"].append({ctx_name: resp_time})
