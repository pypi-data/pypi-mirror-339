from alabebm import run_ebm
from alabebm.data import get_sample_data_path, get_params_path
from alabebm.utils.runners import extract_fname
import os
import json 

cwd = os.getcwd()
print("Current Working Directory:", cwd)
data_dir = f"{cwd}/alabebm/test/my_data"
data_files = os.listdir(data_dir) 

params_file = get_params_path()

# Load parameters
with open(params_file) as f:
    biomarker_params = json.load(f)

with open(f"{cwd}/alabebm/test/all_filename_correct_order_dicts.json", "r") as f:
    all_filename_correct_order_dicts = json.load(f)

for algorithm in ['hard_kmeans', 'mle', 'conjugate_priors', 'em', 'kde']:
    for data_file in data_files:
        fname = data_file.replace('.csv', '')
        results = run_ebm(
            data_file= os.path.join(data_dir, data_file),
            algorithm=algorithm,
            n_iter=200,
            n_shuffle=2,
            burn_in=100,
            thinning=10,
            correct_ordering=all_filename_correct_order_dicts[fname],
            skip_heatmap=True,
            skip_traceplot=False
        )