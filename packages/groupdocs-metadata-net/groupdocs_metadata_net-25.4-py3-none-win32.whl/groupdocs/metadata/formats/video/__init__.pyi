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

class AsfAudioStreamProperty(AsfBaseStreamProperty):
    '''Represents Audio stream property metadata in the ASF media container.'''
    
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
    def stream_type(self) -> groupdocs.metadata.formats.video.AsfStreamType:
        '''Gets the type of this stream.'''
        raise NotImplementedError()
    
    @property
    def stream_number(self) -> int:
        '''Gets the number of this stream.'''
        raise NotImplementedError()
    
    @property
    def start_time(self) -> Optional[int]:
        '''Gets the presentation time of the first object, indicating where this digital media stream
        starts within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def end_time(self) -> Optional[int]:
        '''Gets the presentation time of the last object plus the duration of play, indicating where
        this digital media stream ends within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def bitrate(self) -> Optional[int]:
        '''Gets the leak rate R, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def alternate_bitrate(self) -> Optional[int]:
        '''Gets the leak rate RAlt, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> Optional[groupdocs.metadata.formats.video.AsfExtendedStreamPropertyFlags]:
        '''Gets the flags.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the stream language.'''
        raise NotImplementedError()
    
    @property
    def average_time_per_frame(self) -> Optional[int]:
        '''Gets the average time duration, measured in 100-nanosecond units, of each frame.'''
        raise NotImplementedError()
    
    @property
    def average_bitrate(self) -> Optional[int]:
        '''Gets the average bitrate.'''
        raise NotImplementedError()
    
    @property
    def format_tag(self) -> int:
        '''Gets the unique ID of the codec used to encode the audio data.'''
        raise NotImplementedError()
    
    @property
    def channels(self) -> int:
        '''Gets the number of audio channels.'''
        raise NotImplementedError()
    
    @property
    def samples_per_second(self) -> int:
        '''Gets a value in Hertz (cycles per second) that represents the sampling rate of the audio stream.'''
        raise NotImplementedError()
    
    @property
    def bits_per_sample(self) -> int:
        '''Gets the number of bits per sample of monaural data.'''
        raise NotImplementedError()
    

class AsfBaseDescriptor(groupdocs.metadata.common.MetadataProperty):
    '''Represents an ASF base metadata descriptor object.'''
    
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
    def asf_content_type(self) -> groupdocs.metadata.formats.video.AsfDescriptorType:
        '''Gets the type of the content.'''
        raise NotImplementedError()
    

class AsfBaseStreamProperty(groupdocs.metadata.common.CustomPackage):
    '''Represents base stream property metadata in the ASF media container.'''
    
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
    def stream_type(self) -> groupdocs.metadata.formats.video.AsfStreamType:
        '''Gets the type of this stream.'''
        raise NotImplementedError()
    
    @property
    def stream_number(self) -> int:
        '''Gets the number of this stream.'''
        raise NotImplementedError()
    
    @property
    def start_time(self) -> Optional[int]:
        '''Gets the presentation time of the first object, indicating where this digital media stream
        starts within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def end_time(self) -> Optional[int]:
        '''Gets the presentation time of the last object plus the duration of play, indicating where
        this digital media stream ends within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def bitrate(self) -> Optional[int]:
        '''Gets the leak rate R, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def alternate_bitrate(self) -> Optional[int]:
        '''Gets the leak rate RAlt, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> Optional[groupdocs.metadata.formats.video.AsfExtendedStreamPropertyFlags]:
        '''Gets the flags.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the stream language.'''
        raise NotImplementedError()
    
    @property
    def average_time_per_frame(self) -> Optional[int]:
        '''Gets the average time duration, measured in 100-nanosecond units, of each frame.'''
        raise NotImplementedError()
    
    @property
    def average_bitrate(self) -> Optional[int]:
        '''Gets the average bitrate.'''
        raise NotImplementedError()
    

class AsfCodec(groupdocs.metadata.common.CustomPackage):
    '''Represents ASF codec metadata.'''
    
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
        '''Gets the property name.'''
        raise NotImplementedError()
    
    @property
    def codec_type(self) -> groupdocs.metadata.formats.video.AsfCodecType:
        '''Gets the type of the codec.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the description.'''
        raise NotImplementedError()
    
    @property
    def information(self) -> str:
        '''Gets the information string.'''
        raise NotImplementedError()
    

class AsfContentDescriptor(AsfBaseDescriptor):
    '''Represents an ASF content descriptor object.'''
    
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
    def asf_content_type(self) -> groupdocs.metadata.formats.video.AsfDescriptorType:
        '''Gets the type of the content.'''
        raise NotImplementedError()
    

class AsfMetadataDescriptor(AsfBaseDescriptor):
    '''Represents an ASF metadata descriptor.'''
    
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
    def asf_content_type(self) -> groupdocs.metadata.formats.video.AsfDescriptorType:
        '''Gets the type of the content.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language.'''
        raise NotImplementedError()
    
    @property
    def stream_number(self) -> int:
        '''Gets the stream number.'''
        raise NotImplementedError()
    
    @property
    def original_name(self) -> str:
        '''Gets the original name of the descriptor.'''
        raise NotImplementedError()
    

class AsfMetadataDescriptorCollection(groupdocs.metadata.common.CustomPackage):
    '''Represents a collection of metadata descriptors.'''
    
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
    

class AsfPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents native metadata of the ASF media container.'''
    
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
    def file_id(self) -> UUID:
        '''Gets the unique identifier for this file.'''
        raise NotImplementedError()
    
    @property
    def creation_date(self) -> datetime:
        '''Gets the date and time of the initial creation of the file.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.video.AsfFilePropertyFlags:
        '''Gets the header flags.'''
        raise NotImplementedError()
    
    @property
    def stream_properties(self) -> List[groupdocs.metadata.formats.video.AsfBaseStreamProperty]:
        '''Gets the digital media stream properties.'''
        raise NotImplementedError()
    
    @property
    def metadata_descriptors(self) -> List[groupdocs.metadata.formats.video.AsfBaseDescriptor]:
        '''Gets the metadata descriptors.'''
        raise NotImplementedError()
    
    @property
    def codec_information(self) -> List[groupdocs.metadata.formats.video.AsfCodec]:
        '''Gets the codec info entries.'''
        raise NotImplementedError()
    

class AsfRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an ASF video.'''
    
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
    def asf_package(self) -> groupdocs.metadata.formats.video.AsfPackage:
        '''Gets the ASF metadata package.'''
        raise NotImplementedError()
    
    @property
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    

class AsfVideoStreamProperty(AsfBaseStreamProperty):
    '''Represents Video stream property metadata in the ASF media container.'''
    
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
    def stream_type(self) -> groupdocs.metadata.formats.video.AsfStreamType:
        '''Gets the type of this stream.'''
        raise NotImplementedError()
    
    @property
    def stream_number(self) -> int:
        '''Gets the number of this stream.'''
        raise NotImplementedError()
    
    @property
    def start_time(self) -> Optional[int]:
        '''Gets the presentation time of the first object, indicating where this digital media stream
        starts within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def end_time(self) -> Optional[int]:
        '''Gets the presentation time of the last object plus the duration of play, indicating where
        this digital media stream ends within the context of the timeline of the ASF file as a whole.'''
        raise NotImplementedError()
    
    @property
    def bitrate(self) -> Optional[int]:
        '''Gets the leak rate R, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def alternate_bitrate(self) -> Optional[int]:
        '''Gets the leak rate RAlt, in bits per second, of a leaky bucket that contains the data portion
        of the stream without overflowing, excluding all ASF Data Packet overhead.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> Optional[groupdocs.metadata.formats.video.AsfExtendedStreamPropertyFlags]:
        '''Gets the flags.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the stream language.'''
        raise NotImplementedError()
    
    @property
    def average_time_per_frame(self) -> Optional[int]:
        '''Gets the average time duration, measured in 100-nanosecond units, of each frame.'''
        raise NotImplementedError()
    
    @property
    def average_bitrate(self) -> Optional[int]:
        '''Gets the average bitrate.'''
        raise NotImplementedError()
    
    @property
    def image_width(self) -> int:
        '''Gets the width of the encoded image in pixels.'''
        raise NotImplementedError()
    
    @property
    def image_height(self) -> int:
        '''Gets the height of the encoded image in pixels.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> int:
        '''Gets the video compression Id.'''
        raise NotImplementedError()
    
    @property
    def bits_per_pixels(self) -> int:
        '''Gets the bits per pixels.'''
        raise NotImplementedError()
    

class AviHeader(groupdocs.metadata.common.CustomPackage):
    '''Represents the AVIMAINHEADER structure in an AVI video.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.video.AviHeader` class.'''
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
    def micro_sec_per_frame(self) -> int:
        '''Gets the the number of microseconds between frames. This value indicates the overall timing for the file.'''
        raise NotImplementedError()
    
    @property
    def max_bytes_per_sec(self) -> int:
        '''Gets the approximate maximum data rate of the file.
        
        
        This value indicates the number of bytes per second the system must handle to present an AVI sequence as
        specified by the other parameters contained in the main header and stream header chunks.'''
        raise NotImplementedError()
    
    @property
    def padding_granularity(self) -> int:
        '''Gets the alignment for data, in bytes. Pad the data to multiples of this value.'''
        raise NotImplementedError()
    
    @property
    def avi_header_flags(self) -> groupdocs.metadata.formats.video.AviHeaderFlags:
        '''Gets a bitwise combination of zero or more of the AVI flags.'''
        raise NotImplementedError()
    
    @property
    def total_frames(self) -> int:
        '''Gets the the total number of frames of data in the file.'''
        raise NotImplementedError()
    
    @property
    def initial_frames(self) -> int:
        '''Gets the initial frame for interleaved files.
        
        
        Noninterleaved files should specify zero. If you are creating interleaved files, specify the number of frames
        in the file prior to the initial frame of the AVI sequence in this member.'''
        raise NotImplementedError()
    
    @property
    def streams(self) -> int:
        '''Gets the number of streams in the file. For example, a file with audio and video has two streams.'''
        raise NotImplementedError()
    
    @property
    def suggested_buffer_size(self) -> int:
        '''Gets the suggested buffer size for reading the file.
        
        
        Generally, this size should be large enough to contain the largest chunk in the file.
        If set to zero, or if it is too small, the playback software will have to reallocate memory during playback, which will reduce performance. For an interleaved file,
        the buffer size should be large enough to read an entire record, and not just a chunk.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width of the AVI file in pixels.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height of the AVI file in pixels.'''
        raise NotImplementedError()
    

class AviRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an AVI video.'''
    
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
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    
    @property
    def header(self) -> groupdocs.metadata.formats.video.AviHeader:
        '''Gets the AVI header package.'''
        raise NotImplementedError()
    
    @property
    def riff_info_package(self) -> groupdocs.metadata.formats.riff.RiffInfoPackage:
        '''Gets the package containing RIFF Info tags.'''
        raise NotImplementedError()
    

class FlvHeader(groupdocs.metadata.common.CustomPackage):
    '''Represents a FLV video header.'''
    
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
    def version(self) -> int:
        '''Gets the file version.'''
        raise NotImplementedError()
    
    @property
    def type_flags(self) -> int:
        '''Gets the FLV type flags.'''
        raise NotImplementedError()
    
    @property
    def has_audio_tags(self) -> bool:
        '''Gets a value indicating whether audio tags are present in the file.'''
        raise NotImplementedError()
    
    @property
    def has_video_tags(self) -> bool:
        '''Gets a value indicating whether video tags are present in the file.'''
        raise NotImplementedError()
    

class FlvRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an FLV video.'''
    
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
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    
    @property
    def header(self) -> groupdocs.metadata.formats.video.FlvHeader:
        '''Gets the FLV header package.'''
        raise NotImplementedError()
    

class MatroskaAudioTrack(MatroskaTrack):
    '''Represents audio metadata in a Matroska video.'''
    
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
    def track_number(self) -> int:
        '''Gets the track number as used in the Block Header.
        Using more than 127 tracks is not encouraged, though the design allows an unlimited number.'''
        raise NotImplementedError()
    
    @property
    def track_uid(self) -> int:
        '''Gets the unique ID to identify the Track.
        This SHOULD be kept the same when making a direct stream copy of the Track to another file.'''
        raise NotImplementedError()
    
    @property
    def track_type(self) -> groupdocs.metadata.formats.video.MatroskaTrackType:
        '''Gets the type of the track.'''
        raise NotImplementedError()
    
    @property
    def flag_enabled(self) -> bool:
        '''Gets the enabled flag, true if the track is usable.'''
        raise NotImplementedError()
    
    @property
    def default_duration(self) -> Optional[int]:
        '''Gets the number of nanoseconds (not scaled via :py:attr:`groupdocs.metadata.formats.video.MatroskaSegment.timecode_scale`) per frame.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the human-readable track name.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the track in the Matroska languages form.
        This Element MUST be ignored if the :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language_ietf` Element is used in the same TrackEntry.'''
        raise NotImplementedError()
    
    @property
    def language_ietf(self) -> str:
        '''Gets the language of the track according to BCP 47 and using the IANA Language Subtag Registry.
        If this Element is used, then any :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language` Elements used in the same TrackEntry MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def codec_id(self) -> str:
        '''Gets an ID corresponding to the codec.'''
        raise NotImplementedError()
    
    @property
    def codec_name(self) -> str:
        '''Gets a human-readable string specifying the codec.'''
        raise NotImplementedError()
    
    @property
    def sampling_frequency(self) -> float:
        '''Gets the sampling frequency in Hz.'''
        raise NotImplementedError()
    
    @property
    def output_sampling_frequency(self) -> float:
        '''Gets the real output sampling frequency in Hz (used for SBR techniques).'''
        raise NotImplementedError()
    
    @property
    def channels(self) -> int:
        '''Gets the numbers of channels in the track.'''
        raise NotImplementedError()
    
    @property
    def bit_depth(self) -> Optional[int]:
        '''Gets the bits per sample, mostly used for PCM.'''
        raise NotImplementedError()
    

class MatroskaBasePackage(groupdocs.metadata.common.CustomPackage):
    '''Provides a base metadata class for all packages extracted from a Matroska video.'''
    
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
    

class MatroskaEbmlHeader(MatroskaBasePackage):
    '''Represents EBML header metadata in a Matroska video.'''
    
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
    def version(self) -> int:
        '''Gets the version of the EBML Writer that has been used to create the file.'''
        raise NotImplementedError()
    
    @property
    def read_version(self) -> int:
        '''Gets the minimum version an EBML parser needs to be compliant with to be able to read the file.'''
        raise NotImplementedError()
    
    @property
    def doc_type(self) -> str:
        '''Gets the contents of the file. In the case of a MATROSKA file, its value is \'matroska\'.'''
        raise NotImplementedError()
    
    @property
    def doc_type_version(self) -> int:
        '''Gets the version of the :py:attr:`groupdocs.metadata.formats.video.MatroskaEbmlHeader.doc_type` writer used to create the file.'''
        raise NotImplementedError()
    
    @property
    def doc_type_read_version(self) -> int:
        '''Gets the minimum version number a :py:attr:`groupdocs.metadata.formats.video.MatroskaEbmlHeader.doc_type` parser must be compliant with to read the file.'''
        raise NotImplementedError()
    

class MatroskaPackage(MatroskaBasePackage):
    '''Represents a metadata container in a Matroska video.'''
    
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
    def ebml_header(self) -> groupdocs.metadata.formats.video.MatroskaEbmlHeader:
        '''Gets the EBML header metadata.'''
        raise NotImplementedError()
    
    @property
    def segments(self) -> List[groupdocs.metadata.formats.video.MatroskaSegment]:
        '''Gets the segment information metadata.'''
        raise NotImplementedError()
    
    @property
    def tracks(self) -> List[groupdocs.metadata.formats.video.MatroskaTrack]:
        '''Gets the track metadata entries.'''
        raise NotImplementedError()
    
    @property
    def tags(self) -> List[groupdocs.metadata.formats.video.MatroskaTag]:
        '''Gets the tagging metadata.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> groupdocs.metadata.formats.video.MatroskaContentType:
        '''Gets the Matroska content type.'''
        raise NotImplementedError()
    
    @property
    def subtitle_tracks(self) -> List[groupdocs.metadata.formats.video.MatroskaSubtitleTrack]:
        '''Gets the subtitle metadata entries.'''
        raise NotImplementedError()
    

class MatroskaRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in a Matroska video.'''
    
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
    def matroska_package(self) -> groupdocs.metadata.formats.video.MatroskaPackage:
        '''Gets the Matroska metadata package.'''
        raise NotImplementedError()
    

class MatroskaSegment(MatroskaBasePackage):
    '''Represents a SEGMENTINFO element containing general information about the SEGMENT in a Matroska video.'''
    
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
    def segment_uid(self) -> List[int]:
        '''Gets the unique 128 bit number identifying a SEGMENT.
        Obviously, a file can only be referred to by another file if a SEGMENTUID is present, however, playback is possible without that UID.'''
        raise NotImplementedError()
    
    @property
    def segment_filename(self) -> str:
        '''Gets the filename corresponding to this Segment.'''
        raise NotImplementedError()
    
    @property
    def timecode_scale(self) -> int:
        '''Gets the timecode scale value.
        Each scaled timecode in a MATROSKA file is multiplied by TIMECODESCALE to obtain the timecode in nanoseconds. Note that not all timecodes are scaled!'''
        raise NotImplementedError()
    
    @property
    def duration(self) -> Optional[float]:
        '''Gets the duration of the SEGMENT.
        Please see :py:attr:`groupdocs.metadata.formats.video.MatroskaSegment.timecode_scale` for more information.'''
        raise NotImplementedError()
    
    @property
    def date_utc(self) -> Optional[datetime]:
        '''Gets the date and time that the Segment was created by the muxing application or library.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets the general name of the Segment.'''
        raise NotImplementedError()
    
    @property
    def muxing_app(self) -> str:
        '''Gets the full name of the application or library followed by the version number.'''
        raise NotImplementedError()
    
    @property
    def writing_app(self) -> str:
        '''Gets the full name of the application followed by the version number.'''
        raise NotImplementedError()
    
    @property
    def scaled_duration(self) -> Optional[TimeSpan]:
        '''Gets the scaled duration of the SEGMENT.'''
        raise NotImplementedError()
    

class MatroskaSimpleTag(MatroskaBasePackage):
    '''Represents general information about the target in a Matroska video.'''
    
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
    

class MatroskaSubtitle(MatroskaBasePackage):
    '''Represents subtitle metadata in a Matroska video.'''
    
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
    def timecode(self) -> TimeSpan:
        '''Gets the time code.'''
        raise NotImplementedError()
    
    @property
    def duration(self) -> TimeSpan:
        '''Gets the duration.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the subtitle text.'''
        raise NotImplementedError()
    

class MatroskaSubtitleTrack(MatroskaTrack):
    '''Represents subtitle metadata in a Matroska video.'''
    
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
    def track_number(self) -> int:
        '''Gets the track number as used in the Block Header.
        Using more than 127 tracks is not encouraged, though the design allows an unlimited number.'''
        raise NotImplementedError()
    
    @property
    def track_uid(self) -> int:
        '''Gets the unique ID to identify the Track.
        This SHOULD be kept the same when making a direct stream copy of the Track to another file.'''
        raise NotImplementedError()
    
    @property
    def track_type(self) -> groupdocs.metadata.formats.video.MatroskaTrackType:
        '''Gets the type of the track.'''
        raise NotImplementedError()
    
    @property
    def flag_enabled(self) -> bool:
        '''Gets the enabled flag, true if the track is usable.'''
        raise NotImplementedError()
    
    @property
    def default_duration(self) -> Optional[int]:
        '''Gets the number of nanoseconds (not scaled via :py:attr:`groupdocs.metadata.formats.video.MatroskaSegment.timecode_scale`) per frame.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the human-readable track name.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the track in the Matroska languages form.
        This Element MUST be ignored if the :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language_ietf` Element is used in the same TrackEntry.'''
        raise NotImplementedError()
    
    @property
    def language_ietf(self) -> str:
        '''Gets the language of the track according to BCP 47 and using the IANA Language Subtag Registry.
        If this Element is used, then any :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language` Elements used in the same TrackEntry MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def codec_id(self) -> str:
        '''Gets an ID corresponding to the codec.'''
        raise NotImplementedError()
    
    @property
    def codec_name(self) -> str:
        '''Gets a human-readable string specifying the codec.'''
        raise NotImplementedError()
    
    @property
    def subtitles(self) -> List[groupdocs.metadata.formats.video.MatroskaSubtitle]:
        '''Gets the subtitles.'''
        raise NotImplementedError()
    

class MatroskaTag(MatroskaBasePackage):
    '''Represents metadata describing Tracks, Editions, Chapters, Attachments, or the Segment as a whole in a Matroska video.'''
    
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
    def target_type_value(self) -> groupdocs.metadata.formats.video.MatroskaTargetTypeValue:
        '''Gets the number to indicate the logical level of the target.'''
        raise NotImplementedError()
    
    @property
    def target_type(self) -> str:
        '''Gets an informational string that can be used to display the logical level of the target.
        Like "ALBUM", "TRACK", "MOVIE", "CHAPTER", etc.'''
        raise NotImplementedError()
    
    @property
    def tag_track_uid(self) -> int:
        '''Gets a unique ID to identify the Track(s) the tags belong to.
        If the value is 0 at this level, the tags apply to all tracks in the Segment.'''
        raise NotImplementedError()
    
    @property
    def simple_tags(self) -> groupdocs.metadata.formats.video.MatroskaSimpleTag:
        '''Gets the general information about the target.'''
        raise NotImplementedError()
    

class MatroskaTrack(MatroskaBasePackage):
    '''Represents track metadata in a Matroska video.'''
    
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
    def track_number(self) -> int:
        '''Gets the track number as used in the Block Header.
        Using more than 127 tracks is not encouraged, though the design allows an unlimited number.'''
        raise NotImplementedError()
    
    @property
    def track_uid(self) -> int:
        '''Gets the unique ID to identify the Track.
        This SHOULD be kept the same when making a direct stream copy of the Track to another file.'''
        raise NotImplementedError()
    
    @property
    def track_type(self) -> groupdocs.metadata.formats.video.MatroskaTrackType:
        '''Gets the type of the track.'''
        raise NotImplementedError()
    
    @property
    def flag_enabled(self) -> bool:
        '''Gets the enabled flag, true if the track is usable.'''
        raise NotImplementedError()
    
    @property
    def default_duration(self) -> Optional[int]:
        '''Gets the number of nanoseconds (not scaled via :py:attr:`groupdocs.metadata.formats.video.MatroskaSegment.timecode_scale`) per frame.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the human-readable track name.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the track in the Matroska languages form.
        This Element MUST be ignored if the :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language_ietf` Element is used in the same TrackEntry.'''
        raise NotImplementedError()
    
    @property
    def language_ietf(self) -> str:
        '''Gets the language of the track according to BCP 47 and using the IANA Language Subtag Registry.
        If this Element is used, then any :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language` Elements used in the same TrackEntry MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def codec_id(self) -> str:
        '''Gets an ID corresponding to the codec.'''
        raise NotImplementedError()
    
    @property
    def codec_name(self) -> str:
        '''Gets a human-readable string specifying the codec.'''
        raise NotImplementedError()
    

class MatroskaVideoTrack(MatroskaTrack):
    '''Represents video metadata in a Matroska video.'''
    
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
    def track_number(self) -> int:
        '''Gets the track number as used in the Block Header.
        Using more than 127 tracks is not encouraged, though the design allows an unlimited number.'''
        raise NotImplementedError()
    
    @property
    def track_uid(self) -> int:
        '''Gets the unique ID to identify the Track.
        This SHOULD be kept the same when making a direct stream copy of the Track to another file.'''
        raise NotImplementedError()
    
    @property
    def track_type(self) -> groupdocs.metadata.formats.video.MatroskaTrackType:
        '''Gets the type of the track.'''
        raise NotImplementedError()
    
    @property
    def flag_enabled(self) -> bool:
        '''Gets the enabled flag, true if the track is usable.'''
        raise NotImplementedError()
    
    @property
    def default_duration(self) -> Optional[int]:
        '''Gets the number of nanoseconds (not scaled via :py:attr:`groupdocs.metadata.formats.video.MatroskaSegment.timecode_scale`) per frame.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the human-readable track name.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the track in the Matroska languages form.
        This Element MUST be ignored if the :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language_ietf` Element is used in the same TrackEntry.'''
        raise NotImplementedError()
    
    @property
    def language_ietf(self) -> str:
        '''Gets the language of the track according to BCP 47 and using the IANA Language Subtag Registry.
        If this Element is used, then any :py:attr:`groupdocs.metadata.formats.video.MatroskaTrack.language` Elements used in the same TrackEntry MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def codec_id(self) -> str:
        '''Gets an ID corresponding to the codec.'''
        raise NotImplementedError()
    
    @property
    def codec_name(self) -> str:
        '''Gets a human-readable string specifying the codec.'''
        raise NotImplementedError()
    
    @property
    def flag_interlaced(self) -> groupdocs.metadata.formats.video.MatroskaVideoFlagInterlaced:
        '''Gets a flag to declare if the video is known to be progressive or interlaced and if applicable to declare details about the interlacement.'''
        raise NotImplementedError()
    
    @property
    def field_order(self) -> groupdocs.metadata.formats.video.MatroskaVideoFieldOrder:
        '''Gets declare the field ordering of the video.
        If FlagInterlaced is not set to 1, this Element MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def stereo_mode(self) -> Optional[groupdocs.metadata.formats.video.MatroskaVideoStereoMode]:
        '''Gets the stereo-3D video mode.'''
        raise NotImplementedError()
    
    @property
    def alpha_mode(self) -> Optional[int]:
        '''Gets the alpha Video Mode.
        Presence of this Element indicates that the BlockAdditional Element could contain Alpha data.'''
        raise NotImplementedError()
    
    @property
    def pixel_width(self) -> int:
        '''Gets the width of the encoded video frames in pixels.'''
        raise NotImplementedError()
    
    @property
    def pixel_height(self) -> int:
        '''Gets the height of the encoded video frames in pixels.'''
        raise NotImplementedError()
    
    @property
    def pixel_crop_bottom(self) -> int:
        '''Gets the number of video pixels to remove at the bottom of the image.'''
        raise NotImplementedError()
    
    @property
    def pixel_crop_top(self) -> int:
        '''Gets the number of video pixels to remove at the top of the image.'''
        raise NotImplementedError()
    
    @property
    def pixel_crop_left(self) -> int:
        '''Gets the number of video pixels to remove on the left of the image.'''
        raise NotImplementedError()
    
    @property
    def pixel_crop_right(self) -> int:
        '''Gets the number of video pixels to remove on the right of the image.'''
        raise NotImplementedError()
    
    @property
    def display_width(self) -> Optional[int]:
        '''Gets the width of the video frames to display.
        Applies to the video frame after cropping (PixelCrop* Elements).'''
        raise NotImplementedError()
    
    @property
    def display_height(self) -> Optional[int]:
        '''Gets the height of the video frames to display.
        Applies to the video frame after cropping (PixelCrop* Elements).'''
        raise NotImplementedError()
    
    @property
    def display_unit(self) -> groupdocs.metadata.formats.video.MatroskaVideoDisplayUnit:
        '''Gets the how :py:attr:`groupdocs.metadata.formats.video.MatroskaVideoTrack.display_width`and :py:attr:`groupdocs.metadata.formats.video.MatroskaVideoTrack.display_height` are interpreted.'''
        raise NotImplementedError()
    

class MovAtom(groupdocs.metadata.common.CustomPackage):
    '''Represents a QuickTime atom.'''
    
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
    def offset(self) -> int:
        '''Gets the atom offset.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the atom size in bytes.'''
        raise NotImplementedError()
    
    @property
    def long_size(self) -> int:
        '''Gets the atom size in bytes.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> str:
        '''Gets the 4-characters type.'''
        raise NotImplementedError()
    
    @property
    def data_offset(self) -> int:
        '''Gets the data offset.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the data size in bytes.'''
        raise NotImplementedError()
    
    @property
    def has_extended_size(self) -> bool:
        '''Gets a value indicating whether the extended size field was used to store the atom data.'''
        raise NotImplementedError()
    
    @property
    def atoms(self) -> List[groupdocs.metadata.formats.video.MovAtom]:
        '''Gets an array of :py:class:`groupdocs.metadata.formats.video.MovAtom` atoms.'''
        raise NotImplementedError()
    

class MovPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents QuickTime metadata.'''
    
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
    def director(self) -> str:
        '''Name of the director of the movie content.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Description of the movie file content.'''
        raise NotImplementedError()
    
    @property
    def location_motion(self) -> str:
        '''An indication of the direction the camera is moving during the shot.'''
        raise NotImplementedError()
    
    @property
    def location_facing(self) -> str:
        '''An indication of the direction the camera is facing during the shot.'''
        raise NotImplementedError()
    
    @property
    def location_date(self) -> str:
        '''A date and time, stored using the extended format defined in ISO 8601:2004- Data elements and interchange format.'''
        raise NotImplementedError()
    
    @property
    def location_role(self) -> str:
        '''A single byte, binary value containing a value from the set: 0 indicates “shooting location”, 1 indicates “real location”, 2 indicates “fictional location”.
        Other values are reserved.'''
        raise NotImplementedError()
    
    @property
    def location_note(self) -> str:
        '''Descriptive comment.'''
        raise NotImplementedError()
    
    @property
    def location_body(self) -> str:
        '''The astronomical body, for compatibility with the 3GPP format'''
        raise NotImplementedError()
    
    @property
    def location_name(self) -> str:
        '''Name of the location.'''
        raise NotImplementedError()
    
    @property
    def user_ratings(self) -> str:
        '''A number, assigned by the user, that indicates the rating or relative value of the movie.
        This number can range from 0.0 to 5.0. A value of 0.0 indicates that the user has not rated the movie.'''
        raise NotImplementedError()
    
    @property
    def users(self) -> str:
        '''A name indicating a user-defined collection that includes this movie.'''
        raise NotImplementedError()
    
    @property
    def year(self) -> str:
        '''Year when the movie file or the original content was created or recorded.'''
        raise NotImplementedError()
    
    @property
    def software(self) -> str:
        '''Name of software used to create the movie file content.'''
        raise NotImplementedError()
    
    @property
    def producer(self) -> str:
        '''Name of producer of movie file content.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Album or collection name of which the movie content forms a part'''
        raise NotImplementedError()
    
    @property
    def keywords(self) -> str:
        '''Keywords associated with the movie file content.'''
        raise NotImplementedError()
    
    @property
    def information(self) -> str:
        '''Information about the movie file content.'''
        raise NotImplementedError()
    
    @property
    def genre(self) -> str:
        '''Text describing the genre or genres to which the movie content conforms.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''The title of the movie file content.'''
        raise NotImplementedError()
    
    @property
    def creation_date(self) -> str:
        '''The date the movie file content was created.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> str:
        '''Copyright statement for the movie file content.'''
        raise NotImplementedError()
    
    @property
    def comment(self) -> str:
        '''User entered comment regarding the movie file content.'''
        raise NotImplementedError()
    
    @property
    def author(self) -> str:
        '''Name of the author of the movie file content.'''
        raise NotImplementedError()
    
    @property
    def artwork(self) -> str:
        '''A single image that can represent the movie file content.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Name of the artist who created the movie file content.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> str:
        '''Name of publisher of movie file content.'''
        raise NotImplementedError()
    
    @property
    def movie_creation_time(self) -> Optional[datetime]:
        '''A 32-bit integer that specifies the creation calendar date and time for the movie atom.'''
        raise NotImplementedError()
    
    @movie_creation_time.setter
    def movie_creation_time(self, value : Optional[datetime]) -> None:
        '''A 32-bit integer that specifies the creation calendar date and time for the movie atom.'''
        raise NotImplementedError()
    
    @property
    def movie_modification_time(self) -> Optional[datetime]:
        '''A 32-bit integer that specifies the calendar date and time of the last change to the movie atom.'''
        raise NotImplementedError()
    
    @movie_modification_time.setter
    def movie_modification_time(self, value : Optional[datetime]) -> None:
        '''A 32-bit integer that specifies the calendar date and time of the last change to the movie atom.'''
        raise NotImplementedError()
    
    @property
    def movie_duration(self) -> int:
        '''A time value that indicates the duration of the movie in seconds.'''
        raise NotImplementedError()
    
    @property
    def atoms(self) -> List[groupdocs.metadata.formats.video.MovAtom]:
        '''Gets an array of :py:class:`groupdocs.metadata.formats.video.MovAtom` atoms.'''
        raise NotImplementedError()
    

class MovRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in a QuickTime video.'''
    
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
    def mov_package(self) -> groupdocs.metadata.formats.video.MovPackage:
        '''Gets the QuickTime metadata package.'''
        raise NotImplementedError()
    
    @property
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    

class AsfCodecType:
    '''Defines ASF codec types.'''
    
    UNDEFINED : AsfCodecType
    '''Undefined codec.'''
    VIDEO : AsfCodecType
    '''Video codec.'''
    AUDIO : AsfCodecType
    '''Audio codec.'''
    UNKNOWN : AsfCodecType
    '''Unknown codec.'''

class AsfDescriptorType:
    '''Defines ASF descriptor types.'''
    
    UNICODE : AsfDescriptorType
    '''The unicode string type.'''
    BYTE_ARRAY : AsfDescriptorType
    '''The byte array type.'''
    BOOL : AsfDescriptorType
    '''The 32-bit bool type.'''
    D_WORD : AsfDescriptorType
    '''The 32-bit unsigned integer type.'''
    Q_WORD : AsfDescriptorType
    '''The 64-bit unsigned integer type.'''
    WORD : AsfDescriptorType
    '''The 16-bit unsigned integer type.'''
    GUID : AsfDescriptorType
    '''The 128-bit (16 byte) GUID type.'''

class AsfExtendedStreamPropertyFlags:
    '''Defines ASF extended stream property flags.'''
    
    RELIABLE : AsfExtendedStreamPropertyFlags
    '''This digital media stream, if sent over a network, must be carried over a reliable data communications transport mechanism.'''
    SEEKABLE : AsfExtendedStreamPropertyFlags
    '''This flag should be set only if the stream is seekable.'''
    NO_CLEANPOINTS : AsfExtendedStreamPropertyFlags
    '''The stream does not contain any cleanpoints.'''
    RESEND_LIVE_CLEANPOINTS : AsfExtendedStreamPropertyFlags
    '''A stream is joined in mid-transmission, all information from the most recent
    cleanpoint up to the current time should be sent before normal streaming begins at the current time.'''

class AsfFilePropertyFlags:
    '''Defines ASF file property flags.'''
    
    UNDEFINED : AsfFilePropertyFlags
    '''The undefined flag.'''
    BROADCAST : AsfFilePropertyFlags
    '''Specifies, that a file is in the process of being created,
    and thus that various values stored in the header objects are invalid.'''
    SEEKABLE : AsfFilePropertyFlags
    '''Specifies, that a file is seekable.'''

class AsfStreamType:
    '''Defines ASF stream types.'''
    
    UNDEFINED : AsfStreamType
    '''Undefined stream type.'''
    AUDIO : AsfStreamType
    '''ASF Audio Media.'''
    VIDEO : AsfStreamType
    '''ASF Video Media.'''
    COMMAND : AsfStreamType
    '''ASF Command Media.'''
    JFIF : AsfStreamType
    '''ASF JFIF Media.'''
    DEGRADABLE_JPEG : AsfStreamType
    '''ASF Degradable JPEG Media.'''
    FILE_TRANSFER : AsfStreamType
    '''ASF File Transfer Media.'''
    BINARY : AsfStreamType
    '''ASF Binary Media.'''
    WEB_STREAM_SUBTYPE : AsfStreamType
    '''ASF Web Stream Media Subtype.'''
    WEB_STREAM_FORMAT : AsfStreamType
    '''ASF Web Stream Format.'''

class AviHeaderFlags:
    '''Represents AVI Header flags.'''
    
    HAS_INDEX : AviHeaderFlags
    '''Indicates the AVI file has an index.'''
    MUST_USE_INDEX : AviHeaderFlags
    '''Indicates that application should use the index, rather than the physical ordering of the chunks in the file,
    to determine the order of presentation of the data. For example, this flag could be used to create a list of frames for editing.'''
    IS_INTERLEAVED : AviHeaderFlags
    '''Indicates the AVI file is interleaved.'''
    TRUST_CK_TYPE : AviHeaderFlags
    '''Use CKType to find key frames.'''
    WAS_CAPTURE_FILE : AviHeaderFlags
    '''Indicates the AVI file is a specially allocated file used for capturing real-time video.
    Applications should warn the user before writing over a file with this flag set because the user probably defragmented this file.'''
    COPYRIGHTED : AviHeaderFlags
    '''Indicates the AVI file contains copyrighted data and software.
    When this flag is used, software should not permit the data to be duplicated.'''

class MatroskaContentType:
    '''Represents a Matroska content type.'''
    
    UNDEFINED : MatroskaContentType
    '''Undefined content.'''
    AUDIO : MatroskaContentType
    '''Defines the Matroska audio type.'''
    VIDEO : MatroskaContentType
    '''Defines the Matroska video type.'''
    VIDEO_3D : MatroskaContentType
    '''Defines the Matroska 3D video type.'''

class MatroskaTargetTypeValue:
    '''Represents a number to indicate the logical level of the Matroska tag target.'''
    
    UNDEFINED : MatroskaTargetTypeValue
    '''Undefined level.'''
    COLLECTION : MatroskaTargetTypeValue
    '''COLLECTION level.'''
    EDITION : MatroskaTargetTypeValue
    '''EDITION / ISSUE / VOLUME / OPUS / SEASON / SEQUEL level.'''
    ALBUM : MatroskaTargetTypeValue
    '''ALBUM / OPERA / CONCERT / MOVIE / EPISODE / CONCERT level.'''
    PART : MatroskaTargetTypeValue
    '''PART / SESSION level.'''
    TRACK : MatroskaTargetTypeValue
    '''TRACK / SONG / CHAPTER level.'''
    SUBTRACK : MatroskaTargetTypeValue
    '''SUBTRACK / PART / MOVEMENT / SCENE level.'''
    SHOT : MatroskaTargetTypeValue
    '''SHOT level.'''

class MatroskaTrackType:
    '''Represents Matroska track types coded in 8 bits.'''
    
    UNDEFINED : MatroskaTrackType
    '''The undefined track type.'''
    VIDEO : MatroskaTrackType
    '''Track is a video track.'''
    AUDIO : MatroskaTrackType
    '''Track is an audio track.'''
    COMPLEX : MatroskaTrackType
    '''Track is a complex track, i.e. a combined video and audio track.'''
    LOGO : MatroskaTrackType
    '''Track is a logo track.'''
    SUBTITLE : MatroskaTrackType
    '''Track is a subtitle track.'''
    BUTTON : MatroskaTrackType
    '''Track is a button track.'''
    CONTROL : MatroskaTrackType
    '''Track is a control track.'''

class MatroskaVideoDisplayUnit:
    '''Defines how Matroska DisplayWidth and DisplayHeight are interpreted.'''
    
    PIXELS : MatroskaVideoDisplayUnit
    '''Pixels unit.'''
    CENTIMETERS : MatroskaVideoDisplayUnit
    '''Centimeters unit.'''
    INCHES : MatroskaVideoDisplayUnit
    '''Inches unit.'''
    ASPECT_RATIO : MatroskaVideoDisplayUnit
    '''Display aspect ratio unit.'''
    UNKNOWN : MatroskaVideoDisplayUnit
    '''Unknown unit.'''

class MatroskaVideoFieldOrder:
    '''Represents the field ordering of the Matroska video.
    If FlagInterlaced is not set to 1, this Element MUST be ignored.'''
    
    PROGRESSIVE : MatroskaVideoFieldOrder
    '''Progressive ordering.'''
    TFF : MatroskaVideoFieldOrder
    '''Tiff ordering.'''
    UNDETERMINED : MatroskaVideoFieldOrder
    '''Undetermined ordering.'''
    BFF : MatroskaVideoFieldOrder
    '''Biff ordering.'''
    BFF_SWAPPED : MatroskaVideoFieldOrder
    '''Bff (swapped) ordering.'''
    TFF_SWAPPED : MatroskaVideoFieldOrder
    '''Tff (swapped) ordering.'''

class MatroskaVideoFlagInterlaced:
    '''Represents a flag to declare if the Matroska video is known to be progressive or interlaced
    and if applicable to declare details about the interlacement.'''
    
    UNDETERMINED : MatroskaVideoFlagInterlaced
    '''Undetermined flag.'''
    INTERLACED : MatroskaVideoFlagInterlaced
    '''Interlaced flag.'''
    PROGRESSIVE : MatroskaVideoFlagInterlaced
    '''Progressive flag.'''

class MatroskaVideoStereoMode:
    '''Represents Matroska Stereo-3D video modes.'''
    
    MONO : MatroskaVideoStereoMode
    '''Mono mode.'''
    SIDE_BY_SIDE_LEFT : MatroskaVideoStereoMode
    '''Side by side (left eye first) video mode.'''
    TOP_BOTTOM_RIGHT : MatroskaVideoStereoMode
    '''Top - bottom (right eye is first) video mode.'''
    TOP_BOTTOM_LEFT : MatroskaVideoStereoMode
    '''Top - bottom (left eye is first) video mode.'''
    CHECKBOARD_RIGHT : MatroskaVideoStereoMode
    '''Checkboard (right eye is first) video mode.'''
    CHECKBOARD_LLEFT : MatroskaVideoStereoMode
    '''Checkboard (left eye is first) video mode.'''
    ROW_INTERLEAVED_RIGHT : MatroskaVideoStereoMode
    '''Row interleaved (right eye is first) video mode.'''
    ROW_INTERLEAVED_LEFT : MatroskaVideoStereoMode
    '''Row interleaved (left eye is first) video mode.'''
    COLUMN_INTERLEAVED_RIGHT : MatroskaVideoStereoMode
    '''Column interleaved (right eye is first) video mode.'''
    COLUMN_INTERLEAVED_LEFT : MatroskaVideoStereoMode
    '''Column interleaved (left eye is first) video mode.'''
    ANAGLYPH_CYAN_RED : MatroskaVideoStereoMode
    '''Anaglyph (cyan/red) video mode.'''
    SIDE_BY_SIDE_RIGHT : MatroskaVideoStereoMode
    '''Side by side (right eye first) video mode.'''
    ANAGLYPH_GREEN_MAGENTA : MatroskaVideoStereoMode
    '''Anaglyph (green/magenta) video mode.'''
    BOTH_EYES_LACED_LEFT : MatroskaVideoStereoMode
    '''Both eyes laced in one Block (left eye is first) video mode.'''
    BOTH_EYES_LACED_RIGHT : MatroskaVideoStereoMode
    '''Both eyes laced in one Block (right eye is first) video mode.'''

