from graph_creation.dbManager import DbManager
from graph_creation.graphCreator import GraphCreator
import cProfile

pr = cProfile.Profile()
pr.enable()



#dbManager = DbManager("C:\\Users\\annab\\Box Sync\\Masterarbeit\\DB\\databases")
#dbManager = DbManager("E:\\Master Thesis")

#dbManager = DbManager("D:\Anna Breit\master thesis\databases")

#dbManager.download_resources()
#dbManager.create_db_files()
#dbManager.create_graph()

graph_creator = GraphCreator("D:\Anna Breit\master thesis\\tests")

print ("\n\n############### downloading files #################################")
graph_creator.download_db_files()

print ("\n\n############### creating graph input files #################################")
graph_creator.create_input_files()

print ("\n\n############### creating graph #################################")
graph_creator.create_graph()

pr.disable()
# after your program ends
pr.print_stats(sort="time")