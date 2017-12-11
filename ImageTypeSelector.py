import sys, os
import glob
import pandas as pd
import shutil
import datetime

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

import selectorUI

class XMainWindow(QMainWindow, selectorUI.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.nextButton.clicked.connect(self.nextImage)
        self.saveButton.clicked.connect(self.saveResult)
        self.benignButton.clicked.connect(self.radioButtonClicked)
        self.cancerButton.clicked.connect(self.radioButtonClicked)
        
        self.inputData = InputDataHandler("data")
        self.selectionResults = SelectionResultsHandler(self.inputData)
        self.restore()
        self.current_selection = "benign"
        self.updateImage()    

    def restore(self):
        if os.path.isfile(self.selectionResults.out_path):
            self.selectionResults.restoreFromPreviousWorks()
            self.inputData.restoreFromPreviousWorks(self.selectionResults.current_data_index_list)
            self.loadDataset(self.inputData.current_folder_index)

    def closeEvent(self, event):
        self.selectionResults.export()

    def nextImage(self):
        assert self.current_selection in ["benign", "cancer"], "Invalid selection: %s" % (self.current_selection)
        self.selectionResults.saveSelection(self.inputData.current_folder_index, self.inputData.currentDataIndex(), self.current_selection)
        try:
            self.inputData.nextData()
        except IndexError:
            QMessageBox.information(self, 'Last Image', "This is the last image of the current dataset.\nSwitch to the next dataset.", QMessageBox.Ok, QMessageBox.Ok)
            self.loadDataset(self.inputData.current_folder_index + 1)
        else:
            self.updateImage()
    
    def updateImage(self):
        self.showImage()
        self.currentImageIndex.setText(str(self.inputData.currentDataIndex()+1))

    def showImage(self):
        path = self.inputData.currentDataName()
        assert os.path.isfile(path), "No accessible file: %s" % path
        tumor = QtGui.QPixmap(path)
        self.tumorImage.setPixmap(tumor.scaled(self.tumorImage.width(), self.tumorImage.height(), QtCore.Qt.KeepAspectRatio))

    def saveResult(self):
        self.selectionResults.export()

    def radioButtonClicked(self):
        if self.cancerButton.isChecked():
            self.current_selection = "cancer"
        else: # self.benignButton.isChecked():
            self.current_selection = "benign"

    def loadDataset(self, num):
        try:
            self.inputData.changeDataset(num)
        except IndexError("Dataset you choose is already done."):
            QMessageBox.information(self, 'Last Image', "Dataset you choose is already done.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.curDataset.setText(str(self.inputData.current_folder_index))
            self.numOfWholeImages.setText(str(self.inputData.numberOfCurrentData()))
            self.updateImage()
    

class InputDataHandler():
    def __init__(self, origin_path):
        self.origin_path = origin_path
        self.num_folders = 15
        self.current_folder_index = 0
        self.current_data_index_list = [0 for _ in range(self.num_folders)]
        self.number_of_data_list = []
        for i in range(self.num_folders):
            data_path = os.path.join(self.origin_path, "{0:02}".format(self.current_folder_index), "*.jpg")
            self.number_of_data_list.append(len(glob.glob(data_path)))
    
    def restoreFromPreviousWorks(self, current_data_index_list):
        self.current_data_index_list = current_data_index_list
        for i, (cur_data_idx, num_of_data) in enumerate(zip(self.current_data_index_list, self.number_of_data_list)):
            if cur_data_idx < num_of_data:
                self.current_folder_index = i
                break

    def currentDataFolder(self):
        cur_folder_name = "{0:02}".format(self.current_folder_index)
        return os.path.join(self.origin_path, cur_folder_name)

    def currentDataName(self):
        cur_data_name = "{0:03}.jpg".format(self.current_data_index_list[self.current_folder_index])
        return os.path.join(self.currentDataFolder(), cur_data_name)
    
    def currentDataIndex(self):
        return self.current_data_index_list[self.current_folder_index]

    def numberOfCurrentData(self):
        return self.number_of_data_list[self.current_folder_index]

    def changeDataset(self, idx):
        assert idx >= 0 and idx < self.num_folders, 'out of boundary'
        data_folder_path = os.path.join(self.origin_path, "{0:02}".format(idx))
        assert os.path.isdir(data_folder_path), "No accessible folder: %s" % data_folder_path
        self.current_folder_index = idx
        if self.current_data_index_list[self.current_folder_index] >= self.numberOfCurrentData():
            raise IndexError("Last Image")

    def nextData(self):
        self.current_data_index_list[self.current_folder_index] += 1
        if self.current_data_index_list[self.current_folder_index] >= self.numberOfCurrentData():
            raise IndexError("Last Image")
    

class SelectionResultsHandler():
    def __init__(self, inputDataHandler):
        self.out_path = "result.csv"
        self.num_folderes = 15
        self.table_schema = ["folder", "file", "selection"]
        assert len(inputDataHandler.number_of_data_list) == self.num_folderes, "The number of the output folder should be same with the number of the input folder"
        self.number_of_data_list = inputDataHandler.number_of_data_list
        self.current_data_index_list = inputDataHandler.current_data_index_list
        self.selectionDict = {}
    
    def restoreFromPreviousWorks(self):
        assert os.path.isfile(self.out_path), "No accessible file: %s" % self.out_path
        assert len(self.selectionDict) == 0, "selectionDict does not empty."
        df = pd.read_csv(self.out_path)
        folder_to_file_dict = {}
        for index, row in df.iterrows():
            folder_to_file_dict[row['folder']] = row['file']
            self.selectionDict[(row['folder'], row['file'])] = row['selection']
        for i in range(self.num_folderes):
            if i in folder_to_file_dict.keys():
                self.current_data_index_list[i] = folder_to_file_dict[i] + 1
        

    def saveSelection(self, folder_idx, data_idx, selection):
        assert isinstance(folder_idx, int), "Invalid type of folder_idx: %s" % (type(folder_idx))
        assert isinstance(data_idx, int), "Invalid type of data_idx: %s" % (type(data_idx))
        assert isinstance(selection, str), "Invalid type of selection: %s" % (type(selection))
        assert folder_idx >= 0 and folder_idx < self.num_folderes, 'Out of bounds'
        assert data_idx >= 0 and data_idx < self.number_of_data_list[folder_idx], 'Out of bounds'
        assert selection in ["benign", "cancer"], "Invalid selction: %s" % selection
        self.selectionDict[(folder_idx, data_idx)] = selection

    def export(self):
        csv_list = []
        for key, value in self.selectionDict.items():
            folder = key[0]
            filename = key[1]
            selection = value
            row = (folder, filename, selection)
            csv_list.append(row)
        df = pd.DataFrame(csv_list, columns=self.table_schema)
        df.to_csv(self.out_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = XMainWindow()
    mainwindow.show()
    app.exec_()