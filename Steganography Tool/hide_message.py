from steganography import Steganography

# Create an instance of Steganography
steg = Steganography()

try:
    # Hide a message in an image
    steg.hide_message(
        'my_image.jpg',        # Image in same folder
        'Hello World!',        # Your secret message
        'hidden_message.png'   # Output image name
    )
    print("Message hidden successfully!")
    
except Exception as e:
    print(f"An error occurred: {e}")
