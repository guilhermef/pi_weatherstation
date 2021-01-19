class Display:
    def display_image(self, img_data):
        with open("test.png", "wb") as f:
            f.write(img_data)
