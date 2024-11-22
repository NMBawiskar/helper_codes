from yolo_inference.yolo_inferencer import YoloInference
import os


model_path = r"F:\RuRux\mahindra_press_bed_backend\training_result\2024_11_21_exp20_epoch\weights\best (2).pt"

trained_img_size = (640,640)
yolo_inst = YoloInference(model_path)

# tst_img_path = r'F:\RuRux\mahindra_press_bed_backend\data_annotated\right\val\images\2024_10_30__03_04_53__die_152_job_1014.png'
# result = yolo_inst.get_inference_on_img([tst_img_path])
# print(result)


### Input dir with annotations

input_dir = r'F:\RuRux\mahindra_press_bed_backend\data_collection\left\imgs'
# input_dir = 'test_imgs'
output_dir = r"F:\RuRux\mahindra_press_bed_backend\data_collection\left\inference_yolov11"
# output_dir =r'test_output'
os.makedirs(output_dir, exist_ok=True)
list_images = os.listdir(input_dir)
img_paths = []
for img_name in list_images:
    list_ = img_name.split(".")
    ext = list_[-1]
    if ext == 'png':
        path = os.path.join(input_dir, img_name)
        img_paths.append(path)


n_batch = 8
st_index = 0
for i in range(len(img_paths)):
    end_index = st_index + n_batch
    if end_index > len(img_paths):
        end_index = len(img_paths)
    
    if st_index > len(img_paths):
        break
    
    img_batch = img_paths[st_index:end_index]

    results = yolo_inst.get_inference_on_img(img_batch)
    print("Inference done on img count", len(img_paths))
    yolo_inst.save_annotated_images(results, save_dir_path=output_dir)
    print(f"Saved inference images at {output_dir}")
    st_index = end_index