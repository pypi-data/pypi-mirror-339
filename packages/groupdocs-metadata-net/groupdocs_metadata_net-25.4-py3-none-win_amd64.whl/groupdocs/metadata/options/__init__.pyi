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

class LoadOptions:
    '''Allows a developer to specify additional options (such as a password) when loading a file.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.options.LoadOptions` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, file_format : groupdocs.metadata.common.FileFormat) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.options.LoadOptions` class.
        
        :param file_format: The exact type of the file.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Gets the password for opening an encrypted document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Sets the password for opening an encrypted document.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> groupdocs.metadata.common.FileFormat:
        '''Gets the exact type of the file that is to be loaded.
        The default value is :py:attr:`groupdocs.metadata.common.FileFormat.UNKNOWN` which means that the type should be detected automatically.'''
        raise NotImplementedError()
    

class PreviewOptions:
    '''Provides options to sets requirements and stream delegates for preview generation.'''
    
    @property
    def cache_folder(self) -> str:
        '''Gets the cache folder.
        By default the cache folder is set to user\'s local temp directory.'''
        raise NotImplementedError()
    
    @cache_folder.setter
    def cache_folder(self, value : str) -> None:
        '''Sets the cache folder.
        By default the cache folder is set to user\'s local temp directory.'''
        raise NotImplementedError()
    
    @property
    def max_disk_space_for_cache(self) -> int:
        '''Gets the maximum available disk space for cache in bytes.
        The default value is 1073741824.'''
        raise NotImplementedError()
    
    @max_disk_space_for_cache.setter
    def max_disk_space_for_cache(self, value : int) -> None:
        '''Sets the maximum available disk space for cache in bytes.
        The default value is 1073741824.'''
        raise NotImplementedError()
    
    @property
    def max_memory_for_cache(self) -> int:
        '''Gets the maximum available memory for cache in memory in bytes.
        The default value is 1073741824.'''
        raise NotImplementedError()
    
    @max_memory_for_cache.setter
    def max_memory_for_cache(self, value : int) -> None:
        '''Sets the maximum available memory for cache in memory in bytes.
        The default value is 1073741824.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the page preview width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the page preview width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the page preview height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the page preview height.'''
        raise NotImplementedError()
    
    @property
    def page_numbers(self) -> List[int]:
        '''Gets an array of page numbers to generate previews.'''
        raise NotImplementedError()
    
    @page_numbers.setter
    def page_numbers(self, value : List[int]) -> None:
        '''Sets an array of page numbers to generate previews.'''
        raise NotImplementedError()
    
    @property
    def preview_format(self) -> PreviewOptions.PreviewFormats:
        '''Gets the preview image format.'''
        raise NotImplementedError()
    
    @preview_format.setter
    def preview_format(self, value : PreviewOptions.PreviewFormats) -> None:
        '''Sets the preview image format.'''
        raise NotImplementedError()
    
    @property
    def resolution(self) -> int:
        '''Gets the page preview resolution.'''
        raise NotImplementedError()
    
    @resolution.setter
    def resolution(self, value : int) -> None:
        '''Sets the page preview resolution.'''
        raise NotImplementedError()
    

