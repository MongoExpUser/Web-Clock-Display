# ****************************************************************************************************************************
# ****************************************************************************************************************************
# * @License Starts
# *
# * Copyright © 2015 - present. MongoExpUser
# *
# * License: BSD - https://github.com/MongoExpUser/Web-Clock-Display/blob/master/LICENSE
# *
# * @License Ends
# *
# *
# * ...Ecotert's web_clock_display.py  (released as open-source under BSD 3-Clause "New" or "Revised" License) implements:
#
#  Clock (time) display for the web.
#
#  Clock could be a web site or wall clock, car dashboard clock, appliances dashboard clock,  etc., 
#  but they are all displayed via web request made to server before they are display on the web site, 
#  wall, dashboard, appliances, etc,
#
#  Codes below are modified/adapted from codes  ("""Code for the clock""") on: view-source:https://brython.info/             
#                                                                                                                           
#  This implementation generalises original codes to any type of clock using "Factory" Design Pattern.                       
#                                                                                                                           
#  Licensed: BSD 3-Clause "New" or "Revised" License. See: https://spdx.org/licenses/BSD-3-Clause.html                      
#
#
# ****************************************************************************************************************************
# ****************************************************************************************************************************


# 1. import statements
try:
  from math import sin, cos, pi
  from datetime import datetime, timedelta
  from browser import timer, document, window
  from abc import (ABCMeta, abstractmethod, abstractproperty)
except(ImportError) as err:
  print(str(err))
  return
#=============================================================================================================================

#=============================================================================================================================
# 2. class-1
class TimeDisplay(object, metaclass=ABCMeta):
  """
      Abstract base class interface for making time display (analog or digital)
      Analog or digital time could be: web site or wall clock, car dashboard clock, appliances dashboard clock, etc.)
  """
  # A. class constructor
  @abstractmethod
  def __init__(self, width=None, height=None, ray=None, west_coast_difference=None, east_coast_difference=None):
    raise NotImplementedError('User must define variables and implement methods to use this base class')
  
  # B. class methods
  @abstractmethod
  def needle(self, angle, r1, r2, width, height, ray, ctx, color="#000000"):
    raise NotImplementedError('User must implement "needle" method before it can be invoked')

  @abstractmethod
  def set_clock(self, width, height, ray, canvas, ctx, clock_id):
    raise NotImplementedError('User must implement "needle" method before it can be invoked')

  @abstractmethod
  def show_hours(self, width, height, ray, canvas, ctx):
    raise NotImplementedError('User must implement "set_clock" method before it can be invoked')
    
  def draw_border_set_clock_and_show_hours(self, width, height, ray, canvas, ctx, clock_id):
    raise NotImplementedError('User must implement "add_clock_onto_canvas" method before it can be invoked')
   
  @abstractmethod
  def load_clock(self, clock_id):
    raise NotImplementedError('User must implement "load_clock" method before it can be invoked')
 
  @abstractmethod
  def invoke_clock(self, option=False):
    raise NotImplementedError('User must implement "invoke_clock" method before it can be invoked')
  
  @abstractmethod
  def test_clock(self):
    raise NotImplementedError('User must implement "test_clock" method before it can be invoked')
#=============================================================================================================================

#=============================================================================================================================
# 3. class-2
class AnalogWebClock(object, TimeDisplay):
  """ Make analog clock for display on a web browser using Brython.
      Brython is A Python 3 implementation for client-side web programming.
  """
  # A. class constructor
  def __init__(self, width=None, height=None, ray=None, west_coast_difference=None, east_coast_difference=None):
    # class variables
    # 1. canvas dimensions
    self.width  = width
    self.height = height
    # 2. clock ray
    self.ray = ray
    # 3. others
    self.border_color = "#333"
    self.background_color = "#111"
    self.digits_color_1 = "#fff"
    self.digits_color_2 = "#000"
    self.west_coast_difference = west_coast_difference
    self.east_coast_difference = east_coast_difference
    
  # B. class methods
  def needle(self, angle, r1, r2, width, height, ray, ctx, color="#000000"):
    """Draw a needle at specified angle in specified color. r1 and r2 are percentages of clock ray. """
    x1 = width / 2 - ray * cos(angle) * r1
    y1 = height / 2 - ray * sin(angle) * r1
    x2 = width / 2 + ray * cos(angle) * r2
    y2 = height / 2 + ray * sin(angle) * r2
    ctx.beginPath()
    ctx.strokeStyle = self.digits_color_1
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()

  def set_clock(self, width, height, ray, canvas, ctx, clock_id):
    # erase clock
    ctx.beginPath()
    ctx.fillStyle = self.background_color
    ctx.arc(width / 2, height / 2, ray * 0.89, 0, 2 * pi)
    ctx.fill()
  
    # redraw hours
    self.show_hours(width, height, ray, canvas, ctx)
              
    # print day
      # a. get time now depending on location
    if clock_id == "gmt_clock":
      #utc/gmt same time
      now = datetime.utcnow()
    if clock_id == "us_west_coast_clock":
      # US west coast time (pacific time)
      now = datetime.utcnow() + timedelta(hours=self.west_coast_difference)
    if clock_id == "us_east_coast_clock":
      # US east coast time (eastern time)
      now = datetime.utcnow() + timedelta(hours=self.east_coast_difference)
      # b. then get the "day" from time now
    day = now.day
      
    #set clock other properties
    ctx.font = "bold 14px Arial"
    ctx.textAlign = "center"
    ctx.textBaseline = "middle"
    ctx.fillStyle = self.digits_color_2
    ctx.fillText(day, width * 0.7, height * 0.5)
  
    # draw needles for hour, minute, seconds
    ctx.lineWidth = 2
    hour = now.hour % 12 + now.minute / 60
    angle = hour * 2 * pi / 12 - pi / 2
    self.needle(angle, 0.05, 0.5, width, height, ray, ctx, color="#000000")
    minute = now.minute
    angle = minute * 2 *pi / 60 - pi / 2
    self.needle(angle, 0.05, 0.85, width, height, ray, ctx, color="#000000")
    ctx.lineWidth = 1
    second = now.second + now.microsecond / 1000000
    angle = second * 2 * pi / 60 - pi / 2
    self.needle(angle, 0.05, 0.85, width, height, ray, ctx, color="#FF0000") # red color

  def show_hours(self, width, height, ray, canvas, ctx):
    ctx.beginPath()
    ctx.arc(width / 2, height / 2, ray * 0.05, 0, 2 * pi)
    ctx.fillStyle = self.digits_color_1
    ctx.fill()
    for i in range(1, 13):
      angle = i * pi / 6 - pi / 2
      x3 = width / 2 + ray * cos(angle) * 0.75
      y3 = height / 2 + ray * sin(angle) * 0.75
      ctx.font = "18px Arial"
      ctx.textAlign = "center"
      ctx.textBaseline = "middle"
      ctx.fillText(i, x3, y3)
    # cell for day
    ctx.fillStyle = self.digits_color_1
    ctx.fillRect(width * 0.65, height * 0.47, width * 0.1, height * 0.06)
    
  def draw_border_set_clock_and_show_hours(self, width, height, ray, canvas, ctx, clock_id):
      if hasattr(canvas, 'getContext'):
        ctx = canvas.getContext("2d")
        ctx.beginPath()
        ctx.arc(width / 2, height / 2, ray, 0, 2 * pi)
        ctx.fillStyle = self.background_color
        ctx.fill()
        ctx.beginPath()
        ctx.lineWidth = 6
        ctx.arc(width / 2,height / 2, ray + 3, 0, 2 * pi)
        ctx.strokeStyle = self.border_color
        ctx.stroke()
    
        for i in range(60):
          ctx.lineWidth = 1
          if i%5 == 0:
            ctx.lineWidth = 3
          angle = i * 2 * pi / 60 - pi / 3
          x1 = width / 2 + ray * cos(angle)
          y1 = height / 2 + ray * sin(angle)
          x2 = width / 2 + ray * cos(angle) * 0.9
          y2 = height / 2 + ray * sin(angle) * 0.9
          ctx.beginPath()
          ctx.strokeStyle = self.digits_color_1
          ctx.moveTo(x1, y1)
          ctx.lineTo(x2, y2)
          ctx.stroke()
          
        timer.set_interval(lambda: self.set_clock(width, height, ray, canvas, ctx, clock_id), 100)
        self.show_hours(width, height, ray, canvas, ctx)
      else:
        document['navig_zone'].html = "On Internet Explorer 9 or more, use a Standard rendering engine"
    
  def load_clock(self, clock_id):
    """ finally make the whole analog clock """
    width  = self.width
    height = self.height
    ray = self.ray
    canvas = document[clock_id]
    ctx = canvas.getContext("2d")
    self.draw_border_set_clock_and_show_hours(width, height, ray, canvas, ctx, clock_id)

  def invoke_clock(self, option=False):
    """ invoke methods and make clock_ids available as canvas element ids on the DOM """
    from browser import document, window
    # option 1: as window object-> available to JavaScript (JS) programs on the browser as DOM Object
    # ensure no names collison or conflict with names defined in a JS program or library on the web page
    # load_clock_1, _2 & _3 are attributes of the object window in the module "browser" & can be accessed on the browser DOM
    # Ref: http://brython.info/static_doc/en/jsobjects.html
    if option:
      window.load_clock_1 = self.load_clock("us_west_coast_clock")
      window.load_clock_2 = self.load_clock("gmt_clock")
      window.load_clock_3 = self.load_clock("us_east_coast_clock")
    # option 2: binding to document ids
    # Ref: http://brython.info/static_doc/en/jsobjects.html
    else:
      window.load_clock_1 = document["us_west_coast_clock"].bind("click", self.load_clock("us_west_coast_clock"))
      window.load_clock_2 = document["gmt_clock"].bind("click", self.load_clock("gmt_clock"))
      window.load_clock_3 = document["us_east_coast_clock"].bind("click", self.load_clock("us_east_coast_clock"))

  def test_clock(self):
    """ simple unit test """
    try:
      # 1. invoke Clock class within itself
      analog_web_clock = AnalogWebClock
      # 2. then assert for instance
      assert(issubclass(analog_web_clock, (object, ABCMeta, TimeDisplay)))
    except(AssertionError, TypeError):
      print("AnalogClock is NOT a sub-class of object or ABCMeta or TimeDisplay, or all.")
    else:
      print("YES, AnalogClock is a sub-class of object, ABCMeta and TimeDisplay.")
      return True
#=============================================================================================================================
  
#=============================================================================================================================
# 4. invocations
analog_web_clock = AnalogWebClock(width=250, height=250, ray=100, west_coast_difference=-7, east_coast_difference=-4)
test = analog_web_clock.test_clock()
if test:
  analog_web_clock.invoke_clock(option=True)
#=============================================================================================================================
