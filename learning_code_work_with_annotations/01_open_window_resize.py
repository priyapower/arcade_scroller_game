"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Priya's 2D Funhouse - Resize"
# Resizeable window
START = 0
END = 2000
STEP = 50

class MyGame(arcade.Window):
    """
    Main application class.
    """

    # Now the initialize can take in width, height, and title
    def __init__(self, width, height, title):
        # the Windows class initialization sets resizable to true
        super().__init__(width, height, title, resizable=True)

        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    def on_resize(self, width, height):
        """ This method is automatically called when the window is resized. """

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
        # edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        # The following is to visually see the resize happening because it basically creates Quadrant I of the Cartesean Plane with increments by 50

        # Draw the y labels
        i = 0
        for y in range(START, END, STEP):
            arcade.draw_point(0, y, arcade.color.BLUE, 5)
            arcade.draw_text(f"{y}", 5, y, arcade.color.BLACK, 12, anchor_x="left", anchor_y="bottom")
            i += 1

        # Draw the x labels.
        i = 1
        for x in range(START + STEP, END, STEP):
            arcade.draw_point(x, 0, arcade.color.BLUE, 5)
            arcade.draw_text(f"{x}", x, 5, arcade.color.BLACK, 12, anchor_x="left", anchor_y="bottom")
            i += 1

def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()