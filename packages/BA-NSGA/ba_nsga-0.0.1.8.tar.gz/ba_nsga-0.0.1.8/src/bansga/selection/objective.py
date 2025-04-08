import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cdist
from sage_lib.partition.Partition import Partition
from scipy.spatial import ConvexHull

def objective_energy(scale=1.0):
    """
    Returns a function that computes the (scaled) total energy of each structure.

    Parameters
    ----------
    scale : float
        Factor by which to scale the energy value.

    Returns
    -------
    callable
        A function that accepts a list of structures and returns an ndarray
        of shape (N, ), containing scaled energies.
    """
    def compute(structures):
        values = []
        for s in structures:
            # Suppose 'E' is the total energy stored in AtomPositionManager
            E = getattr(s.AtomPositionManager, 'E', 0.0)
            values.append(scale * E)
        return np.array(values)
    return compute


def objective_formation_energy(reference_potentials=None):
    """
    Returns a function to compute formation energy based on reference chemical potentials.

    Parameters
    ----------
    reference_potentials : dict or None
        Mapping from atom symbol to chemical potential value. For example:
        {'Fe': -3.72, 'Ni': -4.55, ...}
        If None, will return raw energies.

    Returns
    -------
    callable
        A function that accepts a list of structures and returns an ndarray
        of shape (N, ), representing formation energies.
    """
    def compute(structures):
        values = []

        partition = Partition()
        partition.containers = structures
        
        X = np.array([
            [
                np.count_nonzero(structure.AtomPositionManager.atomLabelsList == label)
                for label in partition.uniqueAtomLabels
            ]
            for structure in structures
            ])
        y = np.array([getattr(s.AtomPositionManager, 'E', 0.0) for s in structures])
        
        if reference_potentials is not None:
            # Subtract the sum of reference potentials from total energy
            chemical_potentials = np.array([reference_potentials.get(ual, 0) for ual in partition.uniqueAtomLabels])
            formation_energies = y - X.dot(chemical_potentials)
        else:
            model = Ridge(alpha=1e-5, fit_intercept=False)
            model.fit(X, y)
            chemical_potentials = model.coef_
            formation_energies = y - X.dot(chemical_potentials)

        return np.array(formation_energies)

    return compute


def objective_min_distance_to_hull(reference_potentials:dict=None, variable_species:str=None, A:float=None, mu_range:list=None, steps=20):
    """

    """
    def compute(
        structures,
    ):
        """
        Computes the minimum distance to the convex hull for each structure while varying
        the chemical potential (mu) of exactly one species. All other species use fixed 
        (reference) chemical potentials. Formation-energy calculations are vectorized to
        improve efficiency.

        Parameters
        ----------
        structures : list
            A list of objects containing:
              - structure.AtomPositionManager.atomLabelsList (array of atomic labels)
              - structure.AtomPositionManager.E (float energy)
        reference_potentials : dict
            Reference chemical potentials keyed by species label, e.g. {'A': -3.0, 'B': -2.5}
        variable_species : str
            The species whose chemical potential is varied.
        mu_range : (float, float)
            The (start, end) range for the variable chemical potential.
        steps : int
            Number of discrete mu steps to sample in mu_range.

        Returns
        -------
        min_distances : np.ndarray, shape (N,)
            For each structure (out of N), the minimal distance to the hull found over all 
            tested mu values.
        """

        # 1) Collect structures and get unique labels
        partition = Partition()
        partition.containers = structures
        unique_labels = partition.uniqueAtomLabels
        if not variable_species in unique_labels:
            unique_labels.append(variable_species)

        # 2) Build composition matrix X and energy array y
        #    X[i, j] = # of atoms of species j in structure i
        #    y[i]    = total energy of structure i
        N_structs = len(structures)
        M_species = len(unique_labels)
        X = np.zeros((N_structs, M_species), dtype=float)
        y = np.zeros(N_structs, dtype=float)
        
        for i, struct in enumerate(structures):
            y[i] = getattr(struct.AtomPositionManager, 'E', 0.0)
            labels_array = struct.AtomPositionManager.atomLabelsList
            for j, lbl in enumerate(unique_labels):
                X[i, j] = np.count_nonzero(labels_array == lbl)
        
        # 3) Identify index of the species we vary and prepare reference chemical potentials
        try:
            var_index = unique_labels.index(variable_species)
        except ValueError:
            raise ValueError(f"Species '{variable_species}' not found in unique labels {unique_labels}.")
        
        base_chem_pots = np.array([reference_potentials.get(lbl, 0.0) for lbl in unique_labels])
        
        # --- We will treat the variable species' chemical potential as an addition to 
        #     whatever reference value it has. If you want mu_range to represent the *entire* 
        #     potential (instead of just an offset), adjust accordingly. ---
        
        # 4) Precompute the formation energy offset for everything but the variable species
        #    so that we do not repeatedly recalculate the full dot product.
        #    formation_energy_if_mu_var_were_zero = y - X @ base_chem_pots_zeroed
        #    where base_chem_pots_zeroed has 0 for var_index, but reference values for others.
        base_chem_pots_zeroed = base_chem_pots.copy()
        base_chem_pots_zeroed[var_index] = 0.0
        fE_ref = y - X.dot(base_chem_pots_zeroed)  # shape: (N,)
        
        # 5) Prepare data structures for loop over mu
        min_distances = np.full(N_structs, np.inf, dtype=float)
        mu_values = np.linspace(mu_range[0], mu_range[1], steps)
        
        # 6) Define a function for distance above/below hull
        def distance_above_hull(compositions, energies):
            """
            Returns the 'above-hull' distance for each point in compositions+energies
            using a geometric approach. 
            In practice for materials, you'd typically compute 'energy above hull' at
            each composition. This geometric method is a demonstration for d-dimensional 
            hulls. 
            """
            # We treat compositions as shape (N, M), energies as shape (N,)
            # Points for hull: shape (N, M+1)
            points = np.hstack([compositions, energies[:, None]])
            hull = ConvexHull(points)
            
            # Prepare array for distances of each point from the lower hull
            above_hull_dist = np.zeros(len(points), dtype=float)
            
            # For each hull facet, we get an equation eq: (a_0, a_1, ..., a_(M+1)) 
            # so that eq[0]*x0 + eq[1]*x1 + ... + eq[M]*energy + eq[M+1] = 0
            # We'll check which side of the facet is 'above' vs 'below'. 
            # In principle, you'd filter for 'lower hull' facets. 
            for simplex in hull.simplices:
                eq = hull.equations[simplex]       # shape (M+2,) for M+1 dims
                norm_eq = np.linalg.norm(eq[:-1])  # ignoring the constant term eq[-1]
                
                # Evaluate signed distance for all points
                signed_dist = (points @ eq[:-1] + eq[-1]) / norm_eq
                
                # Determine orientation: if eq for the energy dimension is < 0, 
                # we treat it as a 'lower' facet. (You may need to adapt the sign test.)
                # eq[-2] is often the coefficient for the last 'energy' dimension
                # if you appended compositions first. Adjust as needed.
                if eq[-2] < 0.0:
                    # Keep only positive distances; negative means point is inside/under.
                    # For each point, track the maximum distance above any 'lower' facet.
                    # This effectively measures how far outside the hull the point sits.
                    mask_pos = signed_dist > above_hull_dist
                    above_hull_dist[mask_pos] = signed_dist[mask_pos]
            
            return above_hull_dist
        
        # 7) Main loop over sampled mu values (the new formation-energy computations are vectorized)
        #    The hull must be recomputed for each mu, but the formation-energy calculations are fast.
        fE_array = np.zeros( (N_structs, steps) )
        fE_hull = np.zeros( steps )
        for mu_var_i, mu_var in enumerate(mu_values):
            # If base_chem_pots[var_index] is the reference, then total mu for that species = 
            # base_chem_pots[var_index] + mu_var. 
            # => The variable part is mu_var itself.  
            
            # fE for each structure: 
            #    fE = [ precomputed reference part ] - X[:, var_index]*mu_var - [ reference contribution for var species ]
            # However, we already omitted var species from 'fE_ref'; 
            # so now just subtract (X[:, var_index]* (base_chem_pots[var_index] + mu_var)) 
            # if you want the entire potential; 
            # or subtract X[:, var_index]*mu_var if mu_values are offsets from reference, etc.
            
            total_var_pot = base_chem_pots[var_index] + mu_var
            fE = fE_ref - X[:, var_index] * total_var_pot  # shape: (N,)
            fE_array[:, mu_var_i] = fE / A
            fE_hull[mu_var_i] = np.min(fE_array[:, mu_var_i])
            # (Optional) Reintroduce the reference for the variable species if needed:
            #   fE -= X[:, var_index] * base_chem_pots[var_index]
            # but in this approach we've accounted for everything in fE_ref and total_var_pot.
            
            # Build the hull in composition+energy space. 
            # You can choose raw counts X or normalized fractions. 
        min_distances = np.min(fE_array - fE_hull[np.newaxis, :], axis=1)


        import matplotlib.pyplot as plt
        for n in range(N_structs):
            plt.plot(mu_values, fE_array[n,:])
        print(min_distances)
        print(fE_ref/ A)
        plt.show()

        return min_distances

    return compute

def objective_anomality():
    """
    """
    def compute(structures):

        return min_dist
    return compute




