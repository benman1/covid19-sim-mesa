# COVID-19 multi-agent simulation using Mesa

This is a simplistic multi-agent simulation of how COVID-19 can spread.<br>
<br>
`run.py`: Example python module for running the simulation. The simulation settings can be changed here.<br>
`server.py`: Visualization module that uses a web browser for visualizing the simulation. Running this will display the simulation grid and a chart of results that can be stepped through or run continuously.<br>
<br>
`model.py`: The simulation model.<br>
`person.py`: Agent model that represents one person.<br>
<br>

This was adapted from a simulation created by Maple Rain Research Co., Ltd.<br>

We've introduced hospitalization, hospital capacity, and lockdown policies.<br>

Some additional information on the original simulation can be found [here](https://teck78.blogspot.com/2020/04/using-mesa-framework-to-simulate-spread.html) here.<br>
<br>
This simulation uses the [Mesa](https://github.com/projectmesa/mesa) Mesa framework.