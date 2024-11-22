import os
import glob
import xml.etree.ElementTree as ET

class AnnotationCorrector:
    def __init__(self) -> None:
        pass
    
    def make_all_class_ids_single_class_yolo_annotation(self, dir_yolo_annotations, correct_single_class_id=0):
        """corrects the labels in the given directory"""
        
        for file in os.listdir(dir_yolo_annotations):
            if file.endswith(".txt"):
                file_path = os.path.join(dir_yolo_annotations, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    corrected_lines = []
                    for line in lines:
                        line = line.replace("\n","")
                        data = line.split(" ")
                        wronglabelId, cx, cy, w, h = data
                        corrected_label = str(correct_single_class_id)
                        corrected_line = f"{corrected_label} {cx} {cy} {w} {h}\n"
                        corrected_lines.append(corrected_line)
                
                with open(file_path, 'w') as f:
                    f.writelines(corrected_lines)



class XMLAnnotationCorrector:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def correct_annotations(self, single_class_label='pins'):
        # Loop through all the object tags and change their name tag value
        for obj in self.root.findall('object'):
            name_tag = obj.find('name')
            if name_tag is not None:
                name_tag.text = single_class_label

    def save_changes(self, output_file):
        # Write the modified tree back to an XML file
        self.tree.write(output_file, encoding="utf-8", xml_declaration=True)

def process_directory(directory_path, output_directory):
    # Get a list of all XML files in the directory
    xml_files = glob.glob(os.path.join(directory_path, "*.xml"))

    for xml_file in xml_files:
        # Initialize the corrector for each XML file
        corrector = XMLAnnotationCorrector(xml_file)
        
        # Generate output file path (it will be saved in output_directory)
        file_name = os.path.basename(xml_file)
        output_file = os.path.join(output_directory, file_name)

        # Correct annotations and save the modified XML file
        corrector.correct_annotations()
        corrector.save_changes(output_file)

        print(f"Corrected annotation saved to {output_file}")

    # Path to the directory containing XML files
    


if __name__ == '__main__':
    # annotation_corrector = AnnotationCorrector()
    # dir_yolo_annotations = r"F:\RuRux\mahindra_press_bed_backend\data_annotated\right\annotations_yolo"
    # annotation_corrector.make_all_class_ids_single_class_yolo_annotation(dir_yolo_annotations, correct_single_class_id=0)


    ## Make all xml file objects a single class label
    input_directory = r'F:\RuRux\mahindra_press_bed_backend\data_annotated\right\annotations'  # Change this to your input directory path
    output_directory = r'F:\RuRux\mahindra_press_bed_backend\data_annotated\right\annotations_corrected'  # Change this to your output directory path

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Process all XML files in the input directory
    process_directory(input_directory, output_directory)
