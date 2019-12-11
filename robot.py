from typing import Tuple


class Robot:

    def __init__(self, x, y, orientation, lost_robot_positions: Tuple[int, int, str] = []):
        self._bearing = 0
        self.orientation = orientation
        self.x_coord = x
        self.y_coord = y
        self.lost_robot_positions = lost_robot_positions

    @property
    def orientation(self) -> str:
        # Convert internal '_bearing' into compass 'orientation'
        if self._bearing == 0:
            orientation = 'N'
        elif self._bearing == 90:
            orientation = 'E'
        elif self._bearing == 180:
            orientation = 'S'
        elif self._bearing == 270:
            orientation = 'W'
        else:
            raise AttributeError('Cannot determine orientation')

        return orientation

    @orientation.setter
    def orientation(self, val):
        if type(val) != str:
            raise TypeError('Orientation must be a string')

        # Convert compass heading into degrees
        if val == 'N':
            self._bearing = 0
        elif val == 'E':
            self._bearing = 90
        elif val == 'S':
            self._bearing = 180
        elif val == 'W':
            self._bearing = 270
        else:
            # Could support other orientations in the future, e.g. NW
            raise ValueError('Orientation must be one of N, S, E, or W')

    @property
    def position(self) -> Tuple[int, int, str]:
        return self.x_coord, self.y_coord, self.orientation

    def rotate_left(self) -> None:
        # reduce _bearing by 90 degrees, and modulo 360
        self._bearing -= 90
        self._bearing %= 360

    def rotate_right(self) -> None:
        # increase _bearing by 90 degrees, and modulo 360
        self._bearing += 90
        self._bearing %= 360

    def move_forward(self) -> None:
        if self.position in self.lost_robot_positions:
            # If x, y, and orientation are all the same as a lost robot, ignore
            return

        orientation = self.orientation
        if orientation == 'N':
            # Move up one
            self.y_coord += 1
        elif orientation == 'S':
            # Move down one
            self.y_coord -= 1
        elif orientation == 'E':
            # Move right one
            self.x_coord += 1
        elif orientation == 'W':
            # Move left one
            self.x_coord -= 1


class GridNavigator:

    def __init__(self, max_x: int, max_y: int):
        # Set up the max grid size
        if max_x > 50 or max_y > 50:
            raise ValueError('Maximum grid size is 50')

        self.max_x = max_x
        self.max_y = max_y

        # Default empty list of lost robot positions
        self.lost_robot_positions = []

    def setup(self, initial_x: int, initial_y: int, initial_orientation: str) -> None:
        # Create a robot with the specified initial position and orientation
        self.robot = Robot(initial_x, initial_y, initial_orientation, self.lost_robot_positions)

    def navigate(self, commands: str) -> Tuple[int, int, str, bool]:
        for command in commands:
            orig_x, orig_y, orig_orientation = self.robot.position

            if command == 'L':
                self.robot.rotate_left()
            elif command == 'R':
                self.robot.rotate_right()
            elif command == 'F':
                self.robot.move_forward()
            else:
                raise ValueError(f'Invalid command {command}')

            new_position = self.robot.position

            if new_position[0] > self.max_x or new_position[1] > self.max_y or \
                    new_position[0] < 0 or new_position[1] < 0:
                # New position is outside the specified grid
                # Record the position it was lost out, and return early
                lost_at = (orig_x, orig_y, orig_orientation)
                self.lost_robot_positions.append(lost_at)
                return lost_at, True

        return new_position, False


def main():
    size = input('Initial grid size (x y): ')
    x, y = size.split(' ')
    navigator = GridNavigator(int(x), int(y))

    while True:
        try:
            initial = input('Initial position and orientation (x y O): ')
            if initial == '':
                break
            x, y, orient = initial.split(' ')
            navigator.setup(int(x), int(y), orient)
            position, lost = navigator.navigate(input('Commands: '))
            print(*position, 'LOST' if lost else '')
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
