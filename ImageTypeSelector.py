import sys, os
import glob
import pandas as pd
import shutil
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

import selectorUI

class XMainWindow(QMainWindow, selectorUI.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.benignButton.clicked.connect(self.radioButtonClicked)
        self.cancerButton.clicked.connect(self.radioButtonClicked)
        
        self.out_path = 'results'
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path)
        self.in_path = 'data'
        self.input_data = InputDataHandler(self.in_path)
        self.selection_results = SelectionResultsHandler(self.input_data, self.out_path)
        self.restore()
        self.current_selection = "benign"
        self.updateImage()

    def restore(self):
        if os.path.isfile(self.selection_results.backup_path):
            self.selection_results.restoreFromPreviousWorks()
            self.input_data.restoreFromPreviousWorks(self.selection_results.current_data_index_list)
            self.loadDataset(self.input_data.current_folder_index)

    def closeEvent(self, event):
        self.saveResult()

    def nextImage(self):
        assert self.current_selection in ["benign", "cancer"], "Invalid selection: %s" % (self.current_selection)
        self.selection_results.saveSelection(self.input_data.current_folder_index, self.input_data.currentDataIndex(), self.current_selection)
        try:
            self.input_data.nextData()
        except IndexError:
            reply = QMessageBox.question(self, 'Last Image', "This is the last image of the current dataset.\nDo you want to export the result file and switch to the next dataset?\nAfter Switching, you cannot change selections of current Dataset.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveResult()
                if self.input_data.current_folder_index + 1 == 15:
                    QMessageBox.information(self, 'Last Dataset', "This is the last dataset.\nClose program.", QMessageBox.Ok, QMessageBox.Ok)
                    self.close()
                    return
                self.loadDataset(self.input_data.current_folder_index + 1)
            else:
                self.input_data.prevData()
        else:
            self.updateImage()

    def prevImage(self):
        assert self.current_selection in ["benign", "cancer"], "Invalid selection: %s" % (self.current_selection)
        self.selection_results.saveSelection(self.input_data.current_folder_index, self.input_data.currentDataIndex(), self.current_selection)
        try:
            self.input_data.prevData()
        except IndexError:
            QMessageBox.information(self, 'First Image', "This is the first image of the current dataset.\nDo nothing.", QMessageBox.Ok, QMessageBox.Ok)
            self.input_data.nextData()
        else:
            self.updateImage()

    def updateImage(self):
        self.showImage()
        self.currentImageIndex.setText(str(self.input_data.currentDataIndex()+1))
        try:
            selection = self.selection_results.getSelection(self.input_data.current_folder_index, self.input_data.currentDataIndex())
        except KeyError:
            self.benignButton.setChecked(True)
            self.current_selection = "benign"
        else:
            if selection == "benign":
                self.benignButton.setChecked(True)
            elif selection == "cancer":
                self.cancerButton.setChecked(True)
            self.radioButtonClicked()

    def showImage(self):
        path = self.input_data.currentDataName()
        assert os.path.isfile(path), "No accessible file: %s" % path
        tumor = QtGui.QPixmap(path)
        self.tumorImage.setPixmap(tumor.scaled(self.tumorImage.width(), self.tumorImage.height(), QtCore.Qt.KeepAspectRatio))

    def saveResult(self):
        self.selection_results.export()

    def radioButtonClicked(self):
        if self.cancerButton.isChecked():
            self.current_selection = "cancer"
        else: # self.benignButton.isChecked():
            self.current_selection = "benign"

    def loadDataset(self, num):
        try:
            self.input_data.changeDataset(num)
        except IndexError("Dataset you choose is already done."):
            QMessageBox.information(self, 'Last Image', "Dataset you choose is already done.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.curDataset.setText(str(self.input_data.current_folder_index))
            self.numOfWholeImages.setText(str(self.input_data.numberOfCurrentData()))
            self.updateImage()
    

class InputDataHandler():
    def __init__(self, origin_path):
        self.origin_path = origin_path
        self.num_folders = 15
        self.current_folder_index = 0
        self.current_data_index_list = [0 for _ in range(self.num_folders)]
        self.number_of_data_list = []
        for i in range(self.num_folders):
            data_path = os.path.join(self.origin_path, "{0:02}".format(i), "*.jpg")
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
            self.current_data_index_list[self.current_folder_index] -= 1
        elif self.current_data_index_list[self.current_folder_index] < 0:
            self.current_data_index_list[self.current_folder_index] += 1

    def nextData(self):
        self.current_data_index_list[self.current_folder_index] += 1
        if self.current_data_index_list[self.current_folder_index] >= self.numberOfCurrentData():
            raise IndexError("Last Image")

    def prevData(self):
        self.current_data_index_list[self.current_folder_index] -= 1
        if self.current_data_index_list[self.current_folder_index] < 0:
            raise IndexError("First Image")
    

class SelectionResultsHandler():
    def __init__(self, inputDataHandler, out_folder):
        assert os.path.isdir(out_folder), "out_folder does not exist: %s" % out_folder
        self.backup_path = "backup.imagetypeselector"
        self.result_file_pattern = os.path.join(out_folder, "result_%d%s.csv")
        self.num_folderes = 15
        self.table_schema = ["folder", "file", "selection"]
        assert len(inputDataHandler.number_of_data_list) == self.num_folderes, "The number of the output folder should be same with the number of the input folder"
        self.number_of_data_list = inputDataHandler.number_of_data_list
        self.current_data_index_list = inputDataHandler.current_data_index_list
        self.selection_dict = {}
    
    def restoreFromPreviousWorks(self):
        assert os.path.isfile(self.backup_path), "No accessible file: %s" % self.backup_path
        assert not self.selection_dict, "selection_dict does not empty."
        backup_df = pd.read_csv(self.backup_path)
        folder_to_file_dict = {}
        for _, row in backup_df.iterrows():
            folder_to_file_dict[row['folder']] = row['file']
            self.selection_dict[(row['folder'], row['file'])] = row['selection']
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
        self.selection_dict[(folder_idx, data_idx)] = selection

    def getSelection(self, folder_idx, data_idx):
        assert isinstance(folder_idx, int), "Invalid type of folder_idx: %s" % (type(folder_idx))
        assert isinstance(data_idx, int), "Invalid type of data_idx: %s" % (type(data_idx))
        assert folder_idx >= 0 and folder_idx < self.num_folderes, 'Out of bounds'
        assert data_idx >= 0 and data_idx < self.number_of_data_list[folder_idx], 'Out of bounds'
        return self.selection_dict[(folder_idx, data_idx)]

    def export(self):
        backup_list = []
        result_file_list = [[] for _ in range(self.num_folderes)]
        for key, value in self.selection_dict.items():
            folder = key[0]
            filename = key[1]
            selection = value
            row = (folder, filename, selection)
            backup_list.append(row)
            result_file_list[folder].append(row[1:])
        backup_df = pd.DataFrame(backup_list, columns=self.table_schema)
        backup_df.to_csv(self.backup_path)
        for i, result_file in enumerate(result_file_list):
            if result_file:
                if os.path.exists(self.result_file_pattern % (i, "")):
                    continue
                result_df = pd.DataFrame(result_file, columns=self.table_schema[1:])
                if len(result_file) == self.number_of_data_list[i]: # done dataset
                    result_df.to_csv(self.result_file_pattern % (i, ""))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = XMainWindow()
    mainwindow.show()
    app.exec_()