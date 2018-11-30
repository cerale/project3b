#NAME: Alejandra Cervantes,Ryan Miyahara
#EMAIL: alecer@ucla.edu,rmiyahara144@gmail.com
#ID: 104844623,804585999

import sys
import csv
import classes

everything_is_ok = True
superblock = []
group = []
bfree_list = []
ifree_list = []
inode_list = []
inode_num_list = []
dirent_list = []
indirent_list = []

def block_consistency_audits():
    return

def inode_allocation_audits():
    #Check allocated inodes are not in freelist
    for i in inode_list:
        if i.inode_num in ifree_list: #Inconsistency found
            everything_is_ok = False
            print("ALLOCATED INODE " + str(i.inode_num) + " ON FREELIST")

    #Add inodes to list for checking
    for i in range(len(inode_list)):
        inode_num_list.append(inode_list[i].inode_num)
    #Check unallocated inodes are in freelist
    for i in range(superblock[0].s_first_ino, superblock[0].s_inodes_count):
        if i not in ifree_list and i not in inode_num_list:
            everything_is_ok = False
            print("UNALLOCATED INODE " + str(i) + " NOT ON FREELIST")
    return

def directory_consistency_audits():
    #Check i-node reference count against discovered links
    record_inodelink = [] #Each index + 1 represents an i-node

    #Check for invalid or unallocated inodes while incrementing record of links
    for i in range(superblock[0].s_inodes_count):
        record_inodelink.append(0)
    for directory in dirent_list:
        if((directory.inode_num > superblock[0].s_inodes_count) or (directory.inode_num < 1)): #Invalid inode
            everything_is_ok = False
            print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME " + directory.name + " INVALID INODE " + str(directory.inode_num))
        elif(directory.inode_num not in inode_num_list): #Unallocated inode
            everything_is_ok = False
            print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME " + directory.name + " UNALLOCATED INODE " + str(directory.inode_num))
        elif(directory.inode_num - 1 in range(superblock[0].s_inodes_count)):
            record_inodelink[directory.inode_num - 1] += 1

    #Record of links is completed. Check for correct link counts
    for curr_inode in inode_list:
        if (curr_inode.inode_num in range(superblock[0].s_inodes_count)):
            if (record_inodelink[curr_inode.inode_num - 1] != curr_inode.link_count):
                everything_is_ok = False
                print("INODE " + str(curr_inode.inode_num) + " HAS " + str(record_inodelink[curr_inode.inode_num - 1]) + " LINKS BUT LINKCOUNT IS " + str(curr_inode.link_count))

    #Check for . directory
    for directory in dirent_list:
        if ((directory.name == "'.'") and (directory.parentinode_num != directory.inode_num)):
            everything_is_ok = False
            print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME '.' LINK TO INODE " + str(directory.inode_num) + " SHOULD BE " + str(directory.parentinode_num))

    #Check for .. directory
    
    return
def read_csv():
    try:
        with open(sys.argv[1]) as filename:
            csv_file = csv.reader(filename)
            for row in csv_file:
                if (row[0] == "SUPERBLOCK"):
                    superblock.append(classes.Superblock_Summary(row))
                elif (row[0] == "GROUP"):
                    group.append(classes.Group_Summary(row))
                elif (row[0] == "BFREE"):
                    bfree_list.append(int(row[1]))
                elif (row[0] == "IFREE"):
                    ifree_list.append(int(row[1]))
                elif (row[0] == "INODE"):
                    inode_list.append(classes.Inode_Summary(row))
                elif (row[0] == "DIRENT"):
                    dirent_list.append(classes.Dirent_Summary(row))
                elif (row[0] == "INDIRENT"):
                    indirent_list.append(classes.Indirent_Summary(row))
    except IOError:
        print("Open file failed.", file = sys.stderr)
        sys.exit(1)
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

    #Perform audits
    block_consistency_audits()
    inode_allocation_audits()
    directory_consistency_audits()

    #Exit with the appropriate value
    if everything_is_ok:
        sys.exit(0) #Successful exit
    else:
        sys.exit(2) #Inconsistency found, everything is not ok

if __name__ == "__main__":
    main()
