from alabebm import generate, get_params_path
import os
import numpy as np 
import json 

# Get path to default parameters
params_file = get_params_path()

experiment_names = [
    "sn_kjOrdinalDM_xnjNormal", # Experiment 1
	"sn_kjOrdinalDM_xnjNonNormal", # Experiment 2
    "sn_kjOrdinalUniform_xnjNormal", # Experiment 3
	"sn_kjOrdinalUniform_xnjNonNormal", # Experiment 4
    "sn_kjContinuousUniform", # Experiment 5
	"sn_kjContinuousBeta", # Experiment 6
    "xiNearNormal_kjContinuousUniform", # Experiment 7
	"xiNearNormal_kjContinuousBeta", # Experiment 8
]

def convert_np_types(obj):
    """Convert numpy types in a nested dictionary to Python standard types."""
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return convert_np_types(obj.tolist())
    else:
        return obj

all_exp_dicts = []

for exp_name in experiment_names:
    bm_et_dict = generate(
            experiment_name = exp_name,
            params_file=params_file,
            js = [200],
            rs = [0.25],
            num_of_datasets_per_combination=2,
            output_dir='my_data',
            seed=42,
        )
    all_exp_dicts.append(bm_et_dict)

combined = {k: v for d in all_exp_dicts for k, v in d.items()}

combined = convert_np_types(combined)

# Save to a JSON file
with open("all_filename_correct_order_dicts.json", "w") as f:
    json.dump(combined, f, indent=2)  # indent=2 makes it pretty

    

