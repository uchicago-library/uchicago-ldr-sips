from os.path import basename, join, splitext
from sys import stdout, stderr

def sip_creation(id_parts, file_list, creationdate):
    id_directory = '/'.join(id_parts)
    id_filename = '-'.join(id_parts)
    base_url = join(id_directory,id_filename)
    metsfile = [x for x in file_list \
                if x.canonical_filepath.endswith(".mets.xml")][0]
    dcfile = [x for x in file_list \
              if x.canonical_filepath.endswith(".dc.xml")][0]
    pdffile = [x for x in file_list \
               if x.canonical_filepath.endswith(".pdf")][0]
    xmllist = [x for x in file_list if '/ALTO/' in x.canonical_filepath]
    jpglist = [x for x in file_list if '/JPEG/' in x.canonical_filepath]
    tifflist = [x for x in file_list if '/TIFF/' in x.canonical_filepath]
    
    last_page = [basename(splitext(x.canonical_filepath)[0]).split('_')[1] for x in tifflist]
    last_page = int(last_page[-1].lstrip('0'))
    rem_url = join('rem', id_directory)
    providedcho_url = join(id_directory)
    aggregation_url = join('aggregation', id_directory)
    metsxml_url = join(base_url+'.mets.xml')
    pdf_url = join(base_url+'.pdf')
    dcxml_url = join(base_url+'.dc.xml')

    stdout.write("<{url}>\n".format(url = providedcho_url))
    stdout.write("dc:coverage \"Chicago\";\n")
    stdout.write("dc:date \"{date}\";\n".\
                 format(date = dcfile.date))
    stdout.write("edm:year \"\"\"{year}\"\"\";\n". \
                 format(year = dcfile.date.split('-')[0]))
    stdout.write("dc:description \"{description}\";\n". \
                 format(description = dcfile.description))
    stdout.write("dc:identifier \"%s\";\n" % id_filename)
    stdout.write("dc:language \"en\";\n")
    stdout.write("dc:rights <http://createivecommons.org/licenses/by-nc/"+
                   "4.0/>;\n")
    stdout.write("dc:title \"{title}\";\n". \
                 format(title = dcfile.title))
    stdout.write("dc:type \"text\";\n")
    stdout.write("edm:type \"TEXT\";\n")        
    stdout.write("dcterms:isPartOf <ead/ICU.SPCL.CAMPUB>;\n")
    for n in xmllist:
        b = splitext(basename(n.canonical_filepath))[0]
        page_base_url = join(id_directory, b)
        stdout.write("dcterms:hasPart <{url}>;\n". \
                     format(url = page_base_url))
    stdout.write("a edm:ProvidedCHO.\n\n")

    stdout.write("<{url}>\n".format(url = aggregation_url))
    stdout.write("edm:aggregatedCHO <{providedchourl}>;\n". \
                 format(providedchourl = providedcho_url))
    stdout.write("edm:dataProvider \"University of Chicago Library\";\n")
    stdout.write("edm:isShownAt <http://pi.lib.uchicago.edu/1001/"+
        "dig/campub/{identifier}>;\n". \
                 format(identifier = id_filename))
    stdout.write("edm:isShownBy <{accession}/{dirhead}/{pdf_url}>;\n". \
                 format(accession = pdffile.accession,
                        dirhead = pdffile.dirhead,
                        pdf_url = pdffile.canonical_filepath))


    filtered_list = [x for x in jpglist if '_0001.jpg' in x.canonical_filepath]
    if len(filtered_list) == 0:
        stderr.write("could not find first page jpeg file in file list\n")
    else:
        stdout.write("edm:object <{accession}/{dirhead}/{object_url}>;\n". \
                     format(object_url = filtered_list[0].canonical_filepath,\
                            accession = filtered_list[0].accession,
                            dirhead = filtered_list[0].dirhead))
    stdout.write("edm:provider \"University of Chicago Library\";\n")
    stdout.write("edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
    stdout.write("ore:isDescribedBy <{remurl}>;\n". \
                 format(remurl = rem_url))
    stdout.write("a ore:Aggregation.\n\n")

    stdout.write("<{url}>\n".format( url = rem_url))
    stdout.write("dcterms:created \"{creationdate}\"^^xsd:dateTime;\n". \
                 format(creationdate = creationdate))
    stdout.write("dcterms:creator <http://repository.lib.uchicago.edu/>;\n")
    stdout.write("ore:describes <{aggurl}>;\n". \
                 format(aggurl = aggregation_url))
    stdout.write("a ore:ResourceMap.\n\n")

    stdout.write("<{dcurl}>\n".format(dcurl = join(dcfile.accession,
                                                   dcfile.dirhead,
                                                   dcxml_url)))
    stdout.write("dc:format \"{mimetype}\";\n". \
                 format(mimetype = dcfile.mimetype))
    stdout.write("ore:proxyFor <{providedchourl}>;\n". \
                 format(providedchourl = providedcho_url))
    stdout.write("ore:proxyIn <{aggregationurl}>;\n". \
                 format(aggregationurl = aggregation_url))
    stdout.write("a ore:Proxy.\n\n")


    stdout.write("<{pdfurl}>\n".format(pdfurl = join(pdffile.accession,
                                                     pdffile.dirhead,
                                                     pdf_url)))
    stdout.write("dcterms:isFormatOf <{formatofurl}>;\n". \
                 format(formatofurl = 'http://ldr.lib.uchicago.edu/'+ \
                        join(pdffile.accession, pdffile.dirhead, 
                             providedcho_url)))
    stdout.write("dc:format \"{mimetype}\";\n". \
                 format(mimetype = pdffile.mimetype))
    stdout.write("premis:objectIdentifierType \"ARK\";\n")
    stdout.write("premis:objectIdentifierValue <{accession}/{dirhead}/{pdfurl}>;\n". \
                 format(accession = pdffile.accession,
                        dirhead = pdffile.dirhead,
                        pdfurl = pdffile.canonical_filepath))
    stdout.write("premis:objectCategory \"file\";\n")
    stdout.write("premis:compositionLevel 0;\n")
    stdout.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
    stdout.write("premis:messageDigest \"{checksum}\";\n". \
                 format(checksum = pdffile.checksum))
    stdout.write("premis:messageDigestOriginator \"/sbin/sha256\";\n")
    stdout.write("premis:size {filesize};\n". \
                 format(filesize = pdffile.filesize))
    stdout.write("premis:formatName \"{mime}\";\n". \
                 format(mime = pdffile.mimetype))
    stdout.write("premis:originalName \"{bname}\";\n". \
                 format(bname = basename(pdffile.canonical_filepath)))
    stdout.write("premis:eventIdentifierType \"ARK\";\n")
    stdout.write("premis:eventIdentifierValue \"{eventValue}\";\n". \
                 format(eventValue = pdffile.accession))
    stdout.write("premis:eventType \"creation\";\n")
    stdout.write("premis:eventDateTime \"{cdate}\"^^xsd:dateTime;\n". \
                 format(cdate = pdffile.createdate))
    stdout.write("a edm:WebResource.\n\n")

    stdout.write("<{metsurl}>\n".format(metsurl = join(metsfile.accession,
                                                       metsfile.dirhead,
                                                       metsxml_url)))
    stdout.write("dc:format \"{mimetype}\";\n". \
                 format(mimetype = metsfile.mimetype))
    stdout.write("a rdfs:Resource.\n\n")
    
    for n in xmllist:
        b, extension = splitext(basename(n.canonical_filepath))
        page_base_url = join(id_directory, b)
        page_aggregation_url = join('aggregation', page_base_url)
        page_rem_url = join('rem', page_base_url)
        page_proxy_url = page_base_url
        jpeg_file = [x for x in jpglist if b in x.canonical_filepath][0]
        tiff_file =  [x for x in tifflist if b in x.canonical_filepath][0]

        stdout.write("<{url}>\n".format(url = page_base_url))
        stdout.write("dc:description <{accession}/{dirhead}/{xmlurl}>;\n". \
                     format(accession = n.accession, dirhead = n.dirhead,
                            xmlurl = n.canonical_filepath))
        stdout.write("dc:language \"en\";\n")
        stdout.write("dc:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
        stdout.write("dc:type \"Text\";\n")
        stdout.write("edm:type \"TEXT\";\n")
        stdout.write("dc:title \"Page {number}\";\n". \
                     format(number = str(b.split('_')[1].lstrip('0'))))
        stdout.write("dcterms:isPartOf <{providedchourl}>;\n". \
                     format(providedchourl = providedcho_url))
        
        next_page = int(b.split('_')[1].lstrip('0')) + 1
        if int(b.split('_')[1].lstrip('0')) == last_page:
            zeroes_needed = 4-len(str(next_page))
            next_page_id = '0'*zeroes_needed+str(next_page)
            next_page_filepath = base_url+'_'+next_page_id
            stdout.write("edm:isNextInSequence <{nextpage}>;\n". \
                         format(nextpage = str(next_page_filepath)))
        stdout.write("a ore:ProvidedCHO.\n\n")

        stdout.write("<{url}>\n".format(url = page_rem_url))
        stdout.write("dcterms:created \"\"\"{created}\"\"\"^^xsd:dateTime;\n". \
                     format(created = creationdate))
        stdout.write("dcterms:creator <http://repository.lib.uchicago.edu/>;\n")
        stdout.write("ore:describes <{providedchourl}>;\n". \
                     format(providedchourl = page_base_url))
        stdout.write("a ore:ResourceMap.\n\n")

        stdout.write("<{url}>\n".format(url = page_aggregation_url))
        stdout.write("edm:aggregatedCHO <{page_providedcho_url}>;\n". \
                     format(page_providedcho_url = page_base_url))
        stdout.write("edm:dataProvider \"University of Chicago Library\";\n")
        stdout.write("edm:isShownBy <{accession}/{dirhead}/{tiffurl}>;\n". \
                     format(accession = tiff_file.accession,
                            dirhead = tiff_file.dirhead,
                            tiffurl = tiff_file.canonical_filepath))
        stdout.write("edm:object <{accession}/{dirhead}/{jpegurl}>;\n". \
                     format(accession = jpeg_file.accession,
                            dirhead = jpeg_file.dirhead,
                            jpegurl = jpeg_file.canonical_filepath))
        stdout.write('edm:provider \"University of Chicago Library\";\n')
        stdout.write('edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n')
        stdout.write("ore:isDescribedBy <{remurl}>;\n". \
                     format(remurl = page_rem_url))
        stdout.write("a ore:Aggregation.\n\n")

        stdout.write("<{accession}/{dirhead}/{url}>\n". \
                     format(accession = n.accession,
                            dirhead = n.dirhead,
                            url = n.canonical_filepath))
        stdout.write("dc:format \"{mimetype}\";\n".format(mimetype = n.mimetype))
        stdout.write("a rdfs:Resouce.\n\n")


        stdout.write("<{accession}/{dirhead}/{url}>\n". \
                     format(accession = jpeg_file.accession,
                            dirhead = jpeg_file.dirhead,
                            url = jpeg_file.canonical_filepath))
        stdout.write("dc:format \"{mimetype}\";\n".format(mimetype = jpeg_file.mimetype))
        stdout.write("a rdfs:Resource.\n\n")

        stdout.write("<{accession}/{dirhead}/{url}>\n". \
                     format(accession = tiff_file.accession,
                            dirhead = tiff_file.dirhead,
                            url = tiff_file.canonical_filepath))
        stdout.write("mix:fileSize {filesize};\n". \
                     format(filesize = tiff_file.filesize))
        stdout.write("mix:formatName \"\"\"{mimetype}\"\"\";\n". \
                     format(mimetype = tiff_file.mimetype))
        if getattr(n, 'mixchecksum', None):
            stdout.write("mix:messageDigestAlgorithm \"MD5\";\n")
            stdout.write("mix:messageDigest \"\"{mixchecksum}\"\"\";\n". \
                         format(mixchecksum = tiff_file.mixchecksum))
        if getattr(n, 'imagewidth', None):
            stdout.write("mix:imageWidth {imagewidth};\n". \
                         format(imagewidth = tiff_file.imagewidth))
        if getattr(n, 'imageheight', None):
            stdout.write("mix:imageHeight {imageheight};\n". \
                         format(imageheight = tiff_file.imageheight))
        if getattr(n, 'bitspersample', None):
            stdout.write("mix:bitsPerSampleUnit \"\"\"{bitspersample}\"\"\";\n". \
                         format(bitspersample = tiff_file.bitspersample))
        stdout.write("dc:format \"{mimetype}\";\n". \
                     format(mimetype = tiff_file.mimetype))
        stdout.write("premis:objectIdentifierType \"ARK\";\n")
        stdout.write("premis:objectIdentifierValue <{accession}/{dirhead}/{tiffurl}>;\n". \
                     format(accession = tiff_file.accession,
                            dirhead = tiff_file.dirhead,
                            tiffurl = tiff_file.canonical_filepath))
        stdout.write("premis:objectCategory \"file\";\n")
        stdout.write("premis:compositionLevel 0;\n")
        stdout.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
        stdout.write("premis:messageDigest \"{checksum}\";\n". \
                     format(checksum = tiff_file.checksum))
        stdout.write("premis:messageDigestOriginator \"/sbin/sha256\";\n")
        stdout.write("premis:size {filesize};\n". \
                     format(filesize = tiff_file.filesize))
        stdout.write("premis:formatName \"{mimetype}\";\n". \
                     format(mimetype = tiff_file.mimetype))
        stdout.write("premis:originalName \"{bname}\";\n". \
                     format(bname = basename(tiff_file.canonical_filepath)))
        stdout.write('premis:eventIdentifierType \"ARK\";\n')
        stdout.write("premis:eventIdentifierValue \"{accession}\";\n". \
                     format(accession = tiff_file.accession))
        stdout.write("premis:eventType \"creation\";\n")
        stdout.write("premis:eventDateTime \"{createdate}\"^^xsd:dateTime;\n". \
                     format(createdate = tiff_file.createdate))
        stdout.write("a edm:WebResource.\n\n")

        stdout.write("<{accession}/{dirhead}/{url}>\n". \
                     format(accession = n.accession,
                            dirhead = n.dirhead,
                            url = n.canonical_filepath))
        stdout.write("dc:format \"\"\"{mimetype}\"\"\";\n". \
                     format(mimetype = n.mimetype))
        stdout.write("a rdfs:Resource.\n\n")
