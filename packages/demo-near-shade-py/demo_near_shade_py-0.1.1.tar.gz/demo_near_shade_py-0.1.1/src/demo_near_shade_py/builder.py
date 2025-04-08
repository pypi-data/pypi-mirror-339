class AgentBuilder:
    def __init__(self):
        self._config = {}

    def set_private_key(self, key: str):
        self._config['private_key'] = key
        return self

    def set_contract(self, address: str):
        self._config['contract'] = address
        return self

    def build(self):
        return Agent(**self._config)


class Agent:
    def __init__(self, private_key: str, contract: str):
        self.private_key = private_key
        self.contract = contract

    def run(self):
        print(f"Running agent with contract {self.contract}")
