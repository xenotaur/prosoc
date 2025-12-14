import mujoco
import numpy as np
import mujoco.viewer

# Minimal MJCF model: a world with a single sphere
mjcf = '''
<mujoco>
  <worldbody>
    <body name="ball" pos="0 0 1">
      <geom type="sphere" size="0.1" rgba="1 0 0 1"/>
    </body>
  </worldbody>
</mujoco>
'''

# Load the model from the MJCF string
model = mujoco.MjModel.from_xml_string(mjcf)
data = mujoco.MjData(model)

# Create a viewer and render a single frame
try:
    with mujoco.viewer.launch_passive(model, data) as viewer:
        viewer.sync()
        print("SUCCESS: MuJoCo is installed and working!")
except Exception as e:
    print(f"FAILURE: MuJoCo test failed: {e}") 