# All helper codes

1. Annotation Helpers
    - Helps in annotation conversion, creations from PascalVoc to yolo
    - Helps in creation of YOLO datasets. Organizing and split train test data
2. Pdf Preprcess (Pdf_preprocessor)
    - Helps pdf operations, convert to img, img to pdf, split pdf, resize pdf
    - Deskew images

3. YOLO 
    - Helps in taking inference of YOLO v11 model.
    - Take inference and save annotated images 
    - Create annotations xmls and yolo txt files from inference

4. Logger 
    - Save log date wise
    - Purge old log files
5. S3
    - S3 list files, list sub directories
    - upload download single file or directory to s3 using boto3
    