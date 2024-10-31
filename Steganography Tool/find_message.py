from steganography import Steganography

# Create an instance of Steganography
steg = Steganography()

try:
    # Find the hidden message
    message = steg.find_message('hidden_message.png')
    print(f"Found message: {message}")
    
except Exception as e:
    print(f"An error occurred: {e}")
