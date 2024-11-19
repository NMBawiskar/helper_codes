import xml.etree.ElementTree as eTree
import os

class Annotation_converter:
    def __init__(self, dir_annotation, annotation_type="") -> None:
        self.dir_annotation = dir_annotation


    def convert_xml_file_to_yolo_annotation(self, file_xml_path):
        """function to conver pascal VOC xml annotation to yolo txt anntoation"""
        
        
        
        tree = eTree.parse(file_xml_path)

        label_list = []

        # getting the parent tag of
        # the xml document
        bbox_xyxy_list = []
        root = tree.getroot()
        print(root)
        for element in root:
            tag = element.tag
            if tag == "size":
                imgw, imgh, ch = float(element[0].text), float(element[1].text), float(element[2].text)
                print('size', imgw,imgh,ch)
            
            if tag =='object':
                label = element[0].text
                
                label_list.append(label)
                bbox_element = element[4]
                bbox_xyxy = [float(subElem.text) for subElem in bbox_element]
                bbox_xyxy_list.append(bbox_xyxy)




        bbox_cx_cy_w_h_abs = list(map(self.convert_xyxy_to_cx_cy_w_h, bbox_xyxy_list))
        bbox_cy_cy_w_h_norm = [[cx/imgw, cy/imgh, w/imgw, h/imgh] for cx,cy,w,h in bbox_cx_cy_w_h_abs]


        labels_unique = list(set(label_list))


        list_yolo_annotation = []
        for i, bboxCxCyWHnorm in enumerate(bbox_cy_cy_w_h_norm):
            label = label_list[i]
            label_id = labels_unique.index(label)
            
            line_yolo_annotation = [label_id]
            line_yolo_annotation.extend(bboxCxCyWHnorm)
            list_yolo_annotation.append(line_yolo_annotation)

        return list_yolo_annotation
        

    def convert_xyxy_to_cx_cy_w_h(self, bbox_xyxy):
        """Yolo format class_id center_x center_y width height"""
        x1,y1,x2,y2 = bbox_xyxy
        
        cx, cy = (x1+x2)/2, (y1+y2)/2
        w,h = abs(x2-x1), abs(y2-y1)

        return [cx, cy, w, h]
    

    def convert_dir_xml_to_yolo(self, out_dir_path):
        files_xml = os.listdir(self.dir_annotation)
        files_xml =[filename for filename in files_xml if filename[-3:]=="xml"]
        for filename in files_xml:
            path_in = os.path.join(self.dir_annotation, filename)
            filename_txt = filename.replace('.xml','.txt')
            
            path_out = os.path.join(out_dir_path, filename_txt)
            list_yolo_annotation = self.convert_xml_file_to_yolo_annotation(path_in)
            list_yolo_annotation = [[str(i) for i in lst] for lst in list_yolo_annotation]  
            list_yolo_annotation_str = [" ".join(_lst) + "\n" for _lst in list_yolo_annotation]            
            with open(path_out,'w') as f:
                f.writelines(list_yolo_annotation_str)



if __name__=="__main__":
    path_dir = r"F:\Quicsolv\TRAININGS\ObjectDetection\Mahindra_press_bed_pin_detection\pins_near_to_camera_dataset\pins_near_to_camera_dataset\labels_xml"
    annotation_converter  = Annotation_converter(path_dir)
    # file_path_xml = os.path.join(path_dir, '27_10_2023__12_30_21.xml')
    # list_yolo_annotation = annotation_converter.convert_xml_file_to_yolo_annotation(file_path_xml)
    # list_yolo_annotation = [[str(i) for i in lst] for lst in list_yolo_annotation]  
    # list_yolo_annotation_str = [" ".join(_lst) + "\n" for _lst in list_yolo_annotation]
    # out_path = 'sample.txt'
    # with open(out_path,'w') as f:
    #     f.writelines(list_yolo_annotation_str)

    annotation_converter.convert_dir_xml_to_yolo(out_dir_path="output_yolo_annotations")