import streamlit as st
import yt_dlp
import os


def download_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_video.%(ext)s',  # Specify filename
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            duration = info_dict.get('duration', 0)
            thumbnail = info_dict.get('thumbnail', '')
            # Download video
            ydl.download([url])  # Directly download the video
        return 'downloaded_video.mp4', title, duration, thumbnail
    except Exception as e:
        return str(e), '', 0, ''


st.title("VidGrabber")

url = st.text_input("Enter YouTube Shorts URL:")

if st.button("Extract Video"):
    if url:
        with st.spinner("Extracting..."):
            downloaded_file, title, duration, thumbnail = download_video(url)

        if os.path.exists(downloaded_file):
            st.success("Download complete!")

            # Display video details
            st.subheader("Video Details:")
            st.write(f"**Title:** {title}")
            st.write(f"**Duration:** {duration // 60} minutes {duration % 60} seconds")

            # Display thumbnail image
            if thumbnail:
                st.image(thumbnail, caption=f"{title}", use_container_width=True)

            # Provide the download button
            with open(downloaded_file, "rb") as f:
                st.download_button(
                    label="Download Video",
                    data=f,
                    file_name=downloaded_file,
                    mime="video/mp4"
                )

            # Remove the file after download
            os.remove(downloaded_file)
        else:
            st.error(f"Failed to download video: {downloaded_file}")
