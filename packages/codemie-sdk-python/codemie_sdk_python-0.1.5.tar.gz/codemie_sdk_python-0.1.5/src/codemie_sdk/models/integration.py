"""Models for assistant-related data structures."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, Field, ConfigDict


class CredentialTypes(str, Enum):
    """Enum for credential types."""

    JIRA = "Jira"
    CONFLUENCE = "Confluence"
    GIT = "Git"
    KUBERNETES = "Kubernetes"
    AWS = "AWS"
    GCP = "GCP"
    KEYCLOAK = "Keycloak"
    AZURE = "Azure"
    ELASTIC = "Elastic"
    OPENAPI = "OpenAPI"
    PLUGIN = "Plugin"
    FILESYSTEM = "FileSystem"
    SCHEDULER = "Scheduler"
    WEBHOOK = "Webhook"
    EMAIL = "Email"
    AZURE_DEVOPS = "AzureDevOps"
    SONAR = "Sonar"
    SQL = "SQL"
    TELEGRAM = "Telegram"
    ZEPHYR_CLOUD = "ZephyrCloud"
    ZEPHYR_SQUAD = "ZephyrSquad"
    SERVICE_NOW = "ServiceNow"
    DIAL = "DIAL"


class IntegrationType(str, Enum):
    """Enum for setting types."""

    USER = "user"
    PROJECT = "project"


class CredentialValues(BaseModel):
    """Model for credential values."""

    model_config = ConfigDict(extra="ignore")

    key: str
    value: Any


class Integration(BaseModel):
    """Model for settings configuration."""

    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    user_id: Optional[str] = None
    project_name: str
    alias: Optional[str] = None
    default: bool = False
    credential_type: CredentialTypes
    credential_values: List[CredentialValues]
    setting_type: IntegrationType = Field(default=IntegrationType.USER)
