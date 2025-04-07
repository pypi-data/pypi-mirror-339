import numpy as np
from sklearn.metrics import pairwise_distances

def hash_colition_penalization():
    pass

def evaluate_objectives(structures, objectives_funcs):
    if isinstance(objectives_funcs, list):  
        return np.array([func(structures) for func in objectives_funcs]).T
    else:
        return np.array([objectives_funcs(structures)])

def naive_objectives(structures, objectives_funcs):
    return np.ones( (self.partitions['dataset'].size, len(objectives_funcs)) )

def evaluate_features(structures, features_funcs):
    return np.array([features_funcs(structure) for structure in structures])

def compute_repulsion(candidates_features, selected_features, metric='euclidean', mode='min', invert=True):
    """
    Computes how 'repelled' each candidate is with respect to an already-selected set,
    using some distance measure in a feature space.

    If selected_features is empty, repulsion can be set to 0 or no effect.

    Parameters
    ----------
    candidates_features : np.ndarray
        2D array (Nc, D), where Nc is the number of candidates not yet selected,
        and D is the dimension of the feature space (e.g., composition).
    selected_features : np.ndarray
        2D array (Ns, D), the feature vectors of already-selected structures.
    metric : str, optional
        Distance metric (passed to scikit-learn pairwise_distances), by default 'euclidean'.
    mode : str, optional
        How to combine distances to the selected set. Options:
            'avg' -> average distance
            'min' -> minimum distance
            'max' -> maximum distance
    invert : bool, optional
        If True, compute repulsion as 1 / (distance + eps). If False, use the raw distance.

    Returns
    -------
    np.ndarray
        1D array of length Nc giving each candidate's repulsion with respect to the selected set.
        Higher means more "unique" or "repelled" from the set.
    """
    eps = 1e-12
    Nc = candidates_features.shape[0]

    # If nothing is selected yet, repulsion is zero or you could define it as 1.0
    if selected_features.size == 0:
        return np.zeros(Nc)

    # Distances between each candidate and each selected structure
    dist_matrix = pairwise_distances(candidates_features, selected_features, metric=metric)

    # Combine distances across all selected
    if mode == 'avg':
        dist_value = dist_matrix.mean(axis=1)
    elif mode == 'min':
        dist_value = dist_matrix.min(axis=1)
    elif mode == 'max':
        dist_value = dist_matrix.max(axis=1)
    else:
        raise ValueError("Unsupported mode. Choose among 'avg', 'min', 'max'.")

    if invert:
        repulsion_values = 1.0 / (dist_value + eps)
    else:
        repulsion_values = dist_value

    return repulsion_values

def select_multiobjective_iterative(objectives,
                                    features,
                                    weights=None,
                                    repulsion_weight=0.0,
                                    temperature=1.0,
                                    num_select=10,
                                    repulsion_mode='avg',
                                    metric='euclidean',
                                    random_seed=None):
    """
    Iteratively selects 'num_select' structures from a set of candidates by:
      1) Combining user-defined objectives into a single cost.
      2) Incorporating repulsion from already-selected structures each iteration.
      3) Sampling one candidate at a time from a Boltzmann-like probability distribution.

    Parameters
    ----------
    objectives : np.ndarray
        Shape (N, K). 'K' objectives, each column is a "lower is better" score
        (already enforced by evaluate_objectives).
    features : np.ndarray
        Shape (N, D). Feature vectors for each candidate, used for the repulsion calculation.
    weights : list or np.ndarray, optional
        Weights for each of the K objectives. Must be length K if specified.
        If None, all objectives are weighted equally.
    repulsion_weight : float, optional
        Weight controlling how strongly repulsion (diversity) is rewarded,
        by default 0.0 (i.e., no diversity encouragement).
    temperature : float, optional
        Boltzmann-like temperature for sampling, by default 1.0.
    num_select : int, optional
        Number of structures to select, by default 10.
    repulsion_mode : str, optional
        How repulsion is computed: 'avg', 'min', or 'max'. By default 'avg'.
    metric : str, optional
        Distance metric used for repulsion, by default 'euclidean'.
    random_seed : int or None, optional
        Seed for reproducibility, by default None.

    Returns
    -------
    selected_indices : list
        Indices of the selected structures in the same order they appear in 'objectives' and 'features'.
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    N, K = objectives.shape
    if weights is None:
        weights = np.ones(K) / K
    else:
        weights = np.array(weights, dtype=float)
        if weights.shape[0] != K:
            raise ValueError("Length of `weights` must match number of objectives (K).")

    if temperature < 0:
        temperature = 0

    # ---- Step 1: Normalize each objective to [0..1] so that 0 is best, 1 is worst ----
    # We do min-max normalization per column:
    eps = 1e-12

    # We'll keep track of which candidates remain
    candidate_indices = np.arange(N)
    selected_indices = []

    # Keep a separate array of boolean or something for "not selected yet"
    not_selected_mask = np.ones(N, dtype=bool)

    # We'll store the features of the selected structures so we can recompute repulsion each time
    selected_features = np.empty((0, features.shape[1]))

    # ---- Step 2: Iteratively pick one structure at a time ----
    for _ in range(num_select):
        # 2a) For each candidate not in the selected set, compute final cost
        norm_objectives = np.zeros_like(objectives[not_selected_mask])
        for j in range(K):
            col = objectives[not_selected_mask][:, j]
            cmin, cmax = col.min(), col.max()
            spread = cmax - cmin
            if spread < eps:
                # If all are identical, it doesn't affect selection
                norm_objectives[:, j] = 0.0
            else:
                norm_objectives[:, j] = (col - cmin) / spread

        # Weighted sum of normalized objectives:
        # The lower it is, the better
        partial_cost = np.dot(norm_objectives, weights)

        # If repulsion is used, compute it for the not-yet-selected candidates
        if repulsion_weight > 0.0 and selected_features.size > 0:
            # The subset of features for the not-yet-selected
            sub_features = features[not_selected_mask]
            # Compute a repulsion value for each candidate with respect to the structures in selected_features
            repulsion_vals = compute_repulsion(
                candidates_features=sub_features,
                selected_features=selected_features,
                metric=metric,
                mode=repulsion_mode,
                invert=True  # if True, repulsion = 1/dist
            )
            # Higher repulsion -> we want to *reduce the cost* so it's more likely to be picked
            # So final cost = partial_cost - repulsion_weight * normalized_repulsion
            rmin, rmax = repulsion_vals.min(), repulsion_vals.max()
            if rmax - rmin < eps:
                repulsion_norm = np.zeros_like(repulsion_vals)
            else:
                repulsion_norm = (repulsion_vals - rmin) / (rmax - rmin + eps)

            final_cost = partial_cost - repulsion_weight * repulsion_norm
        else:
            # No repulsion or no selected structures => cost is just from objectives
            final_cost = partial_cost

        # 2b) Convert cost to probabilities: p_i ~ exp(-cost_i / T)
        cost_scaled = final_cost / (temperature + eps)
        probs = np.exp(-cost_scaled)
        sum_probs = probs.sum()
        if sum_probs < eps:
            # fallback to uniform if everything is effectively zero
            probs = np.ones_like(probs) / len(probs)
        else:
            probs /= sum_probs

        # 2c) Sample exactly one candidate from these probabilities
        local_indices = np.where(not_selected_mask)[0]  # The actual global indices of the not-selected
        chosen_local = np.random.choice(len(local_indices), p=probs)
        chosen_global = local_indices[chosen_local]

        # 2d) Mark that candidate as selected
        selected_indices.append(chosen_global)
        not_selected_mask[chosen_global] = False

        # Update selected_features to include the chosen one
        selected_features = np.vstack([selected_features, features[chosen_global]])

    return np.array(selected_indices)

import numpy as np
from sklearn.metrics import pairwise_distances

class EvolutionToolkit:
    """
    A robust toolkit that provides methods for evaluating objectives, evaluating features,
    computing repulsion in feature space, selecting structures according to a multi-objective
    scheme, and penalizing genetic operators that produce hash collisions.

    It also provides extra functionalities for advanced control over the selection process.
    """

    def __init__(self, logger=None):
        """
        Initializes the toolkit with optional logger for debug or info messages.

        Parameters
        ----------
        logger : object, optional
            A logger with .info(), .debug() methods. If None, print statements can be used.
        """
        self.logger = logger

        # Track any relevant stats across multiple calls
        self.collisions_count = 0
        self.extra_tracking = {}

    # -------------------------------------------------------------------------
    # Original Methods Refactored as Class Methods
    # -------------------------------------------------------------------------

    def hash_collision_penalization(self, structure, operator_probabilities, alpha=0.05):
        """
        Reduces the usage probability of whichever genetic operator created this duplicate structure.

        This is called when a hash collision (duplicate structure) is detected.

        Parameters
        ----------
        structure : object
            The structure that triggered a hash collision. We expect
            `structure.AtomPositionManager.metadata["operation"]`
            to indicate "mutation" or "crossover", and possibly the index in
            `structure.AtomPositionManager.metadata["mutation_list"]` or `"crossover_idx"]`.
        operator_probabilities : dict
            Dictionary containing operator probabilities, e.g.:
            {
                "mutation_probs": np.ndarray,  # Probability distribution for each mutation operator
                "crossover_probs": np.ndarray, # Probability distribution for each crossover operator
            }
        alpha : float, optional
            The penalty factor. Probabilities are multiplied by (1 - alpha). By default 0.05.
        """
        meta = structure.AtomPositionManager.metadata
        operation_type = meta.get("operation", "unknown")

        if operation_type == "mutation":
            # structure may have been created by multiple mutation operators
            mutation_list = meta.get("mutation_list", [])
            for idx in mutation_list:
                operator_probabilities["mutation_probs"][idx] *= (1.0 - alpha)

            # If you want to track total collisions for debugging
            self.collisions_count += 1
            if self.logger:
                self.logger.info(f"Hash collision for mutation. Penalized operators: {mutation_list}")

            # Re-normalize
            probs = operator_probabilities["mutation_probs"]
            sum_probs = probs.sum()
            if sum_probs > 1e-12:
                operator_probabilities["mutation_probs"] = probs / sum_probs

        elif operation_type == "crossover":
            co_idx = meta.get("crossover_idx", None)
            if co_idx is not None:
                operator_probabilities["crossover_probs"][co_idx] *= (1.0 - alpha)
                self.collisions_count += 1
                if self.logger:
                    self.logger.info(f"Hash collision for crossover. Penalized operator idx: {co_idx}")

                # Re-normalize
                probs = operator_probabilities["crossover_probs"]
                sum_probs = probs.sum()
                if sum_probs > 1e-12:
                    operator_probabilities["crossover_probs"] = probs / sum_probs

        else:
            # Unknown or untracked operation
            if self.logger:
                self.logger.info("Hash collision detected, but operation is unknown. No penalty applied.")

    def evaluate_objectives(self, structures, objectives_funcs):
        """
        Evaluates the given list of structures using a user-supplied objective function.

        Parameters
        ----------
        structures : list
            List of structures to evaluate.
        objectives_funcs : callable
            A function or callable that, given a list of structures,
            returns an (N, K) array of objective values.

        Returns
        -------
        np.ndarray
            (N, K) array, where N is the number of structures and K the number of objective columns.
        """
        return objectives_funcs(structures)

    def evaluate_features(self, structures, features_funcs):
        """
        Evaluates the given list of structures using a user-supplied feature extractor function.

        Parameters
        ----------
        structures : list
            List of structures to evaluate.
        features_funcs : callable
            A function or callable that, given a list of structures,
            returns an (N, D) array of features.

        Returns
        -------
        np.ndarray
            (N, D) array of feature vectors, one row per structure.
        """
        return features_funcs(structures)

    def compute_repulsion(
        self,
        candidates_features,
        selected_features,
        metric='euclidean',
        mode='min',
        invert=True
    ):
        """
        Computes how 'repelled' each candidate is from an already-selected set, using
        a distance measure in feature space.

        Parameters
        ----------
        candidates_features : np.ndarray
            Shape (Nc, D). Feature vectors for the unselected candidate structures.
        selected_features : np.ndarray
            Shape (Ns, D). Feature vectors of already-selected structures.
        metric : str, optional
            Distance metric (passed to scikit-learn `pairwise_distances`), by default 'euclidean'.
        mode : str, optional
            How to combine candidate-to-selected distances. Valid:
                'avg' -> average distance
                'min' -> minimum distance
                'max' -> maximum distance
        invert : bool, optional
            If True, repulsion = 1.0 / (distance + eps). If False, uses the raw distance.

        Returns
        -------
        np.ndarray
            1D array of length Nc giving each candidate's repulsion measure.
        """
        eps = 1e-12
        Nc = candidates_features.shape[0]

        # If nothing is selected yet, repulsion is zero
        if selected_features.size == 0:
            return np.zeros(Nc)

        # Distances between each candidate and each selected structure
        dist_matrix = pairwise_distances(candidates_features, selected_features, metric=metric)

        # Combine distances
        if mode == 'avg':
            dist_value = dist_matrix.mean(axis=1)
        elif mode == 'min':
            dist_value = dist_matrix.min(axis=1)
        elif mode == 'max':
            dist_value = dist_matrix.max(axis=1)
        else:
            raise ValueError("Unsupported mode. Choose among 'avg', 'min', 'max'.")

        if invert:
            repulsion_values = 1.0 / (dist_value + eps)
        else:
            repulsion_values = dist_value

        return repulsion_values

    def select_multiobjective_iterative(
        self,
        objectives,
        features,
        weights=None,
        repulsion_weight=0.0,
        temperature=1.0,
        num_select=10,
        repulsion_mode='avg',
        metric='euclidean',
        random_seed=None
    ):
        """
        Iteratively selects 'num_select' structures from a set of candidates by:
          1) Combining user-defined objectives into a single cost.
          2) Incorporating repulsion from already-selected structures each iteration.
          3) Sampling one candidate at a time from a Boltzmann-like probability distribution.

        Parameters
        ----------
        objectives : np.ndarray
            Shape (N, K). 'K' objectives, each column is "lower is better".
        features : np.ndarray
            Shape (N, D). Feature vectors for each candidate.
        weights : list or np.ndarray, optional
            Weights for each of the K objectives. Must be length K if specified.
            If None, all objectives are weighted equally.
        repulsion_weight : float, optional
            Weight controlling how strongly repulsion (diversity) is rewarded, by default 0.0.
        temperature : float, optional
            Boltzmann-like temperature for sampling, by default 1.0.
        num_select : int, optional
            Number of structures to select, by default 10.
        repulsion_mode : str, optional
            How repulsion is computed: 'avg', 'min', or 'max'. By default 'avg'.
        metric : str, optional
            Distance metric used for repulsion, by default 'euclidean'.
        random_seed : int or None, optional
            Seed for reproducibility, by default None.

        Returns
        -------
        np.ndarray
            Array of selected indices in the same order they appear in 'objectives' and 'features'.
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        N, K = objectives.shape
        eps = 1e-12

        # If weights not given, uniform weighting
        if weights is None:
            weights = np.ones(K) / K
        else:
            weights = np.array(weights, dtype=float)
            if weights.shape[0] != K:
                raise ValueError("Length of `weights` must match number of objectives (K).")

        # ---- Step 1: Normalize each objective to [0..1] so that 0 is best, 1 is worst ----
        norm_objectives = np.zeros_like(objectives)
        for j in range(K):
            col = objectives[:, j]
            cmin, cmax = col.min(), col.max()
            spread = cmax - cmin
            if spread < eps:
                # If all are identical, set to zero
                norm_objectives[:, j] = 0.0
            else:
                norm_objectives[:, j] = (col - cmin) / spread

        candidate_indices = np.arange(N)
        selected_indices = []
        not_selected_mask = np.ones(N, dtype=bool)
        selected_features = np.empty((0, features.shape[1]))

        # ---- Step 2: Iteratively pick one structure at a time ----
        for _ in range(num_select):
            # Weighted sum of normalized objectives => partial_cost
            partial_cost = np.dot(norm_objectives[not_selected_mask], weights)

            # If repulsion is used and we already have selected structures
            if repulsion_weight > 0.0 and selected_features.size > 0:
                sub_features = features[not_selected_mask]
                repulsion_vals = self.compute_repulsion(
                    candidates_features=sub_features,
                    selected_features=selected_features,
                    metric=metric,
                    mode=repulsion_mode,
                    invert=True
                )
                # Normalize repulsion for a consistent scale
                rmin, rmax = repulsion_vals.min(), repulsion_vals.max()
                if rmax - rmin < eps:
                    repulsion_norm = np.zeros_like(repulsion_vals)
                else:
                    repulsion_norm = (repulsion_vals - rmin) / (rmax - rmin + eps)

                # final_cost = partial_cost - repulsion_weight * normalized_repulsion
                final_cost = partial_cost - repulsion_weight * repulsion_norm
            else:
                final_cost = partial_cost

            # Convert cost to probabilities: p_i ~ exp(-cost_i / T)
            cost_scaled = final_cost / (temperature + eps)
            probs = np.exp(-cost_scaled)
            sum_probs = probs.sum()
            if sum_probs < eps:
                # fallback to uniform if everything is effectively zero
                probs = np.ones_like(probs) / len(probs)
            else:
                probs /= sum_probs

            local_indices = np.where(not_selected_mask)[0]
            chosen_local = np.random.choice(len(local_indices), p=probs)
            chosen_global = local_indices[chosen_local]

            # Mark that candidate as selected
            selected_indices.append(chosen_global)
            not_selected_mask[chosen_global] = False

            # Update selected_features
            selected_features = np.vstack([selected_features, features[chosen_global]])

        return np.array(selected_indices)

    # -------------------------------------------------------------------------
    # New Functionalities (Five Extra Methods)
    # -------------------------------------------------------------------------

    def advanced_rescaling(self, objectives, scale_type='log', base=10.0):
        """
        NEW FUNCTIONALITY (1): Apply an advanced scaling to the objective values.

        Parameters
        ----------
        objectives : np.ndarray
            (N, K) array. Each column is a separate objective.
        scale_type : str, optional
            Type of scaling. Options:
                'log' -> log base 'base'
                'sqrt' -> sqrt scaling
                'none' -> no scaling
        base : float, optional
            The base for logarithmic scaling.

        Returns
        -------
        np.ndarray
            The scaled objectives array.
        """
        scaled = objectives.copy()
        eps = 1e-12

        if scale_type == 'log':
            # log(base(x + eps)) to avoid zero or negative
            scaled = np.log(scaled + eps) / np.log(base)
        elif scale_type == 'sqrt':
            scaled = np.sqrt(np.maximum(scaled, 0))
        elif scale_type == 'none':
            # no change
            pass
        else:
            raise ValueError(f"Unknown scale_type '{scale_type}'")

        if self.logger:
            self.logger.info(f"Applied {scale_type} scaling to objectives.")
        return scaled

    def advanced_diversity_metric(self, features):
        """
        NEW FUNCTIONALITY (2): Compute an advanced measure of dataset diversity.

        Uses e.g. the average pairwise distance in feature space.

        Parameters
        ----------
        features : np.ndarray
            (N, D) array of feature vectors.

        Returns
        -------
        float
            The average pairwise distance among all feature vectors.
        """
        if features.shape[0] < 2:
            return 0.0
        dist_mat = pairwise_distances(features, metric='euclidean')
        tri_indices = np.triu_indices(dist_mat.shape[0], k=1)
        mean_dist = dist_mat[tri_indices].mean()
        if self.logger:
            self.logger.info(f"Average pairwise diversity in features: {mean_dist:.4f}")
        return mean_dist

    def partial_selection(
        self, 
        objectives, 
        features, 
        ratio=0.5, 
        selection_method="best"
    ):
        """
        NEW FUNCTIONALITY (3): Quickly select a fraction of candidates based on a simple heuristic
        such as 'best objective sum' or 'random selection'.

        Parameters
        ----------
        objectives : np.ndarray
            (N, K) array of objective values.
        features : np.ndarray
            (N, D) array of feature vectors (only used for dimension checking or advanced logic).
        ratio : float, optional
            Fraction (0..1) of how many items to select.
        selection_method : str, optional
            How to pick structures:
                'best' -> sorts by sum of objectives and picks the best fraction
                'random' -> picks a random fraction
                'worst' -> picks the worst fraction by sum of objectives
        Returns
        -------
        np.ndarray
            Indices of the selected structures.
        """
        N = objectives.shape[0]
        num_to_select = int(np.ceil(N * ratio))
        if num_to_select <= 0:
            return np.array([], dtype=int)

        sums = objectives.sum(axis=1)

        if selection_method == "best":
            sorted_indices = np.argsort(sums)  # ascending => best first
            chosen = sorted_indices[:num_to_select]
        elif selection_method == "worst":
            sorted_indices = np.argsort(sums)
            chosen = sorted_indices[-num_to_select:]
        elif selection_method == "random":
            chosen = np.random.choice(N, size=num_to_select, replace=False)
        else:
            raise ValueError(f"Unknown selection_method '{selection_method}'")

        if self.logger:
            self.logger.info(
                f"Partial selection method '{selection_method}' chosen. "
                f"Selected {num_to_select} out of {N} total."
            )
        return chosen

    def multi_objective_aggregator(self, objectives, mode="sum_of_squares"):
        """
        NEW FUNCTIONALITY (4): Combine multiple objectives into a single scalar using advanced schemes.

        Parameters
        ----------
        objectives : np.ndarray
            (N, K) array of objective values. Lower is better.
        mode : str, optional
            The aggregator mode. Options:
                "sum_of_squares" -> sum of squares of each objective
                "l2_norm" -> Euclidean norm
                "l1_norm" -> sum of absolute values

        Returns
        -------
        np.ndarray
            A 1D array of length N giving the aggregated cost for each item.
        """
        if mode == "sum_of_squares":
            combined = np.sum(objectives**2, axis=1)
        elif mode == "l2_norm":
            combined = np.sqrt(np.sum(objectives**2, axis=1))
        elif mode == "l1_norm":
            combined = np.sum(np.abs(objectives), axis=1)
        else:
            raise ValueError(f"Unknown aggregator mode '{mode}'")

        if self.logger:
            self.logger.info(f"Aggregated objectives with mode={mode}.")
        return combined

    def specialized_sanity_check(self, objectives, features):
        """
        NEW FUNCTIONALITY (5): Perform a quick sanity check on the shapes and range of the
        objectives and features arrays, ensuring they're not empty or NaN.

        Parameters
        ----------
        objectives : np.ndarray
            (N, K) array of objective values.
        features : np.ndarray
            (N, D) array of feature vectors.

        Raises
        ------
        ValueError
            If shapes don't match or if arrays have NaNs/inf.
        """
        if objectives.shape[0] != features.shape[0]:
            raise ValueError("Number of rows in objectives and features must match.")
        if not np.isfinite(objectives).all():
            raise ValueError("Objectives array contains non-finite values (NaN/inf).")
        if not np.isfinite(features).all():
            raise ValueError("Features array contains non-finite values (NaN/inf).")

        if self.logger:
            self.logger.info("Sanity check passed: shapes match and no NaNs/inf found.")


# ------------------------------------------------------------------------------
# Example usage snippet within your existing code or a main script:
# 
#   # Instantiate the toolkit (pass your logger if desired)
#   evo_toolkit = EvolutionToolkit(logger=my_logger)
#
#   # Evaluate objectives and features:
#   objectives = evo_toolkit.evaluate_objectives(structures, my_objective_func)
#   features = evo_toolkit.evaluate_features(structures, my_feature_func)
# 
#   # Perform advanced scaling or aggregator
#   scaled_objectives = evo_toolkit.advanced_rescaling(objectives, scale_type='log', base=10.0)
#   combined_cost = evo_toolkit.multi_objective_aggregator(scaled_objectives, mode="l2_norm")
#
#   # Check for collisions or partial selection
#   selected_indices = evo_toolkit.select_multiobjective_iterative(objectives, features, num_select=5)
#   partial_indices = evo_toolkit.partial_selection(objectives, features, ratio=0.4, selection_method='random')
#
#   # Example of penalizing collisions
#   operator_probs = {
#       "mutation_probs": np.array([0.33, 0.33, 0.34]),
#       "crossover_probs": np.array([0.5, 0.5])
#   }
#   # If a collision is found:
#   evo_toolkit.hash_collision_penalization(conflicting_structure, operator_probs, alpha=0.1)
#
#   # Check for any potential issues
#   evo_toolkit.specialized_sanity_check(objectives, features)
#
# ------------------------------------------------------------------------------

