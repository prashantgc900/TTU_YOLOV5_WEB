This repository provides a web interface to detect anamolies in sensor images using Yolov5.

The steps to run the web interface can be found below:

1. Change to the directory "/Multiple/updated/" using cd command.
cd "/Multiple/updated/"

2. Run the command flask run.
flask run

3. Go to the website http://127.0.0.1:5000 on your local web browser. You will be directed toward the web interface.
4. Select the files and upload them using Upload Button.
5. After clicking the Upload Button, the images will be stored in instance/upload/ with the current date and time folder. The Yolo model will be implemented on the images and the result annotated images will be  stored on /static/ folder with the current date and time folder. The annotated images will be displayed on the web interface.
6. The resulting image labels can be downloaded with the "Download Label Files" Button. The downloaded file will be in the form of zip.
7. You can filter the images with the drop-down button.

