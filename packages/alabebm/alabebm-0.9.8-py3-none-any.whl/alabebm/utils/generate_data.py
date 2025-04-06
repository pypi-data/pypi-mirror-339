from typing import List, Optional, Tuple, Dict, Union, Any
import json 
import pandas as pd 
import numpy as np 
import os 
from collections import Counter, defaultdict

# List of supported experiment configurations
experiment_names = [
    "sn_kjOrdinalDM_xnjNormal",     # Experiment 1: Ordinal kj with Dirichlet-Multinomial, Normal Xnj
    "sn_kjOrdinalDM_xnjNonNormal",  # Experiment 2: Ordinal kj with Dirichlet-Multinomial, Non-Normal Xnj
    "sn_kjOrdinalUniform_xnjNormal", # Experiment 3: Ordinal kj with Uniform distribution, Normal Xnj
    "sn_kjOrdinalUniform_xnjNonNormal", # Experiment 4: Ordinal kj with Uniform distribution, Non-Normal Xnj
    "sn_kjContinuousUniform",       # Experiment 5: Continuous kj with Uniform distribution
    "sn_kjContinuousBeta",          # Experiment 6: Continuous kj with Beta distribution
    "xiNearNormal_kjContinuousUniform", # Experiment 7: Near-normal Xi with Continuous Uniform kj
    "xiNearNormal_kjContinuousBeta", # Experiment 8: Near-normal Xi with Continuous Beta kj
]

def very_irregular_distribution(
    biomarker: str, 
    bm_params: Dict[str, float], 
    state: str = "affected", 
    size: int = 100000, 
    rng: Optional[np.random.Generator] = None
) -> np.ndarray:
    """
    Generate highly irregular, non-normal samples for a given biomarker and state.
    
    This function creates complex, multi-modal distributions by combining different 
    probability distributions and transformations. Each biomarker receives a 
    custom-designed irregular distribution to simulate realistic biomarker behavior.
    
    Args:
        biomarker: The biomarker identifier (e.g., "MMSE", "AB", "HIP-FCI")
        bm_params: Dictionary containing distribution parameters (means and standard deviations)
        state: Whether the samples are for "affected" or "nonaffected" participants
        size: Number of samples to generate
        rng: Random number generator (if None, a new one will be created)
    
    Returns:
        np.ndarray: An array of irregularly distributed values with the requested size
    """
    if rng is None:
        rng = np.random.default_rng()

    # Select appropriate parameters based on disease state
    mean = bm_params["theta_mean"] if state == "affected" else bm_params["phi_mean"]
    std = bm_params["theta_std"] if state == "affected" else bm_params["phi_std"]

    # Initialize output array and split indices for multi-modal distributions
    base = np.zeros(size)
    segment_1, segment_2, segment_3 = np.array_split(np.arange(size), 3)

    # --- Highly non-normal design per biomarker ---
    if biomarker in ["MMSE", "ADAS"]:
        # Cognitive tests: Triangular + Normal + Exponential mixture
        base[segment_1] = rng.triangular(mean - 2*std, mean - 1.5*std, mean, size=len(segment_1))
        base[segment_2] = rng.normal(mean + std, 0.3 * std, size=len(segment_2))
        base[segment_3] = rng.exponential(scale=0.7 * std, size=len(segment_3)) + mean - 0.5 * std

    elif biomarker in ["AB", "P-Tau"]:
        # CSF biomarkers: Pareto + Uniform + Logistic mixture
        base[segment_1] = rng.pareto(1.5, size=len(segment_1)) * std + mean - 2 * std
        base[segment_2] = rng.uniform(mean - 1.5 * std, mean + 1.5 * std, size=len(segment_2))
        base[segment_3] = rng.logistic(loc=mean, scale=std, size=len(segment_3))

    elif biomarker in ["HIP-FCI", "HIP-GMI"]:
        # Hippocampus metrics: Beta + Exponential + Modified normal
        base[segment_1] = rng.beta(0.5, 0.5, size=len(segment_1)) * 4 * std + mean - 2 * std
        base[segment_2] = rng.exponential(scale=std * 0.4, size=len(segment_2)) * rng.choice([-1, 1], size=len(segment_2)) + mean
        base[segment_3] = rng.normal(mean, std * 0.5, size=len(segment_3)) + rng.choice([0, std * 2], size=len(segment_3))

    elif biomarker in ["AVLT-Sum", "PCC-FCI"]:
        # Memory and PCC metrics: Gamma + Weibull + Normal with spikes
        base[segment_1] = rng.gamma(shape=2, scale=0.5 * std, size=len(segment_1)) + mean - std
        base[segment_2] = rng.weibull(1.0, size=len(segment_2)) * std + mean - std
        base[segment_3] = rng.normal(mean, std * 0.5, size=len(segment_3)) + rng.choice([-1, 1], size=len(segment_3)) * std

    elif biomarker == "FUS-GMI":
        # Fusiform gyrus GMI: Heavy-tailed Cauchy with normal noise
        raw = rng.standard_cauchy(size=size) * std + mean
        raw += rng.normal(0, 0.2 * std, size=size)
        base = np.clip(raw, mean - 4 * std, mean + 4 * std)

    elif biomarker == "FUS-FCI":
        # Fusiform gyrus FCI: Bimodal with sharp spike
        spike_size = size // 10
        base[:spike_size] = rng.normal(mean, 0.2 * std, size=spike_size)
        base[spike_size:] = rng.logistic(loc=mean + std, scale=2 * std, size=size - spike_size)

    else:
        # Default for any other biomarker: Uniform distribution
        base = rng.uniform(mean - 2 * std, mean + 2 * std, size=size)

    # --- Add irregular noise and clip to reasonable range ---
    base += rng.normal(0, 0.2 * std, size=size)  # extra randomness
    base = np.clip(base, mean - 5 * std, mean + 5 * std)

    return base

def generate_measurements_kjOrdinal(
    params: Dict[str, Dict[str, float]], 
    event_time_dict: Dict[str, float], 
    shuffled_biomarkers: np.ndarray, 
    experiment_name: str, 
    all_kjs: np.ndarray, 
    all_diseased: np.ndarray, 
    keep_all_cols: bool, 
    rng: Optional[np.random.Generator] = None
) -> List[Dict[str, Any]]:
    """
    Generate measurements for the ordinal kj experiment types.
    
    This function creates biomarker measurements for each participant based on
    their disease status and disease stage (kj), following the ordinal stage model.
    
    Args:
        params: Dictionary of biomarker parameters
        event_time_dict: Dictionary mapping biomarkers to their event times
        shuffled_biomarkers: Array of biomarkers in randomized order
        experiment_name: Name of the experiment being run
        all_kjs: Array of disease stages for all participants
        all_diseased: Boolean array indicating disease status of participants
        keep_all_cols: Whether to include additional columns in output
        rng: Random number generator
        
    Returns:
        List of dictionaries containing measurement data for all participants and biomarkers
    """
    if rng is None:
        rng = np.random.default_rng()

    data = []
    # Pre-generate non-normal distributions for faster sampling if needed
    irreg_dict = defaultdict(dict)
    if "xnjNonNormal" in experiment_name:
        disease_states = ['affected', 'nonaffected']
        for biomarker in shuffled_biomarkers:
            bm_params = params[biomarker]
            for state in disease_states:
                irreg_dict[biomarker][state] = very_irregular_distribution(
                    biomarker, bm_params, state=state, rng=rng)

    for participant_id, (disease_stage, is_diseased) in enumerate(zip(all_kjs, all_diseased)):
        for biomarker in shuffled_biomarkers:
            bm_params = params[biomarker]
            event_time = event_time_dict[biomarker]
            
            # Determine measurement state based on disease stage vs event time
            if is_diseased and disease_stage >= event_time:
                state = "affected"
                distribution_param = 'theta'  # Parameter for affected state
            else:
                state = "nonaffected"
                distribution_param = 'phi'    # Parameter for non-affected state

            # Generate measurement based on experiment type
            if 'xnjNormal' in experiment_name:
                # Normal distribution sampling
                measurement = rng.normal(
                    bm_params[f"{distribution_param}_mean"], 
                    bm_params[f"{distribution_param}_std"]
                )
            else:
                # Non-normal distribution sampling from pre-generated distributions
                measurement = rng.choice(irreg_dict[biomarker][state], size=1)[0]
            
            # Build data record
            record = {
                "participant": participant_id,
                "biomarker": biomarker,
                "measurement": measurement,
                "diseased": is_diseased,
            }
            
            # Add additional columns if requested
            if keep_all_cols:
                record.update({
                    "event_time": event_time,
                    "k_j": disease_stage,
                    "affected": disease_stage >= event_time
                })
            data.append(record)
    return data

def generate_measurements_kjContinuous(
    event_time_dict: Dict[str, float],
    all_kjs: np.ndarray,
    all_diseased: np.ndarray,
    shuffled_biomarkers: np.ndarray,
    params: Dict[str, Dict[str, float]],
    keep_all_cols: bool,
    rng: Optional[np.random.Generator] = None
) -> List[Dict[str, Any]]:
    """
    Generate measurements for the continuous kj experiment types.
    
    This function creates biomarker measurements for each participant using a
    sigmoid progression model for diseased participants, based on their disease
    stage (continuous kj value).
    
    Args:
        event_time_dict: Dictionary mapping biomarkers to their event times
        all_kjs: Array of disease stages for all participants (continuous values)
        all_diseased: Boolean array indicating disease status of participants
        shuffled_biomarkers: Array of biomarkers in randomized order
        params: Dictionary of biomarker parameters
        keep_all_cols: Whether to include additional columns in output
        rng: Random number generator
        
    Returns:
        List of dictionaries containing measurement data for all participants and biomarkers
    """
    if rng is None:
        rng = np.random.default_rng()
    
    data = []
    for participant_id, (disease_stage, is_diseased) in enumerate(zip(all_kjs, all_diseased)):
        for biomarker_idx, biomarker in enumerate(shuffled_biomarkers):
            event_time = event_time_dict[biomarker]
            bm_params = params[biomarker]
            
            # Generate baseline healthy measurement
            healthy_measurement = rng.normal(bm_params["phi_mean"], bm_params["phi_std"])
            
            if is_diseased:
                # For diseased participants: apply sigmoid progression model
                # The further the disease stage is beyond the event time, the larger the effect
                progression_magnitude = bm_params["R_i"]  # Maximum progression effect
                progression_rate = bm_params["rho_i"]     # Rate of progression
                
                # Sigmoid function for disease progression
                sigmoid_term = progression_magnitude / (1 + np.exp(-progression_rate * (disease_stage - event_time)))
                measurement = sigmoid_term + healthy_measurement
            else:
                # For healthy participants: just use the healthy baseline measurement
                measurement = healthy_measurement
                
            # Build data record
            record = {
                "participant": participant_id,
                "biomarker": biomarker,
                "measurement": measurement,
                "diseased": is_diseased,
            }
            
            # Add additional columns if requested
            if keep_all_cols:
                record.update({
                    "event_time": event_time,
                    "k_j": disease_stage,
                    "affected": disease_stage >= event_time
                })
            
            data.append(record)
    return data 

def generate_data(
    experiment_name: str,
    params_file: str,
    n_participants: int,
    healthy_ratio: float,
    output_dir: str,
    m: int,  # combstr_m
    seed: int,
    dirichlet_alpha: Dict[str, List[float]],
    beta_params: Dict[str, Dict[str, float]],
    prefix: Optional[str],
    suffix: Optional[str],
    keep_all_cols: bool,
    bm_event_time_dicts: Dict[str, Dict[str, int]],
) -> pd.DataFrame:
    """
    Simulate an Event-Based Model (EBM) for disease progression and generate a dataset.
    
    This function generates a dataset for a specific experiment configuration, 
    participant count, and healthy ratio. It handles the simulation of disease 
    stages, biomarker ordering, and creates measurements for each participant.

    Args:
        experiment_name: Identifier for the experiment type
        params_file: Path to the JSON file containing biomarker parameters
        n_participants: Total number of participants to simulate
        healthy_ratio: Proportion of participants to be simulated as healthy
        output_dir: Directory to save the resulting CSV
        m: Dataset variant number (for generating multiple datasets with same parameters)
        seed: Random seed for reproducibility
        dirichlet_alpha: Parameters for Dirichlet distribution for stage distribution
        beta_params: Parameters for various Beta distributions used in the simulations
        prefix: Optional prefix for the output filename
        suffix: Optional suffix for the output filename
        keep_all_cols: Whether to include additional metadata columns in the output
        bm_event_time_dicts: Dictionary to store the true biomarker ordering for evaluation
    
    Returns:
        pd.DataFrame: The generated dataset
    """
    # Parameter validation
    assert n_participants > 0, "Number of participants must be greater than 0."
    assert 0 <= healthy_ratio <= 1, "Healthy ratio must be between 0 and 1."
    assert experiment_name in experiment_names, "Wrong experiment name!"

    # Initialize random number generator
    rng = np.random.default_rng(seed)

    # Load biomarker parameters from file
    with open(params_file) as f:
        params = json.load(f)

    # Randomly shuffle biomarkers to create a ground truth ordering
    shuffled_biomarkers = rng.permutation(np.array(list(params.keys())))
    max_stage = len(shuffled_biomarkers)
    event_times = np.arange(1, max_stage+1)

    # Calculate counts of healthy and diseased participants
    n_healthy = int(n_participants * healthy_ratio)
    n_diseased = n_participants - n_healthy

    # ================================================================
    # Core generation logic based on experiment type
    # ================================================================

    if "kjOrdinal" in experiment_name:
        # Ordinal disease stage experiments (stages are discrete integers)
        
        # Assign event times to biomarkers in shuffled order
        event_time_dict = dict(zip(shuffled_biomarkers, event_times))
        
        # Generate stage distribution for diseased participants
        if 'Uniform' in experiment_name:
            # Use uniform Dirichlet prior (all stages equally likely)
            if len(dirichlet_alpha['uniform']) != max_stage:
                # If alpha parameter count doesn't match stages, replicate the first value
                dirichlet_alphas = [dirichlet_alpha['uniform'][0]] * max_stage
            else:
                dirichlet_alphas = dirichlet_alpha['uniform']
            stage_probs = rng.dirichlet(dirichlet_alphas)
        else:
            # Use multinomial Dirichlet prior (custom stage distribution)
            stage_probs = rng.dirichlet(dirichlet_alpha['multinomial'])
            
        # Sample from multinomial to get actual stage counts
        stage_counts = rng.multinomial(n_diseased, stage_probs)
        
        # Create array of stages (1 to max_stage) for diseased participants
        disease_stages = np.repeat(np.arange(1, max_stage + 1), stage_counts)
        
        # Combine with healthy participants (stage 0)
        all_kjs = np.concatenate([np.zeros(n_healthy), disease_stages])
        all_diseased = all_kjs > 0 

        # Shuffle participant order
        shuffle_idx = rng.permutation(n_participants)
        all_kjs = all_kjs[shuffle_idx]
        all_diseased = all_diseased[shuffle_idx]

        # Generate measurements for all participants and biomarkers
        data = generate_measurements_kjOrdinal(
            params, event_time_dict, shuffled_biomarkers, experiment_name, all_kjs, 
            all_diseased, keep_all_cols, rng=rng)
    
    else:
        # Continuous disease stage experiments (stages are real numbers)
        
        # Generate continuous event times for biomarkers
        if experiment_name.startswith('xi'):
            # Use beta distribution for near-normal event times
            event_time_raw = rng.beta(
                a=beta_params['near_normal']['alpha'], 
                b=beta_params['near_normal']['beta'], 
                size=max_stage)
            # Scale to [0, max_stage]
            event_times = np.clip(event_time_raw * max_stage, 0, max_stage)
        
        # Assign event times to biomarkers
        event_time_dict = dict(zip(shuffled_biomarkers, event_times))

        # Generate continuous disease stages (kj) for diseased participants
        if 'kjContinuousUniform' in experiment_name:
            # Use uniform-like beta for disease stages
            disease_stages_raw = rng.beta(
                a=beta_params['uniform']['alpha'],
                b=beta_params['uniform']['beta'],
                size=n_diseased
            )
        else:
            # Use skewed beta for disease stages
            disease_stages_raw = rng.beta(
                a=beta_params['regular']['alpha'],
                b=beta_params['regular']['beta'],
                size=n_diseased
            )
            
        # Scale disease stages to [0, max_stage]
        disease_stages = np.clip(disease_stages_raw * max_stage, 0, max_stage)

        # Combine with healthy participants (stage 0)
        all_kjs = np.concatenate([np.zeros(n_healthy), disease_stages])
        all_diseased = all_kjs > 0 

        # Shuffle participant order
        shuffle_idx = rng.permutation(n_participants)
        all_kjs = all_kjs[shuffle_idx]
        all_diseased = all_diseased[shuffle_idx]

        # Generate measurements using continuous disease progression model
        data = generate_measurements_kjContinuous(
            event_time_dict, all_kjs, all_diseased, shuffled_biomarkers, params, keep_all_cols, rng=rng)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    
    # Construct filename with parameters encoded
    filename = f"j{n_participants}_r{healthy_ratio}_E{experiment_name}_m{m}"
    if prefix: 
        filename = f"{prefix}_{filename}"
    if suffix: 
        filename = f"{filename}_{suffix}"
    
    # Write to CSV
    df.to_csv(os.path.join(output_dir, f"{filename}.csv"), index=False)

    # Store the ground truth biomarker ordering for evaluation
    # Sort biomarkers by their event time and assign ordinal, sequential indices (1-based)
    bm_event_time_dicts[filename] = dict(zip(
        sorted(event_time_dict, key=lambda x: event_time_dict[x]), 
        np.arange(1, max_stage + 1)))

    return df

def generate(
    experiment_name: str = "sn_kjOrdinalDM_xnjNormal",
    params_file: str = 'params.json',
    js: List[int] = [50, 200, 500, 1000],
    rs: List[float] = [0.1, 0.25, 0.5, 0.75, 0.9],
    num_of_datasets_per_combination: int = 50,
    output_dir: str = 'data',
    seed: Optional[int] = None,
    dirichlet_alpha: Optional[Dict[str, List[float]]] = {
        'uniform': [100], 
        'multinomial':[0.4013728324975898,
                      1.0910444770153345,
                      2.30974117596663,
                      3.8081194066281103,
                      4.889722107892335,
                      4.889722107892335,
                      3.8081194066281103,
                      2.30974117596663,
                      1.0910444770153345,
                      0.4013728324975898]
    },
    beta_params: Dict[str, Dict[str, float]] = {
        'near_normal': {'alpha': 2.0, 'beta': 2.0},
        'uniform': {'alpha': 1, 'beta': 1},
        'regular': {'alpha': 5, 'beta': 2}
    },
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    keep_all_cols: bool = False 
) -> Dict[str, Dict[str, int]]:
    """
    Generate multiple datasets for different experimental configurations.
    
    This function creates a suite of datasets with varying parameters for comprehensive
    evaluation of Event-Based Models (EBMs). It generates datasets for all combinations
    of participant counts, healthy ratios, and variants specified.
    
    Args:
        experiment_name: Type of experiment to run (see experiment_names for valid options)
        params_file: Path to JSON file with biomarker parameters
        js: List of participant counts to generate data for
        rs: List of healthy ratios to generate data for
        num_of_datasets_per_combination: Number of dataset variants to generate per parameter combination
        output_dir: Directory to save generated CSV files
        seed: Master random seed (if None, a random seed will be generated)
        dirichlet_alpha: Parameters for Dirichlet distributions:
            - 'uniform': For uniform stage distribution
            - 'multinomial': For non-uniform stage distribution
        beta_params: Parameters for Beta distributions:
            - 'near_normal': For event times close to normal distribution
            - 'uniform': For approximately uniform distribution
            - 'regular': For skewed distribution
        prefix: Optional prefix for all filenames
        suffix: Optional suffix for all filenames
        keep_all_cols: Whether to include additional metadata columns (k_j, event_time, affected)
        
    Returns:
        Dict mapping filenames to dictionaries of biomarker event time orderings
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize master random number generator
    if seed is None:
        seed = np.random.SeedSequence().entropy 
    rng = np.random.default_rng(seed)

    # Dictionary to store the ground truth biomarker orderings
    # Structure: {filename: {biomarker: event_time_position}}
    bm_event_time_dicts = {}

    # Generate datasets for all parameter combinations
    for participant_count in js:
        for healthy_ratio in rs:
            for variant in range(num_of_datasets_per_combination):
                # Generate a unique seed for each dataset
                sub_seed = rng.integers(0, 1_000_000)
                
                # Generate a single dataset with the current parameter combination
                generate_data(
                    experiment_name=experiment_name,
                    params_file=params_file,
                    n_participants=participant_count,
                    healthy_ratio=healthy_ratio,
                    output_dir=output_dir,
                    m=variant,
                    seed=sub_seed,
                    dirichlet_alpha=dirichlet_alpha,
                    beta_params=beta_params,
                    prefix=prefix,
                    suffix=suffix,
                    keep_all_cols=keep_all_cols,
                    bm_event_time_dicts=bm_event_time_dicts,
                )
                
    print(f"Data generation complete. Files saved in {output_dir}/")
    return bm_event_time_dicts