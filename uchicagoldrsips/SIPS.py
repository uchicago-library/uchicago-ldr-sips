from collections import namedtuple
from os.path import basename, join, splitext
from re import compile as re_compile
from sys import stdout, stderr

class URL(object):
    def __init__(self, subject):
        self.subject = subject

    def __str__(self):
        return "<"+self.subject+">"

class LDRURL(URL):
    def __init__(self, u):
        url = "http://ldr.lib.uchicago.edu/"
        url = join(url, u)
        self.subject = url

class RightsURL(URL):
    def __init__(self):
        self.subject = "http://creativecommons.org/licenses/by-nc/4.0/"

class PIURL(URL):
    def __init__(self, collection_ref, object_identifier):
        url = "http://pi.lib.uchicago.edu/1001/"
        url = join(url, collection_ref, object_identifier)
        self.subject = url

class Value(object):
    string = ""
    def __init__(self,value):
        self.string = value

    def __str__(self):
        return self.string

class IntegerValue():
    def __init__(self, value):
        assert isinstance(value, int)
        self.string = value

    def __str__(self):
        return str(self.string)

class DateValue(Value):
    def __str__(self):
        return "\"\"\"{value}\"\"\"^^^xsd:dateTime". \
            format(value = self.string)

class TextValue(Value):
    def __str__(self):
        return "\"{value}\"".format(value = self.string)

        

class Statement(object):
    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __str__(self):
        return "{element} {value}".format(element = self.element,
                                          value = self.value)

class Triple(object):
    subject = None
    object_type = None
    statements = []

    def __init__(self, subject, object_type):
        self.subject = URL(subject)
        self.object_type = object_type
        self.statements = []

    def add_statement(self, verb, value):
        assert len(verb.split(":")) > 1
        s = Statement(verb, value)
        self.statements.append(s)

    def __repr__(self):
        return self.subject

    def __str__(self):
        return "\n\n<{subject}>\n{statements}\na {type}".format(subject = self.subject,
                                                                type = self.object_type,
                                                                statements = ';\n'.join([str(x) for x in self.statements]))


class ProvidedCHO(Triple):
    def __init__(self, id):
        self.subject = join("/", id)
        self.object_type = "edm:ProvidedCHO"


class Aggregation(Triple):
    def __init__(self, id):
        self.subject = join("/aggregation", id)
        self.object_type = "ore:Aggregation"

class ResourceMap(Triple):
    def __init__(self, id):
        self.subject = join('/rem', id)
        self.object_type = "ore:ResourceMap"

class Proxy(Triple):
    def __init__(self, id):
        self.subject = join("/", id)
        self.object_type = "ore:Proxy"

class WebResource(Triple):
    def __init__(self, id):
        self.subject = join("/", id)
        self.object_type = "edm:WebResource"

class RDFSResource(Triple):
    def __init__(self, id):
        self.subject = join("/", id)
        self.object_type = "rdfs:Resource"
