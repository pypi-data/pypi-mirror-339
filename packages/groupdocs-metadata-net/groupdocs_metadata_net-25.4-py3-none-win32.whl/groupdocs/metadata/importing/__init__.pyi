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

class ImportManager:
    '''Provides a row of methods allowing the user to import metadata properties to various formats.'''
    
    def __init__(self, root_metadata_package : groupdocs.metadata.common.RootMetadataPackage) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.importing.ImportManager` class.
        
        :param root_metadata_package: A collection of metadata properties where the import will be performed.'''
        raise NotImplementedError()
    
    @overload
    def import_metadata(self, file_path : str, format : groupdocs.metadata.importing.ImportFormat, import_options : groupdocs.metadata.importing.ImportOptions) -> None:
        '''Imports the metadata properties to a file.
        
        :param file_path: The full name of the input file.
        :param format: The format of the input file.
        :param import_options: Additional options to use when importing.'''
        raise NotImplementedError()
    
    @overload
    def import_metadata(self, stream : io._IOBase, format : groupdocs.metadata.importing.ImportFormat, import_options : groupdocs.metadata.importing.ImportOptions) -> None:
        '''Imports the metadata properties to a file.
        
        :param stream: The filestream of the input file.
        :param format: The format of the input file.
        :param import_options: Additional options to use when importing.'''
        raise NotImplementedError()
    

class ImportOptions:
    '''Abstract class import options.'''
    

class JsonImportOptions(ImportOptions):
    '''Creates an import options from json file.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.importing.JsonImportOptions` class.'''
        raise NotImplementedError()
    

class ImportFormat:
    '''Defines file formats to which you can import metadata properties.'''
    
    JSON : ImportFormat
    '''Represents the .JSON format.'''

