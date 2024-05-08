from flask import Flask

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()

    # Data used on graph
    x = np.array(["A", "B", "C", "D"])
    y = np.array([3, 8, 1, 10])
  
    ax = fig.subplots()
    ax.bar(x, y)
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
