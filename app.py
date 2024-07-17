import streamlit as st
import os
import tempfile
import cv2
from ultralytics import YOLO
from object_counter import ObjectCounter
import json
import pandas as pd


# OpenCV imshow environment config for Linux
# os.environ['QT_QPA_PLATFORM'] = 'xcb'

# Set Page Config
st.set_page_config(
    page_title="Dashcam Footage Analysis",
    page_icon=":train2:",
    menu_items=None
)

# CSS Markdown For Button
st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

# Initialize session state
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Streamlit application Title
st.title("Dashcam Footage Analysis")

# Function to process the video
def process_video(videoFilepath):

    try:
        os.makedirs(os.path.join('artifacts','model'), exist_ok=True)
        os.makedirs(os.path.join('artifacts','output'), exist_ok=True)
    except OSError as e:
        raise e

    model = YOLO("artifacts/model/yolov8m.pt")

    line_points = [(0, 1000), (1920, 1000), (1920, 750), (0, 750), (0, 1000)]  # line or region points
    # line_points = [(0, 800), (1920, 800)]  # line or region points
    # Define class names for all classes you're tracking
    classes_names = {0: 'pedestrian', 1: 'vehicle', 2: 'vehicle', 3: 'vehicle', 5: 'vehicle', 7: 'vehicle'}
    classes_to_count = [0, 1, 2, 3, 5, 7] # person, bicycle, car, motorcycle, bus, truck

    cap = cv2.VideoCapture(videoFilepath)
    assert cap.isOpened(), "Error reading video file"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH,
                 cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Video writer
    video_writer = cv2.VideoWriter(
        "artifacts/output/dashcam_footage_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Init Object Counter
    counter = ObjectCounter(
        view_img=False,
        reg_pts=line_points,
        classes_names=classes_names,
        draw_tracks=True,
        line_thickness=3,
        track_thickness=3,
        region_thickness=3,
        count_reg_color=(255, 255, 255)
    )

    # Frame counter
    frame_count = 0

    # Define frame skip rate (process every nth frame)
    skip_rate = 1  # Process every Nth frame

    # Progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Video processing completed successfully.")
            break

        if frame_count % skip_rate == 0:
            tracks = model.track(
                frame, persist=True, show=False, verbose=True, classes=classes_to_count, conf=0.4, tracker="bytetrack.yaml")
            frame = counter.start_counting(frame, tracks)
            video_writer.write(frame)

        # Increment frame counter
        frame_count += 1

        # Update progress
        progress_percentage = int((frame_count / total_frames) * 100)
        progress_bar.progress(progress_percentage)
        progress_text.text(
            f"Processing frame {frame_count}/{total_frames} ({progress_percentage}%)")

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

    result = counter.class_wise_count
    st.session_state.video_processed = True
    return result

# Function to display the results
def display_results(result):
    if st.session_state.video_processed:
        vehicle_counting = {}
        vehicle_counting_df = {"Founding": [], "Count": []}
        
        # Display the result
        for r in result:
            total = result[r]['IN'] + result[r]['OUT']
            if total > 0:
                vehicle_counting[r.capitalize()] = total
                vehicle_counting_df['Founding'].append(r.capitalize())
                vehicle_counting_df['Count'].append(total)

        st.write(pd.DataFrame(vehicle_counting_df))

        with open('artifacts/output/result.json', 'w') as json_file:
            json.dump(vehicle_counting, json_file, indent=4)

        col1, col2 = st.columns([1, 1])
        with col1:
            with open('artifacts/output/result.json', 'rb') as f:
                st.download_button('Download Result', f, file_name='result.json')

        with col2:
            with open('artifacts/output/dashcam_footage_counting_output.mp4', 'rb') as f:
                st.download_button('Download Processed Video', f, file_name='processed_video.mp4')

# Function to change video processing state 
def change_video_processed_state(state=False):
    st.session_state.video_processed = state

# File uploader
uploaded_file = st.file_uploader(" ", type=["mp4"], on_change=change_video_processed_state)

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_filepath = tmp_file.name
    
    if not st.session_state.video_processed:
        # Process the video
        st.session_state.result = process_video(tmp_filepath)

    if st.session_state.video_processed:
        display_results(st.session_state.result)

    # Optionally, delete the temporary file
    os.remove(tmp_filepath)

    

    


