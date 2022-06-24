import pygame


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key(key_name):
    ans = False

    # Отключаем показ всех событий, которые происходят в этой итерации
    for eye in pygame.event.get():
        # print(eye)
        pass

    # Получение булевых значений всех кнопок (нажат/нет)
    key_input = pygame.key.get_pressed()

    my_key = getattr(pygame, "K_{}".format(key_name))

    # Проверяем, является ли именно эта кнопка (key_name) нажатой
    if key_input[my_key]:
        ans = True

    pygame.display.update()
    return ans


def main():
    pass


# Проверка для запуска функции
if __name__ == '__main__':
    init()
    while True:
        main()
