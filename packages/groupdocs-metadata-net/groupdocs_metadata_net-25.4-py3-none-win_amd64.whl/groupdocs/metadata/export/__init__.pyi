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

class CsvExportOptions(ExportOptions):
    '''Creates an export options of xml file.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.export.CsvExportOptions` class.'''
        raise NotImplementedError()
    

class ExcelExportOptions(ExportOptions):
    '''Creates an export options of excel file.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.export.ExcelExportOptions` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, group_cells : bool) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.export.ExcelExportOptions` class.
        
        :param group_cells: Group flag.'''
        raise NotImplementedError()
    
    @property
    def group_cells(self) -> bool:
        '''This flag determines whether it is necessary to group rows when exporting to Excel format'''
        raise NotImplementedError()
    
    @group_cells.setter
    def group_cells(self, value : bool) -> None:
        '''This flag determines whether it is necessary to group rows when exporting to Excel format'''
        raise NotImplementedError()
    

class ExportManager:
    '''Provides a row of methods allowing the user to export metadata properties to various formats.'''
    
    def __init__(self, properties : Iterable[groupdocs.metadata.common.MetadataProperty]) -> None:
        raise NotImplementedError()
    
    @overload
    def export(self, file_path : str, format : groupdocs.metadata.export.ExportFormat, export_options : groupdocs.metadata.export.ExportOptions) -> None:
        '''Exports the metadata properties to a file.
        
        :param file_path: The full name of the output file.
        :param format: The format of the output file.
        :param export_options: Additional options to use when exporting a document.'''
        raise NotImplementedError()
    
    @overload
    def export(self, document : io._IOBase, format : groupdocs.metadata.export.ExportFormat, export_options : groupdocs.metadata.export.ExportOptions) -> None:
        '''Exports the metadata properties to a stream.
        
        :param document: The full name of the output file.
        :param format: The format of the output file.
        :param export_options: Additional options to use when exporting a document.'''
        raise NotImplementedError()
    
    @overload
    def export(self, file_path : str, format : groupdocs.metadata.export.ExportFormat) -> None:
        '''Exports the metadata properties to a file.
        
        :param file_path: The full name of the output file.
        :param format: The format of the output file.'''
        raise NotImplementedError()
    
    @overload
    def export(self, document : io._IOBase, format : groupdocs.metadata.export.ExportFormat) -> None:
        '''Exports the metadata properties to a stream.
        
        :param document: The full name of the output file.
        :param format: The format of the output file.'''
        raise NotImplementedError()
    

class ExportOptions:
    '''Abstract class export options.'''
    

class JsonExportOptions(ExportOptions):
    '''Creates an export options of xml file.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.export.JsonExportOptions` class.'''
        raise NotImplementedError()
    

class XmlExportOptions(ExportOptions):
    '''Creates an export options of xml file.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.export.XmlExportOptions` class.'''
        raise NotImplementedError()
    

class ExportFormat:
    '''Defines file formats to which you can export metadata properties.'''
    
    XLS : ExportFormat
    '''Represents the .XLS Excel format.'''
    XLSX : ExportFormat
    '''Represents the .XLSX Excel format.'''
    XML : ExportFormat
    '''Represents the .XML format.'''
    CSV : ExportFormat
    '''Represents the .CSV format.'''
    JSON : ExportFormat
    '''Represents the .JSON format.'''

