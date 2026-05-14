from faker import Faker

class SeededDataGenerator:
    """
    Wrapper around Faker to ensure deterministic data generation.
    Always use this instead of raw Faker instances.
    """
    def __init__(self, seed: int):
        self.seed = seed
        self.faker = Faker()
        Faker.seed(seed)
        self.faker.seed_instance(seed)

    def email(self) -> str:
        return self.faker.email()

    def sha1(self) -> str:
        return self.faker.sha1()

    def random_int(self, min: int, max: int) -> int:
        return self.faker.random_int(min=min, max=max)

    def uuid4(self) -> str:
        # We generally avoid this, but if something absolutely needs a standard uuid format deterministically:
        return self.faker.uuid4()
