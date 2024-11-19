


############### browse file ###############

from PyQt5.QtWidgets import QFileDialog,  QInputDialog, QMainWindow, QStackedWidget, QWidget, QProgressBar, QDialog
    
def browse_vid_file(self):

    qWid = QWidget()
    print("file browse")
    path,_ = QFileDialog.getOpenFileName(qWid, 'Open a file', '','Image Files (*.*)')        
    self.textEdit_vidPath_rtsp.setPlainText(path)

############### browse folder ###############

def browse_folder(self):
    qWid = QWidget()
    print("file browse")
    path_folder = QFileDialog.getExistingDirectory(qWid, 'Select folder', '')        
    self.image_folder_path_textedit.setPlainText(path_folder)
