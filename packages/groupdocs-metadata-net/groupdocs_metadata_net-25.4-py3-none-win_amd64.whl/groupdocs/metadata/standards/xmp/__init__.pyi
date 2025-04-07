from typing import List, Optional, Dict, Iterable, Any, overload
import io
import collections.abc
from collections.abc import Sequence
from datetime import datetime
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
from uuid import UUID
import groupdocs.metadata
import groupdocs.metadata.common
import groupdocs.metadata.exceptions
import groupdocs.metadata.export
import groupdocs.metadata.formats
import groupdocs.metadata.formats.archive
import groupdocs.metadata.formats.audio
import groupdocs.metadata.formats.audio.ogg
import groupdocs.metadata.formats.businesscard
import groupdocs.metadata.formats.cad
import groupdocs.metadata.formats.document
import groupdocs.metadata.formats.ebook
import groupdocs.metadata.formats.ebook.fb2
import groupdocs.metadata.formats.ebook.mobi
import groupdocs.metadata.formats.email
import groupdocs.metadata.formats.fb2
import groupdocs.metadata.formats.font
import groupdocs.metadata.formats.gis
import groupdocs.metadata.formats.image
import groupdocs.metadata.formats.image.dng
import groupdocs.metadata.formats.mpeg
import groupdocs.metadata.formats.peer2peer
import groupdocs.metadata.formats.raw
import groupdocs.metadata.formats.raw.cr2
import groupdocs.metadata.formats.raw.tag
import groupdocs.metadata.formats.riff
import groupdocs.metadata.formats.threed
import groupdocs.metadata.formats.threed.dae
import groupdocs.metadata.formats.threed.fbx
import groupdocs.metadata.formats.threed.stl
import groupdocs.metadata.formats.threed.threeds
import groupdocs.metadata.formats.video
import groupdocs.metadata.importing
import groupdocs.metadata.logging
import groupdocs.metadata.options
import groupdocs.metadata.search
import groupdocs.metadata.standards
import groupdocs.metadata.standards.dublincore
import groupdocs.metadata.standards.exif
import groupdocs.metadata.standards.exif.makernote
import groupdocs.metadata.standards.iptc
import groupdocs.metadata.standards.pkcs
import groupdocs.metadata.standards.signing
import groupdocs.metadata.standards.xmp
import groupdocs.metadata.standards.xmp.schemes
import groupdocs.metadata.tagging

class IXmp:
    '''Defines base operations intended to work with XMP metadata.'''
    
    @property
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    

class IXmpType:
    '''Base interface for XMP type.'''
    
    def get_xmp_representation(self) -> str:
        '''Converts the XMP value to the XML representation.
        
        :returns: A :py:class:`str` representation of the XMP value.'''
        raise NotImplementedError()
    

class XmpArray(XmpValueBase):
    '''Represents base abstraction for XMP array.'''
    
    @overload
    def __init__(self, array_type : groupdocs.metadata.standards.xmp.XmpArrayType, items : List[groupdocs.metadata.standards.xmp.XmpValueBase]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray` class.
        
        :param array_type: Array type.
        :param items: Array items.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, array_type : groupdocs.metadata.standards.xmp.XmpArrayType, items : List[groupdocs.metadata.standards.xmp.XmpComplexType]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray` class.
        
        :param array_type: Array type.
        :param items: Array items.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[str], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a string array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[int], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form an integer array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[datetime], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a date array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[float], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a double array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts XMP value to the xml representation.
        
        :returns: Returns :py:class:`str` representation of XMP value.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def array_type(self) -> groupdocs.metadata.standards.xmp.XmpArrayType:
        '''Gets the type of the XMP array.'''
        raise NotImplementedError()
    

class XmpBoolean(XmpValueBase):
    '''Represents XMP Boolean basic type.'''
    
    @overload
    def __init__(self, value : bool) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpBoolean` class based on boolean value.
        
        :param value: :py:class:`bool` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpBoolean` class with default value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpBoolean` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> bool:
        '''Gets the value.'''
        raise NotImplementedError()
    

class XmpColorantBase(XmpComplexType):
    '''A structure containing the characteristics of a colorant (swatch) used in a document.'''
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> groupdocs.metadata.standards.xmp.XmpColorantColorMode:
        '''Gets the colour space in which the colour is defined. One of: CMYK, RGB, LAB.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> Optional[groupdocs.metadata.standards.xmp.XmpColorType]:
        '''Gets the type of color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : Optional[groupdocs.metadata.standards.xmp.XmpColorType]) -> None:
        '''Sets the type of color.'''
        raise NotImplementedError()
    

class XmpColorantCmyk(XmpColorantBase):
    '''Represents the CMYK Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantCmyk` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, cyan : float, magenta : float, yellow : float, black : float) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantCmyk` class.
        
        :param cyan: Cyan component.
        :param magenta: Magenta component.
        :param yellow: Yellow component.
        :param black: Black component.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> groupdocs.metadata.standards.xmp.XmpColorantColorMode:
        '''Gets the colour space in which the colour is defined. One of: CMYK, RGB, LAB.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> Optional[groupdocs.metadata.standards.xmp.XmpColorType]:
        '''Gets the type of color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : Optional[groupdocs.metadata.standards.xmp.XmpColorType]) -> None:
        '''Sets the type of color.'''
        raise NotImplementedError()
    
    @property
    def black(self) -> Optional[float]:
        '''Gets the black component.'''
        raise NotImplementedError()
    
    @black.setter
    def black(self, value : Optional[float]) -> None:
        '''Sets the black component.'''
        raise NotImplementedError()
    
    @property
    def cyan(self) -> Optional[float]:
        '''Gets the cyan component.'''
        raise NotImplementedError()
    
    @cyan.setter
    def cyan(self, value : Optional[float]) -> None:
        '''Sets the cyan component.'''
        raise NotImplementedError()
    
    @property
    def magenta(self) -> Optional[float]:
        '''Gets the magenta component.'''
        raise NotImplementedError()
    
    @magenta.setter
    def magenta(self, value : Optional[float]) -> None:
        '''Sets the magenta component.'''
        raise NotImplementedError()
    
    @property
    def yellow(self) -> Optional[float]:
        '''Gets the yellow component.'''
        raise NotImplementedError()
    
    @yellow.setter
    def yellow(self, value : Optional[float]) -> None:
        '''Sets the yellow component.'''
        raise NotImplementedError()
    
    @property
    def COLOR_VALUE_MAX(self) -> float:
        '''Color max value in CMYK colorant.'''
        raise NotImplementedError()

    @property
    def COLOR_VALUE_MIN(self) -> float:
        '''Color min value in CMYK colorant.'''
        raise NotImplementedError()


class XmpColorantLab(XmpColorantBase):
    '''Represents the LAB Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantLab` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, a : sbyte, b : sbyte, l : float) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantLab` class.
        
        :param a: A component.
        :param b: B component.
        :param l: L component.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> groupdocs.metadata.standards.xmp.XmpColorantColorMode:
        '''Gets the colour space in which the colour is defined. One of: CMYK, RGB, LAB.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> Optional[groupdocs.metadata.standards.xmp.XmpColorType]:
        '''Gets the type of color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : Optional[groupdocs.metadata.standards.xmp.XmpColorType]) -> None:
        '''Sets the type of color.'''
        raise NotImplementedError()
    
    @property
    def a(self) -> Optional[sbyte]:
        '''Gets the A component.'''
        raise NotImplementedError()
    
    @a.setter
    def a(self, value : Optional[sbyte]) -> None:
        '''Sets the A component.'''
        raise NotImplementedError()
    
    @property
    def b(self) -> Optional[sbyte]:
        '''Gets the B component.'''
        raise NotImplementedError()
    
    @b.setter
    def b(self, value : Optional[sbyte]) -> None:
        '''Sets the B component.'''
        raise NotImplementedError()
    
    @property
    def l(self) -> Optional[float]:
        '''Gets the L component.'''
        raise NotImplementedError()
    
    @l.setter
    def l(self, value : Optional[float]) -> None:
        '''Sets the L component.'''
        raise NotImplementedError()
    
    @property
    def MIN_L(self) -> float:
        '''Component L min value.'''
        raise NotImplementedError()

    @property
    def MAX_L(self) -> float:
        '''Component L max value.'''
        raise NotImplementedError()


class XmpColorantRgb(XmpColorantBase):
    '''Represents the RGB Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantRgb` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, red : int, green : int, blue : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpColorantRgb` class.
        
        :param red: Red component.
        :param green: Green component.
        :param blue: Blue component.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> groupdocs.metadata.standards.xmp.XmpColorantColorMode:
        '''Gets the colour space in which the colour is defined. One of: CMYK, RGB, LAB.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> Optional[groupdocs.metadata.standards.xmp.XmpColorType]:
        '''Gets the type of color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : Optional[groupdocs.metadata.standards.xmp.XmpColorType]) -> None:
        '''Sets the type of color.'''
        raise NotImplementedError()
    
    @property
    def red(self) -> Optional[int]:
        '''Gets the red component.'''
        raise NotImplementedError()
    
    @red.setter
    def red(self, value : Optional[int]) -> None:
        '''Sets the red component.'''
        raise NotImplementedError()
    
    @property
    def green(self) -> Optional[int]:
        '''Gets the green value.'''
        raise NotImplementedError()
    
    @green.setter
    def green(self, value : Optional[int]) -> None:
        '''Sets the green value.'''
        raise NotImplementedError()
    
    @property
    def blue(self) -> Optional[int]:
        '''Gets the blue component.'''
        raise NotImplementedError()
    
    @blue.setter
    def blue(self, value : Optional[int]) -> None:
        '''Sets the blue component.'''
        raise NotImplementedError()
    

class XmpComplexType(XmpMetadataContainer):
    '''Represents base abstraction for XMP Complex value type.'''
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    

class XmpComplexTypeValue(XmpValueBase):
    '''Represents an XMP value containing a complex type instance.'''
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    

class XmpDate(XmpValueBase):
    '''Represents Date in XMP packet.'''
    
    @overload
    def __init__(self, date_time : datetime) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpDate` class.
        
        :param date_time: :py:class:`datetime` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, date_string : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpDate` class.
        
        :param date_string: Date in string representation.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> datetime:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> str:
        '''Gets format string for current value.'''
        raise NotImplementedError()
    
    @property
    def ISO_8601_FORMAT(self) -> str:
        '''The ISO 8601 (roundtrip) format string.'''
        raise NotImplementedError()


class XmpDimensions(XmpComplexType):
    '''Containing dimensions for a drawn object.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpDimensions` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, width : float, height : float) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpDimensions` class.
        
        :param width: The width.
        :param height: The height.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> Optional[float]:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : Optional[float]) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> Optional[float]:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : Optional[float]) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def units(self) -> str:
        '''Gets the units.'''
        raise NotImplementedError()
    
    @units.setter
    def units(self, value : str) -> None:
        '''Sets the units.'''
        raise NotImplementedError()
    

class XmpElementBase(groupdocs.metadata.common.CustomPackage):
    '''Represents base XMP element that contains attributes.'''
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_attribute(self, attribute : str, value : str) -> None:
        '''Adds the attribute.
        
        :param attribute: Attribute key.
        :param value: Attribute value.'''
        raise NotImplementedError()
    
    def clear_attributes(self) -> None:
        '''Removes all attributes.'''
        raise NotImplementedError()
    
    def contains_attribute(self, attribute : str) -> bool:
        '''Determines whether the element contains a specific attribute.
        
        :param attribute: Attribute name.
        :returns: true if attribute is exist; otherwise false.'''
        raise NotImplementedError()
    
    def get_attribute(self, attribute : str) -> str:
        '''Gets the attribute.
        
        :param attribute: The attribute.
        :returns: The attribute value.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    

class XmpFont(XmpComplexType):
    '''A structure containing the characteristics of a font used in a document.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpFont` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, font_family : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpFont` class.
        
        :param font_family: Font family.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def child_font_files(self) -> List[str]:
        '''Gets the list of file names for the fonts that make up a composite font.'''
        raise NotImplementedError()
    
    @child_font_files.setter
    def child_font_files(self, value : List[str]) -> None:
        '''Sets the list of file names for the fonts that make up a composite font.'''
        raise NotImplementedError()
    
    @property
    def is_composite(self) -> Optional[bool]:
        '''Gets a value indicating whether whether the font is composite.'''
        raise NotImplementedError()
    
    @is_composite.setter
    def is_composite(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether whether the font is composite.'''
        raise NotImplementedError()
    
    @property
    def font_face(self) -> str:
        '''Gets the font face name.'''
        raise NotImplementedError()
    
    @font_face.setter
    def font_face(self, value : str) -> None:
        '''Sets the font face name.'''
        raise NotImplementedError()
    
    @property
    def font_family(self) -> str:
        '''Gets the font family name.'''
        raise NotImplementedError()
    
    @font_family.setter
    def font_family(self, value : str) -> None:
        '''Sets the font family name.'''
        raise NotImplementedError()
    
    @property
    def font_file_name(self) -> str:
        '''Gets the font file name (not a complete path).'''
        raise NotImplementedError()
    
    @font_file_name.setter
    def font_file_name(self, value : str) -> None:
        '''Sets the font file name (not a complete path).'''
        raise NotImplementedError()
    
    @property
    def font_name(self) -> str:
        '''Gets the PostScript name of the font.'''
        raise NotImplementedError()
    
    @font_name.setter
    def font_name(self, value : str) -> None:
        '''Sets the PostScript name of the font.'''
        raise NotImplementedError()
    
    @property
    def font_type(self) -> str:
        '''Gets the font type.'''
        raise NotImplementedError()
    
    @font_type.setter
    def font_type(self, value : str) -> None:
        '''Sets the font type.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''Gets the font version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : str) -> None:
        '''Sets the font version.'''
        raise NotImplementedError()
    

class XmpGuid(XmpValueBase):
    '''Represents XMP global unique identifier.'''
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpGuid` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : UUID) -> None:
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> UUID:
        '''Gets the value.'''
        raise NotImplementedError()
    

class XmpHeaderPI(IXmpType):
    '''Represents XMP header processing instruction.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpHeaderPI` class.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts XMP value to the xml representation.
        
        :returns: Returns :py:class:`str` representation of XMP value.'''
        raise NotImplementedError()
    
    @property
    def guid(self) -> str:
        '''Represents Header GUID.'''
        raise NotImplementedError()
    

class XmpInteger(XmpValueBase):
    '''Represents XMP Integer basic type.'''
    
    @overload
    def __init__(self, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpInteger` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpInteger` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpInteger` class.
        
        :param value: String value contained integer.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets the value.'''
        raise NotImplementedError()
    

class XmpJob(XmpComplexType):
    '''Represents Job.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpJob` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> str:
        '''Gets unique id for the job. This field is a reference into some external job management system.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : str) -> None:
        '''Sets unique id for the job. This field is a reference into some external job management system.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets informal name of the job. This name is for user display and informal systems.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets informal name of the job. This name is for user display and informal systems.'''
        raise NotImplementedError()
    
    @property
    def url(self) -> str:
        '''Gets a file URL referencing an external job management file.'''
        raise NotImplementedError()
    
    @url.setter
    def url(self, value : str) -> None:
        '''Sets a file URL referencing an external job management file.'''
        raise NotImplementedError()
    

class XmpLangAlt(XmpArray):
    '''Represents XMP Language Alternative.'''
    
    def __init__(self, default_value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpLangAlt` class.
        
        :param default_value: The default value.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[str], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a string array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[int], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form an integer array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[datetime], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a date array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def from_address(array : List[float], type : groupdocs.metadata.standards.xmp.XmpArrayType) -> groupdocs.metadata.standards.xmp.XmpArray:
        '''Creates an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` instance form a double array.
        
        :param array: The array to create an :py:class:`groupdocs.metadata.standards.xmp.XmpArray` from.
        :param type: The type of the :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.
        :returns: An :py:class:`groupdocs.metadata.standards.xmp.XmpArray` containing all the elements from the original array.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts XMP value to the xml representation.
        
        :returns: Returns :py:class:`str` representation of XMP value.'''
        raise NotImplementedError()
    
    def contains(self, language : str) -> bool:
        '''Determines whether the :py:class:`groupdocs.metadata.standards.xmp.XmpLangAlt` contains the specified language.
        
        :param language: The language to locate in the :py:class:`groupdocs.metadata.standards.xmp.XmpLangAlt`.
        :returns: True if the :py:class:`groupdocs.metadata.standards.xmp.XmpLangAlt` contains an element with the specified language; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def array_type(self) -> groupdocs.metadata.standards.xmp.XmpArrayType:
        '''Gets the type of the XMP array.'''
        raise NotImplementedError()
    
    @property
    def languages(self) -> List[str]:
        '''Gets an array of all languages registered in the instance of :py:class:`groupdocs.metadata.standards.xmp.XmpLangAlt`.'''
        raise NotImplementedError()
    

class XmpMeta(XmpElementBase):
    '''Represents xmpmeta. Optional.
    The purpose of this element is to identify XMP metadata within general XML text that might contain other non-XMP uses of RDF.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpElementBase` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_attribute(self, attribute : str, value : str) -> None:
        '''Adds an attribute.
        
        :param attribute: The attribute.
        :param value: The value.'''
        raise NotImplementedError()
    
    def clear_attributes(self) -> None:
        '''Removes all attributes.'''
        raise NotImplementedError()
    
    def contains_attribute(self, attribute : str) -> bool:
        '''Determines whether the element contains a specific attribute.
        
        :param attribute: Attribute name.
        :returns: true if attribute is exist; otherwise false.'''
        raise NotImplementedError()
    
    def get_attribute(self, attribute : str) -> str:
        '''Gets the attribute.
        
        :param attribute: The attribute.
        :returns: The attribute value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts XMP value to the xml representation.
        
        :returns: Returns :py:class:`str` representation of XMP value.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def adobe_xmp_toolkit(self) -> str:
        '''Gets Adobe XMP toolkit version.'''
        raise NotImplementedError()
    

class XmpMetadataContainer(groupdocs.metadata.common.CustomPackage):
    '''Represents a container for XMP metadata properties.'''
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts the XMP value to the XML representation.
        
        :returns: A :py:class:`str` representation of the XMP value.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    

class XmpNamespaces:
    '''Contains namespaces used in :py:class:`groupdocs.metadata.standards.xmp.XmpPackage` and :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType`.'''
    
    @property
    def XML(self) -> str:
        '''Xml namespace.'''
        raise NotImplementedError()

    @property
    def RDF(self) -> str:
        '''Resource definition framework namespace.'''
        raise NotImplementedError()

    @property
    def BASIC_JOB(self) -> str:
        '''Basic Job Ticket namespace.'''
        raise NotImplementedError()

    @property
    def CAMERA_RAW(self) -> str:
        '''Camera Raw namespace.'''
        raise NotImplementedError()

    @property
    def DUBLIN_CORE(self) -> str:
        '''Dublin Core namespace.'''
        raise NotImplementedError()

    @property
    def IPTC_4_XMP_IIM(self) -> str:
        '''IPTC IIM namespace.'''
        raise NotImplementedError()

    @property
    def IPTC_4_XMP_CORE(self) -> str:
        '''IPTC Core namespace.'''
        raise NotImplementedError()

    @property
    def IPTC_4_XMP_EXT(self) -> str:
        '''IPTC Extension namespace.'''
        raise NotImplementedError()

    @property
    def XMP_BASIC(self) -> str:
        '''XMP Basic namespace.'''
        raise NotImplementedError()

    @property
    def XMP_RIGHTS(self) -> str:
        '''XMP Rights Management namespace.'''
        raise NotImplementedError()

    @property
    def XMP_MM(self) -> str:
        '''XMP digital asset management namespace.'''
        raise NotImplementedError()

    @property
    def XMP_DM(self) -> str:
        '''XMP Dynamic Media namespace.'''
        raise NotImplementedError()

    @property
    def PDF(self) -> str:
        '''Adobe PDF namespace.'''
        raise NotImplementedError()

    @property
    def PHOTOSHOP(self) -> str:
        '''Adobe Photoshop namespace.'''
        raise NotImplementedError()

    @property
    def PAGED_TEXT(self) -> str:
        '''XMP Paged-Text namespace.'''
        raise NotImplementedError()

    @property
    def XMP_GRAPHICS(self) -> str:
        '''XMP graphics namespace.'''
        raise NotImplementedError()

    @property
    def XMP_GRAPHICS_THUMBNAIL(self) -> str:
        '''XMP graphics namespace.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_FONT(self) -> str:
        '''XMP Font type.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_DIMENSIONS(self) -> str:
        '''XMP Dimensions type.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_RESOURCE_REF(self) -> str:
        '''XMP ResourceRef URI.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_RESOURCE_EVENT(self) -> str:
        '''XMP ResourceEvent URI.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_VERSION(self) -> str:
        '''XMP Version.'''
        raise NotImplementedError()

    @property
    def XMP_TYPE_JOB(self) -> str:
        '''XMP Job Ticket.'''
        raise NotImplementedError()


class XmpPackage(XmpMetadataContainer):
    '''Represents base abstraction for XMP package.'''
    
    def __init__(self, prefix : str, namespace_uri : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpPackage` class.
        
        :param prefix: XMP prefix, for example dc:title.
        :param namespace_uri: Namespace uri.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Sets string property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : int) -> None:
        '''Sets integer property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : bool) -> None:
        '''Sets boolean property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : datetime) -> None:
        '''Sets :py:class:`datetime` property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : float) -> None:
        '''Sets double property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpValueBase) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpValueBase` .
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpComplexType) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` .
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpArray) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpArray` .
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts the XMP value to the XML representation.
        
        :returns: A :py:class:`str` representation of the XMP value.'''
        raise NotImplementedError()
    
    def remove(self, name : str) -> bool:
        '''Removes the property with the specified name.
        
        :param name: XMP metadata property name.
        :returns: True if the specified metadata property is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all XMP properties.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the xmlns prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the namespace URI.'''
        raise NotImplementedError()
    
    @property
    def xml_namespace(self) -> str:
        '''Gets the XML namespace.'''
        raise NotImplementedError()
    

class XmpPacketWrapper(groupdocs.metadata.common.MetadataPackage):
    '''Contains serialized XMP package including header and trailer.
    A wrapper consisting of a pair of XML processing instructions (PIs) may be placed around the rdf:RDF element.'''
    
    @overload
    def __init__(self, header : groupdocs.metadata.standards.xmp.XmpHeaderPI, trailer : groupdocs.metadata.standards.xmp.XmpTrailerPI, xmp_meta : groupdocs.metadata.standards.xmp.XmpMeta) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpPacketWrapper` class.
        
        :param header: XMP header processing instruction.
        :param trailer: XMP trailer processing instruction.
        :param xmp_meta: Instance of :py:class:`groupdocs.metadata.standards.xmp.XmpMeta`.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpPacketWrapper` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_package(self, package : groupdocs.metadata.standards.xmp.XmpPackage) -> None:
        '''Adds the package.
        
        :param package: The package.'''
        raise NotImplementedError()
    
    def get_package(self, namespace_uri : str) -> groupdocs.metadata.standards.xmp.XmpPackage:
        '''Gets package by namespace uri.
        
        :param namespace_uri: Package schema uri.
        :returns: Appropriate :py:class:`groupdocs.metadata.standards.xmp.XmpPackage` if package found by ``namespaceUri``; otherwise null.'''
        raise NotImplementedError()
    
    def contains_package(self, namespace_uri : str) -> bool:
        '''Determines whether package is exist in XMP wrapper.
        
        :param namespace_uri: Package namespace URI.
        :returns: ``true`` if package found by ``namespaceUri``; otherwise ``false``.'''
        raise NotImplementedError()
    
    def remove_package(self, package : groupdocs.metadata.standards.xmp.XmpPackage) -> None:
        '''Removes the specified package.
        
        :param package: The package.'''
        raise NotImplementedError()
    
    def clear_packages(self) -> None:
        '''Removes all :py:class:`groupdocs.metadata.standards.xmp.XmpPackage` inside XMP.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def header_pi(self) -> groupdocs.metadata.standards.xmp.XmpHeaderPI:
        '''Gets the header processing instruction.'''
        raise NotImplementedError()
    
    @header_pi.setter
    def header_pi(self, value : groupdocs.metadata.standards.xmp.XmpHeaderPI) -> None:
        '''Sets the header processing instruction.'''
        raise NotImplementedError()
    
    @property
    def meta(self) -> groupdocs.metadata.standards.xmp.XmpMeta:
        '''Gets the XMP meta.'''
        raise NotImplementedError()
    
    @meta.setter
    def meta(self, value : groupdocs.metadata.standards.xmp.XmpMeta) -> None:
        '''Sets the XMP meta.'''
        raise NotImplementedError()
    
    @property
    def trailer_pi(self) -> groupdocs.metadata.standards.xmp.XmpTrailerPI:
        '''Gets the trailer processing instruction.'''
        raise NotImplementedError()
    
    @trailer_pi.setter
    def trailer_pi(self, value : groupdocs.metadata.standards.xmp.XmpTrailerPI) -> None:
        '''Sets the trailer processing instruction.'''
        raise NotImplementedError()
    
    @property
    def packages(self) -> List[groupdocs.metadata.standards.xmp.XmpPackage]:
        '''Gets array of :py:class:`groupdocs.metadata.standards.xmp.XmpPackage` inside XMP.'''
        raise NotImplementedError()
    
    @property
    def package_count(self) -> int:
        '''Gets the number of packages inside the XMP structure.'''
        raise NotImplementedError()
    
    @property
    def schemes(self) -> groupdocs.metadata.standards.xmp.XmpSchemes:
        '''Provides access to known XMP schemas.'''
        raise NotImplementedError()
    

class XmpRational(XmpValueBase):
    '''Represents XMP XmpRational.'''
    
    @overload
    def __init__(self, numerator : int, denominator : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpRational` class.
        
        :param numerator: The numerator.
        :param denominator: The denominator.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpBoolean` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def numerator(self) -> int:
        '''Gets numerator.'''
        raise NotImplementedError()
    
    @property
    def denominator(self) -> int:
        '''Gets denominator'''
        raise NotImplementedError()
    
    @property
    def double_value(self) -> float:
        '''Gets value of rational type presented in double format.'''
        raise NotImplementedError()
    

class XmpReal(XmpValueBase):
    '''Represents XMP Real.'''
    
    @overload
    def __init__(self, value : float) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpReal` class.
        
        :param value: Double value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpReal` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> float:
        '''Gets the value.'''
        raise NotImplementedError()
    

class XmpRenditionClass(XmpText):
    '''Represents XMP RenditionClass.'''
    
    def __init__(self, tokens : List[str]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpRenditionClass` class.
        
        :param tokens: The token.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @property
    def DEFAULT(self) -> str:
        '''The master resource; no additional tokens allowed.'''
        raise NotImplementedError()

    @property
    def DRAFT(self) -> str:
        '''A review rendition.'''
        raise NotImplementedError()

    @property
    def LOW_RES(self) -> str:
        '''A low-resolution, full-size stand-in.'''
        raise NotImplementedError()

    @property
    def PROOF(self) -> str:
        '''A review proof.'''
        raise NotImplementedError()

    @property
    def SCREEN(self) -> str:
        '''Screen resolution or Web rendition.'''
        raise NotImplementedError()

    @property
    def THUMBNAIL(self) -> str:
        '''A simplified or reduced preview. Additional tokens can provide characteristics. The recommended order is thumbnail:format:size:colorspace.'''
        raise NotImplementedError()


class XmpResourceEvent(XmpComplexType):
    '''Represents a high-level event that occurred in the processing of a resource.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpResourceEvent` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def action(self) -> str:
        '''Gets the action that occurred.'''
        raise NotImplementedError()
    
    @action.setter
    def action(self, value : str) -> None:
        '''Sets the action that occurred.'''
        raise NotImplementedError()
    
    @property
    def changed(self) -> str:
        '''Gets a semicolon-delimited list of the parts of the resource that were changed since the previous event history.'''
        raise NotImplementedError()
    
    @changed.setter
    def changed(self, value : str) -> None:
        '''Sets a semicolon-delimited list of the parts of the resource that were changed since the previous event history.'''
        raise NotImplementedError()
    
    @property
    def instance_id(self) -> str:
        '''Gets the value of the xmpMM:InstanceID property for the modified (output) resource.'''
        raise NotImplementedError()
    
    @instance_id.setter
    def instance_id(self, value : str) -> None:
        '''Sets the value of the xmpMM:InstanceID property for the modified (output) resource.'''
        raise NotImplementedError()
    
    @property
    def parameters(self) -> str:
        '''Gets the additional description of the action.'''
        raise NotImplementedError()
    
    @parameters.setter
    def parameters(self, value : str) -> None:
        '''Sets the additional description of the action.'''
        raise NotImplementedError()
    
    @property
    def software_agent(self) -> str:
        '''Gets the software agent that performed the action.'''
        raise NotImplementedError()
    
    @software_agent.setter
    def software_agent(self, value : str) -> None:
        '''Sets the software agent that performed the action.'''
        raise NotImplementedError()
    
    @property
    def when(self) -> Optional[datetime]:
        '''Gets the timestamp of when the action occurred.'''
        raise NotImplementedError()
    
    @when.setter
    def when(self, value : Optional[datetime]) -> None:
        '''Sets the timestamp of when the action occurred.'''
        raise NotImplementedError()
    

class XmpResourceRef(XmpComplexType):
    '''Represents a multiple part reference to a resource.
    
    Used to indicate prior versions, originals of renditions, originals for derived documents, and so on.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpResourceRef` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def alternate_paths(self) -> List[str]:
        '''Gets the referenced resource’s fallback file paths or URLs.'''
        raise NotImplementedError()
    
    @alternate_paths.setter
    def alternate_paths(self, value : List[str]) -> None:
        '''Sets the referenced resource’s fallback file paths or URLs.'''
        raise NotImplementedError()
    
    @property
    def document_id(self) -> str:
        '''Gets the value of the xmpMM:DocumentID property from the referenced resource.'''
        raise NotImplementedError()
    
    @document_id.setter
    def document_id(self, value : str) -> None:
        '''Sets the value of the xmpMM:DocumentID property from the referenced resource.'''
        raise NotImplementedError()
    
    @property
    def file_path(self) -> str:
        '''Gets the referenced resource’s file path or URL.'''
        raise NotImplementedError()
    
    @file_path.setter
    def file_path(self, value : str) -> None:
        '''Sets the referenced resource’s file path or URL.'''
        raise NotImplementedError()
    
    @property
    def instance_id(self) -> str:
        '''Gets the value of the xmpMM:InstanceID property from the referenced resource.'''
        raise NotImplementedError()
    
    @instance_id.setter
    def instance_id(self, value : str) -> None:
        '''Sets the value of the xmpMM:InstanceID property from the referenced resource.'''
        raise NotImplementedError()
    
    @property
    def last_modify_date(self) -> Optional[datetime]:
        '''Gets the value of stEvt:when for the last time the file was written.'''
        raise NotImplementedError()
    
    @last_modify_date.setter
    def last_modify_date(self, value : Optional[datetime]) -> None:
        '''Sets the value of stEvt:when for the last time the file was written.'''
        raise NotImplementedError()
    
    @property
    def manager(self) -> str:
        '''Gets the referenced resource’s xmpMM:Manager.'''
        raise NotImplementedError()
    
    @manager.setter
    def manager(self, value : str) -> None:
        '''Sets the referenced resource’s xmpMM:Manager.'''
        raise NotImplementedError()
    
    @property
    def manager_variant(self) -> str:
        '''Gets the referenced resource’s xmpMM:Manager.'''
        raise NotImplementedError()
    
    @manager_variant.setter
    def manager_variant(self, value : str) -> None:
        '''Sets the referenced resource’s xmpMM:Manager.'''
        raise NotImplementedError()
    
    @property
    def manage_to(self) -> str:
        '''Gets the referenced resource’s xmpMM:ManageTo.'''
        raise NotImplementedError()
    
    @manage_to.setter
    def manage_to(self, value : str) -> None:
        '''Sets the referenced resource’s xmpMM:ManageTo.'''
        raise NotImplementedError()
    
    @property
    def manage_ui(self) -> str:
        '''Gets the referenced resource’s xmpMM:ManageUI.'''
        raise NotImplementedError()
    
    @manage_ui.setter
    def manage_ui(self, value : str) -> None:
        '''Sets the referenced resource’s xmpMM:ManageUI.'''
        raise NotImplementedError()
    
    @property
    def part_mapping(self) -> str:
        '''Gets the name or URI of a mapping function used to map the fromPart to the toPart.'''
        raise NotImplementedError()
    
    @part_mapping.setter
    def part_mapping(self, value : str) -> None:
        '''Sets the name or URI of a mapping function used to map the fromPart to the toPart.'''
        raise NotImplementedError()
    
    @property
    def rendition_class(self) -> str:
        '''Gets the value of the xmpMM:RenditionClass property from the referenced resource.'''
        raise NotImplementedError()
    
    @rendition_class.setter
    def rendition_class(self, value : str) -> None:
        '''Sets the value of the xmpMM:RenditionClass property from the referenced resource.'''
        raise NotImplementedError()
    
    @property
    def rendition_params(self) -> str:
        '''Gets the value of the xmpMM:RenditionParams property from the referenced resource.'''
        raise NotImplementedError()
    
    @rendition_params.setter
    def rendition_params(self, value : str) -> None:
        '''Sets the value of the xmpMM:RenditionParams property from the referenced resource.'''
        raise NotImplementedError()
    
    @property
    def version_id(self) -> str:
        '''Gets the value of the xmpMM:RenditionParams property from the referenced resource.'''
        raise NotImplementedError()
    
    @version_id.setter
    def version_id(self, value : str) -> None:
        '''Sets the value of the xmpMM:RenditionParams property from the referenced resource.'''
        raise NotImplementedError()
    

class XmpSchemes:
    '''Provides access to known XMP schemes.'''
    
    @property
    def camera_raw(self) -> groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage:
        '''Gets the Camera Raw scheme.'''
        raise NotImplementedError()
    
    @camera_raw.setter
    def camera_raw(self, value : groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage) -> None:
        '''Sets the Camera Raw scheme.'''
        raise NotImplementedError()
    
    @property
    def dublin_core(self) -> groupdocs.metadata.standards.xmp.schemes.XmpDublinCorePackage:
        '''Gets the Dublin Core scheme.'''
        raise NotImplementedError()
    
    @dublin_core.setter
    def dublin_core(self, value : groupdocs.metadata.standards.xmp.schemes.XmpDublinCorePackage) -> None:
        '''Sets the Dublin Core scheme.'''
        raise NotImplementedError()
    
    @property
    def paged_text(self) -> groupdocs.metadata.standards.xmp.schemes.XmpPagedTextPackage:
        '''Gets the PagedText scheme.'''
        raise NotImplementedError()
    
    @paged_text.setter
    def paged_text(self, value : groupdocs.metadata.standards.xmp.schemes.XmpPagedTextPackage) -> None:
        '''Sets the PagedText scheme.'''
        raise NotImplementedError()
    
    @property
    def pdf(self) -> groupdocs.metadata.standards.xmp.schemes.XmpPdfPackage:
        '''Gets the PDF scheme.'''
        raise NotImplementedError()
    
    @pdf.setter
    def pdf(self, value : groupdocs.metadata.standards.xmp.schemes.XmpPdfPackage) -> None:
        '''Sets the PDF scheme.'''
        raise NotImplementedError()
    
    @property
    def photoshop(self) -> groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopPackage:
        '''Gets the Photoshop scheme.'''
        raise NotImplementedError()
    
    @photoshop.setter
    def photoshop(self, value : groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopPackage) -> None:
        '''Sets the Photoshop scheme.'''
        raise NotImplementedError()
    
    @property
    def xmp_basic(self) -> groupdocs.metadata.standards.xmp.schemes.XmpBasicPackage:
        '''Gets the XmpBasic scheme.'''
        raise NotImplementedError()
    
    @xmp_basic.setter
    def xmp_basic(self, value : groupdocs.metadata.standards.xmp.schemes.XmpBasicPackage) -> None:
        '''Sets the XmpBasic scheme.'''
        raise NotImplementedError()
    
    @property
    def xmp_dynamic_media(self) -> groupdocs.metadata.standards.xmp.schemes.XmpDynamicMediaPackage:
        '''Gets the XmpDynamicMedia scheme.'''
        raise NotImplementedError()
    
    @xmp_dynamic_media.setter
    def xmp_dynamic_media(self, value : groupdocs.metadata.standards.xmp.schemes.XmpDynamicMediaPackage) -> None:
        '''Sets the XmpDynamicMedia scheme.'''
        raise NotImplementedError()
    
    @property
    def xmp_media_management(self) -> groupdocs.metadata.standards.xmp.schemes.XmpMediaManagementPackage:
        '''Gets the XmpMediaManagement schema.'''
        raise NotImplementedError()
    
    @xmp_media_management.setter
    def xmp_media_management(self, value : groupdocs.metadata.standards.xmp.schemes.XmpMediaManagementPackage) -> None:
        '''Sets the XmpMediaManagement schema.'''
        raise NotImplementedError()
    
    @property
    def xmp_rights_management(self) -> groupdocs.metadata.standards.xmp.schemes.XmpRightsManagementPackage:
        '''Gets the XmpRightsManagement schema.'''
        raise NotImplementedError()
    
    @xmp_rights_management.setter
    def xmp_rights_management(self, value : groupdocs.metadata.standards.xmp.schemes.XmpRightsManagementPackage) -> None:
        '''Sets the XmpRightsManagement schema.'''
        raise NotImplementedError()
    
    @property
    def basic_job_ticket(self) -> groupdocs.metadata.standards.xmp.schemes.XmpBasicJobTicketPackage:
        '''Gets the BasicJobTicket scheme.'''
        raise NotImplementedError()
    
    @basic_job_ticket.setter
    def basic_job_ticket(self, value : groupdocs.metadata.standards.xmp.schemes.XmpBasicJobTicketPackage) -> None:
        '''Sets the BasicJobTicket scheme.'''
        raise NotImplementedError()
    

class XmpText(XmpValueBase):
    '''Represents XMP Text basic type.'''
    
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpText` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the value.'''
        raise NotImplementedError()
    

class XmpThumbnail(XmpComplexType):
    '''Represents a thumbnail image for a file.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpThumbnail` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, width : int, height : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpThumbnail` class.
        
        :param width: The width.
        :param height: The height.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> Optional[int]:
        '''Gets the image width in pixels.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : Optional[int]) -> None:
        '''Sets the image width in pixels.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> Optional[int]:
        '''Gets the image height in pixels.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : Optional[int]) -> None:
        '''Sets the image height in pixels.'''
        raise NotImplementedError()
    
    @property
    def image_base64(self) -> str:
        '''Gets the full thumbnail image data, converted to base 64 notation.'''
        raise NotImplementedError()
    
    @image_base64.setter
    def image_base64(self, value : str) -> None:
        '''Sets the full thumbnail image data, converted to base 64 notation.'''
        raise NotImplementedError()
    
    @property
    def image_data(self) -> List[int]:
        '''Gets the image data.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> str:
        '''Gets the image format. Defined value: JPEG.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : str) -> None:
        '''Sets the image format. Defined value: JPEG.'''
        raise NotImplementedError()
    

class XmpTime(XmpComplexType):
    '''Representation of a time value in seconds.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTime` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, scale : groupdocs.metadata.standards.xmp.XmpRational, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTime` class.
        
        :param scale: The scale.
        :param value: The value.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def scale(self) -> groupdocs.metadata.standards.xmp.XmpRational:
        '''Gets the scale for the time value.'''
        raise NotImplementedError()
    
    @scale.setter
    def scale(self, value : groupdocs.metadata.standards.xmp.XmpRational) -> None:
        '''Sets the scale for the time value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Optional[int]:
        '''Gets the time value in the specified scale.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Optional[int]) -> None:
        '''Sets the time value in the specified scale.'''
        raise NotImplementedError()
    

class XmpTimecode(XmpComplexType):
    '''Represents a timecode value in a video.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTimecode` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, format : groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat, time_value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTimecode` class.
        
        :param format: Time format.
        :param time_value: Time value.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    def set_time_format(self, time_format : groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat) -> None:
        '''Sets the time format.
        
        :param time_format: The time format.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def time_format(self) -> str:
        '''Gets the format used in the time value.'''
        raise NotImplementedError()
    
    @time_format.setter
    def time_format(self, value : str) -> None:
        '''Sets the format used in the time value.'''
        raise NotImplementedError()
    
    @property
    def time_value(self) -> str:
        '''Gets the time value in the specified format. Time values use a colon delimiter in all formats except 2997drop and 5994drop, which uses a semicolon. The four fields indicate hours, minutes, seconds, and frames: hh:mm:ss:ff'''
        raise NotImplementedError()
    
    @time_value.setter
    def time_value(self, value : str) -> None:
        '''Sets the time value in the specified format. Time values use a colon delimiter in all formats except 2997drop and 5994drop, which uses a semicolon. The four fields indicate hours, minutes, seconds, and frames: hh:mm:ss:ff'''
        raise NotImplementedError()
    

class XmpTrailerPI(IXmpType):
    '''Represents XMP trailer processing instruction.'''
    
    @overload
    def __init__(self, is_writable : bool) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTrailerPI` class.
        
        :param is_writable: Indicates whether trailer is writable.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpTrailerPI` class.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Converts XMP value to the xml representation.
        
        :returns: Returns :py:class:`str` representation of XMP value.'''
        raise NotImplementedError()
    
    @property
    def is_writable(self) -> bool:
        '''Indicates whether form may be modified in-place.'''
        raise NotImplementedError()
    

class XmpValueBase(groupdocs.metadata.common.PropertyValue):
    '''Represents base XMP value.'''
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    

class XmpVersion(XmpComplexType):
    '''Represents a version of a document.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.XmpVersion` class.'''
        raise NotImplementedError()
    
    def contains(self, property_name : str) -> bool:
        '''Determines whether the package contains a metadata property with the specified name.
        
        :param property_name: The name of the property to locate in the package.
        :returns: True if the package contains a property with the specified name; otherwise, false.'''
        raise NotImplementedError()
    
    def find_properties(self, specification : groupdocs.metadata.search.Specification) -> Sequence[groupdocs.metadata.common.MetadataProperty]:
        '''Finds the metadata properties satisfying a specification.
        The search is recursive so it affects all nested packages as well.
        
        :param specification: A function to test each metadata property for a condition.
        :returns: A collection that contains properties from the package that satisfy the condition.'''
        raise NotImplementedError()
    
    def update_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Updates known metadata properties satisfying a specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def remove_properties(self, specification : groupdocs.metadata.search.Specification) -> int:
        '''Removes metadata properties satisfying a specification.
        
        :param specification: A specification to test each metadata property for a condition.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def add_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Adds known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A value for the picked properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def set_properties(self, specification : groupdocs.metadata.search.Specification, value : groupdocs.metadata.common.PropertyValue) -> int:
        '''Sets known metadata properties satisfying the specification.
        The operation is recursive so it affects all nested packages as well.
        This method is a combination of :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` and :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from the package.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: :py:class:`str` contained XMP representation.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets the namespace URI associated with the specified prefix.
        
        :param prefix: The prefix of the namespace to get.
        :returns: The associated namespace URI if the prefix is registered; otherwise, null.'''
        raise NotImplementedError()
    
    @property
    def metadata_type(self) -> groupdocs.metadata.common.MetadataType:
        '''Gets the metadata type.'''
        raise NotImplementedError()
    
    @property
    def keys(self) -> Sequence[str]:
        '''Gets a collection of the metadata property names.'''
        raise NotImplementedError()
    
    @property
    def property_descriptors(self) -> Sequence[groupdocs.metadata.common.PropertyDescriptor]:
        '''Gets a collection of descriptors that contain information about properties accessible through the GroupDocs.Metadata search engine.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of metadata properties.'''
        raise NotImplementedError()
    
    @property
    def prefixes(self) -> List[str]:
        '''Gets the namespace prefixes that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def namespace_uris(self) -> List[str]:
        '''Gets the namespace URIs that are used in the :py:class:`groupdocs.metadata.standards.xmp.XmpComplexType` instance.'''
        raise NotImplementedError()
    
    @property
    def comments(self) -> str:
        '''Gets the comments concerning what was changed.'''
        raise NotImplementedError()
    
    @comments.setter
    def comments(self, value : str) -> None:
        '''Sets the comments concerning what was changed.'''
        raise NotImplementedError()
    
    @property
    def event(self) -> groupdocs.metadata.standards.xmp.XmpResourceEvent:
        '''Gets the high-level, formal description of what operation the user performed.'''
        raise NotImplementedError()
    
    @event.setter
    def event(self, value : groupdocs.metadata.standards.xmp.XmpResourceEvent) -> None:
        '''Sets the high-level, formal description of what operation the user performed.'''
        raise NotImplementedError()
    
    @property
    def modifier(self) -> str:
        '''Gets the person who modified this version.'''
        raise NotImplementedError()
    
    @modifier.setter
    def modifier(self, value : str) -> None:
        '''Sets the person who modified this version.'''
        raise NotImplementedError()
    
    @property
    def modify_date(self) -> Optional[datetime]:
        '''Gets the date on which this version was checked in.'''
        raise NotImplementedError()
    
    @modify_date.setter
    def modify_date(self, value : Optional[datetime]) -> None:
        '''Sets the date on which this version was checked in.'''
        raise NotImplementedError()
    
    @property
    def version_number(self) -> str:
        '''Gets the new version number.'''
        raise NotImplementedError()
    
    @version_number.setter
    def version_number(self, value : str) -> None:
        '''Sets the new version number.'''
        raise NotImplementedError()
    

class XmpArrayType:
    '''Represents array type in :py:class:`groupdocs.metadata.standards.xmp.XmpArray`.'''
    
    UNORDERED : XmpArrayType
    '''An unordered array.'''
    ORDERED : XmpArrayType
    '''An ordered array.'''
    ALTERNATIVE : XmpArrayType
    '''An alternative array.'''

class XmpColorType:
    '''Type of color in :py:class:`groupdocs.metadata.standards.xmp.XmpColorantBase`.'''
    
    PROCESS : XmpColorType
    '''The Process color type.'''
    SPOT : XmpColorType
    '''The Spot color type.'''

class XmpColorantColorMode:
    '''Represents color mode in :py:class:`groupdocs.metadata.standards.xmp.XmpColorantBase`.'''
    
    UNDEFINED : XmpColorantColorMode
    '''The color mode is undefined.'''
    CMYK : XmpColorantColorMode
    '''CMYK color mode.'''
    RGB : XmpColorantColorMode
    '''RGB color mode.'''
    LAB : XmpColorantColorMode
    '''LAB color mode.'''

