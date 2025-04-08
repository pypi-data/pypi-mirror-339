"""
widgets.py

Interactive visualization module for maglev simulation using Jupyter widgets.

Provides slider controls for PD gains (Kp, Kd) and plots:
- x and z position over time
- Phase plot of x vs theta

Users can optionally pass in custom simulation parameters and initial state.
"""

from typing import Callable, Optional, Dict, List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Ellipse
import warnings
import contextlib
import io
import sys
import os
import traceback
from ipywidgets import interact, FloatSlider, Button, Output, VBox, HTML, HBox
from IPython.display import display, Javascript, HTML as IPythonHTML
from ipysim.core import simulate_maglev
from ipysim.params import params as default_params, state0 as default_state0

# Globals for external use
t = None
sol = None
Kp = None
Kd = None
last_valid_Kp = None
last_valid_Kd = None

# Context manager to redirect stderr to browser console
@contextlib.contextmanager
def redirect_stderr_to_console():
    """
    Context manager to redirect stderr output to the browser's JavaScript console.
    
    This captures ipywidgets warnings and errors and displays them in the browser console
    instead of in the notebook output.
    """
    # Create a StringIO object to capture stderr
    stderr_capture = io.StringIO()
    
    # Save the original stderr
    old_stderr = sys.stderr
    
    try:
        # Redirect stderr to our capture object
        sys.stderr = stderr_capture
        yield  # Execute the code block inside the with statement
    finally:
        # Get the captured content
        stderr_content = stderr_capture.getvalue()
        
        # Restore the original stderr
        sys.stderr = old_stderr
        
        # If there's content, display it in the browser console
        if stderr_content:
            # Escape quotes and newlines for JavaScript
            stderr_content = stderr_content.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
            # Send to browser console wrapped in a try-catch to prevent errors
            js_code = f"""
            try {{
                console.error('[IPySim error message]: ' + '{stderr_content}');
            }} catch(e) {{
                console.error('Logging failed')
            }}
            """
            try:
                display(Javascript(js_code))
            except:
                pass

def interactive_simulation(
    params: Optional[Dict[str, float]] = None,
    state0: Optional[List[float]] = None,
    T: float = 1.0,
    dt: float = 0.001,
    Kp_default: float = 600.0,
    Kd_default: float = 30.0,
    Kp_min: float = 20.0,  
    Kd_min: float = 10.0,
    evaluation_function: Callable[[np.ndarray, np.ndarray], bool] | None = None,
    sliders_config: Optional[Dict[str, Dict[str, any]]] = None,
) -> None:
    """
    Create an interactive simulation for the maglev system using Jupyter widgets.

    Args:
        # ... existing parameters ...
        sliders_config: Dictionary defining custom sliders. Format:
            {
                "param_name": {
                    "default": default_value,
                    "min": min_value,
                    "max": max_value,
                    "step": step_size,
                    "description": "Label text"
                }
            }
            If None, defaults to Kp and Kd sliders only.
    """
    global t, sol, last_valid_Kp, last_valid_Kd
    params = params or default_params
    state0 = state0 or default_state0
    
    # Initialize last valid values with defaults
    last_valid_Kp = max(Kp_default, Kp_min)
    last_valid_Kd = max(Kd_default, Kd_min)

    # Define default sliders if no config provided
    if sliders_config is None:
        sliders_config = {
            "Kp": {
                "default": max(Kp_default, Kp_min),
                "min": Kp_min,
                "max": 1000,
                "step": 10.0,
                "description": "Kp"
            },
            "Kd": {
                "default": max(Kd_default, Kd_min),
                "min": Kd_min,
                "max": 200,
                "step": 5.0,
                "description": "Kd"
            }
        }

    # Create outputs for visualization
    out = Output()
    animation_out = Output()
    result_output = Output()

    def validate_parameters(Kp: float, Kd: float) -> bool:
        """Validate controller parameters to prevent computation errors."""
        if Kp < Kp_min:
            return False
        if Kd < Kd_min:
            return False
        return True

    def is_valid_solution(solution: np.ndarray) -> bool:
        """Check if the solution is valid and doesn't contain extreme values."""
        if solution is None or solution.size == 0:
            return False
            
        # Check for NaN or Inf values
        if np.isnan(solution).any() or np.isinf(solution).any():
            return False
            
        # Check for extreme values that might cause overflow
        max_abs_value = np.max(np.abs(solution))
        if max_abs_value > 1e10:  # If any value is extremely large
            return False
            
        return True

    def create_maglev_animation(t, sol):
        """
        Create an interactive animation of the maglev system using matplotlib's FuncAnimation.
        
        Args:
            t: Time array
            sol: Solution array containing state variables
            
        Returns:
            IPythonHTML: Interactive HTML animation
        """
        try:
            # Cap the maximum number of frames to 500 for faster animation
            max_frames = 500
            if len(t) > max_frames:
                frame_step = len(t) // max_frames
                t_anim = t[::frame_step]
                sol_anim = sol[::frame_step]
            else:
                t_anim = t
                sol_anim = sol

            # Use an interval that makes the animation last as long as the simulation time
            if len(t_anim) > 0:
                interval = (t_anim[-1] - t_anim[0]) / len(t_anim) * 1000
            else:
                interval = 50

            x = sol_anim[:, 0]      # horizontal position
            z = sol_anim[:, 1]      # vertical position
            theta = sol_anim[:, 2]  # rotation angle
            
            # Create figure with single animation plot
            fig = plt.figure(figsize=(8, 6), dpi=80)
            
            # Animation axis
            ax_anim = fig.add_subplot(111)
            ax_anim.set_xlim(-0.06, 0.06)
            ax_anim.set_ylim(0, 0.12)
            ax_anim.set_aspect('equal')
            ax_anim.set_title('Maglev Animation')
            ax_anim.grid(True)
            
            # Create animation elements
            # Base rectangle
            base = Rectangle((-0.06, 0), 0.12, 0.01, fc='#3a3a3a')
            ax_anim.add_patch(base)
            
            # Electromagnets (circles)
            magnets = []
            for pos in [-0.03, -0.01, 0.01, 0.03]:
                magnet = Circle((pos, 0.01), 0.005, fc='#e63946')
                ax_anim.add_patch(magnet)
                magnets.append(magnet)
            
            # Levitating object (ellipse)
            levitating_object = Ellipse((x[0], z[0]), 0.024, 0.006, 
                                       angle=np.degrees(theta[0]), fc='#1d71b8')
            ax_anim.add_patch(levitating_object)
            
            # Add a text element for the timer
            timer_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes, fontsize=12, color='black')

            # Animation functions
            def init():
                levitating_object.center = (x[0], z[0])
                levitating_object.angle = np.degrees(theta[0])
                timer_text.set_text('Time: 0.00 s')
                return [levitating_object, timer_text]
            
            def update(i):
                # Update levitating object
                levitating_object.center = (x[i], z[i])
                levitating_object.angle = np.degrees(theta[i])
                # For the last frame, explicitly use the full simulation time T
                current_time = t_anim[i] if i < len(t_anim) - 1 else T
                timer_text.set_text(f'Time: {current_time:.2f} s')
                return [levitating_object, timer_text]
            
            # Create animation with HTML5 backend (more compatible)
            plt.rcParams['animation.html'] = 'html5'
            
            ani = animation.FuncAnimation(
                fig, update, frames=len(t_anim),
                init_func=init, blit=True, interval=interval
            )
            
            plt.tight_layout()
            plt.close()  # Close the figure to prevent display in the notebook
            
            # Convert animation to HTML with explicit HTML5 renderer
            html_animation = ani.to_jshtml(default_mode='once')
            
            # Return HTML animation with additional styling for visibility
            return IPythonHTML(f"""
            <div style="width:100%; max-width:800px; margin:0 auto; border:1px solid #ddd; border-radius:5px; padding:10px; background-color:#f9f9f9;">
                <style>
                    .anim-controls button,
                    .anim-controls input[type="range"] {{
                        transform: scale(0.6);  /* shrink buttons and slider */
                        transform-origin: top left;
                    }}
                </style>
                <div class="anim-controls">
                    {html_animation}
                </div>
            </div>
            """)
        
        except Exception as e:
            error_details = traceback.format_exc()
            return IPythonHTML(f"""
            <div style="color:red; border:1px solid #ffaaaa; padding:10px; background-color:#ffeeee; border-radius:5px;">
                <h3>Animation Error</h3>
                <p>Failed to render animation: {str(e)}</p>
                <details>
                    <summary>Error Details</summary>
                    <pre>{error_details}</pre>
                </details>
            </div>
            """)

    def simulate_and_plot(**kwargs) -> None:
        """
        Simulate the maglev system and plot the results.

        Args:
            **kwargs: Variable keyword arguments from the sliders
        """
        global t, sol, last_valid_Kp, last_valid_Kd
        
        # Extract Kp and Kd for stability checking
        Kp = kwargs.get("Kp", last_valid_Kp)
        Kd = kwargs.get("Kd", last_valid_Kd)
        
        # Validate parameters before simulation
        if not validate_parameters(Kp, Kd):
            # Use the last valid values instead
            with redirect_stderr_to_console():
                sliders["Kp"].value = last_valid_Kp
                sliders["Kd"].value = last_valid_Kd
            return
        
        try:
            # Store current values before simulation attempt
            attempted_Kp = Kp
            attempted_Kd = Kd
            
            # Handle initial state modifications if present in kwargs
            current_state0 = state0.copy()
            
            # Update initial state if x0, z0, etc. are in kwargs
            if "x0" in kwargs and kwargs["x0"] is not None:
                current_state0[0] = kwargs["x0"]
            if "z0" in kwargs and kwargs["z0"] is not None:
                current_state0[1] = kwargs["z0"]
            if "theta0" in kwargs and kwargs["theta0"] is not None:
                current_state0[2] = kwargs["theta0"]
            
            # Update any other simulation parameters if present
            current_params = params.copy()
            for param_name, value in kwargs.items():
                if param_name in current_params and param_name not in ["Kp", "Kd"]:
                    current_params[param_name] = value
            
            # Adjust dt for longer simulations to reduce compute load
            sim_dt = dt
            max_points = 5000
            total_points = int(T / sim_dt)
            if total_points > max_points:
                sim_dt = T / max_points  # Use a larger timestep for long simulations
            
            with redirect_stderr_to_console():
                t, sol = simulate_maglev(Kp, Kd, T, sim_dt, current_state0, current_params)
            
            # Validate the solution
            if not is_valid_solution(sol):
                with out:
                    out.clear_output(wait=True)
                    print(f"Simulation with Kp={attempted_Kp}, Kd={attempted_Kd} produced unstable results.")
                    print(f"Rolling back to last valid values: Kp={last_valid_Kp}, Kd={last_valid_Kd}")
                
                # Roll back to last valid values
                with redirect_stderr_to_console():
                    sliders["Kp"].value = last_valid_Kp
                    sliders["Kd"].value = last_valid_Kd
                
                # Re-run simulation with last valid parameters
                with redirect_stderr_to_console():
                    t, sol = simulate_maglev(last_valid_Kp, last_valid_Kd, T, dt, current_state0, current_params)
                
                # Make sure even this solution is valid
                if not is_valid_solution(sol):
                    with out:
                        out.clear_output(wait=True)
                        print("Even the last valid settings produced unstable results.")
                        print("Please try with different Kp and Kd values.")
                    return
            else:
                # Store successful values only if the simulation was valid
                last_valid_Kp = Kp
                last_valid_Kd = Kd
                
            with out:
                out.clear_output(wait=True)
                
                # Additional safety check before plotting
                try:
                    with redirect_stderr_to_console():
                        plt.figure(figsize=(12, 5))
                        
                        # First subplot
                        plt.subplot(1, 2, 1)
                        plt.plot(t, sol[:, 1], label='z (height)')
                        plt.plot(t, sol[:, 0], label='x (horizontal)')
                        plt.xlabel('Time [s]')
                        plt.ylabel('Position [m]')
                        plt.title('Position of levitating magnet')
                        plt.legend()
                        plt.grid(True)
                        
                        # Second subplot
                        plt.subplot(1, 2, 2)
                        plt.plot(sol[:, 0], sol[:, 2])
                        plt.xlabel('x')
                        plt.ylabel('theta')
                        plt.title('Phase plot: x vs theta')
                        plt.grid(True)
                        
                        plt.tight_layout()
                        plt.show()
                except (ValueError, OverflowError) as e:
                    # Catch specific errors during plotting
                    with redirect_stderr_to_console():
                        plt.close('all')  # Close any partially created figures
                    print(f"Error during plotting: {str(e)}")
                    print(f"The simulation may have produced extreme values that cannot be displayed.")
                    print(f"Try different parameters with higher Kp and Kd values.")

        except Exception as e:
            with out:
                out.clear_output(wait=True)
                # Roll back to last valid values
                with redirect_stderr_to_console():
                    sliders["Kp"].value = last_valid_Kp
                    sliders["Kd"].value = last_valid_Kd
                
                # Display error message with rollback information
                print(f"Error: {e}")
                print(f"Rolling back to last valid values: Kp={last_valid_Kp}, Kd={last_valid_Kd}")
                
                # Use last valid values to show a working plot
                if t is not None and sol is not None:
                    with redirect_stderr_to_console():
                        plt.figure(figsize=(12, 5))
                        plt.subplot(1, 2, 1)
                        plt.plot(t, sol[:, 1], label='z (height)')
                        plt.plot(t, sol[:, 0], label='x (horizontal)')
                        plt.xlabel('Time [s]')
                        plt.ylabel('Position [m]')
                        plt.title('Position of levitating magnet')
                        plt.legend()
                        plt.grid(True)

                        plt.subplot(1, 2, 2)
                        plt.plot(sol[:, 0], sol[:, 2])
                        plt.xlabel('x')
                        plt.ylabel('theta')
                        plt.title('Phase plot: x vs theta')
                        plt.grid(True)

                        plt.tight_layout()
                        plt.show()

    def on_run_animation_clicked(_):
        """
        Handle the Run Animation button click.
        
        Args:
            _: Unused button click event parameter
            
        Returns:
            None
        """
        global t, sol
        if t is None or sol is None:
            with animation_out:
                animation_out.clear_output(wait=True)
                print("No simulation data available. Adjust parameters first.")
            return
        
        with animation_out:
            try:
                # Add a loading message while animation is being created
                animation_out.clear_output(wait=True)
                display(HTML("<p>Creating animation, please wait...</p>"))
                
                # Create and display the animation
                animation_html = create_maglev_animation(t, sol)
                
                # Clear the loading message and show animation
                animation_out.clear_output(wait=True)
                display(animation_html)
                
                # Force rendering of animation (helps in some notebook environments)
                display(Javascript("void(0);"))
            except Exception as e:
                animation_out.clear_output(wait=True)
                print(f"Error creating animation: {str(e)}")
                import traceback
                print(traceback.format_exc())

    def evaluate_parameters(_) -> None:
        """
        Evaluate if the current Kp and Kd match the target values.

        Args:
            _ : Unused argument (required for button callback).

        Returns:
            None
        """
        with result_output:
            result_output.clear_output(wait=True)

            # Button that calls this function will not be shown if evaluation_function is None
            assert evaluation_function  
            
            global sol, t
            if sol is None or t is None:
                print("Simulation has not been run, change the parameters.")
                return

            with redirect_stderr_to_console():
                if evaluation_function(sol, t):
                    print("Correct!")
                else:
                    print("Incorrect!")

    # Create sliders dynamically from config
    sliders = {}
    for param_name, config in sliders_config.items():
        sliders[param_name] = FloatSlider(
            value=config.get("default", 0),
            min=config.get("min", 0),
            max=config.get("max", 100),
            step=config.get("step", 1.0),
            description=config.get("description", param_name)
        )
    
    # Add buttons
    evaluate_button = Button(description="Evaluate")
    evaluate_button.on_click(evaluate_parameters)
    run_animation_button = Button(description="Run Animation")
    run_animation_button.on_click(on_run_animation_clicked)

    # Create the interactive widget with dynamic sliders
    with redirect_stderr_to_console():
        interact(
            simulate_and_plot,
            **sliders
        )

    output_widgets = [out, run_animation_button, animation_out]
    if evaluation_function is not None:
        # Adds widgets for evalution
        output_widgets += [evaluate_button, result_output]
    with redirect_stderr_to_console():
        display(VBox(output_widgets))