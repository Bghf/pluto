import unittest
from unittest import TestCase


class Rover:
  def __init__(self):
    self.x = 0
    self.y = 0

  def move_forward(self):
    self.y = self.y + 1

  def move_backward(self):
    self.y = self.y - 1

  def get_state(self):
    return [self.x, self.y]

class TestRover(TestCase) :
  def test_move_forward_increments_y(self):
    rover = Rover()
    rover.move_forward()
    self.assertEqual(rover.get_state() ,[0, 1])

  def test_move_backward_decrements_y(self):
      rover = Rover()
      rover.move_backward()
      self.assertEqual(rover.get_state() ,[0, -1])

if __name__ == '__main__':
    unittest.main()