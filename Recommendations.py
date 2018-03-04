
print ()
import math
import networkx
import operator 
import matplotlib.pyplot

# Read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['SalesRank'] = int(cell[5].strip())
    MetaData['TotalReviews'] = int(cell[6].strip())
    MetaData['AvgRating'] = float(cell[7].strip())
    MetaData['DegreeCentrality'] = int(cell[8].strip())
    MetaData['ClusteringCoeff'] = float(cell[9].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    
# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
# (1) 
#     Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.

purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, purchasedAsin, radius=1)
#print (purchasedAsinEgoGraph.neighbors(purchasedAsin))

# The edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# (2)  
#     Using the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data=True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,e)

# Given the purchasedAsinEgoTrimGraph you constructed above, 
# We can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# (3)  
#     Find the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, and assign it to purchasedAsinNeighbors
purchasedAsinNeighbors = []
for f, t, e in purchasedAsinEgoTrimGraph.edges(data=True):
    if f == purchasedAsin:
        purchasedAsinNeighbors.append(t)
#print(purchasedAsinNeighbors)
#len(purchasedAsinNeighbors)
# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) 
#     Note that, given an asin, we can get at the metadata associated with  
#     it using amazonBooks (similar to lines 49-56 above).
#     Now, come up with a composite measure to make Top Five book 
#     recommendations based on one or more of the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff 
measure = {}

# logic for this step is explained in the word file attached with this code script
for asin in purchasedAsinNeighbors:
    measure[asin] = (math.log(amazonBooks[asin]['TotalReviews']+ 1) +  math.log(amazonBooks[asin]['AvgRating']+1))* 0.5 + math.log(amazonBooks[asin]['DegreeCentrality']+1)*0.3 + (amazonBooks[asin]['ClusteringCoeff'])*0.2

# sorted_measure is dictionary of sorted nearest neighbors in descending order of the composite measure
sorted_measure = dict(sorted(measure.items(), key = operator.itemgetter(1), reverse = True))

# This code below takes only top 5 sorted recommendations
sorted_top5 = {}
c=1
for i in sorted_measure:
    if c > 5:
        break
    sorted_top5[i] = sorted_measure[i]
    c+=1
#print(sorted_top5)

print()
# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5)
n = 1
for i in sorted_top5:
    print("Top ",n," recommendation for the Book with Asin '0805047905' is: ")
    print("Asin = ", i)
    print("Title of the Book = ", amazonBooks[i]['Title'])
    print("SalesRank = ", amazonBooks[i]['SalesRank'])
    print("TotalReviews = ", amazonBooks[i]['TotalReviews'])
    print("AvgRating = ", amazonBooks[i]['AvgRating'])
    print("DegreeCentrality = ", amazonBooks[i]['DegreeCentrality'])
    print("ClusteringCoeff = ", amazonBooks[i]['ClusteringCoeff'])
    print()
    n += 1

