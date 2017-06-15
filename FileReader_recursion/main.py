"""
    author: Aljaž Jelen
    title:  AVL 2nd round
    date:   15/06/2017
    IDE:    PyCharm

"""

import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QDialog, QSizePolicy,
                            QPushButton, QApplication, QMessageBox,
                            QFileDialog,  QGroupBox, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPalette, QIcon

import string

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure




class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=4, dpi=100, word_list=0):
        """ Class for creating embedded Matplotlib widgets
        :param width:       width of widget
        :param height:      height of widget
        :param dpi:         dpi resolution of plot
        :param word_list:   list of words/letters
        """
        self.word_list = word_list

        # Find background color of window and set same for figure
        c = ex.palette().color(QPalette.Background)
        fig = Figure(figsize=(width, height), dpi=dpi,facecolor=((c.red()/255,c.green()/255,c.blue()/255)))
        # Add axes to figure
        self.axes = fig.add_subplot(111)
        # Set stretching policy in terms of resizing
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        # Update geometry
        FigureCanvas.updateGeometry(self)
        # Call plotting routine
        self.plot()
        # Set tight layout
        fig.tight_layout()

    def plot(self):
        """ Method with plotting routine
        :return:
        """
        # Get data - number of first letters
        data = self.word_list
        # Set number of x-ticks
        x = np.arange(0,len(string.ascii_lowercase))
        # Add axes to figure
        ax = self.figure.add_subplot(111)
        # Make right and top spines invisible
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # Find background color of window and set same for ploting area of ax
        c = ex.palette().color(QPalette.Background)
        ax.set_facecolor((c.red()/255,c.green()/255,c.blue()/255))
        # Set number and step of ticks to match position of letters
        ax.xaxis.set_ticks(np.arange(min(x), max(x) + 1, 1.0))
        # Get only lower case letter by ASCII
        a = string.ascii_lowercase
        # Set x ticks to match letters
        ax.set_xticklabels(a)
        # Delete y ticks for more fancy look
        ax.set_yticklabels([])
        # Plot data in bar-like manner
        bars = ax.bar(x, data, 0.6, color='C1')
        # Change even bars color to blue
        for bar in bars[::2]: bar.set_color('C0')
        # Draw changes
        self.draw()


class Example(QMainWindow):
    def __init__(self):
        """ Class with an example code
        """
        super().__init__()
        # Initialize UI
        self.initUI()
        # Make fileNames variable
        self.fileNames = []

    def initUI(self):
        # Initialize top group
        self.initTop()
        # Initialize bottom group
        self.initBot()
        # Create main group box and assign layout
        mainGroup = QGroupBox()
        mainLayout = QVBoxLayout()
        # Add top and bottom group widgets to main widget
        mainLayout.addWidget(self.topGroup,1)
        mainLayout.addWidget(self.botGroup,10)
        mainGroup.setLayout(mainLayout)
        # Set main group with main layout to be central widget
        self.setCentralWidget(mainGroup)
        # Set fancy stuff
        self.setGeometry(400, 400, 550, 400)
        self.setWindowTitle('File statistics')
        self.show()

    def initTop(self):
        """ Method for initializing top box
        :return:        None
        """
        # Choose horizontal layout
        toplayout = QHBoxLayout()
        # Instantiate textEdit and 2 buttons
        textEdit = QTextEdit(self)
        diag = QPushButton('', self)
        searchFilesbtn = QPushButton('>>', self)
        # Set textEdit properties and make it read only
        textEdit.setMaximumHeight(diag.height()*0.8)
        textEdit.setReadOnly(True)
        self.contentPath = textEdit
        toplayout.addWidget(textEdit)
        # Set properties for button for opening file-modal and assign slot
        searchFilesbtn.clicked.connect(self.showDialog)
        toplayout.addWidget(searchFilesbtn)
        # Set properties for button for opening plot-modal and assign slot
        diag.clicked.connect(self.showDiagram)
        diag.setIcon(QIcon('bar.png'))
        diag.resize(diag.sizeHint())
        toplayout.addWidget(diag)
        # Create top group and assign layout
        self.topGroup = QGroupBox("Horizontal top")
        self.topGroup.setLayout(toplayout)


    def initBot(self):
        """ Method for initializing bot box
        :return:        None
        """
        # Choose horizontal layout
        botlayout = QHBoxLayout()
        # Instantiate textEdit, set properties and read only
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        self.folderContent = textEdit
        botlayout.addWidget(textEdit)
        # Create bottom group and assign layout
        self.botGroup = QGroupBox("Horizontal bot")
        self.botGroup.setLayout(botlayout)

    def showDiagram(self):
        """ Method for showing diagram dialog
        :return:    None
        """
        print((self.fileNames))
        #if len(self.fileNames) > 0:
        if (self.fileNames):
            print("HERE")
            # Instantiate dialog
            my_dialog = QDialog(self)
            my_dialog.setWindowTitle("Filename's first letter distribution")
            # Choose general dialog layout
            layout = QVBoxLayout()
            # Instantiate plotting canvas
            diagram = PlotCanvas(self, width=5, height=4, word_list=self.sortByFirstLetter())
            # Add canvas to general layout
            layout.addWidget(diagram)
            # Instantiate button, connect the signal and resize
            qbtn = QPushButton('Close', self)
            qbtn.clicked.connect(my_dialog.close)
            qbtn.resize(qbtn.sizeHint())
            # Choose layout for button, change stretch and add button
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(qbtn)
            # Add button layout to general layout and set this dialog layout
            layout.addLayout(hbox)
            my_dialog.setLayout(layout)
            # Execute dialog
            my_dialog.exec_()
        else:
            reply = QMessageBox.question(self, 'Warning',
                                         "Please select a directory.", QMessageBox.Ok)

    def sortByFirstLetter(self):
        """ Method to sort and return items according to first letter
        :return:        Sorted list of items at selected path
        """
        temp = sorted(self.fileNames,key=lambda s: s.lower())
        temp = self.fileNames
        letter_count = []
        for letter in string.ascii_lowercase:
            letter_count.append(len([i for i in temp if i[0] == letter or i[0] == letter.capitalize()]))
            #for file in self.fileNames:
            #    sort = file[0] in string.ascii_letters
            #x_domain.append()
        #ind = [i for i in temp if i[0] == 'a']
        #print(ind)
        return letter_count

    def showDialog(self):
        """ Method for showing file dialog
        :return:    None
        """
        self.fileNames = []
        # path is a QString containing the path to the directory you selected
        path = QFileDialog.getExistingDirectory(self, "Get Dir Path")
        if path:
            # set text of label to chosen path
            self.contentPath.setText(path)
            # get a content from the path directory:
            content = self.getContent(path)

            if content:
                status = self.recursion(path)
                if status == 1000:
                    reply = QMessageBox.question(self, 'Message',
                                                "More than 1000 files found, terminating process.", QMessageBox.Ok)
                else:
                    reply = QMessageBox.question(self, 'Message',
                                                 str(status) + " files found.", QMessageBox.Ok)

    def getContent(self,path):
        """ Gets files and folders at given path
        :return:        list of items at given path
        """
        return [name for name in os.listdir(str(path))]

    def isFolder(self,f):
        """ Gets type of given folder/file
        :return: 0 if file, 1 if folder
        """
        return os.path.isdir(f)

    def recursion(self,path):
        """ Method used to find all files in given folder and subfolders
            using recursive approach
        :param path:    Path of given directory
        :return:        Number of files found
        """
        # Get content at given path
        files = self.getContent(path)

        # For each item in directory
        for file in files:
            # Check if number of items already exceeds 1000
            if len(self.fileNames) < 1000:
                # Check if item is folder and rerun routine if so
                if self.isFolder(path + "/" + file):
                    self.recursion(path + "/" + file)
                else:   # Item is file, append fo fileNames variable and display it
                    self.folderContent.insertPlainText(file + "\n")
                    self.fileNames.append(file)
            else:
                return len(self.fileNames)
        return len(self.fileNames)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


