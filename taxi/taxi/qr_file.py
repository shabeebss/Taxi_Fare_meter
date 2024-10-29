# import cv2
# from pyzbar import pyzbar
#
#
# def read_barcodes(frame):
#     # Decode barcodes and QR codes from the frame
#     barcodes = pyzbar.decode(frame)
#     for barcode in barcodes:
#         # Get the coordinates of the barcode
#         x, y, w, h = barcode.rect
#         barcode_text = barcode.data.decode('utf-8')  # Decode the barcode data
#         print("Detected QR Code:\n", barcode_text)
#
#         # Draw a rectangle around the barcode
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#         # Optionally, put the decoded text above the rectangle
#         cv2.putText(frame, barcode_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#     return frame
#
#
# def main():
#     # Open the camera (0 for the default camera)
#     camera = cv2.VideoCapture(0)
#
#     if not camera.isOpened():
#         print("Error: Camera not found.")
#         return
#
#     while True:
#         ret, frame = camera.read()  # Read a frame from the camera
#         if not ret:
#             print("Error: Could not read frame.")
#             break
#
#         # Read the barcodes in the current frame
#         frame = read_barcodes(frame)
#
#         # Display the frame with detected barcodes
#         cv2.imshow('Barcode Reader', frame)
#
#         # Exit the loop when the 'Esc' key is pressed
#         if cv2.waitKey(1) & 0xFF == 27:
#             break
#
#     # Release the camera and close the window
#     camera.release()
#     cv2.destroyAllWindows()
#
