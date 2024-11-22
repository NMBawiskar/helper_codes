


from glob import glob
import os
import traceback
from pdf2image import convert_from_path
import fitz
from settings import *
import fitz


class PDF_preprocessor:
    def __init__(self):
        self.gipsa_only_pdf_dir = GIPSA_PAGES_PDF_DIR

    
    def resized_pdf2png(self, file_path, output_folder):
        '''
        This function gets a pdf file as input. If pdf pages size is greater than 1280 x 1024 then resize it and save the page as png.
        (prevents killing of the script due to over RAM usage.)
        
        '''
        filename = os.path.basename(file_path)
        report_name = filename.replace('.pdf','')
        # folder_path = os.path.join(output_folder, filename)

        # os.makedirs(folder_path, exist_ok=True)

        try:
            with fitz.open(file_path) as doc:
                with fitz.open(file_path) as doc2:
                    
                    mat = fitz.Matrix(1, 1)
                    
                    W = 1024
                    H = 1280

                    for i,page in enumerate(doc):
                        rect =  page.rect
                        
                        delta_width = abs(rect.width - W)
                        delta_height = abs(rect.height - H)
                        if rect.height > 1280:
                            delta_height = -delta_height
                        
                        if rect.width > 1024:
                            delta_width = -delta_width
                        
                        new_rect = rect + (0, 0, delta_width, delta_height)

                        indx = doc2.insert_page(i+1, height = new_rect.height, width = new_rect.width)
                        newPage = doc2[i+1]
                        newPage.show_pdf_page(new_rect, doc, i)

                        outFilePath = os.path.join(output_folder, report_name+"-"+str(i+1)+".png")
                        pix = newPage.get_pixmap(matrix = mat) 
                        pix.save(outFilePath)
        except Exception as e:
            print('Exception in fitz.. trying other method..', traceback.format_exc())
            try:
                images = convert_from_path(file_path)

                for i in range(len(images)):
                    print('page-', i)
                    outFilePath = os.path.join(output_folder, report_name+"-"+str(i+1)+".png")
                    images[i].save(outFilePath, 'PNG') 
            except Exception as e:
                return False, None

        return True, glob(os.path.join(output_folder, './*.png'))
    

    def convert_png_to_pdf(self, image_dir, output_pdf_dir, report_name):
        '''
        This function gets a directory of PNG images as input and convert them into a single PDF file.
        
        '''
        image_files = glob(os.path.join(image_dir, '*.png'))
        if not image_files:
            print(f'No PNG images found in the directory: {image_dir}')
            return False
        
        os.makedirs(output_pdf_dir, exist_ok=True)
        
        with fitz.open() as doc:
            for i, image_file in enumerate(image_files):
                print(f'Converting image {i+1}/{len(image_files)}: {image_file}')
                page = fitz.open(image_file)
                doc.insert_pdf(page)

        
    def img2pdf_fitz(self, img_dir, processed_pdf_directory, file_name):
        try:
            doc = fitz.open()  
            # imgPathOut = os.path.join(ProjSettings.rotated_imgs, imgPathOut)
            # imglist = sorted(os.listdir(imgPathOut), key=lambda x: int(''.join(c for c in x if c.isdigit())))
            report_name = os.path.basename(img_dir)
            imglist = sorted(os.listdir(img_dir), key=lambda x: int(x.split(".")[0].split("-")[-1]))
            # pdf_file_name = report_name + '.pdf'
            
            for f in imglist:
                img = fitz.open(os.path.join(img_dir, f)) 
                rect = img[0].rect 
                pdfbytes = img.convert_to_pdf() 
                img.close()  
                imgPDF = fitz.open("pdf", pdfbytes) 
                page = doc.new_page(width=rect.width, height=rect.height)  
                page.show_pdf_page(rect, imgPDF, 0) 

            doc.save(os.path.join(processed_pdf_directory,file_name))
            doc.close()
        except Exception as e:
            print('Error in img2pdf_fitz', traceback.format_exc())
            return False

        return True


    def split_and_save_gipsa_pages_pdf(self,pdf_path, start_page:int, end_page:int):
        pdf_name = os.path.basename(pdf_path)

        doc2 = fitz.open()
        with fitz.open(pdf_path) as doc:
            doc2.insert_pdf(doc, from_page = start_page, to_page = end_page)
        
        out_pdf_path = os.path.join(self.gipsa_only_pdf_dir, pdf_name)
        doc2.save(out_pdf_path)
            