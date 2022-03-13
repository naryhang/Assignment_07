#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# NHang, 2022-Mar-04, Modified processing code
# NHang, 2022-Mar-05, Modified presentation code
# NHang, 2002-Mar-11, Adding structured error handling
# NHang, 2002-Mar-12, Adding pickling
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file (binary)
objFile = None  # file object
strID = None # added empty variable
strTitle = None # added empty variable
strArtist = None # added empty variable


# -- PROCESSING -- #
# adding pickling 
import pickle

class DataProcessor:
    # TO DONE add functions for processing here
    # Created def to add CD
    # Moved code over from presentation I/O 
    # Updated code to match attributes
    def adding_cd(table):
        intID, strTitle, strArtist = IO.user_inputs() 
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(table)
        
    # Created def to delete CD
    # Moved code over from presentation I/O
    # Updated code to match attributes
    # Adding try/except
    def deleting_cd(table):
        intRowNr = -1
        blnCDRemoved = False
        try:
            for row in lstTbl:
                intRowNr += 1
                if row['ID'] == intIDDel:
                    del table[intRowNr]
                    blnCDRemoved = True
        except ValueError:
            print('Could not find this CD!') # not working
        else:
            if blnCDRemoved:
                print('The CD was removed')
        return table
        

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # adding structured error handling for read file
        try:
            with open(file_name, 'r') as objFile:
            #objFile = open(file_name, 'r')
            # read file name
                table.clear()  # this clears existing data and allows to load data from file
                for line in objFile:
                    data = line.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow)
                    #pickling
                    with open(file_name, 'rb') as file:
                        table = pickle.load(file)
                    objFile.close()
                    break
        except FileNotFoundError: # can't find file referencing
            print('The file is not found, check file location')
        return table

    @staticmethod
    def write_file(file_name, table):
        # TO DONE Add code here
        # Moved code over from presentation I/O 
        # Updated code to match attributes
        # adding structured error handling for write file
        try:
            #with open(strFileName, 'wb') as file:
                #pickle.dump(table, file)
            with open(file_name, 'w') as objFile:
            #objFile = open(file_name, 'w')
                for row in table:
                    lstValues = list(row.values())
                    lstValues[0] = str(lstValues[0])
                    objFile.write(','.join(lstValues) + '\n')
                    # unpickling
                    # read from a binary file
                    with open(strFileName,'wb') as file:
                        pickle.dump(table, file)
                objFile.close()             
        except FileNotFoundError: # opening file does not exist 
            print('Error: No such file or directory')
        return table
        

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        try:
        # adding structered error handling
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                raise ValueError
        except ValueError as e:
            print(type(e))
            print('Enter a valid menu selection')
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TO DONE add I/O functions as needed
    # Move CD adding inputs over into functions 
    # Adding structured error handling for int
    @staticmethod
    def user_inputs():
        validID = False
        while not validID:
            try:
                # used float for non digits 
                strID = float(input('Enter ID: ').strip())
            except ValueError: # inappropriate value error
                print('That was not a number!')
            else:
                validID = True
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        intID = int(strID)
        return intID, strTitle, strArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TO DONE move IO code into function
        # IO.user_inputs() *Delete-causing duplicates
        # 3.3.2 Add item to the table
        # TO DONE move processing code into function
        # Call function 
        DataProcessor.adding_cd(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        # TO DONE move processing code into function
        # Call function
        DataProcessor.deleting_cd(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TO DONE move processing code into function
            # Call write function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




