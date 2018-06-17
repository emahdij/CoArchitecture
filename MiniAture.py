import re


class Miniature:
    opcode = {
        "add": "0000",
        "sub": "0001",
        "slt": "0010",
        "or": "0011",
        "nand": "0100",
        "addi": "0101",
        "ori": "0111",
        "slti": "0110",
        "lui": "1000",
        "lw": "1001",
        "sw": "1010",
        "beq": "1011",
        "jalr": "1100",
        "j": "1101",
        "halt": "1110"
    }

    SymbolTable = {
    }

    def __init__(self, url="assemble E:\\assemble.as E:\\program.mc"):
        self.machinecode = []
        self.file = open(str(url).split(" ")[1], "r")
        self.addresultfile = str(url).split(" ")[2]

    def scan(self):
        regex = (
            "(.*?)[\t| ]*(add|sub|slt|or|n and|and)[\t| ]*([0-9]*),([0-9]*),([0-9]*)|(.*?)[\t| ]*(addi|ori|slti|lw|sw|beq|jalr)[\t| ]*([0-9]*),([0-9]*),([0-9]+|[a-z]+)|(.*?)[\t| ]*(lui)[\t| ]*([0-9]*),([0-9]*)|(.*?)[\t| ]*(j)[\t| ]*([0-9]*)|(.*?)[\t| ]*(halt)|(.*?)[\t| ]*(.fill)[\t| ]*([0-9]+|[a-z]+)|(.*?)[\t| ]*(.space)[\t| ]*([0-9]*)")
        self.readfile = self.file.read()
        self.separated = re.findall(regex, self.readfile)
        length = len(self.file.readline())
        self.separated = self.dell_duplicated()
        self.file.close()
        for i in range(self.separated.__len__()):
            self.separated[i][0] = str(self.separated[i][0]).replace("\t", "")
            self.separated[i][0] = str(self.separated[i][0]).replace(" ", "")
            if str(self.separated[i][0]) != '':
                if (str(self.separated[i][0]) in self.SymbolTable):
                    raise Exception("Ops:| " + self.separated[i][0] + " is existed")
                else:
                    newlable = {
                        str(self.separated[i][0]).replace("\t", "").replace(" ", ""): str(i)
                    }
                self.SymbolTable.update(newlable)
        print("scanned")

    def dell_duplicated(self):
        x = 0
        y = 0
        matris = [[0 for x in range(5)] for y in range(self.separated.__len__())]
        for i in range(self.separated.__len__()):
            y = 0
            for j in range(self.separated[i].__len__()):
                if self.separated[i][j] != '':
                    matris[x][y] = self.separated[i][j]
                    y += +1
            x += 1
            for i in range(matris.__len__()):
                if matris[i][0] == "\t\t":
                    matris[i][0] = ''
        return matris

    def print_file(self):
        print(self.readfile)

    def print_bin_file(self):
        for i in range(self.machinecode.__len__()):
            print(self.machinecode[i])

    def file_translate(self):
        for i in range(self.separated.__len__()):
            if self.Rtest(i):
                self.machinecode.append(
                    "0000" + self.opcode.get(self.separated[i][1]) + self.bin_complete(i, 3) + self.bin_complete(i,
                                                                                                                 4) + self.bin_complete(
                        i, 2) + "0" * 12)
            elif self.Jtest(i):
                if (self.separated[i][1] == "j"):
                    if int(self.separated[i][2]) > 65535:
                        raise Exception("Ops:| " + self.separated[i][2] + " is too big")
                    self.machinecode.append(
                        "0000" + self.opcode.get(self.separated[i][1]) + "00000000" + self.bin_complete(i, 2, 2))
                elif self.separated[i][1] == "halt":
                    self.machinecode.append(
                        "0000" + self.opcode.get(self.separated[i][1]) + "0" * 8 + "0" * 16
                    )

            elif self.Itest(i):
                if (self.separated[i][1] != "lui"):
                    if int(self.separated[i][4]) > 65535:
                        raise Exception("Ops:| " + self.separated[i][4] + " is too big")
                    self.machinecode.append(
                        "0000" + self.opcode.get(self.separated[i][1]) + self.bin_complete(i, 3) + self.bin_complete(i,
                                                                                                                     2)
                        + self.bin_complete(i, 4, 2)
                    )
                else:
                    if int(self.separated[i][4]) > 65535:
                        raise Exception("Ops:| " + self.separated[i][4] + " is too big")
                    self.machinecode.append(
                        "0000" + self.opcode.get(self.separated[i][1]) + "0000" + self.bin_complete(i,
                                                                                                    2) + self.bin_complete(
                            i, 3, 2)
                    )
            elif self.directive(i):
                if (self.separated[i][1] == ".fill"):
                    if re.match("[a-zA-Z]", str(self.separated[i][2])):
                        if (self.separated[i][2] in self.SymbolTable):
                            self.machinecode.append(bin(int(self.SymbolTable.get(self.separated[i][2])))[2:])
                        else:
                            raise Exception("Ops:| " + self.separated[i][2] + " not found")
                    else:
                        self.machinecode.append(bin(int(self.separated[i][2]))[2:])

                elif (self.separated[i][1] == ".space"):
                    self.machinecode.append(
                        bin(int(self.separated[i][2]))[2:]
                    )

    def bin_complete(self, i, j, type=1):
        if type == 1:
            st = bin(int(self.separated[i][j]))[2:]
            return "0" * (4 - len(st)) + st
        elif type == 2:
            if re.match("[a-zA-Z]", str(self.separated[i][j])):
                if (self.separated[i][j] in self.SymbolTable):
                    st = bin(int(self.SymbolTable.get(self.separated[i][j])))[2:]
                else:
                    raise Exception("Ops:| " + self.separated[i][j] + " not found")
            else:
                st = bin(int(self.separated[i][j]))[2:]
            return "0" * (16 - len(st)) + st

    def print_decimalcode(self):
        for i in range(self.machinecode.__len__()):
            print(int(self.machinecode[i], 2))

    def savefile(self):
        writefile = open(self.addresultfile, "w")
        for i in range(self.machinecode.__len__()):
            writefile.writelines(str(int(self.machinecode[i], 2))+"\n")
        writefile.close()

    Rtest = lambda self, i: True if "add sub slt or nand".find(self.separated[i][1]) != -1 else False

    Itest = lambda self, i: True if "addi ori slti lui lw sw beq jalr".find(self.separated[i][1]) != -1 else False

    Jtest = lambda self, i: True if "j halt".find(self.separated[i][1]) != -1 else False

    directive = lambda self, i: True if ".fill .space".find(self.separated[i][1]) != -1 else False
