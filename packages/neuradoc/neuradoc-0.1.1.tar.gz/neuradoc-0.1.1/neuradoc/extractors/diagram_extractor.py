"""
Module for extracting and processing diagrams from documents.
"""

import logging
import io
import re
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


def analyze_diagram(image):
    """
    Analyze a diagram image to extract its structure and content.
    
    Args:
        image: PIL Image object or path to image file
        
    Returns:
        dict: Diagram analysis results
    """
    if isinstance(image, str):
        # Load the image if a path is provided
        try:
            image = Image.open(image)
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
    
    # Basic analysis of the diagram
    try:
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Determine if the image is color or grayscale
        is_color = len(img_array.shape) == 3 and img_array.shape[2] >= 3
        
        # Basic color analysis
        color_info = {}
        if is_color:
            # Count unique colors
            flattened = img_array.reshape(-1, img_array.shape[2])
            unique_colors = np.unique(flattened, axis=0)
            color_info['unique_color_count'] = len(unique_colors)
            
            # Calculate color distribution
            if len(unique_colors) < 100:  # Only for images with a reasonable number of colors
                color_counts = {}
                for color in unique_colors:
                    color_tuple = tuple(color)
                    mask = np.all(flattened == color, axis=1)
                    count = np.sum(mask)
                    color_counts[color_tuple] = int(count)
                
                # Find dominant colors (top 5)
                sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
                color_info['dominant_colors'] = [{'color': list(color), 'count': count} 
                                               for color, count in sorted_colors[:5]]
        
        # Basic shape analysis could be added here
        # For a complete implementation, you might want to use OpenCV for shape detection
        
        results = {
            'width': image.width,
            'height': image.height,
            'aspect_ratio': image.width / max(1, image.height),
            'is_color': is_color,
            'colors': color_info
        }
        
        # Determine diagram type based on heuristics
        diagram_type = classify_diagram_type(image, img_array, results)
        results['diagram_type'] = diagram_type
        
        return results
    
    except Exception as e:
        logger.error(f"Error analyzing diagram: {e}")
        return None


def classify_diagram_type(image, img_array, analysis_results):
    """
    Attempt to classify the type of diagram.
    
    Args:
        image: PIL Image object
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        str: Diagram type classification
    """
    # This is a very simple heuristic-based classification
    # A more sophisticated approach would use ML models
    
    # Check for flowchart
    if is_likely_flowchart(img_array, analysis_results):
        return "flowchart"
    
    # Check for bar chart
    if is_likely_bar_chart(img_array, analysis_results):
        return "bar_chart"
    
    # Check for line chart
    if is_likely_line_chart(img_array, analysis_results):
        return "line_chart"
    
    # Check for pie chart
    if is_likely_pie_chart(img_array, analysis_results):
        return "pie_chart"
    
    # Check for network diagram
    if is_likely_network_diagram(img_array, analysis_results):
        return "network_diagram"
    
    # Default classification
    return "general_diagram"


def is_likely_flowchart(img_array, analysis_results):
    """
    Check if the image is likely a flowchart.
    
    Args:
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        bool: True if likely a flowchart
    """
    # Flowcharts typically have:
    # - Rectangular shapes connected by lines
    # - Limited color palette
    # - Often have arrows
    
    # Simple heuristic: flowcharts typically have a limited color palette
    if 'unique_color_count' in analysis_results.get('colors', {}):
        if 5 <= analysis_results['colors']['unique_color_count'] <= 15:
            return True
    
    return False


def is_likely_bar_chart(img_array, analysis_results):
    """
    Check if the image is likely a bar chart.
    
    Args:
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        bool: True if likely a bar chart
    """
    # Simple heuristic: bar charts typically have vertical structures
    # This would require more sophisticated image processing to detect accurately
    return False


def is_likely_line_chart(img_array, analysis_results):
    """
    Check if the image is likely a line chart.
    
    Args:
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        bool: True if likely a line chart
    """
    # Line charts typically have:
    # - Lines connecting points
    # - Often a grid background
    # - X and Y axes
    
    # This would require more sophisticated image processing to detect accurately
    return False


def is_likely_pie_chart(img_array, analysis_results):
    """
    Check if the image is likely a pie chart.
    
    Args:
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        bool: True if likely a pie chart
    """
    # Pie charts typically have:
    # - Circular structure
    # - Multiple colored segments
    # - Often with a legend
    
    # Check for circular structure and multiple colors
    if 'unique_color_count' in analysis_results.get('colors', {}):
        if analysis_results['colors']['unique_color_count'] >= 3:
            # A simple check for squareness - pie charts are typically square-ish
            if 0.9 <= analysis_results['aspect_ratio'] <= 1.1:
                return True
    
    return False


def is_likely_network_diagram(img_array, analysis_results):
    """
    Check if the image is likely a network diagram.
    
    Args:
        img_array: NumPy array of the image
        analysis_results: Results from the diagram analysis
        
    Returns:
        bool: True if likely a network diagram
    """
    # Network diagrams typically have:
    # - Nodes (circles, rectangles) connected by lines
    # - Often have a web-like structure
    
    # This would require more sophisticated image processing to detect accurately
    return False


def extract_svg_from_html(html_content):
    """
    Extract SVG elements from HTML content.
    
    Args:
        html_content (str): HTML content
        
    Returns:
        list: List of SVG strings
    """
    from bs4 import BeautifulSoup
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        svg_elements = []
        
        for svg in soup.find_all('svg'):
            svg_elements.append(str(svg))
        
        return svg_elements
    
    except Exception as e:
        logger.error(f"Error extracting SVG from HTML: {e}")
        return []
