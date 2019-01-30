from graph_creation.graphCreator import GraphCreator
import cProfile
import graph_creation.globalConstant as glob

pr = cProfile.Profile()
pr.enable()

glob.DIRECTED = True
glob.QUALITY = None
glob.INTERACTIVE_MODE = False
glob.SKIP_EXISTING_FILES = True
graph_creator = GraphCreator("C:\\Users\\anna\\Desktop")
#fixme define quality

print ("\n\n############### downloading files #################################")
graph_creator.download_db_files()

print ("\n\n############### creating graph input files #################################")
graph_creator.create_input_files()

#print ("\n\n############### creating graph #################################")
#pr.run('graph_creator.create_graph()')
#pr.print_stats()

pr.disable()

pr.print_stats( sort="time")