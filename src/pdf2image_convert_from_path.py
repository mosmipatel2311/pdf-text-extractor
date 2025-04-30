import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
import re

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def convert_pdf_to_images(pdf_path, image_dir):
    """Convert PDF pages to images using PyMuPDF"""
    try:
        # Create directory for images
        create_directory(image_dir)
        
        # Open PDF
        pdf_document = fitz.open(pdf_path)
        image_paths = []
        
        # Convert each page to image
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            
            # Convert page to image with higher resolution
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            image_path = os.path.join(image_dir, f'page_{page_number + 1}.png')
            pix.save(image_path)
            image_paths.append(image_path)
            print(f"Saved image: {image_path}")
            
        pdf_document.close()
        return image_paths
    
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        raise

def extract_text_from_image(image_path):
    """Extract text from an image using OCR"""
    try:
        # Verify Tesseract installation
        if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
            raise Exception(f"Tesseract not found at: {pytesseract.pytesseract.tesseract_cmd}")
            
        print(f"Processing image: {image_path}")
        
        # Open image
        image = Image.open(image_path)
        
        # Convert image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using OCR with additional configuration
        text = pytesseract.image_to_string(
            image,
            lang='eng',  # Specify language
            config='--psm 3 --oem 3'  # Page segmentation mode and OCR Engine mode
        )
        
        # Clean the text
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = '\n'.join(line for line in text.split('\n') if line.strip())
        
        # Debug print
        print(f"Extracted text length: {len(text)}")
        if not text:
            print("Warning: No text was extracted from the image")
        
        return text
    
    except Exception as e:
        print(f"Error extracting text from {image_path}: {str(e)}")
        return ""

def create_markdown_file(text, output_path, page_num):
    """Create a markdown file for the extracted text"""
    try:
        with open(output_path, 'w', encoding='utf-8') as md_file:
            # Add markdown formatting
            md_file.write(f"# Page {page_num}\n\n")
            md_file.write(text)
            
        print(f"Created markdown file: {output_path}")
        
    except Exception as e:
        print(f"Error creating markdown file: {str(e)}")

def process_pdf(pdf_path, base_output_dir):
    """Main function to process PDF and create markdown files"""
    try:
        # Create output directories
        image_dir = os.path.join(base_output_dir, "images")
        text_dir = os.path.join(base_output_dir, "text")
        markdown_dir = os.path.join(base_output_dir, "markdown")
        
        create_directory(base_output_dir)
        create_directory(image_dir)
        create_directory(text_dir)
        create_directory(markdown_dir)
        
        # Step 1: Convert PDF to images
        print("\nStep 1: Converting PDF to images...")
        image_paths = convert_pdf_to_images(pdf_path, image_dir)
        
        # Step 2: Process each image
        print("\nStep 2: Extracting text from images and creating markdown files...")
        for i, image_path in enumerate(image_paths, 1):
            # Extract text from image
            text = extract_text_from_image(image_path)
            
            # Save text file
            text_path = os.path.join(text_dir, f'page_{i}.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Create markdown file
            md_path = os.path.join(markdown_dir, f'page_{i}.md')
            create_markdown_file(text, md_path, i)
            
        print("\nProcessing complete!")
        print(f"Images saved in: {image_dir}")
        print(f"Text files saved in: {text_dir}")
        print(f"Markdown files saved in: {markdown_dir}")
        
    except Exception as e:
        print(f"An error occurred during processing: {str(e)}")
        raise

if __name__ == "__main__":
    # Specify Tesseract path - MAKE SURE THIS PATH IS CORRECT
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Verify Tesseract installation
    if not os.path.exists(tesseract_path):
        print(f"ERROR: Tesseract not found at {tesseract_path}")
        print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        exit(1)
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Update these paths to match your files
    pdf_path = r"C:\Users\Admin\Documents\workspace\agri-uni-pdf-convertor\AgroTechnologies2018-mini.pdf"
    output_dir = r"C:\Users\Admin\Documents\workspace\agri-uni-pdf-convertor\output_agrotechmdfiles_mini"
    
    print("PDF Path:", pdf_path)
    print("Output Directory:", output_dir)
    print("Tesseract Path:", tesseract_path)
    
    # Process the PDF
    process_pdf(pdf_path, output_dir)


