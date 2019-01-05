#import urllib.request


#url = "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz"
#file_folder = "D:\Anna_Breit\master_thesis\playground"
#file_name = "sql_dump.sql.gz"
#file = os.path.join(file_folder, file_name)
#
#urllib.request.urlretrieve(url, file)
#
#df = dcp.table_to_df(file, "omop_relationship")
#print(df)

class A():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get(self):
        print(self.a)
        print(self.b)


class B(A):
    def __init__(self, a, b):
        super().__init__(a, b)


class C():
    def __init__(self, a, b):
        self.a = 5
        self.b = 5


class X(B, C):
    def __init__(self, a, b):
        super().__init__(a, b)


class D(B):
    def __init__(self, a, b):
        super().__init__(66, 66)


def allClass (cls):
    return set(cls.__subclasses__()).union([x for c in cls.__subclasses__() for x in allClass(c)])

def leaf (cls, classSet = None):
    if classSet is None:
        classSet = set()
    if len(cls.__subclasses__()) == 0:
        classSet.add(cls)
    else:
        classSet.union(x for c in cls.__subclasses__() for x in  leaf(c, classSet))
    return classSet

b=B(1,2)
print(b.a)

#z= [x(1,2) for x in allClass(B)]
#y= [x for x in leaf(B)]
#print(z)
#print(y)

#CONSTANT = "bar"
#
#def setConstant(a):
#    CONSTANT = a
#
#print(CONSTANT)
#setConstant('foo')
#print(CONSTANT)
#
#import graph_creation.constants.globalConstant as c
#print(c.FILE_PATH)
#c.FILE_PATH = 'another'
#print(c.FILE_PATH)
