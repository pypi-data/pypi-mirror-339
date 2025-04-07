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

class RawAsciiTag(RawTag):
    '''Represents a Raw ASCII tag.'''
    
    def __init__(self, tag_id : int, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.raw.tag.RawAsciiTag` class.
        
        :param tag_id: The tag identifier.
        :param value: The value.'''
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
    def tag_type(self) -> groupdocs.metadata.formats.raw.RawTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> int:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_value(self) -> str:
        '''Gets the tag value.'''
        raise NotImplementedError()
    

class RawByteTag(RawTag):
    '''Represents an byte-based TIFF tag.'''
    
    def __init__(self, tag_id : int, value : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.image.TiffByteTag` class.
        
        :param tag_id: The tag identifier.
        :param value: The value.'''
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
    def tag_type(self) -> groupdocs.metadata.formats.raw.RawTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> int:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_value(self) -> List[int]:
        raise NotImplementedError()
    

class RawLongTag(RawTag):
    '''Represents a Raw Long tag.'''
    
    def __init__(self, tag_id : int, value : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.raw.tag.RawLongTag` class.
        
        :param tag_id: The tag identifier.
        :param value: The value.'''
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
    def tag_type(self) -> groupdocs.metadata.formats.raw.RawTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> int:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_value(self) -> List[int]:
        raise NotImplementedError()
    

class RawShortTag(RawTag):
    '''Represents a Raw Short tag.'''
    
    def __init__(self, tag_id : int, value : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.raw.tag.RawShortTag` class.
        
        :param tag_id: The tag identifier.
        :param value: The value.'''
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
    def tag_type(self) -> groupdocs.metadata.formats.raw.RawTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> int:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_value(self) -> List[int]:
        raise NotImplementedError()
    

class RawTag(groupdocs.metadata.common.MetadataProperty):
    '''Represents a RawTag property.'''
    
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
    def tag_type(self) -> groupdocs.metadata.formats.raw.RawTagType:
        '''Gets the type of the tag.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> int:
        '''Gets the tag id.'''
        raise NotImplementedError()
    

