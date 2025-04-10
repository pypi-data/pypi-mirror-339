"""
DBSF - A binary format intended for storing deep learning model weights and metadata primarily for DNA models.

This format is inspired by and based on the GGUF format 
(https://github.com/ggerganov/ggml/blob/master/docs/gguf.md).

File format:
    Header:
        uint32 : magic number (0x46534244 = "DBSF")
        uint32 : format version
        uint64 : number of tensors
        uint64 : number of metadata key-value pairs
        
    Metadata Section:
        For each key-value pair:
            string : key
            uint32 : value type
            <value data based on type>
            
    Tensor Information:
        For each tensor:
            string : name
            uint32 : number of dimensions
            uint64[n_dims] : shape
            uint32 : data type
            uint64 : offset from start of tensor data section
            
    Tensor Data:
        32-byte aligned section containing raw tensor data
"""

import struct
import numpy as np
import json
from enum import IntEnum
from typing import Any, Dict, Optional
import torch

TORCH = 'pytorch'

class DBSFType(IntEnum):
    """Supported data types in DBSF format"""
    F32 = 0
    F16 = 1
    I8 = 24
    I16 = 25
    I32 = 26
    I64 = 27
    F64 = 28

class DBSFMetadataValueType(IntEnum):
    """Metadata value types supported in DBSF format"""
    UINT8 = 0
    INT8 = 1
    UINT16 = 2
    INT16 = 3
    UINT32 = 4
    INT32 = 5
    FLOAT32 = 6
    BOOL = 7
    STRING = 8
    ARRAY = 9
    UINT64 = 10
    INT64 = 11
    FLOAT64 = 12
    JSON = 13  # Added for storing complex nested structures

ALIGNMENT = 32
DBSF_MAGIC = 0x46534244  # "DBSF" in ASCII
DBSF_VERSION = 1

# Standard metadata field names for PyTorch/JAX/TensorFlow compatibility
MODEL_TYPE = "model_type"
MODEL_NAME = "model_name"
MODEL_ARCHITECTURE = "model_architecture"
MODEL_CONFIG = "model_config"

# BPNet specific configuration fields
BPNET_HIDDEN_CHANNELS = "hidden_channels"
BPNET_NUM_LAYERS = "num_layers"
BPNET_IN_CHANNELS = "in_channels"
BPNET_OUT_CHANNELS = "out_channels"
BPNET_NUM_CONTROL_TRACKS = "num_control_tracks"
BPNET_INITIAL_CONV_KERNEL_SIZE = "initial_conv_kernel_size"
BPNET_RESIDUAL_BLOCK_KERNEL_SIZE = "residual_block_kernel_size"
BPNET_PROFILE_CONV_KERNEL_SIZE = "profile_conv_kernel_size"
BPNET_DILATION_RATE = "dilation_rate"
BPNET_ALPHA = "alpha"
BPNET_PROFILE_OUTPUT_BIAS = "profile_output_bias"
BPNET_COUNT_OUTPUT_BIAS = "count_output_bias"
BPNET_INITIAL_CONV_BIAS = "initial_conv_bias"
BPNET_DILATED_CONV_BIAS = "dilated_conv_bias"

# ChromBPNet specific configuration fields
CHROMBPNET_BIAS_CONFIG = "bias_config"
CHROMBPNET_ACCESSIBILITY_CONFIG = "accessibility_config"

# DynamicBPNet specific configuration fields
DYNAMICBPNET_CONTROLLER_CONFIG = "controller_config"

# CellStateController specific configuration fields
CONTROLLER_IN_FEATURES = "in_features"
CONTROLLER_HIDDEN_DIMS = "hidden_dims"
CONTROLLER_OUT_FEATURES = "out_features"
CONTROLLER_DROPOUT = "dropout"

# DragoNNFruit specific configuration fields
DRAGONNFRUIT_BIAS_CONFIG = "bias_config"
DRAGONNFRUIT_ACCESSIBILITY_CONFIG = "accessibility_config"

# Mappings from config keys to constructor parameter names
CONFIG_TO_PARAM_MAPPINGS = {
    # BPNet parameter mappings
    BPNET_HIDDEN_CHANNELS: "hidden_channels",
    BPNET_NUM_LAYERS: "num_layers",
    BPNET_IN_CHANNELS: "in_channels",
    BPNET_OUT_CHANNELS: "out_channels",
    BPNET_NUM_CONTROL_TRACKS: "num_control_tracks",
    BPNET_INITIAL_CONV_KERNEL_SIZE: "initial_conv_kernel_size",
    BPNET_RESIDUAL_BLOCK_KERNEL_SIZE: "residual_block_kernel_size",
    BPNET_PROFILE_CONV_KERNEL_SIZE: "profile_conv_kernel_size",
    BPNET_DILATION_RATE: "dilation_rate",
    BPNET_ALPHA: "alpha",
    BPNET_PROFILE_OUTPUT_BIAS: "profile_output_bias",
    BPNET_COUNT_OUTPUT_BIAS: "count_output_bias",
    BPNET_INITIAL_CONV_BIAS: "initial_conv_bias",
    BPNET_DILATED_CONV_BIAS: "dilated_conv_bias",
    
    # CellStateController parameter mappings
    CONTROLLER_IN_FEATURES: "in_features",
    CONTROLLER_HIDDEN_DIMS: "hidden_dims",
    CONTROLLER_OUT_FEATURES: "out_features",
    CONTROLLER_DROPOUT: "dropout",
}

def get_parameters_dict(model: torch.nn.Module) -> Dict[str, np.ndarray]:
    """
    Extract parameters from a PyTorch model.
    
    Args:
        model: A PyTorch nn.Module
        
    Returns:
        Dictionary mapping parameter names to numpy arrays
    """
    if not isinstance(model, torch.nn.Module):
        raise TypeError("Model must be a torch.nn.Module")
    return {name: param.detach().cpu().numpy() 
            for name, param in model.state_dict().items()}

def get_dtype_from_array(arr) -> DBSFType:
    """Map numpy/torch dtype to DBSF type"""
    dtype_map = {
        np.float32: DBSFType.F32,
        np.float16: DBSFType.F16,
        np.float64: DBSFType.F64,
        np.int8: DBSFType.I8,
        np.int16: DBSFType.I16,
        np.int32: DBSFType.I32,
        np.int64: DBSFType.I64,
    }
    return dtype_map.get(arr.dtype.type, DBSFType.F32)

def align_offset(offset: int) -> int:
    """Align offset to ALIGNMENT boundary"""
    return offset + (ALIGNMENT - (offset % ALIGNMENT)) % ALIGNMENT

def write_string(f, s: str):
    """Write a string in DBSF format (length + UTF-8 bytes)"""
    b = s.encode('utf-8')
    f.write(struct.pack('<Q', len(b)))  # uint64 length
    f.write(b)

def write_metadata_value(f, value_type: DBSFMetadataValueType, value: Any):
    """Write a metadata value based on its type"""
    if value_type == DBSFMetadataValueType.STRING:
        write_string(f, value)
    elif value_type == DBSFMetadataValueType.BOOL:
        f.write(struct.pack('<?', value))
    elif value_type == DBSFMetadataValueType.FLOAT32:
        f.write(struct.pack('<f', value))
    elif value_type == DBSFMetadataValueType.FLOAT64:
        f.write(struct.pack('<d', value))
    elif value_type in [DBSFMetadataValueType.INT32, DBSFMetadataValueType.UINT32]:
        f.write(struct.pack('<I', value))
    elif value_type in [DBSFMetadataValueType.INT64, DBSFMetadataValueType.UINT64]:
        f.write(struct.pack('<Q', value))
    elif value_type == DBSFMetadataValueType.JSON:
        # For complex objects, serialize as JSON string
        json_str = json.dumps(value)
        write_string(f, json_str)

def extract_model_config(model: torch.nn.Module) -> Dict[str, Any]:
    """
    Extract model configuration from a PyTorch model instance.
    
    Args:
        model: A PyTorch model instance
        
    Returns:
        Dictionary containing model configuration parameters
    """
    # Identify model type
    model_class = model.__class__.__name__
    
    if model_class == "BPNet":
        config = {
            MODEL_TYPE: "bpnet",
            MODEL_NAME: getattr(model, "name", None),
            BPNET_HIDDEN_CHANNELS: model.hidden_channels,
            BPNET_NUM_LAYERS: model.num_layers,
            BPNET_IN_CHANNELS: model.in_channels,
            BPNET_OUT_CHANNELS: model.out_channels,
            BPNET_NUM_CONTROL_TRACKS: model.num_control_tracks,
            BPNET_INITIAL_CONV_KERNEL_SIZE: model.initial_conv_kernel_size,
            BPNET_RESIDUAL_BLOCK_KERNEL_SIZE: model.residual_block_kernel_size,
            BPNET_PROFILE_CONV_KERNEL_SIZE: model.profile_kernel_size,
            BPNET_DILATION_RATE: model.dilation_rate,
            BPNET_ALPHA: model.alpha,
            BPNET_PROFILE_OUTPUT_BIAS: model.profile_output_bias,
            BPNET_COUNT_OUTPUT_BIAS: model.count_output_bias,
            BPNET_INITIAL_CONV_BIAS: model.initial_conv_bias,
            BPNET_DILATED_CONV_BIAS: model.dilated_conv_bias,
        }
    elif model_class == "ChromBPNet":
        config = {
            MODEL_TYPE: "chrombpnet",
            MODEL_NAME: getattr(model, "name", None),
            CHROMBPNET_BIAS_CONFIG: extract_model_config(model.bias),
            CHROMBPNET_ACCESSIBILITY_CONFIG: extract_model_config(model.accessibility),
        }
    elif model_class == "CellStateController":
        config = {
            MODEL_TYPE: "cellstatecontroller",
            CONTROLLER_IN_FEATURES: model.in_features,
            CONTROLLER_HIDDEN_DIMS: model.hidden_dims,
            CONTROLLER_OUT_FEATURES: model.out_features,
            CONTROLLER_DROPOUT: model.dropout,
        }
    elif model_class == "DynamicBPNet":
        # Get base BPNet config
        bpnet_config = {
            BPNET_HIDDEN_CHANNELS: model.hidden_channels,
            BPNET_NUM_LAYERS: model.num_layers,
            BPNET_IN_CHANNELS: model.in_channels,
            BPNET_OUT_CHANNELS: model.out_channels,
            BPNET_NUM_CONTROL_TRACKS: model.num_control_tracks,
            BPNET_INITIAL_CONV_KERNEL_SIZE: model.initial_conv_kernel_size,
            BPNET_RESIDUAL_BLOCK_KERNEL_SIZE: model.residual_block_kernel_size,
            BPNET_PROFILE_CONV_KERNEL_SIZE: model.profile_kernel_size,
            BPNET_DILATION_RATE: model.dilation_rate,
            BPNET_ALPHA: model.alpha,
            BPNET_PROFILE_OUTPUT_BIAS: model.profile_output_bias,
            BPNET_COUNT_OUTPUT_BIAS: False,  # DynamicBPNet doesn't use count prediction
            BPNET_INITIAL_CONV_BIAS: model.initial_conv_bias,
            BPNET_DILATED_CONV_BIAS: False,  # DynamicBPNet uses dynamic biases
        }
        
        config = {
            MODEL_TYPE: "dynamicbpnet",
            MODEL_NAME: getattr(model, "name", None),
            DYNAMICBPNET_CONTROLLER_CONFIG: extract_model_config(model.controller),
            **bpnet_config,
        }
    elif model_class == "DragoNNFruit":
        config = {
            MODEL_TYPE: "dragonnfruit",
            MODEL_NAME: getattr(model, "name", None),
            DRAGONNFRUIT_BIAS_CONFIG: extract_model_config(model.bias),
            DRAGONNFRUIT_ACCESSIBILITY_CONFIG: extract_model_config(model.accessibility),
        }
    else:
        # Generic case for unsupported model types
        config = {
            MODEL_TYPE: model_class.lower(),
            MODEL_NAME: getattr(model, "name", None),
        }
    
    return config

def write_dbsf(filename: str, model: torch.nn.Module, metadata: Optional[Dict[str, Any]] = None):
    """
    Write a PyTorch model to a DBSF file format.
    
    Args:
        filename: Path to output file
        model: A PyTorch nn.Module
        metadata: Optional additional metadata to store
    """
    # Extract parameters from model
    params = get_parameters_dict(model)
    
    # Extract model configuration
    model_config = extract_model_config(model)
    
    # Prepare metadata
    meta = {
        MODEL_TYPE: (DBSFMetadataValueType.STRING, TORCH),
        'version': (DBSFMetadataValueType.UINT32, DBSF_VERSION),
        MODEL_CONFIG: (DBSFMetadataValueType.JSON, model_config),
    }
    
    # Add any additional metadata
    if metadata:
        for key, value in metadata.items():
            # Determine value type based on Python type
            if isinstance(value, bool):
                meta[key] = (DBSFMetadataValueType.BOOL, value)
            elif isinstance(value, int):
                if value < 2**32:
                    meta[key] = (DBSFMetadataValueType.INT32, value)
                else:
                    meta[key] = (DBSFMetadataValueType.INT64, value)
            elif isinstance(value, float):
                meta[key] = (DBSFMetadataValueType.FLOAT32, value)
            elif isinstance(value, str):
                meta[key] = (DBSFMetadataValueType.STRING, value)
            else:
                # For complex types, use JSON
                meta[key] = (DBSFMetadataValueType.JSON, value)
    
    with open(filename, 'wb') as f:
        # Write header
        f.write(struct.pack('<I', DBSF_MAGIC))
        f.write(struct.pack('<I', DBSF_VERSION))
        
        # Write counts
        f.write(struct.pack('<Q', len(params)))  # tensor_count
        f.write(struct.pack('<Q', len(meta)))  # metadata_kv_count
        
        # Write metadata
        for key, (value_type, value) in meta.items():
            write_string(f, key)
            f.write(struct.pack('<I', value_type))
            write_metadata_value(f, value_type, value)
        
        # Write tensor information
        tensor_infos = []
        current_offset = 0
        
        for name, param in params.items():
            tensor_infos.append({
                'name': name,
                'dims': param.shape,
                'type': get_dtype_from_array(param),
                'offset': current_offset
            })
            
            size = param.nbytes
            current_offset = align_offset(current_offset + size)
        
        for info in tensor_infos:
            write_string(f, info['name'])
            f.write(struct.pack('<I', len(info['dims'])))
            for dim in info['dims']:
                f.write(struct.pack('<Q', dim))
            f.write(struct.pack('<I', info['type']))
            f.write(struct.pack('<Q', info['offset']))
        
        # Align to ALIGNMENT boundary before tensor data
        current_pos = f.tell()
        padding_size = align_offset(current_pos) - current_pos
        f.write(b'\0' * padding_size)
        
        # Write tensor data
        for param in params.values():
            param_bytes = param.tobytes()
            f.write(param_bytes)
            padding_size = align_offset(len(param_bytes)) - len(param_bytes)
            f.write(b'\0' * padding_size)

def read_string(f) -> str:
    """Read a string in DBSF format (length + UTF-8 bytes)"""
    length = struct.unpack('<Q', f.read(8))[0]
    return f.read(length).decode('utf-8')

def read_metadata_value(f, value_type: DBSFMetadataValueType) -> Any:
    """Read a metadata value based on its type"""
    if value_type == DBSFMetadataValueType.STRING:
        return read_string(f)
    elif value_type == DBSFMetadataValueType.BOOL:
        return bool(struct.unpack('<?', f.read(1))[0])
    elif value_type == DBSFMetadataValueType.FLOAT32:
        return struct.unpack('<f', f.read(4))[0]
    elif value_type == DBSFMetadataValueType.FLOAT64:
        return struct.unpack('<d', f.read(8))[0]
    elif value_type in [DBSFMetadataValueType.INT32, DBSFMetadataValueType.UINT32]:
        return struct.unpack('<I', f.read(4))[0]
    elif value_type in [DBSFMetadataValueType.INT64, DBSFMetadataValueType.UINT64]:
        return struct.unpack('<Q', f.read(8))[0]
    elif value_type == DBSFMetadataValueType.JSON:
        # For complex objects deserialized from JSON
        json_str = read_string(f)
        return json.loads(json_str)
    else:
        raise ValueError(f"Unsupported metadata value type: {value_type}")

def numpy_dtype_from_dbsf(dbsf_type: DBSFType) -> np.dtype:
    """Convert DBSF type to numpy dtype"""
    dtype_map = {
        DBSFType.F32: np.float32,
        DBSFType.F16: np.float16,
        DBSFType.F64: np.float64,
        DBSFType.I8: np.int8,
        DBSFType.I16: np.int16,
        DBSFType.I32: np.int32,
        DBSFType.I64: np.int64,
    }
    return dtype_map.get(dbsf_type, np.float32)

def read_dbsf(filename: str) -> Dict[str, Any]:
    """
    Read a model from a DBSF file format.
    
    Args:
        filename: Path to input file
        
    Returns:
        Dictionary containing:
            - tensors: Dict[str, np.ndarray] - Named tensors
            - metadata: Dict[str, Any] - Model metadata
            - config: Dict[str, Any] - Model configuration
    """
    with open(filename, 'rb') as f:
        # Read and verify header
        magic = struct.unpack('<I', f.read(4))[0]
        if magic != DBSF_MAGIC:
            raise ValueError("Invalid DBSF file: incorrect magic number")
            
        version = struct.unpack('<I', f.read(4))[0]
        if version != DBSF_VERSION:
            raise ValueError(f"Unsupported DBSF version: {version}")
        
        # Read counts
        tensor_count = struct.unpack('<Q', f.read(8))[0]
        metadata_count = struct.unpack('<Q', f.read(8))[0]
        
        # Read metadata
        metadata = {}
        config = None
        for _ in range(metadata_count):
            key = read_string(f)
            value_type = DBSFMetadataValueType(struct.unpack('<I', f.read(4))[0])
            value = read_metadata_value(f, value_type)
            
            # Special handling for model configuration
            if key == MODEL_CONFIG:
                config = value
            
            metadata[key] = value
        
        # Read tensor information
        tensor_infos = []
        for _ in range(tensor_count):
            name = read_string(f)
            n_dims = struct.unpack('<I', f.read(4))[0]
            dims = [struct.unpack('<Q', f.read(8))[0] for _ in range(n_dims)]
            dtype = DBSFType(struct.unpack('<I', f.read(4))[0])
            offset = struct.unpack('<Q', f.read(8))[0]
            
            tensor_infos.append({
                'name': name,
                'shape': tuple(dims),
                'dtype': numpy_dtype_from_dbsf(dtype),
                'offset': offset
            })
        
        # Align to ALIGNMENT boundary before tensor data
        current_pos = f.tell()
        padding_size = align_offset(current_pos) - current_pos
        f.seek(padding_size, 1)  # Skip padding
        
        # Store the start position of tensor data
        tensor_data_start = f.tell()
        
        # Read tensor data
        tensors = {}
        for info in tensor_infos:
            # Seek from tensor data start position
            f.seek(tensor_data_start + info['offset'])
            dtype = np.dtype(info['dtype'])
            size = np.prod(info['shape']) * dtype.itemsize
            data = np.frombuffer(
                f.read(size),
                dtype=dtype
            ).reshape(info['shape'])
            tensors[info['name']] = data
    
    return {
        'tensors': tensors,
        'metadata': metadata,
        'config': config
    }

def create_model_from_config(config: Dict[str, Any]) -> Optional[torch.nn.Module]:
    """
    Create a PyTorch model instance from configuration.
    
    Args:
        config: Model configuration dictionary
        
    Returns:
        PyTorch model instance or None if model type is not supported
    """
    model_type = config.get(MODEL_TYPE)
    
    if model_type == "bpnet":
        # Import here to avoid circular imports
        from ..models.bpnet import BPNet
        
        # Extract parameters with proper mapping to constructor arguments
        params = {}
        for key, value in config.items():
            if key in [MODEL_TYPE, MODEL_NAME] or key.startswith("_"):
                continue
                
            # Map the config key to the constructor parameter name
            param_name = CONFIG_TO_PARAM_MAPPINGS.get(key, key)
            params[param_name] = value
        
        # Add name separately since it's a special case
        if MODEL_NAME in config:
            params["name"] = config[MODEL_NAME]
        
        return BPNet(**params)
    
    elif model_type == "chrombpnet":
        # Import here to avoid circular imports
        from ..models.chrombpnet import ChromBPNet
        
        bias_config = config.get(CHROMBPNET_BIAS_CONFIG, {})
        accessibility_config = config.get(CHROMBPNET_ACCESSIBILITY_CONFIG, {})
        
        bias_model = create_model_from_config(bias_config)
        accessibility_model = create_model_from_config(accessibility_config)
        
        if bias_model and accessibility_model:
            params = {"bias": bias_model, "accessibility": accessibility_model}
            if MODEL_NAME in config:
                params["name"] = config[MODEL_NAME]
            return ChromBPNet(**params)
    
    elif model_type == "dynamicbpnet":
        # Import here to avoid circular imports
        from ..models.dragonnfruit import DynamicBPNet
        
        controller_config = config.get(DYNAMICBPNET_CONTROLLER_CONFIG, {})
        controller = create_model_from_config(controller_config)
        
        if controller:
            # Extract parameters with proper mapping
            params = {"controller": controller}
            for key, value in config.items():
                param_name = CONFIG_TO_PARAM_MAPPINGS.get(key, key)
                if (param_name not in ["dilated_conv_bias"] and
                    key not in [MODEL_TYPE, MODEL_NAME, DYNAMICBPNET_CONTROLLER_CONFIG] and
                    not key.startswith("_")):
                    params[param_name] = value
            
            if MODEL_NAME in config:
                params["name"] = config[MODEL_NAME]
                
            return DynamicBPNet(**params)
    
    elif model_type == "cellstatecontroller":
        # Import here to avoid circular imports
        from ..models.dragonnfruit import CellStateController
        
        # Extract parameters with proper mapping
        params = {}
        for key, value in config.items():
            if key in [MODEL_TYPE, MODEL_NAME] or key.startswith("_"):
                continue
                
            # Map the config key to the constructor parameter name
            param_name = CONFIG_TO_PARAM_MAPPINGS.get(key, key)
            params[param_name] = value
                
        return CellStateController(**params)
    
    elif model_type == "dragonnfruit":
        # Import here to avoid circular imports
        from ..models.dragonnfruit import DragoNNFruit
        
        bias_config = config.get(DRAGONNFRUIT_BIAS_CONFIG, {})
        accessibility_config = config.get(DRAGONNFRUIT_ACCESSIBILITY_CONFIG, {})
        
        bias_model = create_model_from_config(bias_config)
        accessibility_model = create_model_from_config(accessibility_config)
        
        if bias_model and accessibility_model:
            params = {"bias": bias_model, "accessibility": accessibility_model}
            if MODEL_NAME in config:
                params["name"] = config[MODEL_NAME]
            return DragoNNFruit(**params)
    
    return None

def load_into_model(model: torch.nn.Module, dbsf_file: str):
    """
    Load DBSF weights into a PyTorch model.
    
    Args:
        model: A PyTorch nn.Module
        dbsf_file: Path to the DBSF file
        
    Returns:
        Model with loaded weights
    """
    if not isinstance(model, torch.nn.Module):
        raise TypeError("Model must be a torch.nn.Module")
    
    data = read_dbsf(dbsf_file)
    state_dict = {
        name: torch.from_numpy(tensor.copy())
        for name, tensor in data['tensors'].items()
    }
    model.load_state_dict(state_dict)
    return model

def load_model_from_dbsf(dbsf_file: str) -> Optional[torch.nn.Module]:
    """
    Load a model from a DBSF file, creating the model architecture from the stored config.
    
    Args:
        dbsf_file: Path to the DBSF file
        
    Returns:
        A PyTorch model instance with loaded weights
    """
    data = read_dbsf(dbsf_file)
    
    if 'config' not in data or not data['config']:
        raise ValueError("DBSF file does not contain model configuration")
    
    # Create model from configuration
    model = create_model_from_config(data['config'])
    
    if model is None:
        raise ValueError(f"Failed to create model from config: {data['config'].get(MODEL_TYPE)}")
    
    # Load weights into model
    state_dict = {
        name: torch.from_numpy(tensor.copy())
        for name, tensor in data['tensors'].items()
    }
    model.load_state_dict(state_dict)
    
    return model