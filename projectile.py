import pygame
import math

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

# Set up the window
width = 700
height = 500
fps = 60
screen = pygame.display.set_mode((width, height))
screen.fill(BLACK)
clock = pygame.time.Clock()
pygame.display.set_caption("Projectile Motion Simulation")

# Create font object
font = pygame.font.Font(None, 24)

# Set the initial velocity of the projectile
v0 = 75.0
velocityText = font.render("Velocity: {} m/s".format(v0), True, WHITE)

# Set up the initial position of the projectile
x = 0
y = height

# Set the constant acceleration due to gravity
g = 9.81

# Set the time step and initial time
dt = 0.016666667 # chose this to be time realistic at 60 fps (0.1 / 60 = 0.166666666666...)
t = 0

# Initialize trajectory
trajectory = []

# Set flag for angle
angle_set = False

# Set flag for ground reached
ground_reached = False

# Run the simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for mouse click event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not angle_set:
                # Get the angle of projection from the mouse click
                theta = -math.atan2(event.pos[1] - y, event.pos[0] - x)
                vx = v0 * math.cos(theta)
                vy = v0 * math.sin(theta)

                # Calc data
                horizRange = (v0**2 * math.sin(2*theta)) / g
                maxHeight = (vy**2) / (2*g)
                flightTime = 2*(vy/g)

                # Update displayed infos
                angleText = font.render("Theta: {}°".format( round((theta*180)/math.pi, 2) ), True, WHITE)
                rangeText = font.render("Range: {} m".format( round(horizRange, 2) ), True, WHITE)
                heightText = font.render("Max height: {} m".format( round(maxHeight, 2) ), True, WHITE)
                timeText = font.render("Flight duration: {} s".format( round(flightTime, 2) ), True, WHITE)

                angle_set = True
                ground_reached = False
            else:
                x = 0
                y = height
                t = 0
                trajectory = []
                screen.fill(BLACK)
                angle_set = False
                ground_reached = True
                
    if angle_set and not ground_reached:
        # Clear the screen
        screen.fill(BLACK)
        # Update the position and velocity of the projectile
        x += vx * dt
        y -= (vy * dt + 0.5 * g * dt ** 2)
        vy -= g * dt
        t += dt
        # Check ground reached
        if (height - y <= 0):
            ground_reached = True
            y = height
            x = horizRange
            t = flightTime
        # Update dynamic infos
        currentHeightText = font.render("Current height: {} m".format( round(height - y, 2) ), True, WHITE)
        currentDistanceText = font.render("Horizontal distance travelled: {} m".format( round(x, 2) ), True, WHITE)
        timeElapsedText = font.render("Time elapsed: {} s".format( round(t, 2) ), True, WHITE)
        # Update trajectory list
        trajectory.append((x,y))
        # Draw trajectory
        if len(trajectory) > 1:
            for i in range(len(trajectory)-1):
                pygame.draw.line(screen, WHITE, trajectory[i], trajectory[i+1], 1)
        # Draw the projectile on the screen
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), 7)

        # Display throw infos
        screen.blit(velocityText, (30,20))
        screen.blit(angleText, (30,40))
        screen.blit(rangeText, (30, 60))
        screen.blit(heightText, (30, 80))
        screen.blit(timeText, (30, 100))
        screen.blit(currentHeightText, (30, 140))
        screen.blit(currentDistanceText, (30,160))
        screen.blit(timeElapsedText, (30,180))

    # Update the display
    clock.tick(fps)
    pygame.display.update()


# Close the window and exit
pygame.quit()