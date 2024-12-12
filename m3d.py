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
m3d = Maxwell3d(project=project_name, version="2024.1", new_desktop=True, non_graphical=True, close_on_exit=True)
# m3d.clean_proj_folder()

m3d.solution_type = m3d.SOLUTIONS.Maxwell3d.ElectroStatic

if rerun:
    # Create a model
    v1 = m3d.modeler.create_box(origin=[0, 0, 0], sizes=[2, 3, 1], name="V1", material="pec")
    v2 = m3d.modeler.create_box(origin=[3, 0, 0], sizes=[2, 3, 1], name="V2", material="pec")
    vacuum = m3d.modeler.create_box(origin=[-1, -1, -1], sizes=[7, 7, 7], name="vacuum", material="vacuum")

    # assing excitations
    e1 = m3d.assign_voltage(assignment=v1, amplitude=0, name="E1")
    e2 = m3d.assign_voltage(assignment=v2, amplitude=0, name="E2")

    # assign the matrix
    selection = ['E1', 'E2']
    c1 = m3d.assign_matrix(assignment=selection, matrix_name="C1")

    # Create setup
    m3d.create_setup(name="Setup1", MaximumPasses=20, PercentError=1)
    m3d.mesh.assign_length_mesh(v1.id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh1")
    m3d.mesh.assign_length_mesh(v2.id, inside_selection=True, maximum_length=0.1, maximum_elements=100000, name="Mesh2")
    m3d.mesh.generate_mesh("Setup1")

    # Analyse
    m3d.analyze(cores=1)

# Getting capacitance matrix
expressions = m3d.post.available_report_quantities(solution='Setup1 : LastAdaptive', quantities_category='C')
solution = m3d.post.get_solution_data(expressions=expressions, report_category='C')
print ("solution = ", solution)
solution.export_data_to_csv(os.path.join(proj_dir, "capacitance.csv"))

# Dedusing available options
# print ("available_report_solutions = ", m3d.post.available_report_solutions())
# print ("available_quantities_categories = ", m3d.post.available_quantities_categories())
# print ("available_report_quantities = ", m3d.post.available_report_quantities(solution='Setup1 : LastAdaptive',
#                                                                               quantities_category='C'))
# report = m3d.post.create_report('C1.C(E1,E1)', report_category='C', plot_type='Data Table')
# print ("available_display_types = ", m3d.post.available_display_types("C"))

# Save everything
m3d.save_project()
