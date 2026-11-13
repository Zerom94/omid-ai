class Artist:
    def __init__(self, name, birth_year=None, death_year=None):
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year
        self.works = []

    def add_work(self, title, year):
        self.works.append({"title": title, "year": year})

    def __str__(self):
        years = ""
        if self.birth_year:
            years += str(self.birth_year)
        if self.death_year:
            years += f"-{self.death_year}"
        return f"{self.name} ({years})"
