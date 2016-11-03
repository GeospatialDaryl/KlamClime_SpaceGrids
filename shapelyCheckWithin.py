import shapely
from shapely.geometry import shape, Point
import fiona

def explode(coords):
    """Explode a GeoJSON geometry's coordinates object and yield coordinate tuples.
    As long as the input is conforming, the type of the geometry doesn't matter.
       http://gis.stackexchange.com/questions/90553/fiona-get-each-feature-extent-bounds
    """
    for e in coords:
        if isinstance(e, (float, int, long)):
            yield coords
            break
        else:
            for f in explode(e):
                yield f

def bbox(f):
    x, y = zip(*list(explode(f['geometry']['coordinates'])))
    return min(x), min(y), max(x), max(y)

def checkWithin(inputPt, inputSHP = r"J:\inputSHP_HUC10_Phase1\Albers_plyPhase1_HUC10s_SID1013.shp"):
    c = fiona.open(inputSHP, 'r')
    f = c[0]
    geom = shape(f['geometry'])
    return geom.contains(inputPt)

class ShapeContainer:
    def __init__(self, inputSHP):
        import fiona
        from shapely.geometry import shape, Point
        
        self.path = inputSHP
        self.c = fiona.open(inputSHP, 'r')
        self.f = self.c[0]
        self.geom = shape(self.f['geometry'])
    def checkPoint(self,inputPt):
        return self.geom.contains(inputPt)
        
        
inputSHP = r"J:\inputSHP_HUC10_Phase1\Albers_plyPhase1_HUC10s_SID1013.shp"        
    
testPoint = Point(-284547.252  ,371830.926)

checkWithin(testPoint)

thisShp = ShapeContainer(inputSHP)
thisShp.checkPoint(testPoint)
