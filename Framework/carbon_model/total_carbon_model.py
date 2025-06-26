class TotalCarbonModel:
    def __init__(self, embodied_model, operational_model,hardware_life_time): #execution_time must be in ms
        self.embodied_model = embodied_model
        self.operational_model = operational_model
        self.hardware_life_time = hardware_life_time

    def calculate_total_carbon(self) -> float:
        # hardware_life_time_in_ms = (self.hardware_life_time * 3285619200) #convert harware life time from years to milliseconds, 1 year = 52.143 weeks
        #return (self.operational_model.calculate_carbon() + ((self.active_time/self.hardware_life_time)*(self.embodied_model.calculate_carbon())))
        return (self.hardware_life_time * (self.operational_model.calculate_carbon()) + self.embodied_model.calculate_carbon())