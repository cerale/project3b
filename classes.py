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

class Info:
    def __init__(self, block_type, block_num, inode_num, offset):
        if block_type == '':
            blockStr = 'BLOCK'
        else:
            blockStr = ' BLOCK'
        self.block_type = block_type + blockStr
        self.block_num = block_num
        self.inode_num = inode_num
        self.offset = offset
