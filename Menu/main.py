import pygame
import button
import subprocess  # Import the subprocess module to run external scripts

pygame.init()

# Create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Game variables
game_paused = False
menu_state = "main"

# Define fonts
font = pygame.font.SysFont("arialblack", 40)

# Define colours
TEXT_COL = (255, 255, 255)

# Load button images
play_img = pygame.image.load("C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_play_games.png").convert_alpha()
options_img = pygame.image.load("C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_quit.png").convert_alpha()
video_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_video.png').convert_alpha()
audio_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_keys.png').convert_alpha()
back_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_back.png').convert_alpha()
bubble_shooter_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_bubble_shooter.png').convert_alpha()
connect_four_img = pygame.image.load('C:/Users/asus/OneDrive/Desktop/pygame_tutorials-main/Menu/images/button_connect_four.png').convert_alpha()

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
video_button = button.Button(button_x, button_start_y, video_img, 1)
audio_button = button.Button(button_x, button_start_y + button_height + button_padding, audio_img, 1)
keys_button = button.Button(button_x, button_start_y + 2 * (button_height + button_padding), keys_img, 1)
back_button = button.Button(button_x, button_start_y + 3 * (button_height + button_padding), back_img, 1)

# Calculate button positions for Play Games submenu
play_submenu_button_start_y = button_start_y + 2 * (button_height + button_padding)
play_submenu_button_padding = 20
play_submenu_button_x = (SCREEN_WIDTH - button_width) // 2

bubble_shooter_button = button.Button(button_x, button_start_y + button_height + button_padding, bubble_shooter_img, 1)
connect_four_button = button.Button(button_x, button_start_y + 2 * (button_height + button_padding), connect_four_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def start_video():
    cap = cv2.VideoCapture("C:/Users/asus/Downloads/shotballloop.mp4")
    video_width = 500
    video_height = 500
    video_screen = pygame.display.set_mode((video_width, video_height))
    pygame.display.set_caption("Video Player")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (video_width, video_height))  # Resize frame to match window size
        frame = pygame.image.frombuffer(frame.tobytes(), (video_width, video_height), "RGB")
        video_screen.blit(frame, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit the function if ESC key is pressed

def main_menu():
    global game_paused, menu_state

    # Main menu loop
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
                if video_button.draw(screen):
                    print("Video Settings")
                if audio_button.draw(screen):
                    print("Audio Settings")
                if keys_button.draw(screen):
                    start_video()
                if back_button.draw(screen):
                    menu_state = "main"
            elif menu_state == "games":
                if bubble_shooter_button.draw(screen):
                    subprocess.Popen(["python", "C:/Users/asus/OneDrive/Desktop/EPOCH_API/MINOR_main/bubble_game.py"])
                if connect_four_button.draw(screen):
                    subprocess.Popen(["python", "C:/Users/asus/OneDrive/Desktop/EPOCH_API/MINOR_main/connect_four.py"])
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

# Start the main menu loop
main_menu()
