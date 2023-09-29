import pygame, sys
from button import Button
from SimpleLR import SimpleLR
from Polynomial import PolynomialRegression


ORIGIN = (30, 750)

def draw_axis():
    """Draw axis and origin point"""
    # Text
    root_surf = font.render('0', True, 'black')
    root_rect = root_surf.get_rect(center =(20, 760))
    y_label = font.render('Label', True, 'black')
    y_label_rect = y_label.get_rect(center =(70, 50))
    x_label  = font.render('Feature', True, 'black')
    x_label_rect = x_label.get_rect(center =(1040, 770))
    # Vertical axis
    pygame.draw.line(display_surf, 'black', (30, 50), (30, 750), 4)
    pygame.draw.line(display_surf, 'black', (20, 60), (30, 50), 4)
    pygame.draw.line(display_surf, 'black', (40, 60), (30, 50), 4)
    display_surf.blit(y_label, y_label_rect)
    # Horizontal axis
    pygame.draw.line(display_surf, 'black', (30, 750), (1000, 750), 4)
    pygame.draw.line(display_surf, 'black', (990, 740), (1000, 750), 4)
    pygame.draw.line(display_surf, 'black', (990, 760), (1000, 750), 4)
    display_surf.blit(x_label, x_label_rect)
    # Origin point
    display_surf.blit(root_surf, root_rect)

def convert_position(old_pos):
    """convert position from pygame coordinate system to cartesian coordinate system"""
    new_x = old_pos[0] - ORIGIN[0]
    new_y = ORIGIN[1] - old_pos[1]
    return (new_x, new_y)

def revert_position(old_pos):
    """revert position from cartesian coordinate system to pygame coordinate system"""
    new_x = old_pos[0] + ORIGIN[0]
    new_y = ORIGIN[1] - old_pos[1]
    return (new_x, new_y)

def marking_down():
    """for each data point, draw a label at that point"""
    for point in data_points:
        point_rect = label.get_rect(center = point)
        display_surf.blit(label, point_rect)

def drawing_record_table():
    """for each data point we have just choose, draw its coordinate in the record table"""
    # text
    data_text_surf = font.render('Data', True, 'black')
    data_text_rect = data_text_surf.get_rect(topleft =(1070, 50))
    x_text_surf = font.render('X', True, 'black')
    x_text_rect = x_text_surf.get_rect(topleft =(1055, 80))
    y_text_surf = font.render('Y', True, 'black')
    y_text_rect = y_text_surf.get_rect(topleft =(1055, 110))
    fofo_surf = font.render('', True, 'black')
    if data_points:
        x_point_surf = font.render(str(convert_position(data_points[-1])[0]), True, 'black')
        y_point_surf = font.render(str(convert_position(data_points[-1])[1]), True, 'black')
    else:
        x_point_surf = font.render('', True, 'black')
        y_point_surf = font.render('', True, 'black')
    x_point_rect = x_point_surf.get_rect(center =(1135, 91))
    fofo_rect_1 = fofo_surf.get_rect(center =(1135, 91))
    y_point_rect = y_point_surf.get_rect(center =(1135, 121))
    fofo_rect_2 = fofo_surf.get_rect(center =(1135, 121))
    # Draw the table
    pygame.draw.rect(display_surf, 'black', data_text_rect.inflate(100, 10), 2)
    pygame.draw.rect(display_surf, 'black', x_text_rect.inflate(70, 10), 2)
    pygame.draw.rect(display_surf, 'black', y_text_rect.inflate(70, 10), 2)
    pygame.draw.rect(display_surf, 'black', fofo_rect_1.inflate(65, 10), 2)
    pygame.draw.rect(display_surf, 'black', fofo_rect_2.inflate(65, 10), 2)
    # Display the text
    display_surf.blit(data_text_surf, data_text_rect)
    display_surf.blit(x_text_surf, x_text_rect)
    display_surf.blit(y_text_surf, y_text_rect)
    display_surf.blit(x_point_surf, x_point_rect)
    display_surf.blit(y_point_surf, y_point_rect)

def draw_option_box():
    """draw the option box"""
    box_rect = pygame.Rect(990, 20, 200, 460) 
    pygame.draw.rect(display_surf, 'black', box_rect, 3)   
   
def visualize_model(points):
    """draw the line or the curve that represent the model"""
    for i in range(len(points) - 1):
        pygame.draw.line(display_surf, 'deeppink', revert_position(points[i]), revert_position(points[i + 1]), 4)

def draw_mae(mae_value):
    """draw the MAE value of the current model"""
    mae_text_surf = font.render('MAE', True, 'black')
    mae_text_rect = mae_text_surf.get_rect(center =(900, 37))
    mae_value_surf = font.render(str(mae_value), True, 'black')
    mae_value_rect = mae_value_surf.get_rect(center =(900, 67))
    fofo_rect = font.render('', True, 'black').get_rect(center =(900, 67))
    # Draw
    pygame.draw.rect(display_surf, 'black', mae_text_rect.inflate(100, 10), 2)
    display_surf.blit(mae_text_surf, mae_text_rect)
    pygame.draw.rect(display_surf, 'black', fofo_rect.inflate(150, 10), 2)
    display_surf.blit(mae_value_surf, mae_value_rect)
    
# Basic setup
pygame.init()
display_surf = pygame.display.set_mode((1200, 800))
bg_surf = pygame.image.load('Assets/bg.jpg').convert_alpha()
pygame.display.set_caption('Visulizing Regression Models')
can_click = True
click_timer = None
# Fonts
font = pygame.font.Font(None, 32)

# Buttons
clear_button = Button('Clear', 140, 40, (1020, 170), 6, display_surf, font)
SLR_button = Button('SimpleLR', 140, 40, (1020, 230), 6, display_surf, font)
poly_button = Button('Polynomial', 140, 40, (1020, 290), 6, display_surf, font)
mae_button = Button('MAE', 140, 40, (1020, 350), 6, display_surf, font)
close_button = Button('Close', 140, 40, (1020, 410), 6, display_surf, font)
slr_check = False
poly_check = False
mae_check = False

# Data points
label = pygame.image.load('Assets/star.png')
data_points = []
converted_data_points = []

# sounds
mouse_click_sound = pygame.mixer.Sound('Assets/click.wav')
error_sound = pygame.mixer.Sound('Assets/error.mp3')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data_points = [convert_position(point) for point in data_points]
            pygame.quit()
            sys.exit()
    # Click timer and Restricting mouse position
    if not can_click:
        if pygame.time.get_ticks() - click_timer >= 200:
            can_click = True
    if pygame.mouse.get_pressed()[0] and can_click:
        click_timer = pygame.time.get_ticks()
        can_click = False
        if (990 >= pygame.mouse.get_pos()[0] >= 30) and (50 <= pygame.mouse.get_pos()[1] <= 750):
            mouse_click_sound.play()
            data_points.append(pygame.mouse.get_pos())
            click_timer = pygame.time.get_ticks()
        elif not (1190 >= pygame.mouse.get_pos()[0] >= 990 and 20 <= pygame.mouse.get_pos()[1] <= 480):
            error_sound.play()
    
    # Drawing
    display_surf.blit(bg_surf, (0, 0))
    draw_axis()
    marking_down()
    drawing_record_table()
    draw_option_box()
    
    # Active clear button
    clear_button.draw()
    if clear_button.pressed:
        mouse_click_sound.play()
        data_points = []
        converted_data_points = []
        slr_check = poly_check = mae_check = False
        
    # Active SLR button    
    SLR_button.draw()
    if SLR_button.pressed:
        mouse_click_sound.play()
        if data_points:
            converted_data_points = [convert_position(point) for point in data_points]
            slr = SimpleLR(converted_data_points)
            slr.train_model()
            slr_check = True
            poly_check = False
    if slr_check:
        visualize_model(slr.predict())
        
    # Active polynomial button
    poly_button.draw()
    if poly_button.pressed:
        mouse_click_sound.play()
        if data_points:
            converted_data_points = [convert_position(point) for point in data_points]
            poly_reg = PolynomialRegression(converted_data_points)
            poly_reg.train_model()
            poly_check = True
            slr_check = False
    if poly_check:
        visualize_model(poly_reg.predict())
        
    # Active Mae button
    mae_button.draw()
    if mae_button.pressed:
        mouse_click_sound.play()
        if slr_check or poly_check:
            mae_check = True
    if mae_check:
        mae_value = slr.mae() if slr_check else poly_reg.mae()
        draw_mae(mae_value)
        
    # Active close button
    close_button.draw()
    if close_button.pressed:
        mouse_click_sound.play()
        pygame.quit()
        sys.exit()
        
    # Update screen
    pygame.display.update()