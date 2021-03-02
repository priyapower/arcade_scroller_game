"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Priya's 2D Funhouse"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

PLAYER_MOVEMENT_SPEED = 3
GRAVITY =0.8
PLAYER_JUMP_SPEED = 13

LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# DECLARES AN OFFICIAL START COORDINATE (THIS IS FOR RESTARTING THE LEVEL)
PLAYER_START_X = 64
PLAYER_START_Y = 225


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.coin_list = None
        self.wall_list = None
        # NEW LIST FOR FOREGROUND LAYERS ON MAPS
        self.foreground_list = None
        # NEW LIST FOR BACKGROUND LAYERS ON MAPS
        self.background_list = None
        # NEW LIST FOR DONT TOUCH LAYERS ON MAPS
        self.dont_touch_list = None
        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        # MY USER CONTROL UPDATES
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        # WHERE IS THE RIGHT EDGE OF THE MAP?
        self.end_of_map = 0

        # THE LEVEL COUNTER
        self.level = 1

        self.collect_coin_sound = arcade.load_sound("../sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("../sounds/jump1.wav")
        # NEW SOUND LOADED FOR THE END OF THE GAME OR A PLAYER STARTING OVER
        self.game_over = arcade.load_sound("../sounds/gameover1.wav")

        # SINCE THE MAP NOW LOADS A BACKGROUND, WE NO LONGER NEED TO DECLARE A BACKGROUND COLOR THROUGH ARCADE

    # SETUP HAS A NEW PARAMETER OF LEVEL
    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.player_list = arcade.SpriteList()
        # NEW LIST - FOREGROUND
        self.foreground_list = arcade.SpriteList()
        # NEW LIST - BACKGROUND
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        image_source = "images/player_1/female_stand.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        # SET UP SPRITE WITH STATIC START - THIS HELPS WHEN THE PLAYER HAS TO RESTART LEVEL
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # --- Load in a map from the tiled editor ---
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'
        # NAME OF THE LAYER THAT HAS ITEMS FOR FOREGROUND
        foreground_layer_name = 'Foreground'
        # NAME OF THE LATER THAT HAS ITEMS FOR BACKGROUND
        background_layer_name = 'Background'
        # NAME OF THE LATER THAT HAS ITEMS WE SHOULD NOT TOUCH` touch
        dont_touch_layer_name = "Don't Touch"

        # DYNAMIC MAP NAME THAT WILL CYCLE THROUGH ALL MAPS BASED ON THE FILE NAMING
        map_name = f"tmx_map/funhouse_level_{level}.tmx"

        my_map = arcade.tilemap.read_tmx(map_name)

        # CALCULATE THE RIGHT EDGE OF THE VARIABLE "my_map" IN PIXELS
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Background
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name,
                                                            TILE_SCALING)

        # -- Foreground
        self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                            foreground_layer_name,
                                                            TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map,
                                                      coins_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        # --- Other stuff
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        self.wall_list.draw()
        # NEW DRAWING - BACKGROUND
        self.background_list.draw()
        # WHY DOES THE WALL LIST RENDER TWICE??
        self.wall_list.draw()
        self.coin_list.draw()
        # NEW DRAWING - DO NOT TOUCH
        self.dont_touch_list.draw()
        self.player_list.draw()
        # NEW DRAWING FOREGROUND
        self.foreground_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        # A FUN UPDATE WOULD BE TO ADD A LEVEL COUNTER HERE

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

    def update(self, delta_time):
        """ Movement and game logic """

        # MY USER CONTROL UPDATES
        self.player_sprite.change_x = 0

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        self.player_list.update()

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        # TRACK IF WE NEED TO CHANGE THE VIEWPORT
            # THIS VARIABLE USED TO JUST BE "changed"
        changed_viewport = False

        # DID THE PLAYER FALL OFF THE MAP?
        if self.player_sprite.center_y < -100:
            # SET THE PLAYER TO THEIR START COORDINATES
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # SET THE CAMERA TO THE START
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # DID THE PLAYER TOUCH SOMETHING THEY SHOULD NOT?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            # WHY ARE THESE 2 LINES OF CODE NECESSARY?
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            # SEND THE PLAYER BACK TO START COORDINATES
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # SET TEH CAMERA TO THE START
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # DID THE PLAYER GET TO THE END OF A LEVEL?
        if self.player_sprite.center_x >= self.end_of_map:
            # ADVANCE TO THE NEXT LEVEL (INCREASE LEVEL COUNTER BY ONE TO ACCESS NEXT MAP FILE PATH)
            self.level += 1

            # LOAD THE NEXT LEVEL
            self.setup(self.level)

            # SET THE CAMERA TO THE START
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # --- Manage Scrolling ---
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()