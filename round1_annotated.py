"""
Platformer Game
"""
import arcade

# Fixed Screen Size Constants
    # HOW WOULD YOU UPDATE THIS CODE/THIS SECTION IF THE SCREEN COULD BE FULL SCREEN OR DYNAMICALLY CHANGING (See you 01 file updates about resizing)
# Sets the width of the screen to a fixed 1000
SCREEN_WIDTH = 1000
# Sets the height of the screen to a fixed 650
SCREEN_HEIGHT = 650
# Sets the window title to "Priya's 2D Funhouse"
SCREEN_TITLE = "Priya's 2D Funhouse"

# Constants used to scale our sprites from their original size
# Character
CHARACTER_SCALING = 1
# Tile
TILE_SCALING = 0.5
# Coin/ItemsForPickup
COIN_SCALING = 0.5
# Sprite Pixels
SPRITE_PIXEL_SIZE = 128
# Grid Pixels set up by multiplying the pixel size and the tile scaling
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
# Players R,L speed (used to be 10)
PLAYER_MOVEMENT_SPEED = 3
# Players U speed (used to be 20)
PLAYER_JUMP_SPEED = 13
# Constant that represents gravities downward force
# Players D speed (used to be 1)
GRAVITY = 0.8

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
# What is the distance between a screen edge and the player before the world begins to scroll?
    # This is what we are declaring as margins for each edge: left, right, bottom, and top
# If you approach 200 pixels to the left, begin scrolling left
LEFT_VIEWPORT_MARGIN = 200
# If you approach 200 pixels to the right, begin scrolling right
RIGHT_VIEWPORT_MARGIN = 200
# If you approach 150 pixels from the bottom, begin scrolling down
BOTTOM_VIEWPORT_MARGIN = 150
# If you approach 100 pixels from the top, begin scrolling up
TOP_VIEWPORT_MARGIN = 100

# Declares an official start coordinate for your player
    # Sets them BOTTOM LEFT
# Players horizontal position
PLAYER_START_X = 64
# Players vertical position
PLAYER_START_Y = 225


# Creates a MyGame Class that passes the arcade Window class
# (The Window class forms the basis of most advanced games that use Arcade. It represents a window on the screen, and manages events.)
class MyGame(arcade.Window):
    """
    Main application class.
    """

    # Initializes this class; We can create variables and self attributes here
    def __init__(self):

        # Call the parent class (Window Class from arcade) and set up the window based on the constants from above
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should go into a list.
        # The None keyword is used to define a null value, or no value at all.
        # Basically, we are just setting up these variables on self, but they currently have no value

        # For coins we pick up
        self.coin_list = None
        # For walls we can't move through
        self.wall_list = None
        # For the foreground map our players can move behind
        self.foreground_list = None
        # For the background map our players can move in front of
        self.background_list = None
        # For the do not touch map our players will be penalized for hitting
        self.dont_touch_list = None
        # For our player
        self.player_list = None
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine; currently just a (None/Null) variable on self that can be called - will be activated below (in setup, update, and scrolling methods)
        self.physics_engine = None

        # MY USER CONTROL UPDATES
        # Sets self attributes of pressing keys all to False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

        # A level counter - default is set to level 1, increments by 1 in the update method (if player reaches the very right side of the map)
        self.level = 1

        # Load sounds from local directory of "sounds"
        # Sound for collecting coins/collectibles
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        # Sound for player jumping or pressing up
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        # Sound for a player making a mistake (hitting the do not touch; falling off the edge; hitting future enemies)
        self.game_over = arcade.load_sound("sounds/gameover1.wav")

    # This holds our setup (also called on the restarts)
    # Takes arguments of self and level
    # The setup actually creates the object instances, such as graphical sprites.
    # WHY keep init separate from setup?
        # With a setup method split out, later on we can easily add “restart/play again” functionality to the game.
        # A simple call to setup will reset everything.
        # Later, we can expand our game with different levels, and have functions such as setup_level_1 and setup_level_2. -> THIS IS SETUP IN THIS CODE
    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        # These lists save the entire SpriteList()
        # The SpriteList class optimizes drawing, movement, and collision detection.
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        # Our resource lives in the images folder
        # The optional second parameter will scale the sprite up or down
        # Example: if scaling is set to 0.5, and the the sprite is 128x128, then both width and height will be scaled down 50% for a 64x64 sprite.
        # Images are found locally in directory "images"
        image_source = "images/player_1/female_stand.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        # Where is the sprite on the screen?
        # Options for setting:
            # Sprite attribute center_x and center_y (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
            # Sprite attribute top, bottom, left, and right (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
            # Sprite attribute position (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
        # In this case, we set our center x/y to the Constants setup at the very top
        # In essence - this sets up our player sprite with a static start (especially helpful when a player has to restart a level)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        # Add the player_sprite to the player_list
        self.player_list.append(self.player_sprite)

        # ---------------------------------------------------------------------------------
        # ---------------------- Load in a map from the tiled editor ----------------------
        # ---------------------------------------------------------------------------------

        # MAP RULES
            # Maps were created with "Tiled" application
            # Maps have a file type of .tmx
            # Maps have 5 layers: Platforms; Coins; Foreground; Background; Don't Touch
            # If Map is missing any layer, game may not run
            # Maps must be named as "funhouse_level_<#>.tmx" - where the number increments by level incrementation

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "Don't Touch"

        # Map name
        # Dynamic Map Name that will cycle through all maps based on this file name (in update, self.level will continuously increase by 1, therefore, this file name will continuously update by 1)
        map_name = f"tmx_map/funhouse_level_{level}.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the variable "my_map" (the arcade read map) in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # THE FOLLOWING
            # Use Arcade to process the tile map
            # https://arcade.academy/arcade.html?highlight=process_layer#arcade.process_layer
            # parameters/arguments = (map_object,
                                    # layer_name,
                                    # scaling_up_or_down,
                                    # base_directory=where_to_load_images_from,
                                    # use_spatial_hash=boolean_for_whether_spatial,
                                    # hit_box_algorithm=None/Simple/Details,
                                    # hit_box_details=4.5_is_default
                                    # )

        # The wall_list, coin_list, and dont_touch_list use spatial hashing
        # Spatial hashing speeds the time it takes to find collisions, but increases the time it takes to move a sprite.
        # Since we don’t expect the walls or coins to move, we'll turn on spatial hashing for these lists.
        # This doesn't apply to player because a player will move a lot
        # This doesn't apply to the background/foregrounds because players don't "connect/touch" them - aka, there is no collision to detect here

        # ---------------------- Background ----------------------
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # ---------------------- Foreground ----------------------
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)

        # ---------------------- Platforms ----------------------
        # Unsure why there seems to be variable assignment in the parameters ???
        # self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
        #                                               layer_name=platforms_layer_name,
        #                                               scaling=TILE_SCALING,
        #                                               use_spatial_hash=True)


        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # ---------------------- Coins ----------------------
        self.coin_list = arcade.tilemap.process_layer(my_map,
                                                      coins_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # ---------------------- Don't Touch Layer ----------------------
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        # ---------------------- Other stuff ----------------------
        # Set the background color
        if my_map.background_color:
            # Creates a background color from the map (thus, background color will update every time a level is updated IF the map levels have different background colors, which they do in this project)
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        # https://arcade.academy/arcade.html#arcade.PhysicsEngineSimple
            # Simplistic physics engine for use in games without gravity, such as top-down games.
            # It is easier to get started with this engine than more sophisticated engines like PyMunk.
            # Note, it does not currently handle rotation.
        # This engine is what keeps our player from being able to walk through walls or solid objects or fall through the ground
        # The PhysicsEngineSimple class takes two parameters: The moving sprite, and a list of sprites the moving sprite can’t move through.
        # We are allowed to have more than one simple physics engine

        # WE UPGRADED to the PhysicsEnginePlatformer
            # https://arcade.academy/arcade.html?highlight=physicsengineplatformer#arcade.PhysicsEnginePlatformer
        # This takes 4 parameters (player_sprite,
                                 # platforms,
                                 # gravity_constant, (downward acceleration per frame)
                                 # ladders
                                 # )
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    # Holds our drawing functions (how we create visuals for the screen)
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        # Prime arcade to do the drawing commands we will issue after this line
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.dont_touch_list.draw()
        self.player_list.draw()
        self.foreground_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        # -------------------- A FUN UPDATE WOULD BE TO ADD A LEVEL COUNTER HERE --------------------

    # on_key_press: https://arcade.academy/arcade.html#arcade.View.on_key_press
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # # ---------------------- OLD KEY PRESS CODE ----------------------
        # # If a user presses Up, W, or Space
        # if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
        #     # If there isn't blocking the player from jumping
        #     if self.physics_engine.can_jump():
        #         # change_y: https://arcade.academy/arcade.html?highlight=change_y#arcade.Sprite.change_y
        #         # Increases the velocity in the y-plane by the players set speed
        #         self.player_sprite.change_y = PLAYER_JUMP_SPEED
        #
        #         # ALSO
        #         # Play the jump sound from the sound file saved in init
        #         arcade.play_sound(self.jump_sound)
        # # NO CONDITION FOR DOWN BECAUSE THE GRAVITY PHYSICS SHOULD TAKE CARE OF THAT
        # # If a user presses Left or A
        # elif key == arcade.key.LEFT or key == arcade.key.A:
        #     # change_x: https://arcade.academy/arcade.html?highlight=change_y#arcade.Sprite.change_x
        #     # Decreases the velocity in the x-plane by the players set speed
        #     self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        # # If a user presses Right or D
        # elif key == arcade.key.RIGHT or key == arcade.key.D:
        #     # Increases the velocity in the x-plane by the players set speed
        #     self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    # on_key_release: https://arcade.academy/arcade.html#arcade.View.on_key_release
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # # ---------------------- OLD KEY RELEASE CODE ----------------------
        # # This allows a user to press and hold a key because if you release the key, it will reset the velocity to 0
        # # If a user presses Left of A
        # if key == arcade.key.LEFT or key == arcade.key.A:
        #     # Reset velocity of x to zero
        #     self.player_sprite.change_x = 0
        # # If a user presses Right or D
        # elif key == arcade.key.RIGHT or key == arcade.key.D:
        #     # Reset velocity of x to zero
        #     self.player_sprite.change_x = 0

        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    # on_update: https://arcade.academy/arcade.html?highlight=on_update#arcade.Sprite.on_update
    def update(self, delta_time):
        """ Movement and game logic """

        # MY USER CONTROL UPDATES
        # Fix horizontal velocity to 0 (don't need vertical because gravity has an effect here)
        self.player_sprite.change_x = 0

        # The behavior/physics behind a player key stroke where they are trying to move their sprite
        # Specifically the Up movement
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        # Specifically the Left and Right movements
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Update the player_list after these movement changes happen
        self.player_list.update()

        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # Track if we need to change the viewport
        changed_viewport = False

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            # Reset the player to their start
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            # THIS WOULD BE A GREAT PLACE TO REMOVE HEALTH/PLAYER-LIFE ONCE THAT IS PUT INTO GAMEPLAY

            # Set the camera to the start (actually used in the code "if changed_viewport:")
            self.view_left = 0
            self.view_bottom = 0
            # This will force the condition below on the code "if changed_viewport:"
            changed_viewport = True
            # This will play the game-over sound clip (THIS SHOULD BE UPDATED FOR CONDITIONS - IF LIVES LEFT=RESTART NOISE, IF NO LIVES LEFT=GAMEOVER NOISE)
            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            # STOP THE PLAYER FROM MOVING
            # Reset players horizontal velocity to 0
            self.player_sprite.change_x = 0
            # Reset players vertical velocity to 0
            self.player_sprite.change_y = 0
            # RESET THE PLAYER SPRITE TO STARTING COORDINATES
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            # THIS WOULD BE A GREAT PLACE TO REMOVE HEALTH/PLAYER-LIFE ONCE THAT IS PUT INTO GAMEPLAY

            # Set the camera to the start (actually used in the code "if changed_viewport:")
            self.view_left = 0
            self.view_bottom = 0
            # This will force the condition below on the code "if changed_viewport:"
            changed_viewport = True
            # This will play the game-over sound clip
            arcade.play_sound(self.game_over)

        # See if the user got to the end of the level
        # THIS NEEDS AN UPDATE - PLAYER HAS TO GO TOOOOOOO CLOSE TO THE RIGHT SIDE OF THE MAP TO TRIGGER THE NEXT LEVEL
            # Create a basic level where the player simply runs to right side to debug this issue
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
                # Really it is increasing the self.level value by 1, which in turn updates the "file name" that the map is loading from
            self.level += 1

            # Load the next level
                # Because self.level was increased by 1, this can now load the next level because the map level names simple increase by 1 as well
            self.setup(self.level)

            # Set the camera to the start (actually used in the code "if changed_viewport:")
            self.view_left = 0
            self.view_bottom = 0
            # This will force the condition below on the code "if changed_viewport:"
            changed_viewport = True

        # ---------------------- Manage Scrolling ----------------------

        # Scroll left
        # STATIC_VIEWPORT_MARGINS are set at the very top
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        # If the player scrolls towards the left
        if self.player_sprite.left < left_boundary:
            # Set new view_left by subtracting the (left boundary and the sprites left coordinates)
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        # THIS IS TRIGGERED EVERY TIME THAT "changed_viewport" IS SET TO "True"
        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


# This function is outside the MyGame class so that it can call an instance of that class (think of this like a runner function)
def main():
    """ Main method """
    # Call an instance of the MyGame class and set it the variable "window"
    window = MyGame()
    # Call the .setup function on our instance of the MyGame class and pass it the level #
        # default sets .level to 1 and increments only when the "update" method runs this conditional "if self.player_sprite.center_x >= self.end_of_map:"
    window.setup(window.level)
    # The the app using the arcade library method .run
    arcade.run()


# Since python interpreters will first assign special variables (like __name__ will automatically be "__main__" unless hardcoded otherwise or dealing with imports)
# THIS CONDITIONAL says if __name__ is the main string (which is should be), then run the function main
# This is the "runner for the runner"
# This is a method for creating behavior within Python constructs/syntax
# Resources:
    # https://www.freecodecamp.org/news/if-name-main-python-example/
    # https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
    # https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    main()