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

class CanonCameraSettingsPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents CANON camera settings.'''
    
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
    def macro_mode(self) -> int:
        '''Gets the macro mode.'''
        raise NotImplementedError()
    
    @property
    def self_timer(self) -> int:
        '''Gets the self timer.'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> int:
        '''Gets the quality.'''
        raise NotImplementedError()
    
    @property
    def canon_flash_mode(self) -> int:
        '''Gets the canon flash mode.'''
        raise NotImplementedError()
    
    @property
    def continuous_drive(self) -> int:
        '''Gets the continuous drive.'''
        raise NotImplementedError()
    
    @property
    def focus_mode(self) -> int:
        '''Gets the focus mode.'''
        raise NotImplementedError()
    
    @property
    def record_mode(self) -> int:
        '''Gets the record mode.'''
        raise NotImplementedError()
    
    @property
    def canon_image_size(self) -> int:
        '''Gets the size of the canon image.'''
        raise NotImplementedError()
    
    @property
    def easy_mode(self) -> int:
        '''Gets the easy mode.'''
        raise NotImplementedError()
    
    @property
    def digital_zoom(self) -> int:
        '''Gets the digital zoom.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> int:
        '''Gets the contrast.'''
        raise NotImplementedError()
    
    @property
    def saturation(self) -> int:
        '''Gets the saturation.'''
        raise NotImplementedError()
    
    @property
    def sharpness(self) -> int:
        '''Gets the sharpness.'''
        raise NotImplementedError()
    
    @property
    def camera_iso(self) -> int:
        '''Gets the camera iso.'''
        raise NotImplementedError()
    
    @property
    def metering_mode(self) -> int:
        '''Gets the metering mode.'''
        raise NotImplementedError()
    
    @property
    def focus_range(self) -> int:
        '''Gets the focus range.'''
        raise NotImplementedError()
    
    @property
    def af_point(self) -> int:
        '''Gets the AFPoint.'''
        raise NotImplementedError()
    
    @property
    def canon_exposure_mode(self) -> int:
        '''Gets the canon exposure mode.'''
        raise NotImplementedError()
    
    @property
    def lens_type(self) -> int:
        '''Gets the type of the lens.'''
        raise NotImplementedError()
    
    @property
    def max_focal_length(self) -> int:
        '''Gets the maximum length of the focal.'''
        raise NotImplementedError()
    
    @property
    def min_focal_length(self) -> int:
        '''Gets the minimum length of the focal.'''
        raise NotImplementedError()
    
    @property
    def image_stabilization(self) -> int:
        '''Gets the image stabilization.'''
        raise NotImplementedError()
    

class CanonMakerNotePackage(MakerNotePackage):
    '''Represents CANON MakerNote metadata.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.image.TiffTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all TIFF tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : groupdocs.metadata.formats.image.TiffTagID) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A TIFF tag id.
        :returns: True if the specified TIFF tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.image.TiffTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all TIFF tags stored in the package.'''
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
    def camera_settings(self) -> groupdocs.metadata.standards.exif.makernote.CanonCameraSettingsPackage:
        '''Gets the camera settings.'''
        raise NotImplementedError()
    
    @property
    def canon_image_type(self) -> str:
        '''Gets the Canon image type.'''
        raise NotImplementedError()
    
    @property
    def canon_firmware_version(self) -> str:
        '''Gets the canon firmware version.'''
        raise NotImplementedError()
    
    @property
    def file_number(self) -> Optional[int]:
        '''Gets the file number.'''
        raise NotImplementedError()
    
    @property
    def owner_name(self) -> str:
        '''Gets the name of the owner.'''
        raise NotImplementedError()
    
    @property
    def serial_number(self) -> Optional[int]:
        '''Gets the serial number.'''
        raise NotImplementedError()
    
    @property
    def canon_file_length(self) -> Optional[int]:
        '''Gets the length of the canon file.'''
        raise NotImplementedError()
    
    @property
    def canon_model_id(self) -> Optional[int]:
        '''Gets the canon model identifier.'''
        raise NotImplementedError()
    

class MakerNotePackage(groupdocs.metadata.standards.exif.ExifDictionaryBasePackage):
    '''Provides an abstract base class for MakerNote metadata packages.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.image.TiffTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all TIFF tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : groupdocs.metadata.formats.image.TiffTagID) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A TIFF tag id.
        :returns: True if the specified TIFF tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.image.TiffTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all TIFF tags stored in the package.'''
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
    

class NikonMakerNotePackage(MakerNotePackage):
    '''Represents NIKON MakerNote metadata.'''
    
    def __init__(self, tags : List[groupdocs.metadata.formats.image.TiffTag]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.exif.makernote.NikonMakerNotePackage` class.
        
        :param tags: Array of TIFF tags.'''
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.image.TiffTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all TIFF tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : groupdocs.metadata.formats.image.TiffTagID) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A TIFF tag id.
        :returns: True if the specified TIFF tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.image.TiffTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all TIFF tags stored in the package.'''
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
    def maker_note_version(self) -> List[int]:
        '''Gets the MakerNote version.'''
        raise NotImplementedError()
    
    @property
    def iso(self) -> List[int]:
        '''Gets the iso.'''
        raise NotImplementedError()
    
    @property
    def color_mode(self) -> str:
        '''Gets the color mode.'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> str:
        '''Gets the quality string.'''
        raise NotImplementedError()
    
    @property
    def white_balance(self) -> str:
        '''Gets the white balance.'''
        raise NotImplementedError()
    
    @property
    def sharpness(self) -> str:
        '''Gets the sharpness.'''
        raise NotImplementedError()
    
    @property
    def focus_mode(self) -> str:
        '''Gets the focus mode.'''
        raise NotImplementedError()
    
    @property
    def flash_setting(self) -> str:
        '''Gets the flash setting.'''
        raise NotImplementedError()
    
    @property
    def flash_type(self) -> str:
        '''Gets the type of the flash.'''
        raise NotImplementedError()
    

class PanasonicMakerNotePackage(MakerNotePackage):
    '''Represents PANASONIC MakerNote metadata.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.image.TiffTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all TIFF tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : groupdocs.metadata.formats.image.TiffTagID) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A TIFF tag id.
        :returns: True if the specified TIFF tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.image.TiffTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all TIFF tags stored in the package.'''
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
    def image_quality(self) -> Optional[int]:
        '''Gets the image quality.'''
        raise NotImplementedError()
    
    @property
    def firmware_version(self) -> List[int]:
        '''Gets the firmware version.'''
        raise NotImplementedError()
    
    @property
    def white_balance(self) -> Optional[int]:
        '''Gets the white balance.'''
        raise NotImplementedError()
    
    @property
    def focus_mode(self) -> Optional[int]:
        '''Gets the focus mode.'''
        raise NotImplementedError()
    
    @property
    def af_mode(self) -> List[int]:
        '''Gets the AF mode.'''
        raise NotImplementedError()
    
    @property
    def image_stabilization(self) -> Optional[int]:
        '''Gets the image stabilization mode.'''
        raise NotImplementedError()
    
    @property
    def macro_mode(self) -> Optional[int]:
        '''Gets the macro mode.'''
        raise NotImplementedError()
    
    @property
    def shooting_mode(self) -> Optional[int]:
        '''Gets the shooting mode.'''
        raise NotImplementedError()
    
    @property
    def audio(self) -> Optional[int]:
        '''Gets the audio mode.'''
        raise NotImplementedError()
    
    @property
    def lens_type(self) -> str:
        '''Gets the type of the lens.'''
        raise NotImplementedError()
    
    @property
    def lens_serial_number(self) -> str:
        '''Gets the lens serial number.'''
        raise NotImplementedError()
    
    @property
    def accessory_type(self) -> str:
        '''Gets the type of the accessory.'''
        raise NotImplementedError()
    
    @property
    def accessory_serial_number(self) -> str:
        '''Gets the accessory serial number.'''
        raise NotImplementedError()
    

class SonyMakerNotePackage(MakerNotePackage):
    '''Represents SONY MakerNote metadata.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.image.TiffTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all TIFF tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : groupdocs.metadata.formats.image.TiffTagID) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A TIFF tag id.
        :returns: True if the specified TIFF tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.image.TiffTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all TIFF tags stored in the package.'''
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
    def header(self) -> str:
        '''Gets the MakerNote header.'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> Optional[int]:
        '''Gets the image quality.'''
        raise NotImplementedError()
    
    @property
    def white_balance(self) -> Optional[int]:
        '''Gets the white balance.'''
        raise NotImplementedError()
    
    @property
    def teleconverter(self) -> Optional[int]:
        '''Gets the teleconverter type.'''
        raise NotImplementedError()
    
    @property
    def multi_burst_mode(self) -> bool:
        '''Gets a value indicating whether the multi burst mode is on.'''
        raise NotImplementedError()
    
    @property
    def multi_burst_image_width(self) -> Optional[int]:
        '''Gets the width of the multi burst image.'''
        raise NotImplementedError()
    
    @property
    def multi_burst_image_height(self) -> Optional[int]:
        '''Gets the height of the multi burst image.'''
        raise NotImplementedError()
    
    @property
    def rating(self) -> Optional[int]:
        '''Gets the rating.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> Optional[int]:
        '''Gets the contrast.'''
        raise NotImplementedError()
    
    @property
    def saturation(self) -> Optional[int]:
        '''Gets the saturation.'''
        raise NotImplementedError()
    
    @property
    def sharpness(self) -> Optional[int]:
        '''Gets the sharpness.'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> Optional[int]:
        '''Gets the brightness.'''
        raise NotImplementedError()
    
    @property
    def picture_effect(self) -> Optional[int]:
        '''Gets the picture effect.'''
        raise NotImplementedError()
    
    @property
    def soft_skin_effect(self) -> Optional[int]:
        '''Gets the soft skin effect.'''
        raise NotImplementedError()
    
    @property
    def sony_model_id(self) -> Optional[int]:
        '''Gets the sony model identifier.'''
        raise NotImplementedError()
    
    @property
    def creative_style(self) -> str:
        '''Gets the creative style.'''
        raise NotImplementedError()
    
    @property
    def color_temperature(self) -> Optional[int]:
        '''Gets the color temperature.'''
        raise NotImplementedError()
    
    @property
    def color_mode(self) -> Optional[int]:
        '''Gets the color mode.'''
        raise NotImplementedError()
    
    @property
    def macro(self) -> Optional[int]:
        '''Gets the macro.'''
        raise NotImplementedError()
    
    @property
    def exposure_mode(self) -> Optional[int]:
        '''Gets the exposure mode.'''
        raise NotImplementedError()
    
    @property
    def focus_mode(self) -> Optional[int]:
        '''Gets the focus mode.'''
        raise NotImplementedError()
    
    @property
    def jpeg_quality(self) -> Optional[int]:
        '''Gets the JPEG quality.'''
        raise NotImplementedError()
    
    @property
    def af_illuminator(self) -> Optional[int]:
        '''Gets the AF illuminator type.'''
        raise NotImplementedError()
    
    @property
    def flash_level(self) -> Optional[int]:
        '''Gets the flash level.'''
        raise NotImplementedError()
    
    @property
    def release_mode(self) -> Optional[int]:
        '''Gets the release mode.'''
        raise NotImplementedError()
    

