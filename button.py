import cv2 as cv


class Button:
    # Initialization
    def __init__(self, position, width, height, text, color=(255, 255, 255)):

        self.position = position
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self, image):

        cv.rectangle(img=image, pt1=self.position, pt2=(
            self.position[0]+self.width, self.position[1]+self.height), color=self.color, thickness=cv.FILLED)

        # Border
        cv.rectangle(img=image, pt1=self.position, pt2=(
            self.position[0]+self.width, self.position[1]+self.height), color=(0, 0, 0), thickness=3)

        # Text
        cv.putText(img=image, text=self.text, org=(self.position[0]+40, self.position[1]+60),
                   fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 0), thickness=2)

    def clicked(self, image, x, y):

        if self.position[0] < x < self.position[0]+self.width and self.position[1] < y < self.position[1]+self.height:

            cv.rectangle(img=image, pt1=self.position, pt2=(
                self.position[0]+self.width, self.position[1]+self.height), color=(255, 255, 255), thickness=cv.FILLED)

            cv.rectangle(img=image, pt1=self.position, pt2=(
                self.position[0]+self.width, self.position[1]+self.height), color=(0, 0, 0), thickness=3)

            cv.putText(img=image, text=self.text, org=(self.position[0]+20, self.position[1]+70),
                       fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=5, color=(0, 0, 0), thickness=5)

            return True

        else:
            return False
