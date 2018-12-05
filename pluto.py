import unittest
from unittest import TestCase


class Direction:
  NORTH = 0
  EAST = 1
  SOUTH = 2
  WEST = 3

  @staticmethod
  def next_clockwise(direction):
      return (direction + 1) % 4        

  @staticmethod
  def next_anticlockwise(direction):
      return Direction.WEST if direction == Direction.NORTH else (direction - 1) % 4


class Rover:
  def __init__(self, xlimit=100, ylimit=100, obstacles={}):
    self.x = 0
    self.y = 0
    self.direction = Direction.NORTH
    self.xlimit = xlimit
    self.ylimit = ylimit
    self.obstacles = obstacles

  def get_state(self):
    return [self.x, self.y, self.direction]

  def execute(self, cmds):
    for cmd in cmds:
      if cmd == 'F':
        self._move(1)
      elif cmd == 'B':
        self._move(-1)
      elif cmd == 'L':
        self._turn(-90)
      elif cmd == 'R':
        self._turn(90)

  def _reform_bounds(self):
    self.x = self.x % self.xlimit
    self.y = self.y % self.ylimit

  def _move(self, inc):
    prevX = self.x
    prevY = self.y
    if self.direction == Direction.NORTH:
      self.y = self.y + inc
    elif self.direction == Direction.EAST:
      self.x = self.x + inc
    elif self.direction == Direction.SOUTH:
      self.y = self.y - inc
    elif self.direction == Direction.WEST:
      self.x = self.x - inc
    self._reform_bounds()
    # this will not work for incs other than 1, we would need to search all the map
    if (self.x, self.y) in self.obstacles: 
      self.x = prevX
      self.y = prevY

  def _turn(self, degree):
    # todo add other angles for completeness
    if degree == 90:
      self.direction = Direction.next_clockwise(self.direction)
    elif degree == -90:
      self.direction = Direction.next_anticlockwise(self.direction)  


class TestRover(TestCase) :
  def test_move_forward_increments_y(self):
    rover = Rover()
    rover.execute('F')
    self.assertEqual(rover.get_state(), [0, 1, 0])

  def test_move_backward_decrements_y(self):
    rover = Rover()
    rover.execute('F')
    self.assertEqual(rover.get_state(), [0, 1, 0])
    rover.execute('B')
    self.assertEqual(rover.get_state(), [0, 0, 0])

  def test_executes_multiple_commands(self):
    rover = Rover()
    rover.execute('FFFFB')
    self.assertEqual(rover.get_state() ,[0, 3, 0])

  def test_turns_clockwise_correctly(self):
    rover = Rover()
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover.execute('R')
    self.assertEqual(rover.get_state(), [0, 0, 1])
    rover.execute('R')
    self.assertEqual(rover.get_state(), [0, 0, 2])
    rover.execute('R')
    self.assertEqual(rover.get_state(), [0, 0, 3])
    rover.execute('R')
    self.assertEqual(rover.get_state(), [0, 0, 0])

  def test_turns_anticlockwise_correctly(self):
    rover = Rover()
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover.execute('L')
    self.assertEqual(rover.get_state(), [0, 0, 3])
    rover.execute('L')
    self.assertEqual(rover.get_state(), [0, 0, 2])
    rover.execute('L')
    self.assertEqual(rover.get_state(), [0, 0, 1])
    rover.execute('L')
    self.assertEqual(rover.get_state(), [0, 0, 0])
  
  def test_moves_in_the_right_direction(self):
    rover = Rover()
    rover.execute('FFRF')
    self.assertEqual(rover.get_state(), [1, 2, 1])
    rover.execute('RF')
    self.assertEqual(rover.get_state(), [1, 1, 2])
    rover.execute('RF')
    self.assertEqual(rover.get_state(), [0, 1, 3])
    rover.execute('RF')
    self.assertEqual(rover.get_state(), [0, 2, 0])

  def test_wraps_edges_around_y(self):
    rover = Rover(10, 50)
    rover.execute('F' * 49)
    self.assertEqual(rover.get_state(), [0, 49, 0])
    rover.execute('F')
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover = Rover(10, 50)
    rover.execute('F' * 101)
    self.assertEqual(rover.get_state(), [0, 1, 0])

  def test_wraps_edges_around_y2(self):
    rover = Rover(10, 50)
    rover.execute('B' * 101)
    self.assertEqual(rover.get_state(), [0, 49, 0])

  def test_wraps_edges_around_x(self):
    rover = Rover(10, 50)
    rover.execute('R' + 'F' * 9)
    self.assertEqual(rover.get_state(), [9, 0, 1])
    rover.execute('F')
    self.assertEqual(rover.get_state(), [0, 0, 1])

  def test_wraps_edges_around_x2(self):
    rover = Rover(10, 50)
    rover.execute('L' + 'B' * 24)
    self.assertEqual(rover.get_state(), [4, 0, 3])

  def test_wrap_at_0(self):
    rover = Rover()
    rover.execute('BF')
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover.execute('FFBB')
    self.assertEqual(rover.get_state(), [0, 0, 0])

  def test_doesnt_move_if_hits_obstacle(self):
    rover = Rover(10, 10, {(1,2)})
    rover.execute("FFR")
    self.assertEqual(rover.get_state(), [0, 2, 1])
    rover.execute("F")
    self.assertEqual(rover.get_state(), [0, 2, 1])

  def test_doesnt_move_through_obstacles(self):
    rover = Rover(10, 10, {(1,2)})
    rover.execute("RF")
    self.assertEqual(rover.get_state(), [1, 0, 1])
    rover.execute("LFFFFFFFFF")
    self.assertEqual(rover.get_state(), [1, 1, 0])

if __name__ == '__main__':
    unittest.main()