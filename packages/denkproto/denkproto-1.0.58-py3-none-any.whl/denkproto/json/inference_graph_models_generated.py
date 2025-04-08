from __future__ import annotations # Postponed evaluation of annotations
from pydantic import BaseModel, Field
from typing import List, Union, Literal, Dict, Any, Optional, Annotated

class AddNumbersNode(BaseModel):
    """Node that adds two numbers. Base type for all nodes in the graph."""
    node_type: Literal["add_numbers"]
    name: str
    input_number_1: str
    input_number_2: str
    output: str

class BoundingBoxFilterNode(BaseModel):
    """Node that filters bounding boxes based on a threshold. Base type for all nodes in the graph."""
    node_type: Literal["bounding_box_filter"]
    name: str
    input_threshold: str
    input_boxes: str
    output_boxes: str
    output_batch_map: str

class ConstTensorFloat64Data(BaseModel):
    """Constant tensor data of type float64. Base type for constant tensor data."""
    data_type: Literal["float64"]
    data: list[float]

class ConstTensorInt64Data(BaseModel):
    """Constant tensor data of type int64. Base type for constant tensor data."""
    data_type: Literal["int64"]
    data: list[int]

class ConstTensorNode(BaseModel):
    """Node representing a constant tensor. Base type for all nodes in the graph."""
    node_type: Literal["const_tensor"]
    name: str
    output: str
    shape: list[int]
    data: ConstTensorDataBase

class ConstTensorUint64Data(BaseModel):
    """Constant tensor data of type uint64. Base type for constant tensor data."""
    data_type: Literal["uint64"]
    data: list[int]

class GenerateNumberNode(BaseModel):
    """Node that generates a number within a range. Base type for all nodes in the graph."""
    node_type: Literal["generate_number"]
    name: str
    output: str
    min: int
    max: int

class ImageClassificationNode(BaseModel):
    """Node for image classification. Base type for all nodes in the graph."""
    node_type: Literal["image_classification"]
    name: str
    input: str
    output: str
    model_source: ModelSourceBase

class ImageObjectDetectionNode(BaseModel):
    """Node for image object detection. Base type for all nodes in the graph."""
    node_type: Literal["image_object_detection"]
    name: str
    input: str
    output: str
    model_source: ModelSourceBase

class ImageOcrNode(BaseModel):
    """Node for image OCR. Base type for all nodes in the graph."""
    node_type: Literal["image_ocr"]
    name: str
    input: str
    output: str
    model_source: ModelSourceBase

class ImagePatchesNode(BaseModel):
    """Node that extracts patches from an image based on bounding boxes. Base type for all nodes in the graph."""
    node_type: Literal["image_patches"]
    name: str
    input_image: str
    input_boxes: str
    input_batch_map: str
    input_target_size: str
    input_maximum_iterations: str
    output: str

class ImageResizeNode(BaseModel):
    """Node that resizes an image. Base type for all nodes in the graph."""
    node_type: Literal["image_resize"]
    name: str
    input_size: str
    input_image: str
    output: str

class ModelSourceFromNetworkExperimentId(BaseModel):
    """Model source specified by a network experiment ID. Base type for the source of the model."""
    source_type: Literal["network_experiment_id"]
    network_experiment_id: str

class ModelSourceFromNetworkId(BaseModel):
    """Model source specified by a network ID. Base type for the source of the model."""
    source_type: Literal["network_id"]
    network_id: str

class VirtualCameraNode(BaseModel):
    """Node representing a virtual camera source. Base type for all nodes in the graph."""
    node_type: Literal["virtual_camera"]
    name: str
    output: str
    path: str

# --- Main Recipe Class ---
class InferenceGraphRecipe(BaseModel):
    nodes: list[Node]
    license_id: str
    created_at: int

# --- Union Type Definitions ---
ConstTensorDataBase = Annotated[
    Union[
        ConstTensorFloat64Data,
        ConstTensorInt64Data,
        ConstTensorUint64Data
    ],
    Field(discriminator='data_type')
]

ModelSourceBase = Annotated[
    Union[
        ModelSourceFromNetworkExperimentId,
        ModelSourceFromNetworkId
    ],
    Field(discriminator='source_type')
]

Node = Annotated[
    Union[
        AddNumbersNode,
        BoundingBoxFilterNode,
        ConstTensorNode,
        GenerateNumberNode,
        ImageClassificationNode,
        ImageObjectDetectionNode,
        ImageOcrNode,
        ImagePatchesNode,
        ImageResizeNode,
        VirtualCameraNode
    ],
    Field(discriminator='node_type')
]

