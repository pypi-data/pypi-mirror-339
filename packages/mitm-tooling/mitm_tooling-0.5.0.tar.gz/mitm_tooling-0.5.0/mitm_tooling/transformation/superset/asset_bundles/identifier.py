from uuid import UUID

import pydantic

from mitm_tooling.transformation.superset.definitions import DatasetIdentifierMap, \
    DatabaseIdentifier, MitMDatasetIdentifier, BaseSupersetDefinition, DashboardIdentifier

VizDashboardIdentifierMap = dict[str, DashboardIdentifier]
VizCollectionIdentifierMap = dict[str, VizDashboardIdentifierMap]


class DatasourceIdentifierBundle(BaseSupersetDefinition):
    database: DatabaseIdentifier | None = None
    ds_id_map: DatasetIdentifierMap = pydantic.Field(default_factory=dict)

    @property
    def database_uuid(self) -> UUID | None:
        if self.database is not None:
            return self.database.uuid


class MitMDatasetIdentifierBundle(DatasourceIdentifierBundle):
    mitm_dataset: MitMDatasetIdentifier | None = None
    viz_id_map: VizCollectionIdentifierMap = pydantic.Field(default_factory=dict)

    @property
    def mitm_dataset_uuid(self) -> UUID | None:
        if self.mitm_dataset is not None:
            return self.mitm_dataset.uuid
