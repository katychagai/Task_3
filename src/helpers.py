from faker import Faker

fake = Faker()

#Генерирует уникальные данные пользователя для регистрации
def generate_user_data():
  
    return {
        "name": fake.first_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }




