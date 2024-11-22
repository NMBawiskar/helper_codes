from ultralytics import YOLO
import torch
import os

class YoloInference:
    def __init__(self, model_path) -> None:
        self.model_path = model_path
        self.model = None
        self.load_model()


    def load_model(self):
        try:
            self.model = YOLO(self.model_path)
            if torch.cuda.is_available():
                device = torch.cuda.get_device_name()
                # self.model.to('cuda')
            self.model = self.model.cpu()
            self.model.task = 'detect'
            print(f"Successfully loaded YOLO model from {self.model_path}")
        except Exception as e:
            print(f"Error while loading YOLO model: {str(e)}")

    
    def get_inference_on_img(self, img_path_list):
        try:
            # self.model.task ='detect'  ## very important
            results = self.model.predict(img_path_list)
            return results
        except Exception as e:
            print(f"Error while getting inference on image: {str(e)}")
            return None
        
    def save_annotated_images(self, results, save_dir_path):
        for res in results:
            boxes = res.boxes  # Boxes object for bounding box outputs
            img_path = res.path
            img_name = os.path.basename(img_path)
            img_name_wo_ext = img_name.split(".")[0]
            res.plot(labels=False, probs=False, show=False)  # display to screen
            out_path = os.path.join(save_dir_path, f"{img_name_wo_ext}.png")
            res.save(filename=out_path, labels=False, probs=False)