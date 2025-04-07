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

class MpegAudioPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents MPEG audio metadata.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.mpeg.MpegAudioPackage` class.'''
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
    def mpeg_audio_version(self) -> groupdocs.metadata.formats.mpeg.MpegAudioVersion:
        '''Gets the MPEG audio version. Can be MPEG-1, MPEG-2 etc.'''
        raise NotImplementedError()
    
    @property
    def layer(self) -> int:
        '''Gets the layer description. For an MP3 audio it is \'3\'.'''
        raise NotImplementedError()
    
    @property
    def is_protected(self) -> bool:
        '''Gets ``true`` if protected.'''
        raise NotImplementedError()
    
    @property
    def header_position(self) -> int:
        '''Gets the header offset.'''
        raise NotImplementedError()
    
    @property
    def bitrate(self) -> int:
        '''Gets the bitrate.'''
        raise NotImplementedError()
    
    @property
    def frequency(self) -> int:
        '''Gets the frequency.'''
        raise NotImplementedError()
    
    @property
    def padding_bit(self) -> int:
        '''Gets the padding bit.'''
        raise NotImplementedError()
    
    @property
    def private_bit(self) -> bool:
        '''Gets a value indicating whether [private bit].'''
        raise NotImplementedError()
    
    @property
    def channel_mode(self) -> groupdocs.metadata.formats.mpeg.MpegChannelMode:
        '''Gets the channel mode.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> bool:
        '''Gets the copyright bit.'''
        raise NotImplementedError()
    
    @property
    def is_original(self) -> bool:
        '''Gets the original bit.'''
        raise NotImplementedError()
    
    @property
    def emphasis(self) -> groupdocs.metadata.formats.mpeg.MpegEmphasis:
        '''Gets the emphasis.'''
        raise NotImplementedError()
    
    @property
    def mode_extension_bits(self) -> int:
        '''Gets the mode extension bits.'''
        raise NotImplementedError()
    

class MpegAudioVersion:
    '''Represents a particular MPEG standard.'''
    
    MPEG25 : MpegAudioVersion
    '''The MPEG 2.5 standard.'''
    MPEG2 : MpegAudioVersion
    '''The MPEG 2 standard.'''
    MPEG1 : MpegAudioVersion
    '''The MPEG 1 standard.'''

class MpegChannelMode:
    '''Defines MPEG audio channel modes.'''
    
    STEREO : MpegChannelMode
    '''Stereo mode.'''
    JOINT_STEREO : MpegChannelMode
    '''Joint stereo mode.'''
    DUAL_CHANNEL : MpegChannelMode
    '''Dual channel mode.'''
    MONO : MpegChannelMode
    '''Mono mode.'''

class MpegEmphasis:
    '''Defines MPEG emphasis types.'''
    
    NONE : MpegEmphasis
    '''No emphasis indication.'''
    MS5015 : MpegEmphasis
    '''50/15 ms.'''
    RESERVED : MpegEmphasis
    '''Reserved.'''
    CCIT_J17 : MpegEmphasis
    '''CCIT J.17.'''

