import os
import shutil
import time
from ansys.aedt.core import Maxwell3d


rerun = True

# Create an instance of the ``Maxwell3d``.
proj_dir = os.path.join(os.getcwd(), "data3")

if rerun:
    shutil.rmtree(proj_dir)
    if not os.path.exists(proj_dir):
        os.makedirs(proj_dir)
    print ("proj_dir = ", proj_dir)

project_name = os.path.join(proj_dir, "capacitance.aedt")
m3d = Maxwell3d(project=project_name, version="2024.1", new_desktop=True, non_graphical=False, close_on_exit=True)
# m3d.clean_proj_folder()

m3d.solution_type = m3d.SOLUTIONS.Maxwell3d.ElectroStatic

mapping_layers = {1: (0, 100)}
if m3d.import_gds_3d(os.path.join(proj_dir, "../../moonmon/moonmon_460_for_sim.GDS"),
                     mapping_layers, units='nm', import_method=0):
    print("export is successful")
# m3d.export_design_preview_to_jpg(os.path.join(proj_dir, "qqq.jpg" ))
objects_names = m3d.modeler.model_objects
print("objects = ", objects_names)

objects = m3d.modeler.object_list
print("objects = ", objects)

# assing material
if m3d.assign_material(objects,"pec"):
    print("pec is assigned")

subtrace = m3d.modeler.create_box(origin=[-1, -1, -0.5], sizes=[2, 2, 0.5], name="subtrace", material="sapphire")
vacuum = m3d.modeler.create_box(origin=[-1, -1, 0], sizes=[2, 2, 2], name="vacuum", material="vacuum")

# assing excitations
e1 = m3d.assign_voltage(assignment=objects[0], amplitude=0, name="E1")
e2 = m3d.assign_voltage(assignment=objects[1], amplitude=0, name="E2")
e3 = m3d.assign_voltage(assignment=objects[2], amplitude=0, name="E3")

# assign the matrix
selection = ['E1', 'E2', 'E3']
c1 = m3d.assign_matrix(assignment=selection, matrix_name="C1")

if rerun:
#     # Create a model
#     v1 = m3d.modeler.create_box(origin=[0, 0, 0], sizes=[2, 3, 1], name="V1", material="pec")
#     v2 = m3d.modeler.create_box(origin=[3, 0, 0], sizes=[2, 3, 1], name="V2", material="pec")
#     vacuum = m3d.modeler.create_box(origin=[-1, -1, -1], sizes=[7, 7, 7], name="vacuum", material="vacuum")

#     # assing excitations
#     e1 = m3d.assign_voltage(assignment=v1, amplitude=0, name="E1")
#     e2 = m3d.assign_voltage(assignment=v2, amplitude=0, name="E2")

#     # assign the matrix
#     selection = ['E1', 'E2']
#     c1 = m3d.assign_matrix(assignment=selection, matrix_name="C1")

    # Create setup
    m3d.create_setup(name="Setup1", MaximumPasses=20, PercentError=1)
    m3d.mesh.assign_length_mesh(objects[0].id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh1")
    m3d.mesh.assign_length_mesh(objects[1].id, inside_selection=True, maximum_length=0.1, maximum_elements=1000,   name="Mesh2")
    m3d.mesh.assign_length_mesh(objects[2].id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh3")
    m3d.mesh.generate_mesh("Setup1")

    # Analyse
    m3d.analyze(cores=1)

# Getting capacitance matrix
expressions = m3d.post.available_report_quantities(solution='Setup1 : LastAdaptive', quantities_category='C')
solution = m3d.post.get_solution_data(expressions=expressions, report_category='C')
print ("solution = ", solution)
solution.export_data_to_csv(os.path.join(proj_dir, "capacitance_moonmon.csv"))

# Dedusing available options
# print ("available_report_solutions = ", m3d.post.available_report_solutions())
# print ("available_quantities_categories = ", m3d.post.available_quantities_categories())
# print ("available_report_quantities = ", m3d.post.available_report_quantities(solution='Setup1 : LastAdaptive',
#                                                                               quantities_category='C'))
# report = m3d.post.create_report('C1.C(E1,E1)', report_category='C', plot_type='Data Table')
# print ("available_display_types = ", m3d.post.available_display_types("C"))

# Save everything
m3d.save_project()
m3d.release_desktop()