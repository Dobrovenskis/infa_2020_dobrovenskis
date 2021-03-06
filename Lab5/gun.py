from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 1
        self.vy = 1
        self.gravity = 0.5
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        """Перерисовывает ball
        """
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravity

        if self.x > 800:
            self.vx *= -1

        if self.y > 520 and self.vy < 0:
            self.vy *= -1
            self.vy *= 0.5
            self.vx *= 0.5

        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            return True
        else:
            return False

    def delete(self):
        canv.delete(self.id)


class rocket(ball):
    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()


class gun():
    def __init__(self):
        """ Конструктор класса gun
        """
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.y = 450
        self.id = canv.create_line(20, self.y, 50, self.y - 30, width=7)
        self.f2_powerForRocket = 6
        self.V = 0
        self.Vm = 5
        self.an = 0

    def fire2_start(self, event):
        """Начинает прицеливание.

        Происходит при нажатии правой кнопки мыши.
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball(y=self.y)
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def fire_rocket(self, event):
        """Выстрел ракетой.

        Происходит при нажатии левой кнопки мышки.
        Начальные значения компонент скорости ракеты vx и vy зависят от положения мыши.
        """
        global balls, rockets, bullet
        bullet += 1
        new_rocket = rocket(y=self.y)
        new_rocket.r += 2
        self.an = math.atan((event.y - new_rocket.y) / (event.x - new_rocket.x))
        new_rocket.vx = self.f2_powerForRocket * math.cos(self.an)
        new_rocket.vy = - self.f2_powerForRocket * math.sin(self.an)
        balls += [new_rocket]

    def targetting(self, event=0):
        """Прицеливание.  Зависит от положения мыши.
        """
        if event:
            self.an = math.atan((event.y - self.y) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

        self.set_coords()

    def power_up(self):
        """Увеличивает силу пушки.

        Происходит при f2_on = 1.
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1

    def move(self):
        """Функция отвечающая за движение пушки
        """
        self.y += self.V
        if self.y > 470 or self.y < 0:
            self.V *= -1
        self.set_coords()

    def set_speed(self, event):
        """Устанавливает скорость пушки в зависимости от нажатой кнопки

        Если нажата s, то пушка двигается вниз.
        Если нажата w, то пушка двигается вверх
        Если нажат пробел, то пушка не двигается
        """
        if str(event).split().count("char='s'") == 1:
            self.V = self.Vm
        elif str(event).split().count("char='w'") == 1:
            self.V = -self.Vm
        elif str(event).split().count("keysym=space") == 1:
            self.V = 0

    def set_coords(self):
        """Рисует пушку"""
        canv.coords(self.id, 20, self.y,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )


class target():
    def __init__(self, if_Big=False, x=0, y=0, r=0, vx=0, vy=0):
        """ Конструктор класса target
        Args:
            if_Big - если цели созданы из большой цели, то True
            x - координата x
            y - координата y
            r - радиус
            vx - скорость по x
            vy - скорость по y
        """
        self.live = 1
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.time = 0
        self.id = canv.create_oval(0, 0, 0, 0)
        if not (if_Big):
            self.new_target()
        else:
            canv.coords(self.id, x - r, y - r, x + r, y + r)
            canv.itemconfig(self.id, fill='red')

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)
        self.vx = 5 * 1 / 10 * rnd(-10, 10)
        self.vy = 5 * 1 / 10 * rnd(-10, 10)

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)

    def delete(self):
        canv.delete(self.id)

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Отскакивает от стен, движется равномерно.
        """
        self.x += self.vx
        self.y -= self.vy

        if self.x > 800:
            self.vx *= -1
        if self.x < 0:
            self.vx *= -1
        if self.y > 520 and self.vy < 0:
            self.vy *= -1
        if self.y < 0:
            self.vy *= -1
        self.set_coords()

    def reproduction(self):
        """Увеличивает время с начала создания
        """
        self.time += 1

    def create_bomb(self):
        """Создаёт бомбы каждые 40 единиц времени жизни.
        """
        global bombs
        if self.time % 40 == 0:
            new_bomb = bomb(x=self.x, y=self.y)
            bombs += [new_bomb]


class BigTarget(target):
    def __init__(self):
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.idm = []
        self.time = 0
        for i in range(5):
            self.idm.append(canv.create_oval(0, 0, 0, 0))
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        r = self.r = rnd(10, 100)
        self.r_small = r / (2 ** (1 / 2) + 1)
        color = self.color = 'red'
        self.set_coords()
        for i in range(5):
            canv.itemconfig(self.idm[i], fill=color)
        self.vx = 5 * 1 / 10 * rnd(-10, 10)
        self.vy = 5 * 1 / 10 * rnd(-10, 10)

    def set_coords(self):
        canv.coords(self.idm[0], self.x - 2 * self.r_small, self.y - 2 * self.r_small, self.x, self.y)
        canv.coords(self.idm[1], self.x, self.y - 2 * self.r_small, self.x + 2 * self.r_small, self.y)
        canv.coords(self.idm[2], self.x - 2 * self.r_small, self.y, self.x, self.y + 2 * self.r_small)
        canv.coords(self.idm[3], self.x, self.y, self.x + 2 * self.r_small, self.y + 2 * self.r_small)
        canv.coords(self.idm[4], self.x - self.r_small, self.y - self.r_small, self.x + self.r_small,
                    self.y + self.r_small)

    def delete(self, if_reproduction=False):
        """Удаление себя.

        Args:
            if_reproduction - если уничтожилась сама, то True
        """
        global points
        if not (if_reproduction):
            points += 4
        for i in range(5):
            canv.delete(self.idm[i])
        canv.delete(self.id)

    def reproduction(self):
        """На месте большой цели создаёт 5 маленьких.
        """
        global targets
        self.time += 1
        if self.time > 100:
            for i in range(5):
                vx1 = 5 * 1 / 10 * rnd(-10, 10)
                vy1 = 5 * 1 / 10 * rnd(-10, 10)
                t = target(if_Big=True, x=self.x, y=self.y, r=self.r_small, vx=vx1, vy=vy1)
                targets.insert(0, t)
            self.delete(if_reproduction=True)
            targets.remove(self)


class bomb():
    def __init__(self, x, y):
        """Конструктор класса bomb.

        Args:
            x, y - началное местоположение
        """
        self.x = x
        self.y = y
        self.V = 10
        self.r = 10
        self.color = 'black'
        self.id = canv.create_oval(0, 0, 0, 0)
        self.set_coords()
        canv.itemconfig(self.id, fill='black')

    def move(self):
        self.x -= self.V
        self.set_coords()

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def hit_tank(self, tank):
        """Попадание по пушке

        Args:
            tank: пушка с которой проверяется соударение
        """
        global count_popal
        if 20 < self.x < 30 and tank.y - self.r - 7 < self.y < tank.y + self.r:
            print('попали')
            count_popal += 1

    def delete(self):
        canv.delete(self.id)


screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []
rockets = []
targets = []
bombs = []
points = 0
count_popal = 0
okno_pointof = canv.create_text(30, 30, text=points, font='28')


def new_game(number_of_target, number_of_Bigtarget):
    """Создаёт новую игру.
    """
    global gun, targets, screen1, balls, bullet, points, okno_pointof, bombs, count_popal
    bombs = []
    bullet = 0
    balls = []
    targets = []
    count_popal = 0
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    canv.bind('<Button-3>', g1.fire_rocket)
    canv.bind_all('w', g1.set_speed)
    canv.bind_all('<s>', g1.set_speed)
    canv.bind_all('<space>', g1.set_speed)

    for i in range(number_of_target):
        targets.append(target())
    for i in range(number_of_Bigtarget):
        targets.append(BigTarget())
    for t in targets:
        t.live = 1

    while targets or balls:
        g1.move()
        for t in targets:
            t.move()
            t.reproduction()
            t.create_bomb()
        for bom in bombs:
            bom.move()
        for b in balls:
            b.move()

            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
                    t.delete()
                    targets.remove(t)
                    points += 1
                    canv.itemconfig(okno_pointof, text=points)

        for b in bombs:
            b.hit_tank(tank=g1)

        if not (targets):
            canv.bind('<Button-1>', '')
            canv.bind('<ButtonRelease-1>', '')
            if count_popal == 0:
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
            else:
                canv.itemconfig(screen1, text='Вас подбили ' + str(count_popal) + \
                                              ' раза \n' + 'Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
            for k in balls:
                k.delete()
            for k in bombs:
                k.delete()
            balls = []
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()

    time.sleep(2.03)
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game(number_of_target, number_of_Bigtarget))


number_of_target = 2
number_of_Bigtarget = 2
new_game(number_of_target, number_of_Bigtarget)

tk.mainloop()
