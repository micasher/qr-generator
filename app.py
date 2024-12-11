import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from PIL import Image

# Define the data for the QR code
data = "https://example.com"

# Create the QR code
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(data)
qr.make(fit=True)

# Create the QR code image with a vertical gradient color mask
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=VerticalGradiantColorMask(
        back_color=(255, 255, 255),  # White background
        top_color=(0, 0, 0),        # Black at the top
        bottom_color=(0, 0, 255),   # Blue at the bottom
    ),
)

# Convert QR image to RGBA mode for overlay
img = img.convert("RGBA")

# Load the image to overlay in the center
center_image_path = "image_path.png"  # Replace with your image path
center_image = Image.open(center_image_path).convert("RGBA")

# Resize the center image to be a small proportion of the QR code size
qr_width, qr_height = img.size
scale_factor = 0.3  # Adjust this factor to control the size of the center image
new_size = (int(qr_width * scale_factor), int(qr_height * scale_factor))
center_image_resized = center_image.resize(new_size, Image.LANCZOS)

# Calculate the position to center the image
center_x = (qr_width - center_image_resized.size[0]) // 2
center_y = (qr_height - center_image_resized.size[1]) // 2

# Overlay the center image onto the QR code
img.paste(center_image_resized, (center_x, center_y), center_image_resized)

# Save the resulting QR code with the center image
output_path = "generated_qr.png"
img.save(output_path)

print(f"QR code with vertical gradient and center image saved to '{output_path}'.")
