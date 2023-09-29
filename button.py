import pygame, sys

class Button():
    """A class to make a button"""
    def __init__(self, text, width, height, pos, elevation, screen, gui_font):
        self.screen = screen
        
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (71, 95, 119)
        # bottom rectangle
        self.bot_rect = pygame.Rect(pos,(width, elevation))
        self.bot_color = '#354B5E'
        
        self.text_surf = gui_font.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def draw(self):
        # elevation's logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bot_rect.midtop = self.top_rect.midtop
        self.bot_rect.height = self.top_rect.height + self.dynamic_elevation
        
        pygame.draw.rect(self.screen, self.bot_color, self.bot_rect, border_radius= 5)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius= 5)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
           self.top_color = '#D74B4B'
           if pygame.mouse.get_pressed()[0]:
               self.dynamic_elevation = 0
               self.pressed = True
           else:
               self.dynamic_elevation = self.elevation
               if self.pressed:
                   self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = (71, 95, 119)
        
