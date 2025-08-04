"""
This is a MCP server implementation for hexadecimal and binary conversions.
"""

from mcp.server.fastmcp import FastMCP

# create MCP server
mcp = FastMCP(
  name = "Data conversion MCP Server"
)

@mcp.tool()
def DecToHex(DecValue: int) -> str:
  """
  convert decimal value to hexadecimal value
  """
  return_hex_string = ""
  try:
    return_hex_string = str(hex(DecValue))  #convert decimal value to hexadecimal value
  except Exception as err:
    return_hex_string = "processed failed:" + str(err)
  return return_hex_string

@mcp.tool()
def DecToBin(DecValue: int) -> str:
  """
  convert decimal value to binary value
  """
  return_bin_string = ""
  try:
    return_bin_string = str(bin(DecValue))  #convert decimal value to binary value
  except Exception as err:
    return_bin_string = "processed failed:" + str(err)
  return return_bin_string

@mcp.tool()
def BinShiftLeft(BinValue: str) -> str:
  """
  shift binary value to the left one bit position
  """
  return_shiftleft_string = ""
  try:
    int_value = int(BinValue, base=2)  #convert binary value to int value
    #determine bit width
    bit_width = 0
    if int_value < 0:
      return_shiftleft_string = "Only non-negative values are supported"
      return return_shiftleft_string
    elif int_value < 2**4:
      bit_width = 4
    elif int_value < 2**8:
      bit_width = 8
    elif int_value < 2**16:
      bit_width = 16
    else:
      return_shiftleft_string = "Unsupported bit width"
      return return_shiftleft_string
    shift_value1 = int_value << 1  #shift left by one bit
    shift_value_bitwidth = 1 << bit_width  #shift left by bit width
    shift_value = shift_value1 & (shift_value_bitwidth - 1)  #mask to bit width
    format_value = format(shift_value, f"0{bit_width}b")  #format to bit width
    return_shiftleft_string = format_value
  except Exception as err:
    return_shiftleft_string = "processed failed:" + str(err)
  return return_shiftleft_string

@mcp.tool()
def BinShiftRight(BinValue: str) -> str:
  """
  shift binary value to the right one bit position
  """
  return_shiftright_string = ""
  try:
    int_value = int(BinValue, base=2)  #convert binary value to int value
    #determine bit width
    bit_width = 0
    if int_value < 0:
      return_shiftright_string = "Only non-negative values are supported"
      return return_shiftright_string
    elif int_value < 2**4:
      bit_width = 4
    elif int_value < 2**8:
      bit_width = 8
    elif int_value < 2**16:
      bit_width = 16
    else:
      return_shiftright_string = "Unsupported bit width"
      return return_shiftright_string
    shift_value = int_value >> 1  #shift right by one bit
    format_value = format(shift_value, f"0{bit_width}b")  #format to bit width
    return_shiftright_string = format_value
  except Exception as err:
    return_shiftright_string = "processed failed:" + str(err)
  return return_shiftright_string

if __name__ == "__main__":
  mcp.run()  #start MCP server