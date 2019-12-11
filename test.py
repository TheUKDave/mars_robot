from unittest import TestCase

from robot import Robot, GridNavigator


class TestRobotOrientation(TestCase):

    def setUp(self):
        self.robot = Robot(0, 0, 'N')

    def test_initial_orientation(self):
        self.assertEqual(self.robot.orientation, 'N')
        self.robot = Robot(0, 0, 'S')
        self.assertEqual(self.robot.orientation, 'S')
        self.robot = Robot(0, 0, 'E')
        self.assertEqual(self.robot.orientation, 'E')
        self.robot = Robot(0, 0, 'W')
        self.assertEqual(self.robot.orientation, 'W')

    def test_set_orientation(self):
        self.robot.orientation = 'E'
        self.assertEqual(self.robot.orientation, 'E')
        self.robot.orientation = 'S'
        self.assertEqual(self.robot.orientation, 'S')
        self.robot.orientation = 'W'
        self.assertEqual(self.robot.orientation, 'W')
        self.robot.orientation = 'N'
        self.assertEqual(self.robot.orientation, 'N')

    def test_set_bad_orientation(self):
        with self.assertRaises(TypeError):
            self.robot.orientation = 1

        with self.assertRaises(ValueError):
            self.robot.orientation = 'A'

        with self.assertRaises(ValueError):
            self.robot.orientation = 'NW'

    def test_rotate_left(self):
        # Rotate 4 times left (through 360)
        self.robot.rotate_left()
        self.assertEqual(self.robot.orientation, 'W')
        self.robot.rotate_left()
        self.assertEqual(self.robot.orientation, 'S')
        self.robot.rotate_left()
        self.assertEqual(self.robot.orientation, 'E')
        self.robot.rotate_left()
        # We end up back at North
        self.assertEqual(self.robot.orientation, 'N')

    def test_rotate_right(self):
        # Rotate 4 times left (through 360)
        self.robot.rotate_right()
        self.assertEqual(self.robot.orientation, 'E')
        self.robot.rotate_right()
        self.assertEqual(self.robot.orientation, 'S')
        self.robot.rotate_right()
        self.assertEqual(self.robot.orientation, 'W')
        self.robot.rotate_right()
        # We end up back at North
        self.assertEqual(self.robot.orientation, 'N')

    def test_bearing_manipulation(self):
        # Not that this should be done, but to test ...
        self.assertEqual(self.robot._bearing, 0)
        self.robot._bearing = 90
        self.assertEqual(self.robot.orientation, 'E')
        self.robot._bearing = 180
        self.assertEqual(self.robot.orientation, 'S')
        self.robot._bearing = 270
        self.assertEqual(self.robot.orientation, 'W')

    def test_broken_bearing(self):
        # This should certainly never happen
        self.robot._bearing = 45

        with self.assertRaises(AttributeError):
            self.robot.orientation


class TestRobotPosition(TestCase):

    def test_initial_position(self):
        self.robot = Robot(0, 0, 'N')
        self.assertEqual(self.robot.x_coord, 0)
        self.assertEqual(self.robot.y_coord, 0)

        self.robot = Robot(1, 1, 'N')
        self.assertEqual(self.robot.x_coord, 1)
        self.assertEqual(self.robot.y_coord, 1)

        self.robot = Robot(1, 2, 'N')
        self.assertEqual(self.robot.x_coord, 1)
        self.assertEqual(self.robot.y_coord, 2)

    def test_position_attribute(self):
        self.robot = Robot(0, 0, 'N')
        self.assertEqual(self.robot.position, (0, 0, 'N'))

        self.robot = Robot(1, 1, 'E')
        self.assertEqual(self.robot.position, (1, 1, 'E'))

        self.robot = Robot(1, 2, 'S')
        self.assertEqual(self.robot.position, (1, 2, 'S'))

    def test_move_north(self):
        self.robot = Robot(0, 0, 'N')

        # y coordinate should increase
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 1)
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 2)
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 3)

    def test_move_south(self):
        self.robot = Robot(0, 3, 'S')

        # y coordinate should increase
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 2)
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 1)
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, 0)

    def test_move_east(self):
        self.robot = Robot(0, 0, 'E')

        # y coordinate should increase
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 1)
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 2)
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 3)

    def test_move_west(self):
        self.robot = Robot(3, 0, 'W')

        # y coordinate should increase
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 2)
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 1)
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, 0)

    def test_robot_cares_not_for_boundaries(self):
        self.robot = Robot(0, 0, 'S')

        # robot can take negative values for coordinates
        self.robot.move_forward()
        self.assertEqual(self.robot.y_coord, -1)

        self.robot.rotate_right()
        self.robot.move_forward()
        self.assertEqual(self.robot.x_coord, -1)


class TestGridNavigator(TestCase):

    def test_navigator_setup(self):
        navigator = GridNavigator(1, 1)
        navigator.setup(0, 0, 'N')
        self.assertIsInstance(navigator.robot, Robot)
        self.assertEqual(navigator.robot.position, (0, 0, 'N'))

    def test_robot_follows_commands(self):
        navigator = GridNavigator(1, 1)
        navigator.setup(0, 0, 'N')
        result = navigator.navigate('F')
        # Moves forward 1 to new y position, is not LOST
        self.assertEqual(result, ((0, 1, 'N'), False))

        # Turn right (east) and move to new x coord, is not LOST
        result = navigator.navigate('RF')
        self.assertEqual(result, ((1, 1, 'E'), False))

    def test_max_boundary(self):
        navigator = GridNavigator(1, 1)
        navigator.setup(0, 0, 'N')
        result = navigator.navigate('FF')
        # Moves forward 1 to new y position, then gets LOST as it goes past 1
        self.assertEqual(result, ((0, 1, 'N'), True))

        navigator.setup(0, 0, 'E')
        result = navigator.navigate('FF')
        # Moves forward 1 to new x position, then gets LOST as it goes past 1
        self.assertEqual(result, ((1, 0, 'E'), True))

    def test_min_boundary(self):
        navigator = GridNavigator(1, 1)
        navigator.setup(0, 1, 'S')
        result = navigator.navigate('FF')
        # Moves forward 1 to new y position, then gets LOST as it goes negative
        self.assertEqual(result, ((0, 0, 'S'), True))

        navigator.setup(1, 0, 'W')
        result = navigator.navigate('FF')
        # Moves forward 1 to new x position, then gets LOST as it goes negative
        self.assertEqual(result, ((0, 0, 'W'), True))

    def test_lost_robot_scent(self):
        navigator = GridNavigator(1, 1)
        navigator.setup(0, 0, 'N')
        # First robot will get LOST as in above test
        navigator.navigate('FF')

        # Setup again, and test the same commands on a second robot
        navigator.setup(0, 0, 'N')
        result = navigator.navigate('FF')
        # Robot does not get LOST
        self.assertEqual(result, ((0, 1, 'N'), False))


class TestGivenExamples(TestCase):

    def setUp(self):
        self.navigator = GridNavigator(5, 3)

    def test_examples(self):
        self.navigator.setup(1, 1, 'E')
        result = self.navigator.navigate('RFRFRFRF')
        self.assertEqual(result, ((1, 1, 'E'), False))

        self.navigator.setup(3, 2, 'N')
        result = self.navigator.navigate('FRRFLLFFRRFLL')
        self.assertEqual(result, ((3, 3, 'N'), True))

        self.navigator.setup(0, 3, 'W')
        result = self.navigator.navigate('LLFFFLFLFL')
        self.assertEqual(result, ((2, 3, 'S'), False))
