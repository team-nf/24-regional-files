import cmath
import math


class AngleFinder:
    def __init__(self, h, l):
        # asansörün hareket noktasının yerden yüksekliği
        # h değişkeninden çıkarılarak denkleme katılabilir

        # Hedefin yerden yüksekliği
        self.h = h

        # bizim shooterın asansöre göre yüksekliği
        self.l = l

        # robotun hedefe olan uzaklığı
        self.d = None


    def set_distance(self, d):
        self.d = d


    def find_angle(self):
        if self.d is None: return None

        # Matematiği sormayın yordu
        a = complex(-self.d, self.h)
        b = complex(0, -2*self.l)
        c = complex(self.d, self.h)
        s1, s2 = self.discriminant(a, b, c)

        alpha1 = cmath.log(s1)/complex(0, 1)
        alpha2 = cmath.log(s2)/complex(0, 1)

        rv = []
        if 0 < alpha1.real < math.pi/2:
            rv.append(alpha1.real)
        if 0 < alpha2.real < math.pi/2:
            rv.append(alpha2.real)

        if len(rv) != 1:
            return None
        return rv[0]


    def discriminant(self, a, b, c):
        s1 = (-b + cmath.sqrt(b**2 - 4*a*c)) / (2*a)
        s2 = (-b - cmath.sqrt(b**2 - 4*a*c)) / (2*a)
        return s1, s2



def main():
    # parametrelerin anlamları classta yazıyor
    finder = AngleFinder(6, math.sqrt(2))


    finder.set_distance(3.8)
    print(f"angle at distance 3.8: {math.degrees(finder.find_angle())}")

    # This should print 45.0
    finder.set_distance(4)
    print(f"angle at distance 4: {math.degrees(finder.find_angle())}")

    finder.set_distance(4.2)
    print(f"angle at distance 4.2: {math.degrees(finder.find_angle())}")



if __name__ == "__main__":
    main()