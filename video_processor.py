from ultralytics import YOLO
import cv2
# import os

# Define the path to your custom YOLO model
model = YOLO('polyp6.pt')


def process_video(video_path):
    try:
        # load video
        # source = video_path
        cap = cv2.VideoCapture(video_path)

        ret = True
        out = None
        # read frames
        while ret:
            ret, frame = cap.read()

            if ret:

                # detect objects
                # track objects
                results = model.track(frame, persist=False)

                # plot results
                frame_ = results[0].plot()

                # Define the desired output resolution
                output_width = 640  # Set the desired width
                output_height = 360  # Set the desired height

                # visualize
                # resized_frame = cv2.resize(frame_, (frame.shape[1], frame.shape[0]))
                resized_frame = cv2.resize(frame_, (output_width, output_height))

                # To show video while processing:
                # cv2.imshow('frame', resized_frame)

                # Get the original filename and format extension
                # original_filename, extension = os.path.splitext(video_path)

                # Modify the frame rate (fps) parameter in the cv2.VideoWriter constructor
                fps = 15  # Set the desired frame rate (e.g., 15 frames per second)

                # Create VideoWriter object if not already created
                if out is None:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter('static/output.mp4', fourcc, fps, (output_width, output_height))

                # Write the frame into the file 'output.mp4'
                out.write(resized_frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        # Release everything if job is finished
        cap.release()
        if out is not None:
            out.release()
        cv2.destroyAllWindows()

        # Output response and path
        video_path = 'static/output.mp4'
        output = "The video has been processed through the YOLO model"

        return video_path, output

    except Exception as e:
        # Handle any exceptions that occurred during image retrieval or processing
        error_message = str(e)
        return None, error_message  # Return None for the image and the error message

# For Testing          
# process_video('static/input.mp4')
