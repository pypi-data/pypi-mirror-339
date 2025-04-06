import os
import streamlit.components.v1 as components
import streamlit as st

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _counterfactual_slider = components.declare_component(
        "streamlit_counterfactual_slider",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _counterfactual_slider = components.declare_component("streamlit_counterfactual_slider", path=build_dir)


def st_counterfactual_slider(
    name: str,
    min_value: float,
    max_value: float,
    value: float,
    step: float = 0.5,
    survivors_lower: float = None,
    survivors_upper: float = None,
    non_survivors_lower: float = None,
    non_survivors_upper: float = None,
    key: str = None,
):
    """
    A wrapper around the streamlit_counterfactual_slider component.

    Parameters:
        name (str): Label for the slider.
        min_value (float): Minimum slider value.
        max_value (float): Maximum slider value.
        value (float): The initial/standard value.
        step (float, optional): Step size. Defaults to 0.5.
        survivors_lower (float, optional): Lower bound for survivors.
        survivors_upper (float, optional): Upper bound for survivors.
        non_survivors_lower (float, optional): Lower bound for non-survivors.
        non_survivors_upper (float, optional): Upper bound for non-survivors.
        key (str, optional): An optional key for the component.

    Returns:
        The value returned from the component.
    """
    return _counterfactual_slider(
        min=min_value,
        max=max_value,
        step=step,
        defaultValue=value,
        patient_value=value,
        label=name,
        survivors_lower=survivors_lower,
        survivors_upper=survivors_upper,
        non_survivors_lower=non_survivors_lower,
        non_survivors_upper=non_survivors_upper,
        key=key,
    )

