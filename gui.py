import cv2

def drawString(img, text, coord, color, fontScale, fontFace, thickness):
    
    # Get the text size & baseline.
    textSize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    baseline += thickness

    # Adjust the coords for left/right-justified or top/bottom-justified.
    coord = list(coord)
    height, width, channels = img.shape
    if coord[1] >= 0:
        # Coordinates are for the top-left corner of the text from the top-left of the image, so move down by one row.
        coord[1] += textSize[1]
    else:
        # Coordinates are for the bottom-left corner of the text from the bottom-left of the image, so come up from the bottom.
        coord[1] += height - baseline + 1

    # Become right-justified if desired.
    if coord[0] < 0 :
        coord[0] += width - textSize[0] + 1

    # Get the bounding box around the text.
    boundingRect = (coord[0], coord[1] - textSize[0], textSize[1], baseline + textSize[1])

    # Draw anti-aliased text.
    cv2.putText(img, text, (coord[0], coord[1]), fontFace, fontScale, color, thickness, cv2.LINE_AA)

    # Let the user know how big their text is, in case they want to arrange things.
    return boundingRect