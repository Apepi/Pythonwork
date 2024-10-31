# Image Steganography Tool

A Python implementation of LSB (Least Significant Bit) steganography that allows you to hide secret messages within images without noticeable visual changes.

## Features

- Hide text messages within image files
- Extract hidden messages from encoded images
- Minimal visual impact on carrier images
- Supports PNG output format
- Built-in message delimiter for reliable extraction
- Efficient pixel manipulation using NumPy

## Requirements

```
PIL (Pillow)
NumPy
```

Install dependencies using:
```bash
pip install pillow numpy
```

## Usage

### Basic Example

```python
from steganography import Steganography

# Create an instance
steg = Steganography()

# Hide a message
steg.hide_message(
    'input_image.jpg',      # Original image
    'Hello, World!',        # Secret message
    'output_image.png'      # Output image
)

# Find the hidden message
message = steg.find_message('output_image.png')
print(f"Found message: {message}")
```

### Methods

#### hide_message(image_path, message, output_path)
Hides a text message within an image.

Parameters:
- `image_path`: Path to the carrier image
- `message`: Text message to hide
- `output_path`: Path where the encoded image will be saved

#### find_message(image_path)
Extracts a hidden message from an encoded image.

Parameters:
- `image_path`: Path to the image containing the hidden message

Returns:
- The hidden message if found
- "No hidden message found" if no message is detected

## Technical Details

- Uses LSB (Least Significant Bit) technique for message encoding
- Implements message delimiter ("###END###") for reliable message extraction
- Utilizes NumPy for efficient pixel manipulation
- Preserves image quality while maintaining message integrity
- Automatically validates message length against image capacity

## Limitations

- Output images are saved in PNG format to prevent compression losses
- Message size is limited by image dimensions (each character requires 8 pixels)
- Only supports text messages (no binary data)
- Large messages may slightly impact image histogram statistics

## Example Images

Original Image             |  Image with Hidden Message
:-------------------------:|:-------------------------:
[Original Image Here]      |  [Encoded Image Here]
No visual difference is apparent to the human eye

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
