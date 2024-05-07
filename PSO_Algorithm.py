import numpy as np
import random

#評価関数
def evaluate(particle):
    z = 0
    for i in range(len(particle)):
        z += particle[i] ** 2
    return z

def update_position(particle, velocity):
    new_particle = particle + velocity
    return new_particle

def update_velocity(particle, velocity, pbest, gbest, w=0.5, max=0.15):
    new_velocity = np.array([0.0 for i in range(len(particle))])
    # 乱数を生成（重み付け）
    r1 = random.uniform(0, max)
    r2 = random.uniform(0, max)
    for i in range(len(particle)):
        new_velocity[i] = (w * float(velocity[i]) + r1 * (float(pbest[i]) - float(particle[i])) + r2 * (float(gbest[0]) - float(particle[i])))

    return new_velocity

def main():
    N = 100 #粒子の数
    length = 2 #次元数
    para_max = 100 #パラメータ（座標）の最大数
    # 粒子位置の初期化　今回はpsは二次元
    ps = [[random.uniform(-para_max, para_max) for j in range(length)] for i in range(N)]
    # 粒子速度の初期化　今回はpsは二次元
    vs = [[0.0 for j in range(length)] for i in range(N)]
    #パーソナルベストを保持（最初の）
    personal_best_position = ps
    #パーソナルベストの評価（最初の）
    personal_best_scores = [evaluate(p) for p in ps]
    #評価値最小の粒子のインデックスを保持
    best_particle = np.argmin(personal_best_scores)
    #グローバルベストを取得
    global_best_position = personal_best_position[best_particle]

    generation = 30 #イテレーション数
    for t in range(generation):
        #イテレーションごとにdata / pso / pso(t+1).txtに書き込む
        file = open("data/pso/pso" + str(t+1) + "txt", "w")
        for n in range(N):
            #ファイルに書き込み
            file.write(str(ps[n][0])+ " " + str(ps[n][1]) + "\n")
            # 多次元の時のファイル書き込み　file.write(" ".join(map(str, ps[n])) + "\n")
            #粒子の速度の更新
            vs[n] = update_velocity(ps[n], vs[n], personal_best_position[n], global_best_position)
            #粒子の位置の更新
            ps[n] = update_position(ps[n], vs[n])

            score = evaluate(ps[n])
            if score < personal_best_scores[n]:
                personal_best_scores[n] = score
                personal_best_position[n] = ps[n]
        # 評価値最小の粒子のインデックスを保持
        best_particle = np.argmin(personal_best_scores)
        # グローバルベストを取得
        global_best_position = personal_best_position[best_particle]
        file.close()

    print(global_best_position)
    print(min(personal_best_scores))

if __name__ == '__main__':
    main()
