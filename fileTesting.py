
def get_data_from_file(infile):
    my_file = open(infile, "r")
    data_line = my_file.readline()
    database = []
    while data_line:
        data_lst = data_line.split()
        database.append(data_lst)
        data_line = my_file.readline()
    my_file.close()
    return database

def write_data_to_file(outfile, wanted_data): #list
    #["Trung", "89", "1m3"]
    my_file = open(outfile, "a")
    finalize_string = " ".join(wanted_data)
    my_file.write(finalize_string + "\n")
    my_file.close()





def main():
    target_file = "data.txt"
    testing_lst = ["Trungaka", "60", "1m4"]
    print(get_data_from_file(target_file))
    write_data_to_file(target_file, testing_lst)


if __name__ == '__main__':
    main()