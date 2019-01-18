from graph_creation.graphCreator import GraphCreator
import cProfile

pr = cProfile.Profile()
#pr.enable()

#dbManager.download_resources()
#dbManager.create_db_files()
#dbManager.create_graph()

graph_creator = GraphCreator("D:\Anna Breit\master thesis\\databases")

print ("\n\n############### downloading files #################################")
pr.run('graph_creator.download_db_files()')
pr.print_stats()


print ("\n\n############### creating graph input files #################################")
pr.run('graph_creator.create_input_files()')
pr.print_stats()


print ("\n\n############### creating graph #################################")
pr.run('graph_creator.create_graph()')
pr.print_stats()

#pr.disable()
# after your program ends

#pr.print_stats(.1, sort="time")