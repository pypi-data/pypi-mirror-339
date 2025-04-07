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

class XmpAudioChannelType:
    '''Represents audio channel type.'''
    
    @property
    def mono(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets mono audio channel.'''
        raise NotImplementedError()

    @property
    def stereo(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets stereo audio channel.'''
        raise NotImplementedError()

    @property
    def audio51(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets 5.1 audio channel.'''
        raise NotImplementedError()

    @property
    def audio71(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets 7.1 audio channel.'''
        raise NotImplementedError()

    @property
    def audio_16_channel(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets 16 audio channel.'''
        raise NotImplementedError()

    @property
    def other_channel(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType:
        '''Gets other channel.'''
        raise NotImplementedError()


class XmpAudioSampleType:
    '''Represents Audio sample type in :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpDynamicMediaPackage`.'''
    
    @property
    def sample_8_int(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets 8Int audio sample.'''
        raise NotImplementedError()

    @property
    def sample_16_int(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets 16Int audio sample.'''
        raise NotImplementedError()

    @property
    def sample_24_int(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets 24Int audio sample.'''
        raise NotImplementedError()

    @property
    def sample_32_int(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets 32Int audio sample.'''
        raise NotImplementedError()

    @property
    def sample_32_float(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets 32Float audio sample.'''
        raise NotImplementedError()

    @property
    def compressed(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets Compressed audio sample.'''
        raise NotImplementedError()

    @property
    def packed(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets Packed audio sample.'''
        raise NotImplementedError()

    @property
    def other(self) -> groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType:
        '''Gets Other audio sample.'''
        raise NotImplementedError()


class XmpBasicJobTicketPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents Basic Job-Ticket namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpBasicJobTicketPackage` class.'''
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
    
    @property
    def jobs(self) -> List[groupdocs.metadata.standards.xmp.XmpJob]:
        '''Gets the jobs.'''
        raise NotImplementedError()
    
    @jobs.setter
    def jobs(self, value : List[groupdocs.metadata.standards.xmp.XmpJob]) -> None:
        '''Sets the jobs.'''
        raise NotImplementedError()
    

class XmpBasicPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the XMP basic namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpBasicPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Adds string property.
        
        :param name: XmpBasic key.
        :param value: String value.'''
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
    
    @property
    def base_url(self) -> str:
        '''Gets the base URL for relative URLs in the document content.
        If this document contains Internet links, and those links are relative, they are relative to this base URL.'''
        raise NotImplementedError()
    
    @base_url.setter
    def base_url(self, value : str) -> None:
        '''Sets the base URL for relative URLs in the document content.
        If this document contains Internet links, and those links are relative, they are relative to this base URL.'''
        raise NotImplementedError()
    
    @property
    def create_date(self) -> Optional[datetime]:
        '''Gets the date and time the resource was created.'''
        raise NotImplementedError()
    
    @create_date.setter
    def create_date(self, value : Optional[datetime]) -> None:
        '''Sets the date and time the resource was created.'''
        raise NotImplementedError()
    
    @property
    def creator_tool(self) -> str:
        '''Gets the name of the tool used to create the resource.'''
        raise NotImplementedError()
    
    @creator_tool.setter
    def creator_tool(self, value : str) -> None:
        '''Sets the name of the tool used to create the resource.'''
        raise NotImplementedError()
    
    @property
    def identifiers(self) -> List[str]:
        '''Gets an unordered array of text strings that unambiguously identify the resource within a given context.'''
        raise NotImplementedError()
    
    @identifiers.setter
    def identifiers(self, value : List[str]) -> None:
        '''Sets an unordered array of text strings that unambiguously identify the resource within a given context.'''
        raise NotImplementedError()
    
    @property
    def label(self) -> str:
        '''Gets a word or short phrase that identifies the resource as a member of a user-defined collection.'''
        raise NotImplementedError()
    
    @label.setter
    def label(self, value : str) -> None:
        '''Sets a word or short phrase that identifies the resource as a member of a user-defined collection.'''
        raise NotImplementedError()
    
    @property
    def metadata_date(self) -> Optional[datetime]:
        '''Gets the date and time that any metadata for this resource was last changed.'''
        raise NotImplementedError()
    
    @metadata_date.setter
    def metadata_date(self, value : Optional[datetime]) -> None:
        '''Sets the date and time that any metadata for this resource was last changed.'''
        raise NotImplementedError()
    
    @property
    def modify_date(self) -> Optional[datetime]:
        '''Gets the date and time the resource was last modified.'''
        raise NotImplementedError()
    
    @modify_date.setter
    def modify_date(self, value : Optional[datetime]) -> None:
        '''Sets the date and time the resource was last modified.'''
        raise NotImplementedError()
    
    @property
    def nickname(self) -> str:
        '''Gets a short informal name for the resource.'''
        raise NotImplementedError()
    
    @nickname.setter
    def nickname(self, value : str) -> None:
        '''Sets a short informal name for the resource.'''
        raise NotImplementedError()
    
    @property
    def rating(self) -> float:
        '''Gets a user-assigned rating for this file.
        The value shall be -1 or in the range [0..5], where -1 indicates “rejected” and 0 indicates “unrated”.'''
        raise NotImplementedError()
    
    @rating.setter
    def rating(self, value : float) -> None:
        '''Sets a user-assigned rating for this file.
        The value shall be -1 or in the range [0..5], where -1 indicates “rejected” and 0 indicates “unrated”.'''
        raise NotImplementedError()
    
    @property
    def thumbnails(self) -> List[groupdocs.metadata.standards.xmp.XmpThumbnail]:
        '''Gets an array of thumbnail images for the file, which can differ in characteristics such as size or image encoding.'''
        raise NotImplementedError()
    
    @thumbnails.setter
    def thumbnails(self, value : List[groupdocs.metadata.standards.xmp.XmpThumbnail]) -> None:
        '''Sets an array of thumbnail images for the file, which can differ in characteristics such as size or image encoding.'''
        raise NotImplementedError()
    
    @property
    def RATING_REJECTED(self) -> float:
        '''Rating rejected value.'''
        raise NotImplementedError()

    @property
    def RATING_MIN(self) -> float:
        '''Rating min value.'''
        raise NotImplementedError()

    @property
    def RATING_MAX(self) -> float:
        '''Rating max value.'''
        raise NotImplementedError()


class XmpCameraRawPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents Camera Raw schema.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Adds string property.
        
        :param name: XMP metadata key.
        :param value: XMP metadata value.'''
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
    
    def set_white_balance(self, white_balance : groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance) -> None:
        '''Sets the white balance.
        
        :param white_balance: The white balance.'''
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
    
    @property
    def auto_brightness(self) -> Optional[bool]:
        '''Gets the AutoBrightness value. When true, :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.brightness` is automatically adjusted.'''
        raise NotImplementedError()
    
    @auto_brightness.setter
    def auto_brightness(self, value : Optional[bool]) -> None:
        '''Sets the AutoBrightness value. When true, :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.brightness` is automatically adjusted.'''
        raise NotImplementedError()
    
    @property
    def auto_contrast(self) -> Optional[bool]:
        '''Gets the AutoContrast value. When true, "Contrast" is automatically adjusted.'''
        raise NotImplementedError()
    
    @auto_contrast.setter
    def auto_contrast(self, value : Optional[bool]) -> None:
        '''Sets the AutoContrast value. When true, "Contrast" is automatically adjusted.'''
        raise NotImplementedError()
    
    @property
    def auto_exposure(self) -> Optional[bool]:
        '''Gets the AutoExposure value. When true, "Exposure" is automatically adjusted.'''
        raise NotImplementedError()
    
    @auto_exposure.setter
    def auto_exposure(self, value : Optional[bool]) -> None:
        '''Sets the AutoExposure value. When true, "Exposure" is automatically adjusted.'''
        raise NotImplementedError()
    
    @property
    def auto_shadows(self) -> Optional[bool]:
        '''Gets the AutoShadows value. When true, "Shadows" is automatically adjusted.'''
        raise NotImplementedError()
    
    @auto_shadows.setter
    def auto_shadows(self, value : Optional[bool]) -> None:
        '''Sets the AutoShadows value. When true, "Shadows" is automatically adjusted.'''
        raise NotImplementedError()
    
    @property
    def blue_hue(self) -> Optional[int]:
        '''Gets the BlueHue value. Null if undefined.'''
        raise NotImplementedError()
    
    @blue_hue.setter
    def blue_hue(self, value : Optional[int]) -> None:
        '''Sets the BlueHue value. Null if undefined.'''
        raise NotImplementedError()
    
    @property
    def blue_saturation(self) -> Optional[int]:
        '''Gets the BlueSaturation. Null if undefined.'''
        raise NotImplementedError()
    
    @blue_saturation.setter
    def blue_saturation(self, value : Optional[int]) -> None:
        '''Sets the BlueSaturation. Null if undefined.'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> Optional[int]:
        '''Gets the Brightness value. Null if undefined.'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : Optional[int]) -> None:
        '''Sets the Brightness value. Null if undefined.'''
        raise NotImplementedError()
    
    @property
    def camera_profile(self) -> str:
        '''Gets the CameraProfile value.'''
        raise NotImplementedError()
    
    @camera_profile.setter
    def camera_profile(self, value : str) -> None:
        '''Sets the CameraProfile value.'''
        raise NotImplementedError()
    
    @property
    def chromatic_aberration_b(self) -> Optional[int]:
        '''Gets the "Chromatic Aberration, Fix Blue/Yellow Fringe" setting. Null if undefined.'''
        raise NotImplementedError()
    
    @chromatic_aberration_b.setter
    def chromatic_aberration_b(self, value : Optional[int]) -> None:
        '''Sets the "Chromatic Aberration, Fix Blue/Yellow Fringe" setting. Null if undefined.'''
        raise NotImplementedError()
    
    @property
    def chromatic_aberration_r(self) -> Optional[int]:
        '''Gets the "Chromatic Aberration, Fix Red/Cyan Fringe" setting. Null if undefined.'''
        raise NotImplementedError()
    
    @chromatic_aberration_r.setter
    def chromatic_aberration_r(self, value : Optional[int]) -> None:
        '''Sets the "Chromatic Aberration, Fix Red/Cyan Fringe" setting. Null if undefined.'''
        raise NotImplementedError()
    
    @property
    def color_noise_reduction(self) -> Optional[int]:
        '''Gets the Color Noise Reduction setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @color_noise_reduction.setter
    def color_noise_reduction(self, value : Optional[int]) -> None:
        '''Sets the Color Noise Reduction setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> Optional[int]:
        '''Gets the Contrast setting. Range -50 to 100.'''
        raise NotImplementedError()
    
    @contrast.setter
    def contrast(self, value : Optional[int]) -> None:
        '''Sets the Contrast setting. Range -50 to 100.'''
        raise NotImplementedError()
    
    @property
    def crop_top(self) -> Optional[float]:
        '''Gets the CropTop setting. When HasCrop is true, top of the crop rectangle.'''
        raise NotImplementedError()
    
    @crop_top.setter
    def crop_top(self, value : Optional[float]) -> None:
        '''Sets the CropTop setting. When HasCrop is true, top of the crop rectangle.'''
        raise NotImplementedError()
    
    @property
    def crop_left(self) -> Optional[float]:
        '''Gets the CropLeft setting. When HasCrop is true, left of the crop rectangle.'''
        raise NotImplementedError()
    
    @crop_left.setter
    def crop_left(self, value : Optional[float]) -> None:
        '''Sets the CropLeft setting. When HasCrop is true, left of the crop rectangle.'''
        raise NotImplementedError()
    
    @property
    def crop_bottom(self) -> Optional[float]:
        '''Gets the CropBottom setting. When HasCrop is true, bottom of the crop rectangle.'''
        raise NotImplementedError()
    
    @crop_bottom.setter
    def crop_bottom(self, value : Optional[float]) -> None:
        '''Sets the CropBottom setting. When HasCrop is true, bottom of the crop rectangle.'''
        raise NotImplementedError()
    
    @property
    def crop_right(self) -> Optional[float]:
        '''Gets the CropRight setting. When HasCrop is true, right of the crop rectangle.'''
        raise NotImplementedError()
    
    @crop_right.setter
    def crop_right(self, value : Optional[float]) -> None:
        '''Sets the CropRight setting. When HasCrop is true, right of the crop rectangle.'''
        raise NotImplementedError()
    
    @property
    def crop_angle(self) -> Optional[float]:
        '''Gets the CropAngle setting. When HasCrop is true, angle of the crop rectangle.'''
        raise NotImplementedError()
    
    @crop_angle.setter
    def crop_angle(self, value : Optional[float]) -> None:
        '''Sets the CropAngle setting. When HasCrop is true, angle of the crop rectangle.'''
        raise NotImplementedError()
    
    @property
    def crop_width(self) -> Optional[float]:
        '''Gets the width of the resulting cropped image in :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_units` units.'''
        raise NotImplementedError()
    
    @crop_width.setter
    def crop_width(self, value : Optional[float]) -> None:
        '''Sets the width of the resulting cropped image in :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_units` units.'''
        raise NotImplementedError()
    
    @property
    def crop_height(self) -> Optional[float]:
        '''Gets the height of the resulting cropped image in :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_units` units.'''
        raise NotImplementedError()
    
    @crop_height.setter
    def crop_height(self, value : Optional[float]) -> None:
        '''Sets the height of the resulting cropped image in :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_units` units.'''
        raise NotImplementedError()
    
    @property
    def crop_units(self) -> groupdocs.metadata.standards.xmp.schemes.XmpCropUnit:
        '''Gets units for :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_width` and :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_height`.'''
        raise NotImplementedError()
    
    @crop_units.setter
    def crop_units(self, value : groupdocs.metadata.standards.xmp.schemes.XmpCropUnit) -> None:
        '''Sets units for :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_width` and :py:attr:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.crop_height`.'''
        raise NotImplementedError()
    
    @property
    def exposure(self) -> Optional[float]:
        '''Gets the Exposure setting.'''
        raise NotImplementedError()
    
    @exposure.setter
    def exposure(self, value : Optional[float]) -> None:
        '''Sets the Exposure setting.'''
        raise NotImplementedError()
    
    @property
    def green_hue(self) -> Optional[int]:
        '''Gets the Green Hue setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @green_hue.setter
    def green_hue(self, value : Optional[int]) -> None:
        '''Sets the Green Hue setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def green_saturation(self) -> Optional[int]:
        '''Gets the Green Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @green_saturation.setter
    def green_saturation(self, value : Optional[int]) -> None:
        '''Sets the Green Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def has_crop(self) -> Optional[bool]:
        '''Gets the HasCrop value. When true, the image has a cropping rectangle.'''
        raise NotImplementedError()
    
    @has_crop.setter
    def has_crop(self, value : Optional[bool]) -> None:
        '''Sets the HasCrop value. When true, the image has a cropping rectangle.'''
        raise NotImplementedError()
    
    @property
    def has_settings(self) -> Optional[bool]:
        '''Gets HasSettings value. When true, non-default camera raw settings.'''
        raise NotImplementedError()
    
    @has_settings.setter
    def has_settings(self, value : Optional[bool]) -> None:
        '''Sets HasSettings value. When true, non-default camera raw settings.'''
        raise NotImplementedError()
    
    @property
    def luminance_smoothing(self) -> Optional[int]:
        '''Gets the LuminanceSmoothing setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @luminance_smoothing.setter
    def luminance_smoothing(self, value : Optional[int]) -> None:
        '''Sets the LuminanceSmoothing setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def raw_file_name(self) -> str:
        '''Gets the file name for a raw file (not a complete path).'''
        raise NotImplementedError()
    
    @raw_file_name.setter
    def raw_file_name(self, value : str) -> None:
        '''Sets the file name for a raw file (not a complete path).'''
        raise NotImplementedError()
    
    @property
    def red_hue(self) -> Optional[int]:
        '''Gets the Red Hue setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @red_hue.setter
    def red_hue(self, value : Optional[int]) -> None:
        '''Sets the Red Hue setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def red_saturation(self) -> Optional[int]:
        '''Gets the Red Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @red_saturation.setter
    def red_saturation(self, value : Optional[int]) -> None:
        '''Sets the Red Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def saturation(self) -> Optional[int]:
        '''Gets the Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @saturation.setter
    def saturation(self, value : Optional[int]) -> None:
        '''Sets the Saturation setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def shadows(self) -> Optional[int]:
        '''Gets the Shadows setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @shadows.setter
    def shadows(self, value : Optional[int]) -> None:
        '''Sets the Shadows setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def shadow_tint(self) -> Optional[int]:
        '''Gets the ShadowTint setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @shadow_tint.setter
    def shadow_tint(self, value : Optional[int]) -> None:
        '''Sets the ShadowTint setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def sharpness(self) -> Optional[int]:
        '''Gets the Sharpness setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @sharpness.setter
    def sharpness(self, value : Optional[int]) -> None:
        '''Sets the Sharpness setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def temperature(self) -> Optional[int]:
        '''Gets the Temperature setting. Range 2000 to 50000.'''
        raise NotImplementedError()
    
    @temperature.setter
    def temperature(self, value : Optional[int]) -> None:
        '''Sets the Temperature setting. Range 2000 to 50000.'''
        raise NotImplementedError()
    
    @property
    def tint(self) -> Optional[int]:
        '''Gets the Tint setting. Range -150 to 150.'''
        raise NotImplementedError()
    
    @tint.setter
    def tint(self, value : Optional[int]) -> None:
        '''Sets the Tint setting. Range -150 to 150.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''Gets the version of the Camera Raw plug-in.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : str) -> None:
        '''Sets the version of the Camera Raw plug-in.'''
        raise NotImplementedError()
    
    @property
    def vignette_amount(self) -> Optional[int]:
        '''Gets the Vignette Amount setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @vignette_amount.setter
    def vignette_amount(self, value : Optional[int]) -> None:
        '''Sets the Vignette Amount setting. Range -100 to 100.'''
        raise NotImplementedError()
    
    @property
    def vignette_midpoint(self) -> Optional[int]:
        '''Gets the Vignetting Midpoint setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @vignette_midpoint.setter
    def vignette_midpoint(self, value : Optional[int]) -> None:
        '''Sets the Vignetting Midpoint setting. Range 0 to 100.'''
        raise NotImplementedError()
    
    @property
    def white_balance(self) -> str:
        '''Gets White Balance setting. Use :py:func:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage.set_white_balance` to set white balance value.'''
        raise NotImplementedError()
    

class XmpDublinCorePackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the Dublin Core scheme.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpDublinCorePackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpArray) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpArray` .
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
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
    
    def set_contributor(self, contributor : str) -> None:
        '''Sets a single contributor of the resource.
        
        :param contributor: The contributor to set.'''
        raise NotImplementedError()
    
    def set_creator(self, creator : str) -> None:
        '''Sets a single creator of the resource.
        
        :param creator: The creator to set.'''
        raise NotImplementedError()
    
    def set_date(self, date : datetime) -> None:
        '''Sets a single date associated with the resource.
        
        :param date: The date to set.'''
        raise NotImplementedError()
    
    def set_description(self, description : str) -> None:
        '''Sets the resource description, given in a single laguage.
        
        :param description: The description to set.'''
        raise NotImplementedError()
    
    def set_language(self, language : str) -> None:
        '''Sets a single language associated with the resource.
        
        :param language: The language to set.'''
        raise NotImplementedError()
    
    def set_publisher(self, publisher : str) -> None:
        '''Sets a single publisher of the resource.
        
        :param publisher: The publisher to set.'''
        raise NotImplementedError()
    
    def set_relation(self, relation : str) -> None:
        '''Sets a single related resource.
        
        :param relation: The relation to set.'''
        raise NotImplementedError()
    
    def set_rights(self, rights : str) -> None:
        '''Sets the resource rights, given in a single laguage.
        
        :param rights: The rights statements to set.'''
        raise NotImplementedError()
    
    def set_subject(self, subject : str) -> None:
        '''Sets a single subject of the resource.
        
        :param subject: The subject to set.'''
        raise NotImplementedError()
    
    def set_title(self, title : str) -> None:
        '''Sets the resource title, given in a single laguage.
        
        :param title: The title to set.'''
        raise NotImplementedError()
    
    def set_type(self, type : str) -> None:
        '''Sets a single type of the resource.
        
        :param type: The type to set.'''
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
    
    @property
    def contributors(self) -> List[str]:
        '''Gets an array of the contributors.'''
        raise NotImplementedError()
    
    @contributors.setter
    def contributors(self, value : List[str]) -> None:
        '''Sets an array of the contributors.'''
        raise NotImplementedError()
    
    @property
    def coverage(self) -> str:
        '''Gets the extent or scope of the resource.'''
        raise NotImplementedError()
    
    @coverage.setter
    def coverage(self, value : str) -> None:
        '''Sets the extent or scope of the resource.'''
        raise NotImplementedError()
    
    @property
    def creators(self) -> List[str]:
        '''Gets an array of the creators.'''
        raise NotImplementedError()
    
    @creators.setter
    def creators(self, value : List[str]) -> None:
        '''Sets an array of the creators.'''
        raise NotImplementedError()
    
    @property
    def dates(self) -> List[datetime]:
        '''Gets an array of dates associated with an event in the life cycle of the resource.'''
        raise NotImplementedError()
    
    @dates.setter
    def dates(self, value : List[datetime]) -> None:
        '''Sets an array of dates associated with an event in the life cycle of the resource.'''
        raise NotImplementedError()
    
    @property
    def descriptions(self) -> groupdocs.metadata.standards.xmp.XmpLangAlt:
        '''Gets an array of textual descriptions of the content of the resource, given in various languages.'''
        raise NotImplementedError()
    
    @descriptions.setter
    def descriptions(self, value : groupdocs.metadata.standards.xmp.XmpLangAlt) -> None:
        '''Sets an array of textual descriptions of the content of the resource, given in various languages.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> str:
        '''Gets the MIME type of the resource.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : str) -> None:
        '''Sets the MIME type of the resource.'''
        raise NotImplementedError()
    
    @property
    def identifier(self) -> str:
        '''Gets a string value representing an unambiguous reference to the resource within a given context.'''
        raise NotImplementedError()
    
    @identifier.setter
    def identifier(self, value : str) -> None:
        '''Sets a string value representing an unambiguous reference to the resource within a given context.'''
        raise NotImplementedError()
    
    @property
    def languages(self) -> List[str]:
        '''Gets an array of languages used in the content of the resource.'''
        raise NotImplementedError()
    
    @languages.setter
    def languages(self, value : List[str]) -> None:
        '''Sets an array of languages used in the content of the resource.'''
        raise NotImplementedError()
    
    @property
    def publishers(self) -> List[str]:
        '''Gets an array of publishers made the resource available.'''
        raise NotImplementedError()
    
    @publishers.setter
    def publishers(self, value : List[str]) -> None:
        '''Sets an array of publishers made the resource available.'''
        raise NotImplementedError()
    
    @property
    def relations(self) -> List[str]:
        '''Gets an array of the related resources.'''
        raise NotImplementedError()
    
    @relations.setter
    def relations(self, value : List[str]) -> None:
        '''Sets an array of the related resources.'''
        raise NotImplementedError()
    
    @property
    def rights(self) -> groupdocs.metadata.standards.xmp.XmpLangAlt:
        '''Gets an array of the informal rights statements, given in various languages.'''
        raise NotImplementedError()
    
    @rights.setter
    def rights(self, value : groupdocs.metadata.standards.xmp.XmpLangAlt) -> None:
        '''Sets an array of the informal rights statements, given in various languages.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> str:
        '''Gets the related resource from which the described resource is derived.'''
        raise NotImplementedError()
    
    @source.setter
    def source(self, value : str) -> None:
        '''Sets the related resource from which the described resource is derived.'''
        raise NotImplementedError()
    
    @property
    def subjects(self) -> List[str]:
        '''Gets an array of descriptive phrases or keywords that specify the content of the resource.'''
        raise NotImplementedError()
    
    @subjects.setter
    def subjects(self, value : List[str]) -> None:
        '''Sets an array of descriptive phrases or keywords that specify the content of the resource.'''
        raise NotImplementedError()
    
    @property
    def titles(self) -> groupdocs.metadata.standards.xmp.XmpLangAlt:
        '''Gets the title or name of the resource, given in various languages.'''
        raise NotImplementedError()
    
    @titles.setter
    def titles(self, value : groupdocs.metadata.standards.xmp.XmpLangAlt) -> None:
        '''Sets the title or name of the resource, given in various languages.'''
        raise NotImplementedError()
    
    @property
    def types(self) -> List[str]:
        '''Gets an array of string values representing the nature or genre of the resource.'''
        raise NotImplementedError()
    
    @types.setter
    def types(self, value : List[str]) -> None:
        '''Sets an array of string values representing the nature or genre of the resource.'''
        raise NotImplementedError()
    

class XmpDynamicMediaPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents XMP Dynamic Media namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpDynamicMediaPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Sets string property.
        
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
    
    def set_audio_channel_type(self, audio_channel_type : groupdocs.metadata.standards.xmp.schemes.XmpAudioChannelType) -> None:
        '''Sets the audio channel type.
        
        :param audio_channel_type: The audio channel type.'''
        raise NotImplementedError()
    
    def set_audio_sample_type(self, audio_sample_type : groupdocs.metadata.standards.xmp.schemes.XmpAudioSampleType) -> None:
        '''Sets the audio sample type.
        
        :param audio_sample_type: The audio sample type.'''
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
    
    @property
    def abs_peak_audio_file_path(self) -> str:
        '''Gets the absolute path to the file’s peak audio file.'''
        raise NotImplementedError()
    
    @abs_peak_audio_file_path.setter
    def abs_peak_audio_file_path(self, value : str) -> None:
        '''Sets the absolute path to the file’s peak audio file.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Gets the name of the album.'''
        raise NotImplementedError()
    
    @album.setter
    def album(self, value : str) -> None:
        '''Sets the name of the album.'''
        raise NotImplementedError()
    
    @property
    def alt_tape_name(self) -> str:
        '''Gets the alternative tape name, set via the project window or timecode dialog in Premiere.'''
        raise NotImplementedError()
    
    @alt_tape_name.setter
    def alt_tape_name(self, value : str) -> None:
        '''Sets the alternative tape name, set via the project window or timecode dialog in Premiere.'''
        raise NotImplementedError()
    
    @property
    def alt_timecode(self) -> groupdocs.metadata.standards.xmp.XmpTimecode:
        '''Gets the timecode set by the user.'''
        raise NotImplementedError()
    
    @alt_timecode.setter
    def alt_timecode(self, value : groupdocs.metadata.standards.xmp.XmpTimecode) -> None:
        '''Sets the timecode set by the user.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the name of the artist or artists.'''
        raise NotImplementedError()
    
    @artist.setter
    def artist(self, value : str) -> None:
        '''Sets the name of the artist or artists.'''
        raise NotImplementedError()
    
    @property
    def audio_channel_type(self) -> str:
        '''Gets the audio channel type.'''
        raise NotImplementedError()
    
    @audio_channel_type.setter
    def audio_channel_type(self, value : str) -> None:
        '''Sets the audio channel type.'''
        raise NotImplementedError()
    
    @property
    def audio_compressor(self) -> str:
        '''Gets the audio compression used.'''
        raise NotImplementedError()
    
    @audio_compressor.setter
    def audio_compressor(self, value : str) -> None:
        '''Sets the audio compression used.'''
        raise NotImplementedError()
    
    @property
    def audio_sample_rate(self) -> Optional[int]:
        '''Gets the audio sample rate.'''
        raise NotImplementedError()
    
    @audio_sample_rate.setter
    def audio_sample_rate(self, value : Optional[int]) -> None:
        '''Sets the audio sample rate.'''
        raise NotImplementedError()
    
    @property
    def audio_sample_type(self) -> str:
        '''Gets the audio sample type.'''
        raise NotImplementedError()
    
    @audio_sample_type.setter
    def audio_sample_type(self, value : str) -> None:
        '''Sets the audio sample type.'''
        raise NotImplementedError()
    
    @property
    def camera_angle(self) -> str:
        '''Gets the orientation of the camera to the subject in a static shot, from a fixed set of industry standard terminology.'''
        raise NotImplementedError()
    
    @camera_angle.setter
    def camera_angle(self, value : str) -> None:
        '''Sets the orientation of the camera to the subject in a static shot, from a fixed set of industry standard terminology.'''
        raise NotImplementedError()
    
    @property
    def camera_label(self) -> str:
        '''Gets the description of the camera used for a shoot.'''
        raise NotImplementedError()
    
    @camera_label.setter
    def camera_label(self, value : str) -> None:
        '''Sets the description of the camera used for a shoot.'''
        raise NotImplementedError()
    
    @property
    def camera_model(self) -> str:
        '''Gets the make and model of the camera used for a shoot.'''
        raise NotImplementedError()
    
    @camera_model.setter
    def camera_model(self, value : str) -> None:
        '''Sets the make and model of the camera used for a shoot.'''
        raise NotImplementedError()
    
    @property
    def camera_move(self) -> str:
        '''Gets the movement of the camera during the shot, from a fixed set of industry standard terminology.'''
        raise NotImplementedError()
    
    @camera_move.setter
    def camera_move(self, value : str) -> None:
        '''Sets the movement of the camera during the shot, from a fixed set of industry standard terminology.'''
        raise NotImplementedError()
    
    @property
    def client(self) -> str:
        '''Gets the client for the job of which this shot or take is a part.'''
        raise NotImplementedError()
    
    @client.setter
    def client(self, value : str) -> None:
        '''Sets the client for the job of which this shot or take is a part.'''
        raise NotImplementedError()
    
    @property
    def comment(self) -> str:
        '''Gets the user’s comments.'''
        raise NotImplementedError()
    
    @comment.setter
    def comment(self, value : str) -> None:
        '''Sets the user’s comments.'''
        raise NotImplementedError()
    
    @property
    def composer(self) -> str:
        '''Gets the composer’s names.'''
        raise NotImplementedError()
    
    @composer.setter
    def composer(self, value : str) -> None:
        '''Sets the composer’s names.'''
        raise NotImplementedError()
    
    @property
    def director(self) -> str:
        '''Gets the director of the scene.'''
        raise NotImplementedError()
    
    @director.setter
    def director(self, value : str) -> None:
        '''Sets the director of the scene.'''
        raise NotImplementedError()
    
    @property
    def director_photography(self) -> str:
        '''Gets the director of photography for the scene.'''
        raise NotImplementedError()
    
    @director_photography.setter
    def director_photography(self, value : str) -> None:
        '''Sets the director of photography for the scene.'''
        raise NotImplementedError()
    
    @property
    def duration(self) -> groupdocs.metadata.standards.xmp.XmpTime:
        '''Gets the duration of the media file.'''
        raise NotImplementedError()
    
    @duration.setter
    def duration(self, value : groupdocs.metadata.standards.xmp.XmpTime) -> None:
        '''Sets the duration of the media file.'''
        raise NotImplementedError()
    
    @property
    def engineer(self) -> str:
        '''Gets the engineer\'s names.'''
        raise NotImplementedError()
    
    @engineer.setter
    def engineer(self, value : str) -> None:
        '''Sets the engineer\'s names.'''
        raise NotImplementedError()
    
    @property
    def file_data_rate(self) -> groupdocs.metadata.standards.xmp.XmpRational:
        '''Gets the file data rate in megabytes per second.'''
        raise NotImplementedError()
    
    @file_data_rate.setter
    def file_data_rate(self, value : groupdocs.metadata.standards.xmp.XmpRational) -> None:
        '''Sets the file data rate in megabytes per second.'''
        raise NotImplementedError()
    
    @property
    def genre(self) -> str:
        '''Gets the name of the genres.'''
        raise NotImplementedError()
    
    @genre.setter
    def genre(self, value : str) -> None:
        '''Sets the name of the genres.'''
        raise NotImplementedError()
    
    @property
    def good(self) -> Optional[bool]:
        '''Gets a value indicating whether the shot is a keeper.'''
        raise NotImplementedError()
    
    @good.setter
    def good(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether the shot is a keeper.'''
        raise NotImplementedError()
    
    @property
    def instrument(self) -> str:
        '''Gets the musical instruments.'''
        raise NotImplementedError()
    
    @instrument.setter
    def instrument(self, value : str) -> None:
        '''Sets the musical instruments.'''
        raise NotImplementedError()
    
    @property
    def intro_time(self) -> groupdocs.metadata.standards.xmp.XmpTime:
        '''Gets the duration of lead time for queuing music.'''
        raise NotImplementedError()
    
    @intro_time.setter
    def intro_time(self, value : groupdocs.metadata.standards.xmp.XmpTime) -> None:
        '''Sets the duration of lead time for queuing music.'''
        raise NotImplementedError()
    
    @property
    def key(self) -> str:
        '''Gets the audio’s musical key.'''
        raise NotImplementedError()
    
    @key.setter
    def key(self, value : str) -> None:
        '''Sets the audio’s musical key.'''
        raise NotImplementedError()
    
    @property
    def log_comment(self) -> str:
        '''Gets the user’s log comments.'''
        raise NotImplementedError()
    
    @log_comment.setter
    def log_comment(self, value : str) -> None:
        '''Sets the user’s log comments.'''
        raise NotImplementedError()
    
    @property
    def loop(self) -> Optional[bool]:
        '''Gets a value indicating whether the clip can be looped seamlessly.'''
        raise NotImplementedError()
    
    @loop.setter
    def loop(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether the clip can be looped seamlessly.'''
        raise NotImplementedError()
    
    @property
    def number_of_beats(self) -> Optional[float]:
        '''Gets the total number of musical beats in a clip; for example, the beats-per-second times the duration in seconds.'''
        raise NotImplementedError()
    
    @number_of_beats.setter
    def number_of_beats(self, value : Optional[float]) -> None:
        '''Sets the total number of musical beats in a clip; for example, the beats-per-second times the duration in seconds.'''
        raise NotImplementedError()
    
    @property
    def out_cue(self) -> groupdocs.metadata.standards.xmp.XmpTime:
        '''Gets the time at which to fade out.'''
        raise NotImplementedError()
    
    @out_cue.setter
    def out_cue(self, value : groupdocs.metadata.standards.xmp.XmpTime) -> None:
        '''Sets the time at which to fade out.'''
        raise NotImplementedError()
    
    @property
    def project_name(self) -> str:
        '''Gets the name of the project of which this file is a part.'''
        raise NotImplementedError()
    
    @project_name.setter
    def project_name(self, value : str) -> None:
        '''Sets the name of the project of which this file is a part.'''
        raise NotImplementedError()
    
    @property
    def relative_timestamp(self) -> groupdocs.metadata.standards.xmp.XmpTime:
        '''Gets the start time of the media inside the audio project.'''
        raise NotImplementedError()
    
    @relative_timestamp.setter
    def relative_timestamp(self, value : groupdocs.metadata.standards.xmp.XmpTime) -> None:
        '''Sets the start time of the media inside the audio project.'''
        raise NotImplementedError()
    
    @property
    def release_date(self) -> Optional[datetime]:
        '''Gets the date the title was released.'''
        raise NotImplementedError()
    
    @release_date.setter
    def release_date(self, value : Optional[datetime]) -> None:
        '''Sets the date the title was released.'''
        raise NotImplementedError()
    
    @property
    def shot_date(self) -> Optional[datetime]:
        '''Gets the date and time when the video was shot.'''
        raise NotImplementedError()
    
    @shot_date.setter
    def shot_date(self, value : Optional[datetime]) -> None:
        '''Sets the date and time when the video was shot.'''
        raise NotImplementedError()
    
    @property
    def start_timecode(self) -> groupdocs.metadata.standards.xmp.XmpTimecode:
        '''Gets the timecode of the first frame of video in the file, as obtained from the device control.'''
        raise NotImplementedError()
    
    @start_timecode.setter
    def start_timecode(self, value : groupdocs.metadata.standards.xmp.XmpTimecode) -> None:
        '''Sets the timecode of the first frame of video in the file, as obtained from the device control.'''
        raise NotImplementedError()
    
    @property
    def take_number(self) -> Optional[int]:
        '''Gets a numeric value indicating the absolute number of a take.'''
        raise NotImplementedError()
    
    @take_number.setter
    def take_number(self, value : Optional[int]) -> None:
        '''Sets a numeric value indicating the absolute number of a take.'''
        raise NotImplementedError()
    
    @property
    def tempo(self) -> Optional[float]:
        '''Gets the audio’s tempo.'''
        raise NotImplementedError()
    
    @tempo.setter
    def tempo(self, value : Optional[float]) -> None:
        '''Sets the audio’s tempo.'''
        raise NotImplementedError()
    
    @property
    def track_number(self) -> Optional[int]:
        '''Gets a numeric value indicating the order of the audio file within its original recording.'''
        raise NotImplementedError()
    
    @track_number.setter
    def track_number(self, value : Optional[int]) -> None:
        '''Sets a numeric value indicating the order of the audio file within its original recording.'''
        raise NotImplementedError()
    
    @property
    def video_alpha_premultiple_color(self) -> groupdocs.metadata.standards.xmp.XmpColorantBase:
        '''Gets the timecode of the first frame of video in the file, as obtained from the device control.'''
        raise NotImplementedError()
    
    @video_alpha_premultiple_color.setter
    def video_alpha_premultiple_color(self, value : groupdocs.metadata.standards.xmp.XmpColorantBase) -> None:
        '''Sets the timecode of the first frame of video in the file, as obtained from the device control.'''
        raise NotImplementedError()
    
    @property
    def video_alpha_unity_is_transparent(self) -> Optional[bool]:
        '''Gets a value indicating whether the unity is clear.'''
        raise NotImplementedError()
    
    @video_alpha_unity_is_transparent.setter
    def video_alpha_unity_is_transparent(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether the unity is clear.'''
        raise NotImplementedError()
    
    @property
    def video_frame_rate(self) -> Optional[float]:
        '''Gets the video frame rate.'''
        raise NotImplementedError()
    
    @video_frame_rate.setter
    def video_frame_rate(self, value : Optional[float]) -> None:
        '''Sets the video frame rate.'''
        raise NotImplementedError()
    
    @property
    def video_frame_size(self) -> groupdocs.metadata.standards.xmp.XmpDimensions:
        '''Gets the frame size.'''
        raise NotImplementedError()
    
    @video_frame_size.setter
    def video_frame_size(self, value : groupdocs.metadata.standards.xmp.XmpDimensions) -> None:
        '''Sets the frame size.'''
        raise NotImplementedError()
    
    @property
    def video_pixel_aspect_ratio(self) -> groupdocs.metadata.standards.xmp.XmpRational:
        '''Gets the aspect ratio, expressed as wd/ht.'''
        raise NotImplementedError()
    
    @video_pixel_aspect_ratio.setter
    def video_pixel_aspect_ratio(self, value : groupdocs.metadata.standards.xmp.XmpRational) -> None:
        '''Sets the aspect ratio, expressed as wd/ht.'''
        raise NotImplementedError()
    
    @property
    def part_of_compilation(self) -> Optional[bool]:
        '''Gets a value indicating whether the resource is a part of compilation.'''
        raise NotImplementedError()
    
    @part_of_compilation.setter
    def part_of_compilation(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether the resource is a part of compilation.'''
        raise NotImplementedError()
    

class XmpIptcCorePackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the IPTC Core XMP package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpIptcCorePackage` class.'''
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
    
    @property
    def country_code(self) -> str:
        '''Gets the code of the country the content is focusing on. The code should be taken from ISO 3166 two or three letter code.'''
        raise NotImplementedError()
    
    @country_code.setter
    def country_code(self, value : str) -> None:
        '''Sets the code of the country the content is focusing on. The code should be taken from ISO 3166 two or three letter code.'''
        raise NotImplementedError()
    
    @property
    def intellectual_genre(self) -> str:
        '''Gets the intellectual genre. Describes the nature, intellectual, artistic or journalistic characteristic of a news object, not specifically its content.'''
        raise NotImplementedError()
    
    @intellectual_genre.setter
    def intellectual_genre(self, value : str) -> None:
        '''Sets the intellectual genre. Describes the nature, intellectual, artistic or journalistic characteristic of a news object, not specifically its content.'''
        raise NotImplementedError()
    
    @property
    def location(self) -> str:
        '''Gets the location the content is focusing on.'''
        raise NotImplementedError()
    
    @location.setter
    def location(self, value : str) -> None:
        '''Sets the location the content is focusing on.'''
        raise NotImplementedError()
    
    @property
    def scenes(self) -> List[str]:
        '''Gets the scene of the photo content.'''
        raise NotImplementedError()
    
    @scenes.setter
    def scenes(self, value : List[str]) -> None:
        '''Sets the scene of the photo content.'''
        raise NotImplementedError()
    
    @property
    def subject_codes(self) -> List[str]:
        '''Gets one or more Subjects from the IPTC "Subject-NewsCodes" taxonomy to categorize the content.Each Subject is represented as a string of 8 digits in an unordered list.'''
        raise NotImplementedError()
    
    @subject_codes.setter
    def subject_codes(self, value : List[str]) -> None:
        '''Sets one or more Subjects from the IPTC "Subject-NewsCodes" taxonomy to categorize the content.Each Subject is represented as a string of 8 digits in an unordered list.'''
        raise NotImplementedError()
    

class XmpIptcExtensionPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the IPTC Extension XMP package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpIptcExtensionPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Sets string property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpArray) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpArray` .
        
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
    
    @property
    def additional_model_information(self) -> str:
        '''Gets the information about the ethnicity and other facets of the model(s) in a model-released image.'''
        raise NotImplementedError()
    
    @additional_model_information.setter
    def additional_model_information(self, value : str) -> None:
        '''Sets the information about the ethnicity and other facets of the model(s) in a model-released image.'''
        raise NotImplementedError()
    
    @property
    def organisation_in_image_codes(self) -> List[str]:
        '''Gets codes from a controlled vocabulary for identifying the organisations or companies which are featured in the image.'''
        raise NotImplementedError()
    
    @organisation_in_image_codes.setter
    def organisation_in_image_codes(self, value : List[str]) -> None:
        '''Sets codes from a controlled vocabulary for identifying the organisations or companies which are featured in the image.'''
        raise NotImplementedError()
    
    @property
    def organisation_in_image_names(self) -> List[str]:
        '''Gets names of the organisations or companies which are featured in the image.'''
        raise NotImplementedError()
    
    @organisation_in_image_names.setter
    def organisation_in_image_names(self, value : List[str]) -> None:
        '''Sets names of the organisations or companies which are featured in the image.'''
        raise NotImplementedError()
    
    @property
    def ages_of_models(self) -> List[int]:
        '''Gets ages of the human models at the time this image was taken in a model released image.'''
        raise NotImplementedError()
    
    @ages_of_models.setter
    def ages_of_models(self, value : List[int]) -> None:
        '''Sets ages of the human models at the time this image was taken in a model released image.'''
        raise NotImplementedError()
    
    @property
    def persons_in_image(self) -> List[str]:
        '''Gets names of the persons the content of the item is about.'''
        raise NotImplementedError()
    
    @persons_in_image.setter
    def persons_in_image(self, value : List[str]) -> None:
        '''Sets names of the persons the content of the item is about.'''
        raise NotImplementedError()
    
    @property
    def digital_image_guid(self) -> str:
        '''Gets the globally unique identifier for this digital image.'''
        raise NotImplementedError()
    
    @digital_image_guid.setter
    def digital_image_guid(self, value : str) -> None:
        '''Sets the globally unique identifier for this digital image.'''
        raise NotImplementedError()
    
    @property
    def digital_source_type(self) -> str:
        '''Gets the type of the source of this digital image.'''
        raise NotImplementedError()
    
    @digital_source_type.setter
    def digital_source_type(self, value : str) -> None:
        '''Sets the type of the source of this digital image.'''
        raise NotImplementedError()
    
    @property
    def event(self) -> groupdocs.metadata.standards.xmp.XmpLangAlt:
        '''Gets the description of the specific event at which the photo was taken.'''
        raise NotImplementedError()
    
    @event.setter
    def event(self, value : groupdocs.metadata.standards.xmp.XmpLangAlt) -> None:
        '''Sets the description of the specific event at which the photo was taken.'''
        raise NotImplementedError()
    
    @property
    def iptc_last_edited(self) -> Optional[datetime]:
        '''Gets the date and optionally time when any of the IPTC photo metadata fields has been last edited.'''
        raise NotImplementedError()
    
    @iptc_last_edited.setter
    def iptc_last_edited(self, value : Optional[datetime]) -> None:
        '''Sets the date and optionally time when any of the IPTC photo metadata fields has been last edited.'''
        raise NotImplementedError()
    
    @property
    def max_available_height(self) -> Optional[int]:
        '''Gets the maximum available height in pixels of the original photo from which this photo has been derived by downsizing.'''
        raise NotImplementedError()
    
    @max_available_height.setter
    def max_available_height(self, value : Optional[int]) -> None:
        '''Sets the maximum available height in pixels of the original photo from which this photo has been derived by downsizing.'''
        raise NotImplementedError()
    
    @property
    def max_available_width(self) -> Optional[int]:
        '''Gets the the maximum available width in pixels of the original photo from which this photo has been derived by downsizing.'''
        raise NotImplementedError()
    
    @max_available_width.setter
    def max_available_width(self, value : Optional[int]) -> None:
        '''Sets the the maximum available width in pixels of the original photo from which this photo has been derived by downsizing.'''
        raise NotImplementedError()
    

class XmpIptcIimPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the IPTC-IIM XMP package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpIptcIimPackage` class.'''
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
    
    @property
    def model_version(self) -> Optional[int]:
        '''Gets the binary number identifying the version of the Information'''
        raise NotImplementedError()
    
    @model_version.setter
    def model_version(self, value : Optional[int]) -> None:
        '''Sets the binary number identifying the version of the Information'''
        raise NotImplementedError()
    
    @property
    def destination(self) -> List[str]:
        '''Gets the destination. This DataSet is to accommodate some providers who require routing
        information above the appropriate OSI layers.'''
        raise NotImplementedError()
    
    @destination.setter
    def destination(self, value : List[str]) -> None:
        '''Sets the destination. This DataSet is to accommodate some providers who require routing
        information above the appropriate OSI layers.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> Optional[int]:
        '''Gets the binary number identifying the version of the Information'''
        raise NotImplementedError()
    
    @file_format.setter
    def file_format(self, value : Optional[int]) -> None:
        '''Sets the binary number identifying the version of the Information'''
        raise NotImplementedError()
    
    @property
    def file_format_version(self) -> Optional[int]:
        '''Gets the file format version.'''
        raise NotImplementedError()
    
    @file_format_version.setter
    def file_format_version(self, value : Optional[int]) -> None:
        '''Sets the file format version.'''
        raise NotImplementedError()
    
    @property
    def service_identifier(self) -> str:
        '''Gets the service identifier. Identifies the provider and product.'''
        raise NotImplementedError()
    
    @service_identifier.setter
    def service_identifier(self, value : str) -> None:
        '''Sets the service identifier. Identifies the provider and product.'''
        raise NotImplementedError()
    
    @property
    def envelope_number(self) -> str:
        '''Gets the envelope number.'''
        raise NotImplementedError()
    
    @envelope_number.setter
    def envelope_number(self, value : str) -> None:
        '''Sets the envelope number.'''
        raise NotImplementedError()
    
    @property
    def product_i_ds(self) -> List[str]:
        '''Gets the product identifiers.'''
        raise NotImplementedError()
    
    @product_i_ds.setter
    def product_i_ds(self, value : List[str]) -> None:
        '''Sets the product identifiers.'''
        raise NotImplementedError()
    
    @property
    def envelope_priority(self) -> Optional[int]:
        '''Gets the envelope handling priority.'''
        raise NotImplementedError()
    
    @envelope_priority.setter
    def envelope_priority(self, value : Optional[int]) -> None:
        '''Sets the envelope handling priority.'''
        raise NotImplementedError()
    
    @property
    def date_sent(self) -> Optional[datetime]:
        '''Gets the date the service sent the material.'''
        raise NotImplementedError()
    
    @date_sent.setter
    def date_sent(self, value : Optional[datetime]) -> None:
        '''Sets the date the service sent the material.'''
        raise NotImplementedError()
    
    @property
    def unique_name_of_object(self) -> str:
        '''Gets the unique name of the object.'''
        raise NotImplementedError()
    
    @unique_name_of_object.setter
    def unique_name_of_object(self, value : str) -> None:
        '''Sets the unique name of the object.'''
        raise NotImplementedError()
    
    @property
    def object_type_reference(self) -> str:
        '''Gets the object type reference. The Object Type is used to distinguish between different types of objects within the IIM.'''
        raise NotImplementedError()
    
    @object_type_reference.setter
    def object_type_reference(self, value : str) -> None:
        '''Sets the object type reference. The Object Type is used to distinguish between different types of objects within the IIM.'''
        raise NotImplementedError()
    
    @property
    def edit_status(self) -> str:
        '''Gets the status of the object data, according to the practice of the provider.'''
        raise NotImplementedError()
    
    @edit_status.setter
    def edit_status(self, value : str) -> None:
        '''Sets the status of the object data, according to the practice of the provider.'''
        raise NotImplementedError()
    
    @property
    def urgency(self) -> Optional[int]:
        '''Gets the editorial urgency of the content.'''
        raise NotImplementedError()
    
    @urgency.setter
    def urgency(self, value : Optional[int]) -> None:
        '''Sets the editorial urgency of the content.'''
        raise NotImplementedError()
    
    @property
    def category(self) -> str:
        '''Gets the subject of the object data in the opinion of the provider.'''
        raise NotImplementedError()
    
    @category.setter
    def category(self, value : str) -> None:
        '''Sets the subject of the object data in the opinion of the provider.'''
        raise NotImplementedError()
    
    @property
    def supplemental_categories(self) -> List[str]:
        '''Gets the supplemental categories.'''
        raise NotImplementedError()
    
    @supplemental_categories.setter
    def supplemental_categories(self, value : List[str]) -> None:
        '''Sets the supplemental categories.'''
        raise NotImplementedError()
    
    @property
    def fixture_identifier(self) -> str:
        '''Gets the object data that recurs often and predictably.'''
        raise NotImplementedError()
    
    @fixture_identifier.setter
    def fixture_identifier(self, value : str) -> None:
        '''Sets the object data that recurs often and predictably.'''
        raise NotImplementedError()
    
    @property
    def content_location_codes(self) -> List[str]:
        '''Gets the content location codes.'''
        raise NotImplementedError()
    
    @content_location_codes.setter
    def content_location_codes(self, value : List[str]) -> None:
        '''Sets the content location codes.'''
        raise NotImplementedError()
    
    @property
    def content_location_names(self) -> List[str]:
        '''Gets the content location names.'''
        raise NotImplementedError()
    
    @content_location_names.setter
    def content_location_names(self, value : List[str]) -> None:
        '''Sets the content location names.'''
        raise NotImplementedError()
    
    @property
    def release_date(self) -> Optional[datetime]:
        '''Gets the earliest date the provider intends the object to be used.'''
        raise NotImplementedError()
    
    @release_date.setter
    def release_date(self, value : Optional[datetime]) -> None:
        '''Sets the earliest date the provider intends the object to be used.'''
        raise NotImplementedError()
    
    @property
    def expiration_date(self) -> Optional[datetime]:
        '''Gets the latest date the provider or owner intends the object data to be used.'''
        raise NotImplementedError()
    
    @expiration_date.setter
    def expiration_date(self, value : Optional[datetime]) -> None:
        '''Sets the latest date the provider or owner intends the object data to be used.'''
        raise NotImplementedError()
    
    @property
    def action_advised(self) -> str:
        '''Gets the type of action that this object provides to a previous object.'''
        raise NotImplementedError()
    
    @action_advised.setter
    def action_advised(self, value : str) -> None:
        '''Sets the type of action that this object provides to a previous object.'''
        raise NotImplementedError()
    
    @property
    def reference_service(self) -> str:
        '''Gets the Service Identifier of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @reference_service.setter
    def reference_service(self, value : str) -> None:
        '''Sets the Service Identifier of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @property
    def reference_date(self) -> Optional[datetime]:
        '''Gets the date of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @reference_date.setter
    def reference_date(self, value : Optional[datetime]) -> None:
        '''Sets the date of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @property
    def reference_number(self) -> str:
        '''Gets the Envelope Number of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @reference_number.setter
    def reference_number(self, value : str) -> None:
        '''Sets the Envelope Number of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @property
    def digital_creation_date(self) -> Optional[datetime]:
        '''Gets the date the digital representation of the object data was created.'''
        raise NotImplementedError()
    
    @digital_creation_date.setter
    def digital_creation_date(self, value : Optional[datetime]) -> None:
        '''Sets the date the digital representation of the object data was created.'''
        raise NotImplementedError()
    
    @property
    def originating_program(self) -> str:
        '''Gets the type of program used to originate the object data.'''
        raise NotImplementedError()
    
    @originating_program.setter
    def originating_program(self, value : str) -> None:
        '''Sets the type of program used to originate the object data.'''
        raise NotImplementedError()
    
    @property
    def program_version(self) -> str:
        '''Gets the program version.'''
        raise NotImplementedError()
    
    @program_version.setter
    def program_version(self, value : str) -> None:
        '''Sets the program version.'''
        raise NotImplementedError()
    
    @property
    def image_type(self) -> str:
        '''Gets the type of the image.'''
        raise NotImplementedError()
    
    @image_type.setter
    def image_type(self, value : str) -> None:
        '''Sets the type of the image.'''
        raise NotImplementedError()
    
    @property
    def image_orientation(self) -> str:
        '''Gets the image orientation. Indicates the layout of the image area. Allowed values are P (for Portrait), L (for Landscape) and S (for Square).'''
        raise NotImplementedError()
    
    @image_orientation.setter
    def image_orientation(self, value : str) -> None:
        '''Sets the image orientation. Indicates the layout of the image area. Allowed values are P (for Portrait), L (for Landscape) and S (for Square).'''
        raise NotImplementedError()
    
    @property
    def language_identifier(self) -> str:
        '''Gets the language identifier according to the 2-letter codes of ISO 639:1988.'''
        raise NotImplementedError()
    
    @language_identifier.setter
    def language_identifier(self, value : str) -> None:
        '''Sets the language identifier according to the 2-letter codes of ISO 639:1988.'''
        raise NotImplementedError()
    

class XmpMediaManagementPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the XMP Media Management namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpMediaManagementPackage` class.'''
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
    
    @property
    def derived_from(self) -> groupdocs.metadata.standards.xmp.XmpResourceRef:
        '''Gets the reference to the resource from which this one is derived.'''
        raise NotImplementedError()
    
    @derived_from.setter
    def derived_from(self, value : groupdocs.metadata.standards.xmp.XmpResourceRef) -> None:
        '''Sets the reference to the resource from which this one is derived.'''
        raise NotImplementedError()
    
    @property
    def document_id(self) -> str:
        '''Gets the common identifier for all versions and renditions of the resource.'''
        raise NotImplementedError()
    
    @document_id.setter
    def document_id(self, value : str) -> None:
        '''Sets the common identifier for all versions and renditions of the resource.'''
        raise NotImplementedError()
    
    @property
    def history(self) -> List[groupdocs.metadata.standards.xmp.XmpResourceEvent]:
        '''Gets an array of high-level actions that resulted in this resource.'''
        raise NotImplementedError()
    
    @history.setter
    def history(self, value : List[groupdocs.metadata.standards.xmp.XmpResourceEvent]) -> None:
        '''Sets an array of high-level actions that resulted in this resource.'''
        raise NotImplementedError()
    
    @property
    def ingredients(self) -> List[groupdocs.metadata.standards.xmp.XmpResourceRef]:
        '''Gets the references to resources that were incorporated, by inclusion or reference, into this resource.'''
        raise NotImplementedError()
    
    @ingredients.setter
    def ingredients(self, value : List[groupdocs.metadata.standards.xmp.XmpResourceRef]) -> None:
        '''Sets the references to resources that were incorporated, by inclusion or reference, into this resource.'''
        raise NotImplementedError()
    
    @property
    def instance_id(self) -> str:
        '''Gets the identifier for a specific incarnation of a resource, updated each time the file is saved.'''
        raise NotImplementedError()
    
    @instance_id.setter
    def instance_id(self, value : str) -> None:
        '''Sets the identifier for a specific incarnation of a resource, updated each time the file is saved.'''
        raise NotImplementedError()
    
    @property
    def managed_from(self) -> groupdocs.metadata.standards.xmp.XmpResourceRef:
        '''Gets the reference to the document as it was prior to becoming managed.'''
        raise NotImplementedError()
    
    @managed_from.setter
    def managed_from(self, value : groupdocs.metadata.standards.xmp.XmpResourceRef) -> None:
        '''Sets the reference to the document as it was prior to becoming managed.'''
        raise NotImplementedError()
    
    @property
    def manager(self) -> str:
        '''Gets the name of the asset management system that manages this resource.'''
        raise NotImplementedError()
    
    @manager.setter
    def manager(self, value : str) -> None:
        '''Sets the name of the asset management system that manages this resource.'''
        raise NotImplementedError()
    
    @property
    def manage_to(self) -> str:
        '''Gets the URI identifying the managed resource to the asset management system'''
        raise NotImplementedError()
    
    @manage_to.setter
    def manage_to(self, value : str) -> None:
        '''Sets the URI identifying the managed resource to the asset management system'''
        raise NotImplementedError()
    
    @property
    def manage_ui(self) -> str:
        '''Gets the URI that can be used to access information about the managed resource through a web browser.'''
        raise NotImplementedError()
    
    @manage_ui.setter
    def manage_ui(self, value : str) -> None:
        '''Sets the URI that can be used to access information about the managed resource through a web browser.'''
        raise NotImplementedError()
    
    @property
    def manager_variant(self) -> str:
        '''Gets the particular variant of the asset management system.'''
        raise NotImplementedError()
    
    @manager_variant.setter
    def manager_variant(self, value : str) -> None:
        '''Sets the particular variant of the asset management system.'''
        raise NotImplementedError()
    
    @property
    def original_document_id(self) -> str:
        '''Gets the common identifier for the original resource from which the current resource is derived.'''
        raise NotImplementedError()
    
    @original_document_id.setter
    def original_document_id(self, value : str) -> None:
        '''Sets the common identifier for the original resource from which the current resource is derived.'''
        raise NotImplementedError()
    
    @property
    def rendition_class(self) -> str:
        '''Gets the rendition class name for this resource.'''
        raise NotImplementedError()
    
    @rendition_class.setter
    def rendition_class(self, value : str) -> None:
        '''Sets the rendition class name for this resource.'''
        raise NotImplementedError()
    
    @property
    def rendition_params(self) -> str:
        '''Gets the value that is used to provide additional rendition parameters
        that are too complex or verbose to encode in xmpMM:RenditionClass.'''
        raise NotImplementedError()
    
    @rendition_params.setter
    def rendition_params(self, value : str) -> None:
        '''Sets the value that is used to provide additional rendition parameters
        that are too complex or verbose to encode in xmpMM:RenditionClass.'''
        raise NotImplementedError()
    
    @property
    def version_id(self) -> str:
        '''Gets the document version identifier for this resource.'''
        raise NotImplementedError()
    
    @version_id.setter
    def version_id(self, value : str) -> None:
        '''Sets the document version identifier for this resource.'''
        raise NotImplementedError()
    
    @property
    def versions(self) -> List[groupdocs.metadata.standards.xmp.XmpVersion]:
        '''Gets the version history associated with this resource.'''
        raise NotImplementedError()
    
    @versions.setter
    def versions(self, value : List[groupdocs.metadata.standards.xmp.XmpVersion]) -> None:
        '''Sets the version history associated with this resource.'''
        raise NotImplementedError()
    

class XmpPagedTextPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents the XMP Paged-Text package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpPagedTextPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : str) -> None:
        '''Sets string property.
        
        :param name: XMP metadata property name.
        :param value: XMP metadata property value.'''
        raise NotImplementedError()
    
    @overload
    def set(self, name : str, value : groupdocs.metadata.standards.xmp.XmpArray) -> None:
        '''Sets the value inherited from :py:class:`groupdocs.metadata.standards.xmp.XmpArray` .
        
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
    
    @property
    def colorants(self) -> List[groupdocs.metadata.standards.xmp.XmpColorantBase]:
        '''Gets an ordered array of colorants (swatches) that are used in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @colorants.setter
    def colorants(self, value : List[groupdocs.metadata.standards.xmp.XmpColorantBase]) -> None:
        '''Sets an ordered array of colorants (swatches) that are used in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @property
    def fonts(self) -> List[groupdocs.metadata.standards.xmp.XmpFont]:
        '''Gets an unordered array of fonts that are used in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @fonts.setter
    def fonts(self, value : List[groupdocs.metadata.standards.xmp.XmpFont]) -> None:
        '''Sets an unordered array of fonts that are used in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @property
    def max_page_size(self) -> groupdocs.metadata.standards.xmp.XmpDimensions:
        '''Gets the size of the largest page in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @max_page_size.setter
    def max_page_size(self, value : groupdocs.metadata.standards.xmp.XmpDimensions) -> None:
        '''Sets the size of the largest page in the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @property
    def number_of_pages(self) -> Optional[int]:
        '''Gets the number of pages in the document.'''
        raise NotImplementedError()
    
    @number_of_pages.setter
    def number_of_pages(self, value : Optional[int]) -> None:
        '''Sets the number of pages in the document.'''
        raise NotImplementedError()
    
    @property
    def plate_names(self) -> List[str]:
        '''Gets or set an ordered array of plate names that are needed to print the document (including any in contained documents).'''
        raise NotImplementedError()
    
    @plate_names.setter
    def plate_names(self, value : List[str]) -> None:
        '''Set an ordered array of plate names that are needed to print the document (including any in contained documents).'''
        raise NotImplementedError()
    

class XmpPdfPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Specifies properties used with Adobe PDF documents.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpPdfPackage` class.'''
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
    
    @property
    def keywords(self) -> str:
        '''Gets the keywords.'''
        raise NotImplementedError()
    
    @keywords.setter
    def keywords(self, value : str) -> None:
        '''Sets the keywords.'''
        raise NotImplementedError()
    
    @property
    def pdf_version(self) -> str:
        '''Gets the PDF file version. For example, 1.0, 1.3 and so on.'''
        raise NotImplementedError()
    
    @pdf_version.setter
    def pdf_version(self, value : str) -> None:
        '''Sets the PDF file version. For example, 1.0, 1.3 and so on.'''
        raise NotImplementedError()
    
    @property
    def producer(self) -> str:
        '''Gets the name of the tool that created the PDF document.'''
        raise NotImplementedError()
    
    @producer.setter
    def producer(self, value : str) -> None:
        '''Sets the name of the tool that created the PDF document.'''
        raise NotImplementedError()
    
    @property
    def is_trapped(self) -> Optional[bool]:
        '''Gets a value indicating whether the document has been trapped.'''
        raise NotImplementedError()
    
    @is_trapped.setter
    def is_trapped(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether the document has been trapped.'''
        raise NotImplementedError()
    

class XmpPhotoshopPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents Adobe Photoshop namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopPackage` class.'''
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
    
    @property
    def authors_position(self) -> str:
        '''Gets the by-line title.'''
        raise NotImplementedError()
    
    @authors_position.setter
    def authors_position(self, value : str) -> None:
        '''Sets the by-line title.'''
        raise NotImplementedError()
    
    @property
    def caption_writer(self) -> str:
        '''Gets the writer/editor.'''
        raise NotImplementedError()
    
    @caption_writer.setter
    def caption_writer(self, value : str) -> None:
        '''Sets the writer/editor.'''
        raise NotImplementedError()
    
    @property
    def category(self) -> str:
        '''Gets the category. Limited to 3 7-bit ASCII characters.'''
        raise NotImplementedError()
    
    @category.setter
    def category(self, value : str) -> None:
        '''Sets the category. Limited to 3 7-bit ASCII characters.'''
        raise NotImplementedError()
    
    @property
    def city(self) -> str:
        '''Gets the city.'''
        raise NotImplementedError()
    
    @city.setter
    def city(self, value : str) -> None:
        '''Sets the city.'''
        raise NotImplementedError()
    
    @property
    def color_mode(self) -> Optional[groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopColorMode]:
        '''Gets the color mode.'''
        raise NotImplementedError()
    
    @color_mode.setter
    def color_mode(self, value : Optional[groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopColorMode]) -> None:
        '''Sets the color mode.'''
        raise NotImplementedError()
    
    @property
    def country(self) -> str:
        '''Gets the country.'''
        raise NotImplementedError()
    
    @country.setter
    def country(self, value : str) -> None:
        '''Sets the country.'''
        raise NotImplementedError()
    
    @property
    def credit(self) -> str:
        '''Gets the credit.'''
        raise NotImplementedError()
    
    @credit.setter
    def credit(self, value : str) -> None:
        '''Sets the credit.'''
        raise NotImplementedError()
    
    @property
    def date_created(self) -> Optional[datetime]:
        '''Gets the date the intellectual content of the document was created.'''
        raise NotImplementedError()
    
    @date_created.setter
    def date_created(self, value : Optional[datetime]) -> None:
        '''Sets the date the intellectual content of the document was created.'''
        raise NotImplementedError()
    
    @property
    def headline(self) -> str:
        '''Gets the headline.'''
        raise NotImplementedError()
    
    @headline.setter
    def headline(self, value : str) -> None:
        '''Sets the headline.'''
        raise NotImplementedError()
    
    @property
    def history(self) -> str:
        '''Gets the history that appears in the FileInfo panel, if activated in the application preferences.'''
        raise NotImplementedError()
    
    @history.setter
    def history(self, value : str) -> None:
        '''Sets the history that appears in the FileInfo panel, if activated in the application preferences.'''
        raise NotImplementedError()
    
    @property
    def icc_profile(self) -> str:
        '''Gets the color profile, such as AppleRGB, AdobeRGB1998.'''
        raise NotImplementedError()
    
    @icc_profile.setter
    def icc_profile(self, value : str) -> None:
        '''Sets the color profile, such as AppleRGB, AdobeRGB1998.'''
        raise NotImplementedError()
    
    @property
    def instructions(self) -> str:
        '''Gets the special instructions.'''
        raise NotImplementedError()
    
    @instructions.setter
    def instructions(self, value : str) -> None:
        '''Sets the special instructions.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> str:
        '''Gets the source.'''
        raise NotImplementedError()
    
    @source.setter
    def source(self, value : str) -> None:
        '''Sets the source.'''
        raise NotImplementedError()
    
    @property
    def state(self) -> str:
        '''Gets the province/state.'''
        raise NotImplementedError()
    
    @state.setter
    def state(self, value : str) -> None:
        '''Sets the province/state.'''
        raise NotImplementedError()
    
    @property
    def supplemental_categories(self) -> List[str]:
        '''Gets the supplemental categories.'''
        raise NotImplementedError()
    
    @supplemental_categories.setter
    def supplemental_categories(self, value : List[str]) -> None:
        '''Sets the supplemental categories.'''
        raise NotImplementedError()
    
    @property
    def transmission_reference(self) -> str:
        '''Gets the original transmission reference.'''
        raise NotImplementedError()
    
    @transmission_reference.setter
    def transmission_reference(self, value : str) -> None:
        '''Sets the original transmission reference.'''
        raise NotImplementedError()
    
    @property
    def urgency(self) -> Optional[int]:
        '''Gets the urgency.'''
        raise NotImplementedError()
    
    @urgency.setter
    def urgency(self, value : Optional[int]) -> None:
        '''Sets the urgency.'''
        raise NotImplementedError()
    
    @property
    def URGENCY_MAX(self) -> int:
        '''Urgency max value.'''
        raise NotImplementedError()

    @property
    def URGENCY_MIN(self) -> int:
        '''Urgency min value.'''
        raise NotImplementedError()


class XmpRightsManagementPackage(groupdocs.metadata.standards.xmp.XmpPackage):
    '''Represents XMP Rights Management namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpRightsManagementPackage` class.'''
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
    
    @property
    def certificate(self) -> str:
        '''Gets the Web URL for a rights management certificate.'''
        raise NotImplementedError()
    
    @certificate.setter
    def certificate(self, value : str) -> None:
        '''Sets the Web URL for a rights management certificate.'''
        raise NotImplementedError()
    
    @property
    def marked(self) -> Optional[bool]:
        '''Gets a value indicating whether this is a rights-managed resource.'''
        raise NotImplementedError()
    
    @marked.setter
    def marked(self, value : Optional[bool]) -> None:
        '''Sets a value indicating whether this is a rights-managed resource.'''
        raise NotImplementedError()
    
    @property
    def owners(self) -> List[str]:
        '''Gets the legal owners.'''
        raise NotImplementedError()
    
    @owners.setter
    def owners(self, value : List[str]) -> None:
        '''Sets the legal owners.'''
        raise NotImplementedError()
    
    @property
    def usage_terms(self) -> groupdocs.metadata.standards.xmp.XmpLangAlt:
        '''Gets the instructions on how the resource can be legally used, given in a variety of languages.'''
        raise NotImplementedError()
    
    @usage_terms.setter
    def usage_terms(self, value : groupdocs.metadata.standards.xmp.XmpLangAlt) -> None:
        '''Sets the instructions on how the resource can be legally used, given in a variety of languages.'''
        raise NotImplementedError()
    
    @property
    def web_statement(self) -> str:
        '''Gets the Web URL for a statement of the ownership and usage rights for this resource.'''
        raise NotImplementedError()
    
    @web_statement.setter
    def web_statement(self, value : str) -> None:
        '''Sets the Web URL for a statement of the ownership and usage rights for this resource.'''
        raise NotImplementedError()
    

class XmpTimeFormat:
    '''Represents time format in :py:class:`groupdocs.metadata.standards.xmp.XmpTimecode`.'''
    
    @property
    def timecode24(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 24Timecode.'''
        raise NotImplementedError()

    @property
    def timecode25(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 25Timecode.'''
        raise NotImplementedError()

    @property
    def drop_timecode2997(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 2997DropTimecode.'''
        raise NotImplementedError()

    @property
    def non_drop_timecode2997(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 2997NonDropTimecode.'''
        raise NotImplementedError()

    @property
    def timecode30(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 30Timecode.'''
        raise NotImplementedError()

    @property
    def timecode50(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 50Timecode.'''
        raise NotImplementedError()

    @property
    def drop_timecode5994(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 5994DropTimecode.'''
        raise NotImplementedError()

    @property
    def non_drop_timecode5994(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 5994NonDropTimecode.'''
        raise NotImplementedError()

    @property
    def timecode60(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 60Timecode.'''
        raise NotImplementedError()

    @property
    def timecode23976(self) -> groupdocs.metadata.standards.xmp.schemes.XmpTimeFormat:
        '''Gets 23976Timecode.'''
        raise NotImplementedError()


class XmpWhiteBalance:
    '''Represents the White Balance setting in :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage`.'''
    
    @property
    def as_shot(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: As Shot.'''
        raise NotImplementedError()

    @property
    def auto(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Auto.'''
        raise NotImplementedError()

    @property
    def cloudy(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Cloudy.'''
        raise NotImplementedError()

    @property
    def custom(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Custom.'''
        raise NotImplementedError()

    @property
    def daylight(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Daylight.'''
        raise NotImplementedError()

    @property
    def flash(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Flash.'''
        raise NotImplementedError()

    @property
    def fluorescent(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Fluorescent.'''
        raise NotImplementedError()

    @property
    def shade(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Shade.'''
        raise NotImplementedError()

    @property
    def tungsten(self) -> groupdocs.metadata.standards.xmp.schemes.XmpWhiteBalance:
        '''White balance: Tungsten.'''
        raise NotImplementedError()


class XmpCropUnit:
    '''Represent a unit for CropWidth and CropHeight in :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpCameraRawPackage`.'''
    
    PIXELS : XmpCropUnit
    '''Pixels units.'''
    INCHES : XmpCropUnit
    '''Inches units.'''
    CM : XmpCropUnit
    '''Centimeters units.'''

class XmpPhotoshopColorMode:
    '''Represents a color mode in :py:class:`groupdocs.metadata.standards.xmp.schemes.XmpPhotoshopPackage`.'''
    
    BITMAP : XmpPhotoshopColorMode
    '''The bitmap color mode.'''
    GRAY_SCALE : XmpPhotoshopColorMode
    '''The gray scale color mode.'''
    INDEXED_COLOR : XmpPhotoshopColorMode
    '''The indexed color.'''
    RGB : XmpPhotoshopColorMode
    '''The RGB color mode.'''
    CMYK : XmpPhotoshopColorMode
    '''The CMYK color mode.'''
    MULTI_CHANNEL : XmpPhotoshopColorMode
    '''The multi-channel color mode.'''
    DUOTONE : XmpPhotoshopColorMode
    '''The duo-tone color mode.'''
    LAB_COLOR : XmpPhotoshopColorMode
    '''The LAB color mode.'''

