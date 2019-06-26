import numpy as np
import math

class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.minx=0 #screen dimensions
        self.maxx=720 #screen dimensions
        self.miny=0 #screen dimensions
        self.maxy=534 #screen dimensions
        self.tolerance=5 #allowed distance from the edge
        
    def point_on_screen(self):
        if ((self.minx-self.tolerance <= self.x1 <= self.maxx+self.tolerance) and \
             (self.minx-self.tolerance <= self.x2 <= self.maxx+self.tolerance) and \
             (self.miny-self.tolerance <= self.y1 <= self.maxy+self.tolerance) and \
             (self.miny-self.tolerance <= self.y2 <= self.maxy+self.tolerance)):
             return True
        else:
             return False

    def find_line_equation(self):
        A = self.y1 - self.y2
        B = self.x2 - self.x1 
        C = A * self.x1 + B * self.y1 
        return_list = [A, B, C]
        return return_list
    

class CheckLeaf:
    def __init__(self, segA, segB):
        self.segA = segA
        self.segB = segB
        self.segclassA = Segment(segA[0],segA[1],segA[2],segA[3])
        self.segclassB = Segment(segB[0],segB[1],segB[2],segB[3])
        self.coefficients_a = self.segclassA.find_line_equation()
        self.coefficients_b = self.segclassB.find_line_equation()
        self.x1_a = segA[0]
        self.y1_a = segA[1]
        self.x2_a = segA[2]
        self.y2_a = segA[3]
        self.x1_b = segB[0]
        self.y1_b = segB[1]
        self.x2_b = segB[2]
        self.y2_b = segB[3]
        
    def on_screen(self):
        if self.segclassA.point_on_screen() and self.segclassB.point_on_screen():
            return True
        else:
            return False

    def find_the_intersection_point(self):
        coefficient_matrix = np.matrix([[self.coefficients_a[0], self.coefficients_a[1]], [self.coefficients_b[0], self.coefficients_b[1]]])
        RHS_matrix = np.matrix([[self.coefficients_a[2]], [self.coefficients_b[2]]])
        det = np.linalg.det(coefficient_matrix)
        if (det ** 2 > 0.00000001):
            # in this case, the segments intersect somewhere
            inverse_coefficient_matrix = coefficient_matrix.I
            solution = inverse_coefficient_matrix.dot(RHS_matrix)
            newsolution = [float(str(solution[0])[2:-2]),float(str(solution[1])[2:-2])]
            return newsolution
        else:
            # in this case, the lines are essentially parallel, so they will not intersect on screen, if at all.  I've put in a fake point which will fail a later llogic check.
            return ([-1000000, -1000000])

    def line_segments_intersect(self):
        det = np.linalg.det(np.matrix([[self.coefficients_a[0], self.coefficients_a[1]], [self.coefficients_b[0], self.coefficients_b[1]]]))
        if (det ** 2 > 0.0001):
            intersection_point = self.find_the_intersection_point()
            # find boundaries of the line segments.
            min_ax = int(min(self.x1_a, self.x2_a));
            max_ax = int(max(self.x1_a, self.x2_a))
            min_ay = int(min(self.y1_a, self.y2_a));
            max_ay = int(max(self.y1_a, self.y2_a))
            min_bx = int(min(self.x1_b, self.x2_b));
            max_bx = int(max(self.x1_b, self.x2_b))
            min_by = int(min(self.y1_b, self.y2_b));
            max_by = int(max(self.y1_b, self.y2_b))
            # If the intersection is within the boundaries
            # defined by the most extreme values of the coordinates then we can be assured that the
            # line segments actually do intersect. The following if statement returns the necessary
            # TRUE or FALSE that we want to see in order to move on.
            if ((min_ax <= intersection_point[0] <= max_ax) and \
                    (min_ay <= intersection_point[1] <= max_ay) and \
                    (min_bx <= intersection_point[0] <= max_bx) and \
                    (min_by <= intersection_point[1] <= max_by)):
                return True
            else:
                return False
        else:
            return False # a determinent of zero means the line segments are parallel.
        
    def calc_slopes(self):
        slope1 = (self.y1_a - self.y2_a) / (self.x1_a - self.x2_a) if (self.x1_a - self.x2_a) != 0 else 0.0
        slope2 = (self.y1_b - self.y2_b) / (self.x1_b - self.x2_b) if (self.x1_b - self.x2_b) != 0 else 0.0
        return slope1, slope2

    def calc_angle_between_segments(self):
            slope1, slope2 = self.calc_slopes()
            numerator = (slope2 - slope1)
            denominator = (1 + slope2 * slope1)
            if denominator == 0:
                return 90.0
            else:
                return ((math.atan(numerator / denominator) * 180 / math.pi))

    def calc_lengths_minor_major(self):
        """
        returns: 0 - major axis length, 1 - major axis coordinates, 2 - minor axis length, 3 - minor axis coordinates
        """
        length_axis1 = math.sqrt(abs(self.y1_a - self.y2_a) ** 2 + abs(self.x1_a - self.x2_a) ** 2)
        length_axis2 = math.sqrt(abs(self.y1_b - self.y2_b) ** 2 + abs(self.x1_b - self.x2_b) ** 2)
        if length_axis1 > length_axis2:
            return length_axis1, self.segA, length_axis2, self.segB
        else:
            return length_axis2, self.segB, length_axis1, self.segA

