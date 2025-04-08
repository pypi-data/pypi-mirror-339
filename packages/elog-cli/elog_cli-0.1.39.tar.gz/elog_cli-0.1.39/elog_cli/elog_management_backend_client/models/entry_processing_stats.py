from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryProcessingStats")


@_attrs_define
class EntryProcessingStats:
    """Is the result of the processing of entries.

    Attributes:
        processed_entries (Union[Unset, int]): The number of processed entries.
        failed_entries (Union[Unset, int]): The number of failed entries.
        completed (Union[Unset, bool]): Indicate when the schedule is completed.
        error_message (Union[Unset, str]): The error message in case there will be one
    """

    processed_entries: Union[Unset, int] = UNSET
    failed_entries: Union[Unset, int] = UNSET
    completed: Union[Unset, bool] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        processed_entries = self.processed_entries

        failed_entries = self.failed_entries

        completed = self.completed

        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if processed_entries is not UNSET:
            field_dict["processedEntries"] = processed_entries
        if failed_entries is not UNSET:
            field_dict["failedEntries"] = failed_entries
        if completed is not UNSET:
            field_dict["completed"] = completed
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        processed_entries = d.pop("processedEntries", UNSET)

        failed_entries = d.pop("failedEntries", UNSET)

        completed = d.pop("completed", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        entry_processing_stats = cls(
            processed_entries=processed_entries,
            failed_entries=failed_entries,
            completed=completed,
            error_message=error_message,
        )

        entry_processing_stats.additional_properties = d
        return entry_processing_stats

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
