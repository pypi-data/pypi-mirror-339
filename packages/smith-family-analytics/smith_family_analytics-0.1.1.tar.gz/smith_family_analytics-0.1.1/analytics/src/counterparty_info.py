import json


class CounterPartyInfo:
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Deserialize a dictionary to create a CounterPartyInfo instance.
        """
        return CounterPartyInfo(
            source=data.get("source"),  # Retrieve the 'source' key from the dictionary
            target=data.get("target"),  # Retrieve the 'target' key from the dictionary
        )
