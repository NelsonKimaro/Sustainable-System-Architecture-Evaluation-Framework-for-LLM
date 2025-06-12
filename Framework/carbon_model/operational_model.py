
from carbon_model.carbon_base import CarbonModel

class OperationalCarbonModel(CarbonModel):
    def __init__(self, energy_usage_kwh: float, CI_op: float): #CI_op in Kg CO2 per Kwh
        self.energy_usage_kwh = energy_usage_kwh
        self.CI_op = CI_op

    def calculate_carbon(self) -> float:
        total_operational = round((self.energy_usage_kwh * self.CI_op),4)
        return total_operational


   