# qbmc/core/activations.py
import numpy as np
from typing import Dict, List, Union
from preprocessing import QBMCDataProcessor
from learning import QBMCLearner

class QBMCActivator:
    def __init__(self, learner: QBMCLearner = None, is_classification: bool = False):
        self.learner = learner
        self.processor = QBMCDataProcessor() if learner is None else learner.processor
        self.is_classification = is_classification
        
    def load_network(self, learner: QBMCLearner):
        self.learner = learner
        self.processor = learner.processor

    def predict(self, X: np.ndarray, debug: bool = False) -> Union[np.ndarray, List[float]]:
        if self.learner is None:
            raise RuntimeError("No trained network loaded")
            
        X_bin = self.processor.auto_convert(X)
        predictions = []
        
        for x in X_bin:
            result = self.forward_pass(x, debug)
            predictions.append(result['prediction'])
        
        return np.array(predictions)

    def _calculate_feature_pdf(self, x: np.ndarray, layer: List) -> np.ndarray:
        scores = []
        for cell in layer:
            weights = cell.weightArray
            mismatches = weights != x
            first_mismatch = np.argmax(mismatches, axis=1)
            perfect_matches = np.all(~mismatches, axis=1)
            matches = np.where(perfect_matches, self.learner.binsize, first_mismatch)
            max_k = np.max(matches)
            
            # Count how many weights reached max_k (raw count)
            count = np.sum(matches == max_k)
            scores.append(count)
        
        # Return raw counts instead of normalized probabilities
        return np.array(scores)

    def _combine_pdfs(self, feature_pdfs: List[np.ndarray]) -> np.ndarray:
        # Sum counts across features
        combined = np.sum(feature_pdfs, axis=0)
        
        # Normalize to probabilities
        total = np.sum(combined)
        return combined / total if total > 0 else combined

    def _predict_class(self, pdf: np.ndarray) -> int:
        return self.learner.labels_original[np.argmax(pdf)]

    def _predict_value(self, pdf: np.ndarray) -> float:
        return np.dot(pdf, self.learner.labels_original)
    
    def _set_classification(self, is_classification: bool = True):
        self.is_classification = is_classification

    def _is_classification(self) -> bool:
        return self.is_classification

    def forward_pass(self, x_bin: np.ndarray, debug: bool = False) -> Dict:
        result = {'feature_pdfs': [], 'combined_pdf': None, 'prediction': None}
        
        # Calculate PDF for each feature
        for feature_idx, layer in self.learner.feature_layers.items():
            result['feature_pdfs'].append(
                self._calculate_feature_pdf(x_bin[feature_idx], layer)
            )
        if debug:
            print("Feature PDFs:", result['feature_pdfs'])
        
        # Combine probabilities
        result['combined_pdf'] = self._combine_pdfs(result['feature_pdfs'])
        if debug:
            print("Combined PDF:", result['combined_pdf'])
        
        # Make prediction
        if self.is_classification:
            result['prediction'] = self._predict_class(result['combined_pdf'])
        else:
            result['prediction'] = self._predict_value(result['combined_pdf'])
            
        return result

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
    predictions = activator.predict(X_test_class, True)
    
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
    reg_preds = reg_activator.predict(test_reg, True)
    
    print("Test Values:\n", test_reg)
    print("Predictions:", reg_preds)
    assert len(reg_preds) == 2, "Should return 2 predictions"
    assert all(5 <= p <= 19 for p in reg_preds), "Should stay within training range"
    print("✓ Regression prediction verified")
    
    # ===== Test 3: Raw Forward Pass =====
    print("\nTest 3: Raw Forward Pass")
    sample = np.array([0, 0])  # Should match first class
    sample_bin = activator.processor.auto_convert(sample.reshape(1, -1))[0]
    
    result = activator.forward_pass(sample_bin)
    print("Feature PDFs:", [pdf.round(3) for pdf in result['feature_pdfs']])
    print("Combined PDF:", result['combined_pdf'].round(3))
    print("Prediction:", result['prediction'])
    assert result['prediction'] == 0, "Should predict class 0"
    assert np.allclose(np.sum(result['combined_pdf']), 1), "PDF should sum to 1"
    print("✓ Raw forward pass verified")

    # ===== Test 4: Mixed-Type General Test =====
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
    mixed_preds = mixed_activator.predict(test_mixed, True)
    
    print("Test Values:\n", test_mixed)
    print("Predictions:", mixed_preds)
    assert len(mixed_preds) == 2, "Should return 2 predictions"
    assert all(0 <= p <= 2.6 for p in mixed_preds), "Should respect training range"
    print("✓ Mixed-type handling verified")
    
    print("\n=== All QBMCActivator tests passed ===")
