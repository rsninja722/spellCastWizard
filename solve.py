# todo
# blocked tiles
# multiple double/triple letters
# app with camera?
# flowchart of decision making

def main():
    swap = False
    grid = "nboiytsoorfwizdveijecuhaa"

    tripleLetter = (-1,-1)
    doubleLetter = (1,0)
    twoTimes = (3,1)

    # disable: (-1,-1)
    # (0,0) (0,1) (0,2) (0,3) (0,4)
    # (1,0) (1,1) (1,2) (1,3) (1,4)
    # (2,0) (2,1) (2,2) (2,3) (2,4)
    # (3,0) (3,1) (3,2) (3,3) (3,4)
    # (4,0) (4,1) (4,2) (4,3) (4,4)

    scores = {"a":1,"b":4,"c":5,"d":3,"e":1,"f":5,"g":3,"h":4,"i":1,"j":7,"k":6,"l":3,"m":4,"n":2,"o":1,"p":4,"q":8,"r":2,"s":2,"t":2,"u":4,"v":5,"w":5,"x":7,"y":4,"z":8}

    grid = [list(grid.lower())[x*5:x*5+5] for x in range(5)]

    words = trie()

    with open("words.txt","r") as f:
        for i in f:
            if "'" in i or "-" in i:
                continue
            words.add(i.strip().lower())

    searchPoses = dict()
    for row in range(5):
        for col in range(5):
            for i in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                newR,newC = row+i[0],col+i[1]
                if newR < 0 or newR > 4 or newC < 0 or newC > 4:
                    continue
                searchPoses[(row,col)] = searchPoses.get((row,col),[]) + [(newR,newC)]


    found = set()
    paths = dict()
    
    def find(r: int,c: int,word: str,twoX:int,score:int,path:list,swapped:tuple,trieNode:trie,mem:set):
        letter = grid[r][c]
        if swap and not swapped is None and swapped[0] == (r,c):
            letter = swapped[1]
            path += [(r,c,letter)]
        else:
            path += [(r,c,"")]

        word += letter
        mem.add((r,c))
        trieNode = trieNode.children.get(letter)

        if (r,c) == twoTimes:
            twoX = 2
        letterScore = scores[letter] * (2 if (r,c) == doubleLetter else 1) * (3 if (r,c) == tripleLetter else 1)
        score += letterScore

        if words.search(word):
            found.add((word,score*twoX + (10 if len(word) >= 6 else 0)))
            paths[word] = path

        for i in searchPoses.get((r,c)):
            newR,newC = i[0],i[1]
            if (newR,newC) in mem:
                continue
            newLetter = grid[newR][newC]
            if swap and swapped is None:
                for j in "abcdefghijklmnopqrstuvwxyz":
                    if j == newLetter:
                        continue
                    if trieNode.children.get(j) is None:
                        continue
                    find(newR,newC,word,twoX,score,path.copy(),((newR,newC),j),trieNode,mem.copy())
            if trieNode.children.get(newLetter) is None:
                continue
            find(newR,newC,word,twoX,score,path.copy(),swapped,trieNode,mem.copy())

        mem.remove((r,c))

    for row in range(5):
        for col in range(5):
            find(row,col,"",1,0,[],None,words,set())
            if swap:
                for j in "abcdefghijklmnopqrstuvwxyz":
                    if j == grid[row][col]:
                        continue
                    find(row,col,"",1,0,[],((row,col),j),words,set())

    result = list(found)
    result.sort(key=lambda x: x[1],reverse=True)

    print("best: ")
    print(result[0])
    print("---------------")
    path = paths[result[0][0]]
    swapLetters = [x for x in path if x[2] != ""]
    swapLetter = ((-1,-1),"")
    if len(swapLetters) != 0:
        swapLetter = ((swapLetters[0][0],swapLetters[0][1]),swapLetters[0][2])
    for row in range(5):
        line = ""
        for col in range(5):
            if any([x[0] == row and x[1] == col for x in path if x[2] == ""]):
                line += "("+grid[row][col].upper()+")"
            elif (row,col) == swapLetter[0]:
                line += "<"+swapLetter[1].upper()+">"
            else:
                line += " "+grid[row][col]+" "
        print(line)
    print("---------------")

    print("alternatives: ")
    for i in result[1:10]:
        print(i)

class trie:
    def __init__(self):
        self.children = {}
        self.end = False
    
    def add(self,word):
        if len(word) == 0:
            self.end = True
            return
        if word[0] not in self.children:
            self.children[word[0]] = trie()
        self.children[word[0]].add(word[1:])

    def search(self,word):
        if len(word) == 0:
            return self.end
        if word[0] not in self.children:
            return False
        return self.children[word[0]].search(word[1:])

    def __str__(self):
        return "word: " + ("yes, children: " if self.end else "no, children: ") + str(self.children)

main()

# Custom wordlist generated from http://app.aspell.net/create using SCOWL
# with parameters:
#   diacritic: strip
#   max_size: 95
#   max_variant: 1
#   special: hacker roman-numerals
#   spelling: US

# Using Git Commit From: Mon Dec 7 20:14:35 2020 -0500 [5ef55f9]

# Copyright 2000-2019 by Kevin Atkinson

#   Permission to use, copy, modify, distribute and sell these word
#   lists, the associated scripts, the output created from the scripts,
#   and its documentation for any purpose is hereby granted without fee,
#   provided that the above copyright notice appears in all copies and
#   that both that copyright notice and this permission notice appear in
#   supporting documentation. Kevin Atkinson makes no representations
#   about the suitability of this array for any purpose. It is provided
#   "as is" without express or implied warranty.

# Copyright (c) J Ross Beresford 1993-1999. All Rights Reserved.

#   The following restriction is placed on the use of this publication:
#   if The UK Advanced Cryptics Dictionary is used in a software package
#   or redistributed in any form, the copyright notice must be
#   prominently displayed and the text of this document must be included
#   verbatim.

#   There are no other restrictions: I would like to see the list
#   distributed as widely as possible.

# Special credit also goes to Alan Beale <biljir@pobox.com> as he has
# given me an incredible amount of feedback and created a number of
# special lists (those found in the Supplement) in order to help improve
# the overall quality of SCOWL.

# Many sources were used in the creation of SCOWL, most of them were in
# the public domain or used indirectly.  For a full list please see the
# SCOWL readme.

# http://wordlist.aspell.net/