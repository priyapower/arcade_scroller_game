"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 15

# How many pixels to keep as a minimum margin between the character and the edge of the screen.
# What is the distance between a screen edge and the player before the world begins to scroll?
    # This is what we are declaring as margins for each edge: left, right, bottom, and top
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        # MY USER CONTROL UPDATES
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used to keep track of our scrolling
        # These set the original variables of the game for view_bottom and view_left to the integer value 0
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        # Why is this created in __init__ as well as in setup?
            # Potentially for the "restart" option?
        self.view_bottom = 0
        self.view_left = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            image_source2 = ":resources:images/tiles/grassMid.png"
            wall = arcade.Sprite(image_source2, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            image_source3 = ":resources:images/tiles/boxCrate_double.png"
            wall = arcade.Sprite(image_source3, TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """
        # MY USER CONTROL UPDATES
        self.player_sprite.change_x = 0

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        self.player_list.update()
        # Move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport
        # Begins with a boolean variable, "changed", that is set to false (used further down in "if changed" block)
        changed = False

        # Scroll left
        # This sets up the view_left (which is set to 0) summed with the custom margin we set for the left edge
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        # If the player's left coord is less than the left boundary from above
            # .left: https://arcade.academy/arcade.html?highlight=.left#arcade.Sprite.left
            # Return the x coordinate of the left-side of the sprite’s hit box
        if self.player_sprite.left < left_boundary:
            # "-=" is called subtraction assignment: https://python-reference.readthedocs.io/en/latest/docs/operators/subtraction_assignment.html
                # Subtracts a value from the variable and assigns the result to that variable.
            # In this case, first take the left_boundary from above and subtract the player's left coord
            # THEN, subtract that from view_left and reassign view_left with this new number
            # It makes sense that this value is negative, because we would be heading left, aka, in the negative direction on the x-axis
            self.view_left -= left_boundary - self.player_sprite.left
            # Finally, update "changed" to True
            changed = True

        # Scroll right
        # The right_boundary must include the screen width as a component
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        # If a players right coord attempts to exceed the right boundary
        if self.player_sprite.right > right_boundary:
            # Because this is on the right side of the screen, we want to use addition assignment
            # view_left is now a positive value because we are heading right, or in the positive direction on the x-axis
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        # Very similar to above if-block, bit takes in Height and the Top/Bottom viewport margins
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        # This does not need height
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        # Here is where all the above if-blocks come into play
        # If changed is true, then this means our player is attempting to go past the margins near the edge
        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            # .set_viewport: https://arcade.academy/arcade.html?highlight=.set_viewport#arcade.set_viewport
            # This sets what coordinates the window will cover.
            # By default, the lower left coordinate will be (0, 0) and the top y coordinate will be the height of the window in pixels, and the right x coordinate will be the width of the window in pixels.
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()