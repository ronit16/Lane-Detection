import streamlit as st
import os
from main import FindLaneLines

# Function to process image
def process_image(input_path, output_path):
    findLaneLines = FindLaneLines()
    try:
        st.info("Processing image...")
        with st.spinner('Processing...'):
            findLaneLines.process_image(input_path, output_path)
        st.success("Image processed successfully!")
        st.image(output_path, caption="Processed Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# Function to process video
def process_video(input_path, output_path):
    findLaneLines = FindLaneLines()
    try:
        st.info("Processing video...")
        with st.spinner('Processing...'):
            findLaneLines.process_video(input_path, output_path)
        st.success("Video processed successfully!")
        st.video(output_path, format='mp4')
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")

# Main Streamlit app
def main():
    st.title("Lane Lines Detection")

    # Option to select image or video
    option = st.radio("Select Input Type:", ("Image", "Video"))

    if option == "Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            input_path = os.path.join("uploads", uploaded_file.name)
            output_path = os.path.join("outputs", "processed_image.jpg")
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.image(uploaded_file, caption="Original Image", use_column_width=True)
            process_image(input_path, output_path)

    elif option == "Video":
        uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
        if uploaded_file is not None:
            input_path = os.path.join("uploads", uploaded_file.name)
            output_path = os.path.join("outputs", "processed_video.mp4")
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            process_video(input_path, output_path)

if __name__ == "__main__":
    main()
