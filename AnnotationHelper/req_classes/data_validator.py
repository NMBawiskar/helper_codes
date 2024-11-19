import os
from pathlib import Path


class DataValidator:
    def __init__(self, dir_data) -> None:
        self.data_dir = dir_data
        self.parent_dir = Path(self.data_dir).parent
        self.not_found_files = os.path.join(self.parent_dir, 'not_pair_files')
        os.makedirs(self.not_found_files, exist_ok=True)


    def check_and_remove_img_label_not_found(self):
        train_dir = os.path.join(self.data_dir,'train')
        val_dir = os.path.join(self.data_dir,'val')

        train_img_dir = os.path.join(train_dir,'images')
        val_img_dir = os.path.join(val_dir, 'images')

        train_label_dir = os.path.join(train_dir, 'labels')
        val_label_dir = os.path.join(val_dir, 'labels')
        fileMoved =0

        if (os.path.exists(train_img_dir) and os.path.exists(val_img_dir) and 
            os.path.exists(train_label_dir) and os.path.exists(val_label_dir)):

            train_img_files = os.listdir(train_img_dir)
            val_img_files = os.listdir(val_img_dir)
            train_label_files = os.listdir(train_label_dir)
            val_label_files = os.listdir(val_label_dir)

            for train_label_file in train_label_files:
                fileNameWoExt = train_label_file.split(".")[0]
                imgfileName = f"{fileNameWoExt}.png"
                if imgfileName not in train_img_files:                    
                    target_path = os.path.join(self.not_found_files, imgfileName)
                    source_path = os.path.join(train_img_dir, imgfileName)
                    if os.path.exists(target_path):
                        os.rename(source_path, target_path)
                        fileMoved+=1
                
            for val_label_file in val_label_files:
                fileNameWoExt = val_label_file.split(".")[0]
                imgfileName = f"{fileNameWoExt}.png"
                if imgfileName not in val_img_files:                    
                    target_path = os.path.join(self.not_found_files, imgfileName)
                    source_path = os.path.join(val_img_dir, imgfileName)
                    if os.path.exists(target_path):
                        os.rename(source_path, target_path)
                        fileMoved+=1



            for train_img_file in train_img_files:
                fileNameWoExt = train_img_file.split(".")[0]
                label_file_name = f"{fileNameWoExt}.txt"
                if label_file_name not in train_label_files:                    
                    target_path = os.path.join(self.not_found_files, label_file_name)
                    source_path = os.path.join(train_label_dir, label_file_name)
                    if os.path.exists(target_path):
                        os.rename(source_path, target_path)
                        fileMoved+=1

            for val_img_file in val_img_files:
                fileNameWoExt = val_img_file.split(".")[0]
                label_file_name = f"{fileNameWoExt}.txt"
                if label_file_name not in val_label_files:                    
                    target_path = os.path.join(self.not_found_files, label_file_name)
                    source_path = os.path.join(val_label_dir, label_file_name)
                    if os.path.exists(target_path):
                        os.rename(source_path, target_path)
                        fileMoved+=1


if __name__=="__main__":
    data_dir = r"F:\Quicsolv\TRAININGS\ObjectDetection\Mahindra_press_bed_pin_detection\combined_training_dataset"
    data_validator = DataValidator(data_dir)
    data_validator.check_and_remove_img_label_not_found()