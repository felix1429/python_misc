#!/usr/bin/env python
# Dispatch - synchronize two folders


import os, filecmp, shutil
from stat import *

class Dispatch:
    ''' This class represents a synchronization object '''

    def __init__(self, name=''):
        self.name = name
        self.node_list = []
        self.name_list = []
        self.file_copied_count = 0
        self.folder_copied_count = 0

    def add_node(self, node):
        self.node_list.append(node)
        self.name_list.append(node.name)

    def clear_nodes(self):
        self.node_list[:] = []
        self.name_list[:] = []

    def compare_nodes(self):
        ''' This method takes the nodes in the node_list and compares them '''
        nodeListLength = len(self.node_list)
        # For each node in the list
        for node in self.node_list:
            node_index = self.node_list.index(node)
            # If the list has another item after it, compare them
            if node_index < nodeListLength - 1:
                node2 = self.node_list[self.node_list.index(node) + 1]
                try:
                    print('\nSyncing Node ' + self.name_list[node_index] + ' to Node ' + self.name_list[node_index + 1] + ':')
                except UnicodeEncodeError as e:
                    print('Syncing Node 0 to 1')
                # Passes the two root directories of the nodes to the recursive _compare_directories.
                self._compare_directories(node.root_path, node2.root_path)

    def _compare_directories(self, left, right):
        ''' This method compares directories. If there is a common directory, the
            algorithm must compare what is inside of the directory by calling this
            recursively.
        '''
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self._compare_directories(os.path.join(left, d), os.path.join(right, d))
#        if comparison.left_only:
#            self._copy(comparison.left_only, left, right)
        if comparison.right_only:
            self._copy(comparison.right_only, right, left)
        left_newer = []
        right_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                l_modified = os.stat(os.path.join(left, d)).st_mtime
                r_modified = os.stat(os.path.join(right, d)).st_mtime
                if l_modified > r_modified:
                    left_newer.append(d)
                else:
                    right_newer.append(d)
#        self._copy(left_newer, left, right)
        self._copy(right_newer, right, left)

    def _copy(self, file_list, src, dest):
        ''' This method copies a list of files from a source node to a destination node '''
        for f in file_list:
            srcpath = os.path.join(src, os.path.basename(f))
            if os.path.isdir(srcpath):
                shutil.copytree(srcpath, os.path.join(dest, os.path.basename(f)))
                self.folder_copied_count = self.folder_copied_count + 1
                try:
                    print('Copied directory \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"')
                except UnicodeEncodeError:
                    print('Copied directory\n')
            else:
                success = False
                try:
                    shutil.copy2(srcpath, dest)
                    success = True
                except IOError:
                    try:
                        filelist = [f for f in os.listdir(dest)]
                        for f in filelist:
                            os.remove(os.path.join(dest, f))
                        shutil.copy2(srcpath, dest)
                        sucess = True
                    except PermissionError:
                        print("A permission error occurred, the file \""
                              + os.path.basename(srcpath) + "\" may be in use")
                finally:
                    if success:
                        self.file_copied_count = self.file_copied_count + 1
                        try:
                            print('Copied \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"\n')
                        except UnicodeEncodeError:
                            print('Copied file\n')

class Node:
    ''' This class represents a node in a dispatch synchronization '''

    def __init__(self, path, name=''):
        self.name = path
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)

def run(external, pc):
    try:
        a = Dispatch()
        ext_node = Node(external)
        pc_node = Node(pc)
        a.add_node(ext_node)
        a.add_node(pc_node)
        a.compare_nodes()
        a.clear_nodes()
    except FileNotFoundError:
        print("Directory not found, aborting sync")


if __name__ == "__main__":
    run("E:/shares/Album Art", "H:/Music/Album Art")
    run("G:/Media/Album Art", "H:/Music/Album Art")

    run("E:/shares/Music", "H:/Music/Music")
    run("G:/Media/Music", "H:/Music/Music")

    run("E:/shares/Torrent Files", "H:/Torrents/Torrent files")
    run("G:/Torrents/Torrent Files", "H:/Torrents/Torrent files")

    run("E:/shares/uTorrent AppData", "C:/Users/Trevor/AppData/Roaming/uTorrent")
    run("G:/Torrents/uTorrent AppData", "C:/Users/Trevor/AppData/Roaming/uTorrent")
    
    run("G:/Torrents/Media", "H:/Torrents/Media")

    run("G:/Media/Movies", "E:/shares/Movies")

    run("G:/Other/foobar2000", "C:/Users/Trevor/AppData/Roaming/foobar2000")
    run("E:/shares/Other/foobar2000", "C:/Users/Trevor/AppData/Roaming/foobar2000")
    print('Completed')
