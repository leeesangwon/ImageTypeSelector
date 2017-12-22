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

        self.nextImageButton.clicked.connect(self.nextImage)
        self.prevImageButton.clicked.connect(self.prevImage)
        self.nextPatientButton.clicked.connect(self.nextPatient)
        self.prevPatientButton.clicked.connect(self.prevPatient)
        self.benignButton.clicked.connect(self.radioButtonClicked)
        self.cancerButton.clicked.connect(self.radioButtonClicked)
        self.ambiguousCheckBox.stateChanged.connect(self.changeAmbiguity)
        
        self.out_path = 'results'
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path)
        self.in_path = 'data_per_patient'
        self.input_data = InputDataHandler(self.in_path)
        self.selection_results = SelectionResultsHandler(self.input_data, self.out_path)
        self.restore()
        self.loadDataset(self.input_data.current_folder_index)

    def restore(self):
        if os.path.isfile(self.selection_results.backup_path):
            self.selection_results.restoreFromPreviousWorks()
            self.input_data.restoreFromPreviousWorks(self.selection_results.current_patient_dict)

    def closeEvent(self, event):
        self.saveResult()

    def nextPatient(self):
        assert self.selection_results.current_selection in ["benign", "cancer"], "Invalid selection: %s" % (self.selection_results.current_selection)
        self.selection_results.saveSelection(self.input_data.current_folder_index, self.input_data.currentPatientIndex())
        try:
            self.input_data.nextPatient()
        except IndexError:
            reply = QMessageBox.question(self, 'Last Patient', "This is the last patient of the current dataset.\nDo you want to export the result file and switch to the next dataset?\nAfter Switching, you cannot change selections of current Dataset.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveResult()
                if self.input_data.current_folder_index + 1 == self.input_data.num_folders:
                    QMessageBox.information(self, 'Last Dataset', "This is the last dataset.\nClose program.", QMessageBox.Ok, QMessageBox.Ok)
                    self.close()
                    return
                self.loadDataset(self.input_data.current_folder_index + 1)
            else:
                self.input_data.prevPatient()
        else:
            self.updatePatient()

    def prevPatient(self):
        assert self.selection_results.current_selection in ["benign", "cancer"], "Invalid selection: %s" % (self.selection_results.current_selection)
        self.selection_results.saveSelection(self.input_data.current_folder_index, self.input_data.currentPatientIndex())
        try:
            self.input_data.prevPatient()
        except IndexError:
            QMessageBox.information(self, 'First Patient', "This is the first patient of the current dataset.\nDo nothing.", QMessageBox.Ok, QMessageBox.Ok)
            self.input_data.nextPatient()
        else:
            self.updatePatient()

    def updatePatient(self):
        self.updateImage()
        self.numOfWholeImages.setText(str(self.input_data.numberOfCurrentData()))
        self.currentPatientIndex.setText(str(self.input_data.currentPatientIndex() + 1))
        try:
            selection, ambiguity = self.selection_results.getSelection(self.input_data.current_folder_index, self.input_data.currentPatientIndex())
        except KeyError:
            self.benignButton.setChecked(True)
            self.selection_results.current_selection = "benign"
            self.ambiguousCheckBox.setChecked(False)
            self.selection_results.current_ambiguity = False
        else:
            if selection == "benign":
                self.benignButton.setChecked(True)
            elif selection == "cancer":
                self.cancerButton.setChecked(True)
            self.radioButtonClicked()
            if ambiguity:
                self.ambiguousCheckBox.setChecked(True)
            else:
                self.ambiguousCheckBox.setChecked(False)
            self.changeAmbiguity()

    def nextImage(self):
        self.input_data.nextData()
        self.updateImage()

    def prevImage(self):
        self.input_data.prevData()
        self.updateImage()

    def updateImage(self):
        self.showImage()
        self.currentImageIndex.setText(str(int(os.path.splitext(self.input_data.currentDataName())[0])+1))

    def showImage(self):
        path = self.input_data.currentDataPath()
        assert os.path.isfile(path), "No accessible file: %s" % path
        tumor = QtGui.QPixmap(path)
        self.tumorImage.setPixmap(tumor.scaled(self.tumorImage.width(), self.tumorImage.height(), QtCore.Qt.KeepAspectRatio))

    def saveResult(self):
        self.selection_results.export()

    def radioButtonClicked(self):
        if self.cancerButton.isChecked():
            self.selection_results.current_selection = "cancer"
        else: # self.benignButton.isChecked():
            self.selection_results.current_selection = "benign"

    def loadDataset(self, num):
        try:
            self.input_data.changeDataset(num)
        except IndexError("Dataset you choose is already done."):
            QMessageBox.information(self, 'Last Image', "Dataset you choose is already done.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.curDataset.setText(str(self.input_data.current_folder_index))
            self.numOfWholePatients.setText(str(self.input_data.numberOfCurrentPatient()))
            self.updatePatient()

    def changeAmbiguity(self):
        if self.ambiguousCheckBox.isChecked():
            self.selection_results.current_ambiguity = True
        else:
            self.selection_results.current_ambiguity = False


def indexToFolderName(idx):
    return "{0:02}".format(idx)


def indexToPatientName(idx):
    return "{0:03}".format(idx)


def indexToDataName(idx):
    return "{0:02}.jpg".format(idx)

class InputDataHandler():
    def __init__(self, origin_path):
        self.origin_path = origin_path

        folders_list = os.listdir(self.origin_path)
        self.folders_list = [x for x in folders_list if os.path.isdir(os.path.join(self.origin_path, x))]
        self.num_folders = len(self.folders_list)
        self.current_folder_index = 0

        self.patient_list_dict = {folders: os.listdir(os.path.join(self.origin_path, folders)) for folders in self.folders_list}
        self.num_patient_dict = {folders: len(self.patient_list_dict[folders]) for folders in self.folders_list}
        self.current_patient_dict = {folders: 0 for folders in self.folders_list}

        self.data_list_per_patient_dict = {}
        self.num_data_per_patient_dict = {}
        self.current_data_index_dict = {}
        for folders, patient_list in self.patient_list_dict.items():
            for patient in patient_list:
                self.data_list_per_patient_dict[(folders, patient)] = os.listdir(os.path.join(self.origin_path, folders, patient))
                self.num_data_per_patient_dict[(folders, patient)] = len(self.data_list_per_patient_dict[(folders, patient)])
                self.current_data_index_dict[(folders, patient)] = 0
        
    def restoreFromPreviousWorks(self, current_patient_dict):
        self.current_patient_dict = current_patient_dict
        for ((key, cur_patient_idx), num_of_patient) in zip(self.current_patient_dict.items(), self.num_patient_dict.values()):
            if cur_patient_idx < num_of_patient:
                self.current_folder_index = self.folders_list.index(key)
                break

    def currentFolderName(self):
        return indexToFolderName(self.current_folder_index)

    def currentPatientIndex(self):
        return self.current_patient_dict[self.currentFolderName()]

    def currentPatientName(self):
        return indexToPatientName(self.currentPatientIndex())
    
    def currentDataIndex(self):
        return self.current_data_index_dict[(self.currentFolderName(), self.currentPatientName())]
    
    def currentDataName(self):
        return indexToDataName(self.currentDataIndex())

    def currentDataPath(self):
        return os.path.join(self.origin_path, self.currentFolderName(), self.currentPatientName(), self.currentDataName())

    def numberOfCurrentPatient(self):
        return self.num_patient_dict[self.currentFolderName()]

    def numberOfCurrentData(self):
        return self.num_data_per_patient_dict[(self.currentFolderName(), self.currentPatientName())]

    def changeDataset(self, idx):
        assert idx >= 0 and idx < self.num_folders, 'out of boundary'
        data_folder_path = os.path.join(self.origin_path, indexToFolderName(idx))
        assert os.path.isdir(data_folder_path), "No accessible folder: %s" % data_folder_path
        self.current_folder_index = idx
        if self._endOfTheFolder():
            self.prevPatient()
        elif self._beginingOfTheFolder():
            self.nextPatient()

    def nextPatient(self):
        self.current_patient_dict[self.currentFolderName()] += 1
        if self._endOfTheFolder():
            raise IndexError("Last Image")

    def prevPatient(self):
        self.current_patient_dict[self.currentFolderName()] -= 1
        if self._beginingOfTheFolder():
            raise IndexError("First Image")

    def nextData(self):
        self.current_data_index_dict[(self.currentFolderName(), self.currentPatientName())] += 1
        self.current_data_index_dict[(self.currentFolderName(), self.currentPatientName())] %= self.numberOfCurrentData()

    def prevData(self):
        self.current_data_index_dict[(self.currentFolderName(), self.currentPatientName())] -= 1
        self.current_data_index_dict[(self.currentFolderName(), self.currentPatientName())] %= self.numberOfCurrentData()

    def _endOfTheFolder(self):
        return self.current_patient_dict[self.currentFolderName()] >= self.numberOfCurrentPatient()

    def _beginingOfTheFolder(self):
        return self.current_patient_dict[self.currentFolderName()] < 0
    

class SelectionResultsHandler():
    def __init__(self, inputDataHandler, out_folder):
        assert os.path.isdir(out_folder), "out_folder does not exist: %s" % out_folder
        self.backup_path = "backup.imagetypeselector"
        self.result_file_pattern = os.path.join(out_folder, "result_%d%s.csv")
        self.table_schema = ["folder", "patient", "selection", "isAmbiguous"]
        
        self.num_folders = inputDataHandler.num_folders
        self.current_patient_dict = inputDataHandler.current_patient_dict
        self.num_patient_dict = inputDataHandler.num_patient_dict
        self.selection_dict = {}
        self.ambiguity_dict = {}
        self.current_selection = "benign"
        self.current_ambiguity = False
    
    def restoreFromPreviousWorks(self):
        assert os.path.isfile(self.backup_path), "No accessible file: %s" % self.backup_path
        assert not self.selection_dict, "selection_dict does not empty."
        backup_df = pd.read_csv(self.backup_path)
        folder_to_file_dict = {}
        for _, row in backup_df.iterrows():
            folder_to_file_dict[row[self.table_schema[0]]] = row[self.table_schema[1]]
            self.selection_dict[(row[self.table_schema[0]], row[self.table_schema[1]])] = row[self.table_schema[2]]
            self.ambiguity_dict[(row[self.table_schema[0]], row[self.table_schema[1]])] = row[self.table_schema[3]]
        for folder_idx in range(self.num_folders):
            if folder_idx in folder_to_file_dict.keys():
                self.current_patient_dict[indexToFolderName(folder_idx)] = folder_to_file_dict[folder_idx] + 1
        
    def saveSelection(self, folder_idx, patient_idx):
        assert isinstance(folder_idx, int), "Invalid type of folder_idx: %s" % (type(folder_idx))
        assert isinstance(patient_idx, int), "Invalid type of patient_idx: %s" % (type(patient_idx))
        assert isinstance(self.current_selection, str), "Invalid type of selection: %s" % (type(self.current_selection))
        assert isinstance(self.current_ambiguity, bool), "Invalid type of ambiguity: %s" % (type(self.current_ambiguity))
        
        assert folder_idx >= 0 and folder_idx < self.num_folders, 'Out of bounds'
        assert patient_idx >= 0 and patient_idx < self.num_patient_dict[indexToFolderName(folder_idx)], 'Out of bounds'
        assert self.current_selection in ["benign", "cancer"], "Invalid selction: %s" % self.current_selection

        self.selection_dict[(folder_idx, patient_idx)] = self.current_selection
        self.ambiguity_dict[(folder_idx, patient_idx)] = self.current_ambiguity

    def getSelection(self, folder_idx, patient_idx):
        assert isinstance(folder_idx, int), "Invalid type of folder_idx: %s" % (type(folder_idx))
        assert isinstance(patient_idx, int), "Invalid type of patient_idx: %s" % (type(patient_idx))
        assert folder_idx >= 0 and folder_idx < self.num_folders, 'Out of bounds'
        assert patient_idx >= 0 and patient_idx < self.num_patient_dict[indexToFolderName(folder_idx)], 'Out of bounds'
        return (self.selection_dict[(folder_idx, patient_idx)], self.ambiguity_dict[(folder_idx, patient_idx)])

    def export(self):
        backup_list = []
        result_file_list = [[] for _ in range(self.num_folders)]
        for (key, selection), ambiguity in zip(self.selection_dict.items(), self.ambiguity_dict.values()):
            folder = key[0]
            patient = key[1]
            row = (folder, patient, selection, ambiguity)
            backup_list.append(row)
            result_file_list[folder].append(row[1:])
        backup_df = pd.DataFrame(backup_list, columns=self.table_schema)
        backup_df.to_csv(self.backup_path)
        for folder_idx, result_file in enumerate(result_file_list):
            if result_file:
                if os.path.exists(self.result_file_pattern % (folder_idx, "")):
                    continue
                result_df = pd.DataFrame(result_file, columns=self.table_schema[1:])
                if len(result_file) == self.num_patient_dict[indexToFolderName(folder_idx)]: # done dataset
                    result_df.to_csv(self.result_file_pattern % (folder_idx, ""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = XMainWindow()
    mainwindow.show()
    app.exec_()