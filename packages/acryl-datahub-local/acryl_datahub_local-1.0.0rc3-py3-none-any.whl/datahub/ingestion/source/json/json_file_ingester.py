import json
from dataclasses import dataclass
from typing import Iterable, Any
from typing import List, Optional, Dict
import hashlib

from datahub.configuration.common import ConfigModel
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    support_status,
    config_class,
    platform_name,
    capability,
    SupportStatus,
    SourceCapability,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.metadata.schema_classes import (
    SchemaMetadataClass,
    SchemaFieldClass,
    SchemaFieldDataTypeClass,
    StringTypeClass,
    NumberTypeClass,
    BooleanTypeClass,
    GlobalTagsClass,
    TagAssociationClass,
    OtherSchemaClass,
    OwnershipClass,
    OwnerClass,
    EditableDatasetPropertiesClass,
)
from flatten_json import flatten
from pydantic import Field, validator


def infer_type(value: Any) -> SchemaFieldDataTypeClass:
    if isinstance(value, bool):
        return SchemaFieldDataTypeClass(BooleanTypeClass())
    elif isinstance(value, (int, float)):
        return SchemaFieldDataTypeClass(NumberTypeClass())
    else:
        return SchemaFieldDataTypeClass(StringTypeClass())

def collect_schema_fields(data: List[Dict[str, Any]], sample_limit: int = 100) -> Dict[str, Any]:
    field_examples = {}
    for record in data[:sample_limit]:
        flat = flatten(record)
        for field, value in flat.items():
            if field not in field_examples:
                field_examples[field] = value
    return field_examples

class JsonIngestionConfig(ConfigModel):
    path: str = Field(
        description="Path to the local or remote JSON file to ingest."
    )
    dataset_name: str = Field(
        default="json.events",
        description="Dataset name to register inside DataHub (used in the URN)."
    )
    platform: str = Field(
        default="json",
        description="Platform name for the dataset URN (e.g., json, kafka, etc.)."
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional description to attach to the dataset."
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="List of tag URNs to attach to the dataset."
    )
    owners: Optional[List[str]] = Field(
        default=None,
        description="List of owner URNs to assign to the dataset."
    )
    field_descriptions: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional per-field descriptions. Keys are flattened field paths."
    )
    field_tags: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Optional per-field tags. Keys are flattened field paths."
    )
    write_semantics: str = Field(
        default="PATCH",
        description='PATCH will merge with existing metadata; OVERRIDE will replace. Only PATCH is currently supported.'
    )

    @validator("write_semantics")
    @classmethod
    def validate_write_semantics(cls, v: str) -> str:
        if v.upper() not in {"PATCH", "OVERRIDE"}:
            raise ValueError("write_semantics must be either PATCH or OVERRIDE")
        return v.upper()

@dataclass
class JsonIngestionReport(SourceReport):
    total = 0

@platform_name("JSON Ingestion")
@config_class(JsonIngestionConfig)
@support_status(SupportStatus.INCUBATING)
@capability(SourceCapability.SCHEMA_METADATA, "Extracts schema from raw JSON")
@capability(SourceCapability.DESCRIPTIONS, "Supports dataset/field descriptions")
@capability(SourceCapability.TAGS, "Supports dataset/field tags")
@capability(SourceCapability.OWNERSHIP, "Supports dataset ownership")
@capability(SourceCapability.LINEAGE_COARSE, "Supports upstream lineage if added")
class JsonIngestionSource(Source):
    def __init__(self, config: JsonIngestionConfig, ctx: PipelineContext):
        super().__init__(ctx)
        self.config: JsonIngestionConfig = config
        self.report = JsonIngestionReport()

        with open(config.path, "r") as f:
            self.raw_data = json.load(f)

    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext):
        config = JsonIngestionConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        data = self.raw_data.get("data", [])
        if not data:
            return

        flattened_fields = collect_schema_fields(data, sample_limit=100)
        schema_fields = []

        for field, value in flattened_fields.items():
            data_type = infer_type(value)
            field_desc = self.config.field_descriptions.get(field) if self.config.field_descriptions else None
            tags = self.config.field_tags.get(field) if self.config.field_tags else []

            schema_fields.append(
                SchemaFieldClass(
                    fieldPath=field,
                    type=data_type,
                    nativeDataType=type(value).__name__,
                    description=field_desc,
                    globalTags=GlobalTagsClass(
                        tags=[TagAssociationClass(tag) for tag in tags]
                    ) if tags else None
                )
            )

        dataset_urn = f"urn:li:dataset:(urn:li:dataPlatform:{self.config.platform},{self.config.dataset_name},PROD)"

        def schema_hash(fields: List[SchemaFieldClass]) -> str:
            summary = "|".join(f"{f.fieldPath}:{f.nativeDataType}" for f in fields)
            return hashlib.md5(summary.encode("utf-8")).hexdigest()

        yield MetadataWorkUnit(
            id=f"{self.config.dataset_name}-schema",
            mcp=MetadataChangeProposalWrapper(
                entityUrn=dataset_urn,
                aspect=SchemaMetadataClass(
                    schemaName="default",
                    platform=f"urn:li:dataPlatform:{self.config.platform}",
                    version=0,
                    fields=schema_fields,
                    hash=schema_hash(schema_fields),
                    platformSchema=OtherSchemaClass(rawSchema="{}")
                ),
                aspectName="schemaMetadata",
                entityType="dataset"
            )
        )

        if self.config.description:
            yield MetadataWorkUnit(
                id=f"{self.config.dataset_name}-description",
                mcp=MetadataChangeProposalWrapper(
                    entityUrn=dataset_urn,
                    aspect=EditableDatasetPropertiesClass(description=self.config.description),
                    aspectName="editableDatasetProperties",
                    entityType="dataset"
                )
            )

        if self.config.tags:
            yield MetadataWorkUnit(
                id=f"{self.config.dataset_name}-tags",
                mcp=MetadataChangeProposalWrapper(
                    entityUrn=dataset_urn,
                    aspect=GlobalTagsClass(
                        tags=[TagAssociationClass(tag) for tag in self.config.tags]
                    ),
                    aspectName="globalTags",
                    entityType="dataset"
                )
            )

        if self.config.owners:
            yield MetadataWorkUnit(
                id=f"{self.config.dataset_name}-owners",
                mcp=MetadataChangeProposalWrapper(
                    entityUrn=dataset_urn,
                    aspect=OwnershipClass(
                        owners=[
                            OwnerClass(owner=owner, type="DATAOWNER")
                            for owner in self.config.owners
                        ]
                    ),
                    aspectName="ownership",
                    entityType="dataset"
                )
            )

        self.report.total += 1

    def get_report(self) -> JsonIngestionReport:
        return self.report