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

class ExifDictionaryBasePackage(groupdocs.metadata.common.CustomPackage):
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
    

class ExifGpsPackage(ExifDictionaryBasePackage):
    '''Represents GPS metadata in an EXIF metadata package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.exif.ExifGpsPackage` class.'''
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
    def altitude(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the altitude based on the reference in :py:attr:`groupdocs.metadata.standards.exif.ExifGpsPackage.altitude_ref`.
        The reference unit is meters.'''
        raise NotImplementedError()
    
    @altitude.setter
    def altitude(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the altitude based on the reference in :py:attr:`groupdocs.metadata.standards.exif.ExifGpsPackage.altitude_ref`.
        The reference unit is meters.'''
        raise NotImplementedError()
    
    @property
    def altitude_ref(self) -> Optional[groupdocs.metadata.standards.exif.ExifGpsAltitudeRef]:
        '''Gets the altitude used as the reference altitude. If the reference is sea level and the altitude is above sea level, 0 is given.
        If the altitude is below sea level, a value of 1 is given and the altitude is indicated as an absolute value in the :py:attr:`groupdocs.metadata.standards.exif.ExifGpsPackage.altitude` tag.'''
        raise NotImplementedError()
    
    @altitude_ref.setter
    def altitude_ref(self, value : Optional[groupdocs.metadata.standards.exif.ExifGpsAltitudeRef]) -> None:
        '''Sets the altitude used as the reference altitude. If the reference is sea level and the altitude is above sea level, 0 is given.
        If the altitude is below sea level, a value of 1 is given and the altitude is indicated as an absolute value in the :py:attr:`groupdocs.metadata.standards.exif.ExifGpsPackage.altitude` tag.'''
        raise NotImplementedError()
    
    @property
    def area_information(self) -> List[int]:
        '''Gets the character string recording the name of the GPS area. The first byte indicates the character code used, and this is followed by the name of the GPS area.'''
        raise NotImplementedError()
    
    @area_information.setter
    def area_information(self, value : List[int]) -> None:
        '''Sets the character string recording the name of the GPS area. The first byte indicates the character code used, and this is followed by the name of the GPS area.'''
        raise NotImplementedError()
    
    @property
    def date_stamp(self) -> str:
        '''Gets the character string recording date and time information relative to UTC (Coordinated Universal Time). The format is YYYY:MM:DD.'''
        raise NotImplementedError()
    
    @date_stamp.setter
    def date_stamp(self, value : str) -> None:
        '''Sets the character string recording date and time information relative to UTC (Coordinated Universal Time). The format is YYYY:MM:DD.'''
        raise NotImplementedError()
    
    @property
    def dest_bearing(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the GPS bearing to the destination point.
        The range of values is from 0.00 to 359.99.'''
        raise NotImplementedError()
    
    @dest_bearing.setter
    def dest_bearing(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the GPS bearing to the destination point.
        The range of values is from 0.00 to 359.99.'''
        raise NotImplementedError()
    
    @property
    def dest_bearing_ref(self) -> str:
        '''Gets the GPS reference used for giving the bearing to the destination point.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @dest_bearing_ref.setter
    def dest_bearing_ref(self, value : str) -> None:
        '''Sets the GPS reference used for giving the bearing to the destination point.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @property
    def dest_distance(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the GPS distance to the destination point.'''
        raise NotImplementedError()
    
    @dest_distance.setter
    def dest_distance(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the GPS distance to the destination point.'''
        raise NotImplementedError()
    
    @property
    def dest_distance_ref(self) -> str:
        '''Gets the GPS unit used to express the distance to the destination point.
        \'K\', \'M\' and \'N\' represent kilometers, miles and knots.'''
        raise NotImplementedError()
    
    @dest_distance_ref.setter
    def dest_distance_ref(self, value : str) -> None:
        '''Sets the GPS unit used to express the distance to the destination point.
        \'K\', \'M\' and \'N\' represent kilometers, miles and knots.'''
        raise NotImplementedError()
    
    @property
    def dest_latitude(self) -> List[groupdocs.metadata.formats.image.TiffRational]:
        '''Gets the GPS latitude of the destination point.'''
        raise NotImplementedError()
    
    @dest_latitude.setter
    def dest_latitude(self, value : List[groupdocs.metadata.formats.image.TiffRational]) -> None:
        '''Sets the GPS latitude of the destination point.'''
        raise NotImplementedError()
    
    @property
    def dest_latitude_ref(self) -> str:
        '''Gets the GPS value which indicates whether the latitude of the destination point is north or south latitude.
        The ASCII value \'N\' indicates north latitude, and \'S\' is south latitude.'''
        raise NotImplementedError()
    
    @dest_latitude_ref.setter
    def dest_latitude_ref(self, value : str) -> None:
        '''Sets the GPS value which indicates whether the latitude of the destination point is north or south latitude.
        The ASCII value \'N\' indicates north latitude, and \'S\' is south latitude.'''
        raise NotImplementedError()
    
    @property
    def dest_longitude(self) -> List[groupdocs.metadata.formats.image.TiffRational]:
        '''Gets the GPS longitude of the destination point.'''
        raise NotImplementedError()
    
    @dest_longitude.setter
    def dest_longitude(self, value : List[groupdocs.metadata.formats.image.TiffRational]) -> None:
        '''Sets the GPS longitude of the destination point.'''
        raise NotImplementedError()
    
    @property
    def dest_longitude_ref(self) -> str:
        '''Gets the GPS value which indicates whether the longitude of the destination point is east or west longitude.
        ASCII \'E\' indicates east longitude, and \'W\' is west longitude.'''
        raise NotImplementedError()
    
    @dest_longitude_ref.setter
    def dest_longitude_ref(self, value : str) -> None:
        '''Sets the GPS value which indicates whether the longitude of the destination point is east or west longitude.
        ASCII \'E\' indicates east longitude, and \'W\' is west longitude.'''
        raise NotImplementedError()
    
    @property
    def differential(self) -> Optional[int]:
        '''Gets a GPS value which indicates whether differential correction is applied to the GPS receiver.'''
        raise NotImplementedError()
    
    @differential.setter
    def differential(self, value : Optional[int]) -> None:
        '''Sets a GPS value which indicates whether differential correction is applied to the GPS receiver.'''
        raise NotImplementedError()
    
    @property
    def data_degree_of_precision(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the GPS DOP (data degree of precision).
        An HDOP value is written during two-dimensional measurement, and PDOP during three-dimensional measurement.'''
        raise NotImplementedError()
    
    @data_degree_of_precision.setter
    def data_degree_of_precision(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the GPS DOP (data degree of precision).
        An HDOP value is written during two-dimensional measurement, and PDOP during three-dimensional measurement.'''
        raise NotImplementedError()
    
    @property
    def img_direction(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the GPS direction of the image when it was captured.
        The range of values is from 0.00 to 359.99.'''
        raise NotImplementedError()
    
    @img_direction.setter
    def img_direction(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the GPS direction of the image when it was captured.
        The range of values is from 0.00 to 359.99.'''
        raise NotImplementedError()
    
    @property
    def img_direction_ref(self) -> str:
        '''Gets the GPS reference for giving the direction of the image when it is captured.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @img_direction_ref.setter
    def img_direction_ref(self, value : str) -> None:
        '''Sets the GPS reference for giving the direction of the image when it is captured.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @property
    def latitude(self) -> List[groupdocs.metadata.formats.image.TiffRational]:
        '''Gets the GPS latitude.'''
        raise NotImplementedError()
    
    @latitude.setter
    def latitude(self, value : List[groupdocs.metadata.formats.image.TiffRational]) -> None:
        '''Sets the GPS latitude.'''
        raise NotImplementedError()
    
    @property
    def latitude_ref(self) -> str:
        '''Gets a GPS value indicating whether the latitude is north or south latitude.'''
        raise NotImplementedError()
    
    @latitude_ref.setter
    def latitude_ref(self, value : str) -> None:
        '''Sets a GPS value indicating whether the latitude is north or south latitude.'''
        raise NotImplementedError()
    
    @property
    def longitude(self) -> List[groupdocs.metadata.formats.image.TiffRational]:
        '''Gets the GPS longitude.'''
        raise NotImplementedError()
    
    @longitude.setter
    def longitude(self, value : List[groupdocs.metadata.formats.image.TiffRational]) -> None:
        '''Sets the GPS longitude.'''
        raise NotImplementedError()
    
    @property
    def longitude_ref(self) -> str:
        '''Gets a GPS value indicating whether the longitude is east or west longitude.'''
        raise NotImplementedError()
    
    @longitude_ref.setter
    def longitude_ref(self, value : str) -> None:
        '''Sets a GPS value indicating whether the longitude is east or west longitude.'''
        raise NotImplementedError()
    
    @property
    def map_datum(self) -> str:
        '''Gets the geodetic survey data used by the GPS receiver.'''
        raise NotImplementedError()
    
    @map_datum.setter
    def map_datum(self, value : str) -> None:
        '''Sets the geodetic survey data used by the GPS receiver.'''
        raise NotImplementedError()
    
    @property
    def measure_mode(self) -> str:
        '''Gets the GPS measurement mode.'''
        raise NotImplementedError()
    
    @measure_mode.setter
    def measure_mode(self, value : str) -> None:
        '''Sets the GPS measurement mode.'''
        raise NotImplementedError()
    
    @property
    def processing_method(self) -> List[int]:
        '''Gets a character string recording the name of the method used for location finding.
        The first byte indicates the character code used, and this is followed by the name of the method.'''
        raise NotImplementedError()
    
    @processing_method.setter
    def processing_method(self, value : List[int]) -> None:
        '''Sets a character string recording the name of the method used for location finding.
        The first byte indicates the character code used, and this is followed by the name of the method.'''
        raise NotImplementedError()
    
    @property
    def satellites(self) -> str:
        '''Gets the GPS satellites used for measurements.
        This tag can be used to describe the number of satellites,
        their ID number, angle of elevation, azimuth, SNR and other information in ASCII notation. The format is not
        specified. If the GPS receiver is incapable of taking measurements, value of the tag shall be set to NULL.'''
        raise NotImplementedError()
    
    @satellites.setter
    def satellites(self, value : str) -> None:
        '''Sets the GPS satellites used for measurements.
        This tag can be used to describe the number of satellites,
        their ID number, angle of elevation, azimuth, SNR and other information in ASCII notation. The format is not
        specified. If the GPS receiver is incapable of taking measurements, value of the tag shall be set to NULL.'''
        raise NotImplementedError()
    
    @property
    def speed(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the speed of GPS receiver movement.'''
        raise NotImplementedError()
    
    @speed.setter
    def speed(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the speed of GPS receiver movement.'''
        raise NotImplementedError()
    
    @property
    def speed_ref(self) -> str:
        '''Gets the unit used to express the GPS receiver speed of movement.
        \'K\' \'M\' and \'N\' represents kilometers per hour, miles per hour, and knots.'''
        raise NotImplementedError()
    
    @speed_ref.setter
    def speed_ref(self, value : str) -> None:
        '''Sets the unit used to express the GPS receiver speed of movement.
        \'K\' \'M\' and \'N\' represents kilometers per hour, miles per hour, and knots.'''
        raise NotImplementedError()
    
    @property
    def status(self) -> str:
        '''Gets the status of the GPS receiver when the image is recorded.'''
        raise NotImplementedError()
    
    @status.setter
    def status(self, value : str) -> None:
        '''Sets the status of the GPS receiver when the image is recorded.'''
        raise NotImplementedError()
    
    @property
    def time_stamp(self) -> List[groupdocs.metadata.formats.image.TiffRational]:
        '''Gets the time as UTC (Coordinated Universal Time).
        TimeStamp is expressed as three RATIONAL values giving the hour, minute, and second.'''
        raise NotImplementedError()
    
    @time_stamp.setter
    def time_stamp(self, value : List[groupdocs.metadata.formats.image.TiffRational]) -> None:
        '''Sets the time as UTC (Coordinated Universal Time).
        TimeStamp is expressed as three RATIONAL values giving the hour, minute, and second.'''
        raise NotImplementedError()
    
    @property
    def gps_track(self) -> groupdocs.metadata.formats.image.TiffRational:
        '''Gets the direction of GPS receiver movement.'''
        raise NotImplementedError()
    
    @gps_track.setter
    def gps_track(self, value : groupdocs.metadata.formats.image.TiffRational) -> None:
        '''Sets the direction of GPS receiver movement.'''
        raise NotImplementedError()
    
    @property
    def track_ref(self) -> str:
        '''Gets the reference for giving the direction of GPS receiver movement.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @track_ref.setter
    def track_ref(self, value : str) -> None:
        '''Sets the reference for giving the direction of GPS receiver movement.
        \'T\' denotes true direction and \'M\' is magnetic direction.'''
        raise NotImplementedError()
    
    @property
    def version_id(self) -> List[int]:
        '''Gets the version of GPS IFD.'''
        raise NotImplementedError()
    
    @version_id.setter
    def version_id(self, value : List[int]) -> None:
        '''Sets the version of GPS IFD.'''
        raise NotImplementedError()
    

class ExifIfdPackage(ExifDictionaryBasePackage):
    '''Represents the Exif Image File Directory. Exif IFD is a set of tags for recording Exif-specific attribute information.'''
    
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
    def camera_owner_name(self) -> str:
        '''Gets the camera owner\'s name.'''
        raise NotImplementedError()
    
    @camera_owner_name.setter
    def camera_owner_name(self, value : str) -> None:
        '''Sets the camera owner\'s name.'''
        raise NotImplementedError()
    
    @property
    def body_serial_number(self) -> str:
        '''Gets the camera body serial number.'''
        raise NotImplementedError()
    
    @body_serial_number.setter
    def body_serial_number(self, value : str) -> None:
        '''Sets the camera body serial number.'''
        raise NotImplementedError()
    
    @property
    def cfa_pattern(self) -> List[int]:
        '''Gets the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used.'''
        raise NotImplementedError()
    
    @cfa_pattern.setter
    def cfa_pattern(self, value : List[int]) -> None:
        '''Sets the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used.'''
        raise NotImplementedError()
    
    @property
    def user_comment(self) -> str:
        '''Gets the user comment.'''
        raise NotImplementedError()
    
    @user_comment.setter
    def user_comment(self, value : str) -> None:
        '''Sets the user comment.'''
        raise NotImplementedError()
    

class ExifPackage(ExifDictionaryBasePackage):
    '''Represents an EXIF metadata package (Exchangeable Image File Format).'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.exif.ExifPackage` class.'''
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
    def gps_package(self) -> groupdocs.metadata.standards.exif.ExifGpsPackage:
        '''Gets the GPS data.'''
        raise NotImplementedError()
    
    @property
    def exif_ifd_package(self) -> groupdocs.metadata.standards.exif.ExifIfdPackage:
        '''Gets the EXIF IFD data.'''
        raise NotImplementedError()
    
    @property
    def thumbnail(self) -> List[int]:
        '''Gets the image thumbnail represented as an array of bytes.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the name of the camera owner, photographer or image creator.'''
        raise NotImplementedError()
    
    @artist.setter
    def artist(self, value : str) -> None:
        '''Sets the name of the camera owner, photographer or image creator.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> str:
        '''Gets the copyright notice.'''
        raise NotImplementedError()
    
    @copyright.setter
    def copyright(self, value : str) -> None:
        '''Sets the copyright notice.'''
        raise NotImplementedError()
    
    @property
    def date_time(self) -> str:
        '''Gets the date and time of image creation.
        In the EXIF standard, it is the date and time the file was changed.'''
        raise NotImplementedError()
    
    @date_time.setter
    def date_time(self, value : str) -> None:
        '''Sets the date and time of image creation.
        In the EXIF standard, it is the date and time the file was changed.'''
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
    def image_length(self) -> int:
        '''Gets the number of rows of image data.'''
        raise NotImplementedError()
    
    @image_length.setter
    def image_length(self, value : int) -> None:
        '''Sets the number of rows of image data.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> groupdocs.metadata.standards.exif.ExifOrientation:
        '''Gets the orientation.'''
        raise NotImplementedError()
    
    @orientation.setter
    def orientation(self, value : groupdocs.metadata.standards.exif.ExifOrientation) -> None:
        '''Sets the orientation.'''
        raise NotImplementedError()
    
    @property
    def image_width(self) -> int:
        '''Gets the number of columns of image data, equal to the number of pixels per row.'''
        raise NotImplementedError()
    
    @image_width.setter
    def image_width(self, value : int) -> None:
        '''Sets the number of columns of image data, equal to the number of pixels per row.'''
        raise NotImplementedError()
    
    @property
    def make(self) -> str:
        '''Gets the manufacturer of the recording equipment.
        This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image.'''
        raise NotImplementedError()
    
    @make.setter
    def make(self, value : str) -> None:
        '''Sets the manufacturer of the recording equipment.
        This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image.'''
        raise NotImplementedError()
    
    @property
    def model(self) -> str:
        '''Gets the model name or model number of the equipment.
        This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image.'''
        raise NotImplementedError()
    
    @model.setter
    def model(self, value : str) -> None:
        '''Sets the model name or model number of the equipment.
        This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image.'''
        raise NotImplementedError()
    
    @property
    def software(self) -> str:
        '''Gets the name and version of the software or firmware of the camera or image input device used to generate the image.'''
        raise NotImplementedError()
    
    @software.setter
    def software(self, value : str) -> None:
        '''Sets the name and version of the software or firmware of the camera or image input device used to generate the image.'''
        raise NotImplementedError()
    

class IExif:
    '''Defines base operations intended to work with EXIF metadata.'''
    
    @property
    def exif_package(self) -> groupdocs.metadata.standards.exif.ExifPackage:
        '''Gets the EXIF metadata package associated with the file.'''
        raise NotImplementedError()
    
    @exif_package.setter
    def exif_package(self, value : groupdocs.metadata.standards.exif.ExifPackage) -> None:
        '''Sets the EXIF metadata package associated with the file.'''
        raise NotImplementedError()
    

class ExifGpsAltitudeRef:
    '''Represents a GPS altitude reference.'''
    
    ABOVE_SEA_LEVEL : ExifGpsAltitudeRef
    '''Above sea level.'''
    BELOW_SEA_LEVEL : ExifGpsAltitudeRef
    '''Below sea level.'''

class ExifOrientation:
    '''Exif image orientation.'''
    
    TOP_LEFT : ExifOrientation
    '''Top left. Default orientation.'''
    TOP_RIGHT : ExifOrientation
    '''Top right. Horizontally reversed.'''
    BOTTOM_RIGHT : ExifOrientation
    '''Bottom right. Rotated by 180 degrees.'''
    BOTTOM_LEFT : ExifOrientation
    '''Bottom left. Rotated by 180 degrees and then horizontally reversed.'''
    LEFT_TOP : ExifOrientation
    '''Left top. Rotated by 90 degrees counterclockwise and then horizontally reversed.'''
    RIGHT_TOP : ExifOrientation
    '''Right top. Rotated by 90 degrees clockwise.'''
    RIGHT_BOTTOM : ExifOrientation
    '''Right bottom. Rotated by 90 degrees clockwise and then horizontally reversed.'''
    LEFT_BOTTOM : ExifOrientation
    '''Left bottom. Rotated by 90 degrees counterclockwise.'''

