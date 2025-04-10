"""Models for the Cognyx BOM SDK."""

from enum import Enum
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class BomStatus(Enum):
    """Status of a BOM."""

    DRAFT = "draft"
    APPROVED = "published"


class SystemAttributesStyling(TypedDict):
    """Styling for a system attribute."""

    color: str
    icon: str


class SystemAttributes(TypedDict):
    """System attributes for a diversity."""

    styling: SystemAttributesStyling


PermissionsList = TypeVar("PermissionsList", bound=str)


class Auth(TypedDict, Generic[PermissionsList]):
    """Authentication permissions for a diversity."""

    can: dict[PermissionsList, bool]


class Diversity(BaseModel):
    """Represents a diversity."""

    id: str
    name: str
    description: str
    reference: str
    created_at: str
    updated_at: str

    system_attributes: SystemAttributes

    auth: Auth[Literal["view"] | Literal["update"] | Literal["delete"]]


class BomReadinessView(TypedDict):
    """Readiness of a BOM view."""

    id: str
    name: str


class BomReadinessStatusCount(TypedDict):
    """Count of BOM readiness statuses."""

    not_started: int
    in_progress: int
    done: int


class BomReadiness(BaseModel):
    """Readiness of a BOM."""

    view: BomReadinessView
    total_instances: int
    statuses: BomReadinessStatusCount


class BomResponse(BaseModel):
    """Response from the Cognyx BOM API GET /bom/{bom_id}."""

    id: str
    name: str
    description: str
    reference: str
    image: str | None = None
    status: BomStatus

    created_at: str
    updated_at: str

    variability_configurations: None | list[Diversity] = []
    bom_readiness: None | list[BomReadiness] = []

    auth: Auth[
        Literal["comment"]
        | Literal["create"]
        | Literal["create_revision"]
        | Literal["delete"]
        | Literal["update"]
        | Literal["view"]
        | Literal["share"]
    ]


class BomConfig(TypedDict):
    """BOM configuration."""

    default_type: Literal["tree"] | Literal["table"]
    default_view: str


class ProjectSettings(TypedDict):
    """Project settings."""

    bom: BomConfig


class FeaturesSettings(TypedDict):
    """Features settings."""

    projects: ProjectSettings


class GlobalSettingsResponse(BaseModel):
    """Response from the Cognyx BOM API GET /settings/global."""

    app_client_id: str
    cognyx_client_id: str
    features: FeaturesSettings


class BomNode(BaseModel):
    """Node in a BOM tree."""

    id: str
    label: str
    description: str
    reference: str
    group: str


class BomEdge(BaseModel):
    """Edge in a BOM tree."""

    id: int
    source: str = Field(..., alias="from")
    target: str = Field(..., alias="to")


class BomTree(BaseModel):
    """Response from the Cognyx BOM API GET /bom/{bom_id}/tree."""

    nodes: list[BomNode]
    edges: list[BomEdge]
