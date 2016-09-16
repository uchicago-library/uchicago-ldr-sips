from datetime import datetime
from collections import OrderedDict
from os import _exit
from os.path import basename
import json
import re
from xml.etree import ElementTree
from sys import stdout


def merge_pages_into_compound(compound_dict, pages_dict):
    for issue_number, page_info in pages_dict.items():
        if compound_dict.get(issue_number):
            compound_dict[issue_number]['pages'] = page_info['pages']
    return compound_dict


def sort_pages(*args):
    """
    fill_in_please
    """

    def add_a_thing_to_an_object(a_dict, part_name, a_bytestream):
        """
        fill_in_please
        """
        if page_dict.get(part_name) is not None:
            page_dict[part_name].append(a_bytestream)
        else:
            page_dict[part_name] = [a_bytestream]

    def get_new_page_number(a_file_name):
        """
        fill_in_please
        """
        return a_file_name.split('_')[1].split('.')[0]

    def get_old_page_number(a_file_name):
        """
        fill_in_please
        """
        return a_file_name.split('.')[0]

    the_dict = args[0]
    the_id = args[1]
    spec_type = args[2]
    tail = args[3:]
    if the_dict.get(the_id) is not None:
        relevant = the_dict.get(the_id).get('pages')
        print(relevant)
    else:
        the_dict[the_id] = {'pages':{}}
        relevant = the_dict.get(the_id).get('pages')
    for a_list in tail:
        for b_dict in a_list:
            if spec_type == 'new':
                orig_file_name = basename(b_dict['origin'])
                page_number = get_new_page_number(basename(orig_file_name))
            elif spec_type == 'old':
                page_number = get_old_page_number(basename(b_dict['origin']))
            if relevant.get(page_number):
                count = relevant.get(page_number)
                page_dict = relevant.get(page_number)
            else:
                relevant[page_number] = {} 
                page_dict = relevant[page_number]
            orig = b_dict['origin']
            dest = b_dict['dst']
            answer = {'origin':orig, 'dst':dest}
            if 'alto' in orig.lower():
                add_a_thing_to_an_object(page_dict, 'alto', answer)
            elif 'tif' in orig.lower():
                add_a_thing_to_an_object(page_dict, 'tif', answer)
            elif 'pos' in orig.lower():
                add_a_thing_to_an_object(page_dict, 'pos', answer)
            elif 'jpg' in orig.lower():
                add_a_thing_to_an_object(page_dict, 'jpg', answer)
            elif '/xml/' in orig.lower():
                add_a_thing_to_an_object(page_dict, 'xml', answer)
    return the_dict


def create_or_append(a_dict, key, subkey, value):
    """
    fille_in_please
    """
    print(a_dict)
    print(key)
    print(value)
    if a_dict.get(key) is None:
        a_dict[key] = {'dc': [], 'pdf': [],
                       'tiff': [], 'jpeg': [],
                       'xml': [], 'alto': [],
                       'pos': []}
        a_dict[key][subkey] = [value]
    elif a_dict[key].get(subkey) == []:
        a_dict[key][subkey] = [value]
    else:
        a_dict[key][subkey].append(value)


def generate_page_dict(compound_objects):
    """
    fill_in_please
    """
    pages = {}
    for key in compound_objects:
        an_obj = compound_objects.get(key)
        if an_obj.get('alto') and an_obj.get('tif') and an_obj.get('jpg'):
            sort_pages(pages,
                       key,
                       'new',
                       an_obj.get('alto'),
                       an_obj.get('jpg'),
                       an_obj.get('tif'))
        else:
            sort_pages(pages,
                       key,
                       'old',
                       an_obj.get('jpg'),
                       an_obj.get('xml'),
                       an_obj.get('pos'),
                       an_obj.get('tif'))
    return pages


def get_pattern_match_result(a_string, pattern_string):
    """
    fill_in_please
    """
    pattern = re.compile(pattern_string).search(a_string)
    match = a_string[pattern.start():pattern.end()]
    return match

def bytestream_switch(path_string, directory_path, a_bytestream):
    pot_string = a_bytestream['origin']
    lowercase_string = pot_string.lower()
    if pot_string.startswith(dirified):
        if 'tif' in lowercase_string:
            compound_objects = add_a_thing_to_an_object(dirified, 
                                                        'tif',
                                                        b_bytestream)
        elif 'jpg' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(dirified,
                                                    'jpg',
                                                    b_bytestream)
        elif 'pos' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'pos', b_bytestream)
        elif 'alto' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'alto', b_bytestream)
        elif 'pdf' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'pdf', b_bytestream)
        elif 'struct' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'struct', b_bytestream)
        elif 'txt' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'txt', b_bytestream)
        elif 'mets' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'mets', b_bytestream)
        elif 'premis' in lowercase_string:
        pass
        elif '/xml/' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'xml', b_bytestream)
        elif 'dc.xml' in lowercase_string:
        compound_objects = add_a_thing_to_an_object(
            dirified, 'dc', b_bytestream)
        else:
            stderr.write("no matching pattern in {}\n".format(pot_string))
        
    else:
        stderr.write("{} doesn't match the directory id {}.\n".format(
            path_string,
            directory_path))

def arrange_bytestreams():
    """
    fill_in_please
    """
    def add_a_thing_to_an_object(object_id, part_name, a_bytestream):
        """
        fill_in_please
        """
        if compound_objects.get(object_id) is not None:
            an_object = compound_objects.get(object_id)
            object_part = an_object.get(part_name)
            if object_part is not None:
                object_part.append(a_bytestream)
            else:
                rel_record[part_name] = [a_bytestream]
        else:
            compound_objects[object_id] = {part_name: [a_bytestream]}
        return compound_objects

    manifest_file = "data_manifest.json"
    issue_file = "mvol-0001.csv"
    issues = open(issue_file, 'r').readlines()[1:]
    issues = [x.split(',')[2] for x in issues]
    data = None
    with open(manifest_file, 'r') as a_file:
        data = json.load(a_file)
    compound_objects = {}
    bytestreams = [x['bytestreams'] for x in data['objs']]
    all_bytestreams = []
    for n_bytestream in bytestreams:
        all_bytestreams.extend(n_bytestream)
    for n_issue in issues:
        dirified = n_issue.replace('-', '/')
        for b_bytestream in all_bytestreams:
            pot_string = b_bytestream['origin']
            if pot_string.startswith(dirified):
                lowercase_string = pot_string.lower()
                rel_record = compound_objects.get(dirified)
                if 'tif' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'tif', b_bytestream)
                elif 'jpg' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'jpg', b_bytestream)
                elif 'pos' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'pos', b_bytestream)
                elif 'alto' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'alto', b_bytestream)
                elif 'pdf' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'pdf', b_bytestream)
                elif 'struct' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'struct', b_bytestream)
                elif 'txt' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'txt', b_bytestream)
                elif 'mets' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'mets', b_bytestream)
                elif 'premis' in lowercase_string:
                    pass
                elif '/xml/' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'xml', b_bytestream)
                elif 'dc.xml' in lowercase_string:
                    compound_objects = add_a_thing_to_an_object(
                        dirified, 'dc', b_bytestream)
                else:
                    pass
            else:
                pass
    return compound_objects


def make_sip_url(path_string):
    """
    fill_in_please
    """
    url_origin = path_string
    url_list = url_origin.split('/')
    first_arf_after_ar = url_list[:12].index('ar')
    first_arf = url_list[:12][first_arf_after_ar + 1:]
    second_arf_whole = url_list[12:]
    second_arf_pairtreeroot_pos = url_list[12:].index('pairtree_root')
    second_arf = second_arf_whole[second_arf_pairtreeroot_pos + 1:]
    second_arf_arf_pos = second_arf.index('arf')
    second_arf = second_arf[:second_arf_arf_pos]
    first_arf = ''.join(first_arf)
    second_arf = ''.join(second_arf)
    url = first_arf + "/" + second_arf
    return url


def sip_generation(mega_object):
    """
    fill_in_please
    """
    a_file_to_write = "mvol-0001.ttl"
    a_file_to_write_opened = open(a_file_to_write, 'a')
    a_file_to_write_opened.write("@prefix edm: <http://www.europeana.eu/schemas/edm/>.\n")
    a_file_to_write_opened.write("@prefix dc: <http://purl.org/dc/elements/1.1/>.\n")
    a_file_to_write_opened.write("@prefix erc: <http://purl.org/kernel/elements/1.1/>.\n")
    a_file_to_write_opened.write("@prefix dcterms: <http://purl.org/dc/terms/>.\n")
    a_file_to_write_opened.write("@prefix foaf: <http://xmlns.com/foaf/0.1/>.\n")
    a_file_to_write_opened.write("@prefix mix: <http://www.loc.gov/mix/v20>.\n")
    a_file_to_write_opened.write("@prefix oai: <http://www.openarchives.org/OAI/2.0/>.\n")
    a_file_to_write_opened.write("@prefix owl: <http://www.w3.org/2002/07/owl#>.\n")
    a_file_to_write_opened.write("@prefix ore: <http://www.openarchives.org/ore/terms/>.\n")
    a_file_to_write_opened.write("@prefix premis: <info:lc/xmlns/premis-v2>.\n")
    a_file_to_write_opened.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n")
    a_file_to_write_opened.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n")
    a_file_to_write_opened.write("@prefix skos: <http://www.w3.org/2004/02/skos/core#>.\n")
    a_file_to_write_opened.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n")
    a_file_to_write_opened.write("@base <http://ark.lib.uchicago.edu/ark:/61001/>.\n")

    for issue_num, issue_dict in mega_object.items():

        id_parts = issue_num.split('/')
        collection_id_parts = id_parts[0:2]
        collection_id = '-'.join(collection_id_parts)
        handle_id = '-'.join(id_parts)

        issue_rem_url = "mvol-0001/rem/"+issue_num
        issue_aggregation_url = "mvol-0001/aggregation/"+issue_num
        issue_providedcho_url = 'mvol-0001/'+issue_num
      
        a_file_to_write_opened.write("\n") 
        a_file_to_write_opened.write("<" + issue_rem_url + ">\n")
        a_file_to_write_opened.write("dcterms:creator <http://repository.lib.uchicago.edu/>;\n")
        a_file_to_write_opened.write("dcterms:created \"" + datetime.now().isoformat().split('.')[0]+"\"^^xsd:dateTime;\n")
        a_file_to_write_opened.write("dcterms:describes "+ "<" + issue_aggregation_url+">;\n")
        a_file_to_write_opened.write("a ore:ResourceMap.\n\n")
        
        a_file_to_write_opened.write("<" + issue_aggregation_url+">\n")
        a_file_to_write_opened.write("edm:aggregatedCHO " + "<" + issue_providedcho_url+">;\n")
        a_file_to_write_opened.write("edm:dataProvider \"University of Chicago Library\";\n") 
        a_file_to_write_opened.write("edm:isShownAt <http://pi.lib.uchicago.edu/1001/dig/campub/" + handle_id + ">;\n")
       
        test = [x['origin'] for x in mega_object[issue_num]['pdf'] if x['origin'].endswith('pdf')]
        first_page_jpg = [mega_object[issue_num]['pages'][x]['jpg'][0] for x in mega_object[issue_num]['pages'] if x.lstrip('0') == '1'][0]['origin']
        
        a_file_to_write_opened.write("edm:isShownBy <mvol-0001/" + test[0]+ ">;\n")
        a_file_to_write_opened.write("edm:object <" + first_page_jpg + ">;\n")
        a_file_to_write_opened.write("edm:provider \"University of Chicago Library\";\n")
        a_file_to_write_opened.write("edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
        a_file_to_write_opened.write("ore:isDescribedBy " + "<" + issue_rem_url+">;\n")
        a_file_to_write_opened.write("a ore:Aggregation.\n\n")
       
        for part, part_dict in issue_dict.items():
            if part == 'pdf':
                for p in part_dict:
                    if p['origin'].endswith('pdf'):

                        premis_path = p['dst'].replace('content.file','premis.xml')

                        with open(premis_path, 'r') as premis_file:
                            tree = ElementTree.parse(premis_file)
                        root = tree.getroot()
                        objId = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectIdentifier/{http://www.loc.gov/premis/v3}objectIdentifierValue")
                        objIdType = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectIdentifier/{http://www.loc.gov/premis/v3}objectIdentifierType")
                       
                        fixities = root.findall("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}fixity")

                        sha256_messageDigest = None
                        md5_messageDigest = None
                        for n_fixity in fixities:
                            n_algo = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigestAlgorithm").text
                            if n_algo == 'sha256':
                                sha256_messageDigest = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigest")
                            elif n_algo == 'md5':
                                md5_messageDigest = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigest")
                        
                        size = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}size")

                        mimetype = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}format/{http://www.loc.gov/premis/v3}formatDesignation/{http://www.loc.gov/premis/v3}formatName")


                        old_filepath = p['origin']
                        pdf_url = "<mvol-0001/"+p['origin']+">"
                        a_file_to_write_opened.write(pdf_url+"\n")
                        a_file_to_write_opened.write("dc:format \"{}\";\n".format(mimetype.text))
                        a_file_to_write_opened.write("mix:messageDigestAlgorithm \"MD5\";\n")
                        a_file_to_write_opened.write("mix:messageDigest \"{}\";\n".format(md5_messageDigest.text))
                        a_file_to_write_opened.write("premis:messageDigestOriginator \"hashlib.md5\";\n")
                        a_file_to_write_opened.write("dcterms:isFormatOf " + "<" + issue_providedcho_url + ">;\n")
                        a_file_to_write_opened.write("premis:objectIdentifierType \"ARK\";\n")
                        a_file_to_write_opened.write("premis:objectIdentifierValue <mvol-0001/" + p['origin'] + ">;\n")
                        a_file_to_write_opened.write("premis:objectCategory \"file\";\n") 
                        a_file_to_write_opened.write("premis:compositionLevel 0;\n")
                        a_file_to_write_opened.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
                        a_file_to_write_opened.write("premis:messageDigest \"" + sha256_messageDigest.text + "\";\n")
                        a_file_to_write_opened.write("premis:messageDigestOriginator \"hashlib.sha256\";\n")
                        a_file_to_write_opened.write("premis:size " + size.text + ";\n")
                        a_file_to_write_opened.write("premis:formatName \"{}\";\n".format(mimetype.text))
                        a_file_to_write_opened.write("premis:originalName \"{}\";\n".format(basename(p['origin'])))
                        a_file_to_write_opened.write("premis:eventIdentifierType \"ARK\";\n")
                        a_file_to_write_opened.write("premis:eventIdentifierValue \"mvol-0001\";\n")
                        a_file_to_write_opened.write("premis:eventType \"creation\";\n")
                        a_file_to_write_opened.write("premis:eventDateTime \"{}\"^^xsd:dateTime;\n".format(datetime.now().isoformat().split('.')[0]))
                        a_file_to_write_opened.write("a edm:WebResource.\n\n")

            elif part == 'mets':
                 for p in part_dict:
                    if p['origin'].endswith('mets.xml'):
                        old_filepath = p['origin']
                        mets_url = "<mvol-0001/"+p['origin']+">"
                        a_file_to_write_opened.write(mets_url+"\n")
                        a_file_to_write_opened.write("dc:format \"application/xml\";\n")
                        a_file_to_write_opened.write("a rdfs:Resource.\n\n")
            elif part == 'txt':
                  for p in part_dict:
                    if p['origin'].endswith('.txt'):
                        old_filepath = p['origin']
                        txt_url = "<mvol-0001/"+p['origin']+">"
                        a_file_to_write_opened.write(txt_url+"\n")
                        a_file_to_write_opened.write("dc:format \"text/plain\";\n")
                        a_file_to_write_opened.write("a rdfs:Resource.\n\n")
            elif part == 'struct':
                  for p in part_dict:
                    if p['origin'].endswith('.txt'):
                        old_filepath = p['origin']
                        struct_url = "<mvol-0001/"+p['origin']+">"
                        a_file_to_write_opened.write(struct_url+"\n")
                        a_file_to_write_opened.write("dc:format \"text/plain\";\n")
                        a_file_to_write_opened.write("a rdfs:Resource.\n\n")
                        
            elif part == "dc":
                for p in part_dict:
                    if p['origin'].endswith('dc.xml'):
                        old_filepath = p['origin']
                        with open(p['dst'], 'r') as dc_file:
                            tree = ElementTree.parse(dc_file)

                        dc_root = tree.getroot()
                        dc_title = dc_root.find('title')
                        dc_creator = dc_root.find('creator')
                        dc_date = dc_root.find('date')
                        dc_description = dc_root.find('description')
                        url = 'mvol-0001/'+p['origin']
                        dc_url = "<"+url+">"
                        a_file_to_write_opened.write('<mvol-0001/'+p['origin']+">\n")
                        a_file_to_write_opened.write("dc:format \"application/xml\";\n")
                        a_file_to_write_opened.write("ore:proxyFor " + "<" + issue_providedcho_url + ">;\n")
                        a_file_to_write_opened.write("ore:proxyIn " + "<" + issue_aggregation_url + ">;\n")
                        a_file_to_write_opened.write("a ore:Proxy.\n\n")

                        a_file_to_write_opened.write("<" + issue_providedcho_url + ">\n")
                        a_file_to_write_opened.write("dc:coverage \"Chicago\";\n")
                        a_file_to_write_opened.write("dc:date \"" +  dc_date.text + "\";\n")
                        a_file_to_write_opened.write("edm:year \"" + dc_date.text + "\";\n")
                        a_file_to_write_opened.write("dc:description \"" + dc_description.text + "\";\n")
                        a_file_to_write_opened.write("dc:identifier: \"{}\";\n".format(handle_id))
                        a_file_to_write_opened.write("dc:language \"en\";\n")
                        a_file_to_write_opened.write("dc:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
                        a_file_to_write_opened.write("dc:title \"" + dc_title.text + "\";\n")
                        a_file_to_write_opened.write("dc:type \"Text\";\n")
                        a_file_to_write_opened.write("edm:type \"TEXT\";\n")
                        pages = [(len(n), int(n.lstrip('0'))) for n in mega_object[issue_num]['pages']]
                        sorted_pages = sorted(pages, key=lambda x: x[1])
                        a_file_to_write_opened.write("dcterms:isPartOf <http://repository.lib.uchicago.edu/collections/{}/>;\n".format(collection_id))
                        a_file_to_write_opened.write("erc:who \"{}\";\n".format(":unav"))
                        a_file_to_write_opened.write("erc:what \"{}\";\n".format(dc_title.text))
                        a_file_to_write_opened.write("erc:when \"{}\";\n".format(dc_date.text))
                        a_file_to_write_opened.write("erc:where <{}>;\n".format(issue_providedcho_url))
                        for page in sorted_pages:
                            if page[0] == 4:
                                pagenum = handle_id+'_'+str(page[1]).zfill(4)
                            else:
                                pagenum = str(page[1]).zfill(8)
                            a_file_to_write_opened.write("dcterms:hasPart " + "<" + issue_providedcho_url + "/" + pagenum + ">;\n")
                        a_file_to_write_opened.write("a edm:ProvidedCHO.\n\n")

            elif part == 'pages':
                all_pages = [x for x in part_dict]
                for page_number, page_dict in part_dict.items():
                    if len(page_number) == 4:
                        pagenum = handle_id+'_'+str(page_number)
                    else:
                        pagenum = str(page_number)
                    page_rem = "mvol-0001/rem/" + issue_num + "/" + pagenum
                    page_providedcho = 'mvol-0001/' + issue_num + "/" + pagenum 
                    page_aggregation = "mvol-0001/aggregation/" + issue_num + "/" + pagenum 

                    tif_file = [x['origin'] for x in page_dict['tif'] if x['origin'].endswith('.tif')][0]
                    a_file_to_write_opened.write("<" + page_providedcho + ">\n")

                    for p in page_dict:
                       for part in page_dict[p]: 
                            if 'ALTO' in part['origin'] and not part['origin'].endswith('.fits.xml') and not part['origin'].endswith('premis.xml'):
                                a_file_to_write_opened.write("dc:description <mvol-0001/"+part['origin']+">;\n")
                            elif part['origin'].endswith('.pos'):
                                a_file_to_write_opened.write("dc:description <mvol-0001/"+part['origin']+">;\n")
                    a_file_to_write_opened.write("dc:language \"en\";\n")
                    a_file_to_write_opened.write("dc:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
                    a_file_to_write_opened.write("dc:title \"Page {}\";\n".format(str(page_number).lstrip('0')))
                    a_file_to_write_opened.write("dc:type \"Text\";\n")
                    a_file_to_write_opened.write("edm:type \"TEXT\";\n")
                    a_file_to_write_opened.write("dc:isPartOf <" + issue_providedcho_url + ">;\n")

                    nextPageNum = int(str(page_number).lstrip('0')) - 1 
                    if len(page_number) == 4:
                        pn = str(nextPageNum).zfill(4)
                    else:
                        pn = str(nextPageNum).zfill(8)
                    nextPageList = [x for x in all_pages if x==pn]
                    if len(nextPageList) > 0:
                        if len(pn) == 4:
                            pn = handle_id+'_'+pn
                        else:
                            pn = pn
                        a_file_to_write_opened.write("edm:isNextInSequence <" + issue_providedcho_url + "/" + pn + ">;\n")
                    a_file_to_write_opened.write("a edm:ProvidedCHO.\n\n")
                    a_file_to_write_opened.write("<" + page_rem + ">\n")
                    a_file_to_write_opened.write("dcterms:created \"" + datetime.now().isoformat().split('.')[0] + "\"^^xsd:dateTime;\n")
                    a_file_to_write_opened.write("dcterms:creator <http://repository.lib.uchicago.edu/>;\n")
                    a_file_to_write_opened.write("ore:describes <" + page_aggregation + ">;\n")
                    a_file_to_write_opened.write("a ore:ResourceMap.\n\n")

                    a_file_to_write_opened.write("<" + page_aggregation + ">\n")
                    a_file_to_write_opened.write("dcterms:created \"{}\"^^xsd:dateTime;\n".format(datetime.now().isoformat().split('.')[0]))
                    a_file_to_write_opened.write("dcterms:modified \"{}\"^^xsd:dateTime;\n".format(datetime.now().isoformat().split('.')[0]))
                    a_file_to_write_opened.write("edm:aggregatedCHO <" + page_providedcho + ">;\n")
                    a_file_to_write_opened.write("edm:dataProvider \"University of Chicago Library\";\n")

                    tif_file = [x['origin'] for x in page_dict['tif'] if x['origin'].endswith('.tif')][0]
                    jpeg_file = [x['origin'] for x in page_dict['jpg'] if x['origin'].endswith('.jpg')][0]
                    
                    a_file_to_write_opened.write("edm:isShownBy <mvol-0001/" + tif_file + ">;\n")
                    a_file_to_write_opened.write("edm:object <mvol-0001/" + jpeg_file + ">;\n")
                    a_file_to_write_opened.write("edm:provider \"University of Chicago Library\";\n")
                    a_file_to_write_opened.write("edm:rights <http://creativecommons.org/licenses/by-nc/4.0/>;\n")
                    a_file_to_write_opened.write("ore:isDescribedBy <" + page_rem +">;\n") 
                    a_file_to_write_opened.write("a ore:Aggregation.\n\n") 

                    for p in page_dict:
                        for part in page_dict[p]:
                            if part['origin'].endswith('.premis.xml'):
                                pass
                            elif part['origin'].endswith('.fits.xml'):
                                pass
                            elif part['origin'].endswith('.xml'):
                                a_file_to_write_opened.write("<mvol-0001/" + part['origin'] + ">\n")
                                a_file_to_write_opened.write("dc:format \"application/xml\";\n")
                                a_file_to_write_opened.write("a rdfs:Resource.\n\n")

                            elif part['origin'].endswith('tif'):
                                premis_path = part['dst'].replace('content.file','premis.xml')
                                tif_path = part['dst'].replace('content.file', 'fits.xml')

                                with open(tif_path, 'r') as tif_file:
                                    tif_tree = ElementTree.parse(tif_file)

                                root = tif_tree.getroot()
                                imagewidth = root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageWidth")

                                imageheight = root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageWidth")

                                with open(premis_path, 'r') as premis_file:
                                     tree = ElementTree.parse(premis_file)
                                root = tree.getroot()
                                objId = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectIdentifier/{http://www.loc.gov/premis/v3}objectIdentifierValue")
                                objIdType = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectIdentifier/{http://www.loc.gov/premis/v3}objectIdentifierType")
                       
                                fixities = root.findall("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}fixity")
                                sha256_messageDigest = None
                                md5_messageDigest = None
                                for n_fixity in fixities:
                                    n_algo = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigestAlgorithm").text
                                    if n_algo == 'sha256':
                                        sha256_messageDigest = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigest")
                                    elif n_algo == 'md5':
                                        md5_messageDigest = n_fixity.find("{http://www.loc.gov/premis/v3}messageDigest")
                                size = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}size")

                                mimetype = root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}format/{http://www.loc.gov/premis/v3}formatDesignation/{http://www.loc.gov/premis/v3}formatName")
                                a_file_to_write_opened.write("<mvol-0001/" + part['origin'] + ">\n")
                                a_file_to_write_opened.write("dc:format \"{}\";\n".format(mimetype.text))
                                a_file_to_write_opened.write("mix:fileSize {};\n".format(str(size.text)))
                                a_file_to_write_opened.write("mix:formatName \"{}\";\n".format(mimetype.text))
                                a_file_to_write_opened.write("mix:messageDigestAlgorithm \"MD5\";\n")
                                a_file_to_write_opened.write("mix:messageDigest \"{}\";\n".format(md5_messageDigest.text))
                                a_file_to_write_opened.write("premis:messageDigestOriginator \"hashlib.md5\";\n")
                                a_file_to_write_opened.write("mix:imageWidth {};\n".format(imagewidth.text))
                                a_file_to_write_opened.write("mix:imageHeight {};\n".format(imageheight.text))
                                a_file_to_write_opened.write("mix:bitsPerSampleUnit \"integer\";\n")

                                a_file_to_write_opened.write("premis:objetIdentifierType \"ARK\";\n")

                                a_file_to_write_opened.write("premis:objectIdentifierValue <{}>;\n".format('mvol-0001/' + part['origin']))
                                a_file_to_write_opened.write("premis:objectCategory \"file\";\n")
                                a_file_to_write_opened.write("premis:compositionLevel 0;\n")
                                a_file_to_write_opened.write("premis:messageDigestAlgorithm \"SHA-256\";\n")
                                a_file_to_write_opened.write("premis:messageDigest \"{}\";\n".format(sha256_messageDigest.text))
                                a_file_to_write_opened.write("premis:messageDigestOriginator \"hashlib.sha256\";\n")
                                a_file_to_write_opened.write("premis:size \"{}\";\n".format(size.text))
                                a_file_to_write_opened.write("premis:formatName \"{}\";\n".format(mimetype.text))
                                a_file_to_write_opened.write("premis:originalName \"{}\";\n".format(basename(part['origin'])))
                                a_file_to_write_opened.write("premis:eventIdentifierType \"ARK\";\n")
                                a_file_to_write_opened.write("premis:eventIdentifierValue \"mvol-0001\";\n")
                                a_file_to_write_opened.write("premis:eventType \"creation\";\n")
                                a_file_to_write_opened.write("premis:eventDateTime \"{}\"^^xsd:dateTime;\n".format(datetime.now().isoformat().split('.')[0]))
                                a_file_to_write_opened.write("a edm:WebResource.\n\n")

                            elif part['origin'].endswith('.pos'):
                                a_file_to_write_opened.write("<mvol-0001/" + part['origin'] + ">\n")
                                a_file_to_write_opened.write("dc:format \"text/plain\";\n")
                                a_file_to_write_opened.write("a rdfs:Resource.\n\n")

                            elif 'ALTO' in part['origin']:
                                a_file_to_write_opened.write("<mvol-0001/" + part['origin'] + ">\n")
                                a_file_to_write_opened.write("dc:format \"application/xml\";\n")
                                a_file_to_write_opened.write("a rdfs:Resource.\n\n")

                            elif part['origin'].endswith('jpg'):
                                a_file_to_write_opened.write("<mvol-0001/" + part['origin'] + ">\n")
                                a_file_to_write_opened.write("dc:format \"image/jpeg\";\n")
                                a_file_to_write_opened.write("a rdfs:Resource.\n\n")


def main():
    """
    fill_in_please
    """
    try:
        compound = arrange_bytestreams()
        pages = generate_page_dict(compound)
        final_organization = merge_pages_into_compound(compound, pages)
        sip_generation(final_organization)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
