from PIL import Image
import numpy as np

class Steganography:
    def __init__(self):
        self.delimiter = "###END###"
        
    def hide_message(self, image_path, message, output_path):
        """The method to hide a message in an image"""
        # Add delimiter to message and convert to binary
        full_message = message + self.delimiter
        binary_message = ''.join(format(ord(char), '08b') for char in full_message)
        
        # Open and prepare image
        img = Image.open(image_path)
        pixels = np.array(img, dtype=np.uint8)  # Specify uint8 type
        
        # Check if message can fit in image
        if len(binary_message) > pixels.size:
            raise ValueError("Message too long for this image")
            
        # Modify pixels to hide message
        modified_pixels = pixels.copy()
        for i, bit in enumerate(binary_message):
            # Get current pixel value
            current_pixel = int(modified_pixels.flat[i])
            
            # Clear the least significant bit and set it to our message bit
            if int(bit) == 1:
                # If message bit is 1, make pixel odd
                new_pixel = current_pixel | 1
            else:
                # If message bit is 0, make pixel even
                new_pixel = current_pixel & 254  # 254 is 11111110 in binary
                
            modified_pixels.flat[i] = new_pixel
        
        # Save modified image
        encoded_image = Image.fromarray(modified_pixels)
        encoded_image.save(output_path, 'PNG')
        print(f"Message hidden in {output_path}")
            
    def find_message(self, image_path):
        """Find a hidden message in an image"""
        # Open image and get pixels
        img = Image.open(image_path)
        pixels = np.array(img)
        
        # Extract the binary message
        binary_message = ''
        text = ''
        
        # Get least significant bit from each pixel
        for pixel in pixels.flat:
            binary_message += str(pixel & 1)
            
            # Convert every 8 bits to a character
            if len(binary_message) >= 8:
                char = chr(int(binary_message[:8], 2))
                text += char
                binary_message = binary_message[8:]
                
                # Check if we've found the delimiter
                if self.delimiter in text:
                    return text.split(self.delimiter)[0]
        
        return "No hidden message found"
