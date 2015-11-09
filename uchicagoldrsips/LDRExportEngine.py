from sys import stdout,stderr
from collections import namedtuple
from os import stat
from os.path import basename,join,dirname,exists, splitext
from subprocess import Popen,PIPE

import hashlib
from pymarc import MARCReader
from LDRFileTree import FileObject

class ExportError(Exception):
    def __init__(self,message):
        self.message = message

    def __str__(self):
        return "%s" % self.message

    def __repr__(self):
        return "%s" % self.message
        
class Exporter(object):
    repository_root = '/data/repository/ac/'
    tech_mdata_suffix = '.fits.xml'
    mdobject = None
    
    def __init__(self):
        pass

    def remove_leftpad_zeroes(self,s):
        count = 0
        i = ''
        for c in s:
            if c == '0' and not i:
                pass
            else:
                i += c
        return i

    def add_mdobject(self,mdata_object):
        assert mdata_object is FileObject
        self.accession = mdata_object.accession
        self.dirhead = mdata_object.dirhead
        self.mdobject = mdata_object
    
    def get_xml_root(self,mdata_path):
        if exists(mdata_path):
            xml_file = open(mdata_path)
            xml_document = ET.parse(xml_file)
            xml_file.close()
            xml_root = xml_document.getroot()
        else:
            stderr.write("WARNING: The xml file %s does not exist.\n" % mdata_path)
            xml_root = None
        return xml_root

    def get_specific_xml_element_value(xml_root,xml_path):
        if xml_root.find(xml_path):
            return xml_root.find(xml_path).text
        else:
            stderr.write("WARNING: Could not find the element %s in %s.\n" % (tag_name,str(xm_root)))
            return "(:unac)"

    def extract_dublincore_mdata(self,xml_file_path):
        from xml.etree import ElementTree as ET
        from os.path import join
        # xml_file_path = join(self.repository_root,mdobject.accession,
        #                      mdobject.dirhead,mdobject.filepath)
        xml_root = self.get_xml_root(xml_file_path)
        tags = ['title','date','descritpion']
        for tag in tags:
            yield get_specific_xml_element_value(tag)

    def extract_mix_mdata(self,xml_file_path):
        from xml.etree import ElementTree as ET
        from os.path import join
        fits_filepath = dfile.fiepath+self.tch_mdata_suffix
        # xml_file_path = join(self.repository_root,dfile.accession,
        #                      dfile.dirhead,fits_filepath)
        xml_root = self.get_xml_root(xml_file_path)
        namespace = 'http://hul.harvard.edu/ois/xml/ns/fits/fits_outpout'
        fileinfo_tag = '{%s}fileinfo' % namespace
        identification_tag = '{%s}identification' % namespace
        metadata_tag = '{%s}metadata' % namespace
        identity_tag = '{%s}identity' % namespace
        image_tag = '{%s}image' % namespace
        image_height_tag = '{%s}imageHeight' % namespace
        image_width_tag = '{%s}imageWidth' % namespace
        md5checksum_tag = '{%s}md5checksum'
        bitspersample_tag = '{%s}bitsPerSample' % namespace
        size_tag = '{%s}size' % namespace
        xml_paths = ['%s/%s' % (fileinfo_tag,size_tag),
                     '%s/%s' % (identification_tag,identity_tag),
                     '%s/%s/%s' % (metadata_tag,image_tag,image_height_tag),
                     '%s/%s/%s' % (metadata_tag,image_Tag,image_width_tag),
                     '%s/%s/%s' % (fileinfo_tag,md5checksum_tag)]
        for xml_path in xml_paths:
            yield get_specific_xml_element_value(xml_root,xml_path)

    def add_object_providedcho(self):
        subject = join(self.accession,self.dirhead,
                       self.dirtail)
        stype = "edm:ProvidedCHO"

    def add_object_aggregation(self):
        subject = join(self.accession,'aggregation',self.dirhead,
                       self.dirtail)
        stype = "ore:Aggregation"

    def add_object_rem(self):
        subject = join(self.accession,'rem',self.dirhead,
                       self.dirtail)
        stype = "ore:ResourceMap"

    def add_object_webresource(self,web_resource_object):
        assert web_resource_object is FileObject
        subject = join(self.accession,self.dirhead,
                       self.dirtail,basename(web_resource_object.filepath))
        stype = "edm:WebResource"

    def add_page_webresource(self,resource_object):
        assert type(resource_object) is type(FileObject())
        subject = join(self.accession,
                       self.dirhead,resource_object.filepath)
        stype = "edm:WebResource"

    def add_page_resource(self,resource_object):
        assert type(resource_object) is type(FileObject())
        subject = join(self.accession,self.dirhead,
                       page_object.filepath)
        stype = "rdfs:Resource"

    def add_page_aggregation(self):
        subject = join(self.accession,self.dirhead,self.dirtail,page.dirtail)
        stype = "ore:Aggregation"

    def add_page_rem(self):
        subject = join(self.accession,self.dirhead,self.dirtail,page.dirtail)
        stype = "ore:ResourceMap"
                       
class ExpCulturalAnthropology(Exporter):
    noid = None
    mrcfile = None
    masterfiles = []
    
    def create(self,v):
        import re
        import string
        self.mrcfile = v.descriptivemetadata[0]
        self.masterfiles = v.masterfiles
        self.partidentifiers = []
        self.subjects = []
        self.identifier = basename(self.mrcfile.filepath).split('.')[0]
        self.dirhead = self.mrcfile.dirhead
        self.dirtail = dirname(self.mrcfile.filepath)
        self.urlbase = join(self.dirhead,
                            self.dirtail,
                            self.identifier)
        self.accession = self.mrcfile.accession
        fpath = join('/data/repository/ac/',
                     self.mrcfile.accession,
                     self.mrcfile.dirhead,
                     self.mrcfile.filepath)
        fh = open(fpath,'rb')
        m = MARCReader(fh)
        for rec in m:
            self.dctype = "cartographic"
            self.edmtype = "IMAGE"
            self.title = rec.title()
            self.publisher = rec.publisher()
            self.date = rec.pubyear()
            try:
                self.creator = rec.author()
            except:
                self.creator = self.publisher()
            self.year = rec.pubyear()
            self.formatinfo = [x.value() for x in rec.physicaldescription()]
            self.subjects = [x.value() for x in rec.subjects()]
            for f in rec:
                if f.tag == '651':
                    self.coverage = f.value()
                elif f.tag == '255':
                    self.formatinfo.append(f.value())
                elif f.tag ==  '500':
                    self.description = f.value().replace('"','\\"')
                elif f.tag == '856':
                    self.partidentifiers.append(f.value())

    def write(self,writeobj):
        self.resourcemap(writeobj)
        self.providedcho(writeobj)
        self.aggregation(writeobj)
        self.proxy(writeobj)
        for n in self.masterfiles:
            self.webresource(n,writeobj)
                    
    def proxy(self,writeobj):
        writeobj.write("<"+self.accession+"/"+self.urlbase+"/"+self.identifier+".mrc>\n")
        writeobj.write("dc:format \"\"\"%s\"\"\";\n" % self.mrcfile.mimetype)
        writeobj.write("ore:proxyFor <%s>;\n" % join(self.accession,'ac',self.urlbase))
        writeobj.write("ore:proxyIn <%s>;\n" % join(self.accession,'aggregation',self.urlbase))
        writeobj.write("erc:who \"\"\"University of Chicago Library\"\"\";\n")
        writeobj.write("erc:what \"\"\":unapp\"\"\";\n")
        writeobj.write("erc:when \"\"\"%s\"\"\";\n" % self.mrcfile.date)
        writeobj.write("erc:where <%s>;\n" % join(self.accession,self.urlbase,self.identifier+".mrc")) 
        writeobj.write("a ore:Proxy.\n\n")

    def resourcemap(self,writeobj):
        writeobj.write("<"+self.accession+"/rem/"+self.urlbase+">\n")
        writeobj.write("dcterms:creator <http://repository.lib.uchicago.edu>;\n")
        writeobj.write("dcterms:created \"%s\"^^xsd:dateTime;\n" % self.mrcfile.date)
        writeobj.write("ore:describes <%s>;\n" % join(self.accession,'aggregation',self.urlbase))        
        writeobj.write("a ore:ResourceMap.\n\n")

        
    def providedcho(self,writeobj):
        writeobj.write("<"+self.accession+"/"+self.urlbase+">\n")
        writeobj.write("dc:title \"\"\"%s\"\"\";\n" % self.title)
        writeobj.write("dc:creator \"\"\"%s\"\"\";\n" % self.creator)
        writeobj.write("dc:date \"\"\"%s\"\"\";\n" % self.date)
        try:
            writeobj.write("dc:coverage \"\"\"%s\"\"\";\n" % self.coverage)
        except:
            pass
        try:
            writeobj.write("dc:description \"\"\"%s\"\"\";\n" % self.description)
        except:
            pass
        for n in self.formatinfo:
            writeobj.write("dc:format \"\"\"%s\"\"\";\n" % n.encode('utf-8'))        
        for n in self.partidentifiers:
            writeobj.write("dc:identifier \"\"\"%s\"\"\";\n" % n)
            
        for n in self.subjects:
            writeobj.write("dc:subject \"\"\"%s\"\"\";\n" % n)
        writeobj.write("dc:type \"\"\"cartographic\"\"\";\n")
        for n in self.masterfiles:
            purl = join(self.accession,self.urlbase,basename(n.filepath))
            writeobj.write("dcterms:hasPart <%s>;\n" % purl)
        writeobj.write("dcterms:isPartOf <ead/ICU.MAPS.CHI1890>;\n")
        writeobj.write("edm:year \"\"\"%s\"\"\";\n" % self.date)
        writeobj.write("erc:who \"\"\"%s\"\"\";\n" % self.creator)
        writeobj.write("erc:what \"\"\"%s\"\"\";\n" % self.title)
        writeobj.write("erc:when \"\"\"%s\"\"\";\n" % self.date)
        writeobj.write("erc:where <%s>;\n" % join(self.accession,self.urlbase))
        writeobj.write("edm:provider \"\"\"University of Chicago Library\"\"\";\n")
        writeobj.write("edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
        
        writeobj.write("a edm:ProvidedCHO.\n\n")

    def aggregation(self,writeobj):
        writeobj.write("<"+self.accession+"/aggregation/"+self.urlbase+">\n")
        writeobj.write("edm:aggregatedCHO <%s>;\n" % join(self.accession,self.urlbase))
        for n in self.partidentifiers:
            writeobj.write("edm:isShownAt <%s>;\n" % str('http://'+n.split('http://')[1]))
        writeobj.write("erc:who <http;//repository.lib.uchicago.edu/>;\n")
        writeobj.write("erc:what <%s>;\n" % join(self.accession,'ac',self.urlbase))
        writeobj.write("erc:when \"\"\"%s\"\"\";\n" % self.mrcfile.date)
        writeobj.write("erc:where <%s>;\n" % join(self.accession,self.urlbase))
        writeobj.write("ore:isDescribedBy <%s>;\n" % join(self.accession,'rem',self.urlbase))
        writeobj.write("a ore:Aggregation.\n\n")
        
    def webresource(self,n,writeobj):
        writeobj.write("<"+self.accession+"/aggregation/"+self.urlbase+'/'+self.identifier+".tif>\n")
        writeobj.write("dc:format \"\"\"%s\"\"\"\:\n" % n.mimetype )
        writeobj.write("premis:objectIdentifierType \"\"\"ARK\"\"\";\n")
        writeobj.write("premis:objectIdentifierValue <%s>;\n" % join(self.accession,
                                                                     self.urlbase,
                                                                     self.identifier+'.tif'))
        writeobj.write("premis:objectIdentifierCategory \"\"\"%s\"\"\";\n" % 'file')
        writeobj.write("premis:compositionLevel %s;\n" % 0)

        writeobj.write("premis:messageDigest \"\"\"%s\"\"\";\n" % hashlib.md5(open(join('/data/repository/ac/',
                                                                                        n.accession,
                                                                                        n.dirhead,
                                                                                        n.filepath), 'rb').read()).hexdigest())
        writeobj.write("premis:messageDigestAlgorithm \"\"\"%s\"\"\";\n" % 'MD5')
        writeobj.write("premis:messageDigest \"\"\"%s\"\"\";\n" % n.checksum)
        writeobj.write("premis:messageDigestAlgorithm \"\"\"%s\"\"\";\n" % 'SHA-256')
        writeobj.write("premis:messageDigestOriginator \"\"\"%s\"\"\";\n" % "/sbin/sha256")
        writeobj.write("premis:size %s;\n" % n.filesize)
        writeobj.write("premis:formatName \"\"\"%s\"\"\";\n" % n.mimetype)
        writeobj.write("premis:originalName \"\"\"%s\"\"\";\n" % basename(n.filepath))
        writeobj.write("premis:eventIdentifierValue \"\"\"%s\"\"\";\n" % n.accession)
        writeobj.write("premis:eventIdentifierType \"\"\"%s\"\"\";\n" % "ARK")
        writeobj.write("premis:eventDateTime \"\"\"%s\"\"\"^^xsd:dateTime;\n" % n.date)
        writeobj.write("a edm:WebResource.\n\n")
                    
class ExpCampusPub2015(Exporter):
    noid = None
    pages = []
    metsfile = None
    structuralfile = None
    representation = None
    textfile = None
    metsfile = None
    masterfiles = []
    masterxmlfiles = []
    masterrepresentations = []
    valid = False

    def create(self,v):
        from os.path import basename
        print(v)
        # pages = []
        # noid = None
        # mdobject = v.descriptivemetadata[0]
        # metsobject = v.metsfile[0]
        # textfile = v.textfile[0]
        # metsfile = v.metsfile[0]
        # structuralfile = v.structuralfile[0]
        # representation = v.webrepresentation[0]
        # masterfilelist = v.masterfiles
        # masterxmllist = v.mastermetadata
        # jpegfiles = v.masterrepresentations
        # dublincore = v.descriptivemetadata[0]

        # dc_basename = basename(dublincore.filepath)
        # dc_basename_sans_extension,extension = splitext(dc_basename)
        # collection,record,volume,issue = dc_basename_sans_extension.split('-')        
        # new_version_dc_filepath = join('/data/repository/ac/','jsrfb0tc9tvff',
        #                                '2016-109',collection,record,volume,issue.split('.')[0],
        #                                dc_basename)        
        # if exists(new_version_dc_filepath):
        #      filepath = join("2016-109",collection,record,volume,issue.split('.')[0],dc_basename)
        #      checksum = Popen(['sha256',new_version_dc_filepath],stdout=PIPE).communicate()[0].rstrip()
        #      checksum = checksum.split(' = ')[1].rstrip()
        #      size = stat(new_version_dc_filepath).st_size
        #      accession = "jsrfb0tc9tvff"
        #      mimetype = "application/xml"
        #      date = "2016-09-14T13:06:27.724990"
        #      dublincore = FileObject(filepath,accession,date,checksum,mimetype,size)
        #      mdobject = dublincore
        #      self.dublincore = mdobject
        #      self.new_dublincore = True
            
        # else: 
        #     dublincore = v.descriptivemetadata[0]
        #     mdobject = dublincore
        #     self.new_dublincore = False
        #     self.dublincore = mdobject
            
        #     stderr.write("%s\n" % new_version_dc_filepath)
        #     stderr.write("%s\n" % self.new_dublincore)        
        # stderr.write("{filep}\n".format(filep=mdobject.filepath))        
        # textfile = v.textfile[0]
        # representation = v.webrepresentation[0]
        # title,description, \
        #     date,identifier, \
        #     createdate,volume, \
        #     issue,record,accession, \
        #     dirhead = self.extractMetadata(mdobject)
        # ident = identifier.encode('utf-8')
        # identifierpieces = ident.split('-')
        # mdobjectdirn = dirname(mdobject.filepath)
        # mdobjectpieces = mdobjectdirn.split('/')
        # dublincoredirn = dirname(dublincore.filepath)
        # textfiledirn = dirname(textfile.filepath)
        # representationdirn = dirname(representation.filepath)
        # dirncheck = mdobjectdirn == dublincoredirn == textfiledirn == representationdirn
        # if mdobjectdirn != dublincoredirn:
        #     stderr.write("WARNING: dublincore path %s mdobject path %s are mismatched" % \
        #                  (dublincoredirn,mdobjectdirn))
        #     if mdobjectdirn != textfiledirn:
        #         stderr.write("WARNING: dublincore path %s textfile path %s are mismatched" % \
         #                      (dublincoredirn,textfiledirn))
        #     if mdobojectdirn != representationdirn:
        #             stderr.write("WARNING: dublincore path %s representation path %s are mismatched" % \
        #                          (modobjectdirn,representationdirn))
        # c = True
        # for n in identifierpieces:
        #     idx = identifierpieces.index(n)
        #     if mdobjectpieces[idx] != n:
        #         c = False
        #         stderr.write("WARNING: for dublin core path %s and identifier %s, identifier part is %s; path part is %s\n" % \
        #                      (dublincoredirn,identifier,n,mdobjectpieces[idx]))
        # if c:
        #     masterfilelist = sorted(v.masterfiles,key=lambda x: x.filepath)
        #     masterxmllist = sorted(v.mastermetadata,key=lambda x: x.filepath)
        #     masterjpgfiles = sorted(v.masterrepresentations,key=lambda x: x.filepath)
        #     pages = []
        #     for n in masterfilelist:
        #         pageob = namedtuple("pageobject","accession displaypagenum pagenum jpeg xml tiff")            
        #         dn = dirname(n.filepath)
        #         bn = basename(n.filepath).split('.')[0].split('_')[1]
        #         pageob.displaypagenum = self.remove_leftpad_zeroes(bn)
        #         pageob.paddedzeroespagenum = '0000'+bn
        #         pageob.pagenum = bn
        #         if not dn.startswith(dublincoredirn):
        #             stderr.write("The tiff directory %s does not match the directory for " % dn +
        #                          "the dublincore directory %s" %  dublincoredirdn)
        #         xmlfiltered = [x for x in masterxmllist if bn in x.filepath]
        #         jpgfiltered = [x for x in masterjpgfiles if bn in x.filepath]
        #         xmlaccession = [x.accession for x in masterxmllist]
        #         jpgaccession = [x.accession for x in masterjpgfiles]
        #         xmldirheads = [x.dirhead for x in masterxmllist]
        #         jpgdirheads = [x.dirhead for x in masterjpgfiles]
        #         accessions = [x for x in xmlaccession \
        #                       if x in jpgaccession]
        #         dirheads = [x for x in xmldirheads \
        #                     if x in jpgdirheads]
        #         pageob.accession = accessions[0]
        #         pageob.dirhead = dirheads[0]
        #         pageob.xml = xmlfiltered[0]
        #         pageob.jpg = jpgfiltered[0]
        #         n = self.extractMixData(metsfile,bn,n)
        #         pageob.tiff = n

        #         pages.append(pageob)

        #     self.identifier = identifier
        #     self.title = title
        #     self.date = date
        #     self.description = description
        #     self.representation = representation
        #     self.dublincore = dublincore
        #     self.mdobject = mdobject
        #     self.textfile = textfile
        #     self.metsfile = metsfile
        #     self.pages = pages
        #     self.createdate = representation.date
        #     self.accession = representation.accession
        #     self.dirhead = representation.dirhead
        #     self.record = dirname(representation.filepath).split('/')[1]
        #     self.volume = dirname(representation.filepath).split('/')[2]
        #     self.issue = dirname(representation.filepath).split('/')[3]
        #     self.valid = True    
    
    
    # def create(self,v):
    #     from os.path import basename
    #     self.pages = []
    #     self.noid = None
    #     self.dublincore = v.descriptivemetadata[0]
    #     self.mdobject = v.descriptivemetadata[0]
    #     self.textfile = v.textfile[0]
    #     self.metsfile = v.metsfile[0]
    #     self.structuralfile = v.structuralfile[0]
    #     self.representation = v.webrepresentation[0]
        # masterfilelist = v.masterfiles
        # masterxmllist = v.mastermetadata
        # jpegfiles = v.masterrepresentations
        # self.title, self.description, \
        #     self.date, self.identifier, \
        #     self.createdate, self.volume, \
        #     self.issue, self.record, self.accession, \
        #     self.dirhead = self.extractMetadata(self.mdobject)    
        # for n in masterfilelist:
        #     corefn = basename(n.filepath).split('-')[-1].split('_')[1]
        #     atuple = self.extractMixData(self.metsfile,corefn)
        #     try:
        #         n.miximageheight = atuple[5]
        #         n.miximageheight = atuple[5]
        #         n.miximagewidth = atuple[4]
        #         n.mixmessagedigest = atuple[3]
        #         n.mixmessagedigestalgorithm = atuple[2]
        #         n.mixformatname = atuple[1]
        #         n.mixfilesize = atuple[0]
        #     except:
        #         stderr.write("%s no mix data\n" % n.filepath)
        #     p = namedtuple("page","pagenum id files accession dirhead")

        #     p.files  = []
        #     pn = basename(n.filepath).split('.')[0]
        #     p.displaypagenum = '0000'+pn.split('-')[-1].split('_')[1]
        #     p.pagenum = pn
        #     xmlf = filter(lambda x: pn in x.filepath,masterxmllist)[0]
        #     p.files.append(xmlf)
        #     jpegf = filter(lambda x: pn in x.filepath,jpegfiles)[0]
        #     p.files.append(jpegf)
        #     tiff = n
            
        #     p.files.append(tiff)
        #     p.accession = n.accession
        #     p.dirhead = n.dirhead
        #     self.pages.append(p) 
        # self.valid = True
            
    def extractMixData(self,metsobject,searchable,tfileob):
        from xml.etree import ElementTree as ET
        from os.path import join
        xmlfile = join('/data/repository/ac/',metsobject.accession,metsobject.dirhead,metsobject.filepath)
        root = ET.parse(xmlfile).getroot()
        xmldatas = root.findall('{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}techMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData')
        bingo = None
        for n in xmldatas:
            objidvalue = n.find('./{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation/{http://www.loc.gov/mix/v20}ObjectIdentifier/{http://www.loc.gov/mix/v20}objectIdentifierValue')
            test = searchable in objidvalue.text
            if searchable in objidvalue.text:
                mixfilesize = n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation/{http://www.loc.gov/mix/v20}fileSize').text
                tfileob.mixfilesize = mixfilesize
                mixformatname = n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation/{http://www.loc.gov/mix/v20}FormatDesignation/{http://www.loc.gov/mix/v20}formatName').text
                tfileob.mixformatname = mixformatname
                mixdigestalgo = n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation/{http://www.loc.gov/mix/v20}Fixity/{http://www.loc.gov/mix/v20}messageDigestAlgorithm').text
                tfileob.mixdigestalgo = mixdigestalgo
                mixdigest = n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation/{http://www.loc.gov/mix/v20}Fixity/{http://www.loc.gov/mix/v20}messageDigest').text
                tfileob.mixdigest = mixdigest
                miximagewidth = n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicImageInformation/{http://www.loc.gov/mix/v20}BasicImageCharacteristics/{http://www.loc.gov/mix/v20}imageWidth').text
                tfileob.miximagewidth = miximagewidth
                miximageheight =  n.find('{http://www.loc.gov/mix/v20}mix/{http://www.loc.gov/mix/v20}BasicImageInformation/{http://www.loc.gov/mix/v20}BasicImageCharacteristics/{http://www.loc.gov/mix/v20}imageHeight').text
                tfileob.miximageheight = miximageheight
                return tfileob
        stderr.write("%s couldn't be found in %s\n" % (searchable,xmlfile))

        xmlfile = join('/data/repository/ac/',tfileob.accession,tfileob.dirhead,tfileob.filepath+'.fits.xml')
        if exists(xmlfile):

            xmlfile = open(xmlfile)
        else:
            stderr.write("%s does not exists\n" % xmlfile)
            return tfileob
        root = ET.parse(xmlfile).getroot()
        mixfilesize = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fileinfo/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}size').text
        setattr(tfileob,'mixfilesize',mixfilesize)
        mixformatname = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}identification/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}identity').attrib['mimetype']
        setattr(tfileob,'mixformatname',mixformatname)
        miximageheight = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageHeight').text
        setattr(tfileob,'miximageheight',miximageheight)        
        miximagewidth = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageWidth').text
        setattr(tfileob,'miximagewidth',miximagewidth)
        mixdigest =  root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fileinfo/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}md5checksum').text
        setattr(tfileob,'mixdigest',mixdigest)
        mixdigestalgo = 'MD5'
        setattr(tfileob,'mixdigestalgo',mixdigestalgo)        
        mixbitspersample = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}bitsPerSample').text
        setattr(tfileob,'mixbitspersample',mixbitspersample)
        return tfileob
        
        return tfileob
        
    def extractMetadata(self,mdobject):
        from xml.etree import ElementTree as ET
        from os.path import join
        createdate = mdobject.date
        xmlfile = join('/data/repository/ac/',mdobject.accession,mdobject.dirhead,mdobject.filepath)
        root = ET.parse(xmlfile).getroot()
        title = root.find('title')
        description = root.find('description')
        date = root.find('date')
        identifier = root.find('identifier')
        record = identifier.text.split('-')[1]
        volume = identifier.text.split('-')[2]
        issue = identifier.text.split('-')[3]
        return (title.text, description.text,
                date.text, identifier.text,
                createdate, volume, issue,
                record, mdobject.accession,
                mdobject.dirhead)
    
    def write(self,writeobj,count):
        self.issueresourcemap(writeobj)
        count.rems += 1
        self.issueprovidedcho(writeobj)
        count.issueprovidedchos += 1
        self.issueaggregation(writeobj)
        count.issueaggregations += 1
        self.issueproxy(writeobj)
        count.issueproxies += 1

        self.issuemetswebresource(writeobj)

        self.issuewebresource(writeobj)
        count.issuewebresources += 1
        prev = None
        for p in self.pages:
            self.pageprovidedcho(p,writeobj,prev)
            self.pageresourcemap(p,writeobj)
            xmlfile = p.xml
            jpegfile = p.jpg
            tiffile = p.tiff
            self.pageaggregation(p,writeobj,tiffile,jpegfile)
            self.pagetiffwebresource(p,writeobj,tiffile)
            self.pagejpegwebresource(p,writeobj,jpegfile)
            self.pagexmlwebresource(p,writeobj,xmlfile)
            prev = p
        return count
    
    def issueproxy(self,writeobj):
        # start of issue proxy
        #     writeobj.write("<"+self.dublincore.accession+'/'+self.dublincore.dirhead+'/mvol/'+
        #                    self.record+'/'+self.volume+'/'+self.issue+
        #                    self.identifier+'.dc.xml>\n')
        # else:
        writeobj.write("<"+self.mdobject.accession+'/'+self.mdobject.dirhead+'/mvol/'+self.record+'/'+
                       self.volume+'/'+self.issue+'/'+self.identifier+'.dc.xml>\n')

        writeobj.write("dc:format \"%s\";\n" % self.dublincore.mimetype)
        writeobj.write("ore:proxyFor <"+self.accession+'/'+
                     self.dirhead+'/mvol/'+self.record+'/'+self.volume+'/'+self.issue+'>;\n')
        writeobj.write("ore:proxyIn <"+self.accession+'/aggregation/'+
                     self.dirhead+'/mvol/'+self.record+'/'+self.volume+'/'+self.issue+'>;\n')
        writeobj.write("a ore:Proxy.\n\n")
        # end of issue proxy

    def issuemetswebresource(self,writeobj):
        # start of mets web resource
        writeobj.write("<"+
                       self.accession+"/"+self.dirhead+"/mvol/"+
                       self.record+'/'+self.volume+'/'+self.issue+'/'+
                       self.identifier+'.mets.xml>\n')
        writeobj.write("dc:format \"\"\"%s\"\"\";\n" % self.metsfile.mimetype)
        writeobj.write("a rdfs:Resource.\n\n")
        # end of mets web resource
        
    def issueprovidedcho(self,writeobj):
        # start of issue providedcho
        writeobj.write("<%s/%s/mvol/%s/%s/%s>\n" \
                       % (self.accession,self.dirhead,self.record,self.volume,self.issue))
        writeobj.write("dc:coverage \"Chicago\";\n")
        writeobj.write("dc:date \"%s\";\n" % self.date)
        writeobj.write("edm:year \"%s\";\n" % self.date[0:4])
        writeobj.write("dc:description \"%s\";\n"  % self.description)
        writeobj.write("dc:identifier \"%s\";\n" % self.identifier)
        writeobj.write("dc:language \"en\";\n")
        writeobj.write("dc:rights <http:/createivecommons.org/licenses/by-nc/4.0/>;\n")
        writeobj.write("dc:title \"%s\";\n" % self.title)
        writeobj.write("dc:type \"text\";\n")
        writeobj.write("edm:type \"TEXT\";\n")
        writeobj.write("dc:description <"+
                       self.accession+'/aggregation/'+
                       self.dirhead+'/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/'+
                       self.identifier+'.txt>;\n')
        writeobj.write("dcterms:isPartOf <ead/ICU.SPCL.CAMPUB>;\n")
        for p in self.pages:
            writeobj.write("dcterms:hasPart <"+self.accession+'/'+
                           self.dirhead+'/mvol/'+self.record+'/'+self.volume+'/'+self.issue+'/'+p.paddedzeroespagenum+'>;\n')
        writeobj.write("a edm:ProvidedCHO.\n\n")
        # end of issue providedcho
        
    def issueresourcemap(self,writeobj):
        # start of issue resourcemap
        writeobj.write('<'+
                       self.accession+'/rem/'+self.dirhead+'/'+'mvol/'+
                       self.record+'/'+self.volume+'/'+self.issue+'>\n')

        writeobj.write('dcterms:created \"%s\"^^xsd:dateTime;\n' \
                       % self.createdate.split('.')[0])
        writeobj.write("dcterms:creator <http://repository.lib"+
                       ".uchicago.edu/>;\n")
        writeobj.write("ore:describes <"+
                       self.accession+'/aggregation/'+self.dirhead+'/'+'mvol/'+
                       self.record+'/'+self.volume+'/'+self.issue+'>;\n')
        writeobj.write('a ore:ResourceMap.\n\n')
        # end of issue resourcemap

    def issueaggregation(self,writeobj):
        # start of issue aggregation
        writeobj.write("<%s/aggregation/%s/mvol/%s/%s/%s>\n" % \
                       (self.accession,self.dirhead,self.record,
                        self.volume,self.issue))
        writeobj.write("edm:aggregatedCHO <%s/%s/mvol/%s/%s/%s>;\n" % \
                       (self.accession,self.dirhead,self.record,
                        self.volume,self.issue))
        writeobj.write("edm:dataProvider \"University of Chicago Library\";\n")
        writeobj.write("edm:isShownAt <http://pi.lib.uchicago.edu/1001/dig/campub/%s>;\n" % self.identifier)
        writeobj.write("edm:isShownBy <%s/%s/mvol/%s/%s/%s/%s.pdf>;\n" % \
                       (self.representation.accession,
                        self.representation.dirhead,
                        self.record,self.volume,
                        self.issue,self.identifier))

        jpgobject = [x for x in self.pages if int(x.displaypagenum)==1]
        if jpgobject:
            jpgobject = jpgobject[0].jpg
            writeobj.write("edm:object <%s/%s/%s>;\n" % (jpgobject.accession,jpgobject.dirhead,jpgobject.filepath))
        else:
            stderr.write("%s is missing a first page.\n" % join(self.record,self.volume,self.issue))
            
        writeobj.write("edm:provider \"University of Chicago Library\";\n")
        writeobj.write("dc:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
        writeobj.write('ore:isDescribedBy <%s/rem/%s/mvol/%s/%s/%s>;\n' % \
                       (self.accession,self.dirhead,
                        self.record,self.volume,self.issue))
        writeobj.write("a ore:Aggregation.\n\n")
        # end of issue aggregation
        
    def issuewebresource(self,writeobj):
        # start of issue webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/%s.pdf>\n" %
                       (self.accession,self.dirhead,self.record,self.volume,self.issue,self.identifier))
        writeobj.write('dcterms:isFormatOf <http://ldr.lib.uchicago.edu/%s/%s/mvol/%s/%s/%s>;\n' %
                       (self.accession,self.dirhead,self.record,self.volume,self.issue))
        writeobj.write("premis:objectIdentifierType \"ARK\";\n")
        writeobj.write("premis:objectIdentifierValue <%s/%s/mvol/%s/%s/%s/%s.pdf>;\n" %
                       (self.accession,self.dirhead,self.record, self.volume, self.issue, self.identifier))
        writeobj.write("dc:format \"\"\"%s\"\"\";\n" % self.representation.mimetype)
        writeobj.write("premis:objectCategory \"file\";\n")
        writeobj.write("premis:compositionLevel 0;\n")
        writeobj.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
        writeobj.write("premis:messageDigest \"%s\";\n" % self.representation.checksum)
        writeobj.write("premis:messageDigestOriginator \"/sbin/sha256\";\n")
        writeobj.write("premis:size %s;\n" % self.representation.filesize)
        writeobj.write("premis:formatName \"application/pdf\";\n")
        writeobj.write("premis:originalName \"%s.pdf\";\n" % self.identifier)
        writeobj.write("premis:eventIdentifierType \"ARK\";\n")
        writeobj.write("premis:eventIdentifierValue \"%s\";\n" % self.representation.accession) 
        writeobj.write("premis:eventType \"creation\";\n")
        writeobj.write("premis:eventDateTime \"%s\"^^xsd:dateTime;\n" % self.representation.date.split('.')[0])
        writeobj.write("a edm:WebResource.\n\n")
        # end of issue webresource        


    def pageprovidedcho(self,p,writeobj,prev):
        writeobj.write("<"+
                       p.accession+'/'+
                       p.dirhead+'/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/'+
                       str(p.paddedzeroespagenum)+'>\n')
        writeobj.write("dc:description <"+
                       self.accession+'/'+
                       self.dirhead+
                       '/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/ALTO/mvol/'+
                       self.record+'-'+
                       self.volume+'-'+
                       self.issue+'_'+
                       str(p.pagenum)+'.xml>;\n')
        writeobj.write("dc:language \"en\";\n")
        writeobj.write("dc:rights <http://creativecommons.org/"+
                       "licenses/by-nc/4.0/>;\n")
        writeobj.write("dc:type \"Text\";\n")
        writeobj.write("edm:type \"TEXT\";\n")
        writeobj.write("dc:title \"Page %s\";\n" % p.displaypagenum)
        writeobj.write("dcterms:isPartOf <"+
                       self.accession+
                       '/'+self.dirhead+'/mvol/'+
                       self.volume+'/'+self.record+'/'+self.issue+'>;\n')
        if not prev:
            pass
        else:
            writeobj.write("edm:isNextInSequence <"+ \
                         "%s/%s/mvol/%s/%s/%s/%s>;\n" % \
                         (prev.accession, prev.dirhead, self.record,
                          self.volume, self.issue, str(prev.paddedzeroespagenum)))
        writeobj.write("a edm:ProvidedCHO.\n\n")

    def pageresourcemap(self,p,writeobj):
        # start of page resourcemap
        writeobj.write("<"+
                     p.accession+"/rem/"+
                     p.dirhead+"/"+
                     self.record+"/"+
                     self.volume+"/"+
                     self.issue+"/"+
                    str(p.paddedzeroespagenum)+">\n")
        writeobj.write('dcterms:created \"%s\"^^xsd:dateTime;\n' \
                     % self.createdate.split('.')[0])
        writeobj.write('dcterms:creator <http://repository.lib.uchicago.edu/>;\n')
        writeobj.write("ore:describes <"+
        "%s/aggregation/%s/mvol/%s/%s/%s/%s>;\n" %\
                     (self.accession, self.dirhead, self.record,
                      self.volume, self.issue, str(p.paddedzeroespagenum)))
        writeobj.write('a ore:ResourceMap.\n\n')
        # end of page resourcemap

    def pageaggregation(self,p,writeobj,tiff,jpeg):
        # start of page aggregation
        writeobj.write("<"+
                       "%s/aggregation/%s/mvol/%s/%s/%s/%s>\n" % \
                       (p.accession,p.dirhead,self.record,
                        self.volume,self.issue,str(p.paddedzeroespagenum)))
        writeobj.write("edm:aggregatedCHO <"+
                       "%s/%s/mvol/%s/%s/%s/%s>;\n" % \
                       (self.accession,
                        self.dirhead,
                        self.record,
                        self.volume,
                        self.issue,
                        p.paddedzeroespagenum))
        writeobj.write('edm:dataProvider \"University of Chicago'+
                       ' Library\";\n') 
        writeobj.write("edm:isShownBy <"+
                       "%s/%s/mvol/%s/%s/%s/TIFF/%s_%s.tif>;\n" % \
                       (tiff.accession,
                        tiff.dirhead,
                        self.record,
                        self.volume,
                        self.issue,
                        self.identifier,
                        p.pagenum))
        writeobj.write("edm:object <"+
                       "%s/%s/mvol/%s/%s/%s/JPEG/%s_%s.jpg>;\n" % \
                       (jpeg.accession,jpeg.dirhead,self.record,
                        self.volume,self.issue,self.identifier,p.pagenum))
        writeobj.write('edm:provider \"University of Chicago Library\";\n')
        writeobj.write('edm:rights <http://creativecommons.org/'+
                       'licenses/by-nc/4.0/>;\n')
        writeobj.write("ore:isDescribedBy <"+
                       "%s/rem/%s/mvol/%s/%s/%s/%s>;\n" % \
                       (self.accession,self.dirhead,self.record,
                        self.volume,self.issue,p.paddedzeroespagenum))
        writeobj.write("a ore:Aggregation.\n\n")
        # end of page aggregation

    def pagetiffwebresource(self,p,writeobj,tfile):
        # start of tif file edm:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/TIFF/mvol-%s-%s-%s-%s.tif>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)

        try:
            writeobj.write("mix:fileSize %s;\n" % tfile.mixfilesize)
            writeobj.write("mix:formatName \"%s\";\n" % tfile.mixformatname)
            writeobj.write("mix:messageDigestAlgorithm \"%s\";\n" % tfile.mixdigestalgo)
            writeobj.write("mix:messageDigest \"%s\";\n" % tfile.mixdigest)
            writeobj.write("mix:imageWidth %s;\n" % tfile.miximagewidth)
            writeobj.write("mix:imageHeight %s;\n" % tfile.miximageheight)
            writeobj.write("mix:bitsPerSampleUnit \"\"\"%s\"\"\";\n" % tfile.mixbitspersample)
        except:
            pass
        writeobj.write('premis:objectIdentifierType \"ARK\";\n')
        writeobj.write("premis:objectIdentifierValue"+
        " <%s/%s/%s>;\n" \
                     % (tfile.accession, tfile.dirhead, tfile.filepath))
        writeobj.write('premis:objectCategory \"file\";\n')
        writeobj.write('premis:compositionLevel 0;\n')
        writeobj.write('premis:messageDigestAlgorithm \"SHA-256\";\n')
        writeobj.write('premis:messageDigest \"%s\";\n' % tfile.checksum)
        writeobj.write('premis:messageDigestOriginator \"/sbin/sha256\";\n')

        writeobj.write('premis:size %s;\n' % tfile.filesize)
        writeobj.write('premis:formatName \"%s\";\n' % tfile.mimetype)
        writeobj.write('premis:originalName \"%s\";\n' % \
                     basename(tfile.filepath))
        writeobj.write('premis:eventIdentifierType \"ARK\";\n')
        writeobj.write('premis:eventIdentifierValue \"%s\";\n' % tfile.accession)
        writeobj.write('premis:eventType \"creation\";\n')
        writeobj.write('premis:eventDateTime \"%s\"^^xsd:dateTime;\n' % \
                     tfile.date.split('.')[0])
        writeobj.write('a edm:WebResource.\n\n')
        # end of tif file edm:webresource

    def pagejpegwebresource(self,p,writeobj,tfile):
        from os.path import basename
        # start of jpeg file rdfs:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/JPEG/mvol-%s-%s-%s_%s.%s>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum,
                      basename(tfile.filepath).split('.')[1]))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write("a edm:WebResource.\n\n")
        # end of jpeg file rdfs:webresource

    def pagexmlwebresource(self,p,writeobj,tfile):
        # start of pos file rdfs:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/ALTO/mvol-%s-%s-%s_%s.%s>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum,
                      basename(tfile.filepath).split('.')[1]))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write("a rdfs:Resource.\n\n")
        # end of pos file rdfs:webresource
        
class ExpCampusPub2014(Exporter):
    pages = []
    noid = []
    mdobject = None
    textfile = None
    representation = None
    masterfiles = []
    masterxmlfiles = []
    masterrepresentations = []
    masterposfiles = []
    valid = False
    
    def __init__(self):
        pass
    
    def create(self,v):
        from os.path import basename
        pages = []
        noid = None
        dublincore = v.descriptivemetadata[0]

        dc_basename = basename(dublincore.filepath)
        dc_basename_sans_extension,extension = splitext(dc_basename)
        collection,record,volume,issue = dc_basename_sans_extension.split('-')
        new_version_dc_filepath = join('/data/repository/ac/','jsrfb0tc9tvff',
                                       '2016-109',collection,record,volume,issue.split('.')[0],
                                       dc_basename)
        if exists(new_version_dc_filepath):
             filepath = join("2016-109",collection,record,volume,issue.split('.')[0],dc_basename)
             checksum = Popen(['sha256',new_version_dc_filepath],stdout=PIPE).communicate()[0].rstrip()
             checksum = checksum.split(' = ')[1].rstrip()
             size = stat(new_version_dc_filepath).st_size
             accession = "jsrfb0tc9tvff"
             mimetype = "application/xml"
             date = "2016-09-14T13:06:27.724990"
             dublincore = FileObject(filepath,accession,date,checksum,mimetype,size)
             mdobject = dublincore
             self.dublincore = mdobject
             self.new_dublincore = True
            
        else: 
            dublincore = v.descriptivemetadata[0]
            mdobject = dublincore
            self.new_dublincore = False
            self.dublincore = mdobject

        if self.new_dublincore == True:
            stderr.write("{accession}\n".format(accession=mdobject.accession))
            stderr.write("{filep}\n".format(filep=mdobject.filepath))
        
        textfile = v.textfile[0]
        representation = v.webrepresentation[0]
        title,date,identifier,description = self.extractMetadata(mdobject)
        ident = identifier.encode('utf-8')
        identifierpieces = ident.split('-')
        mdobjectdirn = dirname(mdobject.filepath)
        mdobjectpieces = mdobjectdirn.split('/')
        dublincoredirn = dirname(dublincore.filepath)
        textfiledirn = dirname(textfile.filepath)
        representationdirn = dirname(representation.filepath)
        dirncheck = mdobjectdirn == dublincoredirn == textfiledirn == representationdirn
        # if mdobjectdirn != dublincoredirn:
        #     stderr.write("WARNING: dublincore path %s mdobject path %s are mismatched" % \
        #                  (dublincoredirn,mdobjectdirn))
        #     if mdobjectdirn != textfiledirn:
        #         stderr.write("WARNING: dublincore path %s textfile path %s are mismatched" % \
        #                      (dublincoredirn,textfiledirn))
        #     if mdobojectdirn != representationdirn:
        #             stderr.write("WARNING: dublincore path %s representation path %s are mismatched" % \
        #                          (modobjectdirn,representationdirn))
        c = True
        # for n in identifierpieces:
        #     idx = identifierpieces.index(n)
        #     if mdobjectpieces[idx] != n:
        #         c = False
        #         stderr.write("WARNING: for dublin core path %s and identifier %s, identifier part is %s; path part is %s\n" % \
        #                      (dublincoredirn,identifier,n,mdobjectpieces[idx]))
        if c:
            masterfilelist = sorted(v.masterfiles,key=lambda x: x.filepath)
            masterxmllist = sorted(v.mastermetadata,key=lambda x: x.filepath)
            masterjpgfiles = sorted(v.masterrepresentations,key=lambda x: x.filepath)
            masterposfiles = sorted(v.masterocrs,key=lambda x: x.filepath)
            pages = []
            for n in masterfilelist:
                pageob = namedtuple("pageobject","accession displaypagenum pagenum jpeg ocr xml tiff")            
                dn = dirname(n.filepath)
                bn = basename(n.filepath).split('.')[0]
                pageob.displaypagenum = self.remove_leftpad_zeroes(bn)
                pageob.pagenum = bn
                if not dn.startswith(dublincoredirn):
                    stderr.write("The tiff directory %s does not match the directory for " % dn +
                                 "the dublincore directory %s" %  dublincoredirdn)
                    
                xmlfiltered = [x for x in masterxmllist if bn in x.filepath]
                jpgfiltered = [x for x in masterjpgfiles if bn in x.filepath]
                posfiltered = [x for x in masterposfiles if bn in x.filepath]            

                xmlaccession = [x.accession for x in masterxmllist]
                jpgaccession = [x.accession for x in masterjpgfiles]
                posaccession = [x.accession for x in masterposfiles]

                xmldirheads = [x.dirhead for x in masterxmllist]
                jpgdirheads = [x.dirhead for x in masterjpgfiles]
                posdirheads = [x.dirhead for x in masterposfiles]
                
                accessions = [x for x in xmlaccession \
                              if x in jpgaccession \
                              or x in posaccession]

                dirheads = [x for x in xmldirheads \
                            if x in jpgdirheads \
                            or x in posdirheads]
                
                pageob.accession = accessions[0]
                pageob.dirhead = dirheads[0]
                
                pageob.xml = xmlfiltered[0]
                pageob.jpg = jpgfiltered[0]
                pageob.ocr = posfiltered[0]
                n = self.extractMixData(n)
                pageob.tiff = n
                pages.append(pageob)

            self.identifier = identifier
            self.title = title
            self.date = date
            self.description = description
            self.representation = representation
            if self.new_dublincore:
                self.record = dirname(representation.filepath).split('/')[1]
                self.volume = dirname(representation.filepath).split('/')[2]
                self.issue = dirname(representation.filepath).split('/')[3]
            else:
                self.record = dublincoredirn.split('/')[1]
                self.volume = dublincoredirn.split('/')[2]
                self.issue = dublincoredirn.split('/')[3]
            self.textfile = textfile
            self.pages = pages
            self.createdate = representation.date
            self.accession = representation.accession
            self.dirhead = representation.dirhead
            self.valid = True
            
    def extractMetadata(self,mdobject):
        from xml.etree import ElementTree as ET
        from os.path import join
        xmlfile = join('/data/repository/ac/',mdobject.accession,mdobject.dirhead,mdobject.filepath)
        if not exists(xmlfile):
            stderr.write("%s does not exist\n" % xmlfile)
            return ("(:unac)","(:unac)","(:unac)","(:unac)")
        else:
            root = ET.parse(xmlfile).getroot()
            title = root.find('title').text
            description = root.find('description').text
            date = root.find('date').text
            identifier = root.find('identifier').text
            return (title,date,identifier,description)
        
    def extractMixData(self,tiff):
        from xml.etree import ElementTree as ET
        from os.path import join
        xmlfile = join('/data/repository/ac/',tiff.accession,tiff.dirhead,tiff.filepath+'.fits.xml')
        if exists(xmlfile):

            xmlfile = open(xmlfile)
        else:
            stderr.write("%s does not exists\n" % xmlfile)
            return tiff
        root = ET.parse(xmlfile).getroot()
        mixfilesize = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fileinfo/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}size').text
        setattr(tiff,'mixfilesize',mixfilesize)
        mixformatname = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}identification/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}identity').attrib['mimetype']
        setattr(tiff,'mixformatname',mixformatname)
        miximageheight = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageHeight').text
        setattr(tiff,'miximageheight',miximageheight)        
        miximagewidth = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageWidth').text
        setattr(tiff,'miximagewidth',miximagewidth)
        mixdigest =  root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fileinfo/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}md5checksum').text
        setattr(tiff,'mixdigest',mixdigest)
        mixdigestalgo = 'MD5'
        setattr(tiff,'mixdigestalgo',mixdigestalgo)        
        mixbitspersample = root.find('{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}bitsPerSample').text
        setattr(tiff,'mixbitspersample',mixbitspersample)
        return tiff

        
    def write(self,writeobj,counter):
        self.issueresourcemap(writeobj)
        counter.rems += 1
        self.issueprovidedcho(writeobj)
        counter.issueprovidedchos += 1
        self.issueaggregation(writeobj)
        counter.issueaggregations += 1
        self.issueproxy(writeobj)
        counter.issueproxies += 1
        self.issuewebresource(writeobj)
        counter.issuewebresources += 1
        prev = None
        for p in self.pages:
            tiffile = p.tiff
            jpegfile = p.jpg            
            self.pageprovidedcho(p,writeobj,prev)
            counter.pageprovidedchos += 1
            
            self.pageresourcemap(p,writeobj)
            counter.pagerems += 1
            
            self.pageaggregation(p,writeobj,tiffile,jpegfile)
            counter.pageaggregations += 1

            xmlfile = p.xml
            posfile = p.ocr
            self.pagetiffwebresource(p,writeobj,tiffile)
            counter.pagetiffresources += 1
            self.pagejpegwebresource(p,writeobj,jpegfile)
            counter.pagejpgresources += 1
            self.pagexmlwebresource(p,writeobj,xmlfile)
            counter.pagexmlresources += 1
            self.pageposwebresource(p,writeobj,posfile)
            counter.pageocrresources += 1
            prev = p
            
        return counter
    
    def issueproxy(self,writeobj):
        # start of issue proxy
        if self.new_dublincore:
            writeobj.write("<"+self.dublincore.accession+'/'+self.dublincore.dirhead+'/mvol/'+
                           self.record+'/'+self.volume+'/'+self.issue+'/'+
                           self.identifier+'.dc.xml>\n')                             
        else:
            writeobj.write("<"+self.dublincore.accession+'/'+self.dublincore.dirhead+
                           '/mvol/'+self.record+'/'+self.volume+'/'+self.issue+'/'+
                           self.identifier+'.dc.xml>\n')        
            
        writeobj.write("dc:format \"%s\";\n" % self.dublincore.mimetype)
        writeobj.write("ore:proxyFor <"+
                       self.accession+'/'+
                       self.dirhead+'/mvol/'+self.record+'/'+
                       self.volume+'/'+self.issue+'>;\n')
        writeobj.write("ore:proxyIn <"+
                       "/aggregation/"+self.accession+'/'+
                     self.dirhead+'/mvol/'+self.record+'/'+
                       self.volume+'/'+self.issue+'>;\n')
        writeobj.write("a ore:Proxy.\n\n")
        # end of issue proxy

    def issueprovidedcho(self,writeobj):
        # start of issue providedcho
        writeobj.write("<%s/%s/mvol/%s/%s/%s>\n" % (self.accession,self.dirhead,self.record,self.volume,self.issue))
        writeobj.write("dc:coverage \"Chicago\";\n")
        writeobj.write("dc:date \"%s\";\n" % self.date)
        writeobj.write("edm:year \"%s\";\n" % self.date[0:4])
        writeobj.write("dc:description \"%s\";\n"  % self.description)
        writeobj.write("dc:identifier \"%s\";\n" % self.identifier)
        writeobj.write("dc:language \"en\";\n")
        writeobj.write("dc:rights <http://createivecommons.org/licenses/by-nc/"+
                       "4.0/>;\n")
        writeobj.write("dc:title \"%s\";\n" % self.title)
        writeobj.write("dc:type \"text\";\n")
        writeobj.write("edm:type \"TEXT\";\n")        
        writeobj.write("dcterms:isPartOf <ead/ICU.SPCL.CAMPUB>;\n")
        for p in self.pages:
            writeobj.write('dcterms:hasPart <'+self.accession+'/'+
                           self.dirhead+'/mvol/'+self.record+'/'+
                           self.volume+'/'+self.issue+'/'+p.pagenum+'>;\n')
        writeobj.write("a edm:ProvidedCHO.\n\n")

        # end of issue providedcho
        
    def issueresourcemap(self,writeobj):
        # start of issue resourcemap

        writeobj.write('<'+self.accession+'/rem/'+
                       self.dirhead+'/'+'mvol/'+
                       self.record+'/'+self.volume+'/'+self.issue+'>\n')
        writeobj.write("dcterms:created \"%s\"^^xsd:dateTime;\n" \
                       % self.createdate.split('.')[0])
        writeobj.write("dcterms:creator <http://repository.lib.uchicago"+
        ".edu/>;\n")
        writeobj.write("ore:describes <"+
                       self.accession+'/aggregation/'+self.dirhead+'/'+
                       'mvol/'+self.record+'/'+self.volume+'/'+self.issue+'>;\n')
        writeobj.write('a ore:ResourceMap.\n\n')

        # end of issue resourcemap

    def issueaggregation(self,writeobj):
        # start of issue aggregation
        writeobj.write("<"+
                       "%s/aggregation/%s/mvol/%s/%s/%s>\n" % \
                       (self.accession,self.dirhead,self.record,
                        self.volume,self.issue))
        writeobj.write("edm:aggregatedCHO <"+
                       "%s/%s/mvol/%s/%s/%s>;\n" % \
                       (self.accession,self.dirhead,self.record,
                        self.volume,self.issue))
        writeobj.write("edm:dataProvider \"University of Chicago Library\";\n")
        writeobj.write("edm:isShownAt <http://pi.lib.uchicago.edu/1001/"+
                       "dig/campub/mvol-%s-%s-%s>;\n" % (self.record,self.volume,self.issue))
        writeobj.write("edm:isShownBy <"+
                       "%s/%s/mvol/%s/%s/%s/mvol-%s-%s-%s.pdf>;\n" % \
                       (self.representation.accession,
                        self.representation.dirhead,self.record,
                        self.volume,self.issue,self.record,self.volume,self.issue))

        jpgobject = [x for x in self.pages if int(x.displaypagenum)==1]
        if jpgobject:
            jpgobject = jpgobject[0].jpg
            writeobj.write("edm:object <%s/%s/%s>;\n" % (jpgobject.accession,jpgobject.dirhead,jpgobject.filepath))
        else:
            stderr.write("%s is missing a first page.\n" % join(self.record,self.volume,self.issue))
        writeobj.write("edm:provider \"University of Chicago Library\";\n")
        writeobj.write("edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
        writeobj.write('ore:isDescribedBy <%s/rem/%s/mvol/%s/%s/%s>;\n' % \
                       (self.accession,self.dirhead,self.record,self.volume,self.issue))
        writeobj.write("a ore:Aggregation.\n\n")

        # end of issue aggregation        

    def issuewebresource(self,writeobj):
        # start of issue webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/mvol-%s-%s-%s.pdf>\n" %
                       (self.accession,self.dirhead,self.record,self.volume,self.issue,self.record,self.volume,self.issue))
        writeobj.write('dcterms:isFormatOf <http://ldr.lib.uchicago.edu/%s/%s/mvol/%s/%s/%s>;\n' %
                       (self.accession,self.dirhead,self.record,self.volume,self.issue))
        writeobj.write("dc:format \"\"\"%s\"\"\";\n" % self.representation.mimetype)
        writeobj.write("premis:objectIdentifierType \"ARK\";\n")
        writeobj.write("premis:objectIdentifierValue <%s/%s/mvol/%s/%s/%s/mvol-%s-%s-%s.pdf>;\n" %
                       (self.accession,self.dirhead,self.record, self.volume, self.issue, self.record,self.volume,self.issue))
        writeobj.write("premis:objectCategory \"file\";\n")
        writeobj.write("premis:compositionLevel 0;\n")
        writeobj.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
        writeobj.write("premis:messageDigest \"%s\";\n" % self.representation.checksum)
        writeobj.write("premis:messageDigestOriginator \"/sbin/sha256\";\n")
        writeobj.write("premis:size %s;\n" % self.representation.filesize)
        writeobj.write("premis:formatName \"application/pdf\";\n")
        writeobj.write("premis:originalName \"%s.pdf\";\n" % self.identifier)
        writeobj.write("premis:eventIdentifierType \"ARK\";\n")
        writeobj.write("premis:eventIdentifierValue \"%s\";\n" % self.representation.accession) 
        writeobj.write("premis:eventType \"creation\";\n")
        writeobj.write("premis:eventDateTime \"%s\"^^xsd:dateTime;\n" % self.representation.date.split('.')[0])
        writeobj.write("a edm:WebResource.\n\n")

        # end of issue webresource        


    def pageprovidedcho(self,p,writeobj,prev):
        writeobj.write("<"+
                       p.accession+'/'+
                       p.dirhead+'/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/'+
                       str(p.pagenum)+'>\n')
        writeobj.write("dc:description <"+
                       self.accession+'/'+
                       self.dirhead+'/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/pos/'+
                       str(p.pagenum) +'.pos>;\n')
        writeobj.write("dc:description <"+
                       self.accession+'/'+
                       self.dirhead+
                       '/mvol/'+
                       self.record+'/'+
                       self.volume+'/'+
                       self.issue+'/xml/'+
                       str(p.pagenum)+'.xml>;\n')
        writeobj.write("dc:language \"en\";\n")
        writeobj.write("dc:rights <http://creativecommons.org/"+
                       "licenses/by-nc/4.0/>;\n")
        writeobj.write("dc:type \"Text\";\n")
        writeobj.write("edm:type \"TEXT\";\n")
        writeobj.write("dc:title \"Page %s\";\n" % p.displaypagenum)
        writeobj.write("dcterms:isPartOf <"+
                       self.accession+
                       '/'+self.dirhead+'/mvol/'+
                       self.volume+'/'+self.record+'/'+self.issue+'>;\n')
        if not prev:
            pass
        else:
            writeobj.write("edm:isNextInSequence <"+ \
                         "%s/%s/mvol/%s/%s/%s/%s>;\n" % \
                         (prev.accession, prev.dirhead, self.record,
                          self.volume, self.issue, str(prev.pagenum)))
        writeobj.write("a edm:ProvidedCHO.\n\n")

    def pageresourcemap(self,p,writeobj):
        # start of page resourcemap
        writeobj.write("<"+
                     p.accession+"/rem/"+
                     p.dirhead+"/"+
                     self.record+"/"+
                     self.volume+"/"+
                     self.issue+"/"+
                     str(p.pagenum)+">\n")
        writeobj.write('dcterms:created \"%s\"^^xsd:dateTime;\n' \
                     % self.createdate.split('.')[0])
        writeobj.write('dcterms:creator <http://repository.lib.uchicago.edu/>;\n')
        writeobj.write("ore:describes <"+
        "%s/aggregation/%s/mvol/%s/%s/%s/%s>;\n" %\
                     (self.accession, self.dirhead, self.record,
                      self.volume, self.issue, str(p.pagenum)))
        writeobj.write('a ore:ResourceMap.\n\n')
        # end of page resourcemap

    def pageaggregation(self,p,writeobj,tiff,jpeg):
            # start of page aggregation
            writeobj.write("<"+
                         "%s/aggregation/%s/mvol/%s/%s/%s/%s>\n" % \
                         (p.accession,p.dirhead,self.record,
                          self.volume,self.issue,str(p.pagenum)))
            writeobj.write("edm:aggregatedCHO <"+
            "%s/%s/mvol/%s/%s/%s/%s>;\n" % \
                         (self.accession, self.dirhead, self.record,
                          self.volume, self.issue, p.pagenum))
            writeobj.write('edm:dataProvider \"University of Chicago'+
            ' Library\";\n') 
            writeobj.write("edm:isShownBy <"+
                         "%s/%s/mvol/%s/%s/%s/tif/%s.tif>;\n" % \
                         (tiff.accession,tiff.dirhead,self.record,
                          self.volume,self.issue,p.pagenum))
            writeobj.write("edm:object <"+
                         "%s/%s/mvol/%s/%s/%s/jpg/%s.jpg>;\n" % \
                         (jpeg.accession,jpeg.dirhead,self.record,
                          self.volume,self.issue,p.pagenum))
            writeobj.write('edm:provider \"University of Chicago Library\";\n')
            writeobj.write('edm:rights <http://creativecommons.org/'+
            'licenses/by-nc/4.0/>;\n')
            writeobj.write("ore:isDescribedBy <"+
            "%s/rem/%s/mvol/%s/%s/%s/%s>;\n" % \
                         (self.accession,self.dirhead,self.record,
                          self.volume,self.issue,p.pagenum))
            writeobj.write("a ore:Aggregation.\n\n")
            # end of page aggregation

    def pagetiffwebresource(self,p,writeobj,tfile):
        # start of tif file edm:webresource

        writeobj.write("<%s/%s/mvol/%s/%s/%s/tif/%s.tif>\n" % \
                     (tfile.accession,tfile.dirhead,
                      self.record,self.volume,self.issue,p.pagenum))
        try:
            writeobj.write("mix:fileSize %s;\n" % tfile.mixfilesize)
            writeobj.write("mix:formatName \"%s\";\n" % tfile.mixformatname)
            writeobj.write("mix:messageDigestAlgorithm \"%s\";\n" % tfile.mixdigestalgo)
            writeobj.write("mix:messageDigest \"%s\";\n" % tfile.mixdigest)
            writeobj.write("mix:imageWidth %s;\n" % tfile.miximagewidth)
            writeobj.write("mix:imageHeight %s;\n" % tfile.miximageheight)
            writeobj.write("mix:bitsPerSampleUnit \"\"\"%s\"\"\";\n" % tfile.mixbitspersample)
        except:
            pass
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write('premis:objectIdentifierType \"ARK\";\n')
        writeobj.write("premis:objectIdentifierValue"+
        " <%s/%s/%s>;\n" \
                     % (tfile.accession, tfile.dirhead, tfile.filepath))
        writeobj.write('premis:objectCategory \"file\";\n')
        writeobj.write('premis:compositionLevel 0;\n')
        writeobj.write('premis:messageDigestAlgorithm \"SHA-256\";\n')
        writeobj.write('premis:messageDigest \"%s\";\n' % tfile.checksum)
        writeobj.write('premis:messageDigestOriginator \"/sbin/sha256\";\n')
        writeobj.write('premis:size %s;\n' % tfile.filesize)
        writeobj.write('premis:formatName \"%s\";\n' % tfile.mimetype)
        writeobj.write('premis:originalName \"%s\";\n' % \
                     basename(tfile.filepath))
        writeobj.write('premis:eventIdentifierType \"ARK\";\n')
        writeobj.write('premis:eventIdentifierValue \"%s\";\n' % tfile.accession)
        writeobj.write('premis:eventType \"creation\";\n')
        writeobj.write('premis:eventDateTime \"%s\"^^xsd:dateTime;\n' % \
                     tfile.date.split('.')[0])
        writeobj.write('a edm:WebResource.\n\n')

        # end of tif file edm:webresource

    def pagejpegwebresource(self,p,writeobj,tfile):
        from os.path import basename
        # start of jpeg file rdfs:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/jpg/%s.%s>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum,
                      basename(tfile.filepath).split('.')[1]))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write("a edm:WebResource.\n\n")

        # end of jpeg file rdfs:webresource

    def pagexmlwebresource(self,p,writeobj,tfile):
        # start of pos file rdfs:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/xml/%s.%s>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum,
                      basename(tfile.filepath).split('.')[1]))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write("a rdfs:Resource.\n\n")

        # end of pos file rdfs:webresource

    def pageposwebresource(self,p,writeobj,tfile):
        # start of pos file rdfs:webresource
        writeobj.write("<%s/%s/mvol/%s/%s/%s/pos/%s.%s>\n" % \
                     (tfile.accession,
                      tfile.dirhead,
                      self.record,
                      self.volume,
                      self.issue,
                      p.pagenum,
                      basename(tfile.filepath).split('.')[1]))
        writeobj.write('dc:format \"%s\";\n' % tfile.mimetype)
        writeobj.write("a rdfs:Resource.\n\n")

        # end of pos file rdfs:webresource
