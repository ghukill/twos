class SensorValue:
    def __init__(self, name: str, value: float, unit: str):
        self.name = name
        self.value = value
        self.unit = unit
    
    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit
        }
    
    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"