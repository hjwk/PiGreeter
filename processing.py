def detect_faces(cascade, grayscale):
    "Detects faces using a haarcascade in a grayscale image"
    return cascade.detectMultiScale(
        grayscale,
        scaleFactor=1.2,
        minNeighbors=5
    )

def load_images_labels(path, cascade):
    "Loads images from dataset"
    images_paths = [os.path.join(path, f) for f in os.listdir(path)]

    images = []
    labels = []
    names = []
    label = -1
    personName = ""
    for image_path in images_paths:
        img = cv2.imread(image_path)
        newPerson = os.path.split(image_path)[1].split('_')[0]
        if newPerson != personName:
            personName = newPerson
            names.append(personName)
            label = label + 1
        faces = detect_faces(cascade, img)
        for (x, y, w, h) in faces:
            image_resized = cv2.resize( img[y: y + h, x: x + w], (128, 128) )
            image_resized = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
            images.append(image_resized)
            labels.append(label)
            cv2.imshow("Adding faces to training set...", image_resized)
            cv2.waitKey(50)

    cv2.destroyAllWindows()
    return images, labels, names

def process_faces(faces, img):
    "Crops image to separates faces"
    f = []
    for (x, y, w, h) in faces:
        f.append( img[y:y + h, x:x + w] )
    
    return f

def recognize_faces(faces, recognizer, frame):
    "Recognize faces in a list and reacts"
    nbr_predicted = []
    for (x, y, w, h) in faces:
        nbr_predicted.append(recognizer.predict(frame[y:y + h, x:x + h]))
 
    return nbr_predicted

def load_names():
    "Loads people's names from the names.yml file"
    with open('names.yml') as f:
        names = f.read().splitlines()

    return names

def save_names(names):
    "Saves people's names in a .yml file to be loaded later"
    namesFile = open("names.yml", 'w')
    for name in names:
        namesFile.write(name + '\n')
    
    namesFile.close()