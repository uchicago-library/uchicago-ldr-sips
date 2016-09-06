from os import _exit
from uchicagoldrtoolsuite.bit_level.lib.readers.filesystemarchivereader import FileSystemArchiveReader

def main():
    try:
        print("making sips")
        reader = FileSystemArchiveReader()
        reader.read("Z:/ar/", "pht0276ghrk0t")
        print(reader)
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(main())