# YOLO Helper codes

What is it useful for 
- get inference
- For annotation helper refer directory ../AnnotationHelper


## How to use:

### Inference

Use class from yolo_inference\yolo_inferencer.py
Example usage can be found in  yolo_inferen.py
```
    results = yolo_inst.get_inference_on_img(img_batch)    
    yolo_inst.save_annotated_images(results, save_dir_path=output_dir)
    
```


