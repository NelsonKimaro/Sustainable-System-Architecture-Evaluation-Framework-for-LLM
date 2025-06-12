class TotalCarbonModel:
    def __init__(self, embodied_model, operational_model):
        self.embodied_model = embodied_model
        self.operational_model = operational_model

    def calculate_total_carbon(self) -> float:
        return (self.embodied_model.calculate_carbon() + self.operational_model.calculate_carbon())
