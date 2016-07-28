import math

class GravityGuy:

    time_step = None

    y = None

    v_y = None

    x = None

    v_x = None

    screen_center = None


    def accel(self,x,y):
        r = (((self.screen_center[0] - x) ** 2)+((self.screen_center[1] - y) ** 2)) ** .5

        G = 398574979046240

        if x > 0 and y > 0:
            return G/((r+6378100) ** 2)
        else:
            return G/(6378100)**2

    def orbit(self):

        a = self.accel(self.x,self.y)

        theta = math.atan(self.y/self.x)

        if self.x > self.screen_center[0]:
            a_x = a * math.cos(theta) * -1

        else:
            a_x = a * math.cos(theta)

        if self.y > self.screen_center[1]:
            a_y = a * math.cos(theta) * -1

        else:
            a_y = a * math.cos(theta)




        self.v_y = self.v_y + a_y * self.time_step

        self.y = self.time_step * ( self.v_y + a_y * self.time_step / 2 ) + self.y

        self.v_x = self.v_x + a_x * self.time_step

        self.x = self.time_step * ( self.v_x + a_x * self.time_step / 2 ) + self.x


        return self.x,self.y








