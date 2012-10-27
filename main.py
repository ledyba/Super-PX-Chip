# -*- coding: utf-8 -*-

import time
import numpy
import pygame
import copy
import math
from pygame.locals import QUIT, KEYDOWN,K_ESCAPE
from numpy.ma.core import cos, sin

class GL:
	def __init__(self):
		self.mat_ = numpy.eye(4)
		self.matStack_ = [];
	def frustumx(self, width, height, near, far):
		self.mat_ = numpy.matrix([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, float(far+near)/(far-near), 1.0*far*near/(far-near)],
		[0, 0, 1.0/near, 0]]);
	def trans_(self, point):
		np = numpy.dot(list(point)+[1], self.mat_.T)
		x,y,_,d = numpy.array(np)[0].tolist();
		return [x/d,y/d];
	def push(self):
		self.matStack_.append(copy.copy(self.mat_));
	def pop(self):
		self.mat_ = self.matStack_.pop();
	def trans(self, x,y,z):
		np = numpy.dot(self.mat_, [
			[1,0,0,x],
			[0,1,0,y],
			[0,0,1,z],
			[0,0,0,1],
			]);
		self.mat_ = np;
	def scale(self, x,y,z):
		np = numpy.dot(self.mat_, [
			[x,0,0,0],
			[0,y,0,0],
			[0,0,z,0],
			[0,0,0,1],
			]);
		self.mat_ = np;
	def rotate(self, angle, x, y, z):
		c = cos(angle)
		s = sin(angle)
		mat = numpy.matrix([
			[x**2*(1-c)+c,  x*y*(1-c)-z*s, x*z*(1-c)+y*s, 0],
			[y*x*(1-c)+z*s, y**2*(1-c)+c,  y*z*(1-c)-x*s, 0],
			[x*z*(1-c)-y*s, y*z*(1-c)+x*s, z**2*(1-c)+c,  0],
			[0,             0,            0,             1],
		]);
		self.mat_ = numpy.dot(self.mat_, mat);

SCREEN_SIZE=(640,480)
def main():
	# pygameの初期化
	pygame.init()
	
	# 画面を作る
	screen = pygame.display.set_mode( SCREEN_SIZE )
	
	# タイトルを設定
	pygame.display.set_caption('Super PX Chip')
	
	while True:
		screen.fill ((0, 0, 0))
		# 画面に文字を書く
		render(screen)
		# 画面を更新して、変更を反映する
		pygame.display.flip()
		time.sleep(1.0/60);
		# イベントチェック
		for event in pygame.event.get():
			# 終了ボタンが押された場合
			if event.type == QUIT:
				exit()
			# ESCキーが押された場合
			if (event.type == KEYDOWN and event.key  == K_ESCAPE):
				exit()

gl = GL()
gl.frustumx(640, 480, 300, 1800);
gl.trans(0,0, 300);
def render(surface):
	from pygame import draw
	pts = []
	gl.rotate(1.0/180*math.pi, 0.5 , 1 , 0.25);
	#for pt in [(-160,-120,0),(-160,120,0),(160,120,0),(160,-120,0)]:
	z = 0
	for pt in [(-160,-120,z),(-160,120,z),(160,120, z),(160,-120, z)]:
		tp = gl.trans_(pt);
		# 画面の中心に移動
		tp[0]+=320;
		tp[1]+=240;
		pts.append(tp);
	draw.polygon(surface, (255,255,255), pts)

main()
