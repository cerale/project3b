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
inode_num_list = []

class Superblock_Summary:
    def __init__(self, row):
        self.s_blocks_count = int(row[1])
        self.s_inodes_count = int(row[2])
        self.s_block_size = int(row[3])
        self.s_inode_size = int(row[4])
        self.s_blocks_per_group = int(row[5])
        self.s_inodes_per_group = int(row[6])
        self.s_first_ino = int(row[7])

class Group_Summary:
    def __init__(self, row):
        self.group_num = int(row[1])
        self.block_count = int(row[2])
        self.inode_count = int(row[3])
        self.freeblock_count = int(row[4])
        self.freeinode_count = int(row[5])
        self.bitmap_location = int(row[6])
        self.imap_location = int(row[7])
        self.firstblock_location = int(row[8])

class Inode_Summary:
    def __init__(self, row):
        self.inode_num = int(row[1])
        self.file_type = row[2]
        self.mode = row[3]
        self.owner = int(row[4])
        self.group = int(row[5])
        self.link_count = int(row[6])
        self.time_lastchange = row[7]
        self.time_mod = row[8]
        self.time_lastaccess = row[9]
        self.file_size = int(row[10])
        self.block_num = int(row[11])
        self.block_list = []
        self.pointer_list = []
        if (self.file_type == 'd' or self.file_type == 'f'):
            for i in range(12, 24):
                self.block_list.append(int(row[i]))
            for i in range(24, 27):
                self.pointer_list.append(int(row[i]))

class Dirent_Summary:
    def __init__(self, row):
        self.parentinode_num = int(row[1])
        self.logicalbyte_offset = int(row[2])
        self.inode_num = int(row[3])
        self.entry_len = int(row[4])
        self.name_len = int(row[5])
        self.name = str(row[6])

class Indirent_Summary:
    def __init__(self, row):
        self.parentinode_num = int(row[1])
        self.indirection_level = int(row[2])
        self.logicalblock_offset = int(row[3])
        self.indirectblock_num = int(row[4])
        self.referencedblock_num = int(row[5])

def read_csv():
    try:
        with open(sys.argv[1]) as filename:
            csv_file = csv.reader(filename)
            for row in csv_file:
                if (row[0] == "SUPERBLOCK"):
                    superblock.append(Superblock_Summary(row))
                elif (row[0] == "GROUP"):
                    group.append(Group_Summary(row))
                elif (row[0] == "BFREE"):
                    bfree_list.append(int(row[1]))
                elif (row[0] == "IFREE"):
                    ifree_list.append(int(row[1]))
                elif (row[0] == "INODE"):
                    inode_list.append(Inode_Summary(row))
                elif (row[0] == "DIRENT"):
                    dirent_list.append(Dirent_Summary(row))
                elif (row[0] == "INDIRENT"):
                    indirent_list.append(Indirent_Summary(row))
    except IOError:
        print("Open file failed.", file = sys.stderr)
        sys.exit(1)

def block_consistency_audits():
    return

def inode_allocation_audits():
    #Check allocated inodes are not in freelist
    for i in inode_list:
        if i.inode_num in ifree_list: #Inconsistency found
            everything_is_okay = False
            print("ALLOCATED INODE " + str(i.inode_num) + " ON FREELIST")

    #Check unallocated inodes are in freelist
    for i in range(superblock[0].s_first_ino, superblock[0].s_inodes_count):
        if i not in ifree_list and i not in inode_num_list:
            everything_is_okay = False
            print("UNALLOCATED INODE " + str(i) + " NOT ON FREELIST")

    return

def directory_consistency_audits():
    return

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

    for i in range(len(inode_list)):
        inode_num_list.append(inode_list[i].inode_num)

    #Perform audits
    block_consistency_audits()
    inode_allocation_audits()
    directory_consistency_audits()

    if everything_is_ok:
        sys.exit(0) #Successful exit
    else:
        sys.exit(2) #Inconsistency found, everything is not ok

if __name__ == "__main__":
    main()
