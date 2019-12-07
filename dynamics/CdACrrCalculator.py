import matplotlib.pyplot as plt
from parserolldowndata import clean
import os.path
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, 'rolldowndata/test.csv')
data = clean(path)
x = data['time']
y = data['average_velocity']
CdAmin = 0
CdAmax = 1
Crrmin = 0.0015
Crrmax = 0.1
precision = 300


def generate_test_data(CdAmin=CdAmin, CdAmax=CdAmax, Crrmin=Crrmin,
                       Crrmax=Crrmax, vinit=y.iloc[0], time=x.tolist(),
                       precision=precision):
    m = 720  # kg
    g = 9.81  # m/s^2
    rho = 1.225  # kg/m^3
    combos = []
    for i in range(precision):
        CdA = CdAmin + (CdAmax - CdAmin) * i / precision
        combo = []
        for j in range(precision):
            Crr = Crrmin + (Crrmax - Crrmin) * j / precision
            v = []
            v.append(vinit)
            for t in range(1, len(x)):
                dt = time[t] - time[t - 1]
                next_v_half = (v[t - 1] - (((Crr * m * g)
                               + (CdA * rho * v[t - 1] ** 2 / 2))
                               * (dt / 2) / m))
                next_v = (v[t - 1] - (((Crr * m * g)
                          + (CdA * rho * next_v_half ** 2 / 2)) * dt / m))
                if next_v < 0:
                    next_v = 0
                v.append(next_v)
            combo.append(v)
        combos.append(combo)
    return combos


def diff(l1, l2):
    diff = 0
    for i in range(len(l1)):
        diff += (l1[i] - l2[i]) ** 2
    return diff


if __name__ == '__main__':
    velocities = y.tolist()
    plt.plot(x, y, '--bo')

    min_SSE = 100000000000000  # Arbitrarily large value
    datas = generate_test_data()
    for i in range(len(datas)):
        for j in range(len(datas[i])):
            SSE = diff(velocities, datas[i][j])
            if SSE < min_SSE:
                min_SSE = SSE
                a, b = i, j
    Crrmeas = Crrmin + (Crrmax - Crrmin) * b / precision
    CdAmeas = CdAmin + (CdAmax - CdAmin) * a / precision
    plt.plot(x, datas[a][b], '--co')
    plt.show()
    v = [y.iloc[0]]
    for t in range(1, len(x)):
        dt = x.tolist()[t] - x.tolist()[t-1]
        next_v_half = (v[t - 1] - ((Crrmeas * 660 * 9.81)
                       + (CdAmeas * 1.225 * (v[t - 1] ** 2)))
                       * ((dt/2) / 660))
        next_v = (v[t - 1] - ((Crrmeas * 660 * 9.81)
                  + (CdAmeas * 1.225 * (next_v_half ** 2))) * (dt / 660))
        v.append(next_v)
    print('The mesasured Crr is: ' + Crrmeas,
          'The measured CdA is : ' + CdAmeas)
