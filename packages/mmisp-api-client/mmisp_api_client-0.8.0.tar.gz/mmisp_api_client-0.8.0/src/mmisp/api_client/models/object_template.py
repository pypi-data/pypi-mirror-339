from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.object_templates_requirements import ObjectTemplatesRequirements


T = TypeVar("T", bound="ObjectTemplate")


@_attrs_define
class ObjectTemplate:
    """
    Attributes:
        id (int):
        user_id (int):
        org_id (int):
        uuid (UUID):
        name (str):
        meta_category (str):
        description (str):
        version (str):
        requirements (ObjectTemplatesRequirements):
        fixed (bool):
        active (bool):
    """

    id: int
    user_id: int
    org_id: int
    uuid: UUID
    name: str
    meta_category: str
    description: str
    version: str
    requirements: "ObjectTemplatesRequirements"
    fixed: bool
    active: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        org_id = self.org_id

        uuid = str(self.uuid)

        name = self.name

        meta_category = self.meta_category

        description = self.description

        version = self.version

        requirements = self.requirements.to_dict()

        fixed = self.fixed

        active = self.active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "org_id": org_id,
                "uuid": uuid,
                "name": name,
                "meta-category": meta_category,
                "description": description,
                "version": version,
                "requirements": requirements,
                "fixed": fixed,
                "active": active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_templates_requirements import ObjectTemplatesRequirements

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("user_id")

        org_id = d.pop("org_id")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        meta_category = d.pop("meta-category")

        description = d.pop("description")

        version = d.pop("version")

        requirements = ObjectTemplatesRequirements.from_dict(d.pop("requirements"))

        fixed = d.pop("fixed")

        active = d.pop("active")

        object_template = cls(
            id=id,
            user_id=user_id,
            org_id=org_id,
            uuid=uuid,
            name=name,
            meta_category=meta_category,
            description=description,
            version=version,
            requirements=requirements,
            fixed=fixed,
            active=active,
        )

        object_template.additional_properties = d
        return object_template

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
