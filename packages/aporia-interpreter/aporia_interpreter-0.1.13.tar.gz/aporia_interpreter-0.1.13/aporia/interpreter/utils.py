from functools import singledispatch
from unittest import case

from aporia.aporia_ast import *

# apply functions type check and execute operands

# unary
def apply_not(value):
  if isinstance(value, bool):
    return not value
  else:
    raise Exception("Apply Not: Expected boolean type got value:", value)

def apply_negation(value):
  if isinstance(value, (int, float)):
    return - value
  else:
    raise Exception("Apply Negation: Expected int or float type got value:", value)

# Bool BinOp
def apply_and(left, right):
  if isinstance(left, bool) and isinstance(right, bool):
    return left and right
  else:
    raise Exception("Apply And: Expected bool type got values:", left, right)

def apply_or(left, right):
  if isinstance(left, bool) and isinstance(right, bool):
    return left or right
  else:
    raise Exception("Apply Or: Expected bool type got values:", left, right)

# Number BinOp
def apply_add(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left + right
  else:
    raise Exception("Apply Add: Expected int or float type got values:", left, right)

def apply_sub(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left - right
  else:
    raise Exception("Apply Sub: Expected int or float type got values:", left, right)

def apply_mult(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left * right
  else:
    raise Exception("Apply Mult: Expected int or float type got values:", left, right)

def apply_div(left, right):
  ops = (left, right)
  if not all(isinstance(op, (float, int)) for op in ops):
    raise Exception("Apply Div: Expected int or float type got values:", left, right)
  if right == 0:
    raise Exception("Divide by 0 Error.")
  return left / right if any(isinstance(op, float) for op in ops) else left // right

def apply_floor_div(left, right):
  ops = (left, right)
  if not all(isinstance(op, (float, int)) for op in ops):
    raise Exception("Apply Div: Expected int or float type got values:", left, right)
  if right == 0:
    raise Exception("Divide by 0 Error.")
  return left // right

def apply_mod(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    if right == 0:
      raise Exception("Divide by 0 Error.")
    return left % right
  else:
    raise Exception("Apply Mod: Expected int or float type got values:", left, right)

# comparisons
def compare_eq(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left == right
  else:
    raise Exception("Compare Eq: Expected int or float type got values:", left, right)

def compare_neg(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left != right
  else:
    raise Exception("Compare Eq: Expected int or float type got values:", left, right)

def compare_ge(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left >= right
  else:
    raise Exception("Compare Ge: Expected int or float type got values:", left, right)

def compare_gt(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left > right
  else:
    raise Exception("Compare Gt: Expected int or float type got values:", left, right)

def compare_le(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left <= right
  else:
    raise Exception("Compare Le: Expected int or float type got values:", left, right)

def compare_lt(left, right):
  if isinstance(left, (int, float)) and isinstance(right, (int, float)):
    return left < right
  else:
    raise Exception("Compare Lt: Expected int or float type got values:", left, right)

#print formating
@singledispatch
def format_for_print(value):
  raise NotImplementedError("Unsupported types")

@format_for_print.register
def _(value: bool):
  return str(value).lower()

@format_for_print.register
def _(value: int):
  return str(value)

@format_for_print.register
def _(value: float):
  return str(value)

#assignments
def format_for_assign(to_type, value):
  # match on variable type
  match to_type:
    case Bool():
      match value:
        case bool():
          return value
        case int() | float():
          return value % 2 != 0

    case Float():
      return value
    case Int():
      return int(value)

  raise Exception(f"Variable assignment not allowed: Trying to assign value {value} to type {to_type}.")
