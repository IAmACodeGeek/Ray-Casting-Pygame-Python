# Import modules
import pygame
import sys
from settings import *

# Initialize pygame
pygame.init()

# Create a display surface or window
DISP_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Create a window title
pygame.display.set_caption("LEARN RAY CASTING")

# Create the timer
clock = pygame.time.Clock()

def draw_map():
    
    # Fill the background of the map alone
    pygame.draw.rect(DISP_SURF, BLACK, (0, 0, WINDOW_WIDTH / 2, WINDOW_HEIGHT))

    # Iterate through each row
    for row in range(MAP_DIMENSION[0]):
        # Iterate through each column
        for col in range(MAP_DIMENSION[1]):
            # Color of the tile depending upon wall or empty space
            tile_color = GREY if MAP_LAYOUT[row][col] == 1 else (100, 100, 100)

            # Coordinates of the tiles to be drawn on the map
            tile_x, tile_y = col * MAP_TILE_HEIGHT, row * MAP_TILE_WIDTH

            # Drawing the tiles
            pygame.draw.rect(DISP_SURF, tile_color, (tile_x + 1, tile_y + 1, MAP_TILE_WIDTH - 2, MAP_TILE_HEIGHT - 2), 0)

def cast_rays():

    # List to store the tiles which are touched by the rays
    touched_wall_tiles = []
    # Cast each ray
    for nth_ray in range(NO_OF_RAYS):
        # Direction of each ray in angle
        ray_angle = player_angle + PLAYER_HALF_FOV - nth_ray * STEP_ANGLE

        # Increment the length of each ray by a pixel until the ray touches a wall at which point the ray stops growing further and return which wall they touch
        for ray_length in range(1, MAX_RAY_LENGTH//RAY_STEP):
            
            ray_length *= RAY_STEP

            # Coordinates of the end point of the ray 
            target_x = player_x + math.cos(ray_angle) * ray_length
            target_y = player_y - math.sin(ray_angle) * ray_length

            # The tile which the ray touches
            ray_col = int(target_x / MAP_TILE_WIDTH)
            ray_row = int(target_y / MAP_TILE_HEIGHT)

            # If the tile touched by the ray is a wall
            if MAP_LAYOUT[ray_row][ray_col] == 1:
                # If the tile is not already recognised as a wall by the previous rays
                if (ray_row, ray_col) not in touched_wall_tiles:
                    # Add the tile to the list of walls
                    touched_wall_tiles.append((ray_row, ray_col))
                
                # The following code is an optimisation to reduce the number of for loops 
                # while finding the ray_length at which the wall is found since we are incrementing the ray length by 30 for every iterartion, 
                # we will not know what the exact pixel distance at which the wall is from the player. 
                # hence when a wall is found, we decrement 30 from the ray_length and run a for loop by incrementing for each pixel distance to find the exact distance 
                # and not a approximation in steps of 30
                ray_length -= RAY_STEP
                for i in range(RAY_STEP):
                    ray_length += 1
                    target_x = player_x + math.cos(ray_angle) * ray_length
                    target_y = player_y - math.sin(ray_angle) * ray_length
                    ray_col = int(target_x / MAP_TILE_WIDTH)
                    ray_row = int(target_y / MAP_TILE_HEIGHT)
                    if MAP_LAYOUT[ray_row][ray_col] == 1:
                        break
            
                # Color of the wall depending upon distance
                color = 255 / (ray_length ** 0.75 * 0.1 + 0.0001)

                color = color if color <= 150 else 150
                
                # Fix the fish eye effect which is the round appearance of the walls
                ray_length = ray_length * math.cos(player_angle - ray_angle)

                # Set the apparent height of the wall in 3d display
                apparent_height = WALL_HEIGHT / (ray_length + 0.0001) # 0.0001 just to prevent zero error in case the ray length is zero
                
                apparent_height = WINDOW_HEIGHT if apparent_height > WINDOW_HEIGHT else apparent_height

                # Draw the rays on 2d map
                
                pygame.draw.line(DISP_SURF, YELLOW, (player_x, player_y), (target_x, target_y), 1)
                # Display the wall on the 3d display
                pygame.draw.rect(DISP_SURF, (color, color, color), ((WINDOW_WIDTH / 2 + nth_ray * RAY_DISP_WIDTH), (WINDOW_HEIGHT / 2 - apparent_height / 2), RAY_DISP_WIDTH, apparent_height), 0)
                break
    
    for tile in touched_wall_tiles:
        tile_x, tile_y = tile[1] * MAP_TILE_HEIGHT, tile[0] * MAP_TILE_WIDTH

        # Drawing the tiles
        pygame.draw.rect(DISP_SURF, GREEN, (tile_x + 1, tile_y + 1, MAP_TILE_WIDTH - 2, MAP_TILE_HEIGHT - 2), 0)
    
    # Draw the line which shows the direction of the player
    pygame.draw.line(DISP_SURF, BLACK, (player_x, player_y), (player_x + math.cos(player_angle) * DIR_RAY_LENGTH, player_y - math.sin(player_angle) * DIR_RAY_LENGTH), 2)

def movement():
        global player_x, player_y, player_angle

        # Get input from user through the keyboard
        keys = pygame.key.get_pressed()

        # Turn left
        if keys[ord("a")]:
            player_angle += ROTATION_SPEED
        
        # Turn right
        if keys[ord("d")]:
            player_angle -= ROTATION_SPEED

        vertical_move = False
        # Move forward
        if keys[pygame.K_UP]:
            forward = True
            vertical_move = True
            player_x = player_x + math.cos(player_angle) * PLAYER_SPEED
            player_y = player_y - math.sin(player_angle) * PLAYER_SPEED

        # Move backward
        if keys[pygame.K_DOWN]:
            forward = False
            vertical_move = True
            player_x = player_x - math.cos(player_angle) * PLAYER_SPEED
            player_y = player_y + math.sin(player_angle) * PLAYER_SPEED
        
        horizontal_move = False
        # Move left
        if keys[pygame.K_LEFT]:
            right = False
            horizontal_move = True
            player_x = player_x - math.sin(player_angle) * PLAYER_SPEED
            player_y = player_y - math.cos(player_angle) * PLAYER_SPEED
        
        # Move right
        if keys[pygame.K_RIGHT]:
            right = True
            horizontal_move = True
            player_x = player_x + math.sin(player_angle) * PLAYER_SPEED
            player_y = player_y + math.cos(player_angle) * PLAYER_SPEED

        # Tp find what tile the player is in
        player_row = int(player_y / MAP_TILE_HEIGHT)
        player_col = int(player_x / MAP_TILE_WIDTH)

        # To neutralize the movement when the player hits a wall
        if MAP_LAYOUT[player_row][player_col] == 1:
            if (vertical_move and forward):
                player_x = player_x - math.cos(player_angle) * PLAYER_SPEED
                player_y = player_y + math.sin(player_angle) * PLAYER_SPEED
            
            elif(vertical_move and not forward):
                player_x = player_x + math.cos(player_angle) * PLAYER_SPEED
                player_y = player_y - math.sin(player_angle) * PLAYER_SPEED
            
            if (horizontal_move and right):
                player_x = player_x - math.sin(player_angle) * PLAYER_SPEED
                player_y = player_y - math.cos(player_angle) * PLAYER_SPEED
            
            elif (horizontal_move and not right):
                player_x = player_x + math.sin(player_angle) * PLAYER_SPEED
                player_y = player_y + math.cos(player_angle) * PLAYER_SPEED

def main():
    
    # Game loop
    while True:
        
        # Handle the pygame events for input commands
        for event in pygame.event.get():
            # Close button pressed or quit condition
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Draw the map
        draw_map()

        # Update the background for the 3d display for the ceiling and the ground
        pygame.draw.rect(DISP_SURF, GREY, (WINDOW_WIDTH / 2, 0, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 0)
        pygame.draw.rect(DISP_SURF, (100, 100, 100), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT), 0)

        # To cast the rays on the 2d map
        cast_rays()

        # Draw the player on map
        pygame.draw.circle(DISP_SURF, RED, (player_x, player_y), PLAYER_RADIUS)

        # Update the display
        pygame.display.update()

        # Slow down the game
        clock.tick(FPS)

if __name__ == "__main__":
    main()