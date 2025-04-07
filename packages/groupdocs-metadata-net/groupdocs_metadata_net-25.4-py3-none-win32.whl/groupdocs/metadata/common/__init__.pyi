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

class CustomPackage(MetadataPackage):
    '''Provides a container for metadata properties.'''
    
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
    

class DocumentInfo(IDocumentInfo):
    '''Provides common information about a loaded document.'''
    
    @property
    def file_type(self) -> groupdocs.metadata.common.FileTypePackage:
        '''Gets the file type of the loaded document.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size of the loaded document in bytes.'''
        raise NotImplementedError()
    
    @property
    def page_count(self) -> int:
        '''Gets the number of pages (slides, worksheets, etc) in the loaded document.'''
        raise NotImplementedError()
    
    @property
    def pages(self) -> Sequence[groupdocs.metadata.common.PageInfo]:
        '''Gets a collection of objects representing common information about the document pages (slides, worksheets, etc).'''
        raise NotImplementedError()
    
    @property
    def is_encrypted(self) -> bool:
        '''Gets a value indicating whether the document is encrypted and requires a password to open.'''
        raise NotImplementedError()
    

class FileType:
    '''Represents the file type.'''
    
    @staticmethod
    def get_supported_file_types() -> Iterable[groupdocs.metadata.common.FileType]:
        '''Retrieves supported file types.
        
        :returns: A collection of supported file types.'''
        raise NotImplementedError()
    
    @staticmethod
    def from_extension(file_extension : str) -> groupdocs.metadata.common.FileType:
        '''Gets FileType for provided fileExtension
        
        :param file_extension: File extension
        :returns: File type'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the file type description.'''
        raise NotImplementedError()
    
    @property
    def extension(self) -> str:
        '''Gets the file extension.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> groupdocs.metadata.common.FileFormat:
        '''Gets the file format.'''
        raise NotImplementedError()
    
    @property
    def UNKNOWN(self) -> groupdocs.metadata.common.FileType:
        '''Represents unknown file type.'''
        raise NotImplementedError()

    @property
    def TORRENT(self) -> groupdocs.metadata.common.FileType:
        '''Represents TORRENT file type.'''
        raise NotImplementedError()

    @property
    def PDF(self) -> groupdocs.metadata.common.FileType:
        '''Portable Document Format (PDF) is a type of document created by Adobe back in 1990s. The purpose of this
        file format was to introduce a standard for representation of documents and other reference material in
        a format that is independent of application software, hardware as well as Operating System. Learn more
        about this file format `here <https://docs.fileformat.com/pdf/>`.'''
        raise NotImplementedError()

    @property
    def PPT(self) -> groupdocs.metadata.common.FileType:
        '''A file with PPT extension represents PowerPoint file that consists of a collection of slides for
        displaying as SlideShow. It specifies the Binary File Format used by Microsoft PowerPoint 97-2003.
        Learn more about this file format `here <https://wiki.fileformat.com/presentation/ppt/>`.'''
        raise NotImplementedError()

    @property
    def PPTX(self) -> groupdocs.metadata.common.FileType:
        '''Files with PPTX extension are presentation files created with popular Microsoft PowerPoint application.
        Unlike the previous version of presentation file format PPT which was binary, the PPTX format is based
        on the Microsoft PowerPoint open XML presentation file format. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/pptx/>`.'''
        raise NotImplementedError()

    @property
    def POTX(self) -> groupdocs.metadata.common.FileType:
        '''Files with .POTX extension represent Microsoft PowerPoint template presentations that are created with
        Microsoft PowerPoint 2007 and above. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/potx/>`.'''
        raise NotImplementedError()

    @property
    def PPTM(self) -> groupdocs.metadata.common.FileType:
        '''Files with PPTM extension are Macro-enabled Presentation files that are created with
        Microsoft PowerPoint 2007 or higher versions. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/pptm/>`.'''
        raise NotImplementedError()

    @property
    def POTM(self) -> groupdocs.metadata.common.FileType:
        '''Files with POTM extension are Microsoft PowerPoint template files with support for Macros. POTM files
        are created with PowerPoint 2007 or above and contains default settings that can be used to create
        further presentation files. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/potm/>`.'''
        raise NotImplementedError()

    @property
    def PPS(self) -> groupdocs.metadata.common.FileType:
        '''PPS, PowerPoint Slide Show, files are created using Microsoft PowerPoint for Slide Show purpose.
        PPS file reading and creation is supported by Microsoft PowerPoint 97-2003. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/pps/>`.'''
        raise NotImplementedError()

    @property
    def PPSX(self) -> groupdocs.metadata.common.FileType:
        '''PPSX, Power Point Slide Show, file are created using Microsoft PowerPoint 2007 and above for
        Slide Show purpose.  Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/ppsx/>`.'''
        raise NotImplementedError()

    @property
    def PPSM(self) -> groupdocs.metadata.common.FileType:
        '''Files with PPSM extension represent Macro-enabled Slide Show file format created with Microsoft
        PowerPoint 2007 or higher. Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/ppsm/>`.'''
        raise NotImplementedError()

    @property
    def POT(self) -> groupdocs.metadata.common.FileType:
        '''Files with .POT extension represent Microsoft PowerPoint template files in binary format created by PowerPoint 97-2003 versions.
        Learn more about this file format
        `here <https://wiki.fileformat.com/presentation/pot/>`.'''
        raise NotImplementedError()

    @property
    def XLS(self) -> groupdocs.metadata.common.FileType:
        '''Files with XLS extension represent Excel Binary File Format. Such files can be created by Microsoft Excel
        as well as other similar spreadsheet programs such as OpenOffice Calc or Apple Numbers. Learn more about
        this file format `here <https://wiki.fileformat.com/specification/spreadsheet/xls/>`.'''
        raise NotImplementedError()

    @property
    def XLSX(self) -> groupdocs.metadata.common.FileType:
        '''XLSX is well-known format for Microsoft Excel documents that was introduced by Microsoft with the release
        of Microsoft Office 2007. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xlsx/>`.'''
        raise NotImplementedError()

    @property
    def XLSM(self) -> groupdocs.metadata.common.FileType:
        '''Files with XLSM extension is a type of Spreasheet files that support Macros. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xlsm/>`.'''
        raise NotImplementedError()

    @property
    def XLT(self) -> groupdocs.metadata.common.FileType:
        '''Files with .XLT extension are template files created with Microsoft Excel which is a spreadsheet
        application which comes as part of Microsoft Office suite. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xlt/>`.'''
        raise NotImplementedError()

    @property
    def ODT(self) -> groupdocs.metadata.common.FileType:
        '''ODT files are type of documents created with word processing applications that are based on OpenDocument
        Text File format. These are created with word processor applications such as free OpenOffice Writer and
        can hold content such as text, images, objects and styles. Learn more about this file format
        `here <https://wiki.fileformat.com/word-processing/odt/>`.'''
        raise NotImplementedError()

    @property
    def DOT(self) -> groupdocs.metadata.common.FileType:
        '''Files with .DOT extension are template files created by Microsoft Word to have pre-formatted settings
        for generation of further DOC or DOCX files. Learn more about this file format
        `here <https://wiki.fileformat.com/word-processing/dot/>`.'''
        raise NotImplementedError()

    @property
    def DOC(self) -> groupdocs.metadata.common.FileType:
        '''Files with .doc extension represent documents generated by Microsoft Word or other word processing
        documents in binary file format. Learn more about this file format
        `here <https://wiki.fileformat.com/word-processing/doc/>`.'''
        raise NotImplementedError()

    @property
    def DOCX(self) -> groupdocs.metadata.common.FileType:
        '''DOCX is a well-known format for Microsoft Word documents. Introduced from 2007 with the release
        of Microsoft Office 2007, the structure of this new Document format was changed from plain binary
        to a combination of XML and binary files. Learn more about this file format
        `here <https://wiki.fileformat.com/word-processing/docx/>`.'''
        raise NotImplementedError()

    @property
    def XLTX(self) -> groupdocs.metadata.common.FileType:
        '''Files with XLTX extension represent Microsoft Excel Template files that are based on the Office OpenXML
        file format specifications. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xltx/>`.'''
        raise NotImplementedError()

    @property
    def DOTX(self) -> groupdocs.metadata.common.FileType:
        '''Files with DOTX extension are template files created by Microsoft Word to have pre-formatted settings
        for generation of further DOCX files. Learn more about this file format
        `here <https://wiki.fileformat.com/word-processing/dotx/>`.'''
        raise NotImplementedError()

    @property
    def ODS(self) -> groupdocs.metadata.common.FileType:
        '''Files with ODS extension stand for OpenDocument Spreadsheet Document format that are editable by user.
        Learn more about this file format
        `here <https://wiki.fileformat.com/spreadsheet/ods/>`.'''
        raise NotImplementedError()

    @property
    def XLTM(self) -> groupdocs.metadata.common.FileType:
        '''The XLTM file extension represents files that are generated by Microsoft Excel as Macro-enabled
        template files. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xltm/>`.'''
        raise NotImplementedError()

    @property
    def XLSB(self) -> groupdocs.metadata.common.FileType:
        '''XLSB file format specifies the Excel Binary File Format, which is a collection of records and
        structures that specify Excel workbook content. Learn more about this file format
        `here <https://wiki.fileformat.com/specification/spreadsheet/xlsb/>`.'''
        raise NotImplementedError()

    @property
    def DOTM(self) -> groupdocs.metadata.common.FileType:
        '''A file with DOTM extension represents template file created with Microsoft Word 2007 or higher.
        Learn more about this file format `here <https://wiki.fileformat.com/word-processing/dotm/>`.'''
        raise NotImplementedError()

    @property
    def DOCM(self) -> groupdocs.metadata.common.FileType:
        '''DOCM files are Microsoft Word 2007 or higher generated documents with the ability to run macros.
        Learn more about this file format `here <https://wiki.fileformat.com/word-processing/docm/>`.'''
        raise NotImplementedError()

    @property
    def EPUB(self) -> groupdocs.metadata.common.FileType:
        '''Files with .EPUB extension are an e-book file format that provide a standard digital publication format for publishers and consumers.
        Learn more about this file format
        `here <https://wiki.fileformat.com/ebook/epub/>`.'''
        raise NotImplementedError()

    @property
    def TTF(self) -> groupdocs.metadata.common.FileType:
        '''TTF represents font files based on the TrueType specifications font technology.
        TrueType fonts provide highest quality display on computer screens and printers without any dependency on resolution.
        Learn more about this file format
        `here <https://docs.fileformat.com/font/ttf/>`.'''
        raise NotImplementedError()

    @property
    def TTC(self) -> groupdocs.metadata.common.FileType:
        '''TTC (TrueType Collection) is a TrueType font collection format.
        A TTC file can combine the multiple font files into it.
        Learn more about this file format
        `here <https://docs.fileformat.com/font/ttc/>`.'''
        raise NotImplementedError()

    @property
    def OTF(self) -> groupdocs.metadata.common.FileType:
        '''A file with .otf extension refers to OpenType font format.
        OTF font format is more scalable and extends the existing features of TTF formats for digital typography.
        Learn more about this file format
        `here <https://docs.fileformat.com/font/otf/>`.'''
        raise NotImplementedError()

    @property
    def OTC(self) -> groupdocs.metadata.common.FileType:
        '''OTC (OpenType Collection) is a OpenType font collection format.
        An OTC file can combine the multiple font files into it.'''
        raise NotImplementedError()

    @property
    def ONE(self) -> groupdocs.metadata.common.FileType:
        '''File represented by .ONE extension are created by Microsoft OneNote application.
        Learn more about this file format
        `here <https://wiki.fileformat.com/note-taking/one/>`.'''
        raise NotImplementedError()

    @property
    def ZIP(self) -> groupdocs.metadata.common.FileType:
        '''ZIP file extension represents archives that can hold one or more files or directories.
        Learn more about this file format
        `here <https://wiki.fileformat.com/compression/zip/>`.'''
        raise NotImplementedError()

    @property
    def ZIPX(self) -> groupdocs.metadata.common.FileType:
        '''ZIPX is a Zip file in which WinZip has used one or more of its available advanced compression methods.'''
        raise NotImplementedError()

    @property
    def JAR(self) -> groupdocs.metadata.common.FileType:
        '''JAR is a Java Archive file that contains many different application related files as a single file.
        This file format was created to reduce the speed of loading a downloaded Java Applet in browser via HTTP transaction,
        Learn more about this file format
        `here <https://docs.fileformat.com/programming/jar/>`.'''
        raise NotImplementedError()

    @property
    def VCF(self) -> groupdocs.metadata.common.FileType:
        '''VCF (Virtual Card Format) or vCard is a digital file format for storing contact information.
        The format is widely used for data interchange among popular information exchange applications.
        Learn more about this file format
        `here <https://docs.fileformat.com/email/vcf/>`.'''
        raise NotImplementedError()

    @property
    def VCR(self) -> groupdocs.metadata.common.FileType:
        '''VCR (Virtual Card Format) or vCard is a digital file format for storing contact information.
        The format is widely used for data interchange among popular information exchange applications.'''
        raise NotImplementedError()

    @property
    def EML(self) -> groupdocs.metadata.common.FileType:
        '''EML file format represents email messages saved using Outlook and other relevant applications.
        Learn more about this file format `here <https://wiki.fileformat.com/email/eml/>`.'''
        raise NotImplementedError()

    @property
    def MSG(self) -> groupdocs.metadata.common.FileType:
        '''MSG is a file format used by Microsoft Outlook and Exchange to store email messages, contact,
        appointment, or other tasks. Learn more about this file format
        `here <https://wiki.fileformat.com/email/msg/>`.'''
        raise NotImplementedError()

    @property
    def MP3(self) -> groupdocs.metadata.common.FileType:
        '''Files with MP3 extension are digitally encoded file formats for audio files that are formally based
        on the MPEG-1 Audio Layer III or MPEG-2 Audio Layer III.
        Learn more about this file format
        `here <https://wiki.fileformat.com/audio/mp3/>`.'''
        raise NotImplementedError()

    @property
    def WAV(self) -> groupdocs.metadata.common.FileType:
        '''WAV, known for WAVE (Waveform Audio File Format), is a subset of Microsoft\'s Resource Interchange File Format (RIFF)
        specification for storing digital audio files.
        Learn more about this file format
        `here <https://wiki.fileformat.com/audio/wav/>`.'''
        raise NotImplementedError()

    @property
    def BMP(self) -> groupdocs.metadata.common.FileType:
        '''Files having extension .BMP represent Bitmap Image files that are used to store bitmap digital images.
        These images are independent of graphics adapter and are also called device independent bitmap (DIB) file
        format. Learn more about this file format `here <https://wiki.fileformat.com/image/bmp/>`.'''
        raise NotImplementedError()

    @property
    def DJVU(self) -> groupdocs.metadata.common.FileType:
        '''DjVu is a graphics file format intended for scanned documents and books especially those which contain
        the combination of text, drawings, images and photographs.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/djvu/>`.'''
        raise NotImplementedError()

    @property
    def DJV(self) -> groupdocs.metadata.common.FileType:
        '''DjVu is a graphics file format intended for scanned documents and books especially those which contain
        the combination of text, drawings, images and photographs.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/djvu/>`.'''
        raise NotImplementedError()

    @property
    def GIF(self) -> groupdocs.metadata.common.FileType:
        '''A GIF or Graphical Interchange Format is a type of highly compressed image.
        Learn more about this file format `here <https://wiki.fileformat.com/image/gif/>`.'''
        raise NotImplementedError()

    @property
    def JPG(self) -> groupdocs.metadata.common.FileType:
        '''A JPEG is a type of image format that is saved using the method of lossy compression.
        Learn more about this file format `here <https://wiki.fileformat.com/image/jpeg/>`.'''
        raise NotImplementedError()

    @property
    def JPE(self) -> groupdocs.metadata.common.FileType:
        '''A JPEG is a type of image format that is saved using the method of lossy compression.
        Learn more about this file format `here <https://wiki.fileformat.com/image/jpeg/>`.'''
        raise NotImplementedError()

    @property
    def JPEG(self) -> groupdocs.metadata.common.FileType:
        '''A JPEG is a type of image format that is saved using the method of lossy compression.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/jpeg/>`.'''
        raise NotImplementedError()

    @property
    def JP2(self) -> groupdocs.metadata.common.FileType:
        '''JPEG 2000 (JP2) is an image coding system and state-of-the-art image compression standard.
        Designed, using wavelet technology JPEG 2000 can code lossless content in any quality at once.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/jp2/>`.'''
        raise NotImplementedError()

    @property
    def J2K(self) -> groupdocs.metadata.common.FileType:
        '''JPEG 2000 (J2K) is an image coding system and state-of-the-art image compression standard.
        Designed, using wavelet technology JPEG 2000 can code lossless content in any quality at once.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/j2k/>`.'''
        raise NotImplementedError()

    @property
    def JPF(self) -> groupdocs.metadata.common.FileType:
        '''JPEG 2000 (JPF) is an image coding system and state-of-the-art image compression standard.
        Designed, using wavelet technology JPEG 2000 can code lossless content in any quality at once.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/jpf/>`.'''
        raise NotImplementedError()

    @property
    def JPX(self) -> groupdocs.metadata.common.FileType:
        '''JPEG 2000 (JPX) is an image coding system and state-of-the-art image compression standard.
        Designed, using wavelet technology JPEG 2000 can code lossless content in any quality at once.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/jpx/>`.'''
        raise NotImplementedError()

    @property
    def JPM(self) -> groupdocs.metadata.common.FileType:
        '''JPEG 2000 (JPM) is an image coding system and state-of-the-art image compression standard.
        Designed, using wavelet technology JPEG 2000 can code lossless content in any quality at once.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/jpm/>`.'''
        raise NotImplementedError()

    @property
    def MJ2(self) -> groupdocs.metadata.common.FileType:
        '''Video format defined as Motion JPEG 2000 (Part 3); contains a motion sequence of JPEG 2000 images;
        does not involve inter-frame coding, but instead encodes each frame independently using JPEG 2000 compression.'''
        raise NotImplementedError()

    @property
    def PNG(self) -> groupdocs.metadata.common.FileType:
        '''PNG, Portable Network Graphics, refers to a type of raster image file format that use loseless compression.
        Learn more about this file format `here <https://wiki.fileformat.com/image/png/>`.'''
        raise NotImplementedError()

    @property
    def TIFF(self) -> groupdocs.metadata.common.FileType:
        '''TIFF or TIF, Tagged Image File Format, represents raster images that are meant for usage on a variety
        of devices that comply with this file format standard. Learn more about this file format
        `here <https://wiki.fileformat.com/image/tiff/>`.'''
        raise NotImplementedError()

    @property
    def TIF(self) -> groupdocs.metadata.common.FileType:
        '''TIFF or TIF, Tagged Image File Format, represents raster images that are meant for usage on a variety
        of devices that comply with this file format standard. Learn more about this file format
        `here <https://wiki.fileformat.com/image/tiff/>`.'''
        raise NotImplementedError()

    @property
    def WEBP(self) -> groupdocs.metadata.common.FileType:
        '''WebP, introduced by Google, is a modern raster web image file format that is based on lossless and
        lossy compression. It provides same image quality while considerably reducing the image size.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/webp/>`.'''
        raise NotImplementedError()

    @property
    def EMF(self) -> groupdocs.metadata.common.FileType:
        '''Enhanced metafile format (EMF) stores graphical images device-independently.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/emf/>`.'''
        raise NotImplementedError()

    @property
    def WMF(self) -> groupdocs.metadata.common.FileType:
        '''Files with WMF extension represent Microsoft Windows Metafile (WMF) for storing vector as well as bitmap-format images data.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/wmf/>`.'''
        raise NotImplementedError()

    @property
    def PSD(self) -> groupdocs.metadata.common.FileType:
        '''PSD, Photoshop Document, represents Adobe Photoshop\'s native file format used for graphics designing and development.
        Learn more about this file format
        `here <https://wiki.fileformat.com/image/psd/>`.'''
        raise NotImplementedError()

    @property
    def MPP(self) -> groupdocs.metadata.common.FileType:
        '''MPP is proprietary file format developed by Microsoft as file format for Microsoft Project (MSP) which is a project management application software.
        Learn more about this file format
        `here <https://wiki.fileformat.com/project-management/mpp/>`.'''
        raise NotImplementedError()

    @property
    def MPT(self) -> groupdocs.metadata.common.FileType:
        '''MPT is proprietary file format developed by Microsoft as file format for Microsoft Project (MSP) which is a project management application software.
        Learn more about this file format
        `here <https://wiki.fileformat.com/project-management/mpt/>`.'''
        raise NotImplementedError()

    @property
    def VSD(self) -> groupdocs.metadata.common.FileType:
        '''VSD files are drawings created with Microsoft Visio application to represent variety of graphical
        objects and the interconnection between these. Learn more about this file format
        `here <https://wiki.fileformat.com/visio/vsd/>`.'''
        raise NotImplementedError()

    @property
    def VDX(self) -> groupdocs.metadata.common.FileType:
        '''Any drawing or chart created in Microsoft Visio, but saved in XML format have .VDX extension.
        Learn more about this file format `here <https://wiki.fileformat.com/visio/vdx/>`.'''
        raise NotImplementedError()

    @property
    def VSDX(self) -> groupdocs.metadata.common.FileType:
        '''Files with .VSDX extension represent Microsoft Visio file format introduced from Microsoft
        Office 2013 onwards. Learn more about this file format
        `here <https://wiki.fileformat.com/visio/vsdx/>`.'''
        raise NotImplementedError()

    @property
    def VSS(self) -> groupdocs.metadata.common.FileType:
        '''VSS are stencil files created with Microsoft Visio 2007 and earlier. Stencil files provide drawing
        objects that can be included in a .VSD Visio drawing. Learn more about this file format
        `here <https://wiki.fileformat.com/visio/vss/>`.'''
        raise NotImplementedError()

    @property
    def VSX(self) -> groupdocs.metadata.common.FileType:
        '''Files with .VSX extension refer to stencils that consist of drawings and shapes that are used for
        creating diagrams in Microsoft Visio. Learn more about this file format
        `here <https://wiki.fileformat.com/visio/vsx/>`.'''
        raise NotImplementedError()

    @property
    def VTX(self) -> groupdocs.metadata.common.FileType:
        '''Files with .VTX extension refer to Microsoft Visio drawing template that is saved to disc in XML file format.
        Learn more about this file format
        `here <https://docs.fileformat.com/visio/vtx/>`.'''
        raise NotImplementedError()

    @property
    def DICOM(self) -> groupdocs.metadata.common.FileType:
        '''DICOM is the acronym for Digital Imaging and Communications in Medicine and pertains to the field of Medical Informatics.
        DICOM is used for the integration of medical imaging devices like printers, servers,
        scanners etc from various vendors and also contains identification data of each patient for uniqueness.
        Learn more about this file format
        `here <https://docs.fileformat.com/image/dicom/>`.'''
        raise NotImplementedError()

    @property
    def HEIF(self) -> groupdocs.metadata.common.FileType:
        '''An HEIF file is a High-Efficiency Container Image file format that is capable of storing a single image or a sequence of images in a single file.
        HEIF file format compresses the images using the High Efficiency Video Coding (HEVC) standard.
        Learn more about this file format
        `here <https://docs.fileformat.com/image/heif/>`.'''
        raise NotImplementedError()

    @property
    def HEIC(self) -> groupdocs.metadata.common.FileType:
        '''An HEIC file is a High-Efficiency Container Image file format that can store multiple images as a collection in a single file.
        HEIC, like HEIF, are compressed using the High Efficiency Video Coding (HEVC) standard and are smaller in size without compromising the quality.
        Learn more about this file format
        `here <https://docs.fileformat.com/image/heic/>`.'''
        raise NotImplementedError()

    @property
    def DWG(self) -> groupdocs.metadata.common.FileType:
        '''Files with DWG extension represent proprietary binary files used for containing 2D and 3D design data.
        Learn more about this file format
        `here <https://wiki.fileformat.com/cad/dwg/>`.'''
        raise NotImplementedError()

    @property
    def DXF(self) -> groupdocs.metadata.common.FileType:
        '''DXF, Drawing Interchange Format, or Drawing Exchange Format, is a tagged data representation of AutoCAD drawing file.
        Learn more about this file format
        `here <https://wiki.fileformat.com/cad/dxf/>`.'''
        raise NotImplementedError()

    @property
    def AVI(self) -> groupdocs.metadata.common.FileType:
        '''The AVI file format is an Audio Video multimedia container file format that was introduced by Microsoft.
        Learn more about this file format
        `here <https://wiki.fileformat.com/video/avi/>`.'''
        raise NotImplementedError()

    @property
    def MOV(self) -> groupdocs.metadata.common.FileType:
        '''MOV or QuickTime File format is multimedia container which is developed by Apple: contains one or more tracks,
        each track holds a particular type of data i.e. Video, Audio, text etc.
        Learn more about this file format
        `here <https://wiki.fileformat.com/video/mov/>`.'''
        raise NotImplementedError()

    @property
    def QT(self) -> groupdocs.metadata.common.FileType:
        '''MOV or QuickTime File format is multimedia container which is developed by Apple: contains one or more tracks,
        each track holds a particular type of data i.e. Video, Audio, text etc.
        Learn more about this file format
        `here <https://wiki.fileformat.com/video/mov/>`.'''
        raise NotImplementedError()

    @property
    def MKA(self) -> groupdocs.metadata.common.FileType:
        '''MKA (Matroska Audio) is the Matroska multimedia container format used for Audio.
        The MKA format supports several different kinds of audio compression algorithms such as MP3, AAC and Vobis.
        Learn more about this file format
        `here <https://docs.fileformat.com/audio/mka/>`.'''
        raise NotImplementedError()

    @property
    def MKV(self) -> groupdocs.metadata.common.FileType:
        '''MKV (Matroska Video) is a multimedia container similar to MOV and AVI format
        but it supports more than one audio and subtitle track in the same file.
        Learn more about this file format
        `here <https://wiki.fileformat.com/video/mkv/>`.'''
        raise NotImplementedError()

    @property
    def MK3D(self) -> groupdocs.metadata.common.FileType:
        '''MK3D is actually stereoscopic 3D video created using Matroska 3D format.
        The MKV file container uses a StereoMode field’s value to define the type of stereoscopic 3D video stuff.
        Learn more about this file format
        `here <https://docs.fileformat.com/video/mk3d/>`.'''
        raise NotImplementedError()

    @property
    def WEBM(self) -> groupdocs.metadata.common.FileType:
        '''WEBM is a video file based on the open, royalty-free WebM file format.
        It has been designed for sharing video on the web and defines the file container structure including video and audio formats.
        Learn more about this file format
        `here <https://docs.fileformat.com/video/webm/>`.'''
        raise NotImplementedError()

    @property
    def FLV(self) -> groupdocs.metadata.common.FileType:
        '''FLV (Flash Video) is a container file format
        which is used to deliver audio/video content over the internet by using the Adobe Flash Player or Adobe Air.
        Learn more about this file format
        `here <https://docs.fileformat.com/video/flv/>`.'''
        raise NotImplementedError()

    @property
    def ASF(self) -> groupdocs.metadata.common.FileType:
        '''The Advanced Systems Format (ASF) is a digital multimedia container designed primarily for storing and transmitting media streams.
        Microsoft Windows Media Video (WMV) is the compressed video format and Microsoft Windows Media Audio (WMA)
        is the compressed audio format along with additional metadata in the ASF container developed by Microsoft.
        Learn more about this file format
        `here <https://wiki.fileformat.com/video/wmv/>`.'''
        raise NotImplementedError()

    @property
    def DNG(self) -> groupdocs.metadata.common.FileType:
        '''DNG is a digital camera image format used for the storage of raw files. It has been developed by Adobe in September 2004.
        It was basically developed for digital photography. DNG is an extension of TIFF/EP standard format and uses metadata significantly.
        In order to manipulate raw data from digital cameras with the ease of flexibility and artistic control, photographers opt camera raw files.
        JPEG and TIFF formats store images that are processed by the camera, therefore, not much room for alteration is available in such formats.
        `here <https://wiki.fileformat.com/image/dng/>`.'''
        raise NotImplementedError()

    @property
    def CR2(self) -> groupdocs.metadata.common.FileType:
        '''The .CR2 file format (Canon RAW version 2) is a digital photography RAW format created by Canon.
        `here <https://wiki.fileformat.com/image/cr2/>`.'''
        raise NotImplementedError()

    @property
    def CRW(self) -> groupdocs.metadata.common.FileType:
        '''The .CRW file format is a digital photography RAW format created by Canon.
        `here <https://wiki.fileformat.com/image/crw/>`.'''
        raise NotImplementedError()

    @property
    def SEVENZIP(self) -> groupdocs.metadata.common.FileType:
        '''7z is a compressed archive file format that supports several different data compression,
        encryption and pre-processing algorithms.
        The 7z format initially appeared as implemented by the 7-Zip archiver.
        The 7-Zip program is publicly available under the terms of the GNU Lesser General Public License.
        `here <https://wiki.fileformat.com/compression/zip/>`.'''
        raise NotImplementedError()

    @property
    def RAR(self) -> groupdocs.metadata.common.FileType:
        '''RAR is a proprietary archive file format that supports data compression, error correction and file spanning.
        `here <https://wiki.fileformat.com/compression/rar/>`.'''
        raise NotImplementedError()

    @property
    def TAR(self) -> groupdocs.metadata.common.FileType:
        '''In computing, tar is a computer software utility for collecting many files into one archive file, often referred to as a tarball, for distribution or backup purposes.
        `here <https://wiki.fileformat.com/compression/tar/>`.'''
        raise NotImplementedError()

    @property
    def THREEDS(self) -> groupdocs.metadata.common.FileType:
        '''A file with .3ds extension represents 3D Sudio (DOS) mesh file format used by Autodesk 3D Studio. Autodesk 3D Studio has been in 3D file format market since 1990s and has now evolved to 3D Studio MAX for working with 3D modeling, animation and rendering.
        `here <https://wiki.fileformat.com/3d/3ds/>`.'''
        raise NotImplementedError()

    @property
    def DAE(self) -> groupdocs.metadata.common.FileType:
        '''A DAE file is a Digital Asset Exchange file format that is used for exchanging data between interactive 3D applications.
        `here <https://wiki.fileformat.com/3d/dae/>`.'''
        raise NotImplementedError()

    @property
    def FBX(self) -> groupdocs.metadata.common.FileType:
        '''FBX (Filmbox) is a proprietary file format (.fbx) developed by Kaydara and owned by Autodesk since 2006. It is used to provide interoperability between digital content creation applications. FBX is also part of Autodesk Gameware, a series of video game middleware.
        `here <https://wiki.fileformat.com/3d/fbx/>`.'''
        raise NotImplementedError()

    @property
    def STL(self) -> groupdocs.metadata.common.FileType:
        '''STL is a file format native to the stereolithography CAD software created by 3D Systems. Chuck Hull, the inventor of stereolithography and 3D Systems’ founder, reports that the file extension is an abbreviation for stereolithography.
        `here <https://wiki.fileformat.com/3d/stl/>`.'''
        raise NotImplementedError()

    @property
    def SHP(self) -> groupdocs.metadata.common.FileType:
        '''The shapefile format is a geospatial vector data format for geographic information system (GIS) software.
        `here <https://docs.fileformat.com/gis/shp/>`.'''
        raise NotImplementedError()

    @property
    def GEOJSON(self) -> groupdocs.metadata.common.FileType:
        '''GeoJSON is a JSON based format designed to represent the geographical features with their non-spatial attributes.
        `here <https://docs.fileformat.com/gis/geojson/>`.'''
        raise NotImplementedError()

    @property
    def TOPOJSON(self) -> groupdocs.metadata.common.FileType:
        '''TopoJSON is an extension of GeoJSON that encodes topology.
        `here <https://docs.fileformat.com/gis/geojson/>`.'''
        raise NotImplementedError()

    @property
    def GML(self) -> groupdocs.metadata.common.FileType:
        '''GML stands for Geography Markup Language that is based on XML specifications developed by the Open Geospatial Consortium (OGC).
        `here <https://docs.fileformat.com/gis/gml/>`.'''
        raise NotImplementedError()

    @property
    def OSM(self) -> groupdocs.metadata.common.FileType:
        '''OpenStreetMap (OSM) is a huge collection of volunteered geographic information stores in different types of files, using different encoding schemes to convert this data into bits and bytes.
        `here <https://docs.fileformat.com/gis/osm/>`.'''
        raise NotImplementedError()

    @property
    def KML(self) -> groupdocs.metadata.common.FileType:
        '''KML, Keyhole Markup Language) contains geospatial information in XML notation. Files saved as KML can be opened in Geographic Information System (GIS) applications provided they support it.
        `here <https://docs.fileformat.com/gis/kml/>`.'''
        raise NotImplementedError()

    @property
    def GPX(self) -> groupdocs.metadata.common.FileType:
        '''Files with GPX extension represent GPS Exchange format for interchange of GPS data between applications and web services on the internet. It is a light-weight XML file format that contains GPS data i.e. waypoints, routes and tracks to be imported and red by multiple programs.
        `here <https://docs.fileformat.com/gis/gpx/>`.'''
        raise NotImplementedError()

    @property
    def CBSEVEN(self) -> groupdocs.metadata.common.FileType:
        '''A CB7 file refers to Comic Book 7-Zip Archive.
        It is compressed file format commonly used for storing and distributing comic book collections digitally.
        CB7 files are created using 7-Zip compression software, which is known for its high compression ratio.
        `here <https://wiki.fileformat.com/compression/cb7/>`.'''
        raise NotImplementedError()

    @property
    def CBRAR(self) -> groupdocs.metadata.common.FileType:
        '''A Comic Book Archive(CBA) file, also known as Comic Book Archive or Comic Book Reader file,
        is a popular format used to store and distribute digital comic books.
        It typically contains collection of individual comic book pages or images bundled together in single file for easy organization and reading.
        `here <https://wiki.fileformat.com/compression/cba/>`.'''
        raise NotImplementedError()

    @property
    def CBTAR(self) -> groupdocs.metadata.common.FileType:
        '''A Comic Book Archive(CBA) file, also known as Comic Book Archive or Comic Book Reader file,
        is a popular format used to store and distribute digital comic books.
        It typically contains collection of individual comic book pages or images bundled together in single file for easy organization and reading.
        `here <https://wiki.fileformat.com/compression/cba/>`.'''
        raise NotImplementedError()

    @property
    def CBZIP(self) -> groupdocs.metadata.common.FileType:
        '''A Comic Book Archive(CBA) file, also known as Comic Book Archive or Comic Book Reader file,
        is a popular format used to store and distribute digital comic books.
        It typically contains collection of individual comic book pages or images bundled together in single file for easy organization and reading.
        `here <https://wiki.fileformat.com/compression/cba/>`.'''
        raise NotImplementedError()

    @property
    def FB2(self) -> groupdocs.metadata.common.FileType:
        '''Files with .fb2 extension are FictionBook 2.0 eBook files that contains the structure of the eBook.
        It is based on XML format and contains special tags for describing each element of the book.
        It was developed primarily for fictional writings and literature, but is not limited to these only.
        The format accommodates all the metadata as well as content in itself and allows flexibility for a number of operations such as automatic processing, indexing, and conversion to other formats.
        In short, it focuses on describing the structure of the file instead of specifying its appearance.
        Several applications as well as APIs are available to convert FB2 to several other formats on Windows, MacOS, and Linux.
        Learn more about this file format `here <https://docs.fileformat.com/ebook/fb2/>`.'''
        raise NotImplementedError()

    @property
    def MOBI(self) -> groupdocs.metadata.common.FileType:
        '''The MOBI file format is one of the most widely used ebook file formats. The format is an enhancement to the old OEB (Open Ebook Format) format and was used as the proprietary format for Mobipocket Reader. Like EPUB, it is supported by almost all modern e-readers specifically by mobile devices with low bandwidth. The format can be converted to several other formats such as PDF, EPUB, and several other formats using publicly available software applications such as the Kindle app. There are several companies that offer free MOBI books such as Project Gutenberg, Feedbooks, and Open Library.
        Learn more about this file format `here <https://docs.fileformat.com/ebook/mobi/>`.'''
        raise NotImplementedError()

    @property
    def OGG(self) -> groupdocs.metadata.common.FileType:
        '''OGG is an Ogg Vorbis Compressed Audio File that is saved with the .ogg extension. OGG files are used for storing audio data and can include artist and track information and metadata as well. OGG is a free and open container format that is maintained by Xiph.Org Foundation.
        Learn more about this file format `here <https://docs.fileformat.com/audio/ogg/>`.'''
        raise NotImplementedError()


class FileTypePackage(CustomPackage):
    '''Represents a metadata package containing file format information.'''
    
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
    def file_format(self) -> groupdocs.metadata.common.FileFormat:
        '''Gets the file format.'''
        raise NotImplementedError()
    
    @property
    def mime_type(self) -> str:
        '''Gets the MIME type.'''
        raise NotImplementedError()
    
    @property
    def extension(self) -> str:
        '''Gets the file extension.'''
        raise NotImplementedError()
    

class IDocumentInfo:
    '''Provides common information about a loaded document.'''
    
    @property
    def file_type(self) -> groupdocs.metadata.common.FileTypePackage:
        '''Gets the file type of the loaded document.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size of the loaded document in bytes.'''
        raise NotImplementedError()
    
    @property
    def page_count(self) -> int:
        '''Gets the number of pages (slides, worksheets, etc) in the loaded document.'''
        raise NotImplementedError()
    
    @property
    def pages(self) -> Sequence[groupdocs.metadata.common.PageInfo]:
        '''Gets a collection of objects representing common information about the document pages (slides, worksheets, etc).'''
        raise NotImplementedError()
    
    @property
    def is_encrypted(self) -> bool:
        '''Gets a value indicating whether the document is encrypted and requires a password to open.'''
        raise NotImplementedError()
    

class IEnumValueInterpreter:
    '''Represents an interpreter intended to convert various numeric values to descriptive string values.'''
    
    @property
    def output_value_range(self) -> Sequence[str]:
        '''Gets the range of all possible output (interpreted) values.'''
        raise NotImplementedError()
    

class MetadataPackage:
    '''Represents base abstraction for a metadata package.'''
    
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
    

class MetadataProperty:
    '''Represents a metadata property.'''
    
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
    

class MetadataPropertyEqualityComparer:
    '''Defines methods to support the comparison of metadata properties for equality.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def equals(self, x : groupdocs.metadata.common.MetadataProperty, y : groupdocs.metadata.common.MetadataProperty) -> bool:
        '''Determines whether the specified objects are equal.
        
        :param x: The first object of type :py:class:`groupdocs.metadata.common.MetadataProperty` to compare.
        :param y: The second object of type :py:class:`groupdocs.metadata.common.MetadataProperty` to compare.
        :returns: if the specified objects are equal; otherwise, .'''
        raise NotImplementedError()
    
    def get_hash_code(self, obj : groupdocs.metadata.common.MetadataProperty) -> int:
        '''Returns a hash code for the specified object.
        
        :param obj: The :py:class:`groupdocs.metadata.common.MetadataProperty` for which a hash code is to be returned.
        :returns: A hash code for the specified object.'''
        raise NotImplementedError()
    

class PageInfo:
    '''Provides common information about a document page (slide, worksheet, etc).'''
    
    @property
    def width(self) -> int:
        '''Gets the width of the page in document default units.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height of the page in document default units.'''
        raise NotImplementedError()
    
    @property
    def page_number(self) -> int:
        '''Gets the number of the page.'''
        raise NotImplementedError()
    

class PropertyDescriptor:
    '''Represents a descriptor of a property that can be accessed through the GroupDocs.Metadata search engine.'''
    
    @property
    def name(self) -> str:
        '''Gets the property name.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the property type.'''
        raise NotImplementedError()
    
    @property
    def access_level(self) -> groupdocs.metadata.common.PropertyAccessLevels:
        '''Gets the property access level.'''
        raise NotImplementedError()
    
    @property
    def tags(self) -> Sequence[groupdocs.metadata.tagging.PropertyTag]:
        '''Gets a collection of tags associated with the property.'''
        raise NotImplementedError()
    
    @property
    def interpreter(self) -> groupdocs.metadata.common.ValueInterpreter:
        '''Gets the property value interpreter.'''
        raise NotImplementedError()
    

class PropertyValue:
    '''Represents a property value.'''
    
    @overload
    def __init__(self, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with an integer value.
        
        :param value: An :py:class:`int` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : int) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a long value.
        
        :param value: A :py:class:`int` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : bool) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a boolean value.
        
        :param value: A :py:class:`bool` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : float) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a double value.
        
        :param value: A :py:class:`float` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a string value.
        
        :param value: A :py:class:`str` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : datetime) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a :py:class:`datetime` value.
        
        :param value: A :py:class:`datetime` value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, value : TimeSpan) -> None:
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[str]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a string array.
        
        :param values: A string array.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with a byte array.
        
        :param values: A byte array.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[float]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with an array of double values.
        
        :param values: An array of double values.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with an array of integer values.
        
        :param values: An array of integer values.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with an array of long values.
        
        :param values: An array of long values.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, values : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`groupdocs.metadata.common.PropertyValue` class with an array of ushort values.
        
        :param values: An array of ushort values.'''
        raise NotImplementedError()
    
    def accept_value(self, value_acceptor : groupdocs.metadata.common.ValueAcceptor) -> None:
        '''Extracts the property value using a custom :py:class:`groupdocs.metadata.common.ValueAcceptor`.
        
        :param value_acceptor: An acceptor that extracts the value.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the :py:class:`groupdocs.metadata.common.MetadataPropertyType`.'''
        raise NotImplementedError()
    
    @property
    def raw_value(self) -> Any:
        '''Gets the raw value.'''
        raise NotImplementedError()
    

class PropertyValueEqualityComparer:
    '''Defines methods to support the comparison of property values for equality.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def equals(self, x : groupdocs.metadata.common.PropertyValue, y : groupdocs.metadata.common.PropertyValue) -> bool:
        '''Determines whether the specified objects are equal.
        
        :param x: The first object of type :py:class:`groupdocs.metadata.common.PropertyValue` to compare.
        :param y: The second object of type :py:class:`groupdocs.metadata.common.PropertyValue` to compare.
        :returns: if the specified objects are equal; otherwise, .'''
        raise NotImplementedError()
    
    def get_hash_code(self, obj : groupdocs.metadata.common.PropertyValue) -> int:
        '''Returns a hash code for the specified object.
        
        :param obj: The :py:class:`groupdocs.metadata.common.PropertyValue` for which a hash code is to be returned.
        :returns: A hash code for the specified object.'''
        raise NotImplementedError()
    

class Rectangle:
    '''A set of four integers that represent the location and size of a rectangle.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def empty(self) -> groupdocs.metadata.common.Rectangle:
        '''Gets the empty rectangle.'''
        raise NotImplementedError()

    @property
    def x(self) -> int:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> int:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @property
    def left(self) -> int:
        '''Gets the x-coordinate of the left edge of the rectangle.'''
        raise NotImplementedError()
    
    @property
    def top(self) -> int:
        '''Gets the y-coordinate that is the sum of the Y and Height property values of the rectangle.'''
        raise NotImplementedError()
    
    @property
    def right(self) -> int:
        '''Gets the x-coordinate that is the sum of X and Width property values of the rectangle.'''
        raise NotImplementedError()
    
    @property
    def bottom(self) -> int:
        '''Gets the y-coordinate that is the sum of the Y and Height property values of the rectangle.'''
        raise NotImplementedError()
    
    @property
    def is_empty(self) -> bool:
        '''Gets a value indicating whether this instance is empty.'''
        raise NotImplementedError()
    

class RootMetadataPackage(MetadataPackage):
    '''Represents an entry point to all metadata packages presented in a particular file.'''
    
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
    

class ValueAcceptor:
    '''Provides a base abstract class that allows extracting all supported types of values from a :py:class:`groupdocs.metadata.common.PropertyValue` instance.'''
    

class ValueInterpreter:
    '''Defines operations required to interpret metadata property values.'''
    
    def to_interpreted_value(self, original_value : groupdocs.metadata.common.PropertyValue) -> groupdocs.metadata.common.PropertyValue:
        '''Interprets the provided property value.
        
        :param original_value: The value to interpret.
        :returns: The interpreted value.'''
        raise NotImplementedError()
    
    def to_source_value(self, interpreted_value : groupdocs.metadata.common.PropertyValue) -> groupdocs.metadata.common.PropertyValue:
        '''Converts an interpreted value back to its original form.
        
        :param interpreted_value: The interpreted value to convert.
        :returns: The original value.'''
        raise NotImplementedError()
    
    @property
    def interpreted_value_type(self) -> groupdocs.metadata.common.MetadataPropertyType:
        '''Gets the type of the interpreted value.'''
        raise NotImplementedError()
    

class ByteOrder:
    '''Defines various byte orders.'''
    
    UNKNOWN : ByteOrder
    '''The byte order is unknown.'''
    BIG_ENDIAN : ByteOrder
    '''Big endian.'''
    LITTLE_ENDIAN : ByteOrder
    '''Little endian.'''

class FileFormat:
    '''Represents the recognized format of a loaded file.'''
    
    UNKNOWN : FileFormat
    '''The file type is not recognized.'''
    PRESENTATION : FileFormat
    '''A presentation file.
    You must be familiar with PPTX and PPT extension files while working with Microsoft PowerPoint.
    These are Presentation file formats that store collection of records to accommodate presentation data such as slides, shapes,
    text, animations, video, audio and embedded objects.
    Learn more about this file format `here <https://wiki.fileformat.com/presentation/>`.'''
    SPREADSHEET : FileFormat
    '''A spreadsheet file.
    A spreadsheet file contains data in the form of rows and columns.
    You can open, view and edit such files using spreadsheet software applications such as Microsoft Excel that is now available for both Windows and MacOS operating system.
    Similarly, Google sheets is a free online spreadsheet creating and editing tool that works from any web browser.
    Learn more about this file format `here <https://wiki.fileformat.com/spreadsheet/>`.'''
    WORD_PROCESSING : FileFormat
    '''A word processing file.
    A word processing file contains user information in plain text or rich text format. A plain text file format
    contains unformatted text and no font or page settings etc. can be applied.
    In contrast, a rich text file format allows formatting options such as setting fonts type, styles (bold, italic, underline, etc.),
    page margins, headings, bullets and numbers, and several other formatting features.
    Learn more about this file format `here <https://wiki.fileformat.com/word-processing/>`.'''
    DIAGRAM : FileFormat
    '''A diagram file.'''
    NOTE : FileFormat
    '''An electronic note file.
    Note-taking programs such as Microsoft OneNote lets you create, open and edit notes files that contain sections and pages for storing notes.
    A note document can be as simple as a text document as well as more detailed consisting of digital images, audio/video clips, and hand sketch drawings.
    Learn more about this file format `here <https://wiki.fileformat.com/note-taking/>`.'''
    PROJECT_MANAGEMENT : FileFormat
    '''A project management format.
    Have you ever come across and wondered what is an MPP file or how to open it?
    MPP and other similar files are Project file formats that are created by Project Management software such as Microsoft Project.
    A project file is a collection of tasks, resources, and their scheduling to get a measurable output in the form or a product or a service.
    Learn more about this file format `here <https://wiki.fileformat.com/project-management/>`.'''
    PDF : FileFormat
    '''A PDF file.
    Portable Document Format (PDF) is a type of document created by Adobe back in 1990s. The purpose of this
    file format was to introduce a standard for representation of documents and other reference material in
    a format that is independent of application software, hardware as well as Operating System. Learn more
    about this file format `here <https://wiki.fileformat.com/view/pdf/>`.'''
    TIFF : FileFormat
    '''A TIFF image.
    TIFF or TIF, Tagged Image File Format, represents raster images that are meant for usage on a variety
    of devices that comply with this file format standard. Learn more about this file format
    `here <https://wiki.fileformat.com/image/tiff/>`.'''
    JPEG : FileFormat
    '''A JPEG image.
    JPEG is a type of image format that is saved using the method of lossy compression.
    Learn more about this file format `here <https://wiki.fileformat.com/image/jpeg/>`.'''
    PSD : FileFormat
    '''A PSD image.
    PSD, Photoshop Document, represents Adobe Photoshop\'s native file format used for graphics designing and development.
    PSD files may include image layers, adjustment layers, layer masks, annotations, file information, keywords and other Photoshop-specific elements.
    Learn more about this file format `here <https://wiki.fileformat.com/image/psd/>`.'''
    JPEG2000 : FileFormat
    '''A Jpeg2000 image.
    JPEG 2000 (JPX) is an image coding system and state-of-the-art image compression standard. Designed,
    using wavelet technology JPEG 2000 can code lossless content in any quality at once. Learn more about
    this file format `here <https://wiki.fileformat.com/image/jp2/>`.'''
    GIF : FileFormat
    '''A GIF image.
    A GIF or Graphical Interchange Format is a type of highly compressed image.
    Learn more about this file format `here <https://wiki.fileformat.com/image/gif/>`.'''
    PNG : FileFormat
    '''A PNG image.
    PNG, Portable Network Graphics, refers to a type of raster image file format that use lossless compression.
    Learn more about this file format `here <https://wiki.fileformat.com/image/png/>`.'''
    BMP : FileFormat
    '''A BMP image.
    Files having extension .BMP represent Bitmap Image files that are used to store bitmap digital images.
    These images are independent of graphics adapter and are also called device independent bitmap (DIB) file
    format. Learn more about this file format `here <https://wiki.fileformat.com/image/bmp/>`.'''
    DICOM : FileFormat
    '''A DICOM image.
    DICOM is the acronym for Digital Imaging and Communications in Medicine and pertains to the field of Medical Informatics.
    DICOM is the combination of file format definition and a network communications protocol.
    Learn more about this file format ` here  <https://wiki.fileformat.com/image/dicom/>`.'''
    WEB_P : FileFormat
    '''A WEBP image.
    WebP, introduced by Google, is a modern raster web image file format that is based on lossless and
    lossy compression. It provides same image quality while considerably reducing the image size.
    Learn more about this file format `here <https://wiki.fileformat.com/image/webp/>`.'''
    EMF : FileFormat
    '''An EMF image.
    Enhanced metafile format (EMF) stores graphical images device-independently.
    Metafiles of EMF comprises of variable-length records in chronological order that can render the stored image after parsing on any output device.
    Learn more about this file format `here <https://wiki.fileformat.com/image/emf/>`.'''
    WMF : FileFormat
    '''A WMF image.
    Files with WMF extension represent Microsoft Windows Metafile (WMF) for storing vector as well as bitmap-format images data.
    To be more accurate, WMF belongs to the vector file format category of Graphics file formats that is device independent.
    Learn more about this file format `here <https://wiki.fileformat.com/image/wmf/>`.'''
    DJ_VU : FileFormat
    '''A DjVu file.
    DjVu is a graphics file format intended for scanned documents and books especially those which contain the combination of text,
    drawings, images and photographs. It was developed by AT&T Labs.
    Learn more about this file format `here <https://wiki.fileformat.com/image/djvu/>`.'''
    WAV : FileFormat
    '''A WAV audio file.
    WAV, known for WAVE (Waveform Audio File Format), is a subset of Microsoft\'s Resource Interchange File Format (RIFF) specification for storing digital audio files.
    The format doesn\'t apply any compression to the bitstream and stores the audio recordings with different sampling rates and bitrates.
    Learn more about this file format `here <https://wiki.fileformat.com/audio/wav/>`.'''
    MP3 : FileFormat
    '''An Mp3 audio file.
    Files with MP3 extension are digitally encoded file formats for audio files that are formally based on the MPEG-1 Audio Layer III or MPEG-2 Audio Layer III.
    It was developed by the Moving Picture Experts Group (MPEG) that uses Layer 3 audio compression.
    Learn more about this file format `here <https://wiki.fileformat.com/audio/mp3/>`.'''
    AVI : FileFormat
    '''An AVI video.
    The AVI file format is an Audio Video multimedia container file format that was introduced by Microsoft.
    It holds the audio and video data created and compressed using several codecs (Coders/Decoders) such as Xvid and DivX.
    Learn more about this file format `here <https://wiki.fileformat.com/video/avi/>`.'''
    FLV : FileFormat
    '''An FLV video.'''
    ASF : FileFormat
    '''An ASF video.
    The Advanced Systems Format (ASF) is a digital multimedia container designed primarily for storing and transmitting media streams.
    Microsoft Windows Media Video (WMV) is the compressed video format and Microsoft Windows Media Audio (WMA) is the compressed audio format
    along with additional metadata in the ASF container developed by Microsoft.
    Learn more about this file format `here <https://wiki.fileformat.com/video/wmv/>`.'''
    MOV : FileFormat
    '''A QuickTime video.
    Mov or QuickTime File format is multimedia container which is developed by Apple: contains one or more tracks,
    each track holds a particular type of data i.e. Video, Audio, text etc.
    Mov format is compatible both in Windows and Macintosh systems.
    Learn more about this file format `here <https://wiki.fileformat.com/video/mov/>`.'''
    MATROSKA : FileFormat
    '''A video encoded with the Matroska multimedia container.'''
    ZIP : FileFormat
    '''A ZIP archive.
    ZIP file extension represents archives that can hold one or more files or directories.
    The archive can have compression applied to the included files in order to reduce the ZIP file size.
    ZIP file format was made public back in February 1989 by Phil Katz for achieving archiving of files and folders.
    Learn more about this file format `here <https://wiki.fileformat.com/compression/zip/>`.'''
    SEVEN_ZIP : FileFormat
    '''7z is a compressed archive file format that supports several different data compression,
    encryption and pre-processing algorithms.
    The 7z format initially appeared as implemented by the 7-Zip archiver.
    The 7-Zip program is publicly available under the terms of the GNU Lesser General Public License.'''
    V_CARD : FileFormat
    '''A VCard file.
    VCF (Virtual Card Format) or vCard is a digital file format for storing contact information.
    The format is widely used for data interchange among popular information exchange applications.
    Learn more about this file format `here <https://wiki.fileformat.com/email/vcf/>`.'''
    EPUB : FileFormat
    '''An EPUB electronic book.
    Files with .EPUB extension are an e-book file format that provide a standard digital publication format for publishers and consumers.
    The format has been so common by now that it is supported by many e-readers and software applications.
    Learn more about this file format `here <https://wiki.fileformat.com/ebook/epub/>`.'''
    OPEN_TYPE : FileFormat
    '''An OpenType font.'''
    DXF : FileFormat
    '''A DXF (Drawing Exchange Format) drawing.
    DXF, Drawing Interchange Format, or Drawing Exchange Format, is a tagged data representation of AutoCAD drawing file.
    Each element in the file has a prefix integer number called a group code.
    Learn more about this file format `here <https://wiki.fileformat.com/cad/dxf/>`.'''
    DWG : FileFormat
    '''A DWG drawing.
    Files with DWG extension represent proprietary binary files used for containing 2D and 3D design data.
    Like DXF, which are ASCII files, DWG represent the binary file format for CAD (Computer Aided Design) drawings.
    Learn more about this file format `here <https://wiki.fileformat.com/cad/dwg/>`.'''
    EML : FileFormat
    '''An EML email message.
    EML file format represents email messages saved using Outlook and other relevant applications.
    Almost all emailing clients support this file format for its compliance with RFC-822 Internet Message Format Standard.
    Learn more about this file format `here <https://wiki.fileformat.com/email/eml/>`.'''
    MSG : FileFormat
    '''An MSG email message.
    MSG is a file format used by Microsoft Outlook and Exchange to store email messages, contact, appointment, or other tasks.
    Such messages may contain one or more email fields, with the sender, recipient, subject, date,
    and message body, or contact information, appointment particulars, and one or more task specifications.
    Learn more about this file format `here <https://wiki.fileformat.com/email/msg/>`.'''
    TORRENT : FileFormat
    '''A torrent file that contains metadata about files and folders to be distributed.'''
    HEIF : FileFormat
    '''A HEIF/HEIC image.'''
    DNG : FileFormat
    '''A dng RAW image.'''
    CR2 : FileFormat
    '''A CR2 image.'''
    RAR : FileFormat
    '''RAR is a proprietary archive file format that supports data compression, error correction and file spanning.'''
    TAR : FileFormat
    '''In computing, tar is a computer software utility for collecting many files into one archive file, often referred to as a tarball, for distribution or backup purposes.'''
    THREE_DS : FileFormat
    '''3DS is one of the file formats used by the Autodesk 3ds Max 3D modeling, animation and rendering software.'''
    DAE : FileFormat
    '''A DAE file is a Digital Asset Exchange file format that is used for exchanging data between interactive 3D applications.'''
    FBX : FileFormat
    '''FBX (Filmbox) is a proprietary file format (.fbx) developed by Kaydara and owned by Autodesk since 2006. It is used to provide interoperability between digital content creation applications. FBX is also part of Autodesk Gameware, a series of video game middleware.'''
    STL : FileFormat
    '''STL is a file format native to the stereolithography CAD software created by 3D Systems.[3][4][5] Chuck Hull, the inventor of stereolithography and 3D Systems’ founder, reports that the file extension is an abbreviation for stereolithography.'''
    GIS : FileFormat
    '''Gis file.'''
    FB2 : FileFormat
    '''Files with .fb2 extension are FictionBook 2.0 eBook files that contains the structure of the eBook.
    It is based on XML format and contains special tags for describing each element of the book.
    It was developed primarily for fictional writings and literature, but is not limited to these only.
    The format accommodates all the metadata as well as content in itself and allows flexibility for a number of operations such as automatic processing, indexing, and conversion to other formats.
    In short, it focuses on describing the structure of the file instead of specifying its appearance.
    Several applications as well as APIs are available to convert FB2 to several other formats on Windows, MacOS, and Linux.
    Learn more about this file format `here <https://docs.fileformat.com/ebook/fb2/>`.'''
    MOBI : FileFormat
    '''The MOBI file format is one of the most widely used ebook file formats. The format is an enhancement to the old OEB (Open Ebook Format) format and was used as the proprietary format for Mobipocket Reader.'''
    OGG : FileFormat
    '''OGG is an Ogg Vorbis Compressed Audio File that is saved with the .ogg extension. OGG files are used for storing audio data and can include artist and track information and metadata as well. OGG is a free and open container format that is maintained by Xiph.Org Foundation.'''

class MetadataPropertyType:
    '''Defines metadata property types.'''
    
    EMPTY : MetadataPropertyType
    '''Represents an empty (null) property.'''
    STRING : MetadataPropertyType
    '''Represents a string property.'''
    BOOLEAN : MetadataPropertyType
    '''Represents a boolean property.'''
    DATE_TIME : MetadataPropertyType
    '''Represents a date property.'''
    TIME_SPAN : MetadataPropertyType
    '''Represents a time property.'''
    INTEGER : MetadataPropertyType
    '''Represents an integer property.'''
    LONG : MetadataPropertyType
    '''Represents a long integer property.'''
    DOUBLE : MetadataPropertyType
    '''Represents a property with a double or float value.'''
    STRING_ARRAY : MetadataPropertyType
    '''Represents a string array property.'''
    BYTE_ARRAY : MetadataPropertyType
    '''Represents a byte array property.'''
    DOUBLE_ARRAY : MetadataPropertyType
    '''Represents an array of double values.'''
    INTEGER_ARRAY : MetadataPropertyType
    '''Represents an array of integer values.'''
    LONG_ARRAY : MetadataPropertyType
    '''Represents an array of long values.'''
    METADATA : MetadataPropertyType
    '''Represents a nested metadata block.'''
    METADATA_ARRAY : MetadataPropertyType
    '''Represents an array of nested metadata blocks.'''
    GUID : MetadataPropertyType
    '''Represents a global unique identifier value.'''
    PROPERTY_VALUE_ARRAY : MetadataPropertyType
    '''Represents a metadata property value array.'''

class MetadataType:
    '''Specifies the type of a metadata package.'''
    
    UNDEFINED : MetadataType
    '''The type of a metadata package is undefined.'''
    ROOT : MetadataType
    '''A root metadata package containing other format-specific packages.'''
    XMP : MetadataType
    '''An XMP metadata package.'''
    EXIF : MetadataType
    '''An EXIF metadata package,'''
    IPTC : MetadataType
    '''An IPTC metadata package,'''
    DUBLIN_CORE : MetadataType
    '''A Dublin Core metadata package.'''
    IMAGE_RESOURCE_BLOCK : MetadataType
    '''A Photoshop\'s native metadata package.'''
    FILE_FORMAT : MetadataType
    '''A package containing information about the format of a loaded file.'''
    DIGITAL_SIGNATURE : MetadataType
    '''A package containing digital signature metadata.'''
    PRESENTATION : MetadataType
    '''A presentation metadata package.'''
    SPREADSHEET : MetadataType
    '''A spreadsheet metadata package.'''
    WORD_PROCESSING : MetadataType
    '''A word processing metadata package.'''
    DIAGRAM : MetadataType
    '''A diagram metadata package.'''
    NOTE : MetadataType
    '''A metadata package containing information about an electronic note file.'''
    PROJECT_MANAGEMENT : MetadataType
    '''A metadata package containing information about a project management file.'''
    PDF : MetadataType
    '''A PDF metadata package.'''
    DOCUMENT_STATISTICS : MetadataType
    '''A package containing document statistics.'''
    PSD : MetadataType
    '''A metadata package containing information about a Photoshop document.'''
    JPEG2000 : MetadataType
    '''A JPEG2000 native metadata package.'''
    DICOM : MetadataType
    '''A DICOM native metadata package.'''
    BMP : MetadataType
    '''A BMP native metadata package.'''
    WAV : MetadataType
    '''A WAV native metadata package.'''
    ID3V1 : MetadataType
    '''An ID3V1 tag.'''
    ID3V2 : MetadataType
    '''An ID3V2 tag.'''
    MPEG_AUDIO : MetadataType
    '''An MPEG audio native metadata package.'''
    LYRICS3 : MetadataType
    '''A Lyrics3 metadata package.'''
    APE_V2 : MetadataType
    '''An APEv2 metadata package.'''
    AVI : MetadataType
    '''An AVI video native metadata package.'''
    FLV : MetadataType
    '''An FLV video native metadata package.'''
    ASF : MetadataType
    '''An ASF video native metadata package.'''
    MOV : MetadataType
    '''A QuickTime video.'''
    MATROSKA : MetadataType
    '''A native metadata package extracted from a video encoded with the Matroska multimedia container.'''
    ZIP : MetadataType
    '''A native metadata package of a ZIP archive.'''
    SEVEN_ZIP : MetadataType
    '''A native metadata package of a SevenZip archive.'''
    V_CARD : MetadataType
    '''A native metadata package of a VCard.'''
    EPUB : MetadataType
    '''A native metadata package of a EPUB e-book.'''
    OPEN_TYPE : MetadataType
    '''An OpenType font metadata package.'''
    CAD : MetadataType
    '''A metadata package extracted from a CAD drawing.'''
    EML : MetadataType
    '''An EML message metadata package.'''
    MSG : MetadataType
    '''An MSG message metadata package.'''
    TORRENT : MetadataType
    '''A torrent file metadata package.
    Please find more information at `https://en.wikipedia.org/wiki/Torrent_file/ <https://en.wikipedia.org/wiki/Torrent_file/>`.'''
    PNG : MetadataType
    '''A PNG image metadata package.'''
    DNG : MetadataType
    '''A DNG image metadata package.'''
    CR2 : MetadataType
    '''A CR2 image metadata package.'''
    RAR : MetadataType
    '''RAR is a proprietary archive file format that supports data compression, error correction and file spanning.'''
    TAR : MetadataType
    '''In computing, tar is a computer software utility for collecting many files into one archive file, often referred to as a tarball, for distribution or backup purposes.'''
    THREE_DS : MetadataType
    '''3DS is one of the file formats used by the Autodesk 3ds Max 3D modeling, animation and rendering software.'''
    DAE : MetadataType
    '''A DAE file is a Digital Asset Exchange file format that is used for exchanging data between interactive 3D applications.'''
    FBX : MetadataType
    '''FBX (Filmbox) is a proprietary file format (.fbx) developed by Kaydara and owned by Autodesk since 2006. It is used to provide interoperability between digital content creation applications. FBX is also part of Autodesk Gameware, a series of video game middleware.'''
    STL : MetadataType
    '''STL is a file format native to the stereolithography CAD software created by 3D Systems.[3][4][5] Chuck Hull, the inventor of stereolithography and 3D Systems’ founder, reports that the file extension is an abbreviation for stereolithography.'''
    GIS : MetadataType
    '''Gis format'''
    FB2 : MetadataType
    '''Files with .fb2 extension are FictionBook 2.0 eBook files that contains the structure of the eBook.'''
    MOBI : MetadataType
    '''The MOBI file format is one of the most widely used ebook file formats. The format is an enhancement to the old OEB (Open Ebook Format) format and was used as the proprietary format for Mobipocket Reader.'''
    OGG : MetadataType
    '''Ogg format'''

class PropertyAccessLevels:
    '''Defines access levels for metadata properties.'''
    
    READ : PropertyAccessLevels
    '''The property is read-only.'''
    UPDATE : PropertyAccessLevels
    '''It is possible to update the property using the :py:func:`groupdocs.metadata.common.MetadataPackage.update_properties` method.'''
    REMOVE : PropertyAccessLevels
    '''The property can be removed through the :py:func:`groupdocs.metadata.common.MetadataPackage.remove_properties` method.'''
    ADD : PropertyAccessLevels
    '''It is possible to update the property using the :py:func:`groupdocs.metadata.common.MetadataPackage.add_properties` method.'''
    FULL : PropertyAccessLevels
    '''Grants full access to the property.'''
    ADD_OR_UPDATE : PropertyAccessLevels
    '''It is allowed to add and update the property. All other operations are restricted.'''

