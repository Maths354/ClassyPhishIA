from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

class Graph:

    def __init__(self):
        pass

    def grt(self):
        fig = Figure()

        x = np.array(["A", "B", "C", "D"])
        y = np.array([3, 8, 1, 10])
    
        ax = fig.subplots()
        ax.bar(x, y)
        
        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
    
    