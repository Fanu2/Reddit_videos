import cv2
import numpy as np

# Paths to the input images and output video
image_path1 = '/home/jasvir/Pictures/morph/image1.png'
image_path2 = '/home/jasvir/Pictures/morph/image2.png'
output_path = '/home/jasvir/Pictures/morph/metamorphosis.mp4'

# Load the two images
img1 = cv2.imread(image_path1)
img2 = cv2.imread(image_path2)

# Check if images are the same size, resize if not
if img1.shape != img2.shape:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID'
fps = 30
num_frames = 60
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (img1.shape[1], img1.shape[0]))

# Generate frames for the metamorphosis
for i in range(num_frames):
    alpha = i / float(num_frames - 1)  # Interpolation factor
    blended_image = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)

    # Write frame to video
    video_writer.write(blended_image)

# Release the video writer object
video_writer.release()

print(f"Metamorphosis video created at {output_path}")
