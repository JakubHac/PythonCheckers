class Screen:
    def __init__(self):
        self.clickable = []
        self.blittable = []
        self.tickable = []

    def add_blittable(self, blittable):
        self.blittable.append(blittable)

    def remove_blittable(self, blittable):
        self.blittable.remove(blittable)

    def blit(self):
        for blittable in self.blittable:
            blittable.blit()

    def add_clickable(self, clickable):
        self.clickable.append(clickable)
        self.blittable.append(clickable)

    def remove_clickable(self, clickable):
        self.clickable.remove(clickable)
        self.blittable.remove(clickable)

    def handle_click(self, mouse_pos):
        for clickable in self.clickable:
            clickable.check_click(mouse_pos)

    def add_tickable(self, tickable):
        self.tickable.append(tickable)

    def remove_tickable(self, tickable):
        self.tickable.remove(tickable)

    def tick(self):
        for tickable in self.tickable:
            tickable.tick()