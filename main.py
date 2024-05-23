import pygame
import button
import subprocess  
from dotenv import load_dotenv
import bubble_game as bubble_shooter
import connect_four as confour
import game_test as game_test
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

game_paused = False
menu_state = "main"

font = pygame.font.SysFont("arialblack", 40)

TEXT_COL = (255, 255, 255)

# Load button images
play_img = pygame.image.load("images/button_play_games.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
tutorials_img = pygame.image.load('images/button_tutorial.png').convert_alpha()
connect_device_img = pygame.image.load('images/button_connect_device.png').convert_alpha()
controls_img = pygame.image.load('images/button_controls.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()
bubble_shooter_img = pygame.image.load('images/button_bubble_shooter.png').convert_alpha()
connect_four_img = pygame.image.load('images/button_connect_four.png').convert_alpha()

# Calculate button positions
button_width = 200
button_height = 50
button_padding = 20
button_x = (SCREEN_WIDTH - button_width) // 2
button_start_y = SCREEN_HEIGHT // 3

# Create button instances
play_button = button.Button(button_x, button_start_y, play_img, 1)
options_button = button.Button(button_x, button_start_y + button_height + button_padding, options_img, 1)
quit_button = button.Button(button_x, button_start_y + 2 * (button_height + button_padding), quit_img, 1)
tutorials_button = button.Button(button_x, button_start_y, tutorials_img, 1)
connect_device_button = button.Button(button_x, button_start_y + button_height + button_padding, connect_device_img, 1)
controls_button = button.Button(button_x, button_start_y + 2 * (button_height + button_padding), controls_img, 1)
back_button = button.Button(button_x, button_start_y + 3* (button_height + button_padding), back_img, 1)

# Calculate button positions for Play Games submenu
play_submenu_button_start_y = button_start_y + 2 * (button_height + button_padding)
play_submenu_button_padding = 20
play_submenu_button_x = (SCREEN_WIDTH - button_width) // 2

bubble_shooter_button = button.Button(button_x, button_start_y+(button_height + button_padding), bubble_shooter_img, 1)
connect_four_button = button.Button(button_x, button_start_y +  2*(button_height + button_padding), connect_four_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# def start_video():
#     cap = cv2.VideoCapture("C:/Users/asus/Downloads/shotballloop.mp4")
#     video_width = 500
#     video_height = 500
#     video_screen = pygame.display.set_mode((video_width, video_height))
#     pygame.display.set_caption("Video Player")
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame = cv2.resize(frame, (video_width, video_height))  # Resize frame to match window size
#         frame = pygame.image.frombuffer(frame.tobytes(), (video_width, video_height), "RGB")
#         video_screen.blit(frame, (0, 0))
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     return  

def main_menu():
    global game_paused, menu_state

    running = True
    while running:
        screen.fill((52, 78, 91))

        if game_paused:
            if menu_state == "main":
                if play_button.draw(screen):
                    menu_state = "games"
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    running = False
            elif menu_state == "options":
                if tutorials_button.draw(screen):
                    print("Tutorials")
                if connect_device_button.draw(screen):
                    bci_app_path = "C:/Program Files/EmotivApps/EMOTIV Launcher.exe"
                    subprocess.Popen([bci_app_path])
                if controls_button.draw(screen):
                    print("Controls")
                if back_button.draw(screen):
                    menu_state = "main"
            elif menu_state == "games":
                if bubble_shooter_button.draw(screen):
                    bubble_shooter.bubble_start()
                if connect_four_button.draw(screen):
                    confour.start_game()
                if back_button.draw(screen):
                    menu_state = "main"
        else:
            draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        pygame.display.update()

main_menu()
