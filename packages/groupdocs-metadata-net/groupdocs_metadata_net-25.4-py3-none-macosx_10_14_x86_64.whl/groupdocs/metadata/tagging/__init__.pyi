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

class ContentTagCategory(TagCategory):
    '''Provides tags that are attached to metadata properties describing the content of a file.
    The tags are useful to find out the content language, type (genre), subject, rating, etc.'''
    
    @property
    def description(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels properties containing a description of a file.'''
        raise NotImplementedError()
    
    @property
    def comment(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a comment left by a person who contributed in file creation.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels the name given to a file.'''
        raise NotImplementedError()
    
    @property
    def thumbnail(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates a thumbnail image attached to a file.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag indicating the language of the intellectual content of a file.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the subject the intellectual content is focused on.'''
        raise NotImplementedError()
    
    @property
    def table_of_contents(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag indicating properties containing the table of contents of a file.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates the nature or genre of the content of a file.
        It also includes terms describing general categories, functions, aggregation levels for the content.'''
        raise NotImplementedError()
    
    @property
    def rating(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag labeling a user assigned rating of a file.'''
        raise NotImplementedError()
    
    @property
    def keywords(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a metadata property containing keywords that describe the content.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates a metadata property containing information about the format of a file.'''
        raise NotImplementedError()
    
    @property
    def status(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the status of a file.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag labeling the version or revision of a file.'''
        raise NotImplementedError()
    
    @property
    def shared_doc(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes which is a common document for several manufacturers.'''
        raise NotImplementedError()
    
    @property
    def hyperlinks_changed(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the indicates that one or more hyperlinks in this part have been updated exclusively in this part by the manufacturer.'''
        raise NotImplementedError()
    
    @property
    def body(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the body of a email file.'''
        raise NotImplementedError()
    
    @property
    def album(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the album name of a audio file.'''
        raise NotImplementedError()
    

class CorporateTagCategory(TagCategory):
    '''Provides tags intended to mark metadata properties related to a company that participated in file creation.'''
    
    @property
    def company(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property containing information about a company contributed to file creation.
        Alternatively, the tag can refer to a company the file content is about.'''
        raise NotImplementedError()
    
    @property
    def manager(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels information about a person who managed the making process of a file.'''
        raise NotImplementedError()
    

class DocumentTagCategory(TagCategory):
    '''Provides tags that are applied to document-specific properties only.
    The tags can be useful to determine from which part of an office document a property was extracted.'''
    
    @property
    def only_update(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates that the property it not full removal from document.'''
        raise NotImplementedError()
    
    @property
    def built_in(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates that the property it labels is built-in.'''
        raise NotImplementedError()
    
    @property
    def read_only(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates that the property it labels is read-only and cannot be changed by GroupDocs.Metadata.'''
        raise NotImplementedError()
    
    @property
    def hidden_data(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag indicating a document part that is not visible for regular users.'''
        raise NotImplementedError()
    
    @property
    def user_comment(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels user comments shown in the document content.'''
        raise NotImplementedError()
    
    @property
    def page(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a property holding information about a document page.'''
        raise NotImplementedError()
    
    @property
    def statistic(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag indicating a property containing document statistics (word count, character count, etc).'''
        raise NotImplementedError()
    
    @property
    def field(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a property holding information about a form field or calculated field extracted from a document.'''
        raise NotImplementedError()
    
    @property
    def revision(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Get the tag labeling a property containing information about a document revision (tracked change).'''
        raise NotImplementedError()
    

class LegalTagCategory(TagCategory):
    '''Provides tags that are attached to metadata properties holding information about the owners of the file content
    and the rules under which the content can be used.'''
    
    @property
    def copyright(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a copyright notice provided by the owner.'''
        raise NotImplementedError()
    
    @property
    def owner(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes information about the owners of a file.'''
        raise NotImplementedError()
    
    @property
    def usage_terms(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels instructions on how the file can be used.'''
        raise NotImplementedError()
    

class OriginTagCategory(TagCategory):
    '''Provides tags that help a user to determine the origin of a file (e.g. template or another source).'''
    
    @property
    def template(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the template from which the file was created.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a reference to a resource from which the file content is derived.'''
        raise NotImplementedError()
    

class PersonTagCategory(TagCategory):
    '''Provides tags that mark metadata properties holding information about the people contributed to file or intellectual content creation.
    These tags can help you to find the document creator, editor or even the client for whom the work was performed.
    Despite the name of the category some metadata properties marked with the tags can contain a company name rather than a person\'s name.'''
    
    @property
    def creator(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the original author of a file/document.'''
        raise NotImplementedError()
    
    @property
    def contributor(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property containing the name of a person who somehow contributed to file creation.
        Please note that the tag is not applied towards metadata properties marked with more specific tags from this category.
        E.g. if a property labeled with the Creator tag.'''
        raise NotImplementedError()
    
    @property
    def editor(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a person who edited a file.
        The tag is usually used to mark a property containing information about the last editor.'''
        raise NotImplementedError()
    
    @property
    def model(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes information about a person the content of the file is about.
        For photos that is a person shown in the image.'''
        raise NotImplementedError()
    
    @property
    def client(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels information about the client for whom the file/intellectual content was created.'''
        raise NotImplementedError()
    
    @property
    def manager(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels information about a person who managed the making process of a file.'''
        raise NotImplementedError()
    
    @property
    def publisher(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag marking a person responsible for making the file available.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the original performer of a file.'''
        raise NotImplementedError()
    
    @property
    def recipient(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the original recipients of a mail.'''
        raise NotImplementedError()
    

class PropertyTag:
    '''Represents a tag used to mark metadata properties.'''
    
    def equals(self, other : groupdocs.metadata.tagging.PropertyTag) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: True if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def category(self) -> groupdocs.metadata.tagging.TagCategory:
        '''Gets the tag category.'''
        raise NotImplementedError()
    

class PropertyTypeTagCategory(TagCategory):
    '''Provides tags that bear additional information about the type of a property rather than about its purpose.
    Using these tags you can detect metadata properties that contain URL links to external resources,
    properties describing fonts, colors, geolocation and so on.'''
    
    @property
    def link(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a property being a link to an external resource.'''
        raise NotImplementedError()
    
    @property
    def hash(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property holding a hash of the file content.'''
        raise NotImplementedError()
    
    @property
    def measure(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates a property being a measured characteristic of the content.
        It can be the file size, number of pages, page size, etc.'''
        raise NotImplementedError()
    
    @property
    def digital_signature(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a digital signature.'''
        raise NotImplementedError()
    
    @property
    def identifier(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property containing an identifier of the content.'''
        raise NotImplementedError()
    
    @property
    def location(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates a property being a reference to a geographical location.
        The property can contain the name of a city, full address, GPS coordinates, etc.'''
        raise NotImplementedError()
    
    @property
    def font(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes a property describing font characteristics.'''
        raise NotImplementedError()
    
    @property
    def color(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property describing a color.'''
        raise NotImplementedError()
    
    @property
    def bitrate(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels a property describing a bitrate.'''
        raise NotImplementedError()
    

class TagCategory:
    '''Represents a set of tags having some shared characteristics.'''
    

class Tags:
    '''Contains various sets of tags with which most important metadata properties are marked.
    The tags allow you to find and update metadata properties in different packages regardless of the metadata standard and file format.'''
    
    @property
    def person(self) -> groupdocs.metadata.tagging.PersonTagCategory:
        '''Gets a set of tags that mark metadata properties holding information about the people contributed to file or intellectual content creation.
        These tags can help you to find the document creator, editor or even the client for whom the work was performed.
        Despite the name of the category some metadata properties marked with the tags can contain a company name rather than a person\'s name.'''
        raise NotImplementedError()

    @property
    def tool(self) -> groupdocs.metadata.tagging.ToolTagCategory:
        '''Gets the tags intended to mark metadata properties related to the tools (software and hardware) that were used to create a file.'''
        raise NotImplementedError()

    @property
    def time(self) -> groupdocs.metadata.tagging.TimeTagCategory:
        '''Gets a set of tags that mark metadata properties used to describe the lifecycle of a file.
        The tags deal with time points when a file or intellectual content was created, edited, printed, etc.'''
        raise NotImplementedError()

    @property
    def content(self) -> groupdocs.metadata.tagging.ContentTagCategory:
        '''Gets the tags that are attached to metadata properties describing the content of a file.
        The tags are useful to find out the content language, type (genre), subject, rating, etc.'''
        raise NotImplementedError()

    @property
    def property_type(self) -> groupdocs.metadata.tagging.PropertyTypeTagCategory:
        '''Gets a set of tags that bear additional information about the type of a property rather than about its purpose.
        Using these tags you can detect metadata properties that contain URL links to external resources,
        properties describing fonts, colors, geolocation and so on.'''
        raise NotImplementedError()

    @property
    def document(self) -> groupdocs.metadata.tagging.DocumentTagCategory:
        '''Gets a set of tags that are applied to document-specific properties only.
        The tags can be useful to determine from which part of an office document a property was extracted.'''
        raise NotImplementedError()

    @property
    def origin(self) -> groupdocs.metadata.tagging.OriginTagCategory:
        '''Gets the tags that help a user to determine the origin of a file (e.g. template or another source).'''
        raise NotImplementedError()

    @property
    def corporate(self) -> groupdocs.metadata.tagging.CorporateTagCategory:
        '''Gets a set of tags intended to mark metadata properties related to a company that participated in file creation.'''
        raise NotImplementedError()

    @property
    def legal(self) -> groupdocs.metadata.tagging.LegalTagCategory:
        '''Gets a set of tags that are attached to metadata properties holding information about the owners of the file content
        and the rules under which the content can be used.'''
        raise NotImplementedError()


class TimeTagCategory(TagCategory):
    '''Provides tags that mark metadata properties used to describe the lifecycle of a file.
    The tags deal with time points when a file or intellectual content was created, edited, printed, etc.'''
    
    @property
    def intellectual_content_created(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the date the intellectual content of a file was created.'''
        raise NotImplementedError()
    
    @property
    def created(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates the date a file was created.'''
        raise NotImplementedError()
    
    @property
    def modified(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates the date a file was edited.'''
        raise NotImplementedError()
    
    @property
    def published(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that indicates the date a file became available.'''
        raise NotImplementedError()
    
    @property
    def printed(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the date a file was printed.'''
        raise NotImplementedError()
    
    @property
    def expired(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels the latest date the owner intends the file data to be used.'''
        raise NotImplementedError()
    
    @property
    def total_editing_time(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the total editing time of a file.'''
        raise NotImplementedError()
    
    @property
    def duration(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the duration of a media file.'''
        raise NotImplementedError()
    
    @property
    def zone_city(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes the time zone.'''
        raise NotImplementedError()
    

class ToolTagCategory(TagCategory):
    '''Provides tags intended to mark metadata properties related to the tools (software and hardware) that were used to create a file.'''
    
    @property
    def software(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels any kind of software used to create a file.'''
        raise NotImplementedError()
    
    @property
    def hardware(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that denotes any kind of hardware used to create a file.'''
        raise NotImplementedError()
    
    @property
    def software_version(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels properties containing the version of the software used to create a file.'''
        raise NotImplementedError()
    
    @property
    def hardware_version(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that labels properties containing the version of the hardware used to create a file.'''
        raise NotImplementedError()
    
    @property
    def software_manufacturer(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that marks a software manufacturer.'''
        raise NotImplementedError()
    
    @property
    def hardware_manufacturer(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that marks a hardware manufacturer.'''
        raise NotImplementedError()
    
    @property
    def model_id(self) -> groupdocs.metadata.tagging.PropertyTag:
        '''Gets the tag that marks a model id.'''
        raise NotImplementedError()
    

