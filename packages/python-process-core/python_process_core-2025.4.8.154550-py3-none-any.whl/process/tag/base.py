from abc import ABC, abstractmethod
from typing import Generic, TypeVar, ClassVar, Optional, get_origin, get_args
from datetime import datetime
import logging

from asyncua.ua.uatypes import (
    DataValue, 
    Variant, 
    VariantType, 
    StatusCode, 
    DateTime,
    Int32, 
    UInt16,
)


logger = logging.getLogger(__name__)

_T = TypeVar("_T")

class AbstractTag(Generic[_T], DataValue, ABC):
    """
    This class is generic and can be used to create tags of any type.
    It is expected that subclasses will define the type of the tag in the CLS_TYPE class variable.
    The CLS_TYPE class variable is set automatically based on the type of the tag.
    This base class should be tightly integrated with the asyncua library to allow for simple and efficient
    communication with OPC UA servers.
    """
    CLS_TYPE: ClassVar[type]

    def __init_subclass__(cls, **kwargs) -> None:
        if hasattr(cls, 'CLS_TYPE'):
            logger.debug(f"Class {cls.__name__} already has CLS_TYPE set to {cls.CLS_TYPE}, will not inspect base args.")
        elif (orig_bases := getattr(cls, "__orig_bases__", None)) is not None:
            for origin in orig_bases:
                if (origin := get_origin(origin)) is not None and issubclass(origin, AbstractTag):
                    cls.CLS_TYPE = get_args(origin)[0]
                    break
        return super().__init_subclass__(**kwargs)

    @property
    @abstractmethod
    def value(self) -> _T:
        """
        The value associated with the tag.
        """
        pass

    @property
    @abstractmethod
    def status_code(self) -> StatusCode:
        """
        The status code associated with the tag.
        """
        pass

    @property
    @abstractmethod
    def source_timestamp(self) -> datetime:
        """
        The source timestamp associated with the tag.
        """
        pass

    @property
    @abstractmethod
    def source_picoseconds(self) -> int:
        """
        The source picoseconds associated with the tag.
        """
        pass

    def to_variant(
        self, 
        variant_type: Optional[VariantType] = None, 
        dimensions: Optional[list[int | Int32]] = None,
        is_array: Optional[bool] = None
    ) -> Variant:
        """
        Converts the tag to a Variant object.
        This method is expected to be implemented by subclasses.
        """
        if dimensions is not None:
            for idx, d in enumerate(dimensions):
                if not isinstance(d, Int32):
                    dimensions[idx] = Int32(d)
        return Variant(Value=self.value, VariantType=variant_type, Dimensions=dimensions, is_array=is_array)  # type: ignore[reportGeneralTypeIssues]


    def to_datavalue(
        self, 
        variant: Optional[Variant] = None,

    ) -> DataValue:
        """
        Converts the tag to a DataValue object.
        This method is expected to be implemented by subclasses.
        """
        variant = variant or self.to_variant()
        source_timestamp = DateTime.replace(self.source_timestamp)  # type: ignore[reportGeneralTypeIssues]
        return DataValue(Value=variant, StatusCode_=self.status_code, SourceTimestamp=source_timestamp, SourcePicoseconds=UInt16(self.source_picoseconds))