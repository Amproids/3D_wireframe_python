import tkinter as tk
import math
import time
import pprint
import threading

SCREEN_DIMENSIONS = (860, 600)

class CAMERA:
    x = 0
    y = 0
    focal_length = 500

shape_state = -1
shape_rotation = (0.0, 0.0, 0.0) #x axis, y axis, z axis

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

def rotate_polyhedron(polyhedron, rotation):
    def rotate_coordinate(coordinate_tuple, rotation_tuple):
        """Takes a coordinate in 3D space and rotates it about the y axis.
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

def render_polyhedron(canvas, shape, camera):
    """Takes a tkinter canvas, a shape, and a camera and renders directly to the canvas."""
    line_table = []
    focal_length = camera.focal_length
    for edge in shape.edge_table:
        #Pull out coordinates for first point in edge pair
        coordinates1 = shape.vertex_table[edge[0]]
        try:
            #Calculate 2D projected coordinates
            x1 = (focal_length * (coordinates1[0] - camera.x)) / (focal_length + coordinates1[2]) + (SCREEN_DIMENSIONS[1] / 2)
            #since tkinter canvas y coordinate is top to bottom, we flip all the data with the -1 *
            y1 = -1 * (focal_length * (coordinates1[1] - camera.y)) / (focal_length + coordinates1[2]) + (SCREEN_DIMENSIONS[1] / 2)

            #Pull out coordinates for second point in edge pair
            coordinates2 = shape.vertex_table[edge[1]]
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
    cube2 = rectanglular_prism((-150, -150, -150),(300, 200, 300))
    roof = pyramid((-170, 50, -170),(340, 100, 340))
    door = rectangular_plane((-30, -150, -150), (60, 100, 0))
    window1 = rectangular_plane((-120, -100, -150), (70, 50, 0))
    window2 = rectangular_plane((50, -100, -150), (70, 50, 0))

    def refresh_canvas():
        print(shape_rotation)
        canvas.delete("all")
        if shape_state == 0:
            render_polyhedron(canvas, rotate_polyhedron(cube1, shape_rotation), CAMERA)
        elif shape_state == 1:
            render_polyhedron(canvas, rotate_polyhedron(pyramid1, shape_rotation), CAMERA)
        elif shape_state == 2:
            render_polyhedron(canvas, rotate_polyhedron(cube2, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(roof, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(door, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(window1, shape_rotation), CAMERA)
            render_polyhedron(canvas, rotate_polyhedron(window2, shape_rotation), CAMERA)

    def cube_button_clicked():
        global shape_state 
        shape_state = 0
        refresh_canvas()
    def pyramid_button_clicked():
        global shape_state 
        shape_state = 1
        refresh_canvas()
    def house_button_clicked():
        global shape_state 
        shape_state = 2
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

    def move_left():
        CAMERA.x += 50
        refresh_canvas()
    def move_right():
        CAMERA.x -= 50
        refresh_canvas()

    lbl_shape = tk.Label(   root, width=10, text="Shape:"                                  )
    btn_cube = tk.Button(   root, width=10, text="Cube",     command=cube_button_clicked   )
    btn_pyramid = tk.Button(root, width=10, text="Pyramid",  command=pyramid_button_clicked)
    btn_house = tk.Button(  root, width=10, text="House",    command=house_button_clicked  )
    lbl_blank1 = tk.Label(  root, width=10, text=""                                        )
    lbl_rotation = tk.Label(root, width=10, text="Rotation:"                               )
    btn_x = tk.Button(      root, width=10, text=" X ",      command=x_axis_button_clicked )
    btn_y = tk.Button(      root, width=10, text=" Y ",      command=y_axis_button_clicked )
    btn_z = tk.Button(      root, width=10, text=" Z ",      command=z_axis_button_clicked )
    lbl_blank2 = tk.Label(  root, width=10, text=""                                        )

    control_frame = tk.Frame(root, bd=5)
    btn_move_left = tk.Button( control_frame, width=10, text="Left",  command=move_left )
    btn_move_right = tk.Button(control_frame, width=10, text="Right", command=move_right)

    btn_exit = tk.Button(        root, width=10, text="Exit",     command=lambda: root.quit()   )

    canvas.grid(        row=0,  column=0, rowspan=25, stick="ew")
    lbl_shape.grid(     row=0,  column=1, padx=2, pady=2)
    btn_cube.grid(      row=1,  column=1, padx=2, pady=2)
    btn_pyramid.grid(   row=2,  column=1, padx=2, pady=2)
    btn_house.grid(     row=3,  column=1, padx=2, pady=2)
    lbl_blank1.grid(    row=4,  column=1, padx=2, pady=2)
    lbl_rotation.grid(  row=5,  column=1, padx=2, pady=2)
    btn_x.grid(         row=6,  column=1, padx=2, pady=2)
    btn_y.grid(         row=7,  column=1, padx=2, pady=2)
    btn_z.grid(         row=8,  column=1, padx=2, pady=2)
    lbl_blank2.grid(    row=9,  column=1, padx=2, pady=2)

    control_frame.grid( row=10, column=1, padx=1, pady=1)
    btn_move_left.grid( row=0,  column=0, padx=1, pady=1)
    btn_move_right.grid(row=0,  column=1, padx=1, pady=1)

    btn_exit.grid(      row=11, column=1, padx=2, pady=2)

    tk.mainloop()
        
if __name__ == "__main__":
    main()