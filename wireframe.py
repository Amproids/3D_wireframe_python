import tkinter as tk
import math

pi = math.pi
SCREEN_DIMENSIONS = (800, 600)

class CAMERA:
    x = 0
    y = 0
    focal_length = 500

shape_state = -1
shape_rotation = (0.0, 0.0, 0.0) #x axis, y axis, z axis

def transform_polyhedron(polyhedron, transform_tuple):
    def transform_coordinate(coordinate_tuple, transform_tuple):
        """Takes a coordinate in 3D space and transforms it.
        Funciton takes rotation in degrees.
        """
        #extract transformation and coordinate data
        dx = transform_tuple[0]
        dy = transform_tuple[1]
        dz = transform_tuple[2]
        x = coordinate_tuple[0]
        y = coordinate_tuple[1]
        z = coordinate_tuple[2]
        return(x + dx, y + dy, z + dz)
    
    class new_polyhedron:
        edge_table = polyhedron.edge_table
        vertex_table = {}
    for key in polyhedron.vertex_table:
        new_polyhedron.vertex_table.update({key: transform_coordinate(polyhedron.vertex_table[key], transform_tuple)})
    return new_polyhedron

def rotate_polyhedron(polyhedron, rotation):
    def rotate_coordinate(coordinate_tuple, rotation_tuple):
        """Takes a coordinate in 3D space and rotates it about all axis, one at a time.
        Funciton takes rotation in degrees.
        """
        #extract rotation and coordinate data
        pitch = math.radians(rotation_tuple[0])
        yaw = math.radians(rotation_tuple[1])
        roll = math.radians(rotation_tuple[2])
        x = coordinate_tuple[0]
        y = coordinate_tuple[1]
        z = coordinate_tuple[2]
        #rotate about the x axis
        x1 = x
        y1 = (y * math.cos(pitch)) - (z * math.sin(pitch))
        z1 = (y * math.sin(pitch)) + (z * math.cos(pitch))
        #rotate about the y axis
        x2 = (x1 * math.cos(yaw)) - (z1 * math.sin(yaw))
        y2 = y1
        z2 = (x1 * math.sin(yaw)) + (z1 * math.cos(yaw))
        #rotate about the z axis
        x3 = (x2 * math.cos(roll)) - (y2 * math.sin(roll))
        y3 = (x2 * math.sin(roll)) + (y2 * math.cos(roll))
        z3 = z2
        return(x3, y3, z3)
    
    class new_polyhedron:
        edge_table = polyhedron.edge_table
        vertex_table = {}
    for key in polyhedron.vertex_table:
        new_polyhedron.vertex_table.update({key: rotate_coordinate(polyhedron.vertex_table[key], rotation)})
    return new_polyhedron

class rectangular_plane:
    def __init__(self, coordinates=(0, 0, 0), whd=(100, 0, 100)):
        self.edge_table = ('AB', 'BC', 'CD', 'DA')
        self.vertex_table = {
            'A': (coordinates[0],          coordinates[1],          coordinates[2]         ),
            'B': (coordinates[0] + whd[0], coordinates[1],          coordinates[2]         ),
            'C': (coordinates[0] + whd[0], coordinates[1] + whd[1], coordinates[2]         ),
            'D': (coordinates[0],          coordinates[1] + whd[1], coordinates[2]         ),
        }

class rectanglular_prism:
    def __init__(self, coordinates=(0, 0, 0), whd=(100, 100, 100)):
        """Takes 3D coordinate tuple and width, height, depth (whd) tuple and makes usable cube data."""
        self.edge_table = ('AB', 'BC', 'CD', 'DA', 'EF', 'FG', 'GH', 'HE', 'AE', 'BF', 'CG', 'DH')
        self.vertex_table = {
            'A': (coordinates[0],          coordinates[1],          coordinates[2]         ),
            'B': (coordinates[0] + whd[0], coordinates[1],          coordinates[2]         ),
            'C': (coordinates[0] + whd[0], coordinates[1] + whd[1], coordinates[2]         ),
            'D': (coordinates[0],          coordinates[1] + whd[1], coordinates[2]         ),
            'E': (coordinates[0],          coordinates[1],          coordinates[2] + whd[2]),
            'F': (coordinates[0] + whd[0], coordinates[1],          coordinates[2] + whd[2]),
            'G': (coordinates[0] + whd[0], coordinates[1] + whd[1], coordinates[2] + whd[2]),
            'H': (coordinates[0],          coordinates[1] + whd[1], coordinates[2] + whd[2])
    }

class pyramid:
    def __init__(self, coordinates=(0, 0, 0), whd=(100, 100, 100)):
        """Takes 3D coordinate tuple and width, height, depth (whd) tuple and makes usable pyramid data."""
        self.edge_table = ('AB', 'BC', 'CD', 'DA', 'AE', 'BE', 'CE', 'DE')
        self.vertex_table = {
            'A': (coordinates[0],                coordinates[1],          coordinates[2]               ),
            'B': (coordinates[0] + whd[0],       coordinates[1],          coordinates[2]               ),
            'C': (coordinates[0] + whd[0],       coordinates[1],          coordinates[2] + whd[2]      ),
            'D': (coordinates[0],                coordinates[1],          coordinates[2] + whd[2]      ),
            'E': (coordinates[0] + (whd[0] / 2), coordinates[1] + whd[1], coordinates[2] + (whd[2] / 2))
        }

class circle:
    def __init__(self, coordinates=(0, 0, 0), radius=50):
        self.edge_table = ('AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'HI', 'IJ', 'JA')
        self.vertex_table = {
            'A': (coordinates[0] + math.sin(2 * pi * (0/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (0/10)) * radius),
            'B': (coordinates[0] + math.sin(2 * pi * (1/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (1/10)) * radius),
            'C': (coordinates[0] + math.sin(2 * pi * (2/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (2/10)) * radius),
            'D': (coordinates[0] + math.sin(2 * pi * (3/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (3/10)) * radius),
            'E': (coordinates[0] + math.sin(2 * pi * (4/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (4/10)) * radius),
            'F': (coordinates[0] + math.sin(2 * pi * (5/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (5/10)) * radius),
            'G': (coordinates[0] + math.sin(2 * pi * (6/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (6/10)) * radius),
            'H': (coordinates[0] + math.sin(2 * pi * (7/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (7/10)) * radius),
            'I': (coordinates[0] + math.sin(2 * pi * (8/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (8/10)) * radius),
            'J': (coordinates[0] + math.sin(2 * pi * (9/10)) * radius, coordinates[1], coordinates[2] + math.cos(2 * pi * (9/10)) * radius)
        }
        
class sphere:
    def __init__(self, coordinates=(0, 0, 0), radius = 50):
        '''The sphere is gonna be made of a bunch of rotated circles.
        Because of how my code rotates objects about the origin. It will all be built at the origin, then transformed.
        That's why the sphere class is the only one that is made this way.'''
        
        #The first verticle circle is built.
        self.edge_table = ('AAAB', 'ABAC', 'ACAD', 'ADAE', 'AEAF', 'AFAG', 'AGAH', 'AHAI', 'AIAJ', 'AJAA')
        self.vertex_table = {
            'AA': (math.sin(2 * pi * (0/10)) * radius, math.cos(2 * pi * (0/10)) * radius, 0),
            'AB': (math.sin(2 * pi * (1/10)) * radius, math.cos(2 * pi * (1/10)) * radius, 0),
            'AC': (math.sin(2 * pi * (2/10)) * radius, math.cos(2 * pi * (2/10)) * radius, 0),
            'AD': (math.sin(2 * pi * (3/10)) * radius, math.cos(2 * pi * (3/10)) * radius, 0),
            'AE': (math.sin(2 * pi * (4/10)) * radius, math.cos(2 * pi * (4/10)) * radius, 0),
            'AF': (math.sin(2 * pi * (5/10)) * radius, math.cos(2 * pi * (5/10)) * radius, 0),
            'AG': (math.sin(2 * pi * (6/10)) * radius, math.cos(2 * pi * (6/10)) * radius, 0),
            'AH': (math.sin(2 * pi * (7/10)) * radius, math.cos(2 * pi * (7/10)) * radius, 0),
            'AI': (math.sin(2 * pi * (8/10)) * radius, math.cos(2 * pi * (8/10)) * radius, 0),
            'AJ': (math.sin(2 * pi * (9/10)) * radius, math.cos(2 * pi * (9/10)) * radius, 0),
        }

        #Then the circle is rotated
        self.vertex_table = rotate_polyhedron(self, (0, 45, 0)).vertex_table
        #And the next verticle circle is built. It Does not inclue the 0/10 or 5/10 verticies because that is vertex A and F from the first circle.
        self.edge_table = self.edge_table + ('AAAK', 'AKAL', 'ALAM', 'AMAN', 'ANAF', 'AFAO', 'AOAP', 'APAQ', 'AQAR', 'ARAA')
        self.vertex_table.update({
            'AK': (math.sin(2 * pi * (1/10)) * radius, math.cos(2 * pi * (1/10)) * radius, 0),
            'AL': (math.sin(2 * pi * (2/10)) * radius, math.cos(2 * pi * (2/10)) * radius, 0),
            'AM': (math.sin(2 * pi * (3/10)) * radius, math.cos(2 * pi * (3/10)) * radius, 0),
            'AN': (math.sin(2 * pi * (4/10)) * radius, math.cos(2 * pi * (4/10)) * radius, 0),
            'AO': (math.sin(2 * pi * (6/10)) * radius, math.cos(2 * pi * (6/10)) * radius, 0),
            'AP': (math.sin(2 * pi * (7/10)) * radius, math.cos(2 * pi * (7/10)) * radius, 0),
            'AQ': (math.sin(2 * pi * (8/10)) * radius, math.cos(2 * pi * (8/10)) * radius, 0),
            'AR': (math.sin(2 * pi * (9/10)) * radius, math.cos(2 * pi * (9/10)) * radius, 0)
        })
        self.edge_table = self.edge_table + ('ABAK', 'ACAL', 'ADAM', 'AEAN', 'AGAO', 'AHAP', 'AIAQ', 'AJAR')

        #Then the circle is rotated again.
        self.vertex_table = rotate_polyhedron(self, (0, 45, 0)).vertex_table
        #Circle 3 is now built
        self.edge_table = self.edge_table + ('AAAS', 'ASAT', 'ATAU', 'AUAV', 'AVAF', 'AFAW', 'AWAX', 'AXAY', 'AYAZ', 'AZAA')
        self.vertex_table.update({
            'AS': (math.sin(2 * pi * (1/10)) * radius, math.cos(2 * pi * (1/10)) * radius, 0),
            'AT': (math.sin(2 * pi * (2/10)) * radius, math.cos(2 * pi * (2/10)) * radius, 0),
            'AU': (math.sin(2 * pi * (3/10)) * radius, math.cos(2 * pi * (3/10)) * radius, 0),
            'AV': (math.sin(2 * pi * (4/10)) * radius, math.cos(2 * pi * (4/10)) * radius, 0),

            'AW': (math.sin(2 * pi * (6/10)) * radius, math.cos(2 * pi * (6/10)) * radius, 0),
            'AX': (math.sin(2 * pi * (7/10)) * radius, math.cos(2 * pi * (7/10)) * radius, 0),
            'AY': (math.sin(2 * pi * (8/10)) * radius, math.cos(2 * pi * (8/10)) * radius, 0),
            'AZ': (math.sin(2 * pi * (9/10)) * radius, math.cos(2 * pi * (9/10)) * radius, 0)
        })
        self.edge_table = self.edge_table + ('AKAS', 'ALAT', 'AMAU', 'ANAV', 'AOAW', 'APAX', 'AQAY', 'ARAZ')

        #Then the circle is rotated again.
        self.vertex_table = rotate_polyhedron(self, (0, 45, 0)).vertex_table
        #Circle 4 is now built
        self.edge_table = self.edge_table + ('AABA', 'BABB', 'BBBC', 'BCBD', 'BDAF', 'AFBE', 'BEBF', 'BFBG', 'BGBH', 'BHAA')
        self.vertex_table.update({
            'BA': (math.sin(2 * pi * (1/10)) * radius, math.cos(2 * pi * (1/10)) * radius, 0),
            'BB': (math.sin(2 * pi * (2/10)) * radius, math.cos(2 * pi * (2/10)) * radius, 0),
            'BC': (math.sin(2 * pi * (3/10)) * radius, math.cos(2 * pi * (3/10)) * radius, 0),
            'BD': (math.sin(2 * pi * (4/10)) * radius, math.cos(2 * pi * (4/10)) * radius, 0),
            'BE': (math.sin(2 * pi * (6/10)) * radius, math.cos(2 * pi * (6/10)) * radius, 0),
            'BF': (math.sin(2 * pi * (7/10)) * radius, math.cos(2 * pi * (7/10)) * radius, 0),
            'BG': (math.sin(2 * pi * (8/10)) * radius, math.cos(2 * pi * (8/10)) * radius, 0),
            'BH': (math.sin(2 * pi * (9/10)) * radius, math.cos(2 * pi * (9/10)) * radius, 0)
        })
        self.edge_table = self.edge_table + ('ASBA', 'ATBB', 'AUBC', 'AVBD', 'AWBE', 'AXBF', 'AYBG', 'AZBH')
        self.edge_table = self.edge_table + ('BAAJ', 'BBAI', 'BCAH', 'BDAG', 'BEAE', 'BFAD', 'BGAC', 'BHAB')

        self.vertex_table = transform_polyhedron(self, (coordinates[0], coordinates[1], coordinates[2])).vertex_table

def render_polyhedron(canvas, shape, camera):
    """Takes a tkinter canvas, a shape, and a camera and renders directly to the canvas."""
    line_table = []
    focal_length = camera.focal_length
    for edge in shape.edge_table:
        char_length = int(len(edge)/2)
        #Pull out coordinates for first point in edge pair
        coordinates1 = shape.vertex_table[edge[:char_length]]
        try:
            #Calculate 2D projected coordinates
            x1 = (focal_length * (coordinates1[0] - camera.x)) / (focal_length + coordinates1[2]) + (SCREEN_DIMENSIONS[1] / 2)
            #since tkinter canvas y coordinate is top to bottom, we flip all the data with the -1 *
            y1 = -1 * (focal_length * (coordinates1[1] - camera.y)) / (focal_length + coordinates1[2]) + (SCREEN_DIMENSIONS[1] / 2)

            #Pull out coordinates for second point in edge pair
            coordinates2 = shape.vertex_table[edge[char_length:]]
            #Calculate 2D projected coordinates
            x2 = (focal_length * (coordinates2[0] - camera.x)) / (focal_length + coordinates2[2]) + (SCREEN_DIMENSIONS[1] / 2)
            #since tkinter canvas y coordinate is top to bottom, we flip all the data with the -1 *
            y2 = -1 * (focal_length * (coordinates2[1] - camera.y)) / (focal_length + coordinates2[2]) + (SCREEN_DIMENSIONS[1] / 2)
            #Append projected line coordinates into line_table
            line_table.append(((x1, y1), (x2, y2)))
        except ZeroDivisionError:
            pass

    #This is the part of the code that actually renders the polyhedron.
    for line in line_table:
        canvas.create_line(line[0][0], line[0][1], line[1][0], line[1][1])

def main():
    root = tk.Tk()
    root.geometry(f"{SCREEN_DIMENSIONS[0]}x{SCREEN_DIMENSIONS[1]}")
    root.title("3D WireFrame")

    canvas = tk.Canvas(root, width=SCREEN_DIMENSIONS[1], height=SCREEN_DIMENSIONS[1], bg="White")

    cube1 = rectanglular_prism((-100, -100, -100),(200, 200, 200))
    pyramid1 = pyramid((-100, -100, -100),(200, 200, 200))
    sphere1 = sphere((0, 0, 0), 150)

    walls = rectanglular_prism((-150, -150, -150),(300, 200, 300))
    roof = pyramid((-170, 50, -170),(340, 100, 340))
    door = rectangular_plane((-30, -150, -150), (60, 100, 0))
    window1 = rectangular_plane((-120, -100, -150), (70, 50, 0))
    window2 = rectangular_plane((50, -100, -150), (70, 50, 0))
    floor = circle((0, -150, 0), 100)
    roof_ornament = sphere((0, 170, 0), 20)

    def refresh_canvas():
        canvas.delete("all")
        if shape_state == 0:
            render_polyhedron(canvas, rotate_polyhedron(cube1, shape_rotation), CAMERA)
        elif shape_state == 1:
            render_polyhedron(canvas, rotate_polyhedron(pyramid1, shape_rotation), CAMERA)
        elif shape_state == 2:
            render_polyhedron(canvas, rotate_polyhedron(sphere1, shape_rotation), CAMERA)
        elif shape_state == 3:
            render_polyhedron(canvas, rotate_polyhedron(walls, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(roof, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(door, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(window1, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(window2, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(floor, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(roof_ornament, shape_rotation), CAMERA)

    def cube_button_clicked():
        global shape_state 
        shape_state = 0
        refresh_canvas()
    def pyramid_button_clicked():
        global shape_state 
        shape_state = 1
        refresh_canvas()
    def sphere_button_clicked():
        global shape_state 
        shape_state = 2
        refresh_canvas()
    def house_button_clicked():
        global shape_state 
        shape_state = 3
        refresh_canvas()
    def x_axis_button_clicked():
        global shape_rotation
        if shape_rotation[0] + 22.5 == 360:
            shape_rotation = (0.0, shape_rotation[1], shape_rotation[2])
        else:
            shape_rotation = (shape_rotation[0] + 22.5, shape_rotation[1], shape_rotation[2])
        refresh_canvas()
    def y_axis_button_clicked():
        global shape_rotation
        if shape_rotation[1] + 22.5 == 360:
            shape_rotation = (shape_rotation[0], 0.0, shape_rotation[2])
        else:
            shape_rotation = (shape_rotation[0], shape_rotation[1] + 22.5, shape_rotation[2])
        refresh_canvas()
    def z_axis_button_clicked():
        global shape_rotation
        if shape_rotation[2] + 22.5 == 360:
            shape_rotation = (shape_rotation[0], shape_rotation[1], 0.0)
        else:
            shape_rotation = (shape_rotation[0], shape_rotation[1], shape_rotation[2] + 22.5)
        refresh_canvas()
    def move_up():
        CAMERA.y -= 50
        refresh_canvas()
    def move_down():
        CAMERA.y += 50
        refresh_canvas()
    def move_left():
        CAMERA.x += 50
        refresh_canvas()
    def move_right():
        CAMERA.x -= 50
        refresh_canvas()
    def reset_button_clicked():
        global shape_state
        global shape_rotation
        shape_rotation = (0, 0, 0)
        CAMERA.x = 0
        CAMERA.y = 0
        shape_state = -1
        refresh_canvas()

    lbl_shape = tk.Label(   root, width=10, text="Shape:"                                  )
    btn_cube = tk.Button(   root, width=10, text="Cube",     command=cube_button_clicked   )
    btn_pyramid = tk.Button(root, width=10, text="Pyramid",  command=pyramid_button_clicked)
    btn_sphere = tk.Button( root, width=10, text="Sphere",   command=sphere_button_clicked )
    btn_house = tk.Button(  root, width=10, text="House",    command=house_button_clicked  )
    lbl_blank1 = tk.Label(  root, width=10, text=""                                        )

    lbl_rotation = tk.Label(root, width=10, text="Rotation:"                               )
    btn_x = tk.Button(      root, width=10, text=" X ",      command=x_axis_button_clicked )
    btn_y = tk.Button(      root, width=10, text=" Y ",      command=y_axis_button_clicked )
    btn_z = tk.Button(      root, width=10, text=" Z ",      command=z_axis_button_clicked )
    lbl_blank2 = tk.Label(  root, width=10, text=""                                        )

    lbl_transform = tk.Label(root, width=10, text="Transform:"                              )
    control_frame = tk.Frame(root, bd=5)
    btn_move_up = tk.Button(   root,          width=10, text="Up",    command=move_up   )
    btn_move_left = tk.Button( control_frame, width=10, text="Left",  command=move_left )
    btn_move_right = tk.Button(control_frame, width=10, text="Right", command=move_right)
    btn_move_down = tk.Button( root,          width=10, text="Down",  command=move_down )
    lbl_blank3 = tk.Label(  root, width=10, text=""                                        )
    btn_reset = tk.Button(  root, width=10, text="Reset",    command=reset_button_clicked  )
    lbl_blank4 = tk.Label(  root, width=10, text=""                                        )

    btn_exit = tk.Button(        root, width=10, text="Exit",     command=lambda: root.quit()   )

    canvas.grid(        row=0,  column=0, rowspan=25, stick="ew")

    lbl_shape.grid(     row=0,  column=1, padx=2, pady=2)
    btn_cube.grid(      row=1,  column=1, padx=2, pady=2)
    btn_pyramid.grid(   row=2,  column=1, padx=2, pady=2)
    btn_sphere.grid(    row=3,  column=1, padx=2, pady=2)
    btn_house.grid(     row=4,  column=1, padx=2, pady=2)
    lbl_blank1.grid(    row=5,  column=1, padx=2, pady=2)

    lbl_rotation.grid(  row=6,  column=1, padx=2, pady=2)
    btn_x.grid(         row=7,  column=1, padx=2, pady=2)
    btn_y.grid(         row=8,  column=1, padx=2, pady=2)
    btn_z.grid(         row=9,  column=1, padx=2, pady=2)
    lbl_blank2.grid(    row=10, column=1, padx=2, pady=2)

    lbl_transform.grid( row=11, column=1, padx=2, pady=2)
    btn_move_up.grid(   row=12, column=1, padx=1, pady=1)
    control_frame.grid( row=13, column=1, padx=1, pady=1)
    btn_move_left.grid( row=1,  column=0, padx=1, pady=1)
    btn_move_right.grid(row=1,  column=1, padx=1, pady=1)
    btn_move_down.grid( row=14,  column=1, padx=1, pady=1)
    lbl_blank3.grid(    row=15, column=1, padx=2, pady=2)

    btn_reset.grid(     row=16, column=1, padx=2, pady=2)
    lbl_blank4.grid(    row=17, column=1, padx=2, pady=2)

    btn_exit.grid(      row=18, column=1, padx=2, pady=2)

    tk.mainloop()
        
if __name__ == "__main__":
    main()