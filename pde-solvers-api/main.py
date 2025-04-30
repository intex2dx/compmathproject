from fastapi import FastAPI
from fastapi.responses import JSONResponse
import numpy as np
from schemas import HeatEquationInput, Schrodinger2DInput
from solvers.heat_equation import solve_heat_equation
from solvers.schrodinger_2d import solve_2d_schrodinger
import plotly.graph_objects as go

app = FastAPI(title="PDE Solver API")

@app.post("/solve/heat-equation/")
async def solve_heat_eq(params: HeatEquationInput):
    u0 = np.array(params.initial_condition)
    solution = solve_heat_equation(
        alpha=params.alpha,
        length=params.length,
        nx=params.nx,
        nt=params.nt,
        dt=params.dt,
        initial_condition=u0,
        bc=params.boundary_conditions
    )
    return {"solution": solution.tolist()}

@app.post("/solve/schrodinger-2d/")
async def solve_schrodinger_2d(params: Schrodinger2DInput):
    E, psi, X, Y = solve_2d_schrodinger(
        R=params.radius,
        N=params.points
    )
    
    plots = []
    for i in range(3):
        fig = go.Figure(data=[go.Surface(z=psi[i], x=X, y=Y)])
        fig.update_layout(title=f"State {i+1} (E = {E[i]:.4f})")
        plots.append(fig.to_html(full_html=False))
    
    return {
        "energies": E.tolist(),
        "wavefunctions": plots
    }
