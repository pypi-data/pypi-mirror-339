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

class ApePackage(groupdocs.metadata.common.CustomPackage):
    '''Represents an APE v2 metadata package.
    Please find more information at `http://wiki.hydrogenaud.io/index.php?title=APE_key <http://wiki.hydrogenaud.io/index.php?title=APE_key>`.'''
    
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
    def title(self) -> str:
        '''Gets the title.'''
        raise NotImplementedError()
    
    @property
    def subtitle(self) -> str:
        '''Gets the subtitle.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the artist.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Gets the album.'''
        raise NotImplementedError()
    
    @property
    def debut_album(self) -> str:
        '''Gets the debut album.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> str:
        '''Gets the publisher.'''
        raise NotImplementedError()
    
    @property
    def conductor(self) -> str:
        '''Gets the conductor.'''
        raise NotImplementedError()
    
    @property
    def track(self) -> Optional[int]:
        '''Gets the track number.'''
        raise NotImplementedError()
    
    @property
    def composer(self) -> str:
        '''Gets the composer.'''
        raise NotImplementedError()
    
    @property
    def comment(self) -> str:
        '''Gets the comment.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> str:
        '''Gets the copyright.'''
        raise NotImplementedError()
    
    @property
    def publication_right(self) -> str:
        '''Gets the publication right.'''
        raise NotImplementedError()
    
    @property
    def file(self) -> str:
        '''Gets the file.'''
        raise NotImplementedError()
    
    @property
    def isbn(self) -> str:
        '''Gets the ISBN number with check digit. See more: https://en.wikipedia.org/wiki/International_Standard_Book_Number.'''
        raise NotImplementedError()
    
    @property
    def record_location(self) -> str:
        '''Gets the record location.'''
        raise NotImplementedError()
    
    @property
    def genre(self) -> str:
        '''Gets the genre.'''
        raise NotImplementedError()
    
    @property
    def isrc(self) -> str:
        '''Gets the International Standard Recording Number.'''
        raise NotImplementedError()
    
    @property
    def abstract(self) -> str:
        '''Gets the abstract link.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language.'''
        raise NotImplementedError()
    
    @property
    def bibliography(self) -> str:
        '''Gets the bibliography.'''
        raise NotImplementedError()
    

class ID3Tag(groupdocs.metadata.common.CustomPackage):
    '''Represents a base abstract class for the ID3(v1) and ID3(v2) audio tags.'''
    
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
    def version(self) -> str:
        '''Gets the version of the ID3 tag in string format. For example: \'ID3v1.1\'.'''
        raise NotImplementedError()
    

class ID3V1Tag(ID3Tag):
    '''Represents an ID3v1 tag.
    Please find more information at `https://en.wikipedia.org/wiki/ID3#ID3v1 <https://en.wikipedia.org/wiki/ID3#ID3v1>`.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V1Tag` class.'''
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
    def version(self) -> str:
        '''Gets the ID3 version. It can be ID3 or ID3v1.1'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the artist. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @artist.setter
    def artist(self, value : str) -> None:
        '''Sets the artist. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Gets the album. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @album.setter
    def album(self, value : str) -> None:
        '''Sets the album. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @property
    def genre_value(self) -> groupdocs.metadata.formats.audio.ID3V1Genre:
        '''Gets the genre identifier.'''
        raise NotImplementedError()
    
    @property
    def comment(self) -> str:
        '''Gets the comment. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @comment.setter
    def comment(self, value : str) -> None:
        '''Sets the comment. Maximum length is 30 characters.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets the title.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets the title.'''
        raise NotImplementedError()
    
    @property
    def year(self) -> str:
        '''Gets the year. Maximum length is 4 characters.'''
        raise NotImplementedError()
    
    @year.setter
    def year(self, value : str) -> None:
        '''Sets the year. Maximum length is 4 characters.'''
        raise NotImplementedError()
    
    @property
    def track_number(self) -> Optional[int]:
        '''Gets the track number. Presented in a ID3v1.1 tag only.'''
        raise NotImplementedError()
    
    @track_number.setter
    def track_number(self, value : Optional[int]) -> None:
        '''Sets the track number. Presented in a ID3v1.1 tag only.'''
        raise NotImplementedError()
    

class ID3V2AttachedPictureFrame(ID3V2TagFrame):
    '''Represents an APIC frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
    @overload
    def __init__(self, encoding : groupdocs.metadata.formats.audio.ID3V2EncodingType, mime_type : str, picture_type : groupdocs.metadata.formats.audio.ID3V2AttachedPictureType, description : str, picture_data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2AttachedPictureFrame` class.
        
        :param encoding: The frame encoding.
        :param mime_type: The MIME-type of the image.
        :param picture_type: The type of the picture.
        :param description: The description of the picture.
        :param picture_data: The picture data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, picture_type : groupdocs.metadata.formats.audio.ID3V2AttachedPictureType, description : str, picture_data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2AttachedPictureFrame` class.
        
        :param picture_type: The type of the picture.
        :param description: The description of the picture.
        :param picture_data: The picture data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, picture_data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2AttachedPictureFrame` class.
        
        :param picture_data: The picture data.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def description_encoding(self) -> groupdocs.metadata.formats.audio.ID3V2EncodingType:
        '''Gets the encoding used to encode the picture description.'''
        raise NotImplementedError()
    
    @property
    def mime_type(self) -> str:
        '''Gets the MIME type of the picture.'''
        raise NotImplementedError()
    
    @property
    def attached_picture_type(self) -> groupdocs.metadata.formats.audio.ID3V2AttachedPictureType:
        '''Gets the type of the picture.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the picture description.
        The description has a maximum length of 64 characters, but may be empty.'''
        raise NotImplementedError()
    
    @property
    def picture_data(self) -> List[int]:
        '''Gets the picture data.'''
        raise NotImplementedError()
    

class ID3V2CommentFrame(ID3V2TagFrame):
    '''Represents a COMM frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
    def __init__(self, encoding : groupdocs.metadata.formats.audio.ID3V2EncodingType, language : str, description : str, text : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2CommentFrame` class.
        
        :param encoding: The encoding of the comment.
        :param language: The language of the comment.
        :param description: A short content description.
        :param text: The text of the comment.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def comment_encoding(self) -> groupdocs.metadata.formats.audio.ID3V2EncodingType:
        '''Gets the encoding of the comment.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language of the comment (3 characters).'''
        raise NotImplementedError()
    
    @property
    def short_content_description(self) -> str:
        '''Gets the short content description.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text of the comment.'''
        raise NotImplementedError()
    

class ID3V2MlltFrame(ID3V2TagFrame):
    '''Represents an MLLT frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    

class ID3V2PlayCounterFrame(ID3V2TagFrame):
    '''Represents a PCNT frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.
    This is simply a counter of the number of times a file has been played.'''
    
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets the number of times the file has been played.'''
        raise NotImplementedError()
    

class ID3V2PrivateFrame(ID3V2TagFrame):
    '''Represents a PRIV frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.
    The frame is used to contain information from a software producer that its program uses
    and does not fit into the other frames.'''
    
    def __init__(self, owner_identifier : str, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2PrivateFrame` class.
        
        :param owner_identifier: The owner identifier.
        :param data: Frame binary data.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def owner_identifier(self) -> str:
        '''Gets the owner identifier.'''
        raise NotImplementedError()
    
    @property
    def binary_data(self) -> List[int]:
        '''Gets the binary data.'''
        raise NotImplementedError()
    

class ID3V2Tag(ID3Tag):
    '''Represents an ID3v2 tag.
    Please find more information at `https://en.wikipedia.org/wiki/ID3#ID3v2 <https://en.wikipedia.org/wiki/ID3#ID3v2>`.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag` class.'''
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
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.audio.ID3V2TagFrame]:
        '''Creates a list from the package.
        
        :returns: A list of all frames contained in the ID3v2 tag.'''
        raise NotImplementedError()
    
    def remove_attached_pictures(self) -> None:
        '''Removes all attached pictures stored in APIC frames.'''
        raise NotImplementedError()
    
    def get(self, frame_id : str) -> List[groupdocs.metadata.formats.audio.ID3V2TagFrame]:
        '''Gets an array of frames with the specified id.
        
        :param frame_id: The id of the frames to get.
        :returns: An array of frames with the specified id.'''
        raise NotImplementedError()
    
    def set(self, frame : groupdocs.metadata.formats.audio.ID3V2TagFrame) -> None:
        '''Removes all frames having the same id as the specified one and adds the new frame to the tag.
        
        :param frame: The frame to replace all frames of its kind with.'''
        raise NotImplementedError()
    
    def clear(self, frame_id : str) -> None:
        '''Removes all frames with the specified id.
        
        :param frame_id: The id of the frames to remove.'''
        raise NotImplementedError()
    
    def add(self, frame : groupdocs.metadata.formats.audio.ID3V2TagFrame) -> None:
        '''Adds a frame to the tag.
        
        :param frame: The frame to be added to the tag.'''
        raise NotImplementedError()
    
    def remove(self, frame : groupdocs.metadata.formats.audio.ID3V2TagFrame) -> None:
        '''Removes the specified frame from the tag.
        
        :param frame: The frame to be removed from the tag.'''
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
    def version(self) -> str:
        '''Gets the ID3 version.'''
        raise NotImplementedError()
    
    @property
    def tag_size(self) -> int:
        '''Gets the size of the tag.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Gets the Album/Movie/Show title.
        This value is represented by the TALB frame.'''
        raise NotImplementedError()
    
    @album.setter
    def album(self, value : str) -> None:
        '''Sets the Album/Movie/Show title.
        This value is represented by the TALB frame.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group.
        This value is represented by the TPE1 frame.'''
        raise NotImplementedError()
    
    @artist.setter
    def artist(self, value : str) -> None:
        '''Sets the Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group.
        This value is represented by the TPE1 frame.'''
        raise NotImplementedError()
    
    @property
    def band(self) -> str:
        '''Gets the Band/Orchestra/Accompaniment.
        This value is represented by the TPE2 frame.'''
        raise NotImplementedError()
    
    @band.setter
    def band(self, value : str) -> None:
        '''Sets the Band/Orchestra/Accompaniment.
        This value is represented by the TPE2 frame.'''
        raise NotImplementedError()
    
    @property
    def bits_per_minute(self) -> str:
        '''Gets the number of beats per minute in the main part of the audio.
        This value is represented by the TBPM frame.'''
        raise NotImplementedError()
    
    @bits_per_minute.setter
    def bits_per_minute(self, value : str) -> None:
        '''Sets the number of beats per minute in the main part of the audio.
        This value is represented by the TBPM frame.'''
        raise NotImplementedError()
    
    @property
    def composers(self) -> str:
        '''Gets the composers. The names are separated with the "/" character.
        This value is represented by the TCOM frame.'''
        raise NotImplementedError()
    
    @composers.setter
    def composers(self, value : str) -> None:
        '''Sets the composers. The names are separated with the "/" character.
        This value is represented by the TCOM frame.'''
        raise NotImplementedError()
    
    @property
    def content_type(self) -> str:
        '''Gets the content type.
        This value is represented by the TCON frame.'''
        raise NotImplementedError()
    
    @content_type.setter
    def content_type(self, value : str) -> None:
        '''Sets the content type.
        This value is represented by the TCON frame.'''
        raise NotImplementedError()
    
    @property
    def copyright(self) -> str:
        '''Gets the copyright message.
        This value is represented by the TCOP frame.'''
        raise NotImplementedError()
    
    @copyright.setter
    def copyright(self, value : str) -> None:
        '''Sets the copyright message.
        This value is represented by the TCOP frame.'''
        raise NotImplementedError()
    
    @property
    def date(self) -> str:
        '''Gets a numeric string in the DDMM format containing the date for the recording. This field is always four characters long.
        This value is represented by the TDAT frame.'''
        raise NotImplementedError()
    
    @date.setter
    def date(self, value : str) -> None:
        '''Sets a numeric string in the DDMM format containing the date for the recording. This field is always four characters long.
        This value is represented by the TDAT frame.'''
        raise NotImplementedError()
    
    @property
    def encoded_by(self) -> str:
        '''Gets the name of the person or organization that encoded the audio file.
        This value is represented by the TENC frame.'''
        raise NotImplementedError()
    
    @encoded_by.setter
    def encoded_by(self, value : str) -> None:
        '''Sets the name of the person or organization that encoded the audio file.
        This value is represented by the TENC frame.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> str:
        '''Gets the name of the label or publisher.
        This value is represented by the TPUB frame.'''
        raise NotImplementedError()
    
    @publisher.setter
    def publisher(self, value : str) -> None:
        '''Sets the name of the label or publisher.
        This value is represented by the TPUB frame.'''
        raise NotImplementedError()
    
    @property
    def time(self) -> str:
        '''Gets a numeric string in the HHMM format containing the time for the recording. This field is always four characters long.
        This value is represented by the TIME frame.'''
        raise NotImplementedError()
    
    @time.setter
    def time(self, value : str) -> None:
        '''Sets a numeric string in the HHMM format containing the time for the recording. This field is always four characters long.
        This value is represented by the TIME frame.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets the Title/Song name/Content description.
        This value is represented by the TIT2 frame.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets the Title/Song name/Content description.
        This value is represented by the TIT2 frame.'''
        raise NotImplementedError()
    
    @property
    def subtitle(self) -> str:
        '''Gets the Subtitle/Description refinement.
        This value is represented by the TIT3 frame.'''
        raise NotImplementedError()
    
    @subtitle.setter
    def subtitle(self, value : str) -> None:
        '''Sets the Subtitle/Description refinement.
        This value is represented by the TIT3 frame.'''
        raise NotImplementedError()
    
    @property
    def musical_key(self) -> str:
        '''Gets the musical key in which the sound starts.
        This value is represented by the TKEY frame.'''
        raise NotImplementedError()
    
    @musical_key.setter
    def musical_key(self, value : str) -> None:
        '''Sets the musical key in which the sound starts.
        This value is represented by the TKEY frame.'''
        raise NotImplementedError()
    
    @property
    def length_in_milliseconds(self) -> str:
        '''Gets the length of the audio file in milliseconds, represented as a numeric string.
        This value is represented by the TLEN frame.'''
        raise NotImplementedError()
    
    @length_in_milliseconds.setter
    def length_in_milliseconds(self, value : str) -> None:
        '''Sets the length of the audio file in milliseconds, represented as a numeric string.
        This value is represented by the TLEN frame.'''
        raise NotImplementedError()
    
    @property
    def original_album(self) -> str:
        '''Gets the original album/movie/show title.
        This value is represented by the TOAL frame.'''
        raise NotImplementedError()
    
    @original_album.setter
    def original_album(self, value : str) -> None:
        '''Sets the original album/movie/show title.
        This value is represented by the TOAL frame.'''
        raise NotImplementedError()
    
    @property
    def track_number(self) -> str:
        '''Gets a numeric string containing the order number of the audio-file on its original recording.
        This value is represented by the TRCK frame.'''
        raise NotImplementedError()
    
    @track_number.setter
    def track_number(self, value : str) -> None:
        '''Sets a numeric string containing the order number of the audio-file on its original recording.
        This value is represented by the TRCK frame.'''
        raise NotImplementedError()
    
    @property
    def size_in_bytes(self) -> str:
        '''Gets the size of the audio file in bytes, excluding the ID3v2 tag, represented as a numeric string.
        This value is represented by the TSIZ frame.'''
        raise NotImplementedError()
    
    @size_in_bytes.setter
    def size_in_bytes(self, value : str) -> None:
        '''Sets the size of the audio file in bytes, excluding the ID3v2 tag, represented as a numeric string.
        This value is represented by the TSIZ frame.'''
        raise NotImplementedError()
    
    @property
    def isrc(self) -> str:
        '''Gets the International Standard Recording Code (ISRC) (12 characters).
        This value is represented by the TSRC frame.'''
        raise NotImplementedError()
    
    @isrc.setter
    def isrc(self, value : str) -> None:
        '''Sets the International Standard Recording Code (ISRC) (12 characters).
        This value is represented by the TSRC frame.'''
        raise NotImplementedError()
    
    @property
    def software_hardware(self) -> str:
        '''Gets the used audio encoder and its settings when the file was encoded.
        This value is represented by the TSSE frame.'''
        raise NotImplementedError()
    
    @software_hardware.setter
    def software_hardware(self, value : str) -> None:
        '''Sets the used audio encoder and its settings when the file was encoded.
        This value is represented by the TSSE frame.'''
        raise NotImplementedError()
    
    @property
    def year(self) -> str:
        '''Gets a numeric string with a year of the recording. This frames is always four characters long (until the year 10000).
        This value is represented by the TYER frame.'''
        raise NotImplementedError()
    
    @year.setter
    def year(self, value : str) -> None:
        '''Sets a numeric string with a year of the recording. This frames is always four characters long (until the year 10000).
        This value is represented by the TYER frame.'''
        raise NotImplementedError()
    
    @property
    def comments(self) -> List[groupdocs.metadata.formats.audio.ID3V2CommentFrame]:
        '''Gets the user comments.
        This value is represented by the COMM frame.
        The frame is intended for any kind of full text information that does not fit in any other frame.'''
        raise NotImplementedError()
    
    @comments.setter
    def comments(self, value : List[groupdocs.metadata.formats.audio.ID3V2CommentFrame]) -> None:
        '''Sets the user comments.
        This value is represented by the COMM frame.
        The frame is intended for any kind of full text information that does not fit in any other frame.'''
        raise NotImplementedError()
    
    @property
    def attached_pictures(self) -> List[groupdocs.metadata.formats.audio.ID3V2AttachedPictureFrame]:
        '''Gets the attached pictures directly related to the audio file.
        This value is represented by the APIC frame.'''
        raise NotImplementedError()
    
    @attached_pictures.setter
    def attached_pictures(self, value : List[groupdocs.metadata.formats.audio.ID3V2AttachedPictureFrame]) -> None:
        '''Sets the attached pictures directly related to the audio file.
        This value is represented by the APIC frame.'''
        raise NotImplementedError()
    
    @property
    def track_play_counter(self) -> Optional[int]:
        '''Gets the number of times the file has been played.
        This value is represented by the PCNT frame.'''
        raise NotImplementedError()
    

class ID3V2TagFrame(groupdocs.metadata.common.CustomPackage):
    '''Represents a generic frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
    def __init__(self, frame_id : str, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2TagFrame` class.
        
        :param frame_id: The id of the frame (four characters matching the pattern [A-Z0-9]).
        :param data: The content of the frame.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    

class ID3V2TagFrameFlags:
    '''Represents flags used in a ID3v2 tag frame.'''
    
    def equals(self, other : groupdocs.metadata.formats.audio.ID3V2TagFrameFlags) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def tag_alter_preservation(self) -> bool:
        '''Gets the flag that tells the software what to do with this frame if it is unknown and the tag is altered in any way.
        This applies to all kinds of alterations,
        including adding more padding and reordering the frames.'''
        raise NotImplementedError()
    
    @property
    def file_alter_preservation(self) -> bool:
        '''Gets the flag that tells the software what to do with this frame if it is unknown and the file, excluding the tag, is altered.
        This does not apply when the audio is completely replaced with other audio data.'''
        raise NotImplementedError()
    
    @property
    def read_only(self) -> bool:
        '''Gets the tag that tells the software that the contents of this frame is intended to be read-only.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> bool:
        '''Gets a value indicating whether the frame is compressed.'''
        raise NotImplementedError()
    
    @property
    def encryption(self) -> bool:
        '''Gets a value indicating whether the frame is encrypted.
        If set one byte indicating with which method it was encrypted will be appended to the frame header.'''
        raise NotImplementedError()
    
    @property
    def grouping_identity(self) -> bool:
        '''Gets a value indicating whether the frame belongs to a group of frames.
        If set a group identifier byte is added to the frame header.
        Every frame with the same group identifier belongs to the same group.'''
        raise NotImplementedError()
    
    @property
    def unsynchronisation(self) -> bool:
        '''Gets a value indicating whether unsynchronisation was applied to this frame.'''
        raise NotImplementedError()
    
    @property
    def data_length_indicator(self) -> bool:
        '''Gets a value indicating whether a data length indicator has been added to
        the frame. The data length indicator is the value one would write
        as the \'Frame length\' if all of the frame format flags were
        zeroed, represented as a 32 bit synchsafe integer.'''
        raise NotImplementedError()
    

class ID3V2TextFrame(ID3V2TagFrame):
    '''Represents a text frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.
    Almost all frames starting with the T character fall into this category. There is only one exception, which is the TXXX frame represented by the :py:class:`groupdocs.metadata.formats.audio.ID3V2UserDefinedFrame` class.'''
    
    def __init__(self, id : str, encoding : groupdocs.metadata.formats.audio.ID3V2EncodingType, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2TextFrame` class.
        
        :param id: The frame id.
        :param encoding: The encoding of the frame.
        :param value: The frame value.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def text_encoding(self) -> groupdocs.metadata.formats.audio.ID3V2EncodingType:
        '''Gets the text encoding.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text value.'''
        raise NotImplementedError()
    

class ID3V2UrlLinkFrame(ID3V2TagFrame):
    '''Represents a URL link frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`. Name of the frame always starts with the W character.'''
    
    def __init__(self, id : str, url : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2UrlLinkFrame` class.
        
        :param id: The frame id.
        :param url: The URL which is the value of the frame.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def url(self) -> str:
        '''Gets the URL value.'''
        raise NotImplementedError()
    

class ID3V2UserDefinedFrame(ID3V2TagFrame):
    '''Represents a TXXX frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
    @overload
    def __init__(self, description : str, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2UserDefinedFrame` class.
        
        :param description: The description.
        :param value: The value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, encoding : groupdocs.metadata.formats.audio.ID3V2EncodingType, description : str, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2UserDefinedFrame` class.
        
        :param encoding: The encoding of the frame.
        :param description: The description.
        :param value: The text value.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> groupdocs.metadata.formats.audio.ID3V2EncodingType:
        '''Gets the encoding of the frame.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the description.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the value.'''
        raise NotImplementedError()
    

class ID3V2UserDefinedUrlLinkFrame(ID3V2TagFrame):
    '''Represents a WXXX frame in an :py:class:`groupdocs.metadata.formats.audio.ID3V2Tag`.'''
    
    @overload
    def __init__(self, description : str, url : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2UserDefinedUrlLinkFrame` class.
        
        :param description: The description.
        :param url: The actual value of the frame.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, encoding : groupdocs.metadata.formats.audio.ID3V2EncodingType, description : str, url : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.ID3V2UserDefinedUrlLinkFrame` class.
        
        :param encoding: The encoding of the frame.
        :param description: The description.
        :param url: The actual value of the frame.'''
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
    def id(self) -> str:
        '''Gets the id of the frame (four characters matching the pattern [A-Z0-9]).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> groupdocs.metadata.formats.audio.ID3V2TagFrameFlags:
        '''Gets the frame flags.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the frame data.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> groupdocs.metadata.formats.audio.ID3V2EncodingType:
        '''Gets the encoding of the frame.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the description.'''
        raise NotImplementedError()
    
    @property
    def url(self) -> str:
        '''Gets the URL.'''
        raise NotImplementedError()
    

class LyricsField(groupdocs.metadata.common.MetadataProperty):
    '''Represents a :py:class:`groupdocs.metadata.formats.audio.LyricsTag` field.'''
    
    def __init__(self, id : str, data : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.LyricsField` class.
        
        :param id: The three character field id.
        :param data: The field data.'''
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
    def id(self) -> str:
        '''Gets the id of the field (it\'s always three characters long).'''
        raise NotImplementedError()
    
    @property
    def size(self) -> str:
        '''Gets the string representation of the field size.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> str:
        '''Gets the field data.'''
        raise NotImplementedError()
    

class LyricsTag(groupdocs.metadata.common.CustomPackage):
    '''Represents Lyrics3 v2.00 metadata.
    Please find more information at `http://id3.org/Lyrics3v2 <>`.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.LyricsTag` class.'''
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
    
    def set(self, field : groupdocs.metadata.formats.audio.LyricsField) -> None:
        '''Adds or replaces the specified Lyrics3 field.
        
        :param field: The field to be set.'''
        raise NotImplementedError()
    
    def remove(self, id : str) -> None:
        '''Removes the field with the specified id.
        
        :param id: The field identifier.'''
        raise NotImplementedError()
    
    def get(self, id : str) -> str:
        '''Gets the value of the field with the specified id.
        
        :param id: The id of the field.
        :returns: The value if the tag contains a field with the specified id; otherwise, null.'''
        raise NotImplementedError()
    
    def to_list(self) -> Sequence[groupdocs.metadata.formats.audio.LyricsField]:
        '''Creates a list from the package.
        
        :returns: A list of all fields contained in the Lyrics3 tag.'''
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
    def lyrics(self) -> str:
        '''Gets the lyrics.
        This value is represented by the LYR field.'''
        raise NotImplementedError()
    
    @lyrics.setter
    def lyrics(self, value : str) -> None:
        '''Sets the lyrics.
        This value is represented by the LYR field.'''
        raise NotImplementedError()
    
    @property
    def additional_info(self) -> str:
        '''Gets the additional information.
        This value is represented by the INF field.'''
        raise NotImplementedError()
    
    @additional_info.setter
    def additional_info(self, value : str) -> None:
        '''Sets the additional information.
        This value is represented by the INF field.'''
        raise NotImplementedError()
    
    @property
    def author(self) -> str:
        '''Gets the author.
        This value is represented by the AUT field.'''
        raise NotImplementedError()
    
    @author.setter
    def author(self, value : str) -> None:
        '''Sets the author.
        This value is represented by the AUT field.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> str:
        '''Gets the album name.
        This value is represented by the EAL field.'''
        raise NotImplementedError()
    
    @album.setter
    def album(self, value : str) -> None:
        '''Sets the album name.
        This value is represented by the EAL field.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the artist name.
        This value is represented by the EAR field.'''
        raise NotImplementedError()
    
    @artist.setter
    def artist(self, value : str) -> None:
        '''Sets the artist name.
        This value is represented by the EAR field.'''
        raise NotImplementedError()
    
    @property
    def track(self) -> str:
        '''Gets the track title.
        This value is represented by the ETT field.'''
        raise NotImplementedError()
    
    @track.setter
    def track(self, value : str) -> None:
        '''Sets the track title.
        This value is represented by the ETT field.'''
        raise NotImplementedError()
    

class MP3RootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in an MP3 audio.'''
    
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
    
    def remove_ape_v2(self) -> None:
        '''Removes the APEv2 audio tag.'''
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
    def mpeg_audio_package(self) -> groupdocs.metadata.formats.mpeg.MpegAudioPackage:
        '''Gets the MPEG audio metadata package.'''
        raise NotImplementedError()
    
    @property
    def id3v1(self) -> groupdocs.metadata.formats.audio.ID3V1Tag:
        '''Gets the ID3v1 metadata tag.
        Please find more information at `http://id3.org/ID3v1 <http://id3.org/ID3v1>`.'''
        raise NotImplementedError()
    
    @id3v1.setter
    def id3v1(self, value : groupdocs.metadata.formats.audio.ID3V1Tag) -> None:
        '''Sets the ID3v1 metadata tag.
        Please find more information at `http://id3.org/ID3v1 <http://id3.org/ID3v1>`.'''
        raise NotImplementedError()
    
    @property
    def id3v2(self) -> groupdocs.metadata.formats.audio.ID3V2Tag:
        '''Gets the ID3v2 metadata tag.'''
        raise NotImplementedError()
    
    @id3v2.setter
    def id3v2(self, value : groupdocs.metadata.formats.audio.ID3V2Tag) -> None:
        '''Sets the ID3v2 metadata tag.'''
        raise NotImplementedError()
    
    @property
    def lyrics_3v2(self) -> groupdocs.metadata.formats.audio.LyricsTag:
        '''Gets the Lyrics3v2 metadata tag.'''
        raise NotImplementedError()
    
    @lyrics_3v2.setter
    def lyrics_3v2(self, value : groupdocs.metadata.formats.audio.LyricsTag) -> None:
        '''Sets the Lyrics3v2 metadata tag.'''
        raise NotImplementedError()
    
    @property
    def ape_v2(self) -> groupdocs.metadata.formats.audio.ApePackage:
        '''Gets the APE v2 metadata.'''
        raise NotImplementedError()
    
    @property
    def xmp_package(self) -> groupdocs.metadata.standards.xmp.XmpPacketWrapper:
        '''Gets the XMP metadata package.'''
        raise NotImplementedError()
    
    @xmp_package.setter
    def xmp_package(self, value : groupdocs.metadata.standards.xmp.XmpPacketWrapper) -> None:
        '''Sets the XMP metadata package.'''
        raise NotImplementedError()
    

class WavPackage(groupdocs.metadata.common.CustomPackage):
    '''Represents a native metadata package in a WAV audio file.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.formats.audio.WavPackage` class.'''
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
    def audio_format(self) -> int:
        '''Gets the audio format.
        PCM = 1 (i.e. Linear quantization). Values other than 1 indicate some form of compression.'''
        raise NotImplementedError()
    
    @property
    def number_of_channels(self) -> int:
        '''Gets the number of channels.'''
        raise NotImplementedError()
    
    @property
    def sample_rate(self) -> int:
        '''Gets the sample rate.'''
        raise NotImplementedError()
    
    @property
    def byte_rate(self) -> int:
        '''Gets the byte rate.'''
        raise NotImplementedError()
    
    @property
    def block_align(self) -> int:
        '''Gets the block align.'''
        raise NotImplementedError()
    
    @property
    def bits_per_sample(self) -> int:
        '''Gets the bits per sample value.'''
        raise NotImplementedError()
    

class WavRootPackage(groupdocs.metadata.common.RootMetadataPackage):
    '''Represents the root package allowing working with metadata in a WAV audio.'''
    
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
    def wav_package(self) -> groupdocs.metadata.formats.audio.WavPackage:
        '''Gets the WAV native metadata package.'''
        raise NotImplementedError()
    
    @property
    def riff_info_package(self) -> groupdocs.metadata.formats.riff.RiffInfoPackage:
        '''Gets the package containing RIFF Info tags.'''
        raise NotImplementedError()
    

class ID3V1Genre:
    '''Specifies genres used in an Id3v1 tag.'''
    
    BLUES : ID3V1Genre
    '''Represents the Blues genre.'''
    CLASSIC_ROCK : ID3V1Genre
    '''Represents the Classic Rock genre.'''
    COUNTRY : ID3V1Genre
    '''Represents the Country genre.'''
    DANCE : ID3V1Genre
    '''Represents the Dance genre.'''
    DISCO : ID3V1Genre
    '''Represents the Disco genre.'''
    FUNK : ID3V1Genre
    '''Represents the Funk genre.'''
    GRUNGE : ID3V1Genre
    '''Represents the Grunge genre.'''
    HIP_HOP : ID3V1Genre
    '''Represents the Hip-Hop genre.'''
    JAZZ : ID3V1Genre
    '''Represents the Jazz genre.'''
    METAL : ID3V1Genre
    '''Represents the Metal genre.'''
    NEW_AGE : ID3V1Genre
    '''Represents the New Age genre.'''
    OLDIES : ID3V1Genre
    '''Represents the Oldies genre.'''
    OTHER : ID3V1Genre
    '''Represents the Other genre.'''
    POP : ID3V1Genre
    '''Represents the Pop genre.'''
    RHYTHM_AND_BLUES : ID3V1Genre
    '''Represents the Rhythm and Blues genre.'''
    RAP : ID3V1Genre
    '''Represents the Rap genre.'''
    REGGAE : ID3V1Genre
    '''Represents the Reggae genre.'''
    ROCK : ID3V1Genre
    '''Represents the Rock genre.'''
    TECHNO : ID3V1Genre
    '''Represents the Techno genre.'''
    INDUSTRIAL : ID3V1Genre
    '''Represents the Industrial genre.'''
    ALTERNATIVE : ID3V1Genre
    '''Represents the Alternative genre.'''
    SKA : ID3V1Genre
    '''Represents the Ska genre.'''
    DEATH_METAL : ID3V1Genre
    '''Represents the Death Metal genre.'''
    PRANKS : ID3V1Genre
    '''Represents the Pranks genre.'''
    SOUNDTRACK : ID3V1Genre
    '''Represents the Soundtrack genre.'''
    EURO_TECHNO : ID3V1Genre
    '''Represents the Euro-Techno genre.'''
    AMBIENT : ID3V1Genre
    '''Represents the Ambient genre.'''
    TRIP_HOP : ID3V1Genre
    '''Represents the Trip-Hop genre.'''
    VOCAL : ID3V1Genre
    '''Represents the Vocal genre.'''
    JAZZ_AND_FUNK : ID3V1Genre
    '''Represents the JazzAndFunk genre.'''
    FUSION : ID3V1Genre
    '''Represents the Fusion genre.'''
    TRANCE : ID3V1Genre
    '''Represents the Trance genre.'''
    CLASSICAL : ID3V1Genre
    '''Represents the Classical genre.'''
    INSTRUMENTAL : ID3V1Genre
    '''Represents the Instrumental genre.'''
    ACID : ID3V1Genre
    '''Represents the Acid genre.'''
    HOUSE : ID3V1Genre
    '''Represents the House genre.'''
    GAME : ID3V1Genre
    '''Represents the Game genre.'''
    SOUND_CLIP : ID3V1Genre
    '''Represents the Sound Clip genre.'''
    GOSPEL : ID3V1Genre
    '''Represents the Gospel genre.'''
    NOISE : ID3V1Genre
    '''Represents the Noise genre.'''
    ALTERNATIVE_ROCK : ID3V1Genre
    '''Represents the Alternative Rock genre.'''
    BASS : ID3V1Genre
    '''Represents the Bass genre.'''
    SOUL : ID3V1Genre
    '''Represents the Soul genre.'''
    PUNK : ID3V1Genre
    '''Represents the Punk genre.'''
    SPACE : ID3V1Genre
    '''Represents the Space genre.'''
    MEDITATIVE : ID3V1Genre
    '''Represents the Meditative genre.'''
    INSTRUMENTAL_POP : ID3V1Genre
    '''Represents the Instrumental Pop genre.'''
    INSTRUMENTAL_ROCK : ID3V1Genre
    '''Represents the Instrumental Rock genre.'''
    ETHNIC : ID3V1Genre
    '''Represents the Ethnic genre.'''
    GOTHIC : ID3V1Genre
    '''Represents the Gothic genre.'''
    DARKWAVE : ID3V1Genre
    '''Represents the Darkwave genre.'''
    TECHNO_INDUSTRIAL : ID3V1Genre
    '''Represents the Techno-Industrial genre.'''
    ELECTRONIC : ID3V1Genre
    '''Represents the Electronic genre.'''
    POP_FOLK : ID3V1Genre
    '''Represents the Pop-Folk genre.'''
    EURODANCE : ID3V1Genre
    '''Represents the Eurodance genre.'''
    DREAM : ID3V1Genre
    '''Represents the Dream genre.'''
    SOUTHERN_ROCK : ID3V1Genre
    '''Represents the Southern Rock genre.'''
    COMEDY : ID3V1Genre
    '''Represents the Comedy genre.'''
    CULT : ID3V1Genre
    '''Represents the Cult genre.'''
    GANGSTA : ID3V1Genre
    '''Represents the Gangsta genre.'''
    TOP40 : ID3V1Genre
    '''Represents the Top 40 genre.'''
    CHRISTIAN_RAP : ID3V1Genre
    '''Represents the Christian Rap genre.'''
    POP_FUNK : ID3V1Genre
    '''Represents the Pop/Funk genre.'''
    JUNGLE : ID3V1Genre
    '''Represents the Jungle genre.'''
    NATIVE_AMERICAN : ID3V1Genre
    '''Represents the Native American genre.'''
    CABARET : ID3V1Genre
    '''Represents the Cabaret genre.'''
    NEW_WAVE : ID3V1Genre
    '''Represents the New Wave genre.'''
    PSYCHEDELIC : ID3V1Genre
    '''Represents the Psychedelic genre.'''
    RAVE : ID3V1Genre
    '''Represents the Rave genre.'''
    SHOWTUNES : ID3V1Genre
    '''Represents the Showtunes genre.'''
    TRAILER : ID3V1Genre
    '''Represents the Trailer genre.'''
    LO_FI : ID3V1Genre
    '''Represents the Lo-Fi genre.'''
    TRIBAL : ID3V1Genre
    '''Represents the Tribal genre.'''
    ACID_PUNK : ID3V1Genre
    '''Represents the Acid Punk genre.'''
    ACID_JAZZ : ID3V1Genre
    '''Represents the Acid Jazz genre.'''
    POLKA : ID3V1Genre
    '''Represents the Polka genre.'''
    RETRO : ID3V1Genre
    '''Represents the Retro genre.'''
    MUSICAL : ID3V1Genre
    '''Represents the Musical genre.'''
    ROCK_N_ROLL : ID3V1Genre
    '''Represents the Rock \'n\' Roll genre.'''
    HARD_ROCK : ID3V1Genre
    '''Represents the Hard Rock genre.'''

class ID3V2AttachedPictureType:
    '''Represents the type of an attached picture.'''
    
    OTHER : ID3V2AttachedPictureType
    '''Attached picture of any other type.'''
    FILE_ICON_32X32 : ID3V2AttachedPictureType
    '''32x32 pixels file icon (PNG only).'''
    OTHER_FILE_ICON : ID3V2AttachedPictureType
    '''Other file icon.'''
    COVER_FRONT : ID3V2AttachedPictureType
    '''Cover (front).'''
    COVER_BACK : ID3V2AttachedPictureType
    '''Cover (back).'''
    LEAFLET_PAGE : ID3V2AttachedPictureType
    '''Leaflet page.'''
    MEDIA : ID3V2AttachedPictureType
    '''Media (e.g. label side of CD).'''
    LEAD_ARTIST : ID3V2AttachedPictureType
    '''Lead artist/lead performer/soloist.'''
    ARTIST : ID3V2AttachedPictureType
    '''Artist/performer.'''
    CONDUCTOR : ID3V2AttachedPictureType
    '''Conductor.'''
    BAND : ID3V2AttachedPictureType
    '''Band/Orchestra.'''
    COMPOSER : ID3V2AttachedPictureType
    '''Composer/music author.'''
    LYRICIST : ID3V2AttachedPictureType
    '''Lyricist/text writer.'''
    RECORDING_LOCATION : ID3V2AttachedPictureType
    '''Recording Location.'''
    DURING_RECORDING : ID3V2AttachedPictureType
    '''During recording.'''
    DURING_PERFORMANCE : ID3V2AttachedPictureType
    '''During performance.'''
    VIDEO_SCREEN_CAPTURE : ID3V2AttachedPictureType
    '''Movie/video screen capture.'''
    BRIGHT_COLOURED_FISH : ID3V2AttachedPictureType
    '''A bright coloured fish.'''
    ILLUSTRATION : ID3V2AttachedPictureType
    '''Illustration.'''
    ARTIST_LOGO : ID3V2AttachedPictureType
    '''Band/artist logotype.'''
    STUDIO_LOGO : ID3V2AttachedPictureType
    '''Publisher/Studio logotype.'''

class ID3V2EncodingType:
    '''Defines different types of text encoding used in ID3v2.'''
    
    ISO88591 : ID3V2EncodingType
    '''The ISO-8859-1 encoding.'''
    UTF16 : ID3V2EncodingType
    '''The UTF-16 encoding with BOM.'''
    UTF_16_BE : ID3V2EncodingType
    '''The UTF-16 encoding without BOM.'''
    UTF8 : ID3V2EncodingType
    '''The UTF-8 encoding.'''

