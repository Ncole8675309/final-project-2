import numpy as np
from PyQt5.QtWidgets import *
from Matrix_Mover_Gui import Ui_MainWindow
# this is the main programming that creates the matrix and allows for transposition

class commands(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs): #the matrix array should be kept to a 5 x 5 matrix. starting values can be changed
        self.cryptex = np.array([["A", "B", "C", "D", "E"],
                                ["F", "G", "H", "I", "J"],
                                ["K", "L", "M", "N", "O"],
                                ["P", "Q", "R", "S", "T"],
                                ["U", "V", "W", "X", "Y"]])
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        global key
        key = "" #the variable key is used to store the encryption method so others can decode the message

        #sets the values in the matrix on the GUI to the values in the code
        self.updatingMatrix()

        #connecting the buttons to the masterfunct method. yes it's unintuitive but I'm not sure how to use loops with
        #different objects with different names, not do I have the redbull to figure such issue out
        self.btnR.clicked.connect(lambda: self.masterfunct("R"))
        self.btn2R.clicked.connect(lambda: self.masterfunct("2R"))
        self.btnRP.clicked.connect(lambda: self.masterfunct("R'"))
        self.btn2RP.clicked.connect(lambda: self.masterfunct("2R'"))
        self.btnL.clicked.connect(lambda: self.masterfunct("L"))
        self.btnLP.clicked.connect(lambda: self.masterfunct("L'"))
        self.btn2L.clicked.connect(lambda: self.masterfunct("2L"))
        self.btn2LP.clicked.connect(lambda: self.masterfunct("2L'"))
        self.btnM.clicked.connect(lambda: self.masterfunct("M"))
        self.btnMP.clicked.connect(lambda: self.masterfunct("M'"))
        self.btnU.clicked.connect(lambda: self.masterfunct("U"))
        self.btnUP.clicked.connect(lambda: self.masterfunct("U'"))
        self.btn2U.clicked.connect(lambda: self.masterfunct("2U"))
        self.btn2UP.clicked.connect(lambda: self.masterfunct("2U'"))
        self.btnE.clicked.connect(lambda: self.masterfunct("E"))
        self.btnEP.clicked.connect(lambda: self.masterfunct("E'"))
        self.btnD.clicked.connect(lambda: self.masterfunct("D"))
        self.btnDP.clicked.connect(lambda: self.masterfunct("D'"))
        self.btn2D.clicked.connect(lambda: self.masterfunct("2D"))
        self.btn2DP.clicked.connect(lambda: self.masterfunct("2D'"))

        #below is the code that runs when the user is done shifting the matrix and wants to encrypt their message
        self.btnEncrypt.clicked.connect(lambda: self.encryption())


    def colup(self, col):
        #transposes the matrix to access the first column (row when transposed)
        #once done, it calls the rowleft function and transposes again, ending with the correct orientation
        self.cryptex = self.cryptex.transpose()
        self.rowleft(col)
        self.cryptex = self.cryptex.transpose()

    def coldown(self, col):
        #Transposes the matrix to access the first column (row when transposed)
        #once done, it calls the rowright function and transposes once again, getting the correct orientation
        self.cryptex = self.cryptex.transpose()
        self.rowright(col)
        self.cryptex = self.cryptex.transpose()

    def rowleft(self, row):
        #accesses the row, stores the first value, and shifts all other values from right to left one spot
        #the first value is placed at the end once all shifting is complete
        temp_variable = self.cryptex[row][0] #storing the *would be* overwritten value before shifting
        i = 1
        while i < len(self.cryptex[row]):
            self.cryptex[row][i - 1] = self.cryptex[row][i]
            i = i + 1
        self.cryptex[row][-1] = temp_variable

    def rowright(self, row):
        #accesses the row, stores the last value, and shifts all other values from left to right one spot
        #the last value is placed at the beginning once all shifting is complete
        temp_variable = self.cryptex[row][-1] #storing the *would be* overwritten value before shifting
        i = len(self.cryptex[row]) - 1
        while i > 0:
            self.cryptex[row][i] = self.cryptex[row][i - 1]
            i = i - 1
        self.cryptex[row][0] = temp_variable

    def keyshift(self, notat, has_reversal):
        #takes in commands from the master function for all functions in commands
        #using custom notation similar to rubix cube notation
        #(https://ruwix.com/the-rubiks-cube/notation/) for refrence on simple notation
        #(https://ruwix.com/the-rubiks-cube/notation/advanced/) for refrence on all other notations used
        if "3" in notat and "w" in notat:
            span = 3        #set's how many rows or columns need to be rotated at once(1, 2, or 3)
        elif "w" in notat:
            span = 2
        elif "2" in notat:
            span = 2
            needs_breaking = True
        else:
            span = 1
            needs_breaking = False
        while span > 0:
            if has_reversal: #opposite from notation's original direction
                if "D" in notat:
                    self.rowleft(5 - span)
                elif "R" in notat:
                    self.coldown(5 - span)
                elif "U" in notat:
                    self.rowright(span - 1)
                elif "L" in notat:
                    self.colup(span - 1)
                elif "M" in notat:
                    self.colup(2)
                elif "E" in notat:
                    self.rowleft(2)
            else: #normal notation for rubix cube algorithms
                if "D" in notat:
                    self.rowright(5 - span)
                elif "R" in notat:
                    self.colup(5 - span)
                elif "U" in notat:
                    self.rowleft(span - 1)
                elif "L" in notat:
                    self.coldown(span - 1)
                elif "M" in notat:
                    self.coldown(2)
                elif "E" in notat:
                    self.rowright(2)
            if needs_breaking:
                break
            else:
                span = span - 1 #shifts to the next column outward, otherwise ends


    def masterfunct(self, notation):
        #controlls all other functions in commands
        #used to loop keyshift so as to not confuse other programmers with notation
        if notation[-1].isnumeric():
            looping_counter = int(notation[-1]) #int controlling how many loops to run
            notation = notation[0, len(notation) - 2]
        else:
            looping_counter = 0 #if no looping is needed, loop only once
        if "'" in notation:
            has_reversal = True #if it's a prime rotation, meaning it goes the opposite direction
        else:
            has_reversal = False
        while looping_counter > -1: #how many times the selected columns or rows need to rotate
            self.keyshift(notation, has_reversal)
            looping_counter = looping_counter - 1
        global key
        key = key + notation + " " #adds the latest shift of the matrix to the decryption key
        self.updatingMatrix() #updates the matrix for the user to see the changes performed

    def encryption(self): #encrypting the text data in the txtMessage textbox
        listing_matrix = self.cryptex.tolist() #putting the data in an accessable state (for some reason keeping it as a matrix doesn't work)
        message = self.txtMessage.text()
        message = message.upper() #getting the text and putting it into all capital letters for the replace method
        j = 0
        k = 0
        while j < 5:
            while k < 5:
                message = message.replace(str(listing_matrix[j][k]), "(" + str(j) + "," + str(k) + ") ")
                k += 1 #checks each location on the matrix and replaces every instance of the letter with it's coordinates)
            j += 1
            k = 0
        message = message.replace("z", "") #removes any leftover characters (z)
        self.lblEncrypted.setText("Key: " + key + "\n Message: " + message) #displays the encrypted message and it's key
        global key
        key = ""
        self.txtMessage.setText("") #resets the key and the message to encrypt

    def updatingMatrix(self):
        #updates each label in the group to display the changes in the matrix for the user
        #(yes it's unintuitive but the labels names don't follow a pattern when copied so a loop wouldn't work unless
        #I went in and changed every label's name to work, and even then I don't know how to loop with different objects)
        self.lblValue.setText(str(self.cryptex[0][0]))
        self.lblValue_2.setText(str(self.cryptex[0][1]))
        self.lblValue_3.setText(str(self.cryptex[0][2]))
        self.lblValue_4.setText(str(self.cryptex[0][3]))
        self.lblValue_5.setText(str(self.cryptex[0][4]))
        self.lblValue_6.setText(str(self.cryptex[1][1]))
        self.lblValue_7.setText(str(self.cryptex[1][3]))
        self.lblValue_8.setText(str(self.cryptex[1][2]))
        self.lblValue_9.setText(str(self.cryptex[1][4]))
        self.lblValue_10.setText(str(self.cryptex[1][0]))
        self.lblValue_11.setText(str(self.cryptex[2][1]))
        self.lblValue_12.setText(str(self.cryptex[2][3]))
        self.lblValue_13.setText(str(self.cryptex[2][2]))
        self.lblValue_14.setText(str(self.cryptex[2][4]))
        self.lblValue_15.setText(str(self.cryptex[2][0]))
        self.lblValue_16.setText(str(self.cryptex[3][1]))
        self.lblValue_17.setText(str(self.cryptex[3][3]))
        self.lblValue_18.setText(str(self.cryptex[3][2]))
        self.lblValue_19.setText(str(self.cryptex[3][4]))
        self.lblValue_20.setText(str(self.cryptex[3][0]))
        self.lblValue_21.setText(str(self.cryptex[4][1]))
        self.lblValue_22.setText(str(self.cryptex[4][3]))
        self.lblValue_23.setText(str(self.cryptex[4][2]))
        self.lblValue_24.setText(str(self.cryptex[4][4]))
        self.lblValue_25.setText(str(self.cryptex[4][0]))