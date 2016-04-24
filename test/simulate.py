from deco import concurrent
from multiprocessing import Pool

class Body(object):
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
    def update(self, fx, fy, dt):
        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
    def distanceSquared(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

def Simulate(body_list, dt, iterations):
    p = Pool(5)
    next_body_list = {}
    for i in body_list.keys():
        p.apply_async(SimulateBody, [body_list, next_body_list, i, iterations, dt],
            callback = lambda args: next_body_list.__setitem__(args[0], args[1]))
    p.close()
    p.join()
    body_list.update(next_body_list)

def SimulateBody(body_list, next_body_list, index, iterations, dt):
    simulated_body = body_list[index]
    for _ in range(iterations):
        fx = 0
        fy = 0
        for key in body_list.keys():
            if key == index: continue
            body = body_list[key]
            distanceSquared = body.distanceSquared(simulated_body)
            f = body.mass * simulated_body.mass / distanceSquared
            d = distanceSquared ** 0.5
            fx += (body.x - simulated_body.x) / d * f
            fy += (body.y - simulated_body.y) / d * f
        simulated_body.update(fx, fy, dt / iterations)
    return index, simulated_body
