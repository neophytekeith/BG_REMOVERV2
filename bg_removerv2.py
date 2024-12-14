import streamlit as st
from rembg import remove
from PIL import Image
import io

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px 20px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="main-title">Background Remover</div>', unsafe_allow_html=True)

# Sidebar for feedback
st.sidebar.header("Feedback")
feedback = st.sidebar.text_area("What do you think about this app?")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open the uploaded image
    input_image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(input_image, caption="Uploaded Image", use_container_width=True)
    
    # Process the image with progress indicator
    with st.spinner("Removing background..."):
        # Convert image to binary for rembg
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()
        
        # Remove background
        output_bytes = remove(input_bytes)
        output_image = Image.open(io.BytesIO(output_bytes))
    
    # Display the processed image
    st.image(output_image, caption="Image with Background Removed", use_container_width=True)

    # Download button for the output image
    output_file = io.BytesIO()
    output_image.save(output_file, format="PNG")
    output_file.seek(0)
    st.download_button(
        label="Download Image with Removed Background",
        data=output_file,
        file_name="removed_bg.png",
        mime="image/png"
    )

    # Optional: Add background replacement (simple color example)
    st.markdown("### Replace Background (Optional)")
    bg_color = st.color_picker("Pick a background color", "#ffffff")
    if st.button("Apply Background Color"):
        with st.spinner("Applying background..."):
            # Create a new image with the selected background color
            new_bg = Image.new("RGBA", output_image.size, bg_color)
            final_image = Image.alpha_composite(new_bg, output_image.convert("RGBA"))
            st.image(final_image, caption="Image with New Background", use_container_width=True)

            # Download button for new background image
            final_file = io.BytesIO()
            final_image.save(final_file, format="PNG")
            final_file.seek(0)
            st.download_button(
                label="Download Image with New Background",
                data=final_file,
                file_name="new_bg_image.png",
                mime="image/png"
            )

# Footer
st.markdown('<div class="footer">Developed by: Keith Renz</div>', unsafe_allow_html=True)
