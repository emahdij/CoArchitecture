from MiniAture import Miniature


miniature=Miniature("E:\\assemble.txt")
miniature.scan()
print("_-_-_-_-_-_-_-_-_-_-")
print("")
miniature.print_file()
miniature.file_translate()
print("----------------------")
print(miniature.separated)
print(miniature.machinecode)
print(miniature.SymbolTable)
# miniature.print_bin_file()
miniature.print_decimalcode()


