import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import numpy

def show_plot(facets):
    fig = plt.figure(figsize=(18,9))
    ax2 = fig.add_subplot(111, projection='3d')
    colors = list(map("C{}".format, range(len(facets))))
    pc = a3.art3d.Poly3DCollection(facets,  #facecolor=colors, 
                                    edgecolor="k", alpha=0.5)
    ax2.add_collection3d(pc)
    ax2.set_xlabel('x')
    ax2.set_xlim([0,200])
    ax2.set_ylabel('y')
    ax2.set_ylim([200,0])
    ax2.set_zlabel('z')
    ax2.set_zlim([0,200])
    plt.show()
	
def point_in_hyperplane(point, plane, epsilon=0.1):
	return abs(plane[0:-1] @ point + plane[-1]) < epsilon
    
def angle(v, w): 
    return numpy.arccos(v.dot(w)/(numpy.linalg.norm(v)*numpy.linalg.norm(w)))

def order_points(facets):
    g = facets.tolist()
    out = [g.pop(0)]
    base_vector = numpy.array(g[0]) - numpy.array(out[-1])
    #base_vector = g[0] - out[-1]
    max_rotation = 0.
    index = 0
    for i in range(1, len(g)):
        vector = numpy.array(g[i]) - numpy.array(out[-1])
        rotation = angle(base_vector, vector)
        if rotation > max_rotation and rotation <= numpy.pi:
            index = i
            max_rotation = rotation
    out.append(g.pop(index))

    while(g):
        base_vector = numpy.array(out[-2]) - numpy.array(out[-1])
        max_rotation = 0.
        index = 0
        for i in range(0, len(g)):
            vector = numpy.array(g[i]) - numpy.array(out[-1])
            rotation = angle(base_vector, vector)
            if rotation > max_rotation and rotation <= numpy.pi:
                index = i
                max_rotation = rotation
        out.append(g.pop(index))
    return numpy.array(out)
	
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '=', printEnd = "\r"):
	"""
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
	if iteration == total: 
		print()
	
#def plotDistances(distances, retina):
#9003
#17040