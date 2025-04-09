from __future__ import annotations # Postponed evaluation of annotations
from pydantic import BaseModel, Field
from typing import List, Union, Literal, Dict, Any, Optional, Annotated

class BoundingBoxFilterNode(BaseModel):
    """Node that filters bounding boxes based on confidence and IoU thresholds. Base type for all nodes in the graph."""
    node_type: Literal["bounding_box_filter"]
    name: str
    input_bounding_boxes: str
    input_score_threshold: Optional[ThresholdSource] = None
    input_iou_threshold: Optional[ThresholdSource] = None
    output_port_name: Optional[str] = None

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
    output_port_name: Optional[str] = None
    shape: list[int]
    data: ConstTensorDataBase

class ConstTensorUint64Data(BaseModel):
    """Constant tensor data of type uint64. Base type for constant tensor data."""
    data_type: Literal["uint64"]
    data: list[int]

class ImageSize(BaseModel):
    """Represents image dimensions."""
    height: int
    width: int

class ClassificationNode(BaseModel):
    """Node for image classification. Base type for all nodes in the graph."""
    node_type: Literal["image_classification"]
    name: str
    inputImage: str
    output_port_name: Optional[str] = None
    model_source: ModelSourceBase

class ObjectDetectionNode(BaseModel):
    """Node for image object detection. Base type for all nodes in the graph."""
    node_type: Literal["image_object_detection"]
    name: str
    input_image: str
    output_port_name: Optional[str] = None
    model_source: ModelSourceBase
    scale_bounding_boxes: Optional[bool] = None

class OcrNode(BaseModel):
    """Node for image OCR. Base type for all nodes in the graph."""
    node_type: Literal["image_ocr"]
    name: str
    input_image: str
    output_port_name: Optional[str] = None
    model_source: ModelSourceBase

class ImagePatchesNode(BaseModel):
    """Node that extracts patches from an image based on bounding boxes. Base type for all nodes in the graph."""
    node_type: Literal["image_patches"]
    name: str
    input_image: str
    input_bounding_boxes: str
    input_target_size: TargetSizeSource
    input_maximum_iterations: Optional[MaxIterationsCountSource] = None
    output_port_name: Optional[str] = None

class ImageResizeNode(BaseModel):
    """Node that resizes an image. Base type for all nodes in the graph."""
    node_type: Literal["image_resize"]
    name: str
    input_size: str
    input_image: str
    output_port_name: Optional[str] = None

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
    output_port_name: Optional[str] = None
    path: str

# --- Inline Option Classes ---
class MaxIterationsCountSourceTopicOption(BaseModel):
    """Auto-generated class for inline option 'topic' of MaxIterationsCountSource"""
    source_type: Literal["topic"]
    topic: str

class MaxIterationsCountSourceValueOption(BaseModel):
    """Auto-generated class for inline option 'value' of MaxIterationsCountSource"""
    source_type: Literal["value"]
    value: int

class TargetSizeSourceImageSizeOption(BaseModel):
    """Auto-generated class for inline option 'image_size' of TargetSizeSource"""
    source_type: Literal["image_size"]
    size: ImageSize

class TargetSizeSourceTopicOption(BaseModel):
    """Auto-generated class for inline option 'topic' of TargetSizeSource"""
    source_type: Literal["topic"]
    topic: str

class ThresholdSourceTopicOption(BaseModel):
    """Auto-generated class for inline option 'topic' of ThresholdSource"""
    source_type: Literal["topic"]
    topic: str

class ThresholdSourceValueOption(BaseModel):
    """Auto-generated class for inline option 'value' of ThresholdSource"""
    source_type: Literal["value"]
    value: float

# --- Main Recipe Class ---
class InferenceGraphRecipe(BaseModel):
    nodes: List[Node]
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

MaxIterationsCountSource = Annotated[
    Union[
        MaxIterationsCountSourceTopicOption,
        MaxIterationsCountSourceValueOption
    ],
    Field(discriminator='source_type')
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
        BoundingBoxFilterNode,
        ClassificationNode,
        ConstTensorNode,
        ImagePatchesNode,
        ImageResizeNode,
        ObjectDetectionNode,
        OcrNode,
        VirtualCameraNode
    ],
    Field(discriminator='node_type')
]

TargetSizeSource = Annotated[
    Union[
        TargetSizeSourceImageSizeOption,
        TargetSizeSourceTopicOption
    ],
    Field(discriminator='source_type')
]

ThresholdSource = Annotated[
    Union[
        ThresholdSourceTopicOption,
        ThresholdSourceValueOption
    ],
    Field(discriminator='source_type')
]

