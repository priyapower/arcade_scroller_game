"""
Platformer Game
"""
# Imports arcade library
import arcade

# Constants needed for this file
# These represent our fixed window screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Creates a MyGame Class that passes the arcade Window class
# (The Window class forms the basis of most advanced games that use Arcade. It represents a window on the screen, and manages events.)
class MyGame(arcade.Window):
    """
    Main application class.
    """

    # Initializes this class
    def __init__(self):

        # Call the parent class (Window Class from arcade) and set up the window based on the constants from above
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # This lets us set a background color, specifically using the CSS color schemes, selecting cornflower_blue
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    # This will eventually hold our setup
    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    # This will eventually hold our drawing functions
    def on_draw(self):
        """ Render the screen. """

        # Get Arcade to actually do some of the drawing commands that we issue
        arcade.start_render()
        # Code to draw the screen goes here

# This function is outside the MyGame class so that it can call an instance of that class
def main():
    """ Main method """
    # Call an instance of the MyGame class and set it to the variable "window"
    window = MyGame()
    # Call the .setup function from MyGame class
    window.setup()
    # Run the app
    arcade.run()

if __name__ == "__main__":
    main()