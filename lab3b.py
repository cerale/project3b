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
    block_dict = {}
    levels = {1: 'INDIRECT', 2: 'DOUBLE INDIRECT', 3: 'TRIPLE INDIRECT'}
    #third migo is offset
    third_migo = {1: 12, 2: (12+256), 3: (12 + 256 + (256*256))}
        
    for i in inode_list:
        logical_offset = 0
        for j in i.block_list:
            if j != 0:
                if j < 0 or j > (superblock[0].s_blocks_count - 1):
                    everything_is_ok = False
                    print("INVALID BLOCK " + str(j) + " IN INODE "
                          + str(i.inode_num) + " AT OFFSET " + str(logical_offset))
                if j < (group[0].firstblock_location + superblock[0].s_inode_size *
                        group[0].inode_count / superblock[0].s_block_size):
                    everything_is_ok = False
                    print("RESERVED BLOCK " + str(j) + " IN INODE "
                          + str(i.inode_num) + " AT OFFSET " + str(logical_offset))
                elif j in block_dict:
                    block_dict[j].append(classes.Info('', j, i.inode_num, logical_offset))
                else:
                    block_dict[j] = [classes.Info('', j, i.inode_num, logical_offset)]


            logical_offset = logical_offset + 1
        
        for k in range(len(i.pointer_list)):
            ind = levels[k+1]
            logical_offset = third_migo[k+1]
            if i.pointer_list[k] != 0:
                if i.pointer_list[k] < 0 or i.pointer_list[k] > (superblock[0].s_blocks_count-1):
                    everything_is_ok = False
                    print("INVALID " + str(ind) + " BLOCK " 
                              + str(i.pointer_list[k]) + " IN INODE "
                              + str(i.inode_num) +  " AT OFFSET " + str(logical_offset))
                if i.pointer_list[k] < (group[0].firstblock_location + superblock[0].s_inode_size *
                                            group[0].inode_count / superblock[0].s_block_size):
                    everything_is_ok = False
                    print("RESERVED " + str(ind) + " BLOCK " + str(i.pointer_list[k])
                              + " IN INODE " + str(i.inode_num) + " AT OFFSET " + str(logical_offset))                
                elif i.pointer_list[k] in block_dict:
                    block_dict[i.pointer_list[k]].append(classes.Info(ind, i.pointer_list[k], i.inode_num, logical_offset))
                else:
                    block_dict[i.pointer_list[k]] = [classes.Info(ind, i.pointer_list[k], i.inode_num, logical_offset)]
        

    for l in range(len(indirent_list)):
        ind = levels[indirent_list[l].indirection_level]
        logical_offset = indirent_list[l].logicalblock_offset
        if indirent_list[l].referencedblock_num != 0:
            if indirent_list[l].referencedblock_num < 0 or indirent_list[l].referenceblock_num > (superblock[0].s_blocks_count - 1) or indirent_list[l].referenceblock_num < (group[0].firstblock_location + superblock[0].s_inode_size * group[0].inode_count / superblock[0].s_block_size):
                everything_is_ok = False
                print("INVALID " +str(ind) +" BLOCK " + str(indirent_list[l].referencedblock_num) + " IN INODE "
                      + str(indirent_list[l].inode_num) + " AT OFFSET " + str(logical_offset))
            elif indirent_list[l].referencedblock_num:
                block_dict[indirent_list[l].referencedblock_num].append(classes.Info(ind, indirent_list[l].referencedblock_num, indirent_list[l].inode_num, logical_offset))
            else:
                block_dict[indirent_list[l].referencedblock_num] = [classes.Info(ind, indirent_list[l].referencedblock_num, indirent_list[l].inode_num, logical_offset)]

    for block in range(0, superblock[0].s_blocks_count):
        if (group[0].firstblock_location + superblock[0].s_inode_size * group[0].inode_count / superblock[0].s_block_size) <= block <= superblock[0].s_blocks_count-1:
            if block in block_dict and block in bfree_list:
                everything_is_ok = False
                print("ALLOCATED BLOCK " + str(block) + " ON FREELIST")
                
    for block in range(0, superblock[0].s_blocks_count):
        if (group[0].firstblock_location + superblock[0].s_inode_size * group[0].inode_count / superblock[0].s_block_size) <= block <= superblock[0].s_blocks_count-1:
            if block in block_dict:
                my_block = block_dict[block]
            if len(my_block) > 1:
                for duplicate in range(len(my_block)):
                    block_data = my_block[duplicate]
                    everything_is_ok = False
                    print("DUPLICATE " +  str(block_data.block_type) + " " + str(block_data.block_num)
                          + " IN INODE " + str(block_data.inode_num) + " AT OFFSET " 
                          + str(block_data.offset))



    return                            


    
    #Unreferenced audit
'''
    for block in range(0, superblock[0].s_blocks_count):
        if (group[0].firstblock_location + superblock[0].s_inode_size * group[0].inode_count / superblock[0].s_block_size) <= block <= superblock[0].s_blocks_count-1:
            if block not in block_dict and block not in bfree_list:
                everything_is_ok = False
                print("UNREFERENCED BLOCK " + str(block))
'''

   
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

    #Check for correctness of . directory
    for directory in dirent_list:
        if ((directory.name == "'.'") and (directory.parentinode_num != directory.inode_num)):
            everything_is_ok = False
            print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME '.' LINK TO INODE " + str(directory.inode_num) + " SHOULD BE " + str(directory.parentinode_num))

    #Check for correctness of .. directory
    for directory in dirent_list:
        if ((directory.name == "'..'") and (directory.parentinode_num == 2) and (directory.parentinode_num != directory.inode_num)):
            everything_is_ok = False
            print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME '..' LINK TO INODE " + str(directory.inode_num) + " SHOULD BE " + str(directory.parentinode_num))
    for directory in dirent_list:
        parents_maybe = [] #Holds all possible parents
        if ((directory.name == "'..'") and (directory.parentinode_num != 2)):
            for i in dirent_list:
                if ((directory.parentinode_num == i.inode_num) and (directory.parentinode_num != i.parentinode_num)):
                    parents_maybe.append(i)
            for parent_directory in parents_maybe:
                if (directory.inode_num != parent_directory.parentinode_num):
                    everything_is_ok = False
                    print("DIRECTORY INODE " + str(directory.parentinode_num) + " NAME " + directory.name + " LINK TO INODE " + str(directory.inode_num) + " SHOULD BE " + str(parent_directory.parentinode_num))
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
