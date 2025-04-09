"""CoreML conversion utility for local model execution.

This module implements utilities for converting models to CoreML format
for efficient execution on Apple devices.
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CoreMLConverter:
    """Utility for converting models to CoreML format.

    This class provides utilities for converting machine learning models
    to CoreML format for efficient execution on Apple devices.

    Attributes:
        cache_dir: Directory for caching converted models.
        supported_formats: List of supported source formats.
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        compute_units: str = "ALL",
    ):
        """Initialize the CoreML converter.

        Args:
            cache_dir: Directory for caching converted models. If None, a
                default directory will be used.
            compute_units: Compute units to use for CoreML model execution.
                Options are "ALL", "CPU_ONLY", "CPU_AND_GPU", "CPU_AND_NE".
        """
        self.cache_dir = cache_dir or os.path.expanduser("~/.llama_integrations/coreml_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.compute_units = compute_units

        # List of supported source formats
        self.supported_formats = ["onnx", "tensorflow", "pytorch", "keras"]

        # Check if coremltools is available
        try:
            import coremltools

            self.coremltools_available = True
        except ImportError:
            self.coremltools_available = False
            logger.warning(
                "coremltools is not available. Install it with "
                "'pip install coremltools' to enable CoreML conversion."
            )

    async def convert_model(
        self,
        model_path: str,
        source_format: str,
        output_path: Optional[str] = None,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Convert a model to CoreML format.

        Args:
            model_path: Path to the source model.
            source_format: Format of the source model.
            output_path: Path for the converted model. If None, a default
                path will be used.
            model_config: Additional configuration for the model.

        Returns:
            Path to the converted model.
        """
        if not self.coremltools_available:
            raise ImportError(
                "coremltools is not available. Install it with "
                "'pip install coremltools' to enable CoreML conversion."
            )

        if source_format.lower() not in self.supported_formats:
            raise ValueError(
                f"Unsupported source format: {source_format}. "
                f"Supported formats are: {', '.join(self.supported_formats)}"
            )

        # Generate a default output path if none is provided
        if not output_path:
            model_name = os.path.basename(model_path).split(".")[0]
            output_path = os.path.join(self.cache_dir, f"{model_name}.mlmodel")

        # Check if the model is already converted
        if os.path.exists(output_path):
            logger.info("Using cached CoreML model: %s", output_path)
            return output_path

        logger.info("Converting model to CoreML format: %s", model_path)

        # Import coremltools

        # Convert based on source format
        if source_format.lower() == "onnx":
            # Convert from ONNX
            mlmodel = await self._convert_from_onnx(model_path, model_config)
        elif source_format.lower() == "tensorflow":
            # Convert from TensorFlow
            mlmodel = await self._convert_from_tensorflow(model_path, model_config)
        elif source_format.lower() == "pytorch":
            # Convert from PyTorch
            mlmodel = await self._convert_from_pytorch(model_path, model_config)
        elif source_format.lower() == "keras":
            # Convert from Keras
            mlmodel = await self._convert_from_keras(model_path, model_config)
        else:
            raise ValueError(f"Unsupported source format: {source_format}")

        # Set the compute units
        mlmodel.compute_units = self._get_compute_units()

        # Save the model
        mlmodel.save(output_path)

        logger.info("Model converted successfully: %s", output_path)

        return output_path

    async def _convert_from_onnx(
        self,
        model_path: str,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Convert a model from ONNX format to CoreML.

        Args:
            model_path: Path to the ONNX model.
            model_config: Additional configuration for the model.

        Returns:
            CoreML model.
        """
        import coremltools as ct

        # Load the model
        model_config = model_config or {}

        # Convert using convert_from_onnx
        mlmodel = ct.converters.onnx.convert(
            model=model_path,
            minimum_ios_deployment_target=model_config.get("minimum_ios_deployment_target", "13.0"),
            skip_model_load=model_config.get("skip_model_load", False),
        )

        return mlmodel

    async def _convert_from_tensorflow(
        self,
        model_path: str,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Convert a model from TensorFlow format to CoreML.

        Args:
            model_path: Path to the TensorFlow model.
            model_config: Additional configuration for the model.

        Returns:
            CoreML model.
        """
        import coremltools as ct
        import tensorflow as tf

        # Load the model
        tf_model = tf.saved_model.load(model_path)

        # Get model config
        model_config = model_config or {}
        inputs = model_config.get("inputs", [])
        outputs = model_config.get("outputs", [])

        # Convert using convert_from_tensorflow
        mlmodel = ct.convert(
            tf_model,
            inputs=inputs,
            outputs=outputs,
            minimum_ios_deployment_target=model_config.get("minimum_ios_deployment_target", "13.0"),
        )

        return mlmodel

    async def _convert_from_pytorch(
        self,
        model_path: str,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Convert a model from PyTorch format to CoreML.

        Args:
            model_path: Path to the PyTorch model.
            model_config: Additional configuration for the model.

        Returns:
            CoreML model.
        """
        import coremltools as ct
        import torch

        # Load the model
        model_config = model_config or {}
        model_class_name = model_config.get("model_class")

        # This requires the model class to be importable
        if not model_class_name:
            raise ValueError("Model class must be specified for PyTorch conversion")

        # Import the model class dynamically
        module_path, class_name = model_class_name.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        model_class = getattr(module, class_name)

        # Load the model
        model = model_class()
        model.load_state_dict(torch.load(model_path))
        model.eval()

        # Get example inputs
        example_inputs = model_config.get("example_inputs")
        if not example_inputs:
            raise ValueError("Example inputs must be specified for PyTorch conversion")

        # Convert tensor descriptions to actual tensors
        example_tensors = []
        for tensor_desc in example_inputs:
            shape = tensor_desc["shape"]
            dtype_str = tensor_desc.get("dtype", "float32")
            dtype = getattr(torch, dtype_str)
            example_tensors.append(torch.zeros(shape, dtype=dtype))

        # Trace the model
        traced_model = torch.jit.trace(model, example_tensors)

        # Convert using convert_from_pytorch
        mlmodel = ct.convert(
            traced_model,
            inputs=[
                ct.TensorType(
                    name=tensor_desc.get("name", f"input_{i}"),
                    shape=tensor_desc["shape"],
                    dtype=tensor_desc.get("dtype", "float32"),
                )
                for i, tensor_desc in enumerate(example_inputs)
            ],
            minimum_ios_deployment_target=model_config.get("minimum_ios_deployment_target", "13.0"),
        )

        return mlmodel

    async def _convert_from_keras(
        self,
        model_path: str,
        model_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Convert a model from Keras format to CoreML.

        Args:
            model_path: Path to the Keras model.
            model_config: Additional configuration for the model.

        Returns:
            CoreML model.
        """
        import coremltools as ct
        from tensorflow import keras

        # Load the model
        keras_model = keras.models.load_model(model_path)

        # Get model config
        model_config = model_config or {}

        # Convert using convert_from_keras
        mlmodel = ct.convert(
            keras_model,
            inputs=model_config.get("inputs"),
            outputs=model_config.get("outputs"),
            minimum_ios_deployment_target=model_config.get("minimum_ios_deployment_target", "13.0"),
        )

        return mlmodel

    def _get_compute_units(self) -> Any:
        """Get the compute units enum value.

        Returns:
            ComputeUnit enum value.
        """
        import coremltools as ct

        if self.compute_units == "CPU_ONLY":
            return ct.ComputeUnit.CPU_ONLY
        elif self.compute_units == "CPU_AND_GPU":
            return ct.ComputeUnit.CPU_AND_GPU
        elif self.compute_units == "CPU_AND_NE":
            return ct.ComputeUnit.CPU_AND_NE
        else:
            return ct.ComputeUnit.ALL

    def get_cached_models(self) -> List[Dict[str, str]]:
        """Get a list of cached CoreML models.

        Returns:
            List of dictionaries with model information.
        """
        cached_models = []

        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".mlmodel"):
                model_path = os.path.join(self.cache_dir, filename)
                model_info = {
                    "name": filename,
                    "path": model_path,
                    "size": f"{os.path.getsize(model_path) / (1024 * 1024):.2f} MB",
                }
                cached_models.append(model_info)

        return cached_models

    def clear_cache(self) -> None:
        """Clear the CoreML model cache."""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".mlmodel"):
                os.remove(os.path.join(self.cache_dir, filename))
