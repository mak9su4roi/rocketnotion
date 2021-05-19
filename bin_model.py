class MyModel:
  def __init__(self, arg):
    self.parameter = arg
    self.debug = False

  def start_debug(self):
    self.debug = True

  def predict(self, data):
    predicted = []
    for custom in data:
      contours = [(ind%28, ind//28) for ind, elm in enumerate(custom) if elm]
      y_max = max(contours, key=lambda dot: dot[1])[1]
      y_min = min(contours, key=lambda dot: dot[1])[1]
      y_mid = (y_max+y_min)//2

      width = []

      for ind in range(y_min, y_max+1):
        new_contours = list(filter(lambda x: x[1] == ind, contours))
        if not new_contours:
          continue

        x_max = max(new_contours, key=lambda dot: dot[0])[0]
        x_min = min(new_contours, key=lambda dot: dot[0])[0]

        width += [x_max - x_min]

      if self.debug:
        print(f"center: {y_mid-1}, width: {width}")
      predicted += [1 if max(width) < self.parameter else 0]
    return predicted
