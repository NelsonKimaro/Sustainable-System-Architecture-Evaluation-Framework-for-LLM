import pandas as pd
from carbon_model.embodied_model import EmbodiedCarbonModel
from carbon_model.operational_model import OperationalCarbonModel
from carbon_model.total_carbon_model import TotalCarbonModel

def process_total_carbon(operational_path: str, embodied_path: str, output_path: str):
    df_op = pd.read_csv(operational_path)
    df_emb = pd.read_csv(embodied_path)

    # Sanity check
    if len(df_op) != len(df_emb):
        raise ValueError("Mismatch: operational and embodied data must have same number of rows.")
    
    # Output records
    results = []

    for i in range(len(df_op)):
        #  Read Operational Data 
        op_row = df_op.iloc[i]
        operational_model = OperationalCarbonModel(
            energy_usage_kwh = op_row['energy_usage_kwh'],
            CI_op = op_row['CI_op'])
        operational_carbon = operational_model.calculate_carbon()

        #  Read Embodied Data 
        emb_row = df_emb.iloc[i]
        embodied_model = EmbodiedCarbonModel(
            Nr = emb_row['Nr'],
            Kr = emb_row['Kr'],
            chip_area = emb_row['chip_area'],
            CI_fab = emb_row['CI_fab'],
            EPA = emb_row['EPA'],
            GPA = emb_row['GPA'],
            MPA = emb_row['MPA'],
            Y = emb_row['Y'],
            CPS_DRAM = emb_row['CPS_DRAM'],
            CPS_HDD = emb_row['CPS_HDD'],
            CPS_SSD = emb_row['CPS_SSD'],
            capacity_DRAM = emb_row['capacity_DRAM'],
            capacity_HDD = emb_row['capacity_HDD'],
            capacity_SSD = emb_row['capacity_SSD'])
        embodied_carbon = embodied_model.calculate_carbon()

        #  Total Carbon 
        total_model = TotalCarbonModel(embodied_model, operational_model,op_row['hardware_life_time'])
        total_carbon = total_model.calculate_total_carbon()

        #  Combine Results 
        result = {
            'embodied_carbon': f"{embodied_carbon}Kg CO2e",
            'operational_carbon': f"{operational_carbon}Kg CO2e",
            'total_carbon': f"{round(total_carbon,4)}Kg CO2e"
        }

        # Merge original row data too
        result.update(op_row.to_dict())
        result.update(emb_row.to_dict())

        results.append(result)

    # Create final DataFrame and save
    df_result = pd.DataFrame(results)
    df_result.to_csv(output_path, index=False)
    print(f"✅ Carbon results saved to: {output_path}")


if __name__ == "__main__":
    process_total_carbon(
        operational_path=r"carbon_model/data/operational_input_data.csv",
        embodied_path=r"carbon_model/data/embodied_input_data.csv",
        output_path=r"carbon_model/data/carbon_results.csv"
    )

    
