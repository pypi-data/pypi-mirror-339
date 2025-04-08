import cv2
import os
from time import time
from PIL import Image
import numpy as np
import PowerDB as pdb
def make_project(projectpath: str, message_callback=None):
    try:
        os.makedirs(os.path.join(projectpath, 'data'), exist_ok=True)
        os.makedirs(os.path.join(projectpath, 'data', 'classifiers'), exist_ok=True)
        cascade_path = os.path.join(projectpath, 'data', 'haarcascade_frontalface_default.xml')
        source_cascade_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
        if not os.path.exists(cascade_path):
            try:
                with open(source_cascade_path, 'r') as d, open(cascade_path, 'w') as f:
                    f.write(d.read())
            except FileNotFoundError:
                if message_callback:
                    message_callback(f"Error: Haar cascade file not found at '{source_cascade_path}'")
                    return
        pdb.create.make_db(os.path.join(projectpath, 'data', 'userlist.pdb'))
        pdb.create.make_container(os.path.join(projectpath, 'data', 'userlist.pdb'), 'users')
        if message_callback:
            message_callback(f"Project created (if successful) at: {projectpath}")
    except (PermissionError, OSError) as e:
        if message_callback:
            message_callback(f'ERROR during project creation: {e}')
def add_user(projectpath: str, username: str, message_callback=None):
    names = set()
    try:
        z = pdb.container_data.readsectors(os.path.join(projectpath, 'data', 'userlist.pdb'), 0)
    except FileNotFoundError:
        if message_callback:
            message_callback('Error: database file does not exist')
        return
    for i in z:
        names.add(i)
    un = username
    if un == "None":
        if message_callback:
            message_callback("Error: Name cannot be 'None'")
    elif un in names:
        if message_callback:
           message_callback("Error: User already exists!")
    elif len(un) == 0:
        if message_callback:
           message_callback("Error: Name cannot be empty!")
    else:
        name = un
        names.add(name)
        for b in range(len(names)):
            pdb.container_data.insert(os.path.join(projectpath, 'data', 'userlist.pdb'), list(names)[b], [0, b])
        if message_callback:
            message_callback(f"User '{username}' added (if successful).")
def capture_data(projectpath: str, username: str, cameraindex: int = 0, windowed: bool = True, message_callback=None):
    path = os.path.join(projectpath, 'data', username)
    num_of_images = 0
    try:
        detector = cv2.CascadeClassifier(os.path.join(projectpath, 'data', 'haarcascade_frontalface_default.xml'))
    except Exception as e:
        if message_callback:
            message_callback(f'Cascade file does not exist: {e}')
        return
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        if message_callback:
            message_callback(f'Error creating directory: {e}')
        return
    vid = cv2.VideoCapture(cameraindex)
    if not vid.isOpened():
        if message_callback:
            message_callback(f"Error: Could not open camera with index {cameraindex}")
        return
    if message_callback:
        message_callback('Capturing data is in action')
    while True:
        ret, img = vid.read()
        if not ret:
            if message_callback:
                message_callback("Error: Could not read frame.")
            break
        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images) + " images captured"), (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            new_img = img[y:y + h, x:x + w]
            break  # Capture only the first detected face in a frame
        if new_img is not None:  # Only save if a face was detected
            try:
                cv2.imwrite(os.path.join(path, f"{num_of_images}{username}.jpg"), new_img)
                num_of_images += 1
            except Exception as e:
                if message_callback:
                    message_callback(f"Error saving image: {e}")
        if windowed is True:
            cv2.imshow("Face Detection", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        if num_of_images > 300:  # take 300 frames
            break
    vid.release()
    if windowed is True:
        cv2.destroyAllWindows()
    if message_callback:
        message_callback(f"Data capture for '{username}' complete. {num_of_images} images captured.")
def train_data(projectpath: str, username: str, message_callback=None):
    try:
        path = os.path.join(projectpath, "data", username)
        faces = []
        ids = []
        labels = []
        pictures = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for pic in pictures:
            try:
                imgpath = os.path.join(path, pic)
                img = Image.open(imgpath).convert('L')
                imageNp = np.array(img, 'uint8')
                user_id = int(pic.split(username)[0])
                faces.append(imageNp)
                ids.append(user_id)
            except Exception as e:
                if message_callback:
                    message_callback(f"Error processing image {pic}: {e}")
        ids = np.array(ids)
        if not faces:
            if message_callback:
                message_callback(f"No face data found for user '{username}' to train.")
            return
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        classifier_path = os.path.join(projectpath, "data", "classifiers", f"{username}_classifier.xml")
        clf.write(classifier_path)
        if message_callback:
            message_callback(f"Training data for '{username}' complete. Classifier saved to '{classifier_path}'.")
    except FileNotFoundError:
        if message_callback:
            message_callback(f'Path does not exist: {os.path.join(projectpath, "data", username)}')
    except Exception as e:
        if message_callback:
            message_callback(f"An error occurred during training: {e}")
def check_user(projectpath: str, username: str, cameraindex: int = 0, timeout: int = 5, windowed: bool = True, message_callback=None, recognition_threshold=50):
    cap = None
    try:
        face_cascade = cv2.CascadeClassifier(os.path.join(projectpath, 'data', 'haarcascade_frontalface_default.xml'))
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        classifier_path = os.path.join(projectpath, "data", "classifiers", f"{username}_classifier.xml")
        if not os.path.exists(classifier_path):
            if message_callback:
                message_callback(f"Error: Classifier not found at '{classifier_path}' for user '{username}'. Please train data first.")
            return False
        recognizer.read(classifier_path)
        cap = cv2.VideoCapture(cameraindex)
        if not cap.isOpened():
            if message_callback:
                message_callback(f"Error: Could not open camera with index {cameraindex} for checking.")
            return False
        start_time = time()
        recognized = False
        while True:
            ret, frame = cap.read()
            if not ret:
                if message_callback:
                    message_callback("Error: Could not read frame during checking.")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                try:
                    id_, confidence = recognizer.predict(roi_gray)
                    confidence = 100 - int(confidence)
                    if confidence > recognition_threshold:
                        recognized = True
                        text = 'Recognized: ' + username.upper()
                        font = cv2.FONT_HERSHEY_PLAIN
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                        if windowed:
                            cv2.imshow("image", frame)
                            cv2.waitKey(500)
                        if message_callback:
                            message_callback('Congrats, You have already checked in')
                        cap.release()
                        if windowed:
                            cv2.destroyAllWindows()
                        return True
                    else:
                        text = "Unknown Face"
                        font = cv2.FONT_HERSHEY_PLAIN
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                except Exception as e:
                    if message_callback:
                        message_callback(f"Error during recognition: {e}")
            if windowed:
                cv2.imshow("image", frame)
            elapsed_time = time() - start_time
            if elapsed_time >= timeout:
                cap.release()
                if windowed:
                    cv2.destroyAllWindows()
                if message_callback:
                    message_callback('Alert, Please check in again')
                return False
            if cv2.waitKey(20) & 0xFF == ord('q'):
                cap.release()
                if windowed:
                    cv2.destroyAllWindows()
                return False
    except FileNotFoundError:
        if message_callback:
            message_callback('Error: either cascade or classifier is not found')
        return False
    except Exception as e:
        if message_callback:
            message_callback(f"An error occurred during check_user: {e}")
        return False
    finally:
        if cap is not None and cap.isOpened():
            cap.release()
        if windowed:
            cv2.destroyAllWindows()
def remove_user(projectpath: str, username: str, message_callback=None):
    db_path = os.path.join(projectpath, 'data', 'userlist.pdb')
    classifier_file = os.path.join(projectpath, 'data', 'classifiers', f'{username}_classifier.xml')
    user_data_dir = os.path.join(projectpath, 'data', username)
    try:
        all_users = pdb.container_data.readsectors(db_path, 0)
        if username in all_users:
            user_index = all_users.index(username)
            pdb.container_data.delete(db_path, [0, user_index])
            if message_callback:
                message_callback(f"User '{username}' removed from the database.")
        else:
            if message_callback:
                message_callback(f"Error: Username '{username}' not found in the database.")
    except FileNotFoundError:
        if message_callback:
            message_callback('ERROR!! Database file not found.')
        return
    except ValueError:
        if message_callback:
            message_callback(f'ERROR!! Username \'{username}\' does not exist in the database.')
        return
    except Exception as e:
        if message_callback:
            message_callback(f"An error occurred while removing user from database: {e}")
    try:
        if os.path.exists(classifier_file):
            os.remove(classifier_file)
            if message_callback:
                message_callback(f"Classifier file for '{username}' removed.")
        else:
            if message_callback:
                message_callback(f"Warning: Classifier file for '{username}' not found.")
    except (OSError, PermissionError) as e:
        if message_callback:
            message_callback(f'ERROR!! Could not remove classifier file: {e}')
    try:
        if os.path.exists(user_data_dir):
            files = [f for f in os.listdir(user_data_dir) if os.path.isfile(os.path.join(user_data_dir, f))]
            for i in files:
                os.remove(os.path.join(user_data_dir, i))
            os.rmdir(user_data_dir)
            if message_callback:
                message_callback(f"Data directory for '{username}' removed.")
        else:
            if message_callback:
                message_callback(f"Warning: Data directory for '{username}' not found.")
    except (FileNotFoundError, OSError, PermissionError) as e:
        if message_callback:
            message_callback(f'ERROR!! Could not remove user data directory: {e}')
    if message_callback:
        all_users_after_removal = pdb.container_data.readsectors(db_path, 0)
        classifier_exists = os.path.exists(classifier_file)
        data_dir_exists = os.path.exists(user_data_dir)
        if username not in all_users_after_removal and not classifier_exists and not data_dir_exists:
            message_callback('All data about the user got removed (if files existed).')
def full_setup(projectpath: str, username: str, cameraindex: int = 0, windowed: bool = True, message_callback=None):
    make_project(projectpath, message_callback)
    add_user(projectpath, username, message_callback)
    capture_data(projectpath, username, cameraindex, windowed, message_callback)
    train_data(projectpath, username, message_callback)
#THE END