import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from solar_array import SolarArray
global test
test = SolarArray(182, 30.28, 97.73, 8, 0.5)

def main():
    print("hello")
    test = SolarArray(182, 30.28, 97.73, 8, 0.5)
    print(test.totalEnergy())
    print("data")
    temp = test.data()
    total = 0
    for i in temp[1:]:
        total += float(i["Angle"])

    print("total of angles: " + str(total))

if __name__ == '__main__':
    main()

def test_totalEnergy():
    assert(test.totalEnergy() == 2822.6899241928577)

def test_data():
    temp = test.data()
    total = 0
    for i in temp[1:]:
        total += float(i["Angle"])
    assert(total == 2590.0493547179994)