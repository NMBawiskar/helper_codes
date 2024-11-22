from pathlib import Path
import os
import random

class DataSplitter:
    def __init__(self, imgFolder, annotation_label_folder) -> None:
        self.imgFolder = imgFolder
        self.annotation_label_folder = annotation_label_folder


    def split_data_random(self, train_percent = 80):
        path = Path(self.imgFolder)
        dir_parent = path.parent
        train_dir, val_dir = 'train', 'val'
        train_dir_path = os.path.join(dir_parent, train_dir)
        val_dir_path = os.path.join(dir_parent, val_dir)
        os.makedirs(train_dir_path, exist_ok=True)
        os.makedirs(val_dir_path, exist_ok=True)

        imageFiles= os.listdir(self.imgFolder)
        annotations = os.listdir(self.annotation_label_folder)

        
        files_training = int(train_percent* len(annotations)/100)
        random_training_files = random.sample(annotations, files_training)

        print("Training files seleted :", len(random_training_files))
        print("Unique Training files seleted :", len(set(random_training_files)))


        train_img_dir = os.path.join(train_dir_path, 'images')
        val_img_dir = os.path.join(val_dir_path, 'images')

        train_labels_dir = os.path.join(train_dir_path, 'labels')
        val_labels_dir = os.path.join(val_dir_path, 'labels')
        os.makedirs(train_img_dir, exist_ok=True)
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(train_labels_dir, exist_ok=True)
        os.makedirs(val_labels_dir, exist_ok=True)
        
        for annotationFile in annotations:
            fileNameWoExt = annotationFile.split(".")[0]
            fileNameImg = f"{fileNameWoExt}.png"
            if annotationFile in random_training_files:
                if fileNameImg in imageFiles:
                    fileImgPath = os.path.join(self.imgFolder, fileNameImg)
                    target_img_path  = os.path.join(train_img_dir, fileNameImg)
                    os.rename(fileImgPath, target_img_path)
                    sourceLabelPath = os.path.join(self.annotation_label_folder, annotationFile)
                    targetLabelPath = os.path.join(train_labels_dir, annotationFile)
                    os.rename(sourceLabelPath, targetLabelPath)
            else:
                if fileNameImg in imageFiles:
                    fileImgPath = os.path.join(self.imgFolder, fileNameImg)
                    target_img_path  = os.path.join(val_img_dir, fileNameImg)
                    os.rename(fileImgPath, target_img_path)
                    sourceLabelPath = os.path.join(self.annotation_label_folder, annotationFile)
                    targetLabelPath = os.path.join(val_labels_dir, annotationFile)
                    os.rename(sourceLabelPath, targetLabelPath)

        
        

        print(train_dir_path)



if __name__=="__main__":
    imgDirPath = r"F:\RuRux\mahindra_press_bed_backend\data_annotated\left\imgs"
    label_dir_path = r"F:\RuRux\mahindra_press_bed_backend\data_annotated\left\annotations_yolo" 
    dataSplitter = DataSplitter(imgDirPath, label_dir_path)
    dataSplitter.split_data_random()