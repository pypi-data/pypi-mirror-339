# qbmc/core/learning.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from SBmc import SimpleBiomimeticCell

import numpy as np
from typing import Dict, List
from .preprocessing import QBMCDataProcessor

BINSIZE = 9  # Default bin size for quantization

class QBMCLearner:
    def __init__(self, binsize: int = BINSIZE):
        self.binsize = binsize
        self.processor = QBMCDataProcessor(binsize)
        self.feature_layers = {}  # type: Dict[int, List[SimpleBiomimeticCell]]
        self.labels_bin = None
        self.labels_original = None

    def fit(self, X: np.ndarray, y: np.ndarray, debug: bool = False):
        """Main training interface that handles the complete pipeline"""
        # Convert and validate data shapes
        X = np.asarray(X)
        y = np.asarray(y).flatten()
        
        if X.shape[0] != y.shape[0]:
            X = X.T  # Transpose if features are in columns

        if X.shape[0] != y.shape[0]:
            raise ValueError("Number of samples in X and y must match.")
            
        # Preprocess data
        X_bin = self.processor.auto_convert(X)
        y_bin = self.processor.auto_convert(y.reshape(-1, 1)).squeeze(1)
        
        # Get unique labels
        self.labels_original, unique_indices = np.unique(y, return_inverse=True)
        self.labels_bin = np.unique(y_bin, axis=0)

        if debug:
            print(f"Original labels: {self.labels_original}")
            print(f"Unique binary labels:\n{self.labels_bin.astype(int)}")
            print(f"X:\n{X}")
            print(f"y: {y}")
            print(f"y_bin:\n{y_bin.astype(int)}")
            print(f"X_bin:\n{X_bin.astype(int)}")
        
        # Initialize network
        self._initialize_network(X_bin, debug)
        
        # Train network
        self._train_network(X_bin, y_bin, debug)

    def _initialize_network(self, X_bin: np.ndarray, debug: bool = False):
        """Create BMC cells for each feature-label pair"""
        self.feature_layers = {}
        
        for feature_idx in range(X_bin.shape[1]):
            self.feature_layers[feature_idx] = []
            
            for label_idx, label in enumerate(self.labels_bin):
                # Count occurrences of this label pattern
                count = np.sum(np.all(X_bin[:, feature_idx, :] == label, axis=1))
                
                # Create cell
                cell = SimpleBiomimeticCell(label_idx, self.binsize,count,self.binsize)
                cell.output(label)
                self.feature_layers[feature_idx].append(cell)
        
        if debug:
            print(f"Initialized {len(self.feature_layers)} feature layers with {len(self.labels_bin)} labels each.")
            for feature_idx, cells in self.feature_layers.items():
                print(f"Feature {feature_idx}:")
                for cell in cells:
                    print(f"  {cell}: {cell.outputArray.astype(int)}")

    def _train_network(self, X_bin: np.ndarray, y_bin: np.ndarray, debug: bool = False):
        """Learn weights for each feature-label combination"""
        for feature_idx, layer in self.feature_layers.items():
            for cell_idx, cell in enumerate(layer):
                # Find samples with matching label
                matching_mask = np.all(y_bin == self.labels_bin[cell_idx], axis=1)
                relevant_samples = X_bin[matching_mask, feature_idx, :]
                
                # Learn from these samples
                cell.learn(relevant_samples)

        if debug:
            print("Training complete. Feature layers:")
            for feature_idx, cells in self.feature_layers.items():
                print(f"Feature {feature_idx}:")
                for cell in cells:
                    print(f"  {cell}:\n{cell.weightArray.astype(int)}")

    def get_network_state(self) -> Dict:
        """Returns the learned network structure"""
        return {
            'feature_layers': self.feature_layers,
            'labels': self.labels_original,
            'binsize': self.binsize
        }
    
if __name__ == "__main__":
    print("=== Testing QBMCLearner ===")
    
    # ===== Test 1: Basic Classification =====
    print("\nTest 1: Basic Binary Classification")
    X_class = np.array([
        [0, 1, 3, 5, 7, 8],   # Feature 1
        [0, 0, 1, 0, 1, 1]    # Feature 2
    ]).T
    y_class = np.array([0, 0, 1, 0, 1, 1])
    
    clf_learner = QBMCLearner()
    clf_learner.fit(X_class, y_class, True)
    network = clf_learner.get_network_state()
    
    print("Input Features Shape:", X_class.shape)
    print("Unique Labels:", network['labels'])
    print("Feature Layers:", len(network['feature_layers']))
    print("Cells per Feature:", [len(cells) for cells in network['feature_layers'].values()])
    
    # Verify network structure
    assert len(network['feature_layers']) == 2, "Should have 2 feature layers"
    assert all(len(cells) == 2 for cells in network['feature_layers'].values()), "Should have 2 cells per feature (binary classification)"
    print("✓ Basic classification network structure verified")

    # ===== Test 2: Multi-class Classification =====
    print("\nTest 2: Multi-class Classification")
    X_multi = np.array([
        [0, 1, 2, 3, 4, 5],
        [1, 3, 5, 7, 9, 11]
    ]).T
    y_multi = np.array([0, 1, 2, 0, 1, 2])
    
    multi_learner = QBMCLearner()
    multi_learner.fit(X_multi, y_multi, True)
    multi_network = multi_learner.get_network_state()
    
    print("Unique Labels:", multi_network['labels'])
    assert len(multi_network['labels']) == 3, "Should have 3 classes"
    print("✓ Multi-class structure verified")

    # ===== Test 3: Regression =====
    print("\nTest 3: Regression (Continuous Values)")
    X_reg = np.array([
        [1, 2, 3, 5, 6, 8],
        [2, 4, 6, 10, 12, 16]
    ]).T
    y_reg = np.array([5, 7, 9, 13, 15, 19])
    
    reg_learner = QBMCLearner()
    reg_learner.fit(X_reg, y_reg, True)
    reg_network = reg_learner.get_network_state()
    
    print("Unique Output Values:", len(reg_network['labels']))
    assert len(reg_network['labels']) == 6, "Should have unique weights for each output"
    print("✓ Regression network structure verified")

    # ===== Test 4: Single Feature =====
    print("\nTest 4: Single Feature Input")
    X_single = np.array([[0, 1, 0, 1, 0, 1]]).T
    y_single = np.array([0, 1, 0, 1, 0, 1])
    
    single_learner = QBMCLearner()
    single_learner.fit(X_single, y_single, True)
    single_network = single_learner.get_network_state()
    
    assert len(single_network['feature_layers']) == 1, "Should have 1 feature layer"
    print("✓ Single feature handling verified")

    # ===== Test 5: Online Learning =====
    print("\nTest 5: Incremental Learning")
    # Initial training
    X_partial = np.array([[0, 1, 0]]).T
    y_partial = np.array([0, 1, 0])
    inc_learner = QBMCLearner()
    inc_learner.fit(X_partial, y_partial, True)
    
    # Get initial weights
    initial_weights = [cell.weightArray.copy() 
                      for cell in inc_learner.feature_layers[0]]
    
    # Additional training
    X_new = np.array([[1, 0]]).T
    y_new = np.array([1, 0])
    inc_learner.fit(X_new, y_new, True)
    
    # Verify weights changed
    new_weights = [cell.weightArray 
                  for cell in inc_learner.feature_layers[0]]
    assert not all(np.array_equal(w1, w2) for w1, w2 in zip(initial_weights, new_weights)), "Weights should have updated"
    print("✓ Incremental learning verified")

    # ===== Test 6: Edge Cases =====
    print("\nTest 6: Edge Cases")
    
    # Empty input
    try:
        empty_learner = QBMCLearner()
        empty_learner.fit(np.array([]), np.array([]), True)
        assert False, "Should have raised ValueError for empty input"
    except ValueError as e:
        print(f"✓ Empty input handling: {str(e)}")
    
    # Mismatched lengths
    try:
        mismatch_learner = QBMCLearner()
        mismatch_learner.fit(np.array([[1,2],[3,4]]), np.array([1]), True)
        assert False, "Should have raised ValueError for length mismatch"
    except ValueError as e:
        print(f"✓ Length mismatch handling: {str(e)}")

    print("\n=== All QBMCLearner tests passed successfully ===")
