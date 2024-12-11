# Electro DC analysis
import os
import time
from ansys.aedt.core import Maxwell3d

# Create an instance of the ``Maxwell3d``.
proj_dir = os.path.join(os.getcwd(), "data3")
if not os.path.exists(proj_dir):
    os.makedirs(proj_dir)
print ("proj_dir = ", proj_dir)

project_name = os.path.join(proj_dir, "capacitance.aedt")
m3d = Maxwell3d(project=project_name, version="2024.1", new_desktop=True, non_graphical=True, close_on_exit=True)
m3d.solution_type = m3d.SOLUTIONS.Maxwell3d.ElectroStatic #ElectroDCConduction

# Create a model
# Create setup and assign voltage
v1 = m3d.modeler.create_box(origin=[0, 0, 0], sizes=[2, 3, 1], name="V1", material="pec")
v2 = m3d.modeler.create_box(origin=[3, 0, 0], sizes=[2, 3, 1], name="V2", material="pec")
vacuum = m3d.modeler.create_box(origin=[-1, -1, -1], sizes=[7, 7, 7], name="vacuum", material="vacuum")

# assing excitations
e1 = m3d.assign_voltage(assignment=v1, amplitude=0, name="E1")
e2 = m3d.assign_voltage(assignment=v2, amplitude=0, name="E2")

# assign the matrix
selection = ['E1', 'E2']
m3d.assign_matrix(assignment=selection, matrix_name="C1")

# Solve setup
m3d.create_setup(name="Setup1", MaximumPasses=20, PercentError=1)
# m3d.mesh.assign_length_mesh(maxlength=5, maxel="None")
m3d.mesh.assign_length_mesh(v1.id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh1")
m3d.mesh.assign_length_mesh(v2.id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh2")
m3d.mesh.generate_mesh("Setup1")

m3d.analyze(cores=1)

# # ## Compute mass center
# # Compute mass center using PyAEDT advanced fields calculator.
# scalar_function = ""
# mass_center = {
#     "name": "",
#     "description": "Mass center computation",
#     "design_type": ["Maxwell 3D"],
#     "fields_type": ["Fields"],
#     "primary_sweep": "distance",
#     "assignment": "",
#     "assignment_type": ["Solid"],
#     "operations": [
#         scalar_function,
#         "EnterVolume('assignment')",
#         "Operation('VolumeValue')",
#         "Operation('Mean')",
#     ],
#     "report": ["Data Table"],
# }
# mass_center["name"] = "CM_X"
# scalar_function = "Scalar_Function(FuncValue='X')"
# mass_center["operations"][0] = scalar_function
# m3d.post.fields_calculator.add_expression(mass_center, conductor.name)
# mass_center["name"] = "CM_Y"
# scalar_function = "Scalar_Function(FuncValue='Y')"
# mass_center["operations"][0] = scalar_function
# m3d.post.fields_calculator.add_expression(mass_center, conductor.name)
# mass_center["name"] = "CM_Z"
# scalar_function = "Scalar_Function(FuncValue='Z')"
# mass_center["operations"][0] = scalar_function
# m3d.post.fields_calculator.add_expression(mass_center, conductor.name)

# # ## Get mass center
# #
# # Get mass center using the fields calculator.

# xval = m3d.post.get_scalar_field_value(quantity="CM_X")
# yval = m3d.post.get_scalar_field_value(quantity="CM_Y")
# zval = m3d.post.get_scalar_field_value(quantity="CM_Z")

# # ## Create variables
# #
# # Create variables with mass center values.
# m3d[conductor.name + "x"] = str(xval * 1e3) + "mm"
# m3d[conductor.name + "y"] = str(yval * 1e3) + "mm"
# m3d[conductor.name + "z"] = str(zval * 1e3) + "mm"

# # ## Create coordinate system
# #
# # Create a parametric coordinate system.
# cs1 = m3d.modeler.create_coordinate_system(
#     origin=[conductor.name + "x", conductor.name + "y", conductor.name + "z"],
#     reference_cs="Global",
#     name=conductor.name + "CS",
# )

# exported_files = m3d.export_results(export_folder=proj_dir, matrix_name="C1")
# print("exported_files = ", exported_files)
m3d.save_project()
