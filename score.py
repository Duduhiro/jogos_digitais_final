class Score:
    def __init__(self) -> None:
        self.score = 0
        self.streak = 0
        self.max_streak = 0

    def reset(self) -> None:
        self.score = 0
        self.streak = 0
        self.max_streak = 0

    def update_score(self, score: int) -> None:
        self.score += score
    
    def update_streak(self, streak_check: bool) -> None:
        if streak_check:
            self.streak += 1
        else:
            self.streak = 0
        self.max_streak = max(self.streak, self.max_streak)