PIDRegulator:

- init(Kp, Ki, Kd):

  - Kp = Kp
  - Ki = Ki
  - Kd = Kd
  - prev_error = 0
  - integral = 0

- beregn_effekt(self, setpoint, feedback, dt):
  - error = setpoint - feedback
  - self.integral = error \* dt
  - derivative = (error - self.prev_error) / dt
  - control*output = Kp * error + Ki \_ integral + Kd \* derivative
  - self.prev_error = error
  - return control_output

Room:

- init(dimentions:list[float], start_temp, outside_temp, prefered_temp, heat_transfer_coefficient=0.5)

  - air_density
  - heat_transfer_coefficient
  - temperature = start_temp
  - outside_temp = outside_temp
  - prefered_temp = prefered_temp

- volume():

  - return Π (dimentions)

- area():

  - a, b, c = self.dim
  - return 2ab + 2ac + 2bc

- mass():
  - return volume() \* air_density

Heater:

- init(min_power, max_power):

  - min_power
  - max_power
  - current_power

- set_power(wattage):
  - current_power = wattage
  - has to be in the range [min power - max power]

System:

- init():
  - regulator = Regulator()
  - heater = Heater(0, 1000)
  - room = Room([5, 6, 1], 10, 4, 20)

Simulator(System):

- init()
  pass

- tidsstegsim(dt):
  pass

- sim(total_tid, dt)
  - tid = 0
  - do:
    - tidsstegsim(dt)
  - while tid < total_tid
