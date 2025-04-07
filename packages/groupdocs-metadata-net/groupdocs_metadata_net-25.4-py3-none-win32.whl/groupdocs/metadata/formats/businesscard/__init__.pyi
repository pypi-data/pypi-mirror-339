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

class VCardAgentRecord(VCardRecord):
    '''Represents vCard Agent record metadata class.'''
    
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Gets the record value.'''
        raise NotImplementedError()
    

class VCardBasePackage(groupdocs.metadata.common.CustomPackage):
    '''Represents the base VCard metadata class.'''
    
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
    

class VCardBinaryRecord(VCardRecord):
    '''Represents vCard binary record metadata class.'''
    
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> List[int]:
        '''Gets the record value.'''
        raise NotImplementedError()
    

class VCardCalendarRecordset(VCardRecordset):
    '''Represents a set of Calendar vCard records.'''
    
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
    def busy_time_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the URIs for the busy time associated with the object.'''
        raise NotImplementedError()
    
    @property
    def busy_time_entries(self) -> List[str]:
        '''Gets the URIs for the busy time associated with the object.'''
        raise NotImplementedError()
    
    @property
    def calendar_address_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the calendar user addresses to which a scheduling request should be sent for the object represented by the vCard.'''
        raise NotImplementedError()
    
    @property
    def calendar_addresses(self) -> List[str]:
        '''Gets the calendar user addresses to which a scheduling request should be sent for the object represented by the vCard.'''
        raise NotImplementedError()
    
    @property
    def calendar_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the URIs for the calendar associated with the object represented by the vCard.'''
        raise NotImplementedError()
    
    @property
    def uri_calendar_entries(self) -> List[str]:
        '''Gets the URIs for the calendar associated with the object represented by the vCard.'''
        raise NotImplementedError()
    

class VCardCard(VCardRecordset):
    '''Represents a single card extracted from a VCard file.'''
    
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
    
    def get_available_groups(self) -> List[str]:
        '''Gets the available group names.
        
        :returns: The available group names.'''
        raise NotImplementedError()
    
    def filter_by_group(self, group_name : str) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Filters all vCard records by the group name passed as a parameter.
        For more information please see the :py:func:`groupdocs.metadata.formats.businesscard.VCardCard.get_available_groups` method.
        
        :param group_name: The name of the group.
        :returns: The filtered vCard instance.'''
        raise NotImplementedError()
    
    def filter_home_tags(self) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Filters all vCard records marked with the HOME tag.
        
        :returns: The filtered vCard instance.'''
        raise NotImplementedError()
    
    def filter_work_tags(self) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Filters all vCard records marked with the WORK tag.
        
        :returns: Filtered vCard instance.'''
        raise NotImplementedError()
    
    def filter_preferred(self) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Filters the preferred records.
        
        :returns: The filtered vCard instance.'''
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
    def general_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardGeneralRecordset:
        '''Gets the general records.'''
        raise NotImplementedError()
    
    @property
    def identification_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardIdentificationRecordset:
        '''Gets the identification records.'''
        raise NotImplementedError()
    
    @property
    def delivery_addressing_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardDeliveryAddressingRecordset:
        '''Gets the delivery addressing records.'''
        raise NotImplementedError()
    
    @property
    def communication_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardCommunicationRecordset:
        '''Gets the communication records.'''
        raise NotImplementedError()
    
    @property
    def geographical_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardGeographicalRecordset:
        '''Gets the geographical records.'''
        raise NotImplementedError()
    
    @property
    def organizational_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardOrganizationalRecordset:
        '''Gets the organizational records.'''
        raise NotImplementedError()
    
    @property
    def explanatory_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardExplanatoryRecordset:
        '''Gets the explanatory records.'''
        raise NotImplementedError()
    
    @property
    def security_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardSecurityRecordset:
        '''Gets the security records.'''
        raise NotImplementedError()
    
    @property
    def calendar_recordset(self) -> groupdocs.metadata.formats.businesscard.VCardCalendarRecordset:
        '''Gets the calendar records.'''
        raise NotImplementedError()
    
    @property
    def extension_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the private extension records.'''
        raise NotImplementedError()
    

class VCardCommunicationRecordset(VCardRecordset):
    '''Represents a set of Communication vCard records.
    These properties describe information about how to communicate with the object the vCard represents.'''
    
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
    def telephone_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the telephone numbers for telephony communication with the object.'''
        raise NotImplementedError()
    
    @property
    def telephones(self) -> List[str]:
        '''Gets the telephone numbers for telephony communication with the object.'''
        raise NotImplementedError()
    
    @property
    def email_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the electronic mail addresses for communication with the object.'''
        raise NotImplementedError()
    
    @property
    def emails(self) -> List[str]:
        '''Gets the electronic mail addresses for communication with the object.'''
        raise NotImplementedError()
    
    @property
    def mailer(self) -> str:
        '''Gets the type of the electronic mail software that is used by the individual associated with the vCard.'''
        raise NotImplementedError()
    
    @property
    def impp_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the URIs for instant messaging and presence protocol communications with the object.'''
        raise NotImplementedError()
    
    @property
    def impp_entries(self) -> List[str]:
        '''Gets the URIs for instant messaging and presence protocol communications with the object.'''
        raise NotImplementedError()
    
    @property
    def language_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the languages that may be used for contacting the object.'''
        raise NotImplementedError()
    
    @property
    def languages(self) -> List[str]:
        '''Gets the languages that may be used for contacting the object.'''
        raise NotImplementedError()
    

class VCardCustomRecord(VCardRecord):
    '''Represents vCard custom record metadata class.'''
    
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the record value.'''
        raise NotImplementedError()
    

class VCardDateTimeRecord(VCardRecord):
    '''Represents vCard date time record metadata class.'''
    
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> datetime:
        '''Gets the record value.'''
        raise NotImplementedError()
    

class VCardDeliveryAddressingRecordset(VCardRecordset):
    '''Represents a set of Delivery Addressing vCard records.
    These types are concerned with information related to
    the delivery addressing or label for the vCard object.'''
    
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
    def address_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the components of the delivery address of the object.'''
        raise NotImplementedError()
    
    @property
    def addresses(self) -> List[str]:
        '''Gets the components of the delivery address of the object.'''
        raise NotImplementedError()
    
    @property
    def label_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing the formatted text corresponding to delivery address of the object.'''
        raise NotImplementedError()
    
    @property
    def labels(self) -> List[str]:
        '''Gets an array containing the formatted text corresponding to delivery address of the object.'''
        raise NotImplementedError()
    

class VCardExplanatoryRecordset(VCardRecordset):
    '''Represents a set of Explanatory vCard records.
    These properties are concerned with additional explanations,
    such as that related to informational notes or revisions specific to the vCard.'''
    
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
    def category_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the application category information about the vCard, also known as "tags".'''
        raise NotImplementedError()
    
    @property
    def categories(self) -> List[str]:
        '''Gets the application category information about the vCard, also known as "tags".'''
        raise NotImplementedError()
    
    @property
    def note_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the supplemental information or comments that are associated with the vCard.'''
        raise NotImplementedError()
    
    @property
    def notes(self) -> List[str]:
        '''Gets the supplemental information or comments that are associated with the vCard.'''
        raise NotImplementedError()
    
    @property
    def product_identifier_record(self) -> groupdocs.metadata.formats.businesscard.VCardTextRecord:
        '''Gets the identifier of the product that created the vCard object.'''
        raise NotImplementedError()
    
    @property
    def product_identifier(self) -> str:
        '''Gets the identifier of the product that created the vCard object.'''
        raise NotImplementedError()
    
    @property
    def revision(self) -> Optional[datetime]:
        '''Gets the revision information about the current vCard.'''
        raise NotImplementedError()
    
    @property
    def sort_string(self) -> str:
        '''Gets the family name or given name text to be used for national-language-specific sorting of the :py:attr:`groupdocs.metadata.formats.businesscard.VCardIdentificationRecordset.formatted_names` and :py:attr:`groupdocs.metadata.formats.businesscard.VCardIdentificationRecordset.name` types.'''
        raise NotImplementedError()
    
    @property
    def sound_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets the digital sound content information that annotates some aspects of the vCard.'''
        raise NotImplementedError()
    
    @property
    def sound_binary_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardBinaryRecord]:
        '''Gets the digital sound content information that annotates some aspects of the vCard.'''
        raise NotImplementedError()
    
    @property
    def binary_sounds(self) -> List[List[int]]:
        '''Gets the digital sound content information that annotates some aspects of the vCard.'''
        raise NotImplementedError()
    
    @property
    def sound_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the digital sound content information that annotates some aspects of the vCard.'''
        raise NotImplementedError()
    
    @property
    def uri_sounds(self) -> List[str]:
        '''Gets the digital sound content information that annotates some aspects of the vCard.'''
        raise NotImplementedError()
    
    @property
    def uid_record(self) -> groupdocs.metadata.formats.businesscard.VCardTextRecord:
        '''Gets the value that represents a globally unique identifier corresponding to the individual or resource associated with the vCard.'''
        raise NotImplementedError()
    
    @property
    def uid(self) -> str:
        '''Gets the value that represents a globally unique identifier corresponding to the individual or resource associated with the vCard.'''
        raise NotImplementedError()
    
    @property
    def pid_identifier_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the global meaning of the local PID source identifier.'''
        raise NotImplementedError()
    
    @property
    def pid_identifiers(self) -> List[str]:
        '''Gets the global meaning of the local PID source identifier.'''
        raise NotImplementedError()
    
    @property
    def url_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array of URLs pointing to websites that represent the person in some way.'''
        raise NotImplementedError()
    
    @property
    def urls(self) -> List[str]:
        '''Gets an array of URLs pointing to websites that represent the person in some way.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''Gets the version of the vCard specification.'''
        raise NotImplementedError()
    

class VCardGeneralRecordset(VCardRecordset):
    '''Represents a set of General vCard records.'''
    
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
    def source_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the array of sources of directory information contained in the content type.'''
        raise NotImplementedError()
    
    @property
    def sources(self) -> List[str]:
        '''Gets an array containing the sources of the directory information contained in the content type.'''
        raise NotImplementedError()
    
    @property
    def name_of_source(self) -> str:
        '''Gets the textual representation of the SOURCE property.'''
        raise NotImplementedError()
    
    @property
    def kind(self) -> str:
        '''Gets the kind of the object.'''
        raise NotImplementedError()
    
    @property
    def xml_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing extended XML-encoded vCard data.'''
        raise NotImplementedError()
    
    @property
    def xml_entries(self) -> List[str]:
        '''Gets an array containing extended XML-encoded vCard data.'''
        raise NotImplementedError()
    

class VCardGeographicalRecordset(VCardRecordset):
    '''Represents a set of Geographical vCard records.
    These properties are concerned with information associated with
    geographical positions or regions associated with the object the vCard represents.'''
    
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
    def time_zone_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the time zones of the object.'''
        raise NotImplementedError()
    
    @property
    def time_zones(self) -> List[str]:
        '''Gets the time zones of the object.'''
        raise NotImplementedError()
    
    @property
    def geographic_position_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the information related to the global positioning of the object.'''
        raise NotImplementedError()
    
    @property
    def geographic_positions(self) -> List[str]:
        '''Gets the information related to the global positioning of the object.'''
        raise NotImplementedError()
    

class VCardIdentificationRecordset(VCardRecordset):
    '''Represents a set of Identification vCard records.
    These types are used to capture information associated with
    the identification and naming of the entity associated with the vCard.'''
    
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
    def formatted_name_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing the formatted text corresponding to the name of the object.'''
        raise NotImplementedError()
    
    @property
    def formatted_names(self) -> List[str]:
        '''Gets an array containing the formatted text corresponding to the name of the object.'''
        raise NotImplementedError()
    
    @property
    def name_record(self) -> groupdocs.metadata.formats.businesscard.VCardTextRecord:
        '''Gets the components of the name of the object.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the components of the name of the object.'''
        raise NotImplementedError()
    
    @property
    def nickname_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing the text corresponding to the nickname of the object.'''
        raise NotImplementedError()
    
    @property
    def nicknames(self) -> List[str]:
        '''Gets an array containing the text corresponding to the nickname of the object.'''
        raise NotImplementedError()
    
    @property
    def photo_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets an array containing the image or photograph information that annotates some aspects of the object.'''
        raise NotImplementedError()
    
    @property
    def photo_binary_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardBinaryRecord]:
        '''Gets an array containing the image or photograph information represented as binary data that annotates some aspects of the object.'''
        raise NotImplementedError()
    
    @property
    def binary_photos(self) -> List[List[int]]:
        '''Gets an array containing the image or photograph information represented as binary data that annotates some aspects of the object.'''
        raise NotImplementedError()
    
    @property
    def photo_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing the image or photograph information represented by URIs that annotates some aspects of the object.'''
        raise NotImplementedError()
    
    @property
    def uri_photos(self) -> List[str]:
        '''Gets an array containing the image or photograph information represented by URIs that annotates some aspects of the object.'''
        raise NotImplementedError()
    
    @property
    def birthdate_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets an array containing the birth date of the object in different representations.'''
        raise NotImplementedError()
    
    @property
    def birthdate_date_time_record(self) -> groupdocs.metadata.formats.businesscard.VCardDateTimeRecord:
        '''Gets the birth date of the object.'''
        raise NotImplementedError()
    
    @property
    def date_time_birthdate(self) -> Optional[datetime]:
        '''Gets the birth date of the object.'''
        raise NotImplementedError()
    
    @property
    def birthdate_text_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets an array containing the birth date of the object in different text representations.'''
        raise NotImplementedError()
    
    @property
    def text_birthdates(self) -> List[str]:
        '''Gets an array containing the birth date of the object in different text representations.'''
        raise NotImplementedError()
    
    @property
    def anniversary_record(self) -> groupdocs.metadata.formats.businesscard.VCardRecord:
        '''Gets the date of marriage, or equivalent, of the object.'''
        raise NotImplementedError()
    
    @property
    def anniversary_date_time_record(self) -> groupdocs.metadata.formats.businesscard.VCardDateTimeRecord:
        '''Gets the date of marriage represented as a single date-and-or-time value.'''
        raise NotImplementedError()
    
    @property
    def date_time_anniversary(self) -> Optional[datetime]:
        '''Gets the date of marriage represented as a single date-and-or-time value.'''
        raise NotImplementedError()
    
    @property
    def anniversary_text_record(self) -> groupdocs.metadata.formats.businesscard.VCardTextRecord:
        '''Gets the date of marriage represented as a single text value.'''
        raise NotImplementedError()
    
    @property
    def text_anniversary(self) -> str:
        '''Gets the date of marriage represented as a single text value.'''
        raise NotImplementedError()
    
    @property
    def gender_record(self) -> groupdocs.metadata.formats.businesscard.VCardTextRecord:
        '''Gets the components of the sex and gender identity of the object.'''
        raise NotImplementedError()
    
    @property
    def gender(self) -> str:
        '''Gets the components of the sex and gender identity of the object.'''
        raise NotImplementedError()
    

class VCardOrganizationalRecordset(VCardRecordset):
    '''Represents a set of Organizational vCard records.
    These properties are concerned with information associated with
    characteristics of the organization or organizational units of
    the object that the vCard represents.'''
    
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
    def title_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the positions or jobs of the object.'''
        raise NotImplementedError()
    
    @property
    def titles(self) -> List[str]:
        '''Gets the positions or jobs of the object.'''
        raise NotImplementedError()
    
    @property
    def role_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the functions or parts played in a particular situation by the object.'''
        raise NotImplementedError()
    
    @property
    def roles(self) -> List[str]:
        '''Gets the functions or parts played in a particular situation by the object.'''
        raise NotImplementedError()
    
    @property
    def logo_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets the graphic images of the logo associated with the object.'''
        raise NotImplementedError()
    
    @property
    def logo_binary_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardBinaryRecord]:
        '''Gets the graphic images of the logo associated with the object.'''
        raise NotImplementedError()
    
    @property
    def binary_logos(self) -> List[List[int]]:
        '''Gets the graphic images of the logo associated with the object.'''
        raise NotImplementedError()
    
    @property
    def logo_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the URIs of the graphic images of the logo associated with the object.'''
        raise NotImplementedError()
    
    @property
    def uri_logos(self) -> List[str]:
        '''Gets the URIs of the graphic images of the logo associated with the object.'''
        raise NotImplementedError()
    
    @property
    def agent_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets the information about another person who will act on behalf of the vCard object.'''
        raise NotImplementedError()
    
    @property
    def agent_object_record(self) -> groupdocs.metadata.formats.businesscard.VCardAgentRecord:
        '''Gets the information about another person who will act on behalf of the vCard object.'''
        raise NotImplementedError()
    
    @property
    def object_agent(self) -> groupdocs.metadata.formats.businesscard.VCardCard:
        '''Gets the information about another person who will act on behalf of the vCard object.'''
        raise NotImplementedError()
    
    @property
    def agent_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the information about another person who will act on behalf of the vCard object.'''
        raise NotImplementedError()
    
    @property
    def uri_agents(self) -> List[str]:
        '''Gets the information about another person who will act on behalf of the vCard object.'''
        raise NotImplementedError()
    
    @property
    def organization_name_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the organizational names and units associated with the object.'''
        raise NotImplementedError()
    
    @property
    def organization_names(self) -> List[str]:
        '''Gets the organizational names and units associated with the object.'''
        raise NotImplementedError()
    
    @property
    def member_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the members in the group this vCard represents.'''
        raise NotImplementedError()
    
    @property
    def members(self) -> List[str]:
        '''Gets the members in the group this vCard represents.'''
        raise NotImplementedError()
    
    @property
    def relationship_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the relationships between another entity and the entity represented by this vCard.'''
        raise NotImplementedError()
    
    @property
    def relationships(self) -> List[str]:
        '''Gets the relationships between another entity and the entity represented by this vCard.'''
        raise NotImplementedError()
    

class VCardPackage(VCardBasePackage):
    '''Represents VCF (Virtual Contact File) electronic business card format metadata.'''
    
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
    def cards(self) -> List[groupdocs.metadata.formats.businesscard.VCardCard]:
        '''Gets an array of the cards extracted from the file.'''
        raise NotImplementedError()
    

class VCardRecord(VCardBasePackage):
    '''Represents abstract vCard record metadata class.'''
    
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    

class VCardRecordset(VCardBasePackage):
    '''Provides a base vCard record union class.'''
    
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
    

class VCardRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in a VCard file.'''
    
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
    def v_card_package(self) -> groupdocs.metadata.formats.businesscard.VCardPackage:
        '''Gets the VCard metadata package.'''
        raise NotImplementedError()
    

class VCardSecurityRecordset(VCardRecordset):
    '''Represents a set of Security vCard records.
    These properties are concerned with the security of
    communication pathways or access to the vCard.'''
    
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
    def access_classification(self) -> str:
        '''Gets the sensitivity of the information in the vCard.'''
        raise NotImplementedError()
    
    @property
    def public_key_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardRecord]:
        '''Gets the public keys or authentication certificates associated with the object.'''
        raise NotImplementedError()
    
    @property
    def public_key_binary_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardBinaryRecord]:
        '''Gets the public keys or authentication certificates associated with the object.'''
        raise NotImplementedError()
    
    @property
    def binary_public_keys(self) -> List[List[int]]:
        '''Gets the public keys or authentication certificates associated with the object.'''
        raise NotImplementedError()
    
    @property
    def public_key_uri_records(self) -> List[groupdocs.metadata.formats.businesscard.VCardTextRecord]:
        '''Gets the public keys or authentication certificates associated with the object.'''
        raise NotImplementedError()
    
    @property
    def uri_public_keys(self) -> List[str]:
        '''Gets the public keys or authentication certificates associated with the object.'''
        raise NotImplementedError()
    

class VCardTextRecord(VCardRecord):
    '''Represents vCard text record metadata class.'''
    
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
    
    def get_readability_value(self, code_page_name : str) -> str:
        '''Gets the readability value.
        
        :param code_page_name: The using encoding code page name or null for ASCII encoding.
        :returns: The readability value.'''
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
    def group(self) -> str:
        '''Gets the grouping value.'''
        raise NotImplementedError()
    
    @property
    def value_parameters(self) -> List[str]:
        '''Gets the value parameters.'''
        raise NotImplementedError()
    
    @property
    def pref_parameter(self) -> Optional[int]:
        '''Gets the preferred parameter.'''
        raise NotImplementedError()
    
    @property
    def alt_id_parameter(self) -> str:
        '''Gets the alternative representations parameter value.'''
        raise NotImplementedError()
    
    @property
    def type_parameters(self) -> List[str]:
        '''Gets the type parameter values.'''
        raise NotImplementedError()
    
    @property
    def encoding_parameter(self) -> str:
        '''Gets the encoding parameter value.'''
        raise NotImplementedError()
    
    @property
    def language_parameter(self) -> str:
        '''Gets the language parameter value.'''
        raise NotImplementedError()
    
    @property
    def anonym_parameters(self) -> List[str]:
        '''Gets the anonymous parameters.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.businesscard.VCardContentType:
        '''Gets the content type of record.'''
        raise NotImplementedError()
    
    @property
    def type_name(self) -> str:
        '''Gets the type of the record.'''
        raise NotImplementedError()
    
    @property
    def media_type_parameter(self) -> str:
        '''Gets the media type parameter value.'''
        raise NotImplementedError()
    
    @property
    def charset_parameter(self) -> str:
        '''Gets the charset parameter.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the record value.'''
        raise NotImplementedError()
    
    @property
    def is_quoted_printable(self) -> bool:
        '''Gets a value indicating whether this instance is quoted printable string.'''
        raise NotImplementedError()
    

class VCardContentType:
    '''Defines vCard record content types.'''
    
    CUSTOM : VCardContentType
    '''The custom content type.'''
    TEXT : VCardContentType
    '''The text content type.'''
    BINARY : VCardContentType
    '''The binary content type.'''
    DATE_TIME : VCardContentType
    '''The date time content type.'''
    AGENT : VCardContentType
    '''The agent content type.'''

