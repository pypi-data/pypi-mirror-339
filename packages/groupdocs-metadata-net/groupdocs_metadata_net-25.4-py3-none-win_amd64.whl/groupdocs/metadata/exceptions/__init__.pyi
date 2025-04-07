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

class DocumentProtectedException(GroupDocsMetadataException):
    '''The exception that is thrown when document is protected by password.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.DocumentProtectedException` class.'''
        raise NotImplementedError()
    

class GroupDocsMetadataException:
    '''Represents a product-specific exception that is thrown during file processing.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.GroupDocsMetadataException` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, message : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.GroupDocsMetadataException` class.
        
        :param message: The message that describes the error.'''
        raise NotImplementedError()
    

class InvalidFormatException(GroupDocsMetadataException):
    '''The exception that is thrown when a file has an invalid format.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.InvalidFormatException` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, message : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.InvalidFormatException` class.
        
        :param message: The message that describes the error.'''
        raise NotImplementedError()
    

class MetadataValidationException(GroupDocsMetadataException):
    '''The exception that is thrown when validation errors encountered during metadata saving.'''
    
    @property
    def errors(self) -> List[str]:
        '''Gets an array of the validation errors that were encountered during the last metadata saving.'''
        raise NotImplementedError()
    

class XmpException(GroupDocsMetadataException):
    '''The exception that is thrown when XMP has invalid structure.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.XmpException` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, message : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.exceptions.XmpException` class.
        
        :param message: The message.'''
        raise NotImplementedError()
    

