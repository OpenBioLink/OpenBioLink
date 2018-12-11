from db.dbManager import DbManager
import cProfile

pr = cProfile.Profile()
pr.enable()



#dbManager = DbManager("C:\\Users\\annab\\Box Sync\\Masterarbeit\\DB\\databases")
#dbManager = DbManager("E:\\Master Thesis")

dbManager = DbManager("E:\Anna_Breit\master_thesis\databases")

#dbManager.download_resources()
#dbManager.create_db_files()
dbManager.create_graph()



pr.disable()
# after your program ends
pr.print_stats(sort="time")