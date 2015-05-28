#!/usr/bin/env python2.7

import math
import sys

from drawnow import drawnow
from pylab import plt
from random import shuffle, randint, random
from time import sleep

class Point:
	def __init__(self, x, y, name=""):
		self.x = x
		self.y = y
		self.name = name

	@classmethod
	def from_csv_line(cls, line):
		fields = line.strip().split(',')
		name = fields[0]
		x = float(fields[1])
		y = float(fields[2])
		return cls(x, y, name)


def reverse_sublist(lst, start, end):
    lst[start:end] = lst[start:end][::-1]
    return lst


def distance(this, that):
	dx = this.x - that.x
	dy = this.y - that.y
	return math.sqrt(dx * dx + dy * dy)


class Thermometer:
	INIT_TEMPERATURE = 0.1
	DELTA_TEMPERATURE = 0.0000001
	END_TEMPERATURE = 0.00001

	def __init__(self):
		self.temperature = Thermometer.INIT_TEMPERATURE

	def get_temperature(self):
		return self.temperature

	def iterate_temperature(self):
		self.temperature -= Thermometer.DELTA_TEMPERATURE
		return self.temperature >= Thermometer.END_TEMPERATURE


class Route(Thermometer):
	def __init__(self, filename):
		Thermometer.__init__(self)

		self.points = []
		for line in open(filename):
			self.points.append(Point.from_csv_line(line))

		# choosing initial state at random
		shuffle(self.points)

		# switching interactive plots on
		plt.ion()

	def draw(self):
		xx = [p.x for p in self.points]
		yy = [p.y for p in self.points]
		drawnow(lambda : Route.__draw_plot(xx, yy))

	@staticmethod
	def __draw_plot(xx, yy):
		plt.scatter(xx, yy)
		for i in range(0, len(xx)):
			plt.plot([xx[i - 1], xx[i]], [yy[i - 1], yy[i]], linestyle='-', color='r')


	def calc_energy(self):
		energy = 0.
		for i in range(0, len(self.points)):
			energy += distance(self.points[i - 1], self.points[i])
		return energy


	def simulate(self):
		if len(self.points) == 0:
			sys.stderr.write('Empty route. Exiting.\n')
		
		# choosing two random points
		first = 0
		second = 0
		while first == second:
			first = randint(0, len(self.points) - 1)
			second = randint(0, len(self.points) - 1)

		first = min(first, second)
		second = max(first, second)

		energy_old = self.calc_energy()
		reverse_sublist(self.points, first, second)
		energy_new = self.calc_energy()

		if energy_new > energy_old:
			delta_energy = energy_new - energy_old
			p = math.exp(-delta_energy / self.get_temperature())
			print self.get_temperature(), delta_energy
			if random() > p:
				print 'revert'
				reverse_sublist(self.points, first, second)

		# decrease the temperature
		return self.iterate_temperature()


def main():
	r = Route('data/libs.csv')
	r.draw()

	for i in range(10000000):
		if not r.simulate():
			break
		if i % 1000 == 0:
			r.draw()
		#sleep(0.001)

	raw_input("Press Enter to continue...")
	plt.show()

if __name__ == '__main__':
	main()
