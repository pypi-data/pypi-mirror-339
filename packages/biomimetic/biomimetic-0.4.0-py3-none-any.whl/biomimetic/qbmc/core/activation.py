# qbmc/core/activations.py
import numpy as np
from typing import Dict, List, Union
from preprocessing import QBMCDataProcessor
from learning import QBMCLearner

class QBMCActivator:
    def __init__(self, learner: QBMCLearner = None, classification: bool = False):
        self.learner = learner
        self.classification = classification
        self.processor = QBMCDataProcessor() if learner is None else learner.processor
        
    def predict(self, X: np.ndarray, classification: bool = False, debug: bool = False) -> np.ndarray:
        X_bin = self.processor.auto_convert(X)
        return np.array([self.forward_pass(x, classification, debug)['prediction'] for x in X_bin])

    def _calculate_matches(self, x: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """Implements the PDF's matching logic (page 7)"""
        mismatches = weights != x
        first_mismatch = np.argmax(mismatches, axis=1)
        perfect_matches = np.all(~mismatches, axis=1)
        return np.where(perfect_matches, self.learner.binsize, first_mismatch)

    def forward_pass(self, x_bin: np.ndarray, classification:bool = False, debug: bool = False) -> Dict:
        # Step 1: Find global maximum match length across ALL cells
        global_max = -1
        all_matches = []

        if debug:
            print(f"Input binary data:\n{x_bin.astype(int)}")
        
        for feature_idx, layer in self.learner.feature_layers.items():
            feature_matches = []
            for cell in layer:
                if debug:
                    print(f"Passing Through {cell} for feature {feature_idx}")
                    print(f"Having weights:\n{cell.weightArray.astype(int)}")
                    print(f"Having output: {cell.outputArray.astype(int)}")
                matches = self._calculate_matches(x_bin[feature_idx], cell.weightArray)
                feature_matches.append(matches)
                current_max = np.max(matches)
                global_max = max(global_max, current_max)
            all_matches.append(feature_matches)
        
        # Step 2: Calculate probabilities (PDF page 8)
        probabilities = np.zeros(len(self.learner.labels_original))
        
        for label_idx in range(len(self.learner.labels_original)):
            total = 0
            for feature_idx, layer in self.learner.feature_layers.items():
                cell = layer[label_idx]
                matches = all_matches[feature_idx][label_idx]
                count = np.sum(matches == global_max)
                total += count
            
            probabilities[label_idx] = total
        
        # Normalize probabilities
        probabilities /= np.sum(probabilities) if np.sum(probabilities) > 0 else 1

        if debug:
            print(f"Probabilities: {probabilities}")
            print(f"Associated labels: {self.learner.labels_original}")
        
        if classification:
            prediction = self.learner.labels_original[np.argmax(probabilities)]
        else:  # Regression
            prediction = np.dot(probabilities, self.learner.labels_original)
        
        return {
            'probabilities': probabilities,
            'prediction': prediction,
        }

if __name__ == "__main__":
    print("=== Testing QBMCActivator ===")
    
    # Test data from qbmc.pdf (classification)
    X_train_class = np.array([
        [0, 1, 3, 5, 7, 8],   # Feature 1
        [0, 0, 1, 0, 1, 1]     # Feature 2
    ]).T
    y_train_class = np.array([0, 0, 1, 0, 1, 1])
    X_test_class = np.array([
        [2, 4, 6],  # New X values
        [1, 0, 1]    # Corresponding Y indicators
    ]).T
    
    # ===== Test 1: Basic Classification =====
    print("\nTest 1: Binary Classification")
    clf_learner = QBMCLearner()
    clf_learner.fit(X_train_class, y_train_class)
    
    activator = QBMCActivator(clf_learner, True)
    predictions = activator.predict(X_test_class, debug=True)
    
    print("Test Samples:\n", X_test_class)
    print("Predictions:", predictions)
    assert predictions.shape == (3,), "Should return 3 predictions"
    assert all(p in [0, 1] for p in predictions), "Should predict only class 0 or 1"
    print("✓ Classification prediction verified")
    
    # ===== Test 2: Regression =====
    print("\nTest 2: Regression")
    X_reg = np.array([
        [1, 2, 3, 5, 6, 8],   # Feature 1
        [2, 4, 6, 10, 12, 16]  # Feature 2
    ]).T
    y_reg = np.array([5, 7, 9, 13, 15, 19])
    
    reg_learner = QBMCLearner()
    reg_learner.fit(X_reg, y_reg)
    reg_activator = QBMCActivator(reg_learner)
    
    test_reg = np.array([
        [4, 7],  # Between training samples
        [6, 12]  # Exact match to training
    ])
    reg_preds = reg_activator.predict(test_reg, debug=True)
    
    print("Test Values:\n", test_reg)
    print("Predictions:", reg_preds)
    assert len(reg_preds) == 2, "Should return 2 predictions"
    assert all(5 <= p <= 19 for p in reg_preds), "Should stay within training range"
    print("✓ Regression prediction verified")

    # ===== Test 3: Mixed-Type General Test =====
    print("\nTest 4: Mixed Data Types")
    X_mixed = np.array([
        [0.0, 1, 3.1, 5.2],  # Float and int
        [0, 0.5, 1.1, 0.7]    # Float values
    ]).T
    y_mixed = np.array([0, 0.1, 1.3, 2.6])  # Regression
    
    mixed_learner = QBMCLearner()
    mixed_learner.fit(X_mixed, y_mixed)
    mixed_activator = QBMCActivator(mixed_learner)
    
    test_mixed = np.array([
        [2, 1.1],  # Between samples
        [3.1, 1.1] # Exact match
    ])
    mixed_preds = mixed_activator.predict(test_mixed, debug=True)
    
    print("Test Values:\n", test_mixed)
    print("Predictions:", mixed_preds)
    assert len(mixed_preds) == 2, "Should return 2 predictions"
    assert all(0 <= p <= 2.6 for p in mixed_preds), "Should respect training range"
    print("✓ Mixed-type handling verified")
    
    print("\n=== All QBMCActivator tests passed ===")
