"""
Module for extracting images from documents.
"""

import logging
import io
import os
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_images_from_pdf(pdf_path, page_number=None):
    """
    Extract images from a PDF document.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_number (int, optional): Specific page to extract images from.
                                    If None, extracts from all pages.
    
    Returns:
        list: List of tuples (image, bbox) where image is a PIL Image object
              and bbox is a bounding box (x0, y0, x1, y1)
    """
    images = []
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Get the pages to process
        if page_number is not None:
            # Convert from 1-based to 0-based indexing
            page_idx = page_number - 1
            if 0 <= page_idx < len(doc):
                pages = [doc[page_idx]]
            else:
                logger.warning(f"Page {page_number} out of range (1-{len(doc)})")
                return images
        else:
            pages = doc
        
        # Extract images from each page
        for page in pages:
            # Get image lists
            img_list = page.get_images(full=True)
            
            for img_idx, img_info in enumerate(img_list):
                try:
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Load as PIL Image
                    img = Image.open(io.BytesIO(image_bytes))
                    
                    # Get the transformation matrix and calculate the bbox
                    bbox = get_image_bbox(page, img_info, img)
                    
                    images.append((img, bbox))
                except Exception as e:
                    logger.warning(f"Failed to extract image {img_idx} from page {page.number + 1}: {e}")
        
        return images
    
    except Exception as e:
        logger.error(f"Error extracting images from PDF {pdf_path}: {e}")
        return images


def get_image_bbox(page, img_info, img):
    """
    Calculate the bounding box of an image on a PDF page.
    
    Args:
        page: PDF page object
        img_info: Image information from page.get_images()
        img: PIL Image object
        
    Returns:
        tuple: Bounding box (x0, y0, x1, y1) in PDF coordinates
    """
    try:
        xref = img_info[0]
        matrix = fitz.Matrix(1, 1)  # Identity matrix
        
        # Try to get rectangles that contain this image reference
        rects = []
        for rect, xref_list in page.get_image_info():
            if xref in xref_list:
                rects.append(rect)
        
        if rects:
            # Return the first matching rectangle
            return rects[0]
        else:
            # Fallback: use a generic rectangle based on page dimensions
            page_width, page_height = page.rect.width, page.rect.height
            # Approximate a centered image taking 50% of page width
            img_width = page_width * 0.5
            img_height = img_width * img.height / max(img.width, 1)  # Maintain aspect ratio
            x0 = (page_width - img_width) / 2
            y0 = (page_height - img_height) / 2
            return (x0, y0, x0 + img_width, y0 + img_height)
    
    except Exception as e:
        logger.warning(f"Error calculating image bbox: {e}")
        # Return a default bbox
        return (0, 0, 100, 100)


def extract_images_from_html(html_content, base_url=None):
    """
    Extract image references from HTML content.
    
    Args:
        html_content (str): HTML content
        base_url (str, optional): Base URL for resolving relative URLs
        
    Returns:
        list: List of image URLs
    """
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src', '')
            if src:
                # If base_url is provided, resolve relative URLs
                if base_url and not (src.startswith('http://') or src.startswith('https://') or src.startswith('data:')):
                    if src.startswith('/'):
                        # Absolute path relative to domain
                        from urllib.parse import urlparse
                        parsed_base = urlparse(base_url)
                        src = f"{parsed_base.scheme}://{parsed_base.netloc}{src}"
                    else:
                        # Relative path
                        if not base_url.endswith('/'):
                            base_url += '/'
                        src = f"{base_url}{src}"
                
                images.append(src)
        
        return images
    
    except Exception as e:
        logger.error(f"Error extracting images from HTML: {e}")
        return []


def resize_image(image, max_width=800, max_height=600):
    """
    Resize an image while maintaining aspect ratio.
    
    Args:
        image: PIL Image object
        max_width (int): Maximum width
        max_height (int): Maximum height
        
    Returns:
        Image: Resized PIL Image object
    """
    if not image:
        return None
    
    try:
        # Get original dimensions
        width, height = image.size
        
        # Calculate new dimensions maintaining aspect ratio
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize the image
            return image.resize((new_width, new_height), Image.LANCZOS)
        else:
            # No need to resize
            return image
    
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        return image
