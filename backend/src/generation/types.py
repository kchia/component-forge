"""
Type definitions for the code generation module.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class GenerationStage(str, Enum):
    """Stages of the code generation pipeline."""
    PARSING = "parsing"
    INJECTING = "injecting"
    GENERATING = "generating"
    IMPLEMENTING = "implementing"
    ASSEMBLING = "assembling"
    FORMATTING = "formatting"
    COMPLETE = "complete"


class GenerationRequest(BaseModel):
    """Request model for code generation."""
    pattern_id: str = Field(..., description="ID of the pattern to use")
    tokens: Dict[str, Any] = Field(..., description="Design tokens from extraction")
    requirements: Dict[str, Any] = Field(..., description="Approved requirements")
    component_name: Optional[str] = Field(None, description="Optional custom component name")


class PatternStructure(BaseModel):
    """Structured representation of a parsed pattern."""
    component_name: str
    props_interface: str
    imports: List[str]
    variants: List[str]
    modification_points: Dict[str, Any]
    code: str
    metadata: Dict[str, Any]


class TokenMapping(BaseModel):
    """Mapping between design tokens and component styles."""
    colors: Dict[str, str] = Field(default_factory=dict)
    typography: Dict[str, str] = Field(default_factory=dict)
    spacing: Dict[str, str] = Field(default_factory=dict)
    css_variables: str = Field(default="")


class CodeParts(BaseModel):
    """Individual parts of the generated component code."""
    provenance_header: str = Field(default="")
    imports: List[str] = Field(default_factory=list)
    css_variables: str = Field(default="")
    type_definitions: str = Field(default="")
    component_code: str = Field(default="")
    storybook_stories: str = Field(default="")
    component_name: str = Field(default="")


class GenerationMetadata(BaseModel):
    """Metadata about the generation process."""
    latency_ms: int = Field(..., description="Total generation latency in milliseconds")
    stage_latencies: Dict[GenerationStage, int] = Field(default_factory=dict)
    token_count: int = Field(default=0, description="Number of tokens injected")
    lines_of_code: int = Field(default=0, description="Total lines of generated code")
    requirements_implemented: int = Field(default=0, description="Number of requirements implemented")


class GenerationResult(BaseModel):
    """Result of the code generation process."""
    component_code: str = Field(..., description="Generated component code")
    stories_code: str = Field(..., description="Generated Storybook stories code")
    files: Dict[str, str] = Field(..., description="Map of filename to content")
    metadata: GenerationMetadata = Field(..., description="Generation metadata")
    success: bool = Field(default=True)
    error: Optional[str] = Field(None, description="Error message if failed")
