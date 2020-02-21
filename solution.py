from collections import deque
from typing import Deque

class Library:

    gID = 0

    def __init__(self, bpd, signUpT):
        self.bpd = bpd
        self.signUpT = signUpT
        self.bookArr = deque()
        self.ID = Library.gID
        Library.gID += 1

    def addToBookArr(self, bookID, books):
        # add such that sorted in descending order
        if len(self.bookArr) == 0:
            self.bookArr.append(bookID)
            return

        for i in range(len(self.bookArr)):
            if books[bookID] >= books[self.bookArr[i]]:
                self.bookArr.insert(i, bookID)
                return

        self.bookArr.append(bookID)
        return

    def refactorBookArr(self, unique):
        # refactor bookArr based on which books have been processed.
        toBeDeleted = []
        for b in self.bookArr:
            if unique[b] == 1:
                toBeDeleted.append(b)

        for b in toBeDeleted:
            self.bookArr.remove(b)

        return

    def calculateScore(self, daysRemaining, books) -> int:
        # calculate max potential of the lib
        effectiveDays = daysRemaining - self.signUpT
        totalBooks = self.bpd * effectiveDays
        cumsum = 0
        if totalBooks < len(self.bookArr):
            for i in range(totalBooks):
                cumsum += books[self.bookArr[i]]
        else:
            for b in self.bookArr:
                cumsum += books[b]

        return cumsum


class Main:

    def getBestScore(self, libraries: Deque[Library], books, unique, daysRem):
        bestScore = 0
        bestLib = None

        for lib in libraries:
            lib.refactorBookArr(unique)
            score = lib.calculateScore(daysRem, books)
            if score > bestScore:
                bestScore = score
                bestLib = lib

        if bestLib == None:
            return 0, None

        for b in bestLib.bookArr:
            unique[b] = 1

        return bestScore, bestLib


    def printOut(self, libOut, file):
        with open("./output/" + file + "_out.txt", "w") as f:
            f.write(str(len(libOut)) + "\n")
            lines = []
            for l in libOut:
                lines.append(str(l.ID) + " " + str(len(l.bookArr)) + "\n")
                lines.append(" ".join([str(x) for x in l.bookArr]) + "\n")
            f.writelines(lines)
        return



    def main(self, file):
        libraries = deque()
        totalScore = 0
        libOut = []

        with open("./input/" + file + "_in.txt", "r") as f:
            b, l, D = [int(x) for x in f.readline().split()]
            books = [int(x) for x in f.readline().split()]
            unique = [0] * b
            for i in range(l):
                lb, sd, bpd = [int(x) for x in f.readline().split()]
                lbArr = [int(x) for x in f.readline().split()]
                lib = Library(bpd, sd)
                for book in lbArr:
                    lib.addToBookArr(book, books)
                libraries.append(lib)
        # exit(0)
        while D > 0 and len(libraries) > 0:
            bestScore, library = self.getBestScore(libraries, books, unique, D)
            if bestScore == 0:
                break
            libOut.append(library)
            libraries.remove(library)
            totalScore += bestScore
            D -= library.signUpT

        print("File " + file + " total score = " + str(totalScore))

        self.printOut(libOut, file)

        return totalScore

if __name__ == '__main__':
    m = Main()
    t = m.main("a")
    Library.gID = 0
    t += m.main("b")
    Library.gID = 0
    t += m.main("c")
    Library.gID = 0
    t += m.main("d")
    Library.gID = 0
    t += m.main("e")
    Library.gID = 0
    t += m.main("f")

    print("Final score = " + str(t))

    exit(0)
