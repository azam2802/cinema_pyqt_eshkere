from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtGui import QColor, QPen, QRadialGradient, QBrush
from PyQt5.QtCore import Qt, QTimer
import random

class SnowflakeItem(QGraphicsEllipseItem):
    def __init__(self, scene_width, scene_height):
        size = random.uniform(1, 4)
        super().__init__(0, 0, size, size)
        
        self.start_x = random.uniform(0, scene_width)
        self.setPos(self.start_x, -100)
        
        self.fall_speed = random.uniform(100, 300)
        
        self.drift = random.uniform(-20, 20)
        
        self.is_glowing = random.random() < 0.1 
        
        if self.is_glowing:
            self.setBrush(QColor(255, 255, 255, 250))  
            self.glowing_pen = QPen(QColor(255, 255, 255, 250), 2.5)  
            self.setPen(self.glowing_pen)
            
            gradient = QRadialGradient(size/2, size/2, size/2)
            gradient.setColorAt(0, QColor(255, 255, 255, 255))  
            gradient.setColorAt(1, QColor(255, 255, 255, 50))  
            self.setBrush(QBrush(gradient))
        else:
            self.setBrush(QColor(255, 255, 255, 200))  
            self.setPen(QPen(Qt.NoPen)) 

class SnowfallBackground(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFrameShape(QGraphicsView.NoFrame)
        
        self.snowflakes = []
        self.num_snowflakes = 150
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_snowflakes)
        self.animation_timer.start(10)
        
        if hasattr(self.parent(), 'resizeEvent'):
            self.original_resize_event = self.parent().resizeEvent
            self.parent().resizeEvent = self.on_resize
        else:
            self.parent().resizeEvent = self.on_resize

    def on_resize(self, event):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.scene.setSceneRect(0, 0, self.parent().width(), self.parent().height())
        
        self.create_snowflakes()
        
        if hasattr(self, 'original_resize_event'):
            self.original_resize_event(event)

    def create_snowflakes(self):
        for flake in self.snowflakes:
            self.scene.removeItem(flake)
        self.snowflakes.clear()
        
        for _ in range(self.num_snowflakes):
            snowflake = SnowflakeItem(self.width(), self.height())
            self.scene.addItem(snowflake)
            self.snowflakes.append(snowflake)

    def update_snowflakes(self):
        for flake in self.snowflakes:
            current_pos = flake.pos()
            new_y = current_pos.y() + flake.fall_speed / 100
            new_x = current_pos.x() + flake.drift / 40
            
            if new_y > self.height():
                new_y = 0
                new_x = random.uniform(0, self.width())
            
            flake.setPos(new_x, new_y)