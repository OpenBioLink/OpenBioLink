from graph_creation.graphCreator import GraphCreator
import cProfile
import graph_creation.globalConstant as glob

pr = cProfile.Profile()
pr.enable()

glob.DIRECTED = True
glob.QUALITY = None
glob.INTERACTIVE_MODE = True
glob.SKIP_EXISTING_FILES = True
graph_creator = GraphCreator("C:\\Users\\anna\\Desktop\\master")
#graph_creator = GraphCreator("test_data")

#print ("\n\n############### downloading files #################################")
#graph_creator.download_db_files()

print ("\n\n############### creating graph input files #################################")
graph_creator.create_input_files()

print ("\n\n############### creating graph #################################")
graph_creator.create_graph()

pr.disable()

pr.print_stats( sort="time")