from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

class Graph:

    def __init__(self,y_tab=[0,0,0,0]):
        assert isinstance(y_tab,list)
        self.y_tab=y_tab
        self.x_tab=["URL","Certificat","Logo","Mot-clé"]

    def grt(self):
        fig = Figure()

        x = np.array(self.x_tab)
        y = np.array(self.y_tab)
    
        ax = fig.subplots()
        ax.bar(x, y)
        
        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
    
    
