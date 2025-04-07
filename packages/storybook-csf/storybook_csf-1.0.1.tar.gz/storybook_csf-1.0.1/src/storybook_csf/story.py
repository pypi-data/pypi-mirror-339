"""Type definitions for Component Story Format v3."""

from typing import Any, Dict, List, Literal, Optional, Union

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


# Base Types
class SBBaseType(TypedDict, total=False):
    required: bool
    raw: str


class SBScalarType(SBBaseType, total=False):
    name: Literal["boolean", "string", "number", "function", "symbol"]


class SBArrayType(SBBaseType, total=False):
    name: Literal["array"]
    value: "SBType"


class SBObjectType(SBBaseType, total=False):
    name: Literal["object"]
    value: Dict[str, "SBType"]


class SBEnumType(SBBaseType, total=False):
    name: Literal["enum"]
    value: List[Union[str, int]]


class SBIntersectionType(SBBaseType, total=False):
    name: Literal["intersection"]
    value: List["SBType"]


class SBUnionType(SBBaseType, total=False):
    name: Literal["union"]
    value: List["SBType"]


class SBOtherType(SBBaseType, total=False):
    name: Literal["other"]
    value: str


# SBType is a Union of all the above types
SBType = Union[
    SBScalarType,
    SBEnumType,
    SBArrayType,
    SBObjectType,
    SBIntersectionType,
    SBUnionType,
    SBOtherType,
]

# Story Types
StoryId = str
ComponentId = str
ComponentTitle = str
StoryName = str
Tag = str


class StoryIdentifier(TypedDict):
    componentId: ComponentId
    title: ComponentTitle
    kind: ComponentTitle
    """@deprecated"""

    id: StoryId
    name: StoryName
    story: StoryName
    """@deprecated"""

    tags: List[Tag]


Parameters = Dict[str, Any]

# Control Types
ControlType = Literal[
    "object",
    "boolean",
    "check",
    "inline-check",
    "radio",
    "inline-radio",
    "select",
    "multi-select",
    "number",
    "range",
    "file",
    "color",
    "date",
    "text",
]


class ConditionalTest(TypedDict, total=False):
    truthy: Optional[bool]
    exists: Optional[bool]
    eq: Any
    neq: Any


# NOTE: ConditionalValue is defined functionally to allow for the use of the `global` keyword
ConditionalValue = TypedDict("ConditionalValue", {"arg": str, "global": str}, total=False)


# Combine ConditionalValue and ConditionalTest
class Conditional(ConditionalValue, ConditionalTest):
    pass


# Control type definitions - each as a separate TypedDict without inheritance
class ColorControl(TypedDict, total=False):
    type: Literal["color"]
    disable: bool
    presetColors: List[str]
    """@see https://storybook.js.org/docs/api/arg-types#controlpresetcolors"""


class FileControl(TypedDict, total=False):
    type: Literal["file"]
    disable: bool
    accept: str
    """@see https://storybook.js.org/docs/api/arg-types#controlaccept"""


class SelectControl(TypedDict, total=False):
    type: Literal["inline-check", "radio", "inline-radio", "select", "multi-select"]
    disable: bool
    labels: Dict[str, str]
    """@see https://storybook.js.org/docs/api/arg-types#controllabels"""


class NumberControl(TypedDict, total=False):
    type: Literal["number", "range"]
    disable: bool
    max: float
    """@see https://storybook.js.org/docs/api/arg-types#controlmax"""
    min: float
    """@see https://storybook.js.org/docs/api/arg-types#controlmin"""
    step: float
    """@see https://storybook.js.org/docs/api/arg-types#controlstep"""


class BasicControl(TypedDict, total=False):
    type: Literal["object", "boolean", "check", "date", "text"]
    disable: bool


# Union type for all possible control configurations
Control = Union[
    ControlType,  # Simple string literal
    bool,  # False to disable
    BasicControl,
    ColorControl,
    FileControl,
    SelectControl,
    NumberControl,
]


class TableFieldValue(TypedDict, total=False):
    summary: str
    detail: str


class TableField(TypedDict, total=False):
    category: str
    """@see https://storybook.js.org/docs/api/arg-types#tablecategory"""
    defaultValue: TableFieldValue
    """@see https://storybook.js.org/docs/api/arg-types#tabledefaultvalue"""
    disable: bool
    """@see https://storybook.js.org/docs/api/arg-types#tabledisable"""
    subcategory: str
    """@see https://storybook.js.org/docs/api/arg-types#tablesubcategory"""
    type: TableFieldValue
    """@see https://storybook.js.org/docs/api/arg-types#tabletype"""


# InputType, but without `if` as it's a Python keyword.
# So we need to add `if` by instantiating TypedDict as a function.
# But in that case we can't add docstrings. So this base class defines
# all fields that CAN have docstrings.
class InputTypeBase(TypedDict, total=False):
    control: Optional[Control]
    """@see https://storybook.js.org/docs/api/arg-types#control"""
    description: str
    """@see https://storybook.js.org/docs/api/arg-types#description"""
    mapping: Dict[str, Any]
    """@see https://storybook.js.org/docs/api/arg-types#mapping"""
    name: str
    """@see https://storybook.js.org/docs/api/arg-types#name"""
    options: List[Any]
    """@see https://storybook.js.org/docs/api/arg-types#options"""
    table: TableField
    """@see https://storybook.js.org/docs/api/arg-types#table"""
    type: Union[SBType, Literal["boolean", "string", "number", "function", "symbol"]]
    """@see https://storybook.js.org/docs/api/arg-types#type"""
    defaultValue: Any
    """
    @deprecated
    @see https://storybook.js.org/docs/api/arg-types#defaultvalue
    """


InputTypeReserved = TypedDict("InputTypeReserved", {"if": Conditional}, total=False)


class InputType(InputTypeBase, InputTypeReserved):
    pass


Args = Dict[str, Any]
ArgTypes = Dict[str, InputType]
"""@see https://storybook.js.org/docs/api/arg-types#argtypes"""
Globals = Dict[str, Any]
GlobalTypes = Dict[str, InputType]


class BaseAnnotations(TypedDict, total=False):
    parameters: Parameters
    """
    Custom metadata for a story.

    @see [Parameters](https://storybook.js.org/docs/writing-stories/parameters)
    """
    args: Dict[str, Any]  # Partial[TArgs]
    """
    Dynamic data that are provided (and possibly updated by) Storybook and its addons.

    @see [Args](https://storybook.js.org/docs/writing-stories/args)
    """
    argTypes: Dict[str, InputType]  # Partial[ArgTypes[TArgs]]
    """
    ArgTypes encode basic metadata for args, such as `name`, `description`, `defaultValue` for an
    arg. These get automatically filled in by Storybook Docs.

    @see [ArgTypes](https://storybook.js.org/docs/api/arg-types)
    """
    tags: List[Tag]
    """Named tags for a story, used to filter stories in different contexts."""


class ProjectAnnotations(BaseAnnotations, total=False):
    globals: Globals
    """@deprecated Project `globals` renamed to `initialGlobals`"""
    initialGlobals: Globals
    globalTypes: GlobalTypes


class ComponentAnnotations(BaseAnnotations, total=False):
    title: ComponentTitle
    """
    Title of the component which will be presented in the navigation. **Should be unique.**

    Components can be organized in a nested structure using "/" as a separator.

    Since CSF 3.0 this property is optional -- it can be inferred from the filesystem path

    @example Export default { ... title: 'Design System/Atoms/Button' }

    @see [Story Hierarchy](https://storybook.js.org/docs/writing-stories/naming-components-and-hierarchy#structure-and-hierarchy)
    """  # noqa: E501
    id: ComponentId
    """
    Id of the component (prefix of the story id) which is used for URLs.

    By default is inferred from sanitizing the title

    @see [Permalink to stories](https://storybook.js.org/docs/configure/sidebar-and-urls#permalink-to-stories)
    """
    globals: Globals
    """Override the globals values for all stories in this component"""
    stories: List["StoryAnnotations"]
    """
    List of stories in this component - This is specific only to
    [Storybook for Server](https://github.com/storybookjs/storybook/tree/next/code/frameworks/server-webpack5)
    """


class StoryAnnotations(BaseAnnotations, total=False):
    name: StoryName
    """Override the display name in the UI (CSF v3)"""
    storyName: StoryName
    """Override the display name in the UI (CSF v2)"""
    globals: Globals
    """Override the globals values for this story"""
