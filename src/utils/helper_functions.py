from math import cos, sin, sqrt

# Check if a triangle is clockwise (facing front)
def is_clockwise(points):

    # Reads the components of the 3 points A,B,C
    xa, ya = points[0]
    xb, yb = points[1]
    xc, yc = points[2]

    # Calculates "v" is the vector (AB), "w" is the vector (BC)  
    xv, yv = (xb - xa, yb - ya)
    xw, yw = (xc - xb, yc - yb)

    # Calculates the cross product of "v x w" (result is it's z component as it's perpendicular to the xy plane)
    return ( xv * yw - yv * xw ) < 0
    
# Gets the coordinates of the point with a certain "distance" from "position" in the angle's direction
def get_mid_point(position, angle, distance):

    # Angle of the camera's direction, (alfa = angle with xy plane), (beta = angle with it's projection and x axis)
    alfa, beta = angle

    # Camera's focal point "P" position
    xP, yP, zP = position

    # Coordinates of the point with a certain "distance" from "position" in the angle's direction
    x = distance * cos(beta) * cos(alfa) + xP
    y = distance * sin(beta) * cos(alfa) + yP
    z = distance * sin(alfa) + zP

    return (x, y, z)

# Calculates the difference vector from two vectors as input (vector_b - vector_a)
def get_difference_vector(vector_a, vector_b):

    # read the components of both vectors
    xa, ya, za = vector_a
    xb, yb, zb = vector_b

    return ( xb - xa, yb - ya, zb - za )

# Calculates the perpendicular vector to the input vector, (based on their cross product = 0), (it has magnitude = 1) and (it's z = 0)
def get_perpendicular_vector(vector):

    # read the components of both vectors
    xv, yv, zv = vector

    return( - yv / sqrt( xv**2 + yv**2 ), xv / sqrt( xv**2 + yv**2 ), 0 )

# Calculates the vector obtained from the cross product between the two input vectors (vector_a x vector_b)
def get_crossproduct_vector(vector_a, vector_b):

    # read the components of both vectors
    xa, ya, za = vector_a
    xb, yb, zb = vector_b

    return ( - za * yb, za * xb, xa * yb - ya * xb )


# Calculates the vector obtained from the cross product between the two input vectors (vector_a x vector_b)
def get_dotproduct(vector_a, vector_b):

    # read the components of both vectors
    xa, ya, za = vector_a
    xb, yb, zb = vector_b

    return xa * xb + ya * yb + za * zb

# Calculates the distance between two points in 3D space
def get_distance(point_a, point_b):

    # read the components of both points
    xa, ya, za = point_a
    xb, yb, zb = point_b

    return sqrt( (xa-xb)**2 + (ya-yb)**2 +(za-zb)**2 )

# Calculates the coords of the view plane rectangle from the camera's focal point position and it's distance from it, it's direction angle, the plane's size 
def get_frostum(position, near_plane_size, mid_point_near, mid_point_far, vector_v, vector_w, vector_u):

    # The view plane's width and height size
    width, height = near_plane_size

    # Camera's focal point "P" position
    xP, yP, zP = position

    # Near plane and far plane's mid points "N", "F"
    xN, yN, zN = mid_point_near
    xF, yF, zF = mid_point_far

    # Read the coords of all perpendicular vectors of the camera's direction
    xv, yv, zv = vector_v 
    xw, yw, zw = vector_w
    xu, yu, zu = vector_u

    # Variables obtained from solving the system between the lines passing through "N" with "v" and "w" directions distances = width/2 and height/2
    th = height / ( 2 * sqrt( xu**2 + yu**2 + zu**2 ) )
    tw = width  / ( 2 * sqrt( xw**2 + yw**2 ) )

    # The Point "O" which distance from "N" is height/2 and intersects with the line passing through "N" with "u" direction (we just need it's z)
    zO = zN + zu * th

    # The Point "Q" which distance from "N" is width/2  and intersects with the line passing through "N" with "w" direction (it's z = zP)
    xQ, yQ = ( xN + xw * tw, yN + yw * tw )

    # The Point "T" which is basically like the previous one, but just at the opposite side of "N" in the same line (it's z = zP)
    xT, yT = ( xN - xw * tw, yN - yw * tw )

    # Variable obtained from solving the system between the line passing through "O" with "w" direction and the line passing through "Q" with "u" direction
    tq = ( zO - zN ) / zu

    # The coords "A,B,C,D" of the near plane rectangle with it's points named from top left in clockwise order 
    A = xA, yA, zA = ( xQ + xu * tq, yQ + yu * tq, zN + zu * tq )
    B = xB, yB, zB = ( xT + xu * tq, yT + yu * tq, zN + zu * tq )
    C = xC, yC, zC = ( xT - xu * tq, yT - yu * tq, zN - zu * tq )
    D = xD, yD, zD = ( xQ - xu * tq, yQ - yu * tq, zN - zu * tq )

    # The vectors of direction that goes through "P" and each of the points "A,B,C,D" of the near plane rectangle
    xa, ya, za = ( xA - xP, yA - yP, zA - zP )
    xb, yb, zb = ( xB - xP, yB - yP, zB - zP )
    xc, yc, zc = ( xC - xP, yC - yP, zC - zP )
    xd, yd, zd = ( xD - xP, yD - yP, zD - zP )

    # Variable obtained from solving the system between the line passing through "P" with "a" direction and the equation of the far plane
    tf = ( xv * ( xF - xP) + yv * ( yF - yP ) + zv * ( zF - zP) ) / (xv * xa + yv * ya + zv * za)

    # The coords "G,H,I,J" of the far plane rectangle with it's points named from top left in clockwise order 
    G = (xP + xa * tf, yP + ya * tf, zP + za * tf)
    H = (xP + xb * tf, yP + yb * tf, zP + zb * tf)
    I = (xP + xc * tf, yP + yc * tf, zP + zc * tf)
    J = (xP + xd * tf, yP + yd * tf, zP + zd * tf)

    return ( A, B, C, D, G, H, I, J )

def get_render_ratio(position, near_plane_size, view_frostum, point, mid_point_near, vector_v, vector_w, vector_u):
    
    # Camera's focal point "P" position
    xP, yP, zP = position

    # The view plane's width and height size
    width, height = near_plane_size

    # Access the coordinates of the near plane's top left point "A"
    B = xB, yB, zB = view_frostum[1]

    # Point "R" that will get rendered
    xR, yR, zR = point

    # Near plane mid point
    xN, yN, zN = mid_point_near

    # Read the coords of all perpendicular vectors of the camera's direction
    xv, yv, zv = vector_v 
    xw, yw, zw = vector_w
    xu, yu, zu = vector_u
    
    # Vector "e" which direction is of the line passing through "R" and "P"
    xe, ye, ze = ( xP - xR, yP - yR, zP - zR )

    # Variable obtained from solving the system between the line passing through "R" with direction "e" and the near plane equation
    tr = ( xv * ( xN - xR ) + yv * (yN - yR) + zv * ( zN - zR) ) / ( xv * xe + yv * ye + zv * ze)

    # Point "S" obtained from rendering "R" to the near plane 
    xS, yS, zS = ( xR + xe * tr,  yR + ye * tr, zR + ze * tr)
    
    # Variable obtained from solving the system between the line passing through "S" with "w" direction and the line passing through "A" with "u" direction
    ts = ( zB - zS ) / zu

    # The points intersecting the near plane's top side and left side obtained from projecting S into them
    X = (xS + xu * ts, yS + yu * ts, zS + zu * ts)
    Y = (xB - xu * ts, yB - yu * ts, zB - zu * ts)
    
    # Get the distance betwen the point "A" and the projections of "S" which are ("X", "Y")
    dx = get_distance(B, X)
    dy = get_distance(B, Y)

    return dx/width, dy/height

   




