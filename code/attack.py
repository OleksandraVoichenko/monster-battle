from settings import *

class AttackAnimationSprite(pygame.sprite.Sprite):
    def __init__(self, target, frames, groups):
        super().__init__(groups)
        self.frames, self.frame_idx = frames, 0
        self.image = self.frames[self.frame_idx]
        self.rect = self.image.get_frect(center = target.rect.center)


    def update(self, dt):
        self.frame_idx += 5 * dt
        if self.frame_idx < len(self.frames):
            self.image = self.frames[self.frame_idx]
        else:
            self.kill()