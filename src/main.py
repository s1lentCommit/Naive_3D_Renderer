import pygame
from stl import mesh
from math import radians
from utils.colors import Color
from camera.camera import Camera
from utils import helper_functions as hf

# TODO: calculate the sign of the vectors XS and YS for the coordinates of the objects outside the view frustum

def main():

    pygame.init()
    width, height = (1280, 720)
    screen = pygame.display.set_mode((width, height)) 

    camera_position = [-10, -3, 9]
    camera_angle = [radians(-5), radians(0)]
    camera_plane_size = (7, 4)
    camera_near_distance = 4
    camera_far_distance = 10
    camera_speed = 0.5

    object = mesh.Mesh.from_file('assets/teapot2.stl')
    object_vertices = object.vectors.tolist()
    #object_normals  = object.normals.tolist()

    cam = Camera(camera_position, camera_angle, camera_plane_size, camera_near_distance, camera_far_distance, camera_speed)

    while True:       
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: quit()
                
        screen.fill((Color.black))

        keys  = pygame.key.get_pressed()
        cam.move(keys)
        
        for triangle in object_vertices:       
            
            points = []
            
            for vertex in triangle:  
                coord = cam.render(vertex)

                x = width  * coord[0]
                y = height * coord[1]

                points.append([x,y])

            if hf.is_clockwise(points):
                pygame.draw.lines(screen, Color.white, True, points)

        pygame.display.flip()

if __name__ == '__main__':
    main()