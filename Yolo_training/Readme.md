# Training Yolov11 Model on colab 

Training notebook Yolov11_training.ipynb helps train Yolov11 Model on colab. 
Data to be pushed pulled from s3 directory.
Google drive can also be used for the data.

Steps:
1. Create dataset using AnnotationHelpers
2. Custom labelimg program can also be used. [Visit Github](https://github.com/NMBawiskar/Object_detection_corrector)
3. Create train_dataset.yaml file as given in directory. Mention classes and path to images dir of train and val
4. Upload download_training_data.py, upload_data_to_s3.py, train_dataset.yaml to the training directory on colab or download from this repository.
5. Train 