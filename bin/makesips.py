
__author__ = "Tyler Danstrom"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "1.0.0"
__maintainer__ = "Tyler Danstrom"
__email__ = "tdanstrom@uchicago.edu"
__status__ = "Production"
__description__ = "This program takes a random selection of files from the ldr database and evaluates for file corruption."

from sys import argv, path

from argparse import Action, ArgumentParser
from configobj import ConfigObj
from datetime import datetime, timedelta
from grp import getgrgid
from pwd import getpwuid
from hashlib import md5, sha256
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit, stat
from os.path import exists, relpath
from re import compile as re_compile, split as re_split
from sqlalchemy import Table

from uchicagoldr.batch import Batch
from uchicagoldr.database import Database
from uchicagoldrsips.LDRFileTree import Data

def getTree(generator_data):
    d = Data(generator_data)
    d.build()
    if args.pattern:
        d.reSortTree(args.pattern)
    else:
        pass
    return d

def getObjects(data,level):
    from pprint import pprint
    objects = []
    objects = data.getNodesAtCertainHeight(data.tree,level)
    return objects

def evaluate_items(b, createdate):
    for n in b.items:
        header_pat = re_compile('^\d{4}-\d{3}')
        if exists(n.filepath):
            n.root_path = args.root
            accession = n.find_file_accession()
            n.set_accession(accession)
            canonpath = n.find_canonical_filepath()
            if header_pat.search(canonpath):
                canonpath = '/'.join(canonpath.split('/')[1:])
            else:
                canonpath = canonpath
            n.set_canonical_filepath(canonpath)
            n.createdate = createdate
            sha256_fixity = n.find_hash_of_file(sha256)
            md5_fixity = n.find_hash_of_file(md5)
            n.checksum = sha256_fixity

            mime = n.find_file_mime_type()
            size = n.find_file_size()
            n.filesize = size
            accession = n.find_file_accession()
            yield n
        else:
            logger.error("{path} does not exist on the filesystem".format(path=n.filepath))            

def main():
    def find_group_name(filepath):
        unix_stat_of_file = stat(fp)
        grp_id_of_file = unix_stat_of_file.st_gid
        group_name = getattr(getgrgid(grp_id_of_file), 'gr_name', None)
        return group_name

    def find_user_name(filepath):
        uid_of_file = unix_stat_of_file.st_uid
        user_name = getpwuid(uid_of_file)
        return user_name
        
    parser = ArgumentParser(description="{description}". \
                            format(description=__description__),
                            epilog="Copyright University of Chicago; " + \
                            "written by {author} ". \
                            format(author = __author__) + \
                            " <{email}> University of Chicago". \
                            format(email = __email__))
    parser.add_argument("-v", help="See the version of this program",
                        action="version", version=__version__)
    parser.add_argument( \
                         '-b','-verbose',help="set verbose logging",
                         action='store_const',dest='log_level',
                         const=INFO \
    )
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_const',dest='log_level',
                         const=DEBUG \
    )
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         action="store_const",dest="log_loc",
                         const='./{progname}.log'. \
                         format(progname=argv[0]) \
    )
    parser.add_argument("-o","--object_level",
                        help="Enter the level at which object starts",
                        type=int,
                        action='store')
    parser.add_argument("-r", "--root",
                       help="Enter the root of the directory path",
                        action="store")
    parser.add_argument("directory_path", 
                        help="Enter a directory that you need to work on ",
                        action='store')

    parser.add_argument('pattern', help="Enter a pattern to filter files with",
                        action="store")
    global args
    args = parser.parse_args()
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "lib.uchicago.repository.logger" \
    )
    ch = StreamHandler()
    ch.setFormatter(log_format)
    try:
        logger.setLevel(args.log_level)
    except TypeError:
        logger.setLevel(INFO)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    current_date = datetime.now()
    isof_current_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")
    sixty_days_ago_date = current_date - timedelta(days=60)
    isof_sixty_days_ago_date = sixty_days_ago_date.strftime( \
                            "%Y-%m-%dT%H:%M:%S")
    db = Database("sqlite:////media/repo/repository/databases/" +  
                  "official/repositoryAccessions.db.new",tables_to_bind= \
                  ['record'])
                  

    class Record(db.base):
        __table__ = Table('record', db.metadata, autoload=True)
        
    b = Batch(args.root, directory = args.directory_path)
    difference_in_path = relpath(args.directory_path, args.root)

    query = db.session.query(Record.createdate).filter(Record.receipt == \
                                                       difference_in_path) 
    createdate = query.first()[0]
    items = b.find_items(from_directory = True, 
                         filterable = re_compile(args.pattern))
    b.set_items(items)
    try:
        generated_data = evaluate_items(b,createdate)
        count = 0
        objects = {}
        for n in generated_data:
            id_parts = args.pattern.split('/')
            id_parts_enumerated = [x for x in range(args.object_level)]
            id_part_values = [n.canonical_filepath.split('/')[x] \
                              for x in id_parts_enumerated]
            identifier = "-".join(id_part_values)
            try:
                objects[identifier].append(n)
            except KeyError:
                objects[identifier] = [n]
        print(objects.keys())
        return 0
    except KeyboardInterrupt:
         logger.error("Program aborted manually")
         return 131

if __name__ == "__main__":
    _exit(main())
