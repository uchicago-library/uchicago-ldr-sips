'''
Created on Oct 2, 2014

@author: tdanstrom
'''

from sys import stderr, stdout
from datetime import datetime

class FileObject(object):
    filepath = ''
    accession = ''
    date = ''
    checksum = ''

    def __init__(self, filepath, accession, date, checksum, mimetype, size):
        self.dirhead = filepath.split('/')[0]
        filepath = filepath.split('/')[1:]
        filepath = '/'.join(filepath)
        self.filesize = size
        self.filepath = filepath
        self.accession = accession
        self.checksum = checksum
        self.mimetype = mimetype
        self.date = date

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return self.filepath == other.filepath and self.accession == other.accession and self.date == other.date

    def __gt__(self,other):
        if isinstance(other,self.__class__):
            if self.filepath == other.filepath:
                return self.date > other.date
            else:
                return self.filepath > other.filepath

    def __lt__(self,other):
        if isinstance(other,self.__class__):
            if self.filepath == other.filepath:
                return self.date < other.date
            else:
                return self.filepath < other.filepath

    def __hash__(self):
        return hash((self.filepath,self.date))

    def __str__(self):
        return "%s from %s" % (self.filepath,self.date)

    def __repr__(self):
        return "%s from %s" % (self.filepath,self.date)

class Data(object):
    tree = {}
    iterable = None

    def __init__(self, iterable):
        self.tree = {} 
        self.iterable = iterable

    def __str__(self):
        return '< Data() >'

    def searchKeys(self,target,result=[]):
        for k, v in self.tree.items():
            if isinstance(v,dict):
                if k == target:
                    result.append(k)
                self.searchKeys(v,target,result=result)
            else:
                if k == target:
                    result.append(k)
        return result

    def traceAncestry(self, a_dict, target, path=[], result=[]):
        from copy import copy
        for k, v in a_dict.items():
            path.append(k)
            if isinstance(v, dict):
                self.traceAncestry(v, target,path=path,result=result)
            if k == target:
                result.append(copy(path))
            path.pop()
        return result

    def getNode(self, key):
        n = self.traceAncestry(self.tree, key)[-1]
        current = copy(self.tree)
        for i in n:
            current = current[i]
        return current

    def isItLeaf(self, key):
        c = self.get_node(key)
        if type(c) == type({}) and hasattr(c,'files'):
            return True
        else:
            return False

    def reSortTree(self,pattern):
        self.tree = {}
        return self.build(pattern=pattern)

    def moveFiles(self,old,new,filepaths=[]):
        nodetomove = self.getNode(old)
        newlocation = self.getNode(new)
        newfiles = newlocation['files']
        oldfiles = nodetomove['files']
        if not filepaths:
            filepaths = nodetomove['files']
        else:
            pass
        newfiles.extend(filepaths)
        oldfiles = [x for x in oldfiles if x not in filepaths]
        nodetomove['files'] = oldfiles

    def findAndDeleteFiles(self,a_dict, file_string):
        for k,v in a_dict.items():
            if isinstance(v,dict):
                try:
                    old = v['files']
                    new = [x for x in old if not file_string in x.filepath]
                    v['files'] = new
                except:
                    pass
                self.findAndDeleteFiles(v,file_string)

    def deleteFiles(self,key,filepaths):
        node = self.getNode(key)
        files = [x for x in node['files'] if x.filepath not in filepaths]
        node['files'] = files
    
    def deleteNode(self, key):
        nodetodelete = self.getNode(key)
        parentnode = self.getNode(self.traceAncestry(self.tree,key)[-1][-2])
        del parentnode[key]

    def moveNode(self,key,newkey):
        nodetomove = self.getNode(key)
        newparent = self.getNode(self.traceAncestry(self.tree,newkey)[-1][-1])
        newnode = {key:nodetomove}
        newparent.update(nodetomove)

    def normalizePunctuation(self,value):
        from re import compile as re_compile, escape as re_escape
        import string
        punctuations = re_compile('[%s]' % re_escape(string.punctuation))
        return punctuations.sub(' ', value)

    def findWords(self,string):
        from re import compile as re_compile, split as re_split
        pattern = re_compile('\b?\w+\b')
        matches = re_split(pattern,string)
        if matches:
            return matches[0].split(' ')
        else:
            raise ValueError("%s did not have any recognizable single words in the filename" % string)

    def findSpecificPattern(self, string, pattern):
        from re import compile as re_compile
        pattern = re_compile(pattern)
        match = pattern.search(string)
        if match:
            match = match.groups()
            match = [x for x in match if x]
            return match
        else:
            raise ValueError("%s did not match specified pattern" % string)

    def makeleaf(self,a_dict, fobject):
        from functools import reduce
        def uniquify(acc,n):
            if acc == []:
                acc.append(n)
                return acc
            else:
                current = acc[-1]
                if current.filepath == n.filepath:
                    if current.date < n.date:
                        acc[-1] = n
                        return acc
                    else:
                        return acc
                else:
                    acc.append(n)
                    return acc
        try:
            a_dict['files'].append(fobject)
        except KeyError:
            a_dict['files'] = [fobject]
        old = sorted(a_dict['files'])
        new = reduce(uniquify,old,[])
        a_dict['files'] = new
        
    def getDepthOfKey(self, key):
        d = self.traceAncestry(self.tree, key)
        if d == []:
            return 0
        else:
            return len(d[-1])

    def getNodesAtCertainHeight(self, a_dict, height,result=[]):
        for k,v in a_dict.items():
            if isinstance(v,dict):
                check = v['height'] == height
                if check:
                    result.append(v)
                self.getNodesAtCertainHeight(v,height,result=result)
        return result

    def nestDictionary(self, iterable, fobject):
        from os.path import join
        count = 0
        total = len(iterable)
        current = self.tree
        parent = ''
        while (count < total):
            current[iterable[count]] = current.get(iterable[count],{})
            current = current[iterable[count]]
            current['height'] = count
            current['key'] = iterable[count]
            current['parent'] = parent
            current['accession'] = fobject.accession
            parent = parent+'/'+iterable[count]
            count += 1
        self.makeleaf(current, fobject)

    def build(self, pattern=None):
        from re import compile as re_compile, split as re_split
        from os.path import join
        self.pattern = pattern
        for item in self.iterable:
            filepath = join(item.accession, item.filepath)
            fileobject = FileObject(item.filepath,item.accession,item.createdate, item.checksum, item.mimetype, item.filesize)
            s = self.normalizePunctuation(filepath)
            try:
                if not pattern:
                    groups = self.findWords(s)
                else:
                    groups = self.findSpecificPattern(s,pattern)
                self.nestDictionary(groups,fileobject)
            except Exception as e:
                stderr.write("ERROR\t%s\t%s\n" % (datetime.now().isoformat(),str(e)))
        return self.tree
