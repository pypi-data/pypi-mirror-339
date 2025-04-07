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

class EpubPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents metadata in a EPUB e-book.'''
    
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
    def image_cover(self) -> List[int]:
        '''Gets the image cover as an array of bytes.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''Gets the EPUB version.'''
        raise NotImplementedError()
    
    @property
    def unique_identifier(self) -> str:
        '''Gets the package unique identifier.'''
        raise NotImplementedError()
    
    @property
    def abstract(self) -> str:
        '''Gets a summary of the resource.'''
        raise NotImplementedError()
    
    @abstract.setter
    def abstract(self, value : str) -> None:
        '''Sets a summary of the resource.'''
        raise NotImplementedError()
    
    @property
    def access_rights(self) -> str:
        '''Gets the information about who access the resource or an indication of its security status.'''
        raise NotImplementedError()
    
    @access_rights.setter
    def access_rights(self, value : str) -> None:
        '''Sets the information about who access the resource or an indication of its security status.'''
        raise NotImplementedError()
    
    @property
    def accrual_method(self) -> str:
        '''Gets the method by which items are added to a collection.'''
        raise NotImplementedError()
    
    @accrual_method.setter
    def accrual_method(self, value : str) -> None:
        '''Sets the method by which items are added to a collection.'''
        raise NotImplementedError()
    
    @property
    def accrual_periodicity(self) -> str:
        '''Gets the frequency with which items are added to a collection.'''
        raise NotImplementedError()
    
    @accrual_periodicity.setter
    def accrual_periodicity(self, value : str) -> None:
        '''Sets the frequency with which items are added to a collection.'''
        raise NotImplementedError()
    
    @property
    def accrual_policy(self) -> str:
        '''Gets the policy governing the addition of items to a collection.'''
        raise NotImplementedError()
    
    @accrual_policy.setter
    def accrual_policy(self, value : str) -> None:
        '''Sets the policy governing the addition of items to a collection.'''
        raise NotImplementedError()
    
    @property
    def alternative(self) -> str:
        '''Gets an alternative name for the resource.'''
        raise NotImplementedError()
    
    @alternative.setter
    def alternative(self, value : str) -> None:
        '''Sets an alternative name for the resource.'''
        raise NotImplementedError()
    
    @property
    def audience(self) -> str:
        '''Gets a class of agents for whom the resource is intended or useful.'''
        raise NotImplementedError()
    
    @audience.setter
    def audience(self, value : str) -> None:
        '''Sets a class of agents for whom the resource is intended or useful.'''
        raise NotImplementedError()
    
    @property
    def available(self) -> str:
        '''Gets the date that the resource became or will become available.'''
        raise NotImplementedError()
    
    @available.setter
    def available(self, value : str) -> None:
        '''Sets the date that the resource became or will become available.'''
        raise NotImplementedError()
    
    @property
    def bibliographic_citation(self) -> str:
        '''Gets a bibliographic reference for the resource.'''
        raise NotImplementedError()
    
    @bibliographic_citation.setter
    def bibliographic_citation(self, value : str) -> None:
        '''Sets a bibliographic reference for the resource.'''
        raise NotImplementedError()
    
    @property
    def conforms_to(self) -> str:
        '''Gets an established standard to which the described resource conforms.'''
        raise NotImplementedError()
    
    @conforms_to.setter
    def conforms_to(self, value : str) -> None:
        '''Sets an established standard to which the described resource conforms.'''
        raise NotImplementedError()
    
    @property
    def contributor(self) -> str:
        '''Gets an entity responsible for making contributions to the resource.'''
        raise NotImplementedError()
    
    @contributor.setter
    def contributor(self, value : str) -> None:
        '''Sets an entity responsible for making contributions to the resource.'''
        raise NotImplementedError()
    
    @property
    def coverage(self) -> str:
        '''Gets the spatial or temporal topic of the resource, spatial applicability of the resource, or jurisdiction under which the resource is relevant.'''
        raise NotImplementedError()
    
    @coverage.setter
    def coverage(self, value : str) -> None:
        '''Sets the spatial or temporal topic of the resource, spatial applicability of the resource, or jurisdiction under which the resource is relevant.'''
        raise NotImplementedError()
    
    @property
    def created(self) -> str:
        '''Gets the date of creation of the resource.'''
        raise NotImplementedError()
    
    @created.setter
    def created(self, value : str) -> None:
        '''Sets the date of creation of the resource.'''
        raise NotImplementedError()
    
    @property
    def creator(self) -> str:
        '''Gets an entity responsible for making the resource.'''
        raise NotImplementedError()
    
    @creator.setter
    def creator(self, value : str) -> None:
        '''Sets an entity responsible for making the resource.'''
        raise NotImplementedError()
    
    @property
    def date(self) -> str:
        '''Gets a point or period of time associated with an event in the lifecycle of the resource.'''
        raise NotImplementedError()
    
    @date.setter
    def date(self, value : str) -> None:
        '''Sets a point or period of time associated with an event in the lifecycle of the resource.'''
        raise NotImplementedError()
    
    @property
    def date_accepted(self) -> str:
        '''Gets the date of acceptance of the resource.'''
        raise NotImplementedError()
    
    @date_accepted.setter
    def date_accepted(self, value : str) -> None:
        '''Sets the date of acceptance of the resource.'''
        raise NotImplementedError()
    
    @property
    def date_copyrighted(self) -> str:
        '''Gets the date of copyright of the resource.'''
        raise NotImplementedError()
    
    @date_copyrighted.setter
    def date_copyrighted(self, value : str) -> None:
        '''Sets the date of copyright of the resource.'''
        raise NotImplementedError()
    
    @property
    def date_submitted(self) -> str:
        '''Gets the date of submission of the resource.'''
        raise NotImplementedError()
    
    @date_submitted.setter
    def date_submitted(self, value : str) -> None:
        '''Sets the date of submission of the resource.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets an account of the resource.'''
        raise NotImplementedError()
    
    @description.setter
    def description(self, value : str) -> None:
        '''Sets an account of the resource.'''
        raise NotImplementedError()
    
    @property
    def education_level(self) -> str:
        '''Gets a class of agents, defined in terms of progression through an educational or training context, for which the described resource is intended.'''
        raise NotImplementedError()
    
    @education_level.setter
    def education_level(self, value : str) -> None:
        '''Sets a class of agents, defined in terms of progression through an educational or training context, for which the described resource is intended.'''
        raise NotImplementedError()
    
    @property
    def extent(self) -> str:
        '''Gets the size or duration of the resource.'''
        raise NotImplementedError()
    
    @extent.setter
    def extent(self, value : str) -> None:
        '''Sets the size or duration of the resource.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> str:
        '''Gets the file format, physical medium, or dimensions of the resource.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : str) -> None:
        '''Sets the file format, physical medium, or dimensions of the resource.'''
        raise NotImplementedError()
    
    @property
    def has_format(self) -> str:
        '''Gets a related resource that is substantially the same as the pre-existing described resource, but in another format.'''
        raise NotImplementedError()
    
    @has_format.setter
    def has_format(self, value : str) -> None:
        '''Sets a related resource that is substantially the same as the pre-existing described resource, but in another format.'''
        raise NotImplementedError()
    
    @property
    def has_part(self) -> str:
        '''Gets a related resource that is included either physically or logically in the described resource.'''
        raise NotImplementedError()
    
    @has_part.setter
    def has_part(self, value : str) -> None:
        '''Sets a related resource that is included either physically or logically in the described resource.'''
        raise NotImplementedError()
    
    @property
    def has_version(self) -> str:
        '''Gets a related resource that is a version, edition, or adaptation of the described resource.'''
        raise NotImplementedError()
    
    @has_version.setter
    def has_version(self, value : str) -> None:
        '''Sets a related resource that is a version, edition, or adaptation of the described resource.'''
        raise NotImplementedError()
    
    @property
    def identifier(self) -> str:
        '''Gets an unambiguous reference to the resource within a given context.'''
        raise NotImplementedError()
    
    @identifier.setter
    def identifier(self, value : str) -> None:
        '''Sets an unambiguous reference to the resource within a given context.'''
        raise NotImplementedError()
    
    @property
    def instructional_method(self) -> str:
        '''Gets a process, used to engender knowledge, attitudes and skills, that the described resource is designed to support.'''
        raise NotImplementedError()
    
    @instructional_method.setter
    def instructional_method(self, value : str) -> None:
        '''Sets a process, used to engender knowledge, attitudes and skills, that the described resource is designed to support.'''
        raise NotImplementedError()
    
    @property
    def is_format_of(self) -> str:
        '''Gets a pre-existing related resource that is substantially the same as the described resource, but in another format.'''
        raise NotImplementedError()
    
    @is_format_of.setter
    def is_format_of(self, value : str) -> None:
        '''Sets a pre-existing related resource that is substantially the same as the described resource, but in another format.'''
        raise NotImplementedError()
    
    @property
    def is_part_of(self) -> str:
        '''Gets a related resource in which the described resource is physically or logically included.'''
        raise NotImplementedError()
    
    @is_part_of.setter
    def is_part_of(self, value : str) -> None:
        '''Sets a related resource in which the described resource is physically or logically included.'''
        raise NotImplementedError()
    
    @property
    def is_referenced_by(self) -> str:
        '''Gets a related resource that references, cites, or otherwise points to the described resource.'''
        raise NotImplementedError()
    
    @is_referenced_by.setter
    def is_referenced_by(self, value : str) -> None:
        '''Sets a related resource that references, cites, or otherwise points to the described resource.'''
        raise NotImplementedError()
    
    @property
    def is_replaced_by(self) -> str:
        '''Gets a related resource that supplants, displaces, or supersedes the described resource.'''
        raise NotImplementedError()
    
    @is_replaced_by.setter
    def is_replaced_by(self, value : str) -> None:
        '''Sets a related resource that supplants, displaces, or supersedes the described resource.'''
        raise NotImplementedError()
    
    @property
    def is_required_by(self) -> str:
        '''Gets a related resource that requires the described resource to support its function, delivery, or coherence.'''
        raise NotImplementedError()
    
    @is_required_by.setter
    def is_required_by(self, value : str) -> None:
        '''Sets a related resource that requires the described resource to support its function, delivery, or coherence.'''
        raise NotImplementedError()
    
    @property
    def issued(self) -> str:
        '''Gets the date of formal issuance of the resource.'''
        raise NotImplementedError()
    
    @issued.setter
    def issued(self, value : str) -> None:
        '''Sets the date of formal issuance of the resource.'''
        raise NotImplementedError()
    
    @property
    def is_version_of(self) -> str:
        '''Gets a related resource of which the described resource is a version, edition, or adaptation.'''
        raise NotImplementedError()
    
    @is_version_of.setter
    def is_version_of(self, value : str) -> None:
        '''Sets a related resource of which the described resource is a version, edition, or adaptation.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the resource.'''
        raise NotImplementedError()
    
    @language.setter
    def language(self, value : str) -> None:
        '''Sets the language of the resource.'''
        raise NotImplementedError()
    
    @property
    def license(self) -> str:
        '''Gets a legal document giving official permission to do something with the resource.'''
        raise NotImplementedError()
    
    @license.setter
    def license(self, value : str) -> None:
        '''Sets a legal document giving official permission to do something with the resource.'''
        raise NotImplementedError()
    
    @property
    def mediator(self) -> str:
        '''Gets an entity that mediates access to the resource.'''
        raise NotImplementedError()
    
    @mediator.setter
    def mediator(self, value : str) -> None:
        '''Sets an entity that mediates access to the resource.'''
        raise NotImplementedError()
    
    @property
    def medium(self) -> str:
        '''Gets the material or physical carrier of the resource.'''
        raise NotImplementedError()
    
    @medium.setter
    def medium(self, value : str) -> None:
        '''Sets the material or physical carrier of the resource.'''
        raise NotImplementedError()
    
    @property
    def modified(self) -> str:
        '''Gets the date on which the resource was changed.'''
        raise NotImplementedError()
    
    @modified.setter
    def modified(self, value : str) -> None:
        '''Sets the date on which the resource was changed.'''
        raise NotImplementedError()
    
    @property
    def provenance(self) -> str:
        '''Gets a statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity, and interpretation.'''
        raise NotImplementedError()
    
    @provenance.setter
    def provenance(self, value : str) -> None:
        '''Sets a statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity, and interpretation.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> str:
        '''Gets an entity responsible for making the resource available.'''
        raise NotImplementedError()
    
    @publisher.setter
    def publisher(self, value : str) -> None:
        '''Sets an entity responsible for making the resource available.'''
        raise NotImplementedError()
    
    @property
    def references(self) -> str:
        '''Gets a related resource that is referenced, cited, or otherwise pointed to by the described resource.'''
        raise NotImplementedError()
    
    @references.setter
    def references(self, value : str) -> None:
        '''Sets a related resource that is referenced, cited, or otherwise pointed to by the described resource.'''
        raise NotImplementedError()
    
    @property
    def relation(self) -> str:
        '''Gets a related resource.'''
        raise NotImplementedError()
    
    @relation.setter
    def relation(self, value : str) -> None:
        '''Sets a related resource.'''
        raise NotImplementedError()
    
    @property
    def replaces(self) -> str:
        '''Gets a related resource that is supplanted, displaced, or superseded by the described resource.'''
        raise NotImplementedError()
    
    @replaces.setter
    def replaces(self, value : str) -> None:
        '''Sets a related resource that is supplanted, displaced, or superseded by the described resource.'''
        raise NotImplementedError()
    
    @property
    def requires(self) -> str:
        '''Gets a related resource that is required by the described resource to support its function, delivery, or coherence.'''
        raise NotImplementedError()
    
    @requires.setter
    def requires(self, value : str) -> None:
        '''Sets a related resource that is required by the described resource to support its function, delivery, or coherence.'''
        raise NotImplementedError()
    
    @property
    def rights(self) -> str:
        '''Gets the information about rights held in and over the resource.'''
        raise NotImplementedError()
    
    @rights.setter
    def rights(self, value : str) -> None:
        '''Sets the information about rights held in and over the resource.'''
        raise NotImplementedError()
    
    @property
    def rights_holder(self) -> str:
        '''Gets a person or organization owning or managing rights over the resource.'''
        raise NotImplementedError()
    
    @rights_holder.setter
    def rights_holder(self, value : str) -> None:
        '''Sets a person or organization owning or managing rights over the resource.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> str:
        '''Gets a related resource from which the described resource is derived.'''
        raise NotImplementedError()
    
    @source.setter
    def source(self, value : str) -> None:
        '''Sets a related resource from which the described resource is derived.'''
        raise NotImplementedError()
    
    @property
    def spatial(self) -> str:
        '''Gets the spatial characteristics of the resource.'''
        raise NotImplementedError()
    
    @spatial.setter
    def spatial(self, value : str) -> None:
        '''Sets the spatial characteristics of the resource.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets a topic of the resource.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets a topic of the resource.'''
        raise NotImplementedError()
    
    @property
    def table_of_contents(self) -> str:
        '''Gets a list of subunits of the resource.'''
        raise NotImplementedError()
    
    @table_of_contents.setter
    def table_of_contents(self, value : str) -> None:
        '''Sets a list of subunits of the resource.'''
        raise NotImplementedError()
    
    @property
    def temporal(self) -> str:
        '''Gets the temporal characteristics of the resource.'''
        raise NotImplementedError()
    
    @temporal.setter
    def temporal(self, value : str) -> None:
        '''Sets the temporal characteristics of the resource.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets a name given to the resource.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets a name given to the resource.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> str:
        '''Gets the nature or genre of the resource.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : str) -> None:
        '''Sets the nature or genre of the resource.'''
        raise NotImplementedError()
    
    @property
    def valid(self) -> str:
        '''Gets the date (often a range) of validity of a resource.'''
        raise NotImplementedError()
    
    @valid.setter
    def valid(self, value : str) -> None:
        '''Sets the date (often a range) of validity of a resource.'''
        raise NotImplementedError()
    

class EpubRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an EPUB e-book.'''
    
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
    def epub_package(self) -> groupdocs.metadata.formats.ebook.EpubPackage:
        '''Gets the EPUB metadata package.'''
        raise NotImplementedError()
    
    @property
    def dublin_core_package(self) -> groupdocs.metadata.standards.dublincore.DublinCorePackage:
        '''Gets the Dublin Core metadata package extracted from the e-book.'''
        raise NotImplementedError()
    

class Fb2RootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an Fb2 e-book.'''
    
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
    def fb_2_package(self) -> groupdocs.metadata.formats.fb2.Fb2Package:
        '''Gets the Fb2 metadata package.'''
        raise NotImplementedError()
    

