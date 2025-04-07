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

class ConsoleLogger(ILogger):
    '''Writes log messages to the console.'''
    
    def __init__(self) -> None:
        '''The default constructor.'''
        raise NotImplementedError()
    
    def trace(self, message : str) -> None:
        '''Writes trace log message; Trace log messages provides generally useful information about application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message; Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    

class FileLogger(ILogger):
    '''Writes log messages to the file.'''
    
    def __init__(self, file_name : str) -> None:
        '''Create logger to file.
        
        :param file_name: Full file name with path.'''
        raise NotImplementedError()
    
    def trace(self, message : str) -> None:
        '''Writes trace log message; Trace log messages provides generally useful information about application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message; Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    

class ILogger:
    '''Defines the methods that are used to perform logging.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace log message; Trace log messages provides generally useful information about application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message; Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The error message.'''
        raise NotImplementedError()
    

class Logging:
    '''The class provides work with logger.'''
    
    @staticmethod
    def start(logger : groupdocs.metadata.logging.ILogger) -> None:
        '''Start logging.
        
        :param logger: The error message.'''
        raise NotImplementedError()
    
    @staticmethod
    def stop() -> None:
        '''Stop logging.'''
        raise NotImplementedError()
    

