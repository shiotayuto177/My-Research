import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Particle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0.0
        self.dy = 0.0
        self.fitness = None
        self.p_best = None
        self.g_best = None

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_p_best(self):
        if self.p_best == None:
            self.p_best = {'x':self.x, 'y':self.y, 'fitness':self.fitness}
        elif self.p_best['fitness'] > self.fitness:
            self.p_best = {'x':self.x, 'y':self.y, 'fitness':self.fitness}

    def set_g_best(self, g_best):
        self.g_best = g_best

    def updatePosition(self):
        self.x += self.dx
        self.y += self.dy

    def updateVelocity(self, w=0.5, rho_max=0.14):
        rho1 = random.uniform(0, rho_max)
        rho2 = random.uniform(0, rho_max)
        self.dx = w * self.dx + rho1 * (self.p_best['x'] - self.x) + rho2 * (self.g_best['x'] - self.x)
        self.dy = w * self.dy + rho1 * (self.p_best['y'] - self.y) + rho2 * (self.g_best['y'] - self.y)

class Field:
    def __init__(self, N, x_min, x_max, y_min, y_max):
        self.N = N
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.g_best = None
        self.particleList = [Particle(random.uniform(self.x_min, self.x_max), random.uniform(self.y_min, self.y_max)) for i in range(self.N)]
        self.update_best()

    def fitness_func(self, x, y):
        z = x*x + y*y
        return z

    def __set_g_best(self):
        p_index = np.argmin([p.fitness for p in self.particleList])
        self.g_best = {'x':self.particleList[p_index].x,
                       'y':self.particleList[p_index].y,
                       'fitness':self.particleList[p_index].fitness}
    # g_best, p_best の更新
    def update_best(self):
        for particle in self.particleList:
            particle.set_fitness(self.fitness_func(particle.x, particle.y))
            particle.set_p_best()

        self.__set_g_best()
        for particle in self.particleList:
            particle.set_g_best(self.g_best)

    def move_particle(self):
        for particle in self.particleList:
            particle.updatePosition()
            particle.updateVelocity()


pso = Field(N=30,x_min=-5,x_max=5,y_min=-5,y_max=5)
T = 100
for t in range(T):
    pso.move_particle()
    pso.update_best()

# f-string: f 文字列は、変数や式を文字列内に直接埋め込んで表示する
#print(f"x:{pso.g_best['x']},y:{pso.g_best['y']},z:{pso.g_best['fitness']}")


class Animation_3D(Field):
    # コンストラクタ
    def __init__(self, N, x_min, x_max, y_min, y_max):
        super(Animation_3D, self).__init__(N, x_min, x_max, y_min, y_max)
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        xs = np.linspace(self.x_min, self.x_max, 100)
        ys = np.linspace(self.y_min, self.y_max, 100)
        X, Y = np.meshgrid(xs, ys)

        self.ax.plot_wireframe(X, Y, self.fitness_func(X, Y), color='b', rstride=2, cstride=2, linewidth=0.3)
        self.ims = []

    # スナップショット
    def snapshot(self):
        im = self.ax.scatter3D([p.x for p in self.particleList],
                               [p.ｙ for p in self.particleList],
                               [p.fitness for p in self.particleList],
                               c='r')
        self.ims.append([im])
        # 出力

    def output_animation(self):
        global ani  # jupyterでアニメーション表示のためにglobalが必要
        ani = animation.ArtistAnimation(self.fig, self.ims)
        ani.save('./anim_PSO_OOP.gif', writer='pillow')

pso = Animation_3D(N=30, x_min=-5, x_max=5, y_min=-5, y_max=5)  # オブジェクト生成
T = 30  # 制限時間(ループの回数)
for t in range(T):
    pso.move_particle()
    pso.update_best()
    pso.snapshot()
    pso.output_animation()
print(f"x:{pso.g_best['x']},y:{pso.g_best['y']},z:{pso.g_best['fitness']}")
