import numpy
import os
import copy
import math
import lpp_tools as tools
from scipy.spatial import HalfspaceIntersection
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3

class Problem():
	def __init__(self, filename):
		self.c = []
		self.planes = []
		self.equations = 0
		self.dimesions = 0
		with open(filename) as f:
			counter = 0
			for line in f:
				if counter == 0:
					self.equations = int(line.split()[0])
					self.dimesions = int(line.split()[1])
				elif counter <= self.equations :
					self.planes.append([float(x) for x in line.split()])
				else:
					self.c = [float(x) for x in line.split()]
				counter += 1
		self.planes = numpy.array(self.planes)
		#self.planes[:,3] = -self.planes[:,3]
		self.c = numpy.array(self.c)
		self.c = self.c / numpy.linalg.norm(self.c)

	def belong(self, point):
			b = True
			for line in self.planes :
				#print(line[0:-1], line[-1])
				if numpy.dot(point, line[0:-1]) >= line[-1] : 
					b = False
			return b

	def distances(self, points):
		res = []
		for x in points:
			flag = False
			for line in self.planes:
				if numpy.dot(self.c, line[0:-1]) != 0:
					distance = (line[-1] - numpy.dot(x, line[0:-1]))/numpy.dot(self.c, line[0:-1])
					dot = x + self.c * distance
					if self.belong(dot - self.c * .0000001):
						res.append(distance)
						flag = True
			if not flag:
				res.append(math.inf)
		min_distance = min(res)
		for i in range(len(res)):
			if res[i] == math.inf:
				res[i] = min_distance
		return numpy.array(res)

	def projection(self, points):
		res = []
		for x in points:
#			flag = False
			for line in self.planes:
				if numpy.dot(self.c, line[0:-1]) != 0:
					distance = (line[-1] - numpy.dot(x, line[0:-1]))/numpy.dot(self.c, line[0:-1])
					dot = x + self.c * distance
					if self.belong(dot - self.c * .0000001):
						res.append(dot)
#						flag = True
#			if not flag:
#				res.append(x)
		return numpy.array(res)

	def vertices(self, n=0):
		if n < 7: n = len(self.planes)
		feasible_point = numpy.array([100., 100., 100.])
		halfspaces = copy.deepcopy(self.planes)
		halfspaces[:,3] = -halfspaces[:,3]
		hs = HalfspaceIntersection(halfspaces[:n], feasible_point)
		return numpy.array(hs.intersections)
		
	def facets(self, n=0):
		if n < 7: n = len(self.planes)
		out = []
		vertices = self.vertices(n)
		halfspaces = copy.deepcopy(self.planes)
		halfspaces[:,3] = -halfspaces[:,3]
		for plane in halfspaces[:n]:
			s = numpy.array([x for x in vertices if tools.point_in_hyperplane(x, plane)])
			if s.size == 0: continue
			out.append(tools.order_points(s))
		g = numpy.array(out, dtype=object)
		#return g
		return out
	
	def addFacetsToSubplot(self, ax):
		facets = self.facets()
		pc = a3.art3d.Poly3DCollection(facets, edgecolor="k", alpha=0.3)
		ax.add_collection3d(pc)
	
	def adjustSubplot(self, ax2):
		ax2.set_xlabel('x')
		ax2.set_xlim([0,200])
		ax2.set_ylabel('y')
		ax2.set_ylim([200,0])
		ax2.set_zlabel('z')
		ax2.set_zlim([0,200])
		
	def plot(self, filename=''):
        #facets = self.facets()
		plt.ioff()
		fig = plt.figure(figsize=(18,9))
		ax2 = fig.add_subplot(111, projection='3d')
        #colors = list(map("C{}".format, range(len(facets))))
        #pc = a3.art3d.Poly3DCollection(facets,  #facecolor=colors, 
        #                              edgecolor="k", alpha=0.5)
        #ax2.add_collection3d(pc)
		self.addFacetsToSubplot(ax2)
		self.adjustSubplot(ax2)
		ax2.axis('off')
		if not filename:
			plt.show()
		else:
			plt.savefig(filename)
			plt.close(fig)
    
	def savePlotSequence(self, folder):
		plt.ioff()
		for i in range(7, len(self.planes)+1):
			facets = self.facets(i)
			fig = plt.figure(figsize=(18,9))
			ax2 = fig.add_subplot(111, projection='3d')
			pc = a3.art3d.Poly3DCollection(facets, edgecolor="k", alpha=0.5)
			ax2.add_collection3d(pc)
			ax2.set_xlabel('x')
			ax2.set_xlim([0,200])
			ax2.set_ylabel('y')
			ax2.set_ylim([200,0])
			ax2.set_zlabel('z')
			ax2.set_zlim([0,200])
            
			filename = os.path.join(folder, str(i) + '.png')
			plt.savefig(filename)
			print('Saved to ' + filename)
			plt.close(fig)