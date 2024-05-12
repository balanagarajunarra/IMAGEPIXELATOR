import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageFilter

MAX_IMAGE_SIZE = 178956970  # Maximum number of pixels allowed

def upscale_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
    return resized_image

def increase_sharpness(image):
    # Convert image to PIL format
    pil_image = Image.fromarray(image)

    # Apply sharpening filter
    sharpened_image = pil_image.filter(ImageFilter.SHARPEN)

    # Convert back to numpy array
    sharpened_array = np.array(sharpened_image)
    return sharpened_array

def main():
    st.title("Image Upscaler")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Check if image size exceeds the limit
        if image.size > MAX_IMAGE_SIZE:
            st.error("Image size exceeds the limit. Please upload a smaller image.")
            return

        st.image(image, caption="Original Image", use_column_width=True)

        # Define slider for scale percent
        scale_percent = st.slider("Select scale percent", 100, 500, 200)

        if st.button("Upscale Image"):
            upscaled_image = upscale_image(image, scale_percent)
            sharpened_image = increase_sharpness(upscaled_image)
            st.image(sharpened_image, caption="Upscaled & Sharpened Image", use_column_width=True)

            # Save the upscaled and sharpened image
            pil_image = Image.fromarray(sharpened_image)
            st.write("### Download Upscaled & Sharpened Image")
            st.download_button(
                label="Download",
                data=pil_image,
                file_name="upscaled_sharpened_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
