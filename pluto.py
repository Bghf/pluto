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
  def __init__(self):
    self.x = 0
    self.y = 0
    self.direction = Direction.NORTH


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


  def _move(self, inc):
    if self.direction == Direction.NORTH:
      self.y = self.y + inc
    elif self.direction == Direction.EAST:
      self.x = self.x + inc
    elif self.direction == Direction.SOUTH:
      self.y = self.y - inc
    elif self.direction == Direction.WEST:
      self.x = self.x - inc

  def _turn(self, degree):
    if degree == 90:
      self.direction = Direction.next_clockwise(self.direction)
    elif degree == -90:
      self.direction = Direction.next_anticlockwise(self.direction)  

  def get_state(self):
    return [self.x, self.y, self.direction]
      

    
class TestRover(TestCase) :
  def test_move_forward_increments_y(self):
    rover = Rover()
    rover.execute('F')
    self.assertEqual(rover.get_state(), [0, 1, 0])

  def test_move_backward_decrements_y(self):
    rover = Rover()
    rover.execute('B')
    self.assertEqual(rover.get_state(), [0, -1, 0])

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

if __name__ == '__main__':
    unittest.main()