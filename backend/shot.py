from backend.enums import Complexity

class Shot:
    def __init__ (self, shot_id, frames, complexity):
        self.id = shot_id
        self.frames = frames        # first frame is 1, last frame is frames
        self.complexity = complexity

    def set_complexity(self, complexity):
        self.complexity = complexity

    def __repr__(self):
            return f"Shot('{self.id}', {self.frames}, {self.complexity})"