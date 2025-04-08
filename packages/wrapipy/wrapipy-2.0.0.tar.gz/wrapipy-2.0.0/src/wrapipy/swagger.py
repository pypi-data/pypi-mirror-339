"""Pydantic models of Swagger 2.0 components.

## Pydantic Models

For all `pydantic.BaseModel` child classes it holds that:

- You can create a new model by parsing and validating input data from keyword arguments.
- The initialisation raises `pydantic_core.ValidationError` if the input data cannot be validated to form a valid model.
- `self` is explicitly positional-only to allow `self` as a field name.
"""

from __future__ import annotations

import re
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

__pdoc__ = {}
RE_MIME_TYPE = re.compile(
    r'\w+\/[\w\.-]+(?:\+(?:[\w\.-]+))*(?:\s*;\s*(?:[^=]+?)(?:="?(?:[\S\.-]+?)"?)?)*$'
)
"""Regular expression matching MIME types."""
RE_URL = re.compile(
    r"(?:http[s]?:\/\/.)?(?:www\.)?[-a-zA-Z0-9@%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)"
)
"""Regular expression matching a URL."""
RE_EMAIL = re.compile(r"^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$")
"""Regular expression matching an email address."""
RE_RESPONSES = re.compile(r"\d{3}|default")
"""Regular expression matching a response code."""

Schemes = List[Literal["http", "https", "ws", "wss"]]
"""The set of schemes allowed in Swagger 2.0."""
ObjectType = Literal[
    "string", "number", "integer", "boolean", "array", "object", "file"
]
"""List of types allowed in Swagger 2.0."""
ObjectSubtype = Literal[
    "int32",
    "int64",
    "float",
    "double",
    "byte",
    "binary",
    "date",
    "dateTime",
    "password",
]
"""List of formats allowed in Swagger 2.0."""
Number = Union[int, float]
"""A float or an integer"""
SecurityRequirement = Dict[str, List[str]]
"""A security requirement entry."""
URLString = Annotated[str, Field(pattern=RE_URL)]
"""A string expressing a URL."""
EmailString = Annotated[str, Field(pattern=RE_EMAIL)]
"""A string expressing an email."""
MimeEntry = Annotated[str, Field(pattern=RE_MIME_TYPE)]
"""A string expressing a MIME type."""
ResponseString = Annotated[str, Field(pattern=RE_RESPONSES)]
"""A string expressing a response code."""
MimeList = List[MimeEntry]
"""A list of MIME type strings."""


def _aliased(x: str) -> str:
    """_aliased.

    Args:
        x (str): x

    Returns:
        str:
    """
    return f"\n\nThe field name is `{x}` in Swagger."


def _opt_attr_model(x: str) -> str:
    """_opt_attr_model.

    Args:
        x (str): x

    Returns:
        str:
    """
    return f"A model with an optional `{x}` attribute."


def _swagger_link(x: str) -> str:
    """_swagger_link.

    Args:
        x (str): x

    Returns:
        str:
    """
    return f"[Swagger's {x} Object](https://swagger.io/specification/v2/#{x.lower().replace(' ', '-')}-object)"


def _pydantic(x: str) -> str:
    """_pydantic.

    Args:
        x (str): x

    Returns:
        str:
    """
    return f"A Pydantic representation of {_swagger_link(x)}."


class HasName(BaseModel):
    """A model with an optional `name` attribute."""

    __pdoc__["HasName.__init__"] = _opt_attr_model("name")
    name: Optional[str] = Field(default=None)
    __pdoc__["HasName.name"] = "Name."
    __pdoc__["HasName.model_config"] = False


class HasURL(BaseModel):
    """A model with an optional `url` attribute."""

    __pdoc__["HasURL.__init__"] = _opt_attr_model("url")
    url: Optional[URLString] = Field(default=None)
    __pdoc__["HasURL.url"] = "URL."
    __pdoc__["HasURL.model_config"] = False


class HasDesc(BaseModel):
    """A model with an optional `description` attribute."""

    __pdoc__["HasDesc.__init__"] = _opt_attr_model("description")
    description: Optional[str] = Field(default=None)
    __pdoc__["HasDesc.description"] = "Description."
    __pdoc__["HasDesc.model_config"] = False


class HasTitle(BaseModel):
    """A model with an optional `title` attribute."""

    __pdoc__["HasTitle.__init__"] = _opt_attr_model("title")
    title: Optional[str] = Field(default=None)
    __pdoc__["HasTitle.title"] = "Title."
    __pdoc__["HasTitle.model_config"] = False


class HasRef(BaseModel):
    """A model with an optional `ref` attribute."""

    __pdoc__["HasRef.__init__"] = _opt_attr_model("ref")
    ref: Optional[str] = Field(alias="$ref", default=None)
    __pdoc__["HasRef.ref"] = f"The name of the referenced object. {_aliased('$ref')}"
    __pdoc__["HasRef.model_config"] = False


class HasSchema(BaseModel):
    """A model with an optional `schema` attribute."""

    __pdoc__["HasSchema.__init__"] = _opt_attr_model("schema_")
    schema_: Optional[Union[SwaggerSchema, SwaggerReference]] = Field(
        default=None, alias="schema"
    )
    __pdoc__["HasSchema.schema_"] = (
        "A reference (`SwaggerReference`) to a schema object or the schema object (`SwaggerSchema`)."
        + _aliased("schema")
    )
    __pdoc__["HasSchema.model_config"] = False


class HasTypes(BaseModel):
    """A model with a `type` attribute and an optional `format` attribute."""

    __pdoc__["HasTypes.__init__"] = (
        "A model with a `type` attribute and an optional `format` attribute."
    )
    type_: ObjectType = Field(alias="type", default="string")
    __pdoc__["HasTypes.type_"] = f"The data type. {_aliased('type')}"
    format_: Optional[ObjectSubtype] = Field(alias="format", default=None)
    __pdoc__["HasTypes.format_"] = f"The data format. {_aliased('format')}"
    __pdoc__["HasTypes.model_config"] = False


class SwaggerExternalDocs(HasURL, HasDesc):
    """A Pydantic representation of Swagger's External Documentation Object."""

    __pdoc__["SwaggerExternalDocs.__init__"] = _pydantic("External Documentation")
    __pdoc__["SwaggerExternalDocs.model_config"] = False


class HasExternalDocs(BaseModel):
    """HasExternalDocs.
    """

    __pdoc__["HasExternalDocs.__init__"] = _opt_attr_model("external_docs")
    external_docs: Optional[SwaggerExternalDocs] = Field(
        default=None, alias="externalDocs"
    )
    __pdoc__["HasExternalDocs.external_docs"] = _aliased("externalDocs")
    __pdoc__["HasExternalDocs.model_config"] = False


class SwaggerLicense(HasURL, HasName):
    """A Pydantic representation of Swagger's License Object."""

    __pdoc__["SwaggerLicense.__init__"] = _pydantic("License")
    __pdoc__["SwaggerLicense.model_config"] = False


class SwaggerReference(HasRef):
    """A Pydantic representation of Swagger's Reference Object."""

    __pdoc__["SwaggerReference.__init__"] = _pydantic("Reference")
    __pdoc__["SwaggerReference.model_config"] = False


class SwaggerContact(HasURL, HasName):
    """A Pydantic representation of Swagger's Contact Object."""

    __pdoc__["SwaggerContact.__init__"] = _pydantic("Contact")
    email: Optional[EmailString] = Field(default=None)
    __pdoc__["SwaggerContact.email"] = " "
    __pdoc__["SwaggerContact.model_config"] = False


class SwaggerTag(HasDesc, HasName, HasExternalDocs):
    """A Pydantic representation of Swagger's Tag Object."""

    __pdoc__["SwaggerTag.__init__"] = _pydantic("Tag")
    __pdoc__["SwaggerTag.model_config"] = False


class SwaggerInfo(HasDesc, HasTitle):
    """A Pydantic representation of Swagger's Info Object."""

    __pdoc__["SwaggerInfo.__init__"] = _pydantic("Info")
    terms: Optional[str] = Field(alias="termsOfService", default=None)
    __pdoc__["SwaggerInfo.terms"] = _aliased("termsOfService")
    contact: Optional[SwaggerContact] = Field(default=None)
    __pdoc__["SwaggerInfo.contact"] = " "
    license_: Optional[SwaggerLicense] = Field(alias="license", default=None)
    __pdoc__["SwaggerInfo.license_"] = _aliased("license")
    version: str = Field(default="1.0.0")
    __pdoc__["SwaggerInfo.version"] = " "
    __pdoc__["SwaggerInfo.model_config"] = False


class SwaggerXML(HasName):
    """A Pydantic representation of Swagger's XML Object."""

    __pdoc__["SwaggerXML.__init__"] = _pydantic("XML")
    namespace: Optional[str] = Field(default=None)
    __pdoc__["SwaggerXML.namespace"] = " "
    prefix: Optional[str] = Field(default=None)
    __pdoc__["SwaggerXML.prefix"] = " "
    attribute: bool = Field(default=False)
    __pdoc__["SwaggerXML.attribute"] = " "
    wrapped: bool = Field(default=False)
    __pdoc__["SwaggerXML.wrapped"] = " "
    __pdoc__["SwaggerXML.model_config"] = False


class SwaggerItem(HasTypes):
    """A model of item-related fields in Swagger shared by Swagger's Items Object, Schema Object,
    Parameter Object, and Header Object.
    """

    __pdoc__["SwaggerItem.__init__"] = (
        f"A model of item-related fields in Swagger shared by {_swagger_link('Items')}, "
        + f"{_swagger_link('Schema')}, {_swagger_link('Parameter')}, and {_swagger_link('Header')}."
    )
    default: Any = Field(default=None)
    __pdoc__["SwaggerItem.default"] = " "
    maximum: Optional[Number] = Field(default=None)
    __pdoc__["SwaggerItem.maximum"] = " "
    exclusive_maximum: Optional[bool] = Field(alias="exclusiveMaximum", default=None)
    __pdoc__["SwaggerItem.exclusive_maximum"] = _aliased("exclusiveMaximum")
    minimum: Optional[Number] = Field(default=None)
    __pdoc__["SwaggerItem.minimum"] = " "
    exclusive_minimum: Optional[bool] = Field(alias="exclusiveMinimum", default=None)
    __pdoc__["SwaggerItem.exclusive_minimum"] = _aliased("exclusiveMinimum")
    max_length: Optional[int] = Field(alias="maxLength", default=None)
    __pdoc__["SwaggerItem.max_length"] = _aliased("maxLength")
    min_length: Optional[int] = Field(alias="minLength", default=None)
    __pdoc__["SwaggerItem.min_length"] = _aliased("minLength")
    pattern: Optional[str] = Field(default=None)
    __pdoc__["SwaggerItem.pattern"] = " "
    max_items: Optional[int] = Field(alias="maxItems", default=None)
    __pdoc__["SwaggerItem.max_items"] = _aliased("maxItems")
    min_items: Optional[int] = Field(alias="minItems", default=None)
    __pdoc__["SwaggerItem.min_items"] = _aliased("minItems")
    unique_items: Optional[bool] = Field(alias="uniqueItems", default=None)
    __pdoc__["SwaggerItem.unique_items"] = _aliased("uniqueItems")
    enum: Optional[List] = Field(default=None)
    __pdoc__["SwaggerItem.enum"] = " "
    multiple: Optional[Number] = Field(alias="multipleOf", default=None)
    __pdoc__["SwaggerItem.multiple"] = _aliased("multipleOf")
    items: Optional[SwaggerItems] = Field(default=None)
    __pdoc__["SwaggerItem.items"] = " "
    __pdoc__["SwaggerItem.model_config"] = False


class SwaggerSchema(SwaggerItem, HasDesc, HasTitle, HasRef, HasExternalDocs):
    """A Pydantic representation of Swagger's Schema Object."""

    __pdoc__["SwaggerSchema.__init__"] = _pydantic("Schema")
    max_properties: Optional[Number] = Field(alias="maxProperties", default=None)
    __pdoc__["SwaggerSchema.max_properties"] = _aliased("maxProperties")
    min_properties: Optional[Number] = Field(alias="minProperties", default=None)
    __pdoc__["SwaggerSchema.min_properties"] = _aliased("minProperties")
    required: bool = Field(default=False)
    __pdoc__["SwaggerSchema.required"] = " "
    all_of: Optional[List[SwaggerSchema]] = Field(default=None)
    __pdoc__["SwaggerSchema.all_of"] = " "
    properties: Optional[Dict[str, SwaggerSchema]] = Field(default=None)
    __pdoc__["SwaggerSchema.properties"] = " "
    additional_properties: Optional[SwaggerSchema] = Field(
        default=None, alias="additionalProperties"
    )
    __pdoc__["SwaggerSchema.additional_properties"] = _aliased("additionalProperties")
    discriminator: Optional[str] = Field(default=None)
    __pdoc__["SwaggerSchema.discriminator"] = " "
    read_only: bool = Field(default=False, alias="readOnly")
    __pdoc__["SwaggerSchema.read_only"] = _aliased("readOnly")
    xml: Optional[SwaggerXML] = Field(default=None)
    __pdoc__["SwaggerSchema.xml"] = " "
    example: Any = Field(default=None)
    __pdoc__["SwaggerSchema.example"] = " "
    __pdoc__["SwaggerSchema.model_config"] = False


class SwaggerItems(SwaggerItem):
    """A Pydantic representation of Swagger's Items Object."""

    __pdoc__["SwaggerItems.__init__"] = _pydantic("Items")
    collection_format: Literal["csv", "ssv", "tsv", "pipes", "multi"] = Field(
        default="csv", alias="collectionFormat"
    )
    __pdoc__["SwaggerItems.collection_format"] = _aliased("collectionFormat")
    __pdoc__["SwaggerItems.model_config"] = False


class SwaggerHeader(SwaggerItems, HasDesc):
    """A Pydantic representation of Swagger's Header Object."""

    __pdoc__["SwaggerHeader.__init__"] = _pydantic("Header")
    __pdoc__["SwaggerHeader.model_config"] = False


class SwaggerResponse(HasDesc, HasSchema):
    """A Pydantic representation of Swagger's Response Object."""

    __pdoc__["SwaggerResponse.__init__"] = _pydantic("Response")
    headers: Optional[Dict[str, SwaggerHeader]] = Field(default=None)
    __pdoc__["SwaggerResponse.headers"] = " "
    examples: Optional[Dict[MimeEntry, Any]] = Field(default=None)
    __pdoc__["SwaggerResponse.examples"] = " "
    __pdoc__["SwaggerResponse.model_config"] = False


class SwaggerParameter(HasDesc, HasName, HasSchema, SwaggerItems):
    """A Pydantic representation of Swagger's Parameter Object."""

    __pdoc__["SwaggerParameter.__init__"] = _pydantic("Parameter")
    in_: Literal["query", "header", "path", "formData", "body"] = Field(
        alias="in", default="query"
    )
    __pdoc__["SwaggerParameter.in_"] = _aliased("in")
    required: bool = Field(default=False)
    __pdoc__["SwaggerParameter.required"] = " "
    allow_empty: bool = Field(default=False, alias="allowEmptyValue")
    __pdoc__["SwaggerParameter.allow_empty"] = _aliased("allowEmptyValue")
    __pdoc__["SwaggerParameter.model_config"] = False


class SwaggerOperation(HasDesc, HasExternalDocs):
    """A Pydantic representation of Swagger's Operation Object."""

    __pdoc__["SwaggerOperation.__init__"] = _pydantic("Operation")
    responses: Union[
        Dict[ResponseString, SwaggerResponse],
        SwaggerReference,
    ]
    __pdoc__["SwaggerOperation.responses"] = " "
    tags: Optional[List[str]] = Field(default=None)
    __pdoc__["SwaggerOperation.tags"] = " "
    summary: Optional[str] = Field(default=None)
    __pdoc__["SwaggerOperation.summary"] = " "
    operation_id: Optional[str] = Field(alias="operationId", default=None)
    __pdoc__["SwaggerOperation.operation_id"] = _aliased("operationId")
    consumes: Optional[MimeList] = Field(default=None)
    __pdoc__["SwaggerOperation.consumes"] = " "
    produces: Optional[MimeList] = Field(default=None)
    __pdoc__["SwaggerOperation.produces"] = " "
    parameters: Optional[List[SwaggerParameter]] = Field(default=None)
    __pdoc__["SwaggerOperation.parameters"] = " "
    schemes: Optional[Schemes] = Field(default=None)
    __pdoc__["SwaggerOperation.schemes"] = " "
    deprecated: bool = Field(default=False)
    __pdoc__["SwaggerOperation.deprecated"] = " "
    security: Optional[SecurityRequirement] = Field(default=None)
    __pdoc__["SwaggerOperation.security"] = " "
    __pdoc__["SwaggerOperation.model_config"] = False


class SwaggerPath(HasRef):
    """A Pydantic representation of Swagger's Paths Object as `Dict[str, SwaggerPath]`."""

    __pdoc__["SwaggerPath.__init__"] = (
        f"A Pydantic representation of {_swagger_link('Paths')} as `Dict[str, SwaggerPath]`."
    )
    get: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.get"] = " "
    put: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.put"] = " "
    post: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.post"] = " "
    delete: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.delete"] = " "
    options: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.options"] = " "
    head: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.head"] = " "
    patch: Optional[SwaggerOperation] = Field(default=None)
    __pdoc__["SwaggerPath.patch"] = " "
    parameters: Optional[List[Union[SwaggerReference, SwaggerParameter]]] = Field(
        default=None
    )
    __pdoc__["SwaggerPath.parameters"] = " "
    __pdoc__["SwaggerPath.model_config"] = False


class SwaggerSecurityScheme(HasDesc, HasName):
    """A Pydantic representation of Swagger's Security Scheme Object."""

    __pdoc__["SwaggerSecurityScheme.__init__"] = _pydantic("Security Scheme")
    type_: str = Field(alias="type")
    __pdoc__["SwaggerSecurityScheme.type_"] = _aliased("type")
    in_: Literal["query", "header"] = Field(alias="in", default="query")
    __pdoc__["SwaggerSecurityScheme.in_"] = _aliased("in")
    flow: Literal["implicit", "password", "application", "accessCode"] = Field(
        default="implicit"
    )
    __pdoc__["SwaggerSecurityScheme.flow"] = " "
    authorization_url: Optional[str] = Field(alias="authorizationUrl", default=None)
    __pdoc__["SwaggerSecurityScheme.authorization_url"] = _aliased("authorizationUrl")
    token_url: Optional[str] = Field(alias="tokenUrl", default=None)
    __pdoc__["SwaggerSecurityScheme.token_url"] = _aliased("tokenUrl")
    scopes: Dict[str, str] = Field(default={})
    __pdoc__["SwaggerSecurityScheme.scopes"] = " "
    __pdoc__["SwaggerSecurityScheme.model_config"] = False


class SwaggerDoc(HasExternalDocs):
    """A Pydantic representation of Swagger 2.0."""

    __pdoc__["SwaggerDoc.__init__"] = (
        "A Pydantic representation of [Swagger 2.0](https://swagger.io/specification/v2/)."
    )
    swagger: str = Field(default="2.0")
    __pdoc__["SwaggerDoc.swagger"] = (
        'The Swagger version. Should be `"2.0"` as others were not tested.'
    )
    info: SwaggerInfo = Field(default=SwaggerInfo())
    __pdoc__["SwaggerDoc.info"] = " "
    host: Optional[str] = Field(default=None)
    __pdoc__["SwaggerDoc.host"] = "The host without the protocol indication."
    base_path: Optional[str] = Field(alias="basePath", default=None)
    __pdoc__["SwaggerDoc.base_path"] = (
        "Path to be added after the host for each request of every endpoint."
        + _aliased("basePath")
    )
    schemes: Schemes = Field(default=["http"])
    __pdoc__["SwaggerDoc.schemes"] = " "
    consumes: MimeList = Field(default=None)
    __pdoc__["SwaggerDoc.consumes"] = " "
    produces: MimeList = Field(default=None)
    __pdoc__["SwaggerDoc.produces"] = " "
    paths: Dict[str, SwaggerPath] = Field(default={})
    __pdoc__["SwaggerDoc.paths"] = " "
    definitions: Optional[Dict[str, SwaggerSchema]] = Field(default=None)
    __pdoc__["SwaggerDoc.definitions"] = " "
    parameters: Optional[Dict[str, SwaggerParameter]] = Field(default=None)
    __pdoc__["SwaggerDoc.parameters"] = " "
    responses: Optional[Union[Dict[str, SwaggerResponse], SwaggerReference]] = Field(
        default=None
    )
    __pdoc__["SwaggerDoc.responses"] = " "
    security_definitions: Optional[Dict[str, SwaggerSecurityScheme]] = Field(
        default=None, alias="securityDefinitions"
    )
    __pdoc__["SwaggerDoc.security_definitions"] = _aliased("securityDefinitions")
    security: Optional[SecurityRequirement] = Field(default=None)
    __pdoc__["SwaggerDoc.security"] = " "
    tags: Optional[List[SwaggerTag]] = Field(default=None)
    __pdoc__["SwaggerDoc.tags"] = " "
    __pdoc__["SwaggerDoc.model_config"] = False
