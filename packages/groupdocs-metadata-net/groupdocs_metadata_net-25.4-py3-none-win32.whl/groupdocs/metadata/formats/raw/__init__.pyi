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

class ExifTag(groupdocs.metadata.common.MetadataProperty):
    '''Represents a ExifTag property.'''
    
    @property
    def name(self) -> str:
        '''Gets the property name.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> groupdocs.metadata.common.PropertyValue:
        '''Gets the property value.'''
        raise NotImplementedError()
    
    @property
    def interpreted_value(self) -> groupdocs.metadata.common.PropertyValue:
        '''Gets the interpreted property value, if available.
        The interpreted value is a user-friendly form of the original property value.
        For example, it returns a human-readable string instead of numeric flags and ids,
        if necessary, translates byte arrays to text, etc.'''
        raise NotImplementedError()
    
    @property
    def descriptor(self) -> groupdocs.metadata.common.PropertyDescriptor:
        '''Gets the descriptor associated with the metadata property.'''
        raise NotImplementedError()
    
    @property
    def tags(self) -> Sequence[groupdocs.metadata.tagging.PropertyTag]:
        '''Gets a collection of tags associated with the property.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> groupdocs.metadata.formats.image.TiffTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> groupdocs.metadata.formats.raw.ExifTagID:
        '''Gets the tag id.'''
        raise NotImplementedError()
    

class GpsIfdPackage(RawDictionaryBasePackage):
    '''Represents GPS IFD.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def gps_version_id(self) -> List[int]:
        '''Gets the GPSVersionID.'''
        raise NotImplementedError()
    
    @property
    def gps_latitude_ref(self) -> str:
        '''Gets the GPSLatitudeRef.'''
        raise NotImplementedError()
    
    @property
    def gps_latitude(self) -> List[float]:
        '''Gets the GPSLatitude.'''
        raise NotImplementedError()
    
    @property
    def gps_longitude_ref(self) -> str:
        '''Gets the GPSLongitudeRef.'''
        raise NotImplementedError()
    
    @property
    def gps_longitude(self) -> List[float]:
        '''Gets the GPSLongitude.'''
        raise NotImplementedError()
    
    @property
    def gps_altitude_ref(self) -> int:
        '''Gets the GPSAltitudeRef.'''
        raise NotImplementedError()
    
    @property
    def gps_altitude(self) -> float:
        '''Gets the GPSAltitude.'''
        raise NotImplementedError()
    
    @property
    def gps_time_stamp(self) -> List[float]:
        '''Gets the GPSTimeStamp.'''
        raise NotImplementedError()
    
    @property
    def gps_satellites(self) -> str:
        '''Gets the GPSSatellites.'''
        raise NotImplementedError()
    
    @property
    def gps_status(self) -> str:
        '''Gets the GPSStatus.'''
        raise NotImplementedError()
    
    @property
    def gps_measure_mode(self) -> str:
        '''Gets the GPSMeasureMode.'''
        raise NotImplementedError()
    
    @property
    def gpsdop(self) -> float:
        '''Gets the GPSDOP.'''
        raise NotImplementedError()
    
    @property
    def gps_speed_ref(self) -> str:
        '''Gets the GPSSpeedRef.'''
        raise NotImplementedError()
    
    @property
    def gps_speed(self) -> float:
        '''Gets the GPSSpeed.'''
        raise NotImplementedError()
    
    @property
    def gps_track_ref(self) -> str:
        '''Gets the GPSTrackRef.'''
        raise NotImplementedError()
    
    @property
    def gps_track(self) -> float:
        '''Gets the GPSTrack.'''
        raise NotImplementedError()
    
    @property
    def gps_img_direction_ref(self) -> str:
        '''Gets the GPSImgDirectionRef.'''
        raise NotImplementedError()
    
    @property
    def gps_img_direction(self) -> float:
        '''Gets the GPSImgDirection.'''
        raise NotImplementedError()
    
    @property
    def gps_map_datum(self) -> str:
        '''Gets the GPSMapDatum.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_latitude_ref(self) -> str:
        '''Gets the GPSDestLatitudeRef.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_latitude(self) -> List[float]:
        '''Gets the GPSDestLatitude.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_longitude_ref(self) -> str:
        '''Gets the GPSDestLongitudeRef.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_longitude(self) -> List[float]:
        '''Gets the GPSDestLongitude.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_bearing_ref(self) -> str:
        '''Gets the GPSDestBearingRef.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_bearing(self) -> float:
        '''Gets the GPSDestBearing.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_distance_ref(self) -> str:
        '''Gets the GPSDestDistanceRef.'''
        raise NotImplementedError()
    
    @property
    def gps_dest_distance(self) -> float:
        '''Gets the GPSDestDistance.'''
        raise NotImplementedError()
    
    @property
    def gps_processing_method(self) -> str:
        '''Gets the GPSProcessingMethod.'''
        raise NotImplementedError()
    
    @property
    def gps_area_information(self) -> int:
        '''Gets the GPSAreaInformation.'''
        raise NotImplementedError()
    
    @property
    def gps_date_stamp(self) -> str:
        '''Gets the GPSDateStamp.'''
        raise NotImplementedError()
    
    @property
    def gps_differential(self) -> int:
        '''Gets the GPSDifferential.'''
        raise NotImplementedError()
    
    @property
    def gpsh_positioning_error(self) -> float:
        '''Gets the GPSHPositioningError.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class InteroperabilityIFDPointerPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents Interoperability IFD.'''
    
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
    def tag_interop_index(self) -> str:
        '''Gets the TagInteropIndex.'''
        raise NotImplementedError()
    
    @property
    def tag_interop_version(self) -> List[int]:
        '''Gets the TagInteropVersion.'''
        raise NotImplementedError()
    

class RawDictionaryBasePackage(groupdocs.metadata.common.CustomPackage):
    '''Provides an abstract base class for EXIF metadata dictionaries.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawExifTagPackage(RawDictionaryBasePackage):
    '''Represents Exif tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def raw_maker_note_package(self) -> groupdocs.metadata.formats.raw.RawMakerNotePackage:
        '''Gets the Manufacturer notes (MakerNote).'''
        raise NotImplementedError()
    
    @property
    def interoperability_ifd_pointer_package(self) -> groupdocs.metadata.formats.raw.InteroperabilityIFDPointerPackage:
        '''Gets the Interoperability tag (Interoperability IFD Pointer).'''
        raise NotImplementedError()
    
    @property
    def interoperability_ifd_pointer(self) -> int:
        '''Gets the Interoperability tag (Interoperability IFD Pointer).'''
        raise NotImplementedError()
    
    @property
    def exposure_time(self) -> float:
        '''Gets the Exposure time.'''
        raise NotImplementedError()
    
    @property
    def f_number(self) -> float:
        '''Gets the F number.'''
        raise NotImplementedError()
    
    @property
    def exposure_program(self) -> int:
        '''Gets the Exposure program.'''
        raise NotImplementedError()
    
    @property
    def spectral_sensitivity(self) -> str:
        '''Gets the Spectral sensitivity.'''
        raise NotImplementedError()
    
    @property
    def photographic_sensitivity(self) -> int:
        '''Gets the Photographic Sensitivity.'''
        raise NotImplementedError()
    
    @property
    def oecf(self) -> List[int]:
        '''Gets the Optoelectric conversion factor.'''
        raise NotImplementedError()
    
    @property
    def sensitivity_type(self) -> int:
        '''Gets the Sensitivity Type.'''
        raise NotImplementedError()
    
    @property
    def standard_output_sensitivity(self) -> int:
        '''Gets the Standard Output Sensitivity.'''
        raise NotImplementedError()
    
    @property
    def recommended_exposure_index(self) -> int:
        '''Gets the Recommended ExposureIndexs.'''
        raise NotImplementedError()
    
    @property
    def iso_speed(self) -> int:
        '''Gets the ISO Speed.'''
        raise NotImplementedError()
    
    @property
    def iso_speed_latitudeyyy(self) -> int:
        '''Gets the ISO Speed Latitude yyy.'''
        raise NotImplementedError()
    
    @property
    def iso_speed_latitudezzz(self) -> int:
        '''Gets the ISO Speed Latitude zzz.'''
        raise NotImplementedError()
    
    @property
    def exif_version(self) -> List[int]:
        '''Gets the ExifVersion.'''
        raise NotImplementedError()
    
    @property
    def date_time_original(self) -> str:
        '''Gets the Date and time of original data generation.'''
        raise NotImplementedError()
    
    @property
    def date_time_digitized(self) -> str:
        '''Gets the Date and time of digital data generation.'''
        raise NotImplementedError()
    
    @property
    def offset_time(self) -> str:
        '''Gets the Offset data of DateTime.'''
        raise NotImplementedError()
    
    @property
    def offset_time_original(self) -> str:
        '''Gets the Offset data of DateTimeOriginal.'''
        raise NotImplementedError()
    
    @property
    def offset_time_digitized(self) -> str:
        '''Gets the Offset data of DateTimeDigitized.'''
        raise NotImplementedError()
    
    @property
    def components_configuration(self) -> List[int]:
        '''Gets the Meaning of each component.'''
        raise NotImplementedError()
    
    @property
    def shutter_speed_value(self) -> float:
        '''Gets the Shutter speed.'''
        raise NotImplementedError()
    
    @property
    def aperture_value(self) -> float:
        '''Gets the Aperture.'''
        raise NotImplementedError()
    
    @property
    def brightness_value(self) -> float:
        '''Gets the Brightness.'''
        raise NotImplementedError()
    
    @property
    def exposure_bias_value(self) -> float:
        '''Gets the Exposure bias.'''
        raise NotImplementedError()
    
    @property
    def max_aperture_value(self) -> float:
        '''Gets the Maximum lens aperture.'''
        raise NotImplementedError()
    
    @property
    def subject_distance(self) -> float:
        '''Gets the Subject distance.'''
        raise NotImplementedError()
    
    @property
    def metering_mode(self) -> int:
        '''Gets the Metering mode.'''
        raise NotImplementedError()
    
    @property
    def light_source(self) -> int:
        '''Gets the Light source.'''
        raise NotImplementedError()
    
    @property
    def flash(self) -> int:
        '''Gets the Flash.'''
        raise NotImplementedError()
    
    @property
    def focal_length(self) -> float:
        '''Gets the Lens focal length.'''
        raise NotImplementedError()
    
    @property
    def subject_area(self) -> int:
        '''Gets the Subject area.'''
        raise NotImplementedError()
    
    @property
    def user_comment(self) -> List[int]:
        '''Gets the User comments.'''
        raise NotImplementedError()
    
    @property
    def sub_sec_time(self) -> str:
        '''Gets the DateTime subseconds.'''
        raise NotImplementedError()
    
    @property
    def sub_sec_time_original(self) -> str:
        '''Gets the DateTimeOriginal subseconds.'''
        raise NotImplementedError()
    
    @property
    def sub_sec_time_digitized(self) -> str:
        '''Gets the DateTimeDigitized subseconds.'''
        raise NotImplementedError()
    
    @property
    def temperature(self) -> float:
        '''Gets the Temperature.'''
        raise NotImplementedError()
    
    @property
    def humidity(self) -> float:
        '''Gets the Humidity.'''
        raise NotImplementedError()
    
    @property
    def pressure(self) -> float:
        '''Gets the Pressure.'''
        raise NotImplementedError()
    
    @property
    def water_depth(self) -> float:
        '''Gets the WaterDepth.'''
        raise NotImplementedError()
    
    @property
    def acceleration(self) -> float:
        '''Gets the Acceleration.'''
        raise NotImplementedError()
    
    @property
    def camera_elevation_angle(self) -> float:
        '''Gets the Camera elevation angle.'''
        raise NotImplementedError()
    
    @property
    def flashpix_version(self) -> List[int]:
        '''Gets the Temperature.'''
        raise NotImplementedError()
    
    @property
    def color_space(self) -> int:
        '''Gets the Color space information .'''
        raise NotImplementedError()
    
    @property
    def pixel_x_dimension(self) -> int:
        '''Gets the Valid image width.'''
        raise NotImplementedError()
    
    @property
    def pixel_y_dimension(self) -> int:
        '''Gets the Valid image height.'''
        raise NotImplementedError()
    
    @property
    def related_sound_file(self) -> str:
        '''Gets the Related audio file.'''
        raise NotImplementedError()
    
    @property
    def flash_energy(self) -> float:
        '''Gets the Flash energy.'''
        raise NotImplementedError()
    
    @property
    def spatial_frequency_response(self) -> List[int]:
        '''Gets the Spatial frequency response.'''
        raise NotImplementedError()
    
    @property
    def focal_plane_x_resolution(self) -> float:
        '''Gets Focal plane X resolution.'''
        raise NotImplementedError()
    
    @property
    def focal_plane_y_resolution(self) -> float:
        '''Gets the Focal plane Y resolution.'''
        raise NotImplementedError()
    
    @property
    def focal_plane_resolution_unit(self) -> int:
        '''Gets the Focal plane resolution unit.'''
        raise NotImplementedError()
    
    @property
    def subject_location(self) -> int:
        '''Gets the Subject location.'''
        raise NotImplementedError()
    
    @property
    def exposure_index(self) -> float:
        '''Gets the Exposure index.'''
        raise NotImplementedError()
    
    @property
    def sensing_method(self) -> int:
        '''Gets the Sensing method.'''
        raise NotImplementedError()
    
    @property
    def file_source(self) -> List[int]:
        '''Gets the File source.'''
        raise NotImplementedError()
    
    @property
    def scene_type(self) -> List[int]:
        '''Gets the Scene Type.'''
        raise NotImplementedError()
    
    @property
    def cfa_pattern(self) -> List[int]:
        '''Gets the CFA pattern.'''
        raise NotImplementedError()
    
    @property
    def custom_rendered(self) -> int:
        '''Gets the Custom image processing.'''
        raise NotImplementedError()
    
    @property
    def exposure_mode(self) -> int:
        '''Gets the Exposure mode.'''
        raise NotImplementedError()
    
    @property
    def white_balance(self) -> int:
        '''Gets the White balance.'''
        raise NotImplementedError()
    
    @property
    def digital_zoom_ratio(self) -> float:
        '''Gets the Digital zoom ratio.'''
        raise NotImplementedError()
    
    @property
    def focal_length_in_35mm_film(self) -> int:
        '''Gets the Focal length in 35 mm film.'''
        raise NotImplementedError()
    
    @property
    def scene_capture_type(self) -> int:
        '''Gets the Scene capture type.'''
        raise NotImplementedError()
    
    @property
    def gain_control(self) -> float:
        '''Gets the Gain control.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> int:
        '''Gets the Contrast.'''
        raise NotImplementedError()
    
    @property
    def saturation(self) -> int:
        '''Gets the Saturation.'''
        raise NotImplementedError()
    
    @property
    def sharpness(self) -> int:
        '''Gets the Sharpness.'''
        raise NotImplementedError()
    
    @property
    def device_setting_description(self) -> List[int]:
        '''Gets the Device settings description.'''
        raise NotImplementedError()
    
    @property
    def subject_distance_range(self) -> int:
        '''Gets the Subject distance range.'''
        raise NotImplementedError()
    
    @property
    def image_unique_id(self) -> str:
        '''Gets the Unique image ID.'''
        raise NotImplementedError()
    
    @property
    def camera_owner_name(self) -> str:
        '''Gets the Camera Owner Name.'''
        raise NotImplementedError()
    
    @property
    def body_serial_number(self) -> str:
        '''Gets the Body Serial Number.'''
        raise NotImplementedError()
    
    @property
    def lens_specification(self) -> List[float]:
        '''Gets the Lens Specification.'''
        raise NotImplementedError()
    
    @property
    def lens_model(self) -> str:
        '''Gets the Lens Model.'''
        raise NotImplementedError()
    
    @property
    def lens_make(self) -> str:
        '''Gets the Lens Make.'''
        raise NotImplementedError()
    
    @property
    def lens_serial_number(self) -> str:
        '''Gets the Lens Serial Number.'''
        raise NotImplementedError()
    
    @property
    def composite_image(self) -> int:
        '''Gets the Composite image.'''
        raise NotImplementedError()
    
    @property
    def source_image_number_of_composite_image(self) -> int:
        '''Gets the Source image number of composite image.'''
        raise NotImplementedError()
    
    @property
    def source_exposure_times_of_composite_image(self) -> List[int]:
        '''Gets the Source exposure times of composite image.'''
        raise NotImplementedError()
    
    @property
    def gamma(self) -> float:
        '''Gets the Gamma.'''
        raise NotImplementedError()
    
    @property
    def maker_note(self) -> int:
        '''Gets the Standard Output Sensitivity.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawIFD1Package(RawDictionaryBasePackage):
    '''Represents IFD1 tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def thumbnail_offset(self) -> int:
        '''Gets the ThumbnailOffset.'''
        raise NotImplementedError()
    
    @property
    def thumbnail_lenght(self) -> int:
        '''Gets the ThumbnailLenght.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawIFD2Package(RawDictionaryBasePackage):
    '''Represents IFD1 tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def image_width(self) -> int:
        '''Gets the image width.'''
        raise NotImplementedError()
    
    @property
    def image_height(self) -> int:
        '''Gets the image height.'''
        raise NotImplementedError()
    
    @property
    def bits_per_sample(self) -> List[int]:
        '''Gets the image BitsPerSample.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> int:
        '''Gets the image Compression.'''
        raise NotImplementedError()
    
    @property
    def photometric_interpretation(self) -> int:
        '''Gets the image PhotometricInterpretation.'''
        raise NotImplementedError()
    
    @property
    def strip_offset(self) -> int:
        '''Gets the image StripOffset.'''
        raise NotImplementedError()
    
    @property
    def samples_per_pixel(self) -> int:
        '''Gets the SamplesPerPixel.'''
        raise NotImplementedError()
    
    @property
    def row_per_strip(self) -> int:
        '''Gets the RowPerStrip.'''
        raise NotImplementedError()
    
    @property
    def strip_byte_counts(self) -> int:
        '''Gets the StripByteCounts.'''
        raise NotImplementedError()
    
    @property
    def planar_configuration(self) -> int:
        '''Gets the PlanarConfiguration.'''
        raise NotImplementedError()
    
    @property
    def unknown1(self) -> int:
        '''Gets the Unknown1.'''
        raise NotImplementedError()
    
    @property
    def unknown2(self) -> int:
        '''Gets the Unknown2.'''
        raise NotImplementedError()
    
    @property
    def unknown3(self) -> List[int]:
        '''Gets the Unknown3.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawIFD3Package(RawDictionaryBasePackage):
    '''Represents IFD1 tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def image_width(self) -> int:
        '''Gets the image width.'''
        raise NotImplementedError()
    
    @property
    def image_height(self) -> int:
        '''Gets the image height.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> int:
        '''Gets the image Compression.'''
        raise NotImplementedError()
    
    @property
    def strip_offset(self) -> int:
        '''Gets the image StripOffset.'''
        raise NotImplementedError()
    
    @property
    def strip_byte_counts(self) -> int:
        '''Gets the image StripByteCounts.'''
        raise NotImplementedError()
    
    @property
    def unknown1(self) -> int:
        '''Gets the Unknown1.'''
        raise NotImplementedError()
    
    @property
    def unknown2(self) -> int:
        '''Gets the Unknown2.'''
        raise NotImplementedError()
    
    @property
    def unknown3(self) -> List[int]:
        '''Gets the Unknown3.'''
        raise NotImplementedError()
    
    @property
    def unknown4(self) -> int:
        '''Gets the Unknown4.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawMakerNotePackage(RawDictionaryBasePackage):
    '''Represents Raw MakerNotes tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class RawPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents Raw Package.'''
    
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
    

class RawTiffTagPackage(RawDictionaryBasePackage):
    '''Represents Tiff tags.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.raw.tag.RawTag]:
        '''Creates a list from the package.
        
        :returns: A list that contains all Raw tags from the package.'''
        raise NotImplementedError()
    
    def remove(self, tag_id : int) -> bool:
        '''Removes the property with the specified id.
        
        :param tag_id: A Raw tag id.
        :returns: True if the specified Raw tag is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    def set(self, tag : groupdocs.metadata.formats.raw.tag.RawTag) -> None:
        '''Adds or replaces the specified tag.
        
        :param tag: The tag to set.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all Raw tags stored in the package.'''
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
    def raw_ifd1_package(self) -> groupdocs.metadata.formats.raw.RawIFD1Package:
        '''Gets the IFD1.'''
        raise NotImplementedError()
    
    @property
    def raw_ifd2_package(self) -> groupdocs.metadata.formats.raw.RawIFD2Package:
        '''Gets the IFD2.'''
        raise NotImplementedError()
    
    @property
    def raw_ifd3_package(self) -> groupdocs.metadata.formats.raw.RawIFD3Package:
        '''Gets the IFD3.'''
        raise NotImplementedError()
    
    @property
    def raw_exif_tag_package(self) -> groupdocs.metadata.formats.raw.RawExifTagPackage:
        '''Gets the Exif tag (Exif IFD Pointer).'''
        raise NotImplementedError()
    
    @property
    def gps_ifd_package(self) -> groupdocs.metadata.formats.raw.GpsIfdPackage:
        '''Gets the GPS tag (GPSInfo IFD Pointer).'''
        raise NotImplementedError()
    
    @property
    def image_width(self) -> int:
        '''Gets the image width.'''
        raise NotImplementedError()
    
    @property
    def image_height(self) -> int:
        '''Gets the image height.'''
        raise NotImplementedError()
    
    @property
    def bits_per_sample(self) -> List[int]:
        '''Gets the bits per sample.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> int:
        '''Gets compression.'''
        raise NotImplementedError()
    
    @property
    def photometric_interpretation(self) -> int:
        '''Gets 	PhotometricInterpretation.'''
        raise NotImplementedError()
    
    @property
    def image_description(self) -> str:
        '''Gets a character string giving the title of the image.
        It may be a comment such as "1988 company picnic" or the like.'''
        raise NotImplementedError()
    
    @image_description.setter
    def image_description(self, value : str) -> None:
        '''Sets a character string giving the title of the image.
        It may be a comment such as "1988 company picnic" or the like.'''
        raise NotImplementedError()
    
    @property
    def make(self) -> str:
        '''Gets the macro mode.'''
        raise NotImplementedError()
    
    @property
    def model(self) -> str:
        '''Gets the model.'''
        raise NotImplementedError()
    
    @property
    def strip_offset(self) -> int:
        '''Gets the StripOffset.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> int:
        '''Gets the orientation.'''
        raise NotImplementedError()
    
    @property
    def samples_per_pixel(self) -> int:
        '''Gets the SamplesPerPixel.'''
        raise NotImplementedError()
    
    @property
    def rows_per_strip(self) -> int:
        '''Gets the RowsPerStrip.'''
        raise NotImplementedError()
    
    @property
    def strip_byte_counts(self) -> int:
        '''Gets the strip byte counts.'''
        raise NotImplementedError()
    
    @property
    def x_resolution(self) -> float:
        '''Gets the XResolution.'''
        raise NotImplementedError()
    
    @property
    def y_resolution(self) -> float:
        '''Gets the YResolution.'''
        raise NotImplementedError()
    
    @property
    def planar_configuration(self) -> int:
        '''Gets the PlanarConfiguration.'''
        raise NotImplementedError()
    
    @property
    def resolution_unit(self) -> int:
        '''Gets the Resolution Unit.'''
        raise NotImplementedError()
    
    @property
    def transfer_function(self) -> List[int]:
        '''Gets the TransferFunction.'''
        raise NotImplementedError()
    
    @property
    def software(self) -> str:
        '''Gets the Software.'''
        raise NotImplementedError()
    
    @property
    def date_time(self) -> str:
        '''Gets the DateTime.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the Artist.'''
        raise NotImplementedError()
    
    @property
    def white_point(self) -> List[float]:
        '''Gets the WhitePoint.'''
        raise NotImplementedError()
    
    @property
    def primary_chromaticities(self) -> List[float]:
        '''Gets the PrimaryChromaticities.'''
        raise NotImplementedError()
    
    @property
    def jpeg_interchange_format(self) -> int:
        '''Gets the JpegInterchangeFormat.'''
        raise NotImplementedError()
    
    @property
    def jpeg_interchange_format_length(self) -> int:
        '''Gets the JpegInterchangeFormatLength.'''
        raise NotImplementedError()
    
    @property
    def y_cb_cr_coefficients(self) -> List[float]:
        '''Gets the YCbCrCoefficients.'''
        raise NotImplementedError()
    
    @property
    def y_cb_cr_sub_sampling(self) -> List[int]:
        '''Gets the YCbCrSubSampling.'''
        raise NotImplementedError()
    
    @property
    def y_cb_cr_positioning(self) -> int:
        '''Gets the YCbCrPositioning.'''
        raise NotImplementedError()
    
    @property
    def reference_black_white(self) -> List[float]:
        '''Gets the ReferenceBlackWhite.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> str:
        '''Gets the Copyright.'''
        raise NotImplementedError()
    
    @property
    def exif(self) -> int:
        '''Gets the EXIF.'''
        raise NotImplementedError()
    
    @property
    def gps_ifd(self) -> int:
        '''Gets the EXIF.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.formats.raw.tag.RawTag:
        raise NotImplementedError()
    

class ExifTagID:
    '''Defines ids of Exif tags.'''
    
    EXPOSURE_TIME : ExifTagID
    '''Exposure Time'''
    F_NUMBER : ExifTagID
    '''F-Number'''
    EXPOSURE_PROGRAM : ExifTagID
    '''ExposureProgram'''
    SPECTRAL_SENSITIVITY : ExifTagID
    '''SpectralSensitivity'''
    GPS_INFO : ExifTagID
    '''GPSInfo'''
    ISO_SPEED_RATINGS : ExifTagID
    '''ISO Speed Ratings'''
    MAKER_NOTE_CANON : ExifTagID
    '''ISO Speed Ratings'''

class GpsIfdIndex:
    '''Defines ids of GpsIfd tags.'''
    
    GPS_VERSION_ID : GpsIfdIndex
    '''Indicates the GPSVersionID.'''
    GPS_LATITUDE_REF : GpsIfdIndex
    '''Indicates the GPSLatitudeRef.'''
    GPS_LATITUDE : GpsIfdIndex
    '''Indicates the GPSLatitude.'''
    GPS_LONGITUDE_REF : GpsIfdIndex
    '''Indicates the GPSLongitudeRef.'''
    GPS_LONGITUDE : GpsIfdIndex
    '''Indicates the GPSLongitude.'''
    GPS_ALTITUDE_REF : GpsIfdIndex
    '''Indicates the GPSAltitudeRef.'''
    GPS_ALTITUDE : GpsIfdIndex
    '''Indicates the GPSAltitude.'''
    GPS_TIME_STAMP : GpsIfdIndex
    '''Indicates the GPSTimeStamp.'''
    GPS_SATELLITES : GpsIfdIndex
    '''Indicates the GPSSatellites.'''
    GPS_STATUS : GpsIfdIndex
    '''Indicates the GPSStatus.'''
    GPS_MEASURE_MODE : GpsIfdIndex
    '''Indicates the GPSMeasureMode.'''
    GPSDOP : GpsIfdIndex
    '''Indicates the GPSDOP.'''
    GPS_SPEED_REF : GpsIfdIndex
    '''Indicates the GPSSpeedRef.'''
    GPS_SPEED : GpsIfdIndex
    '''Indicates the GPSSpeed.'''
    GPS_TRACK_REF : GpsIfdIndex
    '''Indicates the GPSTrackRef.'''
    GPS_TRACK : GpsIfdIndex
    '''Indicates the GPSTrack.'''
    GPS_IMG_DIRECTION_REF : GpsIfdIndex
    '''Indicates the GPSImgDirectionRef.'''
    GPS_IMG_DIRECTION : GpsIfdIndex
    '''Indicates the GPSImgDirection.'''
    GPS_MAP_DATUM : GpsIfdIndex
    '''Indicates the GPSMapDatum.'''
    GPS_DEST_LATITUDE_REF : GpsIfdIndex
    '''Indicates the GPSDestLatitudeRef.'''
    GPS_DEST_LATITUDE : GpsIfdIndex
    '''Indicates the GPSDestLatitude.'''
    GPS_DEST_LONGITUDE_REF : GpsIfdIndex
    '''Indicates the GPSDestLongitudeRef.'''
    GPS_DEST_LONGITUDE : GpsIfdIndex
    '''Indicates the GPSDestLongitude.'''
    GPS_DEST_BEARING_REF : GpsIfdIndex
    '''Indicates the GPSDestBearingRef.'''
    GPS_DEST_BEARING : GpsIfdIndex
    '''Indicates the GPSDestBearing.'''
    GPS_DEST_DISTANCE_REF : GpsIfdIndex
    '''Indicates the GPSDestDistanceRef.'''
    GPS_DEST_DISTANCE : GpsIfdIndex
    '''Indicates the GPSDestDistance.'''
    GPS_PROCESSING_METHOD : GpsIfdIndex
    '''Indicates the GPSProcessingMethod.'''
    GPS_AREA_INFORMATION : GpsIfdIndex
    '''Indicates the GPSAreaInformation.'''
    GPS_DATE_STAMP : GpsIfdIndex
    '''Indicates the GPSDateStamp.'''
    GPS_DIFFERENTIAL : GpsIfdIndex
    '''Indicates the GPSDifferential.'''
    GPSH_POSITIONING_ERROR : GpsIfdIndex
    '''Indicates the GPSHPositioningError.'''

class InteroperabilityIFDPointerIndex:
    '''Defines ids of InteroperabilityIFDPointer tags.'''
    
    TAG_INTEROP_INDEX : InteroperabilityIFDPointerIndex
    '''Indicates the TagInteropIndex.'''
    TAG_INTEROP_VERSION : InteroperabilityIFDPointerIndex
    '''Indicates the TagInteropVersion.'''

class RawExifIndex:
    '''Defines ids of RawExif tags.'''
    
    EXPOSURE_TIME : RawExifIndex
    '''Indicates the ExposureTime.'''
    F_NUMBER : RawExifIndex
    '''Indicates the FNumber.'''
    EXPOSURE_PROGRAM : RawExifIndex
    '''Indicates the ExposureProgram.'''
    SPECTRAL_SENSITIVITY : RawExifIndex
    '''Indicates the SpectralSensitivity.'''
    PHOTOGRAPHIC_SENSITIVITY : RawExifIndex
    '''Indicates the PhotographicSensitivity.'''
    OECF : RawExifIndex
    '''Indicates the OECF.'''
    SENSITIVITY_TYPE : RawExifIndex
    '''Indicates the SensitivityType.'''
    STANDARD_OUTPUT_SENSITIVITY : RawExifIndex
    '''Indicates the StandardOutputSensitivity.'''
    RECOMMENDED_EXPOSURE_INDEX : RawExifIndex
    '''Indicates the RecommendedExposureIndex.'''
    ISO_SPEED : RawExifIndex
    '''Indicates the ISOSpeed.'''
    ISO_SPEED_LATITUDEYYY : RawExifIndex
    '''Indicates the ISOSpeedLatitudeyyy.'''
    ISO_SPEED_LATITUDEZZZ : RawExifIndex
    '''Indicates the ISOSpeedLatitudezzz.'''
    EXIF_VERSION : RawExifIndex
    '''Indicates the ExifVersion.'''
    DATE_TIME_ORIGINAL : RawExifIndex
    '''Indicates the DateTimeOriginal.'''
    DATE_TIME_DIGITIZED : RawExifIndex
    '''Indicates the DateTimeDigitized.'''
    OFFSET_TIME : RawExifIndex
    '''Indicates the OffsetTime.'''
    OFFSET_TIME_ORIGINAL : RawExifIndex
    '''Indicates the OffsetTimeOriginal.'''
    OFFSET_TIME_DIGITIZED : RawExifIndex
    '''Indicates the OffsetTimeDigitized.'''
    COMPONENTS_CONFIGURATION : RawExifIndex
    '''Indicates the ComponentsConfiguration.'''
    SHUTTER_SPEED_VALUE : RawExifIndex
    '''Indicates the ShutterSpeedValue.'''
    APERTURE_VALUE : RawExifIndex
    '''Indicates the ApertureValue.'''
    BRIGHTNESS_VALUE : RawExifIndex
    '''Indicates the BrightnessValue.'''
    EXPOSURE_BIAS_VALUE : RawExifIndex
    '''Indicates the ExposureBiasValue.'''
    MAX_APERTURE_VALUE : RawExifIndex
    '''Indicates the MaxApertureValue.'''
    SUBJECT_DISTANCE : RawExifIndex
    '''Indicates the SubjectDistance.'''
    METERING_MODE : RawExifIndex
    '''Indicates the MeteringMode.'''
    LIGHT_SOURCE : RawExifIndex
    '''Indicates the LightSource.'''
    FLASH : RawExifIndex
    '''Indicates the Flash.'''
    FOCAL_LENGTH : RawExifIndex
    '''Indicates the FocalLength.'''
    SUBJECT_AREA : RawExifIndex
    '''Indicates the SubjectArea.'''
    MAKER_NOTE : RawExifIndex
    '''Indicates the MakerNote.'''
    USER_COMMENT : RawExifIndex
    '''Indicates the UserComment.'''
    SUB_SEC_TIME : RawExifIndex
    '''Indicates the SubSecTime.'''
    SUB_SEC_TIME_ORIGINAL : RawExifIndex
    '''Indicates the SubSecTimeOriginal.'''
    SUB_SEC_TIME_DIGITIZED : RawExifIndex
    '''Indicates the SubSecTimeDigitized.'''
    TEMPERATURE : RawExifIndex
    '''Indicates the Temperature.'''
    HUMIDITY : RawExifIndex
    '''Indicates the Humidity.'''
    PRESSURE : RawExifIndex
    '''Indicates the Pressure.'''
    WATER_DEPTH : RawExifIndex
    '''Indicates the WaterDepth.'''
    ACCELERATION : RawExifIndex
    '''Indicates the Acceleration.'''
    CAMERA_ELEVATION_ANGLE : RawExifIndex
    '''Indicates the CameraElevationAngle.'''
    FLASHPIX_VERSION : RawExifIndex
    '''Indicates the FlashpixVersion.'''
    COLOR_SPACE : RawExifIndex
    '''Indicates the ColorSpace.'''
    PIXEL_X_DIMENSION : RawExifIndex
    '''Indicates the PixelXDimension.'''
    PIXEL_Y_DIMENSION : RawExifIndex
    '''Indicates the PixelYDimension.'''
    RELATED_SOUND_FILE : RawExifIndex
    '''Indicates the RelatedSoundFile.'''
    INTEROPERABILITY_IFD_POINTER : RawExifIndex
    '''Indicates the InteroperabilityIFDPointer.'''
    FLASH_ENERGY : RawExifIndex
    '''Indicates the FlashEnergy.'''
    SPATIAL_FREQUENCY_RESPONSE : RawExifIndex
    '''Indicates the SpatialFrequencyResponse.'''
    FOCAL_PLANE_X_RESOLUTION : RawExifIndex
    '''Indicates the FocalPlaneXResolution.'''
    FOCAL_PLANE_Y_RESOLUTION : RawExifIndex
    '''Indicates the FocalPlaneYResolution.'''
    FOCAL_PLANE_RESOLUTION_UNIT : RawExifIndex
    '''Indicates the FocalPlaneResolutionUnit.'''
    SUBJECT_LOCATION : RawExifIndex
    '''Indicates the SubjectLocation.'''
    EXPOSURE_INDEX : RawExifIndex
    '''Indicates the ExposureIndex.'''
    SENSING_METHOD : RawExifIndex
    '''Indicates the SensingMethod.'''
    FILE_SOURCE : RawExifIndex
    '''Indicates the FileSource.'''
    SCENE_TYPE : RawExifIndex
    '''Indicates the SceneType.'''
    CFA_PATTERN : RawExifIndex
    '''Indicates the CFAPattern.'''
    CUSTOM_RENDERED : RawExifIndex
    '''Indicates the CustomRendered.'''
    EXPOSURE_MODE : RawExifIndex
    '''Indicates the ExposureMode.'''
    WHITE_BALANCE : RawExifIndex
    '''Indicates the WhiteBalance.'''
    DIGITAL_ZOOM_RATIO : RawExifIndex
    '''Indicates the DigitalZoomRatio.'''
    FOCAL_LENGTH_IN_35MM_FILM : RawExifIndex
    '''Indicates the FocalLengthIn35mmFilm.'''
    SCENE_CAPTURE_TYPE : RawExifIndex
    '''Indicates the SceneCaptureType.'''
    GAIN_CONTROL : RawExifIndex
    '''Indicates the GainControl.'''
    CONTRAST : RawExifIndex
    '''Indicates the Contrast.'''
    SATURATION : RawExifIndex
    '''Indicates the Saturation.'''
    SHARPNESS : RawExifIndex
    '''Indicates the Sharpness.'''
    DEVICE_SETTING_DESCRIPTION : RawExifIndex
    '''Indicates the DeviceSettingDescription.'''
    SUBJECT_DISTANCE_RANGE : RawExifIndex
    '''Indicates the SubjectDistanceRange.'''
    IMAGE_UNIQUE_ID : RawExifIndex
    '''Indicates the ImageUniqueID.'''
    CAMERA_OWNER_NAME : RawExifIndex
    '''Indicates the CameraOwnerName.'''
    BODY_SERIAL_NUMBER : RawExifIndex
    '''Indicates the BodySerialNumber.'''
    LENS_SPECIFICATION : RawExifIndex
    '''Indicates the LensSpecification.'''
    LENS_MAKE : RawExifIndex
    '''Indicates the LensMake.'''
    LENS_MODEL : RawExifIndex
    '''Indicates the LensModel.'''
    LENS_SERIAL_NUMBER : RawExifIndex
    '''Indicates the LensSerialNumber.'''
    COMPOSITE_IMAGE : RawExifIndex
    '''Indicates the CompositeImage.'''
    SOURCE_IMAGE_NUMBER_OF_COMPOSITE_IMAGE : RawExifIndex
    '''Indicates the SourceImageNumberOfCompositeImage.'''
    SOURCE_EXPOSURE_TIMES_OF_COMPOSITE_IMAGE : RawExifIndex
    '''Indicates the SourceExposureTimesOfCompositeImage.'''
    GAMMA : RawExifIndex
    '''Indicates the Gamma.'''

class RawTagType:
    '''Represents the IFD data type.'''
    
    BYTE : RawTagType
    '''An 8-bit unsigned integer.'''
    ASCII : RawTagType
    '''An 8-bit byte with a 7-bit ASCII character.'''
    SHORT : RawTagType
    '''A 16-bit unsigned integer.'''
    LONG : RawTagType
    '''A 32-bit unsigned integer.'''
    RATIONAL : RawTagType
    '''A pair of LONGs, numerator then denominator.'''
    S_BYTE : RawTagType
    '''An 8-bit signed integer.'''
    UNDEFINED : RawTagType
    '''An undefined 8-bit byte.'''
    S_SHORT : RawTagType
    '''A 16-bit signed integer.'''
    S_LONG : RawTagType
    '''A 32-bit signed integer.'''
    S_RATIONAL : RawTagType
    '''A pair of SLONGs, numerator then denominator.'''
    FLOAT : RawTagType
    '''A 4-byte IEEE floating point value.'''
    DOUBLE : RawTagType
    '''An 8-byte IEEE floating point value.'''
    SUB_IFD : RawTagType
    '''A 4-byte long offset value'''

