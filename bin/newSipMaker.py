from os import _exit
from uchicagoldrtoolsuite.bit_level.lib.readers.filesystemarchivereader import FileSystemArchiveReader

def main():
    try:
        print("making sips")
        reader = FileSystemArchiveReader()
        reader = reader.read("/data/repository/tr/ar/", "pht0276ghrk0t")
        for n_segment in reader.segment_list:
            for n_msuite in n_segment.materialsuite_list:
                print(n_msuite)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())
