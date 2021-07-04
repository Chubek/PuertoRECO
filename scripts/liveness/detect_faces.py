from mtcnn import MTCNN

def get_face_bboxes(img_array):
    detector = MTCNN()

    detection = detector.detect_faces(img_array)

    return [det['box'] for det in detection]