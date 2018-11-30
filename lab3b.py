#NAME: Alejandra Cervantes,Ryan Miyahara
#EMAIL: alecer@ucla.edu,rmiyahara144@gmail.com
#ID: 104844623,804585999

import sys
import csv

everything_is_ok = True
superblock = []
group = []
bfree_list = []
ifree_list = []
inode_list = []
dirent_list = []
indirent_list = []

class Superblock_Summary:
    def __init__(self, row):
        self.s_blocks_count = row[1]
        self.s_inodes_count = row[2]
        self.s_block_size = row[3]
        self.s_inode_size = row[4]
        self.s_blocks_per_group = row[5]
        self.s_inodes_per_group = row[6]
        self.s_first_ino = row[7]

class Group_Summary:
    def __init__(self, row):
        self.group_num = row[1]
        self.block_count = row[2]
        self.inode_count = row[3]
        self.freeblock_count = row[4]
        self.freeinode_count = row[5]
        self.bitmap_location = row[6]
        self.imap_location = row[7]
        self.firstblock_location = row[8]

class Inode_Summary:
    def __init__(self, row):
        self.inode_num = row[1]
        self.file_type = row[2]
        self.mode = row[3]
        self.owner = row[4]
        self.group = row[5]
        self.link_count = row[6]
        self.time_lastchange = row[7]
        self.time_mod = row[8]
        self.time_lastaccess = row[9]
        self.file_size = row[10]
        self.block_num = row[11]

class Dirent_Summary:
    def __init__(self, row):
        self.parentinode_num = row[1]
        self.logicalbyte_offset = row[2]
        self.inode_num = row[3]
        self.entry_len = row[4]
        self.name_len = row[5]
        self.name = row[6]

class Indirent_Summary:
    def __init__(self, row):
        self.parentinode_num = row[1]
        self.indirection_level = row[2]
        self.logicalblock_offset = row[3]
        self.indirectblock_num = row[4]
        self.referencedblock_num = row[5]

def read_csv():
    try:
        with open(sys.argv[1]) as filename:
            csv_file = csv.reader(filename)
            for change in csv_file: #Cast all the numbers to ints
                for i in change:
                    if(i.isdigit()):
                        i = int(i)

            for row in csv_file:
                if (row[0] == "SUPERBLOCK"):
                    superblock.append(Superblock_Summary(row))
                elif (row[0] == "GROUP"):
                    group.append(Group_Summary(row))
                elif (row[0] == "BFREE"):
                    bfree_list.append(row[1])
                elif (row[0] == "IFREE"):
                    ifree_list.append(row[1])
                elif (row[0] == "INODE"):
                    inode_list.append(Inode_Summary(row))
                elif (row[0] == "DIRENT"):
                    dirent_list.append(Dirent_Summary(row))
                elif (row[0] == "INDIRENT"):
                    indirent_list.append(Indirent_Summary(row))
    except IOError:
        print("Open file failed.", file = sys.stderr)
        sys.exit(1)

def main():
    #Check argument
    if (len(sys.argv) != 2):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    if (len(filename) < 4):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)
    format = filename[len(filename) - 4:]
    if (format != ".csv"):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)

    #Take in data
    read_csv()

    if everything_is_ok:
        sys.exit(0) #Successful exit
    else:
        sys.exit(2) #Inconsistency found, everything is not ok

if __name__ == "__main__":
    main()