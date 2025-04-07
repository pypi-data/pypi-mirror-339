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

class Fb2Author(groupdocs.metadata.common.CustomPackage):
    '''Represents an information about the author of the book.'''
    
    def __init__(self, first_name : str, middle_name : str, last_name : str, nick_name : str, home_page : str, email : str, id : str) -> None:
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
    def first_name(self) -> str:
        '''Gets the First Name.'''
        raise NotImplementedError()
    
    @property
    def middle_name(self) -> str:
        '''Gets the Middle Name.'''
        raise NotImplementedError()
    
    @property
    def last_name(self) -> str:
        '''Gets the Last Name.'''
        raise NotImplementedError()
    
    @property
    def nick_name(self) -> str:
        '''Gets the NickName.'''
        raise NotImplementedError()
    
    @property
    def home_page(self) -> str:
        '''Gets the HomePage.'''
        raise NotImplementedError()
    
    @property
    def email(self) -> str:
        '''Gets the Email.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> str:
        '''Gets the Id.'''
        raise NotImplementedError()
    

class Fb2DocumentInfo(groupdocs.metadata.common.CustomPackage):
    '''Description of information about the work (including translation, but excluding publication).'''
    
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
    def authors(self) -> List[groupdocs.metadata.formats.ebook.fb2.Fb2Author]:
        '''Information about the author of the document'''
        raise NotImplementedError()
    
    @property
    def program_used(self) -> str:
        '''The programs that were used in preparing the document are listed.'''
        raise NotImplementedError()
    
    @property
    def date(self) -> str:
        '''Date'''
        raise NotImplementedError()
    
    @property
    def src_url(self) -> str:
        '''Where did the original document available online come from'''
        raise NotImplementedError()
    
    @property
    def src_ocr(self) -> str:
        '''The author of the OCR or original document posted online.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> str:
        '''Gets the Id.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> str:
        '''FB2 document version.'''
        raise NotImplementedError()
    
    @property
    def publishers(self) -> List[groupdocs.metadata.formats.ebook.fb2.Fb2Author]:
        '''Information about the author of the document'''
        raise NotImplementedError()
    

class Fb2PublishInfo(groupdocs.metadata.common.CustomPackage):
    '''Information about the paper (or other) publication on the basis of which the FB2.x document was created. It is not recommended to fill in data from an arbitrary publication if the source is unknown, except for the case when verification was carried out on it and the document was brought to the form of this publication. If the source is unknown, it is better to omit this element altogether.'''
    
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
    def book_name(self) -> str:
        '''The title of the original (paper) book.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> str:
        '''The title of the original (paper) book.'''
        raise NotImplementedError()
    
    @property
    def city(self) -> str:
        '''City, place of publication of the original (paper) book.'''
        raise NotImplementedError()
    
    @property
    def year(self) -> str:
        '''Year of publication of the original (paper) book.'''
        raise NotImplementedError()
    
    @property
    def isbn(self) -> str:
        '''ISBN of the original (paper) book.'''
        raise NotImplementedError()
    
    @property
    def sequence(self) -> groupdocs.metadata.formats.ebook.fb2.Fb2Sequence:
        '''The series of publications that the book belongs to and the number in the series.'''
        raise NotImplementedError()
    

class Fb2Sequence(groupdocs.metadata.common.CustomPackage):
    '''Represents an information about the sequence of the book.'''
    
    def __init__(self, name : str, number : int, lang : str) -> None:
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
    def name(self) -> str:
        '''Series title'''
        raise NotImplementedError()
    
    @property
    def number(self) -> Optional[int]:
        '''Book number in the series.'''
        raise NotImplementedError()
    
    @property
    def lang(self) -> str:
        '''Gets the language.'''
        raise NotImplementedError()
    

class Fb2TitleInfo(groupdocs.metadata.common.CustomPackage):
    '''Description of information about the work (including translation, but excluding publication).'''
    
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
    def book_title(self) -> str:
        '''The title of the book. It can either match the book title (book-name) or differ (for example, when there are several works under one cover).'''
        raise NotImplementedError()
    
    @property
    def authors(self) -> List[groupdocs.metadata.formats.ebook.fb2.Fb2Author]:
        '''Information about the author of the book'''
        raise NotImplementedError()
    
    @property
    def genres(self) -> List[groupdocs.metadata.formats.ebook.fb2.Fb2Genre]:
        '''Describes the genre of the book. It is used to place the book in the library rubricator, for this reason the list of possible genres is strictly defined. It is allowed to specify several genres.'''
        raise NotImplementedError()
    
    @property
    def keywords(self) -> str:
        '''List of keywords for the book. Intended for use by search engines.'''
        raise NotImplementedError()
    
    @property
    def date(self) -> str:
        '''Date'''
        raise NotImplementedError()
    
    @property
    def coverpage(self) -> List[str]:
        '''Contains a link to a graphic image of the book cover.'''
        raise NotImplementedError()
    
    @property
    def lang(self) -> str:
        '''Language of the book (work)'''
        raise NotImplementedError()
    
    @property
    def src_lang(self) -> str:
        '''Original language (for translations).'''
        raise NotImplementedError()
    
    @property
    def translators(self) -> List[groupdocs.metadata.formats.ebook.fb2.Fb2Author]:
        '''Information about the author of the book'''
        raise NotImplementedError()
    
    @property
    def sequence(self) -> groupdocs.metadata.formats.ebook.fb2.Fb2Sequence:
        '''The series of publications that the book belongs to and the number in the series.'''
        raise NotImplementedError()
    

class Fb2Genre:
    '''Defines Fb2 genres'''
    
    SF_HISTORY : Fb2Genre
    SF_ACTION : Fb2Genre
    SF_EPIC : Fb2Genre
    SF_HEROIC : Fb2Genre
    SF_DETECTIVE : Fb2Genre
    SF_CYBERPUNK : Fb2Genre
    SF_SPACE : Fb2Genre
    SF_SOCIAL : Fb2Genre
    SF_HORROR : Fb2Genre
    SF_HUMOR : Fb2Genre
    SF_FANTASY : Fb2Genre
    SF : Fb2Genre
    DET_CLASSIC : Fb2Genre
    DET_POLICE : Fb2Genre
    DET_ACTION : Fb2Genre
    DET_IRONY : Fb2Genre
    DET_HISTORY : Fb2Genre
    DET_ESPIONAGE : Fb2Genre
    DET_CRIME : Fb2Genre
    DET_POLITICAL : Fb2Genre
    DET_MANIAC : Fb2Genre
    DET_HARD : Fb2Genre
    THRILLER : Fb2Genre
    DETECTIVE : Fb2Genre
    PROSE_CLASSIC : Fb2Genre
    PROSE_HISTORY : Fb2Genre
    PROSE_CONTEMPORARY : Fb2Genre
    PROSE_COUNTER : Fb2Genre
    PROSE_RUS_CLASSIC : Fb2Genre
    PROSE_SU_CLASSICS : Fb2Genre
    LOVE_CONTEMPORARY : Fb2Genre
    LOVE_HISTORY : Fb2Genre
    LOVE_DETECTIVE : Fb2Genre
    LOVE_SHORT : Fb2Genre
    LOVE_EROTICA : Fb2Genre
    ADV_WESTERN : Fb2Genre
    ADV_HISTORY : Fb2Genre
    ADV_INDIAN : Fb2Genre
    ADV_MARITIME : Fb2Genre
    ADV_GEO : Fb2Genre
    ADV_ANIMAL : Fb2Genre
    ADVENTURE : Fb2Genre
    CHILD_TALE : Fb2Genre
    CHILD_VERSE : Fb2Genre
    CHILD_PROSE : Fb2Genre
    CHILD_SF : Fb2Genre
    CHILD_DET : Fb2Genre
    CHILD_ADV : Fb2Genre
    CHILD_EDUCATION : Fb2Genre
    CHILDREN : Fb2Genre
    POETRY : Fb2Genre
    DRAMATURGY : Fb2Genre
    ANTIQUE_ANT : Fb2Genre
    ANTIQUE_EUROPEAN : Fb2Genre
    ANTIQUE_RUSSIAN : Fb2Genre
    ANTIQUE_EAST : Fb2Genre
    ANTIQUE_MYTHS : Fb2Genre
    ANTIQUE : Fb2Genre
    SCI_HISTORY : Fb2Genre
    SCI_PSYCHOLOGY : Fb2Genre
    SCI_CULTURE : Fb2Genre
    SCI_RELIGION : Fb2Genre
    SCI_PHILOSOPHY : Fb2Genre
    SCI_POLITICS : Fb2Genre
    SCI_BUSINESS : Fb2Genre
    SCI_JURIS : Fb2Genre
    SCI_LINGUISTIC : Fb2Genre
    SCI_MEDICINE : Fb2Genre
    SCI_PHYS : Fb2Genre
    SCI_MATH : Fb2Genre
    SCI_CHEM : Fb2Genre
    SCI_BIOLOGY : Fb2Genre
    SCI_TECH : Fb2Genre
    SCIENCE : Fb2Genre
    COMP_WWW : Fb2Genre
    COMP_PROGRAMMING : Fb2Genre
    COMP_HARD : Fb2Genre
    COMP_SOFT : Fb2Genre
    COMP_DB : Fb2Genre
    COMP_OSNET : Fb2Genre
    COMPUTERS : Fb2Genre
    REF_ENCYC : Fb2Genre
    REF_DICT : Fb2Genre
    REF_REF : Fb2Genre
    REF_GUIDE : Fb2Genre
    REFERENCE : Fb2Genre
    NONF_BIOGRAPHY : Fb2Genre
    NONF_PUBLICISM : Fb2Genre
    NONF_CRITICISM : Fb2Genre
    DESIGN : Fb2Genre
    NONFICTION : Fb2Genre
    RELIGION_REL : Fb2Genre
    RELIGION_ESOTERICS : Fb2Genre
    RELIGION_SELF : Fb2Genre
    RELIGION : Fb2Genre
    HUMOR_ANECDOTE : Fb2Genre
    HUMOR_PROSE : Fb2Genre
    HUMOR_VERSE : Fb2Genre
    HUMOR : Fb2Genre
    HOME_COOKING : Fb2Genre
    HOME_PETS : Fb2Genre
    HOME_CRAFTS : Fb2Genre
    HOME_ENTERTAIN : Fb2Genre
    HOME_HEALTH : Fb2Genre
    HOME_GARDEN : Fb2Genre
    HOME_DIY : Fb2Genre
    HOME_SPORT : Fb2Genre
    HOME_SEX : Fb2Genre
    HOME : Fb2Genre

