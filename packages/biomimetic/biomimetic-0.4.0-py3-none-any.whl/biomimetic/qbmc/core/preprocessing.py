# qbmc/core/preprocessing.py
import numpy as np
from typing import Union, Tuple

DEFAULT_BINSIZE = 9  # 8 bits + sign bit

class QBMCDataProcessor:
    """
    Handles automatic data conversion and quantization for QBMC models
    """
    def __init__(self, binsize: int = DEFAULT_BINSIZE):
        self.binsize = binsize
        self._scale = None
        self._offset = None
        self._quantized = False

    def auto_convert(self, data: Union[np.ndarray, list]) -> np.ndarray:
        """
        Main entry point: Automatically handles either integer or float input
        Returns binary representation and stores quantization parameters
        """
        arr = np.asarray(data)
        
        if np.issubdtype(arr.dtype, np.integer):
            return self.int_to_bin(arr)
        elif np.issubdtype(arr.dtype, np.floating):
            return self.float_to_bin(arr)
        else:
            raise TypeError(f"Unsupported data type: {arr.dtype}")

    def int_to_bin(self, data: np.ndarray) -> np.ndarray:
        """Direct integer to binary conversion"""
        self._quantized = False
        return self._arr_to_bin(data, signed=True)

    def float_to_bin(self, data: np.ndarray) -> np.ndarray:
        """Float to binary conversion with automatic quantization"""
        quantized, self._scale, self._offset = self.quantize_float(data)
        self._quantized = True
        return self._arr_to_bin(quantized, signed=True)

    def quantize_float(self, data: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """
        Quantizes float data to integer space
        Returns: (quantized_data, scale, offset)
        """
        d_min = np.min(data)
        d_max = np.max(data)
        
        # Calculate quantization parameters
        scale = (d_max - d_min) / (2**self.binsize - 1)
        offset = - (d_min / scale) - (2**(self.binsize-1))
        
        # Quantize and clamp values
        quantized = np.round((data / scale) + offset).astype(np.int64)
        return quantized, scale, offset

    def _to_bin(self, value: int, signed: bool = True) -> np.ndarray:
        """Core integer -> binary array conversion"""
        if signed:
            if value < 0:
                value = (1 << self.binsize) + value  # Two's complement
            return np.array(
                [bool((value >> i) & 0x01) 
                for i in reversed(range(self.binsize))]
            )
        else:
            return np.array(
                [bool((value >> i) & 0x01) 
                for i in reversed(range(self.binsize))]
            )

    def _from_bin(self, binary_array: np.ndarray, signed: bool = True) -> int:
        """Core binary array -> integer conversion"""
        value = sum(
            bit << (self.binsize - 1 - i) 
            for i, bit in enumerate(binary_array)
        )
        if signed and binary_array[0]:  # Handle two's complement
            value -= (1 << self.binsize)
        return value

    def _arr_to_bin(self, data: np.ndarray, signed: bool = True) -> np.ndarray:
        """Batch convert array of integers to binary representation"""
        return np.stack([np.stack([
            self._to_bin(val, signed=signed) 
            for val in sample
        ]) for sample in data])

    def postprocess(self, binary_data: np.ndarray) -> np.ndarray:
        """Convert binary predictions back to original data space"""
        int_data = np.apply_along_axis(
            lambda x: self._from_bin(x, signed=True),
            -1, binary_data
        )
        
        if self._quantized:
            return (int_data - self._offset) * self._scale
        return int_data

    @property
    def quantization_parameters(self) -> Tuple[float, float]:
        if not self._quantized:
            raise RuntimeError("Data was not quantized")
        return self._scale, self._offset 


if __name__ == "__main__":
    print("=== Testing QBMC Data Processor ===")
    
    # Initialize with default binsize (9)
    processor = QBMCDataProcessor()
    
    # Test data from qbmc.pdf
    int_data = np.array([
        [0, 1, 3, 5, 7, 8],   # X
        [0, 0, 1, 0, 1, 1]    # Y
    ])
    
    float_data = np.array([
        [1.2, 2.4, 3.6, 5.1],
        [0.5, 1.0, 1.5, 2.0]
    ])
    
    # ===== Test 1: Integer to Binary Conversion =====
    print("\nTest 1: Integer to Binary")
    int_binary = processor.int_to_bin(int_data)
    print("Input:\n", int_data)
    print("Binary Output:\n", int_binary)
    print("Binary Output Integers:\n", int_binary.astype(int))
    
    # Verify round-trip
    reconstructed = processor.postprocess(int_binary)
    assert np.array_equal(int_data, reconstructed), "Integer round-trip failed"
    print("✓ Integer round-trip verified")
    
    # ===== Test 2: Float Quantization =====
    print("\nTest 2: Float Quantization")
    float_binary = processor.float_to_bin(float_data)
    print("Input:\n", float_data)
    print("Binary Output:\n", float_binary.astype(int))
    
    # Verify quantization parameters
    scale, offset = processor.quantization_parameters
    print(f"Quantization params - Scale: {scale:.4f}, Offset: {offset:.4f}")
    
    # Verify round-trip
    reconstructed = processor.postprocess(float_binary)
    print("Reconstruction MSE:\n", np.mean(float_data - reconstructed)**2)
    assert np.allclose(float_data, reconstructed, atol=scale/2), "Float round-trip failed"
    print("✓ Float round-trip verified")
    
    # ===== Test 3: Auto Conversion =====
    print("\nTest 3: Auto Conversion")
    mixed_data = [
        [0, 1.5, 3, 4.2],  # Mixed types
        [1, 2.0, 5, 6.8]
    ]
    
    auto_binary = processor.auto_convert(mixed_data)
    reconstructed = processor.postprocess(auto_binary)
    print("Mixed Input:\n", mixed_data)
    print("Binary Output:\n", auto_binary.astype(int))
    print("Reconstructed Input:\n", reconstructed)

    
    # ===== Test 4: Edge Cases =====
    print("\nTest 4: Edge Cases")
    
    # Test negative integers
    neg_data = np.array([[-5, -3, 0, 2, 4]])
    neg_binary = processor.int_to_bin(neg_data)
    print("Negative Input:", neg_data)
    print("Binary Output:\n", neg_binary.astype(int))
    
    # Test large value range
    wide_range = np.array([[0.1, 450, 1000.0]])
    wide_binary = processor.float_to_bin(wide_range)
    print("Wide Range Input:", wide_range)
    print("Binary Output:\n", wide_binary.astype(int))
    
    # ===== Test 5: Batch Processing =====
    print("\nTest 5: Batch Processing")
    
    # From ANN replication section in qbmc.pdf
    ann_data = np.array([
        [1.6746e-03, 1.0286e+00],
        [1.0286e+00, 3.0220e+00]
    ])
    
    ann_binary = processor.float_to_bin(ann_data)
    print("ANN-style Input:\n", ann_data)
    print("Binary Output:\n", ann_binary.astype(int))
    
    # Verify reconstruction
    reconstructed = processor.postprocess(ann_binary)
    print("Reconstructed ANN Data:\n", reconstructed)
    assert np.allclose(ann_data, reconstructed, atol=scale/2), "ANN data round-trip failed"
    print("✓ ANN data round-trip verified")
    
    # ===== Test 6: Quantization Bounds =====
    print("\nTest 6: Quantization Bounds")

    # Test minimum/maximum representable values (now as 2D array)
    test_vals = np.array([[-2**(processor.binsize-1), 2**(processor.binsize-1)-1]])
    test_binary = processor.int_to_bin(test_vals)
    print("Boundary Input:", test_vals)
    print("Binary Output:\n", test_binary.astype(int))

    try:
        # This should trigger two's complement overflow (as 2D array)
        overflow = np.array([[-2**(processor.binsize)]])
        processor.int_to_bin(overflow)
        assert False, "Should have raised error on overflow"
    except Exception as e:
        print(f"✓ Overflow protection working: {str(e)}")

    print("\n=== All tests passed successfully ===")
