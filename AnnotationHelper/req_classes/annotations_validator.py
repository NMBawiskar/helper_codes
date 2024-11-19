import os



class YoloAnnotationValidator:
    def __init__(self, dir_yolo_annotations) -> None:
        self.dir_yolo_annotations = dir_yolo_annotations

    def validate_number_of_labels(self, required_label_count):
        """Check and validate if number of labels in annotated files is required or not
        checks unique labelids in each file found
        """
        label_dictionary = self.get_label_counts()

        count_unique_labels = len(label_dictionary.keys())
        if count_unique_labels == required_label_count:
            print(f"Validation Success !! files contain unique labels count as required i.e. {count_unique_labels}")
            return True
        else:
            print(f"required unique label count is {required_label_count} but labels in files are {count_unique_labels}")
            return False

    def get_label_counts(self):
        """return dictionary of each labelId and its count"""
      
        files = os.listdir(self.dir_yolo_annotations)
        
        label_dictionary = {}
        
        for fileName in files:
            path_in = os.path.join(self.dir_yolo_annotations, fileName)
            ext = fileName.split(".")[-1]
            if ext == 'txt':
                with open(path_in, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.replace("\n","")
                        data = line.split(" ")
                        labelId, cx, cy, w, h = data
                        if labelId not in label_dictionary:
                            label_dictionary[labelId]= 0
                        
                        label_dictionary[labelId]+=1
        
        print("label count dictionary", label_dictionary)
        return label_dictionary

    def validate_minimum_height_width_of_object(self, imgSize_for_training, min_pix_ht_or_wd = 6):
        """ imgSize_for_training : tuple (w, h)"""
        
        print(f"Considering image size {imgSize_for_training} for training, following is the object size validation result.")
        files = os.listdir(self.dir_yolo_annotations)
        wImg, hImg = imgSize_for_training
        files_violating_validation = []
        n_objects_under_size = 0
        
        for fileName in files:
            path_in = os.path.join(self.dir_yolo_annotations, fileName)
            ext = fileName.split(".")[-1]
            if ext == 'txt':
                with open(path_in, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.replace("\n","")
                        data = line.split(" ")
                        data = [float(numstr.strip()) for numstr in data]
                        labelId, cx, cy, w, h = data
                        cx_abs, cy_abs, w_abs, h_abs = cx * wImg, cy * hImg, w * wImg, h* hImg
                        if w_abs < min_pix_ht_or_wd or h_abs <min_pix_ht_or_wd:
                            n_objects_under_size+=1
                            if fileName not in files_violating_validation:
                                files_violating_validation.append(fileName)


        print(f"Total objects found undersized {n_objects_under_size}")
        print(f"Filenames in which undersized object found {len(files_violating_validation)}")


if __name__=="__main__":
    dir_yolo_annotations=r'F:\Quicsolv\TRAININGS\ObjectDetection\Mahindra_press_bed_pin_detection\latest_pins_dataset_new\content\pins_dataset\train\labels'
    # dir_yolo_annotations=r'output_yolo_annotations'
    yoloAnnotationValidator = YoloAnnotationValidator(dir_yolo_annotations)

    ## how many labels should be there 
    label_count_required = 1

    yoloAnnotationValidator.validate_number_of_labels(required_label_count=label_count_required)

    yoloAnnotationValidator.validate_minimum_height_width_of_object(imgSize_for_training=(960,960), min_pix_ht_or_wd=4)