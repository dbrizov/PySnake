import pygame
from engine.time import Time
from engine.screen import Screen


class GameLoop():
    def __init__(self, fps=60):
        Time.set_fps(fps)
        self._background = pygame.Surface(Screen.get_size()).convert()
        self._background.fill((128, 128, 128))
        self._font = pygame.font.SysFont("mono", 20, bold=True)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            Time._tick()

            self.draw_text("FPS: {:.0f}     PLAYTIME: {:.2f} SECONDS".format(Time.get_fps(), Time.get_play_time()))
            pygame.display.flip()
            Screen.get_surface().blit(self._background, (0, 0))

        pygame.quit()

    def draw_text(self, text):
        fw, fh = self._font.size(text)
        surface = self._font.render(text, True, (0, 255, 0))
        Screen.get_surface().blit(surface, ((Screen.get_width() - fw) // 2, (Screen.get_height() - fh) // 2))
