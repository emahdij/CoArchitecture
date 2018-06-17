from MiniAture import Miniature

# assemble E:\\assemble.txt E:\\program.mc
arg = ""
while arg.split(" ")[0] != "assemble":
    arg = input()
miniature = Miniature(arg)
miniature.scan()
print("-----------------------------")
miniature.file_translate()
print("file translated")
miniature.unCheck()
print("-----------------------------")
miniature.print_bin_file()
print("-----------------------------")
miniature.print_decimalcode()
print("-----------------------------")
miniature.savefile()
# print(miniature.recognized)
# print(miniature.separated)
# print(miniature.SymbolTable)
