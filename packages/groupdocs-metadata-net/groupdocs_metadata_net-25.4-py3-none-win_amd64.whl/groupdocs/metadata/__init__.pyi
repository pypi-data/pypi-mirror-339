
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

class License:
    '''Represents GroupDocs.Metadata license. License class should be applied once per AppDomain.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.License` class.'''
        raise NotImplementedError()
    
    @overload
    def set_license(self, file_path : str) -> None:
        '''Licenses the component.
        
        :param file_path: The absolute path to a license file.'''
        raise NotImplementedError()
    
    @overload
    def set_license(self, stream : io._IOBase) -> None:
        '''Licenses the component.
        
        :param stream: License stream.'''
        raise NotImplementedError()
    

class Metadata:
    '''Provides the main class to access metadata in all supported formats.'''
    
    @overload
    def __init__(self, file_path : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.Metadata` class.
        
        :param file_path: A string that contains the full name of the file from which to create a :py:class:`groupdocs.metadata.Metadata` instance.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document : io._IOBase) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.Metadata` class.
        
        :param document: A stream that contains the document to load.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, file_path : str, load_options : groupdocs.metadata.options.LoadOptions) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.Metadata` class.
        
        :param file_path: A string that contains the full name of the file from which to create a :py:class:`groupdocs.metadata.Metadata` instance.
        :param load_options: Additional options to use when loading a document.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document : io._IOBase, load_options : groupdocs.metadata.options.LoadOptions) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.Metadata` class.
        
        :param document: A stream that contains the document to load.
        :param load_options: Additional options to use when loading a document.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, uri : Uri) -> None:
        raise NotImplementedError()
    
    @overload
    def __init__(self, uri : Uri, load_options : groupdocs.metadata.options.LoadOptions) -> None:
        raise NotImplementedError()
    
    @overload
    def save(self) -> None:
        '''Saves all changes made in the loaded document.'''
        raise NotImplementedError()
    
    @overload
    def save(self, document : io._IOBase) -> None:
        '''Saves the document content into a stream.
        
        :param document: An output stream for the document.'''
        raise NotImplementedError()
    
    @overload
    def save(self, file_path : str) -> None:
        '''Saves the document content to the specified file.
        
        :param file_path: The full name of the output file.'''
        raise NotImplementedError()
    
    @overload
    def copy_to(self, metadata : groupdocs.metadata.common.MetadataPackage) -> None:
        '''Copy known metadata properties from source package to destination package.
        The operation is recursive so it affects all nested packages as well.
        If an existing property its value is updated.
        If there is a known property missing in a destination package it is added to the package.
        If there is a known property missing in a source package it is not remove from destination package. If that need, use Sanitize method before.
        
        :param metadata: A destination metadata package.'''
        raise NotImplementedError()
    
    @overload
    def copy_to(self, metadata : groupdocs.metadata.common.MetadataPackage, tags : List[groupdocs.metadata.tagging.PropertyTag]) -> int:
        raise NotImplementedError()
    
    def get_root_package(self) -> groupdocs.metadata.common.RootMetadataPackage:
        '''Gets the root package providing access to all metadata properties extracted from the file.
        
        :returns: The root package providing access to all metadata properties extracted from the file.'''
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
        This method is a combination of :py:func:`groupdocs.metadata.Metadata.add_properties` and :py:func:`groupdocs.metadata.Metadata.update_properties`.
        If an existing property satisfies the specification its value is updated.
        If there is a known property missing in the package that satisfies the specification it is added to the package.
        
        :param specification: A specification to test each metadata property for a condition.
        :param value: A new value for the filtered properties.
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def sanitize(self) -> int:
        '''Removes writable metadata properties from all detected packages or whole packages if possible.
        The operation is recursive so it affects all nested packages as well.
        
        :returns: The number of affected properties.'''
        raise NotImplementedError()
    
    def generate_preview(self, preview_options : groupdocs.metadata.options.PreviewOptions) -> None:
        '''Creates preview images for specified pages.
        
        :param preview_options: A set of options for preview generation.'''
        raise NotImplementedError()
    
    def get_document_info(self) -> groupdocs.metadata.common.IDocumentInfo:
        '''Gets common information about the loaded document.
        
        :returns: An object representing common document information.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> groupdocs.metadata.common.FileFormat:
        '''Gets the type of the loaded file (if recognized).'''
        raise NotImplementedError()
    

class Metered:
    '''Provides methods to set a metered key.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def set_metered_key(self, public_key : str, private_key : str) -> None:
        '''Sets metered public and private key
        
        :param public_key: public key
        :param private_key: private key'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_quantity() -> float:
        '''Gets the consumption file size.
        
        :returns: The consumption file size.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_credit() -> float:
        '''Gets the consumption credit.
        
        :returns: The consumption credit.'''
        raise NotImplementedError()
    

