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

class OpenTypeBaseNameRecord(groupdocs.metadata.common.CustomPackage):
    '''Represents the base OpenType Name table record class.'''
    
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
    def name_id(self) -> groupdocs.metadata.formats.font.OpenTypeName:
        '''Gets the name identifier.'''
        raise NotImplementedError()
    
    @property
    def platform(self) -> groupdocs.metadata.formats.font.OpenTypePlatform:
        '''Gets the platform identifier.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the string value of record.'''
        raise NotImplementedError()
    

class OpenTypeFont(groupdocs.metadata.common.CustomPackage):
    '''Represents a single font extracted from a file.'''
    
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
    def sfnt_version(self) -> groupdocs.metadata.formats.font.OpenTypeVersion:
        '''Gets the header SFNT version.'''
        raise NotImplementedError()
    
    @property
    def major_version(self) -> int:
        '''Gets the header major version.'''
        raise NotImplementedError()
    
    @property
    def minor_version(self) -> int:
        '''Gets the header minor version.'''
        raise NotImplementedError()
    
    @property
    def font_revision(self) -> float:
        '''Gets the font revision.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.font.OpenTypeFlags:
        '''Gets the header flags.'''
        raise NotImplementedError()
    
    @property
    def created(self) -> datetime:
        '''Gets the created date.'''
        raise NotImplementedError()
    
    @property
    def modified(self) -> datetime:
        '''Gets the modified date.'''
        raise NotImplementedError()
    
    @property
    def glyph_bounds(self) -> groupdocs.metadata.common.Rectangle:
        '''Gets the glyph bounds.'''
        raise NotImplementedError()
    
    @property
    def style(self) -> groupdocs.metadata.formats.font.OpenTypeStyles:
        '''Gets the font style.'''
        raise NotImplementedError()
    
    @property
    def direction_hint(self) -> groupdocs.metadata.formats.font.OpenTypeDirectionHint:
        '''Gets the direction hint.'''
        raise NotImplementedError()
    
    @property
    def names(self) -> List[groupdocs.metadata.formats.font.OpenTypeBaseNameRecord]:
        '''Gets the name records.'''
        raise NotImplementedError()
    
    @property
    def font_family_name(self) -> str:
        '''Gets the name of the font family.'''
        raise NotImplementedError()
    
    @property
    def font_subfamily_name(self) -> str:
        '''Gets the name of the font subfamily.'''
        raise NotImplementedError()
    
    @property
    def full_font_name(self) -> str:
        '''Gets the full name of the font.'''
        raise NotImplementedError()
    
    @property
    def typographic_family(self) -> str:
        '''Gets the typographic family.'''
        raise NotImplementedError()
    
    @property
    def typographic_subfamily(self) -> str:
        '''Gets the typographic subfamily.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> groupdocs.metadata.formats.font.OpenTypeWeight:
        '''Gets the font weight.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> groupdocs.metadata.formats.font.OpenTypeWidth:
        '''Gets the font width.'''
        raise NotImplementedError()
    
    @property
    def embedding_licensing_rights(self) -> groupdocs.metadata.formats.font.OpenTypeLicensingRights:
        '''Gets the embedding licensing rights type.'''
        raise NotImplementedError()
    

class OpenTypeMacintoshNameRecord(OpenTypeBaseNameRecord):
    '''Represents the Name record table value for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.MACINTOSH` platform.'''
    
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
    def name_id(self) -> groupdocs.metadata.formats.font.OpenTypeName:
        '''Gets the name identifier.'''
        raise NotImplementedError()
    
    @property
    def platform(self) -> groupdocs.metadata.formats.font.OpenTypePlatform:
        '''Gets the platform identifier.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the string value of record.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> groupdocs.metadata.formats.font.OpenTypeMacintoshEncoding:
        '''Gets the encoding identifier.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> groupdocs.metadata.formats.font.OpenTypeMacintoshLanguage:
        '''Gets the language identifier.'''
        raise NotImplementedError()
    

class OpenTypePackage(groupdocs.metadata.common.CustomPackage):
    '''Represents an OpenType font metadata package.'''
    
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
    def fonts(self) -> List[groupdocs.metadata.formats.font.OpenTypeFont]:
        '''Gets an array of the fonts extracted from the file.'''
        raise NotImplementedError()
    

class OpenTypeRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an OpenType font file.'''
    
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
    def file_type(self) -> groupdocs.metadata.common.FileTypePackage:
        '''Gets the file type metadata package.'''
        raise NotImplementedError()
    
    @property
    def open_type_package(self) -> groupdocs.metadata.formats.font.OpenTypePackage:
        '''Gets the OpenType metadata package.'''
        raise NotImplementedError()
    
    @property
    def digital_signature_package(self) -> groupdocs.metadata.standards.pkcs.CmsPackage:
        '''Gets the digital signature metadata package.'''
        raise NotImplementedError()
    

class OpenTypeUnicodeNameRecord(OpenTypeBaseNameRecord):
    '''Represents the Name record table value for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.UNICODE` platform.'''
    
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
    def name_id(self) -> groupdocs.metadata.formats.font.OpenTypeName:
        '''Gets the name identifier.'''
        raise NotImplementedError()
    
    @property
    def platform(self) -> groupdocs.metadata.formats.font.OpenTypePlatform:
        '''Gets the platform identifier.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the string value of record.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> groupdocs.metadata.formats.font.OpenTypeUnicodeEncoding:
        '''Gets the encoding identifier.'''
        raise NotImplementedError()
    

class OpenTypeWindowsNameRecord(OpenTypeBaseNameRecord):
    '''Represents the Name record table value for :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.WINDOWS` platform.'''
    
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
    def name_id(self) -> groupdocs.metadata.formats.font.OpenTypeName:
        '''Gets the name identifier.'''
        raise NotImplementedError()
    
    @property
    def platform(self) -> groupdocs.metadata.formats.font.OpenTypePlatform:
        '''Gets the platform identifier.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the string value of record.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> groupdocs.metadata.formats.font.OpenTypeWindowsEncoding:
        '''Gets the encoding identifier.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> groupdocs.metadata.formats.font.OpenTypeWindowsLanguage:
        '''Gets the language identifier.'''
        raise NotImplementedError()
    

class OpenTypeDigitalSignatureFlags:
    '''Represents OpenType font digital signature flags.'''
    
    NONE : OpenTypeDigitalSignatureFlags
    '''Undefined flag.'''
    CANNOT_BE_RESIGNED : OpenTypeDigitalSignatureFlags
    '''Cannot be resigned.'''

class OpenTypeDirectionHint:
    '''Represents the OpenType font direction.'''
    
    FULLY_MIXED : OpenTypeDirectionHint
    '''Fully mixed directional glyphs.'''
    ONLY_LEFT_TO_RIGHT : OpenTypeDirectionHint
    '''Only strongly left to right.'''
    LEFT_TO_RIGHT_AND_NEUTRALS : OpenTypeDirectionHint
    '''Like :py:attr:`groupdocs.metadata.formats.font.OpenTypeDirectionHint.ONLY_LEFT_TO_RIGHT` but also contains neutrals.'''
    ONLY_RIGHT_TO_LEFT : OpenTypeDirectionHint
    '''Only strongly right to left.'''
    RIGHT_TO_LEFT_AND_NEUTRALS : OpenTypeDirectionHint
    '''Like :py:attr:`groupdocs.metadata.formats.font.OpenTypeDirectionHint.ONLY_RIGHT_TO_LEFT` but also contains neutrals.'''

class OpenTypeFlags:
    '''Represents OpenType font header flags.'''
    
    NONE : OpenTypeFlags
    '''Undefined, no flags.'''
    BASELINE_AT_Y0 : OpenTypeFlags
    '''Baseline for font at y=0.'''
    LEFT_SIDEBEARING_AT_X0 : OpenTypeFlags
    '''Left sidebearing point at x=0 (relevant only for TrueType rasterizers).'''
    DEPEND_ON_POINT_SIZE : OpenTypeFlags
    '''Instructions may depend on point size.'''
    FORCE_TO_INTEGER : OpenTypeFlags
    '''Force ppem to integer values for all internal scaler math; may use fractional ppem sizes if this bit is clear.'''
    ALTER_ADVANCE_WIDTH : OpenTypeFlags
    '''Instructions may alter advance width (the advance widths might not scale linearly).'''
    LOSSLESS : OpenTypeFlags
    '''Font data is “lossless” as a result of having been subjected to optimizing transformation and/or compression.'''
    CONVERTED : OpenTypeFlags
    '''Font converted (produce compatible metrics).'''
    OPTIMIZED : OpenTypeFlags
    '''Font optimized for ClearType™.'''
    RESORT : OpenTypeFlags
    '''Last Resort font.'''

class OpenTypeIsoEncoding:
    '''Represents encoding for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.ISO` platform.'''
    
    ASCII_7_BIT : OpenTypeIsoEncoding
    '''The 7-bit ASCII encoding.'''
    ISO10646 : OpenTypeIsoEncoding
    '''The ISO 10646 encoding.'''
    ISO8859 : OpenTypeIsoEncoding
    '''The ISO 8859-1 encoding.'''

class OpenTypeLicensingRights:
    '''Indicates font embedding licensing rights for the font.'''
    
    NONE : OpenTypeLicensingRights
    '''The undefined licensing rights.'''
    USAGE_PERMISSIONS_MASK : OpenTypeLicensingRights
    '''Usage permissions mask.'''
    INSTALLABLE_EMBEDDING : OpenTypeLicensingRights
    '''Installable embedding.
    The font may be embedded, and may be permanently installed for use on a remote systems, or for use by other users.'''
    RESTRICTED_LICENSE_EMBEDDING : OpenTypeLicensingRights
    '''Restricted License embedding.
    The font must not be modified, embedded or exchanged in any manner without first obtaining explicit permission of the legal owner.'''
    PREVIEW_AND_PRINT_EMBEDDING : OpenTypeLicensingRights
    '''Preview and Print embedding.
    The font may be embedded, and may be temporarily loaded on other systems for purposes of viewing or printing the document.
    Documents containing Preview & Print fonts must be opened “read-only”; no edits can be applied to the document.'''
    EDITABLE_EMBEDDING : OpenTypeLicensingRights
    '''Editable embedding.
    The font may be embedded, and may be temporarily loaded on other systems.
    As with Preview and Print embedding, documents containing Editable fonts may be opened for reading.
    In addition, editing is permitted, including ability to format new text using the embedded font, and changes may be saved.'''
    NO_SUBSETTING : OpenTypeLicensingRights
    '''No subsetting.
    When this bit is set, the font may not be subsetted prior to embedding. Other embedding restrictions specified in bits 0 to 3 and bit 9 also apply.'''
    BITMAP_EMBEDDING_ONLY : OpenTypeLicensingRights
    '''Bitmap embedding only.
    When this bit is set, only bitmaps contained in the font may be embedded. No outline data may be embedded.
    If there are no bitmaps available in the font, then the font is considered unembeddable and the embedding services will fail.
    Other embedding restrictions specified in bits 0-3 and 8 also apply.'''

class OpenTypeMacintoshEncoding:
    '''Represents encoding for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.MACINTOSH` platform.'''
    
    DEFAULT_SEMANTICS : OpenTypeMacintoshEncoding
    '''Default semantics.'''
    VERSION_11_SEMANTICS : OpenTypeMacintoshEncoding
    '''Version 1.1 semantics.'''
    ISO_106461993_SEMANTICS : OpenTypeMacintoshEncoding
    '''ISO 10646 1993 semantics (deprecated).'''
    UNICODE_20_BMP_ONLY : OpenTypeMacintoshEncoding
    '''Unicode 2.0 or later semantics (BMP only).'''
    UNICODE_20_NON_BMP : OpenTypeMacintoshEncoding
    '''Unicode 2.0 or later semantics (non-BMP characters allowed).'''
    UNICODE_VARIATION_SEQUENCES : OpenTypeMacintoshEncoding
    '''Unicode Variation Sequences.'''
    FULL_UNICODE_COVERAGE : OpenTypeMacintoshEncoding
    '''Full Unicode coverage.'''

class OpenTypeMacintoshLanguage:
    '''Represents language enum for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.MACINTOSH` platform.'''
    
    ENGLISH : OpenTypeMacintoshLanguage
    '''The english language.'''
    FRENCH : OpenTypeMacintoshLanguage
    '''The french language.'''
    GERMAN : OpenTypeMacintoshLanguage
    '''The german language.'''
    ITALIAN : OpenTypeMacintoshLanguage
    '''The italian language.'''
    DUTCH : OpenTypeMacintoshLanguage
    '''The dutch language.'''
    SWEDISH : OpenTypeMacintoshLanguage
    '''The swedish language.'''
    SPANISH : OpenTypeMacintoshLanguage
    '''The spanish language.'''
    DANISH : OpenTypeMacintoshLanguage
    '''The danish language.'''
    PORTUGUESE : OpenTypeMacintoshLanguage
    '''The portuguese language.'''
    NORWEGIAN : OpenTypeMacintoshLanguage
    '''The norwegian language.'''
    HEBREW : OpenTypeMacintoshLanguage
    '''The hebrew language.'''
    JAPANESE : OpenTypeMacintoshLanguage
    '''The japanese language.'''
    ARABIC : OpenTypeMacintoshLanguage
    '''The arabic language.'''
    FINNISH : OpenTypeMacintoshLanguage
    '''The finnish language.'''
    GREEK : OpenTypeMacintoshLanguage
    '''The greek language.'''
    ICELANDIC : OpenTypeMacintoshLanguage
    '''The icelandic language.'''
    MALTESE : OpenTypeMacintoshLanguage
    '''The maltese language.'''
    TURKISH : OpenTypeMacintoshLanguage
    '''The turkish language.'''
    CROATIAN : OpenTypeMacintoshLanguage
    '''The croatian language.'''
    CHINESE_TRADITIONAL : OpenTypeMacintoshLanguage
    '''The chinese traditional language.'''
    URDU : OpenTypeMacintoshLanguage
    '''The urdu language.'''
    HINDI : OpenTypeMacintoshLanguage
    '''The hindi language.'''
    THAI : OpenTypeMacintoshLanguage
    '''The thai language.'''
    KOREAN : OpenTypeMacintoshLanguage
    '''The korean language.'''
    LITHUANIAN : OpenTypeMacintoshLanguage
    '''The lithuanian language.'''
    POLISH : OpenTypeMacintoshLanguage
    '''The polish language.'''
    HUNGARIAN : OpenTypeMacintoshLanguage
    '''The hungarian language.'''
    ESTONIAN : OpenTypeMacintoshLanguage
    '''The estonian language.'''
    LATVIAN : OpenTypeMacintoshLanguage
    '''The latvian language.'''
    SAMI : OpenTypeMacintoshLanguage
    '''The sami language.'''
    FAROESE : OpenTypeMacintoshLanguage
    '''The faroese language.'''
    FARSI_PERSIAN : OpenTypeMacintoshLanguage
    '''The farsi persian language.'''
    RUSSIAN : OpenTypeMacintoshLanguage
    '''The russian language.'''
    CHINESE_SIMPLIFIED : OpenTypeMacintoshLanguage
    '''The chinese simplifie language.'''
    FLEMISH : OpenTypeMacintoshLanguage
    '''The flemish language.'''
    IRISH_GAELIC : OpenTypeMacintoshLanguage
    '''The irish gaelic language.'''
    ALBANIAN : OpenTypeMacintoshLanguage
    '''The albanian language.'''
    ROMANIAN : OpenTypeMacintoshLanguage
    '''The romanian language.'''
    CZECH : OpenTypeMacintoshLanguage
    '''The czech language.'''
    SLOVAK : OpenTypeMacintoshLanguage
    '''The slovak language.'''
    SLOVENIAN : OpenTypeMacintoshLanguage
    '''The slovenian language.'''
    YIDDISH : OpenTypeMacintoshLanguage
    '''The yiddish language.'''
    SERBIAN : OpenTypeMacintoshLanguage
    '''The serbian language.'''
    MACEDONIAN : OpenTypeMacintoshLanguage
    '''The macedonian language.'''
    BULGARIAN : OpenTypeMacintoshLanguage
    '''The bulgarian language.'''
    UKRAINIAN : OpenTypeMacintoshLanguage
    '''The ukrainian language.'''
    BYELORUSSIAN : OpenTypeMacintoshLanguage
    '''The byelorussian language.'''
    UZBEK : OpenTypeMacintoshLanguage
    '''The uzbek language.'''
    KAZAKH : OpenTypeMacintoshLanguage
    '''The kazakh language.'''
    AZERBAIJANI_CYRILLIC : OpenTypeMacintoshLanguage
    '''The azerbaijani cyrillic language.'''
    AZERBAIJANI_ARABIC : OpenTypeMacintoshLanguage
    '''The azerbaijani arabic language.'''
    ARMENIAN : OpenTypeMacintoshLanguage
    '''The armenian language.'''
    GEORGIAN : OpenTypeMacintoshLanguage
    '''The georgian language.'''
    MOLDAVIAN : OpenTypeMacintoshLanguage
    '''The moldavian language.'''
    KIRGHIZ : OpenTypeMacintoshLanguage
    '''The kirghiz language.'''
    TAJIKI : OpenTypeMacintoshLanguage
    '''The tajiki language.'''
    TURKMEN : OpenTypeMacintoshLanguage
    '''The turkmen language.'''
    MONGOLIAN_MONGOLIAN : OpenTypeMacintoshLanguage
    '''The mongolian mongolian language.'''
    MONGOLIAN_CYRILLIC : OpenTypeMacintoshLanguage
    '''The mongolian cyrillic language.'''
    PASHTO : OpenTypeMacintoshLanguage
    '''The pashto language.'''
    KURDISH : OpenTypeMacintoshLanguage
    '''The kurdish language.'''
    KASHMIRI : OpenTypeMacintoshLanguage
    '''The kashmiri language.'''
    SINDHI : OpenTypeMacintoshLanguage
    '''The sindhi language.'''
    TIBETAN : OpenTypeMacintoshLanguage
    '''The tibetan language.'''
    NEPALI : OpenTypeMacintoshLanguage
    '''The nepali language.'''
    SANSKRIT : OpenTypeMacintoshLanguage
    '''The sanskrit language.'''
    MARATHI : OpenTypeMacintoshLanguage
    '''The marathi language.'''
    BENGALI : OpenTypeMacintoshLanguage
    '''The bengali language.'''
    ASSAMESE : OpenTypeMacintoshLanguage
    '''The assamese language.'''
    GUJARATI : OpenTypeMacintoshLanguage
    '''The gujarati language.'''
    PUNJABI : OpenTypeMacintoshLanguage
    '''The punjabi language.'''
    ORIYA : OpenTypeMacintoshLanguage
    '''The oriya language.'''
    MALAYALAM : OpenTypeMacintoshLanguage
    '''The malayalam language.'''
    KANNADA : OpenTypeMacintoshLanguage
    '''The kannada language.'''
    TAMIL : OpenTypeMacintoshLanguage
    '''The tamil language.'''
    TELUGU : OpenTypeMacintoshLanguage
    '''The telugu language.'''
    SINHALESE : OpenTypeMacintoshLanguage
    '''The sinhalese language.'''
    BURMESE : OpenTypeMacintoshLanguage
    '''The burmese language.'''
    KHMER : OpenTypeMacintoshLanguage
    '''The khmer language.'''
    LAO : OpenTypeMacintoshLanguage
    '''The lao language.'''
    VIETNAMESE : OpenTypeMacintoshLanguage
    '''The vietnamese language.'''
    INDONESIAN : OpenTypeMacintoshLanguage
    '''The indonesian language.'''
    TAGALOG : OpenTypeMacintoshLanguage
    '''The tagalog language.'''
    MALAY_ROMAN : OpenTypeMacintoshLanguage
    '''The malay roman language.'''
    MALAY_ARABIC : OpenTypeMacintoshLanguage
    '''The malay arabic language.'''
    AMHARIC : OpenTypeMacintoshLanguage
    '''The amharic language.'''
    TIGRINYA : OpenTypeMacintoshLanguage
    '''The tigrinya language.'''
    GALLA : OpenTypeMacintoshLanguage
    '''The galla language.'''
    SOMALI : OpenTypeMacintoshLanguage
    '''The somali language.'''
    SWAHILI : OpenTypeMacintoshLanguage
    '''The swahili language.'''
    KINYARWANDA_OR_RUANDA : OpenTypeMacintoshLanguage
    '''The kinyarwanda or ruanda language.'''
    RUNDI : OpenTypeMacintoshLanguage
    '''The rundi language.'''
    NYANJA_OR_CHEWA : OpenTypeMacintoshLanguage
    '''The nyanja or chewa language.'''
    MALAGASY : OpenTypeMacintoshLanguage
    '''The malagasy language.'''
    ESPERANTO : OpenTypeMacintoshLanguage
    '''The esperanto language.'''
    WELSH : OpenTypeMacintoshLanguage
    '''The welsh language.'''
    BASQUE : OpenTypeMacintoshLanguage
    '''The basque language.'''
    CATALAN : OpenTypeMacintoshLanguage
    '''The catalan language.'''
    LATIN : OpenTypeMacintoshLanguage
    '''The latin language.'''
    QUECHUA : OpenTypeMacintoshLanguage
    '''The quechua language.'''
    GUARANI : OpenTypeMacintoshLanguage
    '''The guarani language.'''
    AYMARA : OpenTypeMacintoshLanguage
    '''The aymara language.'''
    TATAR : OpenTypeMacintoshLanguage
    '''The tatar language.'''
    UIGHUR : OpenTypeMacintoshLanguage
    '''The uighur language.'''
    DZONGKHA : OpenTypeMacintoshLanguage
    '''The dzongkha language.'''
    JAVANESE_ROMAN : OpenTypeMacintoshLanguage
    '''The javanese roman language.'''
    SUNDANESE_ROMAN : OpenTypeMacintoshLanguage
    '''The sundanese roman language.'''
    GALICIAN : OpenTypeMacintoshLanguage
    '''The galician language.'''
    AFRIKAANS : OpenTypeMacintoshLanguage
    '''The afrikaans language.'''
    BRETON : OpenTypeMacintoshLanguage
    '''The breton language.'''
    INUKTITUT : OpenTypeMacintoshLanguage
    '''The inuktitut language.'''
    SCOTTISH_GAELIC : OpenTypeMacintoshLanguage
    '''The scottish gaelic language.'''
    MANX_GAELIC : OpenTypeMacintoshLanguage
    '''The manx gaelic language.'''
    IRISH_GAELIC_WITH_DOT_ABOVE : OpenTypeMacintoshLanguage
    '''The irish gaelic with dot above language.'''
    TONGAN : OpenTypeMacintoshLanguage
    '''The tongan language.'''
    GREEK_POLYTONIC : OpenTypeMacintoshLanguage
    '''The greek polytonic language.'''
    GREENLANDIC : OpenTypeMacintoshLanguage
    '''The greenlandic language.'''
    AZERBAIJANI_ROMAN : OpenTypeMacintoshLanguage
    '''The azerbaijani roman language.'''

class OpenTypeName:
    '''Defines pre-defined IDs, they apply to all platforms unless indicated otherwise.'''
    
    COPYRIGHT_NOTICE : OpenTypeName
    '''Copyright notice.'''
    FONT_FAMILY_NAME : OpenTypeName
    '''Font Family name.'''
    FONT_SUBFAMILY_NAME : OpenTypeName
    '''Font Subfamily name.'''
    UNIQUE_FONT_IDENTIFIER : OpenTypeName
    '''Unique font identifier.'''
    FULL_FONT_NAME : OpenTypeName
    '''Full font name that reflects all family and relevant subfamily descriptors.'''
    VERSION_STRING : OpenTypeName
    '''Version string.'''
    POST_SCRIPT_NAME : OpenTypeName
    '''PostScript name for the font.'''
    TRADEMARK : OpenTypeName
    '''Trademark notice/information for this font.'''
    MANUFACTURER_NAME : OpenTypeName
    '''Manufacturer Name.'''
    DESIGNER : OpenTypeName
    '''Designer; name of the designer of the typeface.'''
    DESCRIPTION : OpenTypeName
    '''Description of the typeface.'''
    URL_VENDOR : OpenTypeName
    '''URL of font vendor (with protocol, e.g., http://, ftp://).'''
    URL_DESIGNER : OpenTypeName
    '''URL of typeface designer (with protocol, e.g., http://, ftp://).'''
    LICENSE_DESCRIPTION : OpenTypeName
    '''Description of how the font may be legally used, or different example scenarios for licensed use.'''
    LICENSE_INFO_URL : OpenTypeName
    '''URL where additional licensing information can be found.'''
    TYPOGRAPHIC_FAMILY : OpenTypeName
    '''Typographic Family name.'''
    TYPOGRAPHIC_SUBFAMILY : OpenTypeName
    '''Typographic Subfamily name.'''
    COMPATIBLE_FULL : OpenTypeName
    '''Compatible Full (Macintosh only).
    On the Macintosh, the menu name is constructed using the FOND resource.'''
    SAMPLE_TEXT : OpenTypeName
    '''Sample text.
    This can be the font name, or any other text that the designer thinks is the best sample to display the font in.'''
    POST_SCRIPT_CID_FINDFONT : OpenTypeName
    '''PostScript CID findfont name.'''
    WWS_FAMILY_NAME : OpenTypeName
    '''WWS Family Name.'''
    WWS_SUBFAMILY_NAME : OpenTypeName
    '''WWS Subfamily Name.'''
    LIGHT_BACKGROUND_PALETTE : OpenTypeName
    '''Light Background Palette.'''
    DARK_BACKGROUND_PALETTE : OpenTypeName
    '''Dark Background Palette.'''
    VARIATIONS_POST_SCRIPT_NAME_PREFIX : OpenTypeName
    '''Variations PostScript Name Prefix.'''

class OpenTypePlatform:
    '''Represents OpenType platform for Name table.'''
    
    UNICODE : OpenTypePlatform
    '''The Unicode platform.'''
    MACINTOSH : OpenTypePlatform
    '''The Macintosh platform.'''
    ISO : OpenTypePlatform
    '''The ISO [deprecated] platform.'''
    WINDOWS : OpenTypePlatform
    '''The Windows platform.'''
    CUSTOM : OpenTypePlatform
    '''The Custom platform.'''

class OpenTypeStyles:
    '''Represents the OpenType font style.'''
    
    REGULAR : OpenTypeStyles
    '''Normal text.'''
    BOLD : OpenTypeStyles
    '''Bold text.'''
    ITALIC : OpenTypeStyles
    '''Italic text.'''
    UNDERLINE : OpenTypeStyles
    '''Underlined text.'''
    OUTLINE : OpenTypeStyles
    '''Outline text.'''
    SHADOW : OpenTypeStyles
    '''Shadow text.'''
    CONDENSED : OpenTypeStyles
    '''Condensed text.'''
    EXTENDED : OpenTypeStyles
    '''Extended text.'''

class OpenTypeUnicodeEncoding:
    '''Represents encoding for :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.UNICODE` platform.'''
    
    UNICODE10 : OpenTypeUnicodeEncoding
    '''Unicode 1.0 semantics.'''
    UNICODE11 : OpenTypeUnicodeEncoding
    '''Unicode 1.1 semantics.'''
    ISO : OpenTypeUnicodeEncoding
    '''ISO/IEC 10646 semantics.'''
    UNICODE_20_BMP : OpenTypeUnicodeEncoding
    '''Unicode 2.0 and onwards semantics, Unicode BMP only (\'cmap\' subtable formats 0, 4, 6).'''
    UNICODE_20_FULL : OpenTypeUnicodeEncoding
    '''Unicode 2.0 and onwards semantics, Unicode full repertoire (\'cmap\' subtable formats 0, 4, 6, 10, 12).'''
    UNICODE_VARIATION : OpenTypeUnicodeEncoding
    '''Unicode Variation Sequences (\'cmap\' subtable format 14).'''
    UNICODE_FULL : OpenTypeUnicodeEncoding
    '''Unicode full repertoire (\'cmap\' subtable formats 0, 4, 6, 10, 12, 13).'''

class OpenTypeVersion:
    '''Represents the OpenType version.'''
    
    TRUE_TYPE : OpenTypeVersion
    '''The TrueType font.'''
    CFF : OpenTypeVersion
    '''The OpenType font with PostScript outlines.'''
    TRUE_TYPE_OS_X : OpenTypeVersion
    '''The OS X and iOS TrueType font.'''

class OpenTypeWeight:
    '''Represents the OpenType font weight.
    Indicates the visual weight (degree of blackness or thickness of strokes) of the characters in the font.
    Values from 1 to 1000 are valid.'''
    
    UNDEFINED : OpenTypeWeight
    '''The undefined weight.'''
    THIN : OpenTypeWeight
    '''The Thin weight.'''
    EXTRA_LIGHT : OpenTypeWeight
    '''The Extra-light (Ultra-light) weight.'''
    LIGHT : OpenTypeWeight
    '''The Light weight.'''
    NORMAL : OpenTypeWeight
    '''The Normal (Regular) weight.'''
    MEDIUM : OpenTypeWeight
    '''The Medium weight.'''
    SEMI_BOLD : OpenTypeWeight
    '''The Semi-bold (Demi-bold) weight.'''
    BOLD : OpenTypeWeight
    '''The Bold weight.'''
    EXTRA_BOLD : OpenTypeWeight
    '''The Extra-bold (Ultra-bold) weight.'''
    HEAVY : OpenTypeWeight
    '''The Black (Heavy) weight.'''

class OpenTypeWidth:
    '''Represents the OpenType font width.
    Indicates a relative change from the normal aspect ratio (width to height ratio)
    as specified by a font designer for the glyphs in a font.'''
    
    UNDEFINED : OpenTypeWidth
    '''The undefined wifth.'''
    ULTRA_CONDENSED : OpenTypeWidth
    '''The Ultra-condensed wifth.'''
    EXTRA_CONDENSED : OpenTypeWidth
    '''The Extra-condensed wifth.'''
    CONDENSED : OpenTypeWidth
    '''The Condensed wifth.'''
    SEMI_CONDENSED : OpenTypeWidth
    '''The Semi-condensed wifth.'''
    MEDIUM : OpenTypeWidth
    '''The Medium (normal) wifth.'''
    SEMI_EXPANDED : OpenTypeWidth
    '''The Semi-expanded wifth.'''
    EXPANDED : OpenTypeWidth
    '''The Expanded wifth.'''
    EXTRA_EXPANDED : OpenTypeWidth
    '''The Extra-expanded wifth.'''
    ULTRA_EXPANDED : OpenTypeWidth
    '''The Ultra-expanded wifth.'''

class OpenTypeWindowsEncoding:
    '''Represents encoding for the :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.WINDOWS` platform.'''
    
    SYMBOL : OpenTypeWindowsEncoding
    '''The Symbol encoding.'''
    UNICODE_BMP : OpenTypeWindowsEncoding
    '''The Unicode BMP encoding.'''
    SHIFT_JIS : OpenTypeWindowsEncoding
    '''The ShiftJIS encoding.'''
    PRC : OpenTypeWindowsEncoding
    '''The PRC encoding.'''
    BIG5 : OpenTypeWindowsEncoding
    '''The Big5 encoding.'''
    WANSUNG : OpenTypeWindowsEncoding
    '''The Wansung encoding.'''
    JOHAB : OpenTypeWindowsEncoding
    '''The Johab encoding.'''
    UNICODE_FULL : OpenTypeWindowsEncoding
    '''The Unicode full repertoire encoding.'''

class OpenTypeWindowsLanguage:
    '''Represents language for :py:attr:`groupdocs.metadata.formats.font.OpenTypePlatform.WINDOWS` platform.'''
    
    UNKNOWN : OpenTypeWindowsLanguage
    '''The unknown language.'''
    AFRIKAANS_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The afrikaans south africa language.'''
    ALBANIAN_ALBANIA : OpenTypeWindowsLanguage
    '''The albanian Albania language.'''
    ALSATIAN_FRANCE : OpenTypeWindowsLanguage
    '''The alsatian France language.'''
    AMHARIC_ETHIOPIA : OpenTypeWindowsLanguage
    '''The amharic Rthiopia language.'''
    ARABIC_ALGERIA : OpenTypeWindowsLanguage
    '''The arabic Algeria language.'''
    ARABIC_BAHRAIN : OpenTypeWindowsLanguage
    '''The arabic Bahrain language.'''
    ARABIC_EGYPT : OpenTypeWindowsLanguage
    '''The arabic Egypt language.'''
    ARABIC_IRAQ : OpenTypeWindowsLanguage
    '''The arabic Iraq language.'''
    ARABIC_JORDAN : OpenTypeWindowsLanguage
    '''The arabic Jordan language.'''
    ARABIC_KUWAIT : OpenTypeWindowsLanguage
    '''The arabic Kuwait language.'''
    ARABIC_LEBANON : OpenTypeWindowsLanguage
    '''The arabic Lebanon language.'''
    ARABIC_LIBYA : OpenTypeWindowsLanguage
    '''The arabic Libya language.'''
    ARABIC_MOROCCO : OpenTypeWindowsLanguage
    '''The arabic Morocco language.'''
    ARABIC_OMAN : OpenTypeWindowsLanguage
    '''The arabic Oman language.'''
    ARABIC_QATAR : OpenTypeWindowsLanguage
    '''The arabic Qatar language.'''
    ARABIC_SAUDI_ARABIA : OpenTypeWindowsLanguage
    '''The arabic Saudi Arabia language.'''
    ARABIC_SYRIA : OpenTypeWindowsLanguage
    '''The arabic Syria language.'''
    ARABIC_TUNISIA : OpenTypeWindowsLanguage
    '''The arabic Tunisia language.'''
    ARABIC_UAE : OpenTypeWindowsLanguage
    '''The arabic UAE language.'''
    ARABIC_YEMEN : OpenTypeWindowsLanguage
    '''The arabic Yemen language.'''
    ARMENIAN_ARMENIA : OpenTypeWindowsLanguage
    '''The armenian Armenia language.'''
    ASSAMESE_INDIA : OpenTypeWindowsLanguage
    '''The assamese India language.'''
    AZERI_CYRILLIC_AZERBAIJAN : OpenTypeWindowsLanguage
    '''The azeri cyrillic Azerbaijan language.'''
    AZERI_LATIN_AZERBAIJAN : OpenTypeWindowsLanguage
    '''The azeri latin Azerbaijan language.'''
    BASHKIR_RUSSIA : OpenTypeWindowsLanguage
    '''The bashkir Russia language.'''
    BASQUE_BASQUE : OpenTypeWindowsLanguage
    '''The basque Basque language.'''
    BELARUSIAN_BELARUS : OpenTypeWindowsLanguage
    '''The belarusian Belarus language.'''
    BENGALI_BANGLADESH : OpenTypeWindowsLanguage
    '''The bengali Bangladesh language.'''
    BENGALI_INDIA : OpenTypeWindowsLanguage
    '''The bengali India language.'''
    BOSNIAN_LATIN_BOSNIA_AND_HERZEGOVINA : OpenTypeWindowsLanguage
    '''The bosnian latin Bosnia and Herzegovina language.'''
    BRETON_FRANCE : OpenTypeWindowsLanguage
    '''The breton France language.'''
    BULGARIAN_BULGARIA : OpenTypeWindowsLanguage
    '''The bulgarian Bulgaria language.'''
    CATALAN_CATALAN : OpenTypeWindowsLanguage
    '''The catalan Catalan language.'''
    CHINESE_HONG_KONG_SAR : OpenTypeWindowsLanguage
    '''The chinese Hong Kong SAR language.'''
    CHINESE_MACAO_SAR : OpenTypeWindowsLanguage
    '''The chinese Macao SAR language.'''
    CHINESE_PEOPLES_REPUBLIC_OF_CHINA : OpenTypeWindowsLanguage
    '''The chinese Peoples Republic of China language.'''
    CHINESE_SINGAPORE : OpenTypeWindowsLanguage
    '''The chinese Singapore language.'''
    CHINESE_TAIWAN : OpenTypeWindowsLanguage
    '''The chinese Taiwan language.'''
    CORSICAN_FRANCE : OpenTypeWindowsLanguage
    '''The corsican France language.'''
    CROATIAN_CROATIA : OpenTypeWindowsLanguage
    '''The croatian Croatia language.'''
    CROATIAN_LATIN_BOSNIA_AND_HERZEGOVINA : OpenTypeWindowsLanguage
    '''The croatian latin Bosnia and Herzegovina language.'''
    CZECH_CZECH_REPUBLIC : OpenTypeWindowsLanguage
    '''The czech Czech Republic language.'''
    DANISH_DENMARK : OpenTypeWindowsLanguage
    '''The danish Denmark language.'''
    DARI_AFGHANISTAN : OpenTypeWindowsLanguage
    '''The dari Afghanistan language.'''
    DIVEHI_MALDIVES : OpenTypeWindowsLanguage
    '''The divehi Maldives language.'''
    DUTCH_BELGIUM : OpenTypeWindowsLanguage
    '''The dutch Belgium language.'''
    DUTCH_NETHERLANDS : OpenTypeWindowsLanguage
    '''The dutch Netherlands language.'''
    ENGLISH_AUSTRALIA : OpenTypeWindowsLanguage
    '''The english Australia language.'''
    ENGLISH_BELIZE : OpenTypeWindowsLanguage
    '''The english Belize language.'''
    ENGLISH_CANADA : OpenTypeWindowsLanguage
    '''The english Canada language.'''
    ENGLISH_CARIBBEAN : OpenTypeWindowsLanguage
    '''The english Caribbean language.'''
    ENGLISH_INDIA : OpenTypeWindowsLanguage
    '''The english India language.'''
    ENGLISH_IRELAND : OpenTypeWindowsLanguage
    '''The english Ireland language.'''
    ENGLISH_JAMAICA : OpenTypeWindowsLanguage
    '''The english Jamaica language.'''
    ENGLISH_MALAYSIA : OpenTypeWindowsLanguage
    '''The english Malaysia language.'''
    ENGLISH_NEW_ZEALAND : OpenTypeWindowsLanguage
    '''The english New Zealand language.'''
    ENGLISH_REPUBLIC_OF_THE_PHILIPPINES : OpenTypeWindowsLanguage
    '''The english Republic of the Philippines language.'''
    ENGLISH_SINGAPORE : OpenTypeWindowsLanguage
    '''The english Singapore language.'''
    ENGLISH_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The english south africa language.'''
    ENGLISH_TRINIDAD_AND_TOBAGO : OpenTypeWindowsLanguage
    '''The english Trinidad and Tobago language.'''
    ENGLISH_UNITED_KINGDOM : OpenTypeWindowsLanguage
    '''The english United Kingdom language.'''
    ENGLISH_UNITED_STATES : OpenTypeWindowsLanguage
    '''The english United States language.'''
    ENGLISH_ZIMBABWE : OpenTypeWindowsLanguage
    '''The english Zimbabwe language.'''
    ESTONIAN_ESTONIA : OpenTypeWindowsLanguage
    '''The estonian Estonia language.'''
    FAROESE_FAROE_ISLANDS : OpenTypeWindowsLanguage
    '''The faroese Faroe Islands language.'''
    FILIPINO_PHILIPPINES : OpenTypeWindowsLanguage
    '''The filipino Philippines language.'''
    FINNISH_FINLAND : OpenTypeWindowsLanguage
    '''The finnish Finland language.'''
    FRENCH_BELGIUM : OpenTypeWindowsLanguage
    '''The french Belgium language.'''
    FRENCH_CANADA : OpenTypeWindowsLanguage
    '''The french Canada language.'''
    FRENCH_FRANCE : OpenTypeWindowsLanguage
    '''The french France language.'''
    FRENCH_LUXEMBOURG : OpenTypeWindowsLanguage
    '''The french Luxembourg language.'''
    FRENCH_PRINCIPALITY_OF_MONACO : OpenTypeWindowsLanguage
    '''The french Principality of Monaco language.'''
    FRENCH_SWITZERLAND : OpenTypeWindowsLanguage
    '''The french Switzerland language.'''
    FRISIAN_NETHERLANDS : OpenTypeWindowsLanguage
    '''The frisian Netherlands language.'''
    GALICIAN_GALICIAN : OpenTypeWindowsLanguage
    '''The galician Galician language.'''
    GEORGIAN_GEORGIA : OpenTypeWindowsLanguage
    '''The georgian Georgia language.'''
    GERMAN_AUSTRIA : OpenTypeWindowsLanguage
    '''The german Austria language.'''
    GERMAN_GERMANY : OpenTypeWindowsLanguage
    '''The german Germany language.'''
    GERMAN_LIECHTENSTEIN : OpenTypeWindowsLanguage
    '''The german Liechtenstein language.'''
    GERMAN_LUXEMBOURG : OpenTypeWindowsLanguage
    '''The german Luxembourg language.'''
    GERMAN_SWITZERLAND : OpenTypeWindowsLanguage
    '''The german Switzerland language.'''
    GREEK_GREECE : OpenTypeWindowsLanguage
    '''The greek Greece language.'''
    GREENLANDIC_GREENLAND : OpenTypeWindowsLanguage
    '''The greenlandic Greenland language.'''
    GUJARATI_INDIA : OpenTypeWindowsLanguage
    '''The gujarati India language.'''
    HAUSA_LATIN_NIGERIA : OpenTypeWindowsLanguage
    '''The hausa latin Nigeria language.'''
    HEBREW_ISRAEL : OpenTypeWindowsLanguage
    '''The hebrew Israel language.'''
    HINDI_INDIA : OpenTypeWindowsLanguage
    '''The hindi India language.'''
    HUNGARIAN_HUNGARY : OpenTypeWindowsLanguage
    '''The hungarian Hungary language.'''
    ICELANDIC_ICELAND : OpenTypeWindowsLanguage
    '''The icelandic Iceland language.'''
    IGBO_NIGERIA : OpenTypeWindowsLanguage
    '''The igbo Nigeria language.'''
    INDONESIAN_INDONESIA : OpenTypeWindowsLanguage
    '''The indonesian Indonesia language.'''
    INUKTITUT_CANADA : OpenTypeWindowsLanguage
    '''The inuktitut Canada language.'''
    INUKTITUT_LATIN_CANADA : OpenTypeWindowsLanguage
    '''The inuktitut latin Canada language.'''
    IRISH_IRELAND : OpenTypeWindowsLanguage
    '''The irish Ireland language.'''
    ISI_XHOSA_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The isi xhosa South Africa language.'''
    ISI_ZULU_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The isi zulu South Africa language.'''
    ITALIAN_ITALY : OpenTypeWindowsLanguage
    '''The italian Italy language.'''
    ITALIAN_SWITZERLAND : OpenTypeWindowsLanguage
    '''The italian Switzerland language.'''
    JAPANESE_JAPAN : OpenTypeWindowsLanguage
    '''The japanese Japan language.'''
    KANNADA_INDIA : OpenTypeWindowsLanguage
    '''The kannada India language.'''
    KAZAKH_KAZAKHSTAN : OpenTypeWindowsLanguage
    '''The kazakh Kazakhstan language.'''
    KHMER_CAMBODIA : OpenTypeWindowsLanguage
    '''The khmer Cambodia language.'''
    KICHE_GUATEMALA : OpenTypeWindowsLanguage
    '''The kiche Guatemala language.'''
    KINYARWANDA_RWANDA : OpenTypeWindowsLanguage
    '''The kinyarwanda Rwanda language.'''
    KISWAHILI_KENYA : OpenTypeWindowsLanguage
    '''The kiswahili Kenya language.'''
    KONKANI_INDIA : OpenTypeWindowsLanguage
    '''The konkani India language.'''
    KOREAN_KOREA : OpenTypeWindowsLanguage
    '''The korean Korea language.'''
    KYRGYZ_KYRGYZSTAN : OpenTypeWindowsLanguage
    '''The kyrgyz Kyrgyzstan language.'''
    LAO_LAO_PDR : OpenTypeWindowsLanguage
    '''The lao lao PDR language.'''
    LATVIAN_LATVIA : OpenTypeWindowsLanguage
    '''The latvian Latvia language.'''
    LITHUANIAN_LITHUANIA : OpenTypeWindowsLanguage
    '''The lithuanian Lithuania language.'''
    LOWER_SORBIAN_GERMANY : OpenTypeWindowsLanguage
    '''The lower sorbian Germany language.'''
    LUXEMBOURGISH_LUXEMBOURG : OpenTypeWindowsLanguage
    '''The luxembourgish Luxembourg language.'''
    MACEDONIAN_FYROM_FORMER_YUGOSLAV_REPUBLIC_OF_MACEDONIA : OpenTypeWindowsLanguage
    '''The macedonian fyrom former Yugoslav Republic of Macedonia language.'''
    MALAY_BRUNEI_DARUSSALAM : OpenTypeWindowsLanguage
    '''The malay brunei Darussalam language.'''
    MALAY_MALAYSIA : OpenTypeWindowsLanguage
    '''The malay Malaysia language.'''
    MALAYALAM_INDIA : OpenTypeWindowsLanguage
    '''The malayalam India language.'''
    MALTESE_MALTA : OpenTypeWindowsLanguage
    '''The maltese Malta language.'''
    MAORI_NEW_ZEALAND : OpenTypeWindowsLanguage
    '''The maori New Zealand language.'''
    MAPUDUNGUN_CHILE : OpenTypeWindowsLanguage
    '''The mapudungun Chile language.'''
    MARATHI_INDIA : OpenTypeWindowsLanguage
    '''The marathi India language.'''
    MOHAWK_MOHAWK : OpenTypeWindowsLanguage
    '''The mohawk Mohawk language.'''
    MONGOLIAN_CYRILLIC_MONGOLIA : OpenTypeWindowsLanguage
    '''The mongolian cyrillic Mongolia language.'''
    MONGOLIAN_TRADITIONAL_PEOPLES_REPUBLIC_OF_CHINA : OpenTypeWindowsLanguage
    '''The mongolian traditional Peoples Republic of China language.'''
    NEPALI_NEPAL : OpenTypeWindowsLanguage
    '''The nepali Nepal language.'''
    NORWEGIAN_BOKMAL_NORWAY : OpenTypeWindowsLanguage
    '''The norwegian bokmal Norway language.'''
    NORWEGIAN_NYNORSK_NORWAY : OpenTypeWindowsLanguage
    '''The norwegian nynorsk Norway language.'''
    OCCITAN_FRANCE : OpenTypeWindowsLanguage
    '''The occitan France language.'''
    ODIA_FORMERLY_ORIYA_INDIA : OpenTypeWindowsLanguage
    '''The odia formerly oriya India language.'''
    PASHTO_AFGHANISTAN : OpenTypeWindowsLanguage
    '''The pashto Afghanistan language.'''
    POLISH_POLAND : OpenTypeWindowsLanguage
    '''The polish Poland language.'''
    PORTUGUESE_BRAZIL : OpenTypeWindowsLanguage
    '''The portuguese Brazil language.'''
    PORTUGUESE_PORTUGAL : OpenTypeWindowsLanguage
    '''The portuguese Portugal language.'''
    PUNJABI_INDIA : OpenTypeWindowsLanguage
    '''The punjabi India language.'''
    QUECHUA_BOLIVIA : OpenTypeWindowsLanguage
    '''The quechua Bolivia language.'''
    QUECHUA_ECUADOR : OpenTypeWindowsLanguage
    '''The quechua Ecuador language.'''
    QUECHUA_PERU : OpenTypeWindowsLanguage
    '''The quechua Peru language.'''
    ROMANIAN_ROMANIA : OpenTypeWindowsLanguage
    '''The romanian Romania language.'''
    ROMANSH_SWITZERLAND : OpenTypeWindowsLanguage
    '''The romansh Switzerland language.'''
    RUSSIAN_RUSSIA : OpenTypeWindowsLanguage
    '''The russian Russia language.'''
    SAMI_INARI_FINLAND : OpenTypeWindowsLanguage
    '''The sami inari Finland language.'''
    SAMI_LULE_NORWAY : OpenTypeWindowsLanguage
    '''The sami lule Norway language.'''
    SAMI_LULE_SWEDEN : OpenTypeWindowsLanguage
    '''The sami lule Sweden language.'''
    SAMI_NORTHERN_FINLAND : OpenTypeWindowsLanguage
    '''The sami northern Finland language.'''
    SAMI_NORTHERN_NORWAY : OpenTypeWindowsLanguage
    '''The sami northern Norway language.'''
    SAMI_NORTHERN_SWEDEN : OpenTypeWindowsLanguage
    '''The sami northern Sweden language.'''
    SAMI_SKOLT_FINLAND : OpenTypeWindowsLanguage
    '''The sami skolt Finland language.'''
    SAMI_SOUTHERN_NORWAY : OpenTypeWindowsLanguage
    '''The sami southern Norway language.'''
    SAMI_SOUTHERN_SWEDEN : OpenTypeWindowsLanguage
    '''The sami southern Sweden language.'''
    SANSKRIT_INDIA : OpenTypeWindowsLanguage
    '''The sanskrit India language.'''
    SERBIAN_CYRILLIC_BOSNIA_AND_HERZEGOVINA : OpenTypeWindowsLanguage
    '''The serbian cyrillic Bosnia and Herzegovina language.'''
    SERBIAN_CYRILLIC_SERBIA : OpenTypeWindowsLanguage
    '''The serbian cyrillic Serbia language.'''
    SERBIAN_LATIN_BOSNIA_AND_HERZEGOVINA : OpenTypeWindowsLanguage
    '''The serbian latin Bosnia and Herzegovina language.'''
    SERBIAN_LATIN_SERBIA : OpenTypeWindowsLanguage
    '''The serbian latin Serbia language.'''
    SESOTHO_SA_LEBOA_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The sesotho sa leboa South Africa language.'''
    SETSWANA_SOUTH_AFRICA : OpenTypeWindowsLanguage
    '''The setswana South Africa language.'''
    SINHALA_SRI_LANKA : OpenTypeWindowsLanguage
    '''The sinhala Sri Lanka language.'''
    SLOVAK_SLOVAKIA : OpenTypeWindowsLanguage
    '''The slovak Slovakia language.'''
    SLOVENIAN_SLOVENIA : OpenTypeWindowsLanguage
    '''The slovenian Slovenia language.'''
    SPANISH_ARGENTINA : OpenTypeWindowsLanguage
    '''The spanish Argentina language.'''
    SPANISH_BOLIVIA : OpenTypeWindowsLanguage
    '''The spanish Bolivia language.'''
    SPANISH_CHILE : OpenTypeWindowsLanguage
    '''The spanish Chile language.'''
    SPANISH_COLOMBIA : OpenTypeWindowsLanguage
    '''The spanish Colombia language.'''
    SPANISH_COSTA_RICA : OpenTypeWindowsLanguage
    '''The spanish Costa Rica language.'''
    SPANISH_DOMINICAN_REPUBLIC : OpenTypeWindowsLanguage
    '''The spanish Dominican Republic language.'''
    SPANISH_ECUADOR : OpenTypeWindowsLanguage
    '''The spanish Ecuador language.'''
    SPANISH_EL_SALVADOR : OpenTypeWindowsLanguage
    '''The spanish El Salvador language.'''
    SPANISH_GUATEMALA : OpenTypeWindowsLanguage
    '''The spanish Guatemala language.'''
    SPANISH_HONDURAS : OpenTypeWindowsLanguage
    '''The spanish Honduras language.'''
    SPANISH_MEXICO : OpenTypeWindowsLanguage
    '''The spanish Mexico language.'''
    SPANISH_NICARAGUA : OpenTypeWindowsLanguage
    '''The spanish Nicaragua language.'''
    SPANISH_PANAMA : OpenTypeWindowsLanguage
    '''The spanish Panama language.'''
    SPANISH_PARAGUAY : OpenTypeWindowsLanguage
    '''The spanish Paraguay language.'''
    SPANISH_PERU : OpenTypeWindowsLanguage
    '''The spanish Peru language.'''
    SPANISH_PUERTO_RICO : OpenTypeWindowsLanguage
    '''The spanish Puerto Rico language.'''
    SPANISH_MODERN_SORT_SPAIN : OpenTypeWindowsLanguage
    '''The spanish modern sort Spain language.'''
    SPANISH_TRADITIONAL_SORT_SPAIN : OpenTypeWindowsLanguage
    '''The spanish traditional sort Spain language.'''
    SPANISH_UNITED_STATES : OpenTypeWindowsLanguage
    '''The spanish United States language.'''
    SPANISH_URUGUAY : OpenTypeWindowsLanguage
    '''The spanish Uruguay language.'''
    SPANISH_VENEZUELA : OpenTypeWindowsLanguage
    '''The spanish Venezuela language.'''
    SWEDEN_FINLAND : OpenTypeWindowsLanguage
    '''The sweden Finland language.'''
    SWEDISH_SWEDEN : OpenTypeWindowsLanguage
    '''The swedish Sweden language.'''
    SYRIAC_SYRIA : OpenTypeWindowsLanguage
    '''The syriac Syria language.'''
    TAJIK_CYRILLIC_TAJIKISTAN : OpenTypeWindowsLanguage
    '''The tajik cyrillic tajikistan language.'''
    TAMAZIGHT_LATIN_ALGERIA : OpenTypeWindowsLanguage
    '''The tamazight latin Algeria language.'''
    TAMIL_INDIA : OpenTypeWindowsLanguage
    '''The tamil India language.'''
    TATAR_RUSSIA : OpenTypeWindowsLanguage
    '''The tatar Russia language.'''
    TELUGU_INDIA : OpenTypeWindowsLanguage
    '''The telugu India language.'''
    THAI_THAILAND : OpenTypeWindowsLanguage
    '''The thai Thailand language.'''
    TIBETAN_PRC : OpenTypeWindowsLanguage
    '''The tibetan PRC language.'''
    TURKISH_TURKEY : OpenTypeWindowsLanguage
    '''The turkish Turkey language.'''
    TURKMEN_TURKMENISTAN : OpenTypeWindowsLanguage
    '''The turkmen Turkmenistan language.'''
    UIGHUR_PRC : OpenTypeWindowsLanguage
    '''The uighur PRC language.'''
    UKRAINIAN_UKRAINE : OpenTypeWindowsLanguage
    '''The ukrainian Ukraine language.'''
    UPPER_SORBIAN_GERMANY : OpenTypeWindowsLanguage
    '''The upper sorbian Germany language.'''
    URDU_ISLAMIC_REPUBLIC_OF_PAKISTAN : OpenTypeWindowsLanguage
    '''The urdu Islamic Republic of Pakistan language.'''
    UZBEK_CYRILLIC_UZBEKISTAN : OpenTypeWindowsLanguage
    '''The uzbek cyrillic Uzbekistan language.'''
    UZBEK_LATIN_UZBEKISTAN : OpenTypeWindowsLanguage
    '''The uzbek latin Uzbekistan language.'''
    VIETNAMESE_VIETNAM : OpenTypeWindowsLanguage
    '''The vietnamese Vietnam language.'''
    WELSH_UNITED_KINGDOM : OpenTypeWindowsLanguage
    '''The welsh United Kingdom language.'''
    WOLOF_SENEGAL : OpenTypeWindowsLanguage
    '''The wolof Senegal language.'''
    YAKUT_RUSSIA : OpenTypeWindowsLanguage
    '''The yakut Russia language.'''
    YI_PRC : OpenTypeWindowsLanguage
    '''The yi PRC language.'''
    YORUBA_NIGERIA : OpenTypeWindowsLanguage
    '''The yoruba Nigeria language.'''

