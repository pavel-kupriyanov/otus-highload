import asyncio
import random
import string

from social_network.db.managers import (
    AuthUserManager,
    FriendshipManager,
    HobbiesManager,
    UsersHobbyManager
)
from social_network.db.models import (
    AuthUser,
    Gender,
    Friendship,
    Hobby,
    UserHobby
)
from social_network.db.db import DatabaseConnector

from social_network.utils.security import hash_password
from social_network.settings import settings, Settings

USER_MALE_NAMES = (
    'Павел',
    'Иван',
    'Сергей',
    'Петр',
    'Василий',
    'Александр',
    'Алексей',
    'Дмитрий',
)

USER_FEMALE_NAMES = (
    'Елена',
    'Мария',
    'Виктория',
    'Евгения',
    'Александра',
    'Анастасия',
    'Наталья',
    'Алина'
)

USER_LAST_NAMES = (
    'Петров',
    'Иванов',
    'Сидоров',
    'Куприянов',
    'Алексеев',
    'Яблоков',
    'Помидоров',
    'Андреев',
    'Васильев',
)

CITIES = (
    'Москва',
    'Санкт-Петербург',
    'Нижний Новгород',
    'Екатеринбург',
    'Владивосток',
    'Сочи',
)

HOBBIES = (
    'Футбол',
    'Настольные игры',
    'Фехтование',
    'Волейбол',
    'Чтение',
    'Программирование',
    'Пение',
    'Танцы',
    'Путешествия',
    'Скалолазание',
    'Плавание',
    'Прокрастинация',
    'Варгеймы',
    'Компьютерные игры',
)


def random_str(n: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def generate_email() -> str:
    name, domain = random_str(10), random_str(4)
    return f'{name}@{domain}.com'


async def create_user(manager: AuthUserManager) -> AuthUser:
    gender = random.choice([Gender.MALE, Gender.FEMALE])
    names = USER_MALE_NAMES if gender == Gender.MALE else USER_FEMALE_NAMES
    first_name = random.choice(names)
    last_name = random.choice(USER_LAST_NAMES)
    if gender == Gender.FEMALE:
        last_name += 'a'
    age = random.randint(18, 60)
    city = random.choice(CITIES)
    hashed_password, salt = hash_password('secret_password')
    return await manager.create(email=generate_email(),
                                hashed_password=hashed_password,
                                salt=salt,
                                age=age,
                                first_name=first_name,
                                last_name=last_name,
                                city=city,
                                gender=gender)


async def create_friendship(manager: FriendshipManager, user1: AuthUser,
                            user2: AuthUser) -> Friendship:
    return await manager.create(user1.id, user2.id)


async def create_hobby(manager: HobbiesManager, name: str) -> Hobby:
    return await manager.create(name)


async def add_hobby_to_user(manager: UsersHobbyManager, user: AuthUser,
                            hobby: Hobby) -> UserHobby:
    return await manager.create(user.id, hobby.id)


async def fill_db(conf: Settings, count: 100, create_hobbies=True):
    connector = DatabaseConnector(conf.DATABASE)
    user_manager = AuthUserManager(connector, settings)
    friendship_manager = FriendshipManager(connector, settings)
    hobbies_manager = HobbiesManager(connector, settings)
    user_hobby_manager = UsersHobbyManager(connector, settings)
    users = []
    for i in range(1, count + 1):
        user = await create_user(user_manager)
        print(i, user)
        users.append(user)

    hobbies = []

    if create_hobbies:
        for hobby_name in HOBBIES:
            hobby = await create_hobby(hobbies_manager, hobby_name)
            print(hobby)
            hobbies.append(hobby)
    else:
        hobbies = await hobbies_manager.list()

    for user in users:
        # Users will have more that number_of_friends names because for each
        # user we try to create friendship
        number_of_friends = random.randint(0, 5)
        friends = random.choices(users, k=number_of_friends)
        for friend in friends:
            try:
                friendship = await create_friendship(friendship_manager, user,
                                                     friend)
                print(friendship)
            except Exception as e:
                print(repr(e))

        number_of_hobbies = random.randint(0, 5)
        user_hobbies = random.choices(hobbies, k=number_of_hobbies)
        for hobby in user_hobbies:
            try:
                u_hobby = await add_hobby_to_user(user_hobby_manager, user,
                                                  hobby)
                print(u_hobby)
            except Exception as e:
                print(repr(e))


def main(conf: Settings):
    asyncio.run(fill_db(conf, 100, create_hobbies=True))


if __name__ == '__main__':
    main(settings)
