import math

class Segment():

    def __init__(self, points, startIndex, endIndex, multiplier=None):
        self.points = points
        self.slope = 0
        self.intercept = 0
        self.startIndex = startIndex
        self.endIndex = endIndex - 1
        self.turning_points = [0, self.endIndex]
        self.threshold = 0
        self.multiplier = multiplier
        self.threshold = self.get_threshold()
        
    def get_threshold(self):
        points_sum = 0
        for ycoord in self.points:
          points_sum += ycoord
        points_avg = points_sum / len(self.points)
        diffs = []
        for ycoord in self.points:
          diffs.append(math.pow(ycoord - points_avg, 2))
        variance = sum(diffs) / (len(diffs)-1)
        stdev = math.sqrt(variance)
        print ('thresh: ', stdev * self.multiplier )
        return stdev * self.multiplier 

    def get_max(self):
        max_found = False
        delta = 0
        max_delta = 0
        for seg in range(0, len(self.turning_points) - 1):
            print(self.turning_points)
            print('len: ', len(self.points))
            self.startIndex = self.turning_points[seg]
            self.endIndex = self.turning_points[seg + 1]
            x2 = self.endIndex
            x1 = self.startIndex
            y2 = self.points[x2]
            y1 = self.points[x1]
            print('start: ', x1, 'val: ', y1)
            print('end: ', x2, 'val: ', y2)
            length = x2 - x1
            self.slope = (y2 - y1) / (length)
            self.intercept = -1 * ((self.slope * x1) - y1)
            for i in range(self.startIndex, self.endIndex):
                x_coord = i
                y_coord = self.points[i]
                point_error = self.slope * x_coord + self.intercept
                d = math.pow(point_error - y_coord, 2)
                print('error: ', d)
                if d > delta:
                    max_x = x_coord
                    max_delta = d
                    print('delta: ', max_delta, 'x: ', max_x)
                    delta = d
        if (max_delta) > self.threshold:
            self.turning_points.append(max_x)
            self.turning_points = sorted(self.turning_points)
            max_found = True
        else:
            max_found = False
        return sorted(self.turning_points), max_found
    
    def get_turning_points(self):
        max_found = True
        tp = self.turning_points
        while max_found == True:
            print('start: ', self.startIndex)
            print('end: ', self.endIndex)
            print('points: ', self.turning_points)
            tp, max_found = self.get_max()
        return sorted(tp)
        