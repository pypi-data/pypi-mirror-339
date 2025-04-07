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

class IIptc:
    '''Represents base operations intended to work with IPTC metadata.
    Please find more information at `http://en.wikipedia.org/wiki/International_Press_Telecommunications_Council <http://en.wikipedia.org/wiki/International_Press_Telecommunications_Council>`.'''
    
    @property
    def iptc_package(self) -> groupdocs.metadata.standards.iptc.IptcRecordSet:
        '''Gets the IPTC metadata package associated with the file.'''
        raise NotImplementedError()
    
    @iptc_package.setter
    def iptc_package(self, value : groupdocs.metadata.standards.iptc.IptcRecordSet) -> None:
        '''Sets the IPTC metadata package associated with the file.'''
        raise NotImplementedError()
    

class IptcApplicationRecord(IptcRecord):
    '''Represents an IPTC Application Record.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcApplicationRecord` class.'''
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.standards.iptc.IptcDataSet]:
        '''Creates a list from the package.
        
        :returns: A list that contains all IPTC dataSets from the package.'''
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
    def record_number(self) -> int:
        '''Gets the record number.'''
        raise NotImplementedError()
    
    @property
    def by_line(self) -> str:
        '''Gets the name of the creator of the object, e.g. writer, photographer or graphic artist.'''
        raise NotImplementedError()
    
    @by_line.setter
    def by_line(self, value : str) -> None:
        '''Sets the name of the creator of the object, e.g. writer, photographer or graphic artist.'''
        raise NotImplementedError()
    
    @property
    def by_lines(self) -> List[str]:
        '''Gets the names of the creators of the object, e.g. writer, photographer or graphic artist.'''
        raise NotImplementedError()
    
    @by_lines.setter
    def by_lines(self, value : List[str]) -> None:
        '''Sets the names of the creators of the object, e.g. writer, photographer or graphic artist.'''
        raise NotImplementedError()
    
    @property
    def by_line_title(self) -> str:
        '''Gets the title of the creator or creators of the object.'''
        raise NotImplementedError()
    
    @by_line_title.setter
    def by_line_title(self, value : str) -> None:
        '''Sets the title of the creator or creators of the object.'''
        raise NotImplementedError()
    
    @property
    def by_line_titles(self) -> List[str]:
        '''Gets the titles of the creator or creators of the object.'''
        raise NotImplementedError()
    
    @by_line_titles.setter
    def by_line_titles(self, value : List[str]) -> None:
        '''Sets the titles of the creator or creators of the object.'''
        raise NotImplementedError()
    
    @property
    def content_location_code(self) -> str:
        '''Gets the content location code.'''
        raise NotImplementedError()
    
    @content_location_code.setter
    def content_location_code(self, value : str) -> None:
        '''Sets the content location code.'''
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
    def content_location_name(self) -> str:
        '''Gets the content location name.'''
        raise NotImplementedError()
    
    @content_location_name.setter
    def content_location_name(self, value : str) -> None:
        '''Sets the content location name.'''
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
    def date_created(self) -> Optional[datetime]:
        '''Gets the date the intellectual content of the object was created.'''
        raise NotImplementedError()
    
    @date_created.setter
    def date_created(self, value : Optional[datetime]) -> None:
        '''Sets the date the intellectual content of the object was created.'''
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
    def reference_dates(self) -> List[datetime]:
        '''Gets the dates of a prior envelope to which the current object refers.'''
        raise NotImplementedError()
    
    @property
    def release_date(self) -> Optional[datetime]:
        '''Gets the release date.'''
        raise NotImplementedError()
    
    @release_date.setter
    def release_date(self, value : Optional[datetime]) -> None:
        '''Sets the release date.'''
        raise NotImplementedError()
    
    @property
    def credit(self) -> str:
        '''Gets information about the provider of the object, not necessarily the owner/creator.'''
        raise NotImplementedError()
    
    @credit.setter
    def credit(self, value : str) -> None:
        '''Sets information about the provider of the object, not necessarily the owner/creator.'''
        raise NotImplementedError()
    
    @property
    def headline(self) -> str:
        '''Gets a publishable entry providing a synopsis of the contents of the object.'''
        raise NotImplementedError()
    
    @headline.setter
    def headline(self, value : str) -> None:
        '''Sets a publishable entry providing a synopsis of the contents of the object.'''
        raise NotImplementedError()
    
    @property
    def copyright_notice(self) -> str:
        '''Gets the copyright notice.'''
        raise NotImplementedError()
    
    @copyright_notice.setter
    def copyright_notice(self, value : str) -> None:
        '''Sets the copyright notice.'''
        raise NotImplementedError()
    
    @property
    def contact(self) -> str:
        '''Gets information about the person or organisation which can provide further background information on the object.'''
        raise NotImplementedError()
    
    @contact.setter
    def contact(self, value : str) -> None:
        '''Sets information about the person or organisation which can provide further background information on the object.'''
        raise NotImplementedError()
    
    @property
    def contacts(self) -> List[str]:
        '''Gets information about the person or organisation which can provide further background information on the object.'''
        raise NotImplementedError()
    
    @contacts.setter
    def contacts(self, value : List[str]) -> None:
        '''Sets information about the person or organisation which can provide further background information on the object.'''
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
    def caption_abstract(self) -> str:
        '''Gets a textual description of the object, particularly used where the object is not text.'''
        raise NotImplementedError()
    
    @caption_abstract.setter
    def caption_abstract(self, value : str) -> None:
        '''Sets a textual description of the object, particularly used where the object is not text.'''
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
    def all_keywords(self) -> List[str]:
        '''Gets the keywords.'''
        raise NotImplementedError()
    
    @all_keywords.setter
    def all_keywords(self, value : List[str]) -> None:
        '''Sets the keywords.'''
        raise NotImplementedError()
    
    @property
    def program_version(self) -> str:
        '''Gets the program version.'''
        raise NotImplementedError()
    
    @program_version.setter
    def program_version(self, value : str) -> None:
        '''Sets the program version.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.standards.iptc.IptcDataSet:
        raise NotImplementedError()
    

class IptcDataSet(groupdocs.metadata.common.MetadataProperty):
    '''Represents an IPTC DataSet (metadata property).'''
    
    @overload
    def __init__(self, record_number : int, data_set_number : int, value : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcDataSet` class.
        
        :param record_number: The record number.
        :param data_set_number: The dataSet number.
        :param value: A byte array value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, record_number : int, data_set_number : int, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcDataSet` class.
        
        :param record_number: The record number.
        :param data_set_number: The dataSet number.
        :param value: A string value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, record_number : int, data_set_number : int, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcDataSet` class.
        
        :param record_number: The record number.
        :param data_set_number: The dataSet number.
        :param value: An integer value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, record_number : int, data_set_number : int, value : datetime) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcDataSet` class.
        
        :param record_number: The record number.
        :param data_set_number: The dataSet number.
        :param value: A date value.'''
        raise NotImplementedError()
    
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
    def record_number(self) -> int:
        '''Gets the record number.'''
        raise NotImplementedError()
    
    @property
    def data_set_number(self) -> int:
        '''Gets the dataSet number.'''
        raise NotImplementedError()
    
    @property
    def alternative_name(self) -> str:
        '''Gets the alternative name of the dataSet.'''
        raise NotImplementedError()
    

class IptcEnvelopeRecord(IptcRecord):
    '''Represents an IPTC Envelope Record.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcEnvelopeRecord` class.'''
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.standards.iptc.IptcDataSet]:
        '''Creates a list from the package.
        
        :returns: A list that contains all IPTC dataSets from the package.'''
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
    def record_number(self) -> int:
        '''Gets the record number.'''
        raise NotImplementedError()
    
    @property
    def model_version(self) -> Optional[int]:
        '''Gets a number identifying the version of the information.'''
        raise NotImplementedError()
    
    @model_version.setter
    def model_version(self, value : Optional[int]) -> None:
        '''Sets a number identifying the version of the information.'''
        raise NotImplementedError()
    
    @property
    def destination(self) -> str:
        '''Gets the destination.'''
        raise NotImplementedError()
    
    @destination.setter
    def destination(self, value : str) -> None:
        '''Sets the destination.'''
        raise NotImplementedError()
    
    @property
    def destinations(self) -> List[str]:
        '''Gets an array of destinations.'''
        raise NotImplementedError()
    
    @destinations.setter
    def destinations(self, value : List[str]) -> None:
        '''Sets an array of destinations.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> Optional[int]:
        '''Gets the file format.'''
        raise NotImplementedError()
    
    @file_format.setter
    def file_format(self, value : Optional[int]) -> None:
        '''Sets the file format.'''
        raise NotImplementedError()
    
    @property
    def file_format_version(self) -> Optional[int]:
        '''Gets the file format version.
        A number representing the particular version of the File Format specified in :py:attr:`groupdocs.metadata.standards.iptc.IptcEnvelopeRecord.file_format`.'''
        raise NotImplementedError()
    
    @file_format_version.setter
    def file_format_version(self, value : Optional[int]) -> None:
        '''Sets the file format version.
        A number representing the particular version of the File Format specified in :py:attr:`groupdocs.metadata.standards.iptc.IptcEnvelopeRecord.file_format`.'''
        raise NotImplementedError()
    
    @property
    def service_identifier(self) -> str:
        '''Gets the service identifier.'''
        raise NotImplementedError()
    
    @service_identifier.setter
    def service_identifier(self, value : str) -> None:
        '''Sets the service identifier.'''
        raise NotImplementedError()
    
    @property
    def product_id(self) -> str:
        '''Gets the product identifier.'''
        raise NotImplementedError()
    
    @product_id.setter
    def product_id(self, value : str) -> None:
        '''Sets the product identifier.'''
        raise NotImplementedError()
    
    @property
    def product_ids(self) -> List[str]:
        '''Gets the product identifiers.'''
        raise NotImplementedError()
    
    @product_ids.setter
    def product_ids(self, value : List[str]) -> None:
        '''Sets the product identifiers.'''
        raise NotImplementedError()
    
    @property
    def date_sent(self) -> Optional[datetime]:
        '''Gets the date the service sent the material.'''
        raise NotImplementedError()
    
    @date_sent.setter
    def date_sent(self, value : Optional[datetime]) -> None:
        '''Sets the date the service sent the material.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.standards.iptc.IptcDataSet:
        raise NotImplementedError()
    

class IptcRecord(groupdocs.metadata.common.CustomPackage):
    '''Represents an IPTC record.'''
    
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.standards.iptc.IptcDataSet]:
        '''Creates a list from the package.
        
        :returns: A list that contains all IPTC dataSets from the package.'''
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
    def record_number(self) -> int:
        '''Gets the record number.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.standards.iptc.IptcDataSet:
        raise NotImplementedError()
    

class IptcRecordSet(groupdocs.metadata.common.CustomPackage):
    '''Represents a collection of IPTC records.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcRecordSet` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data_sets : List[groupdocs.metadata.standards.iptc.IptcDataSet]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.standards.iptc.IptcRecordSet` class.
        
        :param data_sets: An array of IPTC dataSets.'''
        raise NotImplementedError()
    
    @overload
    def remove(self, record_number : int, data_set_number : int) -> bool:
        '''Removes the dataSet with the specified record and dataSet number.
        
        :param record_number: The record number.
        :param data_set_number: The dataSet number.
        :returns: True if the specified IPTC dataSet is found and removed; otherwise, false.'''
        raise NotImplementedError()
    
    @overload
    def remove(self, record_number : int) -> bool:
        '''Removes the record with the specified record number.
        
        :param record_number: The record number.
        :returns: True if the specified IPTC record is found and removed; otherwise, false.'''
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
    
    def set(self, data_set : groupdocs.metadata.standards.iptc.IptcDataSet) -> None:
        '''Adds or updates the specified dataSet in the appropriate record.
        
        :param data_set: The IPTC dataSet to add/update.'''
        raise NotImplementedError()
    
    def add(self, data_set : groupdocs.metadata.standards.iptc.IptcDataSet) -> None:
        '''Adds the specified dataSet to the appropriate record.
        The dataSet is considered as repeatable if a dataSet with the specified number already exists.
        
        :param data_set: The IPTC dataSet to add.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all records from the collection.'''
        raise NotImplementedError()
    
    def to_data_set_list(self) -> Sequence[groupdocs.metadata.standards.iptc.IptcDataSet]:
        '''Creates a list of dataSets from the package.
        
        :returns: A list that contains all IPTC dataSets from the package.'''
        raise NotImplementedError()
    
    def to_list(self) -> Sequence[groupdocs.metadata.standards.iptc.IptcRecord]:
        '''Creates a list from the package.
        
        :returns: A list that contains all IPTC records from the package.'''
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
    def envelope_record(self) -> groupdocs.metadata.standards.iptc.IptcEnvelopeRecord:
        '''Gets the Envelope Record.'''
        raise NotImplementedError()
    
    @envelope_record.setter
    def envelope_record(self, value : groupdocs.metadata.standards.iptc.IptcEnvelopeRecord) -> None:
        '''Sets the Envelope Record.'''
        raise NotImplementedError()
    
    @property
    def application_record(self) -> groupdocs.metadata.standards.iptc.IptcApplicationRecord:
        '''Gets the Application Record.'''
        raise NotImplementedError()
    
    @application_record.setter
    def application_record(self, value : groupdocs.metadata.standards.iptc.IptcApplicationRecord) -> None:
        '''Sets the Application Record.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.metadata.standards.iptc.IptcRecord:
        raise NotImplementedError()
    

class IptcApplicationRecordDataSet:
    '''Defines IPTC Application Record dataSet numbers.'''
    
    RECORD_VERSION : IptcApplicationRecordDataSet
    '''Represents the record version. Binary. Always 2 in JPEGs.'''
    OBJECT_TYPE_REFERENCE : IptcApplicationRecordDataSet
    '''Object type reference. Used pattern: "/\d{2}:[\w\s]{0,64}?/".'''
    OBJECT_ATTRIBUTE_REFERENCE : IptcApplicationRecordDataSet
    '''The object attribute reference.'''
    OBJECT_NAME : IptcApplicationRecordDataSet
    '''Used as a shorthand reference for the object.'''
    EDIT_STATUS : IptcApplicationRecordDataSet
    '''Status of the objectdata, according to the practice of the provider.'''
    EDITORIAL_UPDATE : IptcApplicationRecordDataSet
    '''Indicates the type of update that this object provides to a previous object.'''
    URGENCY : IptcApplicationRecordDataSet
    '''Specifies the editorial urgency of content and not necessarily the envelope handling priority (see 1:60, Envelope Priority).'''
    SUBJECT_REFERENCE : IptcApplicationRecordDataSet
    '''The subject reference.'''
    CATEGORY : IptcApplicationRecordDataSet
    '''Identifies the subject of the objectdata in the opinion of the provider.'''
    SUPPLEMENTAL_CATEGORY : IptcApplicationRecordDataSet
    '''Supplemental categories further refine the subject of an objectdata.
    
    Only a single supplemental category may be contained in each DataSet. A supplemental category may include any of the recognised categories as used in 2:15.'''
    FIXTURE_IDENTIFIER : IptcApplicationRecordDataSet
    '''The fixture identifier.'''
    KEYWORDS : IptcApplicationRecordDataSet
    '''Used to indicate specific information retrieval words.
    Each keyword uses a single Keywords DataSet. Multiple keywords use multiple Keywords DataSets.'''
    CONTENT_LOCATION_CODE : IptcApplicationRecordDataSet
    '''Indicates the code of a country/geographical location referenced by the content of the object.'''
    CONTENT_LOCATION_NAME : IptcApplicationRecordDataSet
    '''Provides a full, publishable name of a country/geographical location referenced by the content of the object,
    
    according to guidelines of the provider.'''
    RELEASE_DATE : IptcApplicationRecordDataSet
    '''Designates in the form CCYYMMDD the earliest date the provider intends the object to be used. Follows ISO 8601 standard.'''
    RELEASE_TIME : IptcApplicationRecordDataSet
    '''Designates in the form HHMMSS±HHMM the earliest time the provider intends the object to be used. Follows ISO 8601 standard.'''
    EXPIRATION_DATE : IptcApplicationRecordDataSet
    '''Designates in the form CCYYMMDD the latest date the provider or owner intends the objectdata to be used. Follows ISO 8601 standard.'''
    SPECIAL_INSTRUCTIONS : IptcApplicationRecordDataSet
    '''Other editorial instructions concerning the use of the objectdata, such as embargoes and warnings.'''
    ACTION_ADVISED : IptcApplicationRecordDataSet
    '''Indicates the type of action that this object provides to a previous object.'''
    REFERENCE_SERVICE : IptcApplicationRecordDataSet
    '''Identifies the Service Identifier of a prior envelope to which the current object refers.'''
    REFERENCE_DATE : IptcApplicationRecordDataSet
    '''Identifies the date of a prior envelope to which the current object refers.'''
    REFERENCE_NUMBER : IptcApplicationRecordDataSet
    '''Identifies the Envelope Number of a prior envelope to which the current object refers.'''
    DATE_CREATED : IptcApplicationRecordDataSet
    '''Represented in the form CCYYMMDD to designate the date the intellectual content of the objectdata was created rather than the date of the creation of the physical representation.'''
    TIME_CREATED : IptcApplicationRecordDataSet
    '''Represented in the form HHMMSS±HHMM to designate the time the intellectual content of the objectdata
    current source material was created rather than the creation of the physical representation.'''
    DIGITAL_CREATION_DATE : IptcApplicationRecordDataSet
    '''Represented in the form CCYYMMDD to designate the date the digital representation of the objectdata was created.'''
    DIGITAL_CREATION_TIME : IptcApplicationRecordDataSet
    '''Represented in the form HHMMSS±HHMM to designate the time the digital representation of the objectdata was created.'''
    ORIGINATING_PROGRAM : IptcApplicationRecordDataSet
    '''Identifies the type of program used to originate the objectdata.'''
    PROGRAM_VERSION : IptcApplicationRecordDataSet
    '''Used to identify the version of the program mentioned in 2:65. DataSet 2:70 is invalid if 2:65 is not present.'''
    OBJECT_CYCLE : IptcApplicationRecordDataSet
    '''Consisting of an alphabetic character. Where: \'a\' = morning, \'p\' = evening, \'b\' = both.'''
    BYLINE : IptcApplicationRecordDataSet
    '''Contains name of the creator of the objectdata, e.g. writer, photographer or graphic artist.'''
    BYLINE_TITLE : IptcApplicationRecordDataSet
    '''A by-line title is the title of the creator or creators of an object data.'''
    CITY : IptcApplicationRecordDataSet
    '''Identifies city of objectdata origin according to guidelines established by the provider.'''
    SUB_LOCATION : IptcApplicationRecordDataSet
    '''Identifies the location within a city from which the objectdata originates, according to guidelines established by the provider.'''
    PROVINCE_STATE : IptcApplicationRecordDataSet
    '''Identifies Province/State of origin according to guidelines established by the provider.'''
    PRIMARY_LOCATION_CODE : IptcApplicationRecordDataSet
    '''Indicates the code of the country/primary location where the intellectual property of the objectdata was created, e.g. a photo was taken, an event occurred.'''
    PRIMARY_LOCATION_NAME : IptcApplicationRecordDataSet
    '''Provides full, publishable, name of the country/primary location where the intellectual property of the objectdata was created,
    according to guidelines of the provider.'''
    ORIGINAL_TRANSMISSION_REFERENCE : IptcApplicationRecordDataSet
    '''A code representing the location of original transmission according to practices of the provider.'''
    HEADLINE : IptcApplicationRecordDataSet
    '''A publishable entry providing a synopsis of the contents of the objectdata.'''
    CREDIT : IptcApplicationRecordDataSet
    '''Identifies the provider of the objectdata, not necessarily the owner/creator.'''
    SOURCE : IptcApplicationRecordDataSet
    '''The name of a person or party who has a role in the content supply chain.
    This could be an agency, a member of an agency, an individual or a combination.'''
    COPYRIGHT_NOTICE : IptcApplicationRecordDataSet
    '''Contains any necessary copyright notice.'''
    CONTACT : IptcApplicationRecordDataSet
    '''Identifies the person or organization which can provide further background information on the object data.'''
    CAPTION_ABSTRACT : IptcApplicationRecordDataSet
    '''A textual description of the objectdata, particularly used where the object is not text.'''
    WRITER_EDITOR : IptcApplicationRecordDataSet
    '''Identification of the name of the person involved in the writing, editing or correcting the objectdata or caption/abstract.'''
    RASTERIZED_CAPTION : IptcApplicationRecordDataSet
    '''Image width 460 pixels and image height 128 pixels. Scanning direction bottom to top, left to right.'''
    IMAGE_TYPE : IptcApplicationRecordDataSet
    '''The numeric characters 1 to 4 indicate the number of components in an image, in single or multiple envelopes.'''
    IMAGE_ORIENTATION : IptcApplicationRecordDataSet
    '''Indicates the layout of the image area.'''
    LANGUAGE_IDENTIFIER : IptcApplicationRecordDataSet
    '''Describes the major national language of the object, according to the 2-letter codes of ISO 639:1988.'''
    AUDIO_TYPE : IptcApplicationRecordDataSet
    '''The audio type.'''
    AUDIO_SAMPLING_RATE : IptcApplicationRecordDataSet
    '''Sampling rate numeric characters, representing the sampling rate in hertz (Hz).'''
    AUDIO_SAMPLING_RESOLUTION : IptcApplicationRecordDataSet
    '''The number of bits in each audio sample.'''
    AUDIO_DURATION : IptcApplicationRecordDataSet
    '''Duration Designates in the form HHMMSS the running time of an audio object data when played back at the speed at which it was recorded.'''
    AUDIO_OUTCUE : IptcApplicationRecordDataSet
    '''Identifies the content of the end of an audio objectdata, according to guidelines established by the provider.'''
    OBJ_DATA_PREVIEW_FILE_FORMAT : IptcApplicationRecordDataSet
    '''A binary number representing the file format of the ObjectData Preview.'''
    OBJ_DATA_PREVIEW_FILE_FORMAT_VER : IptcApplicationRecordDataSet
    '''A binary number representing the particular version of the ObjectData Preview File Format specified in 2:200.'''
    OBJ_DATA_PREVIEW_DATA : IptcApplicationRecordDataSet
    '''The object data preview.'''

class IptcEnvelopeRecordDataSet:
    '''Defines IPTC Envelope Record dataSet numbers.'''
    
    MODEL_VERSION : IptcEnvelopeRecordDataSet
    '''A binary number identifying the version of the Information
    
    
    Interchange Model, Part I, utilised by the provider. Version numbers are assigned by IPTC and NAA.
    
    
    The version number of this record is four (4).'''
    DESTINATION : IptcEnvelopeRecordDataSet
    '''Optional, repeatable, maximum 1024 octets, consisting of sequentially contiguous graphic characters.
    
    
    This DataSet is to accommodate some providers who require routing information above the appropriate OSI layers.'''
    FILE_FORMAT : IptcEnvelopeRecordDataSet
    '''File format.'''
    FILE_FORMAT_VERSION : IptcEnvelopeRecordDataSet
    '''Mandatory, not repeatable, two octets.
    
    
    A binary number representing the particular version of the File Format specified in 1:20.
    
    
    A list of File Formats, including version cross references, is included as Appendix A.'''
    SERVICE_IDENTIFIER : IptcEnvelopeRecordDataSet
    '''Mandatory, not repeatable. Up to 10 octets, consisting of graphic characters.
    
    
    Identifies the provider and product.'''
    ENVELOPE_NUMBER : IptcEnvelopeRecordDataSet
    '''Mandatory, not repeatable, eight octets, consisting of numeric characters.
    
    
    The characters form a number that will be unique for the date
    specified in 1:70 and for the Service Identifier specified in 1:30.
    
    
    If identical envelope numbers appear with the same date and
    with the same Service Identifier, records 2-9 must be unchanged
    from the original.
    
    
    This is not intended to be a sequential serial
    number reception check.'''
    PRODUCT_ID : IptcEnvelopeRecordDataSet
    '''Optional, repeatable. Up to 32 octets, consisting of graphic characters.
    
    
    Allows a provider to identify subsets of its overall service.
    
    
    Used to provide receiving organization data on which to select, route, or otherwise handle data.'''
    ENVELOPE_PRIORITY : IptcEnvelopeRecordDataSet
    '''Optional, not repeatable. A single octet, consisting of a numeric character.
    
    
    Specifies the envelope handling priority and not the editorial urgency (see 2:10, Urgency).
    \'1\' indicates the most urgent,
    \'5\' the normal urgency,
    and \'8\' the least urgent copy.
    The numeral \'9\' indicates a User Defined Priority.
    The numeral \'0\' is reserved for future use.'''
    DATE_SENT : IptcEnvelopeRecordDataSet
    '''Mandatory, not repeatable. Eight octets, consisting of numeric characters.
    
    
    Uses the format CCYYMMDD (century, year, month, day) as defined in ISO 8601 to indicate year, month and day the service sent the material.'''
    TIME_SENT : IptcEnvelopeRecordDataSet
    '''Uses the format HHMMSS±HHMM where HHMMSS refers to
    local hour, minute and seconds and HHMM refers to hours and
    minutes ahead (+) or behind (-) Universal Coordinated Time as
    described in ISO 8601. This is the time the service sent the
    material.'''
    CODED_CHARACTER_SET : IptcEnvelopeRecordDataSet
    '''Optional, not repeatable, up to 32 octets, consisting of one or
    more control functions used for the announcement, invocation or
    designation of coded character sets. The control functions follow
    the ISO 2022 standard and may consist of the escape control
    character and one or more graphic characters. For more details
    see Appendix C, the IPTC-NAA Code Library.'''
    UNO : IptcEnvelopeRecordDataSet
    '''Invalid (eternal identifier).'''
    ARM_IDENTIFIER : IptcEnvelopeRecordDataSet
    '''The DataSet identifies the Abstract Relationship Method (ARM) which is described
    in a document registered by the originator of the ARM with the IPTC and NAA.'''
    ARM_VERSION : IptcEnvelopeRecordDataSet
    '''Binary number representing the particular version of the ARM specified in DataSet 1:120.'''

class IptcRecordType:
    '''Defines IPTC record types.'''
    
    ENVELOPE_RECORD : IptcRecordType
    '''Represents an Envelope Record.'''
    APPLICATION_RECORD : IptcRecordType
    '''Represents an Application Record.'''

