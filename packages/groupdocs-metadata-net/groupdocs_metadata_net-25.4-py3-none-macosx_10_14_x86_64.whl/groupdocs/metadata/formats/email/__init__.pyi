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

class EmailAttachmentPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents a metadata package containing email attachment name.'''
    
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
    def name(self) -> str:
        '''Gets the attachment name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Gets the attachment name.'''
        raise NotImplementedError()
    

class EmailHeaderPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents a metadata package containing email message headers.'''
    
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
    
    def get(self, header : str) -> str:
        '''Gets the value of the specified header.
        
        :param header: An email header.
        :returns: The value if the package contains the specified header; otherwise, null.'''
        raise NotImplementedError()
    
    def set(self, header : str, value : groupdocs.metadata.common.PropertyValue) -> None:
        '''Set the value of the specified header.
        
        :param header: An email header.
        :param value: An email header value.'''
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
    

class EmailPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents email message metadata.'''
    
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
    def subject(self) -> str:
        '''Gets the email subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets the email subject.'''
        raise NotImplementedError()
    
    @property
    def recipients(self) -> List[str]:
        '''Gets the array of the email recipients.'''
        raise NotImplementedError()
    
    @recipients.setter
    def recipients(self, value : List[str]) -> None:
        '''Sets the array of the email recipients.'''
        raise NotImplementedError()
    
    @property
    def carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @carbon_copy_recipients.setter
    def carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def blind_carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @blind_carbon_copy_recipients.setter
    def blind_carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def sender_email_address(self) -> str:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @sender_email_address.setter
    def sender_email_address(self, value : str) -> None:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @property
    def headers(self) -> groupdocs.metadata.formats.email.EmailHeaderPackage:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    
    @headers.setter
    def headers(self, value : groupdocs.metadata.formats.email.EmailHeaderPackage) -> None:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    

class EmailRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an email message.'''
    
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
    
    def clear_attachments(self) -> None:
        '''Removes all the attachments form the email message.'''
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
    def email_package(self) -> groupdocs.metadata.formats.email.EmailPackage:
        '''Gets the email metadata package.'''
        raise NotImplementedError()
    

class EmlPackage(EmailPackage):
    '''Represents EML message metadata.'''
    
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
    def subject(self) -> str:
        '''Gets the email subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets the email subject.'''
        raise NotImplementedError()
    
    @property
    def recipients(self) -> List[str]:
        '''Gets the array of the email recipients.'''
        raise NotImplementedError()
    
    @recipients.setter
    def recipients(self, value : List[str]) -> None:
        '''Sets the array of the email recipients.'''
        raise NotImplementedError()
    
    @property
    def carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @carbon_copy_recipients.setter
    def carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def blind_carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @blind_carbon_copy_recipients.setter
    def blind_carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def sender_email_address(self) -> str:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @sender_email_address.setter
    def sender_email_address(self, value : str) -> None:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @property
    def headers(self) -> groupdocs.metadata.formats.email.EmailHeaderPackage:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    
    @headers.setter
    def headers(self, value : groupdocs.metadata.formats.email.EmailHeaderPackage) -> None:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    
    @property
    def attachments(self) -> List[groupdocs.metadata.formats.email.EmailAttachmentPackage]:
        '''Gets an array of the attached files.'''
        raise NotImplementedError()
    
    @attachments.setter
    def attachments(self, value : List[groupdocs.metadata.formats.email.EmailAttachmentPackage]) -> None:
        '''Gets an array of the attached files.'''
        raise NotImplementedError()
    

class EmlRootPackage(EmailRootPackage):
    '''Represents the root package allowing working with metadata in an EML email message.'''
    
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
    
    def clear_attachments(self) -> None:
        '''Removes all the attachments form the email message.'''
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
    def email_package(self) -> groupdocs.metadata.formats.email.EmlPackage:
        '''Gets the EML metadata package.'''
        raise NotImplementedError()
    

class MsgAttachmentPackage(EmailAttachmentPackage):
    '''Represents a metadata package containing email attachment name and data.'''
    
    def __init__(self, name : str, content : List[int]) -> None:
        '''MsgAttachmentPackage constructor
        
        :param name: Attachment name
        :param content: Attachment file which byte[]'''
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
    def name(self) -> str:
        '''Gets the attachment name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Gets the attachment name.'''
        raise NotImplementedError()
    
    @property
    def content(self) -> List[int]:
        '''Gets the last attachment data on byte array.'''
        raise NotImplementedError()
    
    @content.setter
    def content(self, value : List[int]) -> None:
        '''Gets the last attachment data on byte array.'''
        raise NotImplementedError()
    

class MsgPackage(EmailPackage):
    '''Represents MSG message metadata.'''
    
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
    def subject(self) -> str:
        '''Gets the email subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets the email subject.'''
        raise NotImplementedError()
    
    @property
    def recipients(self) -> List[str]:
        '''Gets the array of the email recipients.'''
        raise NotImplementedError()
    
    @recipients.setter
    def recipients(self, value : List[str]) -> None:
        '''Sets the array of the email recipients.'''
        raise NotImplementedError()
    
    @property
    def carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @carbon_copy_recipients.setter
    def carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of CC (carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def blind_carbon_copy_recipients(self) -> List[str]:
        '''Gets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @blind_carbon_copy_recipients.setter
    def blind_carbon_copy_recipients(self, value : List[str]) -> None:
        '''Sets the array of BCC (blind carbon copy) recipients of the email message.'''
        raise NotImplementedError()
    
    @property
    def sender_email_address(self) -> str:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @sender_email_address.setter
    def sender_email_address(self, value : str) -> None:
        '''Gets the email address of the sender.'''
        raise NotImplementedError()
    
    @property
    def headers(self) -> groupdocs.metadata.formats.email.EmailHeaderPackage:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    
    @headers.setter
    def headers(self, value : groupdocs.metadata.formats.email.EmailHeaderPackage) -> None:
        '''Gets a metadata package containing the email headers.'''
        raise NotImplementedError()
    
    @property
    def body(self) -> str:
        '''Gets the email message text.'''
        raise NotImplementedError()
    
    @body.setter
    def body(self, value : str) -> None:
        '''Gets the email message text.'''
        raise NotImplementedError()
    
    @property
    def categories(self) -> List[str]:
        '''Gets the array of categories or keywords.'''
        raise NotImplementedError()
    
    @categories.setter
    def categories(self, value : List[str]) -> None:
        '''Gets the array of categories or keywords.'''
        raise NotImplementedError()
    
    @property
    def delivery_time(self) -> datetime:
        '''Gets the date and time the message was delivered.'''
        raise NotImplementedError()
    
    @delivery_time.setter
    def delivery_time(self, value : datetime) -> None:
        '''Gets the date and time the message was delivered.'''
        raise NotImplementedError()
    
    @property
    def client_submit_time(self) -> datetime:
        '''Gets the date and time the message was submit.'''
        raise NotImplementedError()
    
    @client_submit_time.setter
    def client_submit_time(self, value : datetime) -> None:
        '''Gets the date and time the message was submit.'''
        raise NotImplementedError()
    
    @property
    def sender_name(self) -> str:
        '''Gets the name of the sender.'''
        raise NotImplementedError()
    
    @sender_name.setter
    def sender_name(self, value : str) -> None:
        '''Gets the name of the sender.'''
        raise NotImplementedError()
    
    @property
    def internet_message_id(self) -> str:
        '''Gets the message id of the message.'''
        raise NotImplementedError()
    
    @property
    def billing(self) -> str:
        '''Contains the billing information associated with an item.'''
        raise NotImplementedError()
    
    @billing.setter
    def billing(self, value : str) -> None:
        '''Contains the billing information associated with an item.'''
        raise NotImplementedError()
    
    @property
    def body_html(self) -> str:
        '''Gets the BodyRtf of the message converted to HTML, if present, otherwise an empty string.'''
        raise NotImplementedError()
    
    @body_html.setter
    def body_html(self, value : str) -> None:
        '''Gets the BodyRtf of the message converted to HTML, if present, otherwise an empty string.'''
        raise NotImplementedError()
    
    @property
    def body_rtf(self) -> str:
        '''Gets the BodyRtf of the message.'''
        raise NotImplementedError()
    
    @body_rtf.setter
    def body_rtf(self, value : str) -> None:
        '''Gets the BodyRtf of the message.'''
        raise NotImplementedError()
    
    @property
    def conversation_topic(self) -> str:
        '''Gets the Conversation Topic.'''
        raise NotImplementedError()
    
    @property
    def display_bcc(self) -> str:
        '''Gets the Display Bcc.'''
        raise NotImplementedError()
    
    @property
    def display_cc(self) -> str:
        '''Gets the Display Cc.'''
        raise NotImplementedError()
    
    @property
    def display_name(self) -> str:
        '''Gets the Display Name.'''
        raise NotImplementedError()
    
    @property
    def display_name_prefix(self) -> str:
        '''Gets the Display Name Prefix.'''
        raise NotImplementedError()
    
    @property
    def display_to(self) -> str:
        '''Gets the Display To.'''
        raise NotImplementedError()
    
    @property
    def is_encrypted(self) -> bool:
        '''Gets the Is Encrypted.'''
        raise NotImplementedError()
    
    @property
    def is_signed(self) -> bool:
        '''Gets the Is Signed.'''
        raise NotImplementedError()
    
    @property
    def is_template(self) -> bool:
        '''Gets the Is Template.'''
        raise NotImplementedError()
    
    @property
    def normalized_subject(self) -> str:
        '''Gets the Normalized Subject.'''
        raise NotImplementedError()
    
    @property
    def read_receipt_requested(self) -> bool:
        '''Gets the Read Receipt Requested.'''
        raise NotImplementedError()
    
    @read_receipt_requested.setter
    def read_receipt_requested(self, value : bool) -> None:
        '''Gets the Read Receipt Requested.'''
        raise NotImplementedError()
    
    @property
    def reply_to(self) -> str:
        '''Gets the Reply To.'''
        raise NotImplementedError()
    
    @reply_to.setter
    def reply_to(self, value : str) -> None:
        '''Gets the Reply To.'''
        raise NotImplementedError()
    
    @property
    def sender_address_type(self) -> str:
        '''Gets the Sender Address Type.'''
        raise NotImplementedError()
    
    @property
    def sender_smtp_address(self) -> str:
        '''Gets the Sender Smtp Address.'''
        raise NotImplementedError()
    
    @sender_smtp_address.setter
    def sender_smtp_address(self, value : str) -> None:
        '''Gets the Sender Smtp Address.'''
        raise NotImplementedError()
    
    @property
    def sent_representing_address_type(self) -> str:
        '''Gets the Sent Representing Address Type.'''
        raise NotImplementedError()
    
    @property
    def sent_representing_email_address(self) -> str:
        '''Gets the Sent Representing Email Address.'''
        raise NotImplementedError()
    
    @sent_representing_email_address.setter
    def sent_representing_email_address(self, value : str) -> None:
        '''Gets the Sent Representing Email Address.'''
        raise NotImplementedError()
    
    @property
    def sent_representing_name(self) -> str:
        '''Gets the Sent Representing Name.'''
        raise NotImplementedError()
    
    @sent_representing_name.setter
    def sent_representing_name(self, value : str) -> None:
        '''Gets the Sent Representing Name.'''
        raise NotImplementedError()
    
    @property
    def sent_representing_smtp_address(self) -> str:
        '''Gets the Sent Representing Smtp Address.'''
        raise NotImplementedError()
    
    @property
    def transport_message_headers(self) -> str:
        '''Gets the Transport Message Headers.'''
        raise NotImplementedError()
    
    @property
    def mileage(self) -> str:
        '''Gets the Mileage.'''
        raise NotImplementedError()
    
    @mileage.setter
    def mileage(self, value : str) -> None:
        '''Gets the Mileage.'''
        raise NotImplementedError()
    
    @property
    def subject_prefix(self) -> str:
        '''Gets the Subject Prefix.'''
        raise NotImplementedError()
    
    @property
    def attachments(self) -> List[groupdocs.metadata.formats.email.MsgAttachmentPackage]:
        '''Gets an array of the attached files.'''
        raise NotImplementedError()
    
    @attachments.setter
    def attachments(self, value : List[groupdocs.metadata.formats.email.MsgAttachmentPackage]) -> None:
        '''Gets an array of the attached files.'''
        raise NotImplementedError()
    

class MsgRootPackage(EmailRootPackage):
    '''Represents the root package allowing working with metadata in an MSG email message.'''
    
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
    
    def clear_attachments(self) -> None:
        '''Removes all the attachments form the email message.'''
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
    def email_package(self) -> groupdocs.metadata.formats.email.MsgPackage:
        '''Gets the MSG metadata package.'''
        raise NotImplementedError()
    

