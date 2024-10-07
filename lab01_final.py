"""
Name: Angelina Kim
Date: Fall 2024
Purpose: Simulate effects electric and gravitational force from rotating
         satellites on free-moving balls.
"""

from cmu_graphics import *
import time
import math
from random import randrange

def dist(xy1: float, xy2: float) -> float:
    """Calculate distance between two points."""
    return math.sqrt((xy1[0] - xy2[0])**2 + (xy1[1] - xy2[1])**2)

class TimeStamp:
    """Measures time passed.

    Each individual object (e.g., satellite, ball) has a timestamp."""
    def __init__(self):
        self.timeStamp = time.time()
        self.timeLapse = 0
        
    def time_lapse(self) -> float:
        """Calculates and resets time passed."""
        currentTime = time.time()
        self.timeLapse = (currentTime - self.timeStamp)
        self.timeStamp = currentTime
        return self.timeLapse

class Point:
    """Updates object location.

    Helpful for calculating kinetics involving forces or collisions."""
    def __init__(self, xy_parameter: list):
        self.xy_current = [0, 0]
        self.XY_next = [0, 0]
        # Current or previous graph point
        self.xy_current[0] = xy_parameter[0]
        self.xy_current[1] = xy_parameter[1]
        # For calculation and new point
        self.XY_next[0] = xy_parameter[0]
        self.XY_next[1] = xy_parameter[1]        
    
    def update_point(self) -> None:
        """Current point is updated based on calculated point."""
        self.xy_current[0] = self.XY_next[0]
        self.xy_current[1] = self.XY_next[1]
        return None
    
    def copy_point(self) -> None:
        """Copy current point to new point for calculation purpose."""
        self.XY_next[0] = self.xy_current[0]
        self.XY_next[1] = self.xy_current[1]
        return None
        
class GravitationalForce:
    """For gravity force vector calculation."""
    def __init__(self, mass: float):
        self.xyGForce = [0, 0]
        self.mass = mass
        
    def g_force(self, objects: "Ball | Satellite") -> list:
        """Calculating gravity force vector based on object's mass."""
        self.xyGForce = [0, 0]
        vector = [0, 0]

        for obj in objects:
            if obj.name == 'Ball' or obj.name == 'Satellite':
                # Avoids force from itself
                if obj.xy_current[0] != self.xy_current[0] and \
                    obj.xy_current[1] != self.xy_current[1]:
                    vector[0] = obj.xy_current[0] - self.xy_current[0]
                    vector[1] = obj.xy_current[1] - self.xy_current[1]

                    # Pseudo gravitational force formula with  d instead of d^2
                    # for visual exaggeration
                    force = self.mass * obj.mass / dist(self.xy_current, 
                        obj.xy_current)
                    self.xyGForce[0] += vector[0] * force
                    self.xyGForce[1] += vector[1] * force
        return self.xyGForce

class ElectricForce:
    """For electric force calculation."""
    def __init__(self, charge: float):
        self.charge = charge
        self.xyEForce = [0, 0]

    def e_force(self, objects: list) -> list:
        """Calculates & returns electric force vector from objects."""
        self.xyEForce = [0, 0]
        vector = [0, 0]

        for obj in objects:
            # Forces from physical objects only
            if obj.name == 'Ball' or obj.name == 'Satellite':
                # Avoid force from itself
                if obj.xy_current[0] != self.xy_current[0] and \
                    obj.xy_current[1] != self.xy_current[1]:
                    vector[0] = self.xy_current[0] - obj.xy_current[0]
                    vector[1] = self.xy_current[1] - obj.xy_current[1]

                    # Pseudo electric force formula with d instead of d^2
                    # for visual exaggeration
                    force = self.charge * obj.charge / dist(self.xy_current, 
                        obj.xy_current)
                    self.xyEForce[0] += vector[0] * force
                    self.xyEForce[1] += vector[1] * force
        return self.xyEForce

class Boundary:
    """Boundary of app object.

    Detects object collision with boundaries.
    Sets vector for ricochet."""
    def __init__(self, xy1: list, xy2: list):
        # Boundary defined by two points xy1 and xy2, xy1 < xy2
        self.name = 'Boundary'
        self.xy1 = [0, 0]
        self.xy2 = [0, 0]
        self.xy1[0] = xy1[0]
        self.xy1[1] = xy1[1]
        self.xy2[0] = xy2[0]
        self.xy2[1] = xy2[1]

        Line(xy1[0], xy1[1], xy1[0], xy2[1])
        Line(xy1[0], xy1[1], xy2[0], xy1[1])
        Line(xy2[0], xy1[1], xy2[0], xy2[1])
        Line(xy1[0], xy2[1], xy2[0], xy2[1])

    def collision(self, xy_current, xyVelocity: list,
            radius: float, timeLapse: float) -> list:
        reflectVelocity = [0, 0]
        reflectVelocity[0] = xyVelocity[0]
        reflectVelocity[1] = xyVelocity[1]
        XY_next = [0, 0]
        XY_next[0] = xy_current[0]
        XY_next[1] = xy_current[1]

        # Change velocity direction with elastic collision to wall
        if xy_current[0] - self.xy1[0] < radius:
            reflectVelocity = [-xyVelocity[0], xyVelocity[1]]
            XY_next[0] = self.xy1[0] + radius
            XY_next[0] += reflectVelocity[0] * timeLapse
            XY_next[1] += reflectVelocity[1] * timeLapse

        if self.xy2[0] - xy_current[0] < radius:
            reflectVelocity = [-xyVelocity[0], xyVelocity[1]]
            XY_next[0] = self.xy2[0] - radius
            XY_next[0] += reflectVelocity[0] * timeLapse 
            XY_next[1] += reflectVelocity[1] * timeLapse

        if xy_current[1] - self.xy1[1] < radius:
            reflectVelocity = [xyVelocity[0], -xyVelocity[1]]
            XY_next[1] = self.xy1[1] + radius
            XY_next[0] += reflectVelocity[0] * timeLapse 
            XY_next[1] += reflectVelocity[1] * timeLapse

        if self.xy2[1] - xy_current[1] < radius:
            reflectVelocity = [xyVelocity[0], -xyVelocity[1]]
            XY_next[1] = self.xy2[1] - radius
            XY_next[0] += reflectVelocity[0] * timeLapse 
            XY_next[1] += reflectVelocity[1] * timeLapse
        
        # All the objects should stay inside the boundary
        if XY_next[0] - self.xy1[0] < radius:
            XY_next[0] = self.xy1[0] + radius
        if self.xy2[0] - XY_next[0] < radius:
            XY_next[0] = self.xy2[0] - radius
        if XY_next[1] - self.xy1[1] < radius:
            XY_next[1] = self.xy1[1] + radius
        if self.xy2[1] - XY_next[1] < radius:
            XY_next[1] = self.xy2[1] - radius
            
        return [XY_next, reflectVelocity]
    
    def movement(self, objects: list) -> None:
        """Boundary does not move.

        Returns nothing for compatability in onStep()."""
        return None
    
    def update(self, objects: list) -> None:
        """Boundary does not move.

        Returns nothing for compatability in onStep()."""
        return None

class PhysicalProperty:
    """Defines physical characteristics of object."""
    def __init__(self, mass: float, charge: float):
        self.mass = mass
        self.charge = charge
        
class KineticStatus:
    """To calculate object kinetic factors."""
    def __init__(self):
        # Need current and future velocity in case of collision
        self.velocity0 = [0, 0]
        self.velocity1 = [0, 0]
        self.energy = [0, 0]
        self.momentum = [0, 0]

    def kinetic_status_update(self):
        # Copy calculated velocity to current velocity
        self.velocity0[0] = self.velocity1[0]
        self.velocity0[1] = self.velocity1[1]
        
class OrbitalEngine:
    """Sets satellite orbit variables"""
    def __init__(self):
        # In rad / sec
        self.omegaOrbit = 0.1
        self.centerOrbit = [0, 0]
        self.radiusOrbit = 400
        self.directionOrbit = 1
        
class PhysicalObject(PhysicalProperty, GravitationalForce, ElectricForce,
        KineticStatus):
    """Creates physical object with kinetic & electrical properties."""
    def __init__(self, mass: float, charge: float):
        PhysicalProperty.__init__(self, mass, charge)
        KineticStatus.__init__(self)
        GravitationalForce.__init__(self, mass)
        ElectricForce.__init__(self, charge)

        # Positive change is blue
        # Negative charge is red
        # Neutral charge is black
        if charge > 0:
            self.chargeColor = "blue"
        elif charge < 0 :
            self.chargeColor = "red"
        else:
            self.chargeColor = 'black'
                         
# Classes for actual moving objects on app object
class Ball(TimeStamp, Point, PhysicalObject):
    """For ball(s) in app object."""
    def __init__(self, xy_current: list, radius: float, mass: float, 
            charge: float):
        self.name = 'Ball'
        TimeStamp.__init__(self)
        Point.__init__(self, xy_current)
        PhysicalObject.__init__(self, mass, charge)
        self.radius = radius
        self.circle =  Circle(self.xy_current[0], self.xy_current[1],
            radius, fill = self.chargeColor)
        self.weight = mass
        
    def movement(self, objects: list) -> None:
        """Calculate ball velocity based on gravity & electric force."""
        t = self.time_lapse()

        # From xy to XY for calculation
        self.copy_point()

        # Collect force
        self.g_force(objects)
        self.e_force(objects)

        # Total force from G and E
        tXForce = self.xyGForce[0] + self.xyEForce[0]
        tYForce = self.xyGForce[1] + self.xyEForce[1]

        # Acceleration from force
        tXAcc = tXForce / self.mass
        tYAcc = tYForce / self.mass
        
        # Calculate next position
        # Formula: A = dv/dt
        self.velocity1[0] = self.velocity0[0] + tXAcc * t
        self.velocity1[1] = self.velocity0[1] + tYAcc * t

        # Formula: v = dx/dt
        self.XY_next[0] = self.xy_current[0] + self.velocity1[0] * t
        self.XY_next[1] = self.xy_current[1] + self.velocity1[1] * t

        return None
        
    def update(self, objects: list) -> None:
        """Updating ball position based on nearby forces 

        Or object collisions."""
        self.check_collision(objects, self.radius)
        
        # Finalize object movement after collision
        self.update_point() 
        self.kinetic_status_update()
        self.circle.centerX = self.xy_current[0]
        self.circle.centerY = self.xy_current[1]
        return None

    def check_collision(self, objects: list, radius = 1) -> None:
        for obj in objects:
            # Check ball and satellites
            if obj.name == 'Ball' or obj.name == 'Satellite':
                # Exclude itself
                if obj.xy_current[0] != self.xy_current[0] and \
                        obj.xy_current[1] != self.xy_current[1]:
                    # If center of two are closer 
                    # Than the sum of radii at new position XY
                    if dist(self.XY_next, obj.xy_current) < self.radius + \
                            obj.radius:
                        # Prepare metrics for momemtum calculation
                        massDiff = self.mass - obj.mass
                        massSum = self.mass + obj.mass

                        # Velocity after collision
                        self.velocity1[0] = massDiff / massSum \
                            * self.velocity0[0] + 2 * obj.mass \
                            * obj.velocity0[0] / massSum
                        self.velocity1[1] = massDiff / massSum \
                            * self.velocity0[1] + 2 * obj.mass \
                            * obj.velocity0[1]/ massSum

                        # Re-calculate position with reflected velocity
                        self.XY_next[0] = self.xy_current[0] + \
                            self.velocity1[0] * self.timeLapse
                        self.XY_next[1] = self.xy_current[1] + \
                            self.velocity1[1] * self.timeLapse
        
        # Check if ball should bounce at the boundary with a new position
        for obj in objects:
            if obj.name == 'Boundary':
                [xyUpdate, velocityUpdate] = obj.collision(self.XY_next,
                    self.velocity1, radius, self.timeLapse)

                self.XY_next[0] = xyUpdate[0]
                self.XY_next[1] = xyUpdate[1]
                self.velocity1[0] = velocityUpdate[0]
                self.velocity1[1] = velocityUpdate[1]
        return None
    
class Satellite(TimeStamp, Point, OrbitalEngine, PhysicalObject):
    """For moving satellites in ring."""
    def __init__(self, xy_current: list, radius: float, mass: float, 
            charge: float, omega: float, orbitRadius: float, angle: float):
        self.name = 'Satellite'
        TimeStamp.__init__(self)
        Point.__init__(self, xy_current)
        PhysicalObject.__init__(self, mass, charge)
        self.radius = radius
        self.omega = omega
        self.orbitRadius = orbitRadius
        self.angle = angle

        # Orbit around center
        tX = app.centerPlayground[0] + self.orbitRadius * math.cos(self.angle)
        tY = app.centerPlayground[1] + self.orbitRadius * math.sin(self.angle)
        self.circle =  Circle(tX, tY, radius, fill = self.chargeColor)
        self.xy_current[0] = tX
        self.xy_current[1] = tY
        
    def movement(self, objects: "Satellite") -> None:
        """Circular satellite movement."""
        t = self.time_lapse()

        # From xy to XY for calculation
        self.copy_point()
        
        # Angular rotation by timeLapse
        self.angle += t * self.omega
        self.XY_next[0] = app.centerPlayground[0] + self.orbitRadius \
            * math.cos(self.angle)
        self.XY_next[1] = app.centerPlayground[1] + self.orbitRadius \
            * math.sin(self.angle)
        return None
        
    def update(self, objects: list) -> None:
        """Updating satellite position to update nearby vector field points."""
        self.update_point()
        self.circle.centerX = self.xy_current[0]
        self.circle.centerY = self.xy_current[1] 
        return None
        
class PointForceField(Point, GravitationalForce, ElectricForce):
    """For creating and updating field vectors.

    Blue vectors = gravity force
    Red vectors = electrical force
    Black vectors = average of both forces"""
    def __init__(self, xy_current: list):
        self.name = 'Field'
        Point.__init__(self, xy_current)
        GravitationalForce.__init__(self, 1)
        ElectricForce.__init__(self, 1)
        
        # Initial zero force field lines
        self.line_g = Line(xy_current[0], xy_current[1], xy_current[0], 
            xy_current[1], fill='blue')
        self.line_e = Line(xy_current[0], xy_current[1], xy_current[0], 
            xy_current[1], fill='red')
        self.line_t = Line(xy_current[0], xy_current[1], xy_current[0], 
            xy_current[1], fill='black')

    def movement(self, objects: list) -> None:
        """Collects sum of forces from objects."""
        self.g_force(objects)
        self.e_force(objects)
        return None
        
    def update(self, objects: list) -> None:
        """Collecting calculated force vectors & updating field vectors."""
        self.line_g.x2 = self.xyGForce[0] + self.xy_current[0]
        self.line_g.y2 = self.xyGForce[1] + self.xy_current[1]
        self.line_e.x2 = self.xyEForce[0] + self.xy_current[0]
        self.line_e.y2 = self.xyEForce[1] + self.xy_current[1]
        self.line_t.x2 = self.xyGForce[0] + self.xyEForce[0] + \
            self.xy_current[0]
        self.line_t.y2 = self.xyGForce[1] + self.xyEForce[1] + \
            self.xy_current[1]
        return None

def mouse_click_range_check(xy_current: float, xy1: float, xy2: float) -> bool:
    """A function that checks if a mouse click xy is inside a box defined 

    By xy1 and xy2"""
    if xy1[0] < xy_current[0] and xy_current[0] < xy2[0] and xy1[1] < \
            xy_current[1] and xy_current[1] < xy2[1]:
        return True
    else:
        return False

class menuItem:
    """For menu item buttons.

    It can highlight with selected() and deselected()."""
    def __init__(self, stringCategory: type, stringName: str, 
            xy_current: float, size: list, selected: bool):
        self.category = stringCategory
        self.name = stringName
        self.leftTop = [0, 0]
        self.size = [0, 0]

        self.leftTop[0] = xy_current[0]
        self.leftTop[1] = xy_current[1]
        self.size[0] = size[0]
        self.size[1] = size[1]
        self.Button = Rect(self.leftTop[0], self.leftTop[1], self.size[0],
            self.size[1], fill = 'white', border = 'black')
        self.String = Label(stringName, self.leftTop[0] + self.size[0] / 2,
            self.leftTop[1] + self.size[1] / 2)
        if selected == True:
            self.selected()
        else:
            self.deselected()

    def selected(self) -> None:
        """Highlight selection."""
        self.Button.fill = 'black'
        self.String.fill = 'white'
        return None

    def deselected(self) -> None:
        """Remove highlighted selection."""
        self.Button.fill = 'white'
        self.String.fill = 'black'
        return None

def onMousePress(mouseX: float, mouseY: float) -> None:
    clickedXY = [mouseX, mouseY]

    # Check if playground was clicked
    if mouse_click_range_check(clickedXY, [0,0],
        [app.widthPlayground, app.heightPlayground]) == True:

        # Add satellite or ball to playground
        match app.menuChargeType:
            # Positive
            case 'Positive':
                chargeSign = 1
            # Negative
            case 'Negative':
                chargeSign = -1
            # Neutral
            case 'Neutral':
                chargeSign = 0

        match app.menuRotationDirection:
            case 'CW':
                rotationSign = 1
            case 'CCW':
                rotationSign = -1

        match app.menuObjectType:
            case 'Satellite':
                # Get radian angle and radius from playground center
                vectorX = clickedXY[0] - app.centerPlayground[0]
                vectorY = clickedXY[1] - app.centerPlayground[1]
                orbitRadius = dist(clickedXY, app.centerPlayground)
                angle = math.atan2(vectorY, vectorX)
                app.objs.append( 
                                Satellite(app.centerPlayground, 
                                          app.radiusSatellite, 
                                          app.massSatellite, 
                                          app.chargeSatellite * chargeSign,
                                          app.omegaBall * rotationSign,
                                          orbitRadius, angle)) 

            case 'Ball':
                # Add ball at clicked point
                app.objs.append( 
                                Ball(clickedXY, 
                                     app.radiusBall, 
                                     app.massBall, 
                                     app.chargeBall * chargeSign) )

    else:
        # Check if menu items were clicked
        clickedCategory = ''
        clickedName = ''
        # First find out clicked category and name
        for object in app.menuList:
            if mouse_click_range_check(clickedXY, object.leftTop, 
                [object.leftTop[0] + object.size[0], object.leftTop[1] 
                 + object.size[1]] ) == True:
                clickedCategory = object.category
                clickedName = object.name
        
        match clickedCategory:
            case 'Object type':
                # Set the selected type to the variable
                app.menuObjectType = clickedName
                # Highlight selected item'
                # And de-select other items in the same category
                for object in app.menuList:
                    if object.category == clickedCategory:
                        if object.name == clickedName:
                            object.selected()
                        else:
                            object.deselected()

            case 'Charge type':
                # Set the selected type to the variable
                app.menuChargeType = clickedName
                # Highlight selected item
                # And de-select other items in the same category
                for object in app.menuList:
                    if object.category == clickedCategory:
                        if object.name == clickedName:
                            object.selected()
                        else:
                            object.deselected()
                            
            case 'Rotation direction':
                # Set the selected type to the variable
                app.menuRotationDirection = clickedName
                # Highlight selected item
                # And de-select other items in the same category
                for object in app.menuList:
                    if object.category == clickedCategory:
                        if object.name == clickedName:
                            object.selected()
                        else:
                            object.deselected()

            case 'Satellite speed':
                match clickedName:
                    # Set ratio
                    case 'Increase':
                        ratio = app.menuSatelliteSpeedStepRatio
                    case 'Decrease':
                        ratio = 1/app.menuSatelliteSpeedStepRatio
                # Change angular speed of all satellites
                for object in app.objs:
                    if object.name == 'Satellite':
                        object.omega *= ratio

            case 'Satellite mass':
                match clickedName:
                    case 'Increase':
                        ratio = app.menuSatelliteMassStepRatio
                    case 'Decrease':
                        ratio = 1/app.menuSatelliteMassStepRatio
                # Change mass of all satellites
                for object in app.objs:
                    if object.name == 'Satellite':
                        object.mass *= ratio    

            case 'Satellite charge':
                match clickedName:
                    case 'Increase':
                        ratio = app.menuSatelliteChargeStepRatio
                    case 'Decrease':
                        ratio = 1/app.menuSatelliteChargeStepRatio
                # Change charge of all satellites
                for object in app.objs:
                    if object.name == 'Satellite':
                        object.charge *= ratio                

            case 'Ball mass':
                match clickedName:
                    case 'Increase':
                        ratio = app.menuBallMassStepRatio
                    case 'Decrease':
                        ratio = 1/app.menuBallMassStepRatio
                # Change mass of all balls
                for object in app.objs:
                    if object.name == 'Ball':
                        object.mass *= ratio    
                        
            case 'Ball charge':
                match clickedName:
                    case 'Increase':
                        ratio = app.menuBallMassStepRatio
                    case 'Decrease':
                        ratio = 1/app.menuBallMassStepRatio
                # Change mass of all satellites
                for object in app.objs:
                    if object.name == 'Ball':
                        object.charge *= ratio
    return None

def menu_setup() -> None:
    """Creates menu selection items."""

    app.menuObjectTypeList = ['Satellite', 'Ball']
    app.menuObjectType = 'Satellite'
    app.menuChargeTypeList = ['Positive', 'Negative', 'Neutral']
    app.menuChargeType = 'Positive'
    app.menuRotationDirectionList = ['CW', 'CCW']
    app.menuRotationDirection = 'CW'
    app.menuSatelliteSpeed = ['Increase', 'Decrease']
    app.menuSatelliteSpeedStepRatio = 1.25
    app.menuSatelliteMass = ['Increase', 'Decrease']
    app.menuSatelliteMassStepRatio = 1.25
    app.menuSatelliteCharge = ['Increase', 'Decrease']
    app.menuSatelliteChargeStepRatio = 1.25
    app.menuBallMass = ['Increase', 'Decrease']
    app.menuBallMassStepRatio = 1.25
    app.menuBallCharge = ['Increase', 'Decrease']
    app.menuButtonSize = [90, 50]

    # menuItem object list
    app.menuList=[]
    
    # Object type menu
    menuString = 'Object type'
    Label(menuString, app.widthPlayground + 15, 20, align='left')
    for i in range(len(app.menuObjectTypeList)):
        # First item is displayed as selected
        if i == 0: 
            selected = True
        else:
            selected = False
        # Add button and text in the list
        app.menuList.append( menuItem( menuString, app.menuObjectTypeList[i],
            [app.widthPlayground + 10 + 100 *i, 30], app.menuButtonSize,
            selected) )
        
    # Charge type menu
    menuString = 'Charge type'
    Label(menuString, app.widthPlayground + 15, 100, align='left')
    for i in range(len(app.menuChargeTypeList)):
        if i == 0:
            selected = True
        else:
            selected = False
        app.menuList.append( menuItem( menuString, app.menuChargeTypeList[i], 
            [app.widthPlayground + 10 + 100 *i, 110], app.menuButtonSize, 
            selected) )
        
    # Satellite rotation direction menu
    menuString = 'Rotation direction'
    Label(menuString, app.widthPlayground + 15, 180, align='left')
    for i in range(len(app.menuRotationDirectionList)):
        if i == 0:
            selected = True
        else:
            selected = False
        app.menuList.append( menuItem( menuString, 
            app.menuRotationDirectionList[i], 
            [app.widthPlayground + 10 + 100 *i, 190], app.menuButtonSize, 
            selected) )

    # Instruction to add ball or satellite
    Label('Click on the field to place a satelliet or ball', 
        app.widthPlayground + 15, 260, align = 'left')

    # Satellite rotation speed increase menu
    menuString = 'Satellite speed'
    Label(menuString, app.widthPlayground + 15, 310, align='left')
    for i in range(len(app.menuSatelliteSpeed)):
        app.menuList.append( menuItem( menuString, app.menuSatelliteSpeed[i], 
            [app.widthPlayground + 10 + 100 *i, 320], app.menuButtonSize, 
            selected) )

    # Satellite mass increase menu
    menuString = 'Satellite mass'
    Label('Satellite mass', app.widthPlayground + 15, 390, align='left')
    for i in range(len(app.menuSatelliteMass)):
        app.menuList.append( menuItem( menuString, app.menuSatelliteMass[i], 
            [app.widthPlayground + 10 + 100 *i, 400], app.menuButtonSize, 
            selected) )

    # Satellite charge increase menu
    menuString = 'Satellite charge'
    Label(menuString, app.widthPlayground + 15, 470, align='left')
    for i in range(len(app.menuSatelliteCharge)):
        app.menuList.append( menuItem( menuString, app.menuSatelliteCharge[i], 
            [app.widthPlayground + 10 + 100 *i, 480], app.menuButtonSize, 
            selected) )

    # Ball charge increase menu
    menuString = 'Ball mass'
    Label(menuString, app.widthPlayground + 15, 550, align='left')
    for i in range(len(app.menuBallMass)):
        app.menuList.append( menuItem( menuString, app.menuBallMass[i], 
            [app.widthPlayground + 10 + 100 *i, 560], app.menuButtonSize, 
            selected) )

    # Ball mass increase menu
    menuString = 'Ball charge'
    Label(menuString, app.widthPlayground + 15, 630, align='left')
    for i in range(len(app.menuBallCharge)):
        app.menuList.append( menuItem( menuString, app.menuBallCharge[i],  
            [app.widthPlayground + 10 + 100 *i, 640], app.menuButtonSize, 
            selected) )
    return None

# Frame update
def onStep() -> None:
    for object in app.objs:
        object.movement(app.objs)
        object.update(app.objs)
    return None

# Set up screen
def setup() -> None:
    # Global setup
    xCanvas = 1024
    yCanvas = 720
    app.width = xCanvas
    app.height = yCanvas
    app.background = "white"

    # Define playground
    app.widthPlayground = 720
    app.heightPlayground = 720
    app.centerPlayground = [app.widthPlayground/2, app.heightPlayground/2]
    
    # Object setup
    app.radiusBall = 5
    app.radiusSatellite = 10
    app.massBall = 0.1
    app.massSatellite = 5
    app.chargeBall = 0.5
    app.chargeSatellite = 5
    app.omegaBall = 0.2

    # Setup menu
    menu_setup()
    
    # Field vector setup
    app.nColMeter = 12
    app.nRowMeter = 12

    # Graphics objects to interact
    app.objs = []
    app.objs.append(Boundary([0, 0], [app.widthPlayground, 
        app.heightPlayground]))
    
    # Add force field vectors
    for i in range(app.nColMeter):
        for j in range(app.nRowMeter):
            tX = ( i + 1 ) / ( app.nColMeter + 1 ) * app.widthPlayground
            tY = ( j + 1 ) / ( app.nRowMeter + 1 ) * app.heightPlayground
            app.objs.append(PointForceField([tX, tY]))

    # Add three satellites
    app.objs.append(Satellite(app.centerPlayground, app.radiusSatellite, 
        app.massSatellite, 0*app.chargeSatellite, app.omegaBall, 300, 0))
    app.objs.append(Satellite(app.centerPlayground, app.radiusSatellite, 
        app.massSatellite, app.chargeSatellite, -app.omegaBall, 280, 
        math.pi/3))
    app.objs.append(Satellite(app.centerPlayground, app.radiusSatellite, 
        app.massSatellite, -app.chargeSatellite, app.omegaBall, 320, 
        math.pi/2))
    
    # Add four balls
    app.objs.append(Ball([app.widthPlayground/2 - 100, 
        app.heightPlayground/2 - 100], app.radiusBall, app.massBall, 
        0*app.chargeBall))
    app.objs.append(Ball([app.widthPlayground/2 + 100, 
        app.heightPlayground/2 + 100], app.radiusBall, app.massBall, 
        0*app.chargeBall))
    app.objs.append(Ball([app.widthPlayground/2,
        app.heightPlayground/2 + 150], app.radiusBall, app.massBall,
        app.chargeBall))
    app.objs.append(Ball([app.widthPlayground/2, 
        app.heightPlayground/2 - 150], app.radiusBall, app.massBall, 
        -app.chargeBall))
    return None

setup()
cmu_graphics.run()