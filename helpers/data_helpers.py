from faker import Faker

fake = Faker()


class DataHelper:

    @staticmethod
    def entity_setup_data():
        return {
            "addition": {
                "additional_info": fake.sentence(),
                "additional_number": fake.random_int(min=1, max=99)
            },
            "important_numbers": [
                fake.random_int(min=1, max=99),
                fake.random_int(min=1, max=99),
                fake.random_int(min=1, max=99)
            ],
            "title": fake.text(max_nb_chars=15),
            "verified": fake.boolean()
        }
