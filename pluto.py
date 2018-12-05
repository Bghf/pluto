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

  def move_forward(self):
    if self.direction == Direction.NORTH:
        self.y = self.y + 1
    elif self.direction == Direction.EAST:
        self.x = self.x + 1
    elif self.direction == Direction.SOUTH:
        self.y = self.y - 1
    elif self.direction == Direction.WEST:
        self.x = self.x - 1

  def move_backward(self):
    if self.direction == Direction.NORTH:
        self.y = self.y - 1
    elif self.direction == Direction.EAST:
        self.x = self.x - 1
    elif self.direction == Direction.SOUTH:
        self.y = self.y + 1
    elif self.direction == Direction.WEST:
        self.x = self.x + 1

  def get_state(self):
    return [self.x, self.y, self.direction]

  def turn_clockwise(self):
    self.direction = Direction.next_clockwise(self.direction)

  def turn_anticlockwise(self):
    self.direction = Direction.next_anticlockwise(self.direction)        

    
class TestRover(TestCase) :
  def test_move_forward_increments_y(self):
    rover = Rover()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[0, 1, 0])

  def test_move_backward_decrements_y(self):
    rover = Rover()
    rover.move_backward()
    self.assertEqual(rover.get_state() ,[0, -1, 0])

  def test_turns_clockwise_correctly(self):
    rover = Rover()
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover.turn_clockwise()
    self.assertEqual(rover.get_state(), [0, 0, 1])
    rover.turn_clockwise()
    self.assertEqual(rover.get_state(), [0, 0, 2])
    rover.turn_clockwise()
    self.assertEqual(rover.get_state(), [0, 0, 3])
    rover.turn_clockwise()
    self.assertEqual(rover.get_state(), [0, 0, 0])


  def test_turns_anticlockwise_correctly(self):
    rover = Rover()
    self.assertEqual(rover.get_state(), [0, 0, 0])
    rover.turn_anticlockwise()
    self.assertEqual(rover.get_state(), [0, 0, 3])
    rover.turn_anticlockwise()
    self.assertEqual(rover.get_state(), [0, 0, 2])
    rover.turn_anticlockwise()
    self.assertEqual(rover.get_state(), [0, 0, 1])
    rover.turn_anticlockwise()
    self.assertEqual(rover.get_state(), [0, 0, 0])
  
  def test_moves_in_the_right_direction(self):
    rover = Rover()
    rover.move_forward()
    rover.move_forward()
    rover.turn_clockwise()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[1, 2, 1])
    rover.turn_clockwise()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[1, 1, 2])
    rover.turn_clockwise()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[0, 1, 3])
    rover.turn_clockwise()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[0, 2, 0])


if __name__ == '__main__':
    unittest.main()