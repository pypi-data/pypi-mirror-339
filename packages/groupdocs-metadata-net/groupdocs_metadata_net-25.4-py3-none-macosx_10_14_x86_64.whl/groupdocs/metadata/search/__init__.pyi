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

class AndSpecification(Specification):
    '''Represents a composite specification that uses the logical AND operator to combine two given search specifications.'''
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def left(self) -> groupdocs.metadata.search.Specification:
        '''Gets the left specification.'''
        raise NotImplementedError()
    
    @property
    def right(self) -> groupdocs.metadata.search.Specification:
        '''Gets the right specification.'''
        raise NotImplementedError()
    

class AnySpecification(Specification):
    '''Represents a specification that applies no filters to a property.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    

class ContainsTagSpecification(Specification):
    '''Represents a specification that checks whether the passed property contains the specified tag.'''
    
    def __init__(self, tag : groupdocs.metadata.tagging.PropertyTag) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.ContainsTagSpecification` class.
        
        :param tag: The tag a property must contain to satisfy the specification.'''
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def tag(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag a property must contain to satisfy the specification.'''
        raise NotImplementedError()
    

class FallsIntoCategorySpecification(Specification):
    '''Represents a specification that verifies whether the passed property falls into a particular category
    (i.e. contains tags from the specified category).'''
    
    def __init__(self, category : groupdocs.metadata.tagging.TagCategory) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.FallsIntoCategorySpecification` class.
        
        :param category: The category into which a property must fall to satisfy the specification.'''
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def category(self) -> groupdocs.metadata.tagging.TagCategory:
        '''Gets the category into which a property must fall to satisfy the specification.'''
        raise NotImplementedError()
    

class NotSpecification(Specification):
    '''Represents a composite specification that negates any other specification.'''
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def wrapped(self) -> groupdocs.metadata.search.Specification:
        '''Gets the base specification to be negated.'''
        raise NotImplementedError()
    

class OfTypeSpecification(Specification):
    '''Represents a specification that filters properties of a particular type.'''
    
    def __init__(self, property_type : groupdocs.metadata.common.MetadataPropertyType) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.OfTypeSpecification` class.
        
        :param property_type: The type of properties that satisfy the specification.'''
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def property_type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the type of properties that satisfy the specification.'''
        raise NotImplementedError()
    

class OrSpecification(Specification):
    '''Represents a composite specification that uses the logical OR operator to combine two given search specifications.'''
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def left(self) -> groupdocs.metadata.search.Specification:
        '''Gets the left specification.'''
        raise NotImplementedError()
    
    @property
    def right(self) -> groupdocs.metadata.search.Specification:
        '''Gets the right specification.'''
        raise NotImplementedError()
    

class Specification:
    '''Provides a base abstract class for search specifications that can be combined using logical operators.'''
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    

class WithNameSpecification(Specification):
    '''Represents a specification that filters properties with a particular name.'''
    
    @overload
    def __init__(self, property_name : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.WithNameSpecification` class.
        
        :param property_name: The type of properties that satisfy the specification.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, property_name : str, ignore_case : bool) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.WithNameSpecification` class.
        
        :param property_name: The type of properties that satisfy the specification.
        :param ignore_case: A value indicating whether the case of the strings being compared should be ignored.'''
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def property_name(self) -> str:
        '''Gets the name of properties that satisfy the specification.'''
        raise NotImplementedError()
    
    @property
    def ignore_case(self) -> bool:
        '''Gets a value indicating whether the case of the strings being compared should be ignored.'''
        raise NotImplementedError()
    

class WithValueSpecification(Specification):
    '''Represents a specification that filters properties with a particular value.'''
    
    def __init__(self, property_value : Any) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.search.WithNameSpecification` class.
        
        :param property_value: The type of properties that satisfy the specification.'''
        raise NotImplementedError()
    
    def is_satisfied_by(self, candidate : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Verifies whether a :py:class:`groupdocs.metadata.common.MetadataProperty` satisfies the specification.
        
        :param candidate: A metadata property to test.
        :returns: True, if the passed property satisfies the specification; otherwise, false.'''
        raise NotImplementedError()
    
    def both(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical AND operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def either(self, other : groupdocs.metadata.search.Specification) -> groupdocs.metadata.search.Specification:
        '''Combines two search specifications using the logical OR operator.
        
        :param other: A specification to combine with.
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    def is_not(self) -> groupdocs.metadata.search.Specification:
        '''Negates the specification.
        
        :returns: A composite specification.'''
        raise NotImplementedError()
    
    @property
    def property_value(self) -> Any:
        '''Gets the value of properties that satisfy the specification.'''
        raise NotImplementedError()
    

