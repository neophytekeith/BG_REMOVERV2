import streamlit as st
from rembg import remove
from PIL import Image
import io
from datetime import datetime
import pytz

# Function to get greeting based on time in the Philippines
def get_greeting():
    philippines_tz = pytz.timezone('Asia/Manila')
    current_time = datetime.now(philippines_tz)
    hour = current_time.hour

    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    elif 18 <= hour < 22:
        return "Good Evening"
    else:
        return "Good Night"

# Sidebar for light/dark mode toggle
mode = st.sidebar.radio("Select Mode", ("Light Mode", "Dark Mode"))

# CSS for Light and Dark modes
if mode == "Light Mode":
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
        .greeting {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            margin-top: 20px;
            color: #000;
            display: inline-block;
            animation: colorChange 5s infinite, fadeIn 2s ease-in-out;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #555;
        }
        /* Animation for color change and letter fade-in */
        @keyframes colorChange {
            0% { color: #4CAF50; }
            25% { color: #FF5733; }
            50% { color: #33A1FF; }
            75% { color: #FF33A1; }
            100% { color: #4CAF50; }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .greeting span {
            display: inline-block;
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        /* Delay the letter appearance */
        .greeting span:nth-child(1) { animation-delay: 0s; }
        .greeting span:nth-child(2) { animation-delay: 0.1s; }
        .greeting span:nth-child(3) { animation-delay: 0.2s; }
        .greeting span:nth-child(4) { animation-delay: 0.3s; }
        .greeting span:nth-child(5) { animation-delay: 0.4s; }
        .greeting span:nth-child(6) { animation-delay: 0.5s; }
        .greeting span:nth-child(7) { animation-delay: 0.6s; }
        .greeting span:nth-child(8) { animation-delay: 0.7s; }
        .greeting span:nth-child(9) { animation-delay: 0.8s; }
        .greeting span:nth-child(10) { animation-delay: 0.9s; }
        .greeting span:nth-child(11) { animation-delay: 1s; }
        </style>
        """,
        unsafe_allow_html=True
    )

else:  # Dark Mode
    st.markdown(
        """
        <style>
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #BB86FC;
            margin-bottom: 20px;
        }
        .greeting {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            margin-top: 20px;
            color: #fff;
            display: inline-block;
            animation: colorChange 5s infinite, fadeIn 2s ease-in-out;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #BBBBBB;
        }
        /* Animation for color change and letter fade-in */
        @keyframes colorChange {
            0% { color: #BB86FC; }
            25% { color: #03DAC6; }
            50% { color: #FF0266; }
            75% { color: #BB86FC; }
            100% { color: #03DAC6; }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .greeting span {
            display: inline-block;
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        /* Delay the letter appearance */
        .greeting span:nth-child(1) { animation-delay: 0s; }
        .greeting span:nth-child(2) { animation-delay: 0.1s; }
        .greeting span:nth-child(3) { animation-delay: 0.2s; }
        .greeting span:nth-child(4) { animation-delay: 0.3s; }
        .greeting span:nth-child(5) { animation-delay: 0.4s; }
        .greeting span:nth-child(6) { animation-delay: 0.5s; }
        .greeting span:nth-child(7) { animation-delay: 0.6s; }
        .greeting span:nth-child(8) { animation-delay: 0.7s; }
        .greeting span:nth-child(9) { animation-delay: 0.8s; }
        .greeting span:nth-child(10) { animation-delay: 0.9s; }
        .greeting span:nth-child(11) { animation-delay: 1s; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Header for BG Remover V2
st.markdown('<div class="main-title">BG Remover V2</div>', unsafe_allow_html=True)

# Greeting based on the time in the Philippines
greeting = get_greeting()

# Animated Greeting with proper handling of spaces
greeting_with_spaces = "".join([f"<span>{letter}</span>" if letter != " " else " " for letter in greeting])
st.markdown(f'<div class="greeting">{greeting_with_spaces}</div>', unsafe_allow_html=True)

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
