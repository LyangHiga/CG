#! /usr/bin/env python
# coding=utf-8

import numpy
from math import sqrt


class Delaunay:
    def __init__(self,center=(0,0),radius=99999):

        center = numpy.asarray(center)
        self.corners = [center+radius*numpy.array((-1, -1)),
                       center+radius*numpy.array((+1, -1)),
                       center+radius*numpy.array((+1, +1)),
                       center+radius*numpy.array((-1, +1))]

        self.triangles = {}
        self.circles = {}

        T1 = (0, 1, 3)
        T2 = (2, 3, 1)
        self.triangles[T1] = [T2, None, None]
        self.triangles[T2] = [T1, None, None]

        for t in self.triangles:
            self.circles[t] = self.circumference(t)

    def circumference(self, tri):
        pts = numpy.asarray([self.corners[v] for v in tri])
        pts2 = numpy.dot(pts, pts.T)
        A = numpy.bmat([[2 * pts2, [[1],
                                 [1],
                                 [1]]],
                      [[[1, 1, 1, 0]]]])

        b = numpy.hstack((numpy.sum(pts * pts, axis=1), [1]))
        x = numpy.linalg.solve(A, b)
        bar_corners = x[:-1]
        center = numpy.dot(bar_corners, pts)

        r = numpy.sum(numpy.square(pts[0] - center))  
        return (center, r)

    def inside(self, tri, p):
        center, r = self.circles[tri]
        return numpy.sum(numpy.square(center - p)) <= r

    def addPoint(self, point):
        p = [point.x,point.y]
        p = numpy.asarray(p)

        idx = len(self.corners)
        self.corners.append(p)

        bad_triangles = []
        for T in self.triangles:
            if self.inside(T, p):
                bad_triangles.append(T)

        bordo = []
        T = bad_triangles[0]
        edge = 0
        while True:
            tri_op = self.triangles[T][edge]
            if tri_op not in bad_triangles:
                bordo.append((T[(edge+1) % 3], T[(edge-1) % 3], tri_op))

                edge = (edge + 1) % 3
                if bordo[0][0] == bordo[-1][1]:
                    break
            else:
                edge = (self.triangles[tri_op].index(T) + 1) % 3
                T = tri_op

        for T in bad_triangles:
            del self.triangles[T]
            del self.circles[T]

        new_triangles = []
        for (a0, a1, tri_op) in bordo:
            T = (idx, a0, a1)
            self.circles[T] = self.circumference(T)
            self.triangles[T] = [tri_op, None, None]

            if tri_op:
                for i, neigh in enumerate(self.triangles[tri_op]):
                    if neigh:
                        if a1 in neigh and a0 in neigh:
                            self.triangles[tri_op][i] = T

            new_triangles.append(T)

        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            self.triangles[T][1] = new_triangles[(i+1) % N]   
            self.triangles[T][2] = new_triangles[(i-1) % N]   

    def tri(self):
        return [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]