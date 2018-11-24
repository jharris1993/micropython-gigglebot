import time
import microbit

N = 10000

# read the button n times
def read_button(n):
        is_pressed = microbit.button_a.is_pressed
        for i in range(n/10):
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()
                is_pressed()

def time_it(f, n):
        t0 = time.ticks_us()
        f(n)
        t1 = time.ticks_us()
        dt = time.ticks_diff(t1, t0)
        fmt = '{:5.3f} sec, {:6.3} usec/button : {:8.2f} kbuttons/sec'
        print(fmt.format(dt * 1e-6, dt / n, n / dt * 1e3))

def call_it():
        time_it(read_button, N)

# call_it()