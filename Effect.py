import pygame


class Effect:
    def __init__(self, x, y, images, size):
        self.images = images
        self.index = 0
        self.x = x
        self.y = y
        self.finished = False
        self.size = size

    def update(self):
        if self.index < len(self.images):
            self.index += 1
        else:
            self.finished = True

    def draw(self, surface):
        if self.index < len(self.images):
            surface.blit(self.images[self.index], (self.x - self.size[0] / 2, self.y - self.size[1] / 2))


class CapacitorCollisionEffect(Effect):
    def __init__(self, x, y):
        size = [142, 200]
        origin_images = [pygame.image.load(f"./capacitor_collision_effect/frame_{str(num).zfill(2)}_delay-0.1s.gif") for num in range(0, 16)]
        images = [pygame.transform.scale(origin_image, (size[0], size[1])) for origin_image in origin_images]
        super().__init__(x, y, images, size)


class RegisterCollisionEffect(Effect):
    def __init__(self, x, y):
        size = [50, 50]
        origin_images = [pygame.image.load(f"./register_collision_effect/frame_{str(num).zfill(1)}_delay-0.04s.gif") for num in range(0, 8)]
        images = [pygame.transform.scale(origin_image, (size[0], size[1])) for origin_image in origin_images]

        super().__init__(x, y, images, size)
