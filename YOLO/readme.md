# YOLO Helper codes

Here it can be useful to 
- get inference
- For annotation helper refer directory ../AnnotationHelper


## How to use:

### Inference

Use class from yolo_inference\yolo_inferencer.py
```
    results = yolo_inst.get_inference_on_img(img_batch)    
    yolo_inst.save_annotated_images(results, save_dir_path=output_dir)
    
```


