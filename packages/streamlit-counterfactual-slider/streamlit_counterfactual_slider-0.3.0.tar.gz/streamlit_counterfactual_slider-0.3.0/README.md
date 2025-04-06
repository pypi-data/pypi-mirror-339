# Counterfactual Slider Component

This repository contains a custom [Streamlit](https://streamlit.io) Component for creating an interactive counterfactual slider. The counterfactual slider allows users to explore "what-if" scenarios by adjusting input values and observing the corresponding changes in outputs.

For complete information on Streamlit Components, visit the [Streamlit Components documentation](https://docs.streamlit.io/library/components).

## Overview

The Counterfactual Slider Component is built with a Python API and a frontend powered by modern web technologies. It enables seamless interaction between Python and the frontend, making it easy to integrate into any Streamlit app.

### Key Features:
- **Interactive Sliders**: Adjust input values dynamically.
- **Real-time Feedback**: Observe changes in outputs instantly.
- **Advanced Parameters**: Define bounds for specific groups like survivors and non-survivors.

### Example Usage:
```python
import streamlit as st
from counterfactual_slider import st_counterfactual_slider

# Use the counterfactual slider in your Streamlit app:
selected_value = st_counterfactual_slider(
    name="Adjust Value",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
    survivors_lower=20,
    survivors_upper=80,
    non_survivors_lower=10,
    non_survivors_upper=90,
)
st.write(f"Selected Value: {selected_value}")
```

## Quickstart

Follow these steps to set up and use the Counterfactual Slider Component:

1. **Install the Package**:
    - Install the component directly from PyPI:
      ```bash
      pip install streamlit-counterfactual-slider
      ```

2. **Use in Your Streamlit App**:
    - Import and integrate the slider into your Streamlit app as shown in the example above.

3. **Run Your App**:
    - Save your Streamlit script (e.g., `app.py`) and run it:
      ```bash
      streamlit run app.py
      ```

That's it! The Counterfactual Slider Component is ready to use in your Streamlit application.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
