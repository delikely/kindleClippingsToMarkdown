#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import fileinput
print "—————————————————————————————Kinde——————————————————————————————————"

mdFile = "My Clippings.md"
txtFile = "My Clippings.txt";
text = ""
title = ""
time = ""
content = ""

def isTitleExist(mdFile,mdTitle,option):
    mdTitle = "# " + mdTitle
    if option == "current":
        with open(mdFile) as file:
            for line in file.readlines():
                if line == mdTitle:
                    return 1
        return 0
    if option == "next":
        flag  = 0
        with open(mdFile) as file:
            for line in file.readlines():
                if line == mdTitle and flag == 0:
                    flag = 1
                    continue
                if flag == 1 and line[0] == "#":
                        return line
        return -1

class Insert_line(object):

    def __init__(self, file, keyword, newline):
        self.__file = file
        self.__key = keyword
        self.__newline = newline

    def _get_specify_lineno(self):
        i = 1
        try:
            f = open("%s" % self.__file)
        except IOError,e:
            print e[1] + ' "%s"' % e.filename
            sys.exit(1)
        while True:
            line = f.readline()
            if not line: break
            if "%s" % self.__key in line:
                return i
                break
            i += 1
        f.close()

    def _inserted_newline_list(self):
        if self._get_specify_lineno():
            # ls = os.linesep
            f = open("%s" % self.__file)
            li = f.readlines()
            f.close()
            li.insert(self._get_specify_lineno() - 1, self.__newline)
            return li

    def inserted_new_file(self):
        if self._inserted_newline_list():
            lines = self._inserted_newline_list()
            os.system("cp %s %s.bak" % (self.__file, self.__file))
            f = open("%s" % self.__file, 'w')
            f.writelines(lines)
            f.close()
        else:
            print 'No such keyword "%s"' % self.__key


with open(txtFile) as file:
    for line in file.readlines():
        if line == "==========\n":
            title = ""
            time = ""
            content = ""
        else:
            if title == "":
                title = line
                if isTitleExist(mdFile,title,"current") == 0:
                    if title[0] == " ":
                        title = title[1,]
                    f = open(mdFile,'a')
                    f.write("# "+ title + " \n")
                    f.close()
                continue
            if time == "" and title != "":
                time = line
                continue
            if time !="" and title != "":
                content = line
                nextTitle = isTitleExist(mdFile,title,"next")
                if nextTitle != -1:
                    file = Insert_line(mdFile, nextTitle, content)
                    file.inserted_new_file()
                else:
                    f = open(mdFile,'a')
                    f.write(content)
                    f.close()
                continue
