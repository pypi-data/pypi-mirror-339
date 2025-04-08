import hashlib
import spglib

class CanonicalHashMap:
    """
    A manager for storing canonical hashes of periodic crystal structures
    indexed by composition. This allows efficient duplicate detection
    among structures with the *same* composition.

    In practice, you create an instance of this class, and for each
    structure (with a known composition):
        1) Compute the canonical hash via spglib standardization
        2) Store or check if it has already been stored
    using the provided methods.

    Attributes
    ----------
    symprec : float
        Symmetry tolerance used by spglib for standardizing the cell.
    _hash_map : dict
        Internal dictionary: composition_key -> set of canonical hashes.

        Each 'composition_key' is derived from a dictionary of elements
        mapping to their integer amounts (e.g., {"Fe": 2, "Co": 1})
        turned into a string such as 'Co1-Fe2'.
    """

    def __init__(self, symprec: float = 1e-2, debug: bool = False):
        """
        Initialize the CompositionHashMap with a chosen symmetry precision.

        Parameters
        ----------
        symprec : float, optional (default=1e-2)
            Symmetry detection tolerance for spglib.standardize_cell(). 
            Larger values are more lenient; smaller values are stricter.
        """
        self.symprec = symprec
        self._hash_map = {}  # { 'comp_key': set([hash1, hash2, ...]) }
        self.debug = debug
        
    @staticmethod
    def _composition_key(composition: dict) -> str:
        """
        Convert a composition dictionary (e.g., {"Fe":2, "Co":1})
        into a canonical string that can be used as a dictionary key.

        Sorting the items ensures that {"Co":1, "Fe":2} and {"Fe":2, "Co":1}
        produce the same key.

        Parameters
        ----------
        composition : dict
            Dictionary of element symbols (or IDs) mapped to integer stoichiometry.

        Returns
        -------
        str
            A canonical string representing the composition (e.g. "Co1-Fe2").
        """
        # Sort by element symbol to ensure a consistent order
        items_sorted = sorted(composition.items())  
        # Build a string like "Co1-Fe2" for the composition
        return "-".join(f"{elem}{amt}" for elem, amt in items_sorted)

    def _canonical_hash(self, container) -> str:
        """
        Compute a canonical SHA256 hash for the given periodic structure.

        This relies on spglib to standardize the crystal cell, making the
        resulting hash invariant under translations, rotations, and site
        ordering (within the tolerance 'symprec').

        The 'container' object must expose:
            container.AtomPositionManager.latticeVectors    # shape (3,3)
            container.AtomPositionManager.atomPositions_fractional  # shape (N,3)
            container.AtomPositionManager.get_atomic_numbers()       # length N

        Parameters
        ----------
        container : object
            A structure-like object which provides the necessary lattice/atom info.

        Returns
        -------
        str
            The canonical (SHA256) hash string for this structure.
        """
        # Extract lattice and atomic data (must match your container's API)
        lattice_matrix = container.AtomPositionManager.latticeVectors
        frac_coords    = container.AtomPositionManager.atomPositions_fractional
        species_list   = container.AtomPositionManager.get_atomic_numbers()

        # Prepare data for spglib
        cell = (lattice_matrix, frac_coords, species_list)

        # Standardize the cell: to_primitive=False, no_idealize=True
        # means we get a consistent orientation but do not reduce
        # the cell to the primitive or idealized form.
        std_lattice, std_coords, std_species = spglib.standardize_cell(
            cell,
            to_primitive=False,
            no_idealize=True,
            symprec=self.symprec
        )

        # Build a fingerprint from the standardized cell
        # Sort atoms by (species, x, y, z) to remove site-order ambiguity
        entries = []
        for spec, coord in zip(std_species, std_coords):
            entries.append(f"{spec}:{coord[0]:.8f},{coord[1]:.8f},{coord[2]:.8f}")
        entries.sort()

        # Flatten the standardized lattice into a single string
        lattice_str = ",".join(f"{val:.8f}" for row in std_lattice for val in row)
        # Combine lattice with sorted site list
        fingerprint = lattice_str + "|" + ";".join(entries)

        # Return the final SHA256 hash
        return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()

    def add_structure(self, container) -> bool:
        """
        Attempt to register the canonical hash of 'container' under the given composition.

        If the hash is already present, that implies this structure
        (under the same composition) is a duplicate.

        Parameters
        ----------
        container : object
            The structure to be hashed.

        Returns
        -------
        bool
            True if this is a newly added hash (i.e., not seen before),
            False if this exact structure hash was already registered 
            under the same composition.
        """
        # Build a canonical key for the composition
        comp_key = self._composition_key( container.AtomPositionManager.atomCountDict )
        # Compute the canonical hash
        hval = self._canonical_hash(container)

        # If no entry for this composition yet, create one
        if comp_key not in self._hash_map:
            self._hash_map[comp_key] = set()

        if not hasattr(container.AtomPositionManager, 'metadata'):
              container.AtomPositionManager.metadata = {}
        if not isinstance(container.AtomPositionManager.metadata, dict):
            container.AtomPositionManager.metadata = {}

        container.AtomPositionManager.metadata['hash'] = hval

        # Check if the hash is already known
        if hval in self._hash_map[comp_key]:
            # Duplicate for that composition
            return False
        else:
            # This is a new structure hash
            self._hash_map[comp_key].add(hval)
            return True

    def already_visited(self, container) -> bool:
        """
        Check whether 'container' (for the given composition) is already registered.

        This method *does not* add the structure if missing. It just tests duplication.

        Parameters
        ----------
        container : object
            The structure to be hashed.

        Returns
        -------
        bool
            True if the structure's hash is already known for this composition,
            False otherwise.
        """
        # Build the composition key
        comp_key = self._composition_key(container.AtomPositionManager.atomCountDict)
        # If composition not seen, it can't be visited
        if comp_key not in self._hash_map:
            return False

        # Compute hash
        hval = self._canonical_hash(container)
        # Return True if it exists in the set, else False
        return (hval in self._hash_map[comp_key])

    def get_num_structures_for_composition(self, composition: dict) -> int:
        """
        Retrieve how many *unique* structures have been registered under 'composition'.

        Parameters
        ----------
        composition : dict
            The composition to query, e.g. {"Fe":2, "Co":1}.

        Returns
        -------
        int
            The count of distinct structure hashes for that composition.
        """
        comp_key = self._composition_key(composition)
        if comp_key not in self._hash_map:
            return 0
        return len(self._hash_map[comp_key])

    def total_compositions(self) -> int:
        """
        Return how many distinct compositions are currently registered.

        Returns
        -------
        int
            The number of unique composition keys in this HashMap.
        """
        return len(self._hash_map)
