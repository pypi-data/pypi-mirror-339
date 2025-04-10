import unittest
from ..src.treepruner import (prune_tree_CPA, prune_tree_PSFA)
from ..src.utils import NEWICK_TREE

class TestPruneTree(unittest.TestCase):
    

    def test_prune_tree(self): 
        #Test if pruning runs without error and returns expected results.
        output_file, percentage_remaining = prune_tree_PSFA(NEWICK_TREE)

        self.assertGreater(percentage_remaining, 0)  # Ensure some tree remains after pruning
    
    def tearDown(self):
        #Cleanup test files.
        import os
        os.remove("psfa_tree.newick")

if __name__ == "__main__":
    unittest.main()
