import matplotlib.pyplot as plt
import math
from abc import ABC, abstractmethod
from geometry.airfoil import Airfoil

 

class NACA4(Airfoil):
    """
    NACA airfoil 4 digit generator:

        NACAMPXX:
            - M is the maximum camber divided by 100. 
            - P is the position of the maximum camber divided by 10. 
            - XX is the thickness divided by 100. 

    The NACA airfoil section is created from a camber line and a thickness distribution plotted perpendicular to the camber line.
    Source: http://airfoiltools.com/airfoil/naca4digit
    """
    name: str

    #Airfoil Digits
    MPXX: str
    M: float
    P: float
    XX: float

    #Thickness distribution constants
    A_0 = 0.2969 
    A_1 = -0.126
    A_2 = -0.3516 
    A_3 = 0.2843
    A_4 = -0.1036 #closed trailing edge
    #A_4 = -0.1015 #open trailing edge

    def __init__(self, MPXX: str):
        self.MPXX = MPXX
        self.M = float(MPXX[0])/100
        self.P = float(MPXX[1])/10
        self.XX = float(MPXX[2:])/100
        self.name = f"naca{MPXX}"


    def __mean_camber_line_front(self, x: int):
        return (self.M/(self.P**2))*(2*self.P*x-x**2)
    
    def __mean_camber_line_back(self, x: int):
        return (self.M/((1-self.P)**2))*((1-2*self.P)+2*self.P*x-x**2)
    
    def mean_camber_line(self, x: int):
        if (0 <= x) and ( x <= self.P):
            return self.__mean_camber_line_front(x)
        elif (self.P < x) and (x <= 1):
            return self.__mean_camber_line_back(x)

    def __mean_camber_line_front_gradient(self, x):
        return ((2*self.M)/(self.P**2))*(self.P - x)
    
    def __mean_camber_line_back_gradient(self, x):
        return ((2*self.M)/((1-self.P)**2))*(self.P - x)
    
    def __mean_camber_gradient(self, x):
        if (0 <= x) and ( x <= self.P):
            return self.__mean_camber_line_front_gradient(x)
        return self.__mean_camber_line_back_gradient(x)
    
    def __omega(self, x):
        return math.atan(self.__mean_camber_gradient(x))
        
    def thickness_distribution(self, x: int):
        return (self.XX/0.2)*(self.A_0*x**(0.5) + self.A_1*x + self.A_2*x**2 + self.A_3*x**3 + self.A_4*x**4)

    def upper_surface_x(self, x):
        return x - self.thickness_distribution(x)*math.sin(self.__omega(x))

    def upper_surface_y(self, x):
        return self.mean_camber_line(x) + self.thickness_distribution(x)*math.cos(self.__omega(x))
    
    def lower_surface_x(self, x):
        return x + self.thickness_distribution(x)*math.sin(self.__omega(x))
    
    def lower_surface_y(self, x):
        return self.mean_camber_line(x) - self.thickness_distribution(x)*math.cos(self.__omega(x))
        
    def get_lin_dist_surface_points(self, number_points: int):
        upper_surface_points = list()
        lower_surface_points = list()
        airfoil_surface_points = list()

        upper_surface_points.append((0, 0, 0))

        for i in range(1, number_points):
            x = i/number_points
            p1 = (0, self.upper_surface_x(x), self.upper_surface_y(x))
            p2 = (0, self.lower_surface_x(x), self.lower_surface_y(x))

            upper_surface_points.append(p1)
            lower_surface_points.append(p2)

        upper_surface_points.append((0, 1, 0))
        lower_surface_points.append((0, 1, 0))
        upper_surface_points.reverse()

        airfoil_surface_points = upper_surface_points + lower_surface_points
        return airfoil_surface_points
    

class NACA5(Airfoil):
    """
    NACA 5 digit airfoil generator.

    NACA LPQXX:

        - L : design lift coefficient, design_cl = 0.15 * L
        - P : position of maximum camber * 20
        - Q : 0 = normal camber
              1 = reflex camber
        - XX: thickness in percent chord

    Examples:
        NACA23012
        NACA23112
        NACA24015

    Based on:
    http://airfoiltools.com/airfoil/naca5digit
    """

    name: str

    # Airfoil digits
    LPQXX: str

    L: int
    P: int
    Q: int
    XX: float

    design_cl: float
    camber_scale: float
    camber_pos: float

    REFERENCE_DESIGN_CL = 0.30

    # Thickness distribution constants
    A_0 = 0.2969
    A_1 = -0.1260
    A_2 = -0.3516
    A_3 = 0.2843
    A_4 = -0.1036  # closed TE
    # A_4 = -0.1015 # open TE

    # Standard 5-digit constants
    # Format:
    # position_digit : (m, k1)
    STANDARD_TABLE = {
        1: (0.0580, 361.4),
        2: (0.1260, 51.64),
        3: (0.2025, 15.957),
        4: (0.2900, 6.643),
        5: (0.3910, 3.230),
    }

    # Reflexed airfoil constants
    # position_digit : (m, k1, k2/k1)
    REFLEX_TABLE = {
        2: (0.1300, 51.990, 0.000764),
        3: (0.2170, 15.793, 0.00677),
        4: (0.3180, 6.520, 0.0303),
        5: (0.4410, 3.191, 0.1355),
    }

    def __init__(self, LPQXX: str):

        self.LPQXX = LPQXX

        self.L = int(LPQXX[0])
        self.P = int(LPQXX[1])
        self.Q = int(LPQXX[2])
        self.XX = float(LPQXX[3:]) / 100

        self.design_cl = self.L * 0.15
        self.camber_scale = self.design_cl / self.REFERENCE_DESIGN_CL
        self.camber_pos = self.P * 0.05

        self.name = f"naca{LPQXX}"

        # Load constants
        if self.Q == 0:
            self.m, base_k1 = self.STANDARD_TABLE[self.P]
        else:
            self.m, base_k1, self.k2k1 = self.REFLEX_TABLE[self.P]

        self.k1 = base_k1 * self.camber_scale


    def __mean_camber_standard_front(self, x):
        return ((self.k1 / 6)* (x**3 - 3 * self.m * x**2 + self.m**2 * (3 - self.m) * x))

    def __mean_camber_standard_back(self, x):
        return (self.k1 / 6) * self.m**3 * (1 - x)

    def __mean_camber_reflex_front(self, x):
        return (
            (self.k1 / 6)* ((x - self.m) ** 3- self.k2k1 * (1 - self.m) ** 3 * x- self.m**3 * x                + self.m**3
            )
        )

    def __mean_camber_reflex_back(self, x):
        return (
            (self.k1 / 6)
            * (
                self.k2k1 * (x - self.m) ** 3
                - self.k2k1 * (1 - self.m) ** 3 * x
                - self.m**3 * x
                + self.m**3
            )
        )

    def mean_camber_line(self, x):

        if self.Q == 0:
            if x < self.m:
                return self.__mean_camber_standard_front(x)
            return self.__mean_camber_standard_back(x)

        else:
            if x < self.m:
                return self.__mean_camber_reflex_front(x)
            return self.__mean_camber_reflex_back(x)


    def __mean_camber_gradient_standard_front(self, x):
        return (
            (self.k1 / 6)
            * (
                3 * x**2
                - 6 * self.m * x
                + self.m**2 * (3 - self.m)
            )
        )

    def __mean_camber_gradient_standard_back(self, x):
        return -(self.k1 / 6) * self.m**3

    def __mean_camber_gradient_reflex_front(self, x):
        return (
            (self.k1 / 6)
            * (
                3 * (x - self.m) ** 2
                - self.k2k1 * (1 - self.m) ** 3
                - self.m**3
            )
        )

    def __mean_camber_gradient_reflex_back(self, x):
        return (
            (self.k1 / 6)
            * (
                3 * self.k2k1 * (x - self.m) ** 2
                - self.k2k1 * (1 - self.m) ** 3
                - self.m**3
            )
        )

    def __mean_camber_gradient(self, x):

        if self.Q == 0:
            if x < self.m:
                return self.__mean_camber_gradient_standard_front(x)
            return self.__mean_camber_gradient_standard_back(x)

        else:
            if x < self.m:
                return self.__mean_camber_gradient_reflex_front(x)
            return self.__mean_camber_gradient_reflex_back(x)


    def __omega(self, x):
        return math.atan(self.__mean_camber_gradient(x))

    def thickness_distribution(self, x):
        return (
            (self.XX / 0.2)
            * (
                self.A_0 * math.sqrt(x)
                + self.A_1 * x
                + self.A_2 * x**2
                + self.A_3 * x**3
                + self.A_4 * x**4
            )
        )



    def upper_surface_x(self, x):
        return x - self.thickness_distribution(x) * math.sin(self.__omega(x))

    def upper_surface_y(self, x):
        return self.mean_camber_line(x) + (
            self.thickness_distribution(x) * math.cos(self.__omega(x))
        )

    def lower_surface_x(self, x):
        return x + self.thickness_distribution(x) * math.sin(self.__omega(x))

    def lower_surface_y(self, x):
        return self.mean_camber_line(x) - (
            self.thickness_distribution(x) * math.cos(self.__omega(x))
        )


    def get_lin_dist_surface_points(self, number_points: int):

        upper_surface_points = []
        lower_surface_points = []

        upper_surface_points.append((0, 0, 0))

        for i in range(1, number_points):

            x = i / number_points

            p1 = (0, self.upper_surface_x(x), self.upper_surface_y(x))

            p2 = (0, self.lower_surface_x(x), self.lower_surface_y(x))

            upper_surface_points.append(p1)
            lower_surface_points.append(p2)

        upper_surface_points.append((0, 1, 0))
        lower_surface_points.append((0, 1, 0))

        upper_surface_points.reverse()

        return upper_surface_points + lower_surface_points
