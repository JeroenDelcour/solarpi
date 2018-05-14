# coding: utf-8
import pandas as pd
from struct import iter_unpack
from asciiplot import ap
from read import read

battery = [[datetime, voltage, current] for datetime, voltage, current in read('data/battery.data', last_days=1)]

p = ap.AFigure()
print(p.plot(range(len(battery)), [b[1] for b in battery]))
