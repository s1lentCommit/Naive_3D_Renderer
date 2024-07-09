import pygame
from utils import helper_functions as hf

# Camera object that renders the objects
class Camera:
    def __init__(self, position, angle, near_plane_size, near_plane, far_plane, speed):

        self.position            = position
        self.angle               = angle
        self.near_plane_size     = near_plane_size
        self.near_plane_distance = near_plane
        self.far_plane_distance  = far_plane
        self.speed               = speed

        # Get the coordinates of the points with "near_plane_distance/far_plane_distance" from the camera's "position" in the "angle's" direction
        self.mid_point_near = hf.get_mid_point(self.position, self.angle, self.near_plane_distance)
        self.mid_point_far  = hf.get_mid_point(self.position, self.angle, self.far_plane_distance)

        # Vector "v" which direction is perpendicular to the view plane
        self.vector_v = hf.get_difference_vector(self.mid_point_near, self.position)

    # Renders a point by returning the ratio of it's x,y coordinates in the screen
    def render(self, point):
        
        # Get the coordinates of the points with "near_plane_distance/far_plane_distance" from the camera's "position" in the "angle's" direction
        self.mid_point_near = hf.get_mid_point(self.position, self.angle, self.near_plane_distance)
        self.mid_point_far  = hf.get_mid_point(self.position, self.angle, self.far_plane_distance)

        # Vector "v" which direction is perpendicular to the view plane
        self.vector_v = hf.get_difference_vector(self.mid_point_near, self.position)
        
        # Vector "w" which direction is perpendicular v, it's z = 0 and has magnitude = 1
        vector_w = hf.get_perpendicular_vector(self.vector_v)

        # Vector "u" which direction is perpendicular to both "v" and "w" vectors
        vector_u = hf.get_crossproduct_vector(self.vector_v, vector_w)

        # Get the coordinates of the view frostum solid
        view_frostum = hf.get_frostum(self.position, self.near_plane_size, self.mid_point_near, self.mid_point_far, self.vector_v, vector_w, vector_u)

        # Render the point by returning the ratio of it's x,y coordinates in the screen
        return hf.get_render_ratio(self.position, self.near_plane_size, view_frostum, point, self.mid_point_near, self.vector_v, vector_w, vector_u)
    
    def move(self, keys):
        if keys[pygame.K_w]: self.position[0] += self.speed
        if keys[pygame.K_s]: self.position[0] -= self.speed
        if keys[pygame.K_a]: self.position[1] += self.speed
        if keys[pygame.K_d]: self.position[1] -= self.speed

        if keys[pygame.K_SPACE]:  self.position[2] += self.speed
        if keys[pygame.K_LSHIFT]: self.position[2] -= self.speed

        if keys[pygame.K_p]: print(self.position)