from carbon_model.carbon_base import CarbonModel
import pandas as pd

class EmbodiedCarbonModel(CarbonModel):
    def __init__(self, 
                 Nr: float, 
                 Kr: float,
                 chip_area: float,
                 CI_fab: float,
                 EPA: float,
                 GPA: float,
                 MPA: float,
                 Y: float,
                 CPS_DRAM: float,
                 CPS_HDD: float,
                 CPS_SSD: float,
                 capacity_DRAM: float,
                 capacity_HDD: float,
                 capacity_SSD: float):
        self.Nr = Nr
        self.Kr = Kr
        self.chip_area = chip_area
        self.CI_fab = CI_fab
        self.EPA = EPA
        self.GPA = GPA
        self.MPA = MPA
        self.Y = Y
        self.CPS_DRAM = CPS_DRAM
        self.CPS_HDD = CPS_HDD
        self.CPS_SSD = CPS_SSD
        self.capacity_DRAM = capacity_DRAM
        self.capacity_HDD = capacity_HDD
        self.capacity_SSD = capacity_SSD

    def calculate_carbon(self) ->float:
        total_embodied = round((self.packaging_em() + self.processor_em() + self.memory_em()),5)
        return total_embodied

    def packaging_em(self) ->float:
        return self.Nr * self.Kr
    
    def processor_em(self) -> float:
        return (1/self.Y) * (((self.CI_fab * self.EPA) + self.GPA + self.MPA) * self.chip_area)
    
    def memory_em(self) -> float:
        return ((self.CPS_DRAM * self.capacity_DRAM) + (self.CPS_HDD * self.capacity_HDD) + (self.CPS_SSD * self.capacity_SSD))
        


    # @classmethod
    # def from_embodied_data_csv(cls, filepath: str, row_index: int=0):
    #     df = pd.read_csv(filepath)
    #     row = df.iloc[row_index]
    #     return cls(
    #         materials_data = 
    #     )

