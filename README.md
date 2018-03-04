# Book-Recommendations-Using-Social-Network-Analysis

We will be using the Amazon Meta-Data Set maintained on the SNAP site. This data set is comprised of product and review metdata on 548,552 different products. The data was collected in 2006 by crawling the Amazon website.


The following information is available for each product in this dataset:
•	Id: Product id (number 0, ..., 548551)
•	ASIN: Amazon Standard Identification Number. 
The Amazon Standard Identification Number (ASIN) is a 10-character alphanumeric unique identifier assigned by Amazon.com for product identification. You can lookup products by ASIN using following link: https://www.amazon.com/product-reviews/<ASIN> 
•	title: Name/title of the product
•	group: Product group. The product group can be Book, DVD, Video or Music.
•	salesrank: Amazon Salesrank
The Amazon sales rank represents how a product is selling in comparison to other products in its primary category. The lower the rank, the better a product is selling. 
•	similar: ASINs of co-purchased products (people who buy X also buy Y)
•	categories: Location in product category hierarchy to which the product belongs (separated by |, category id in [])
•	reviews: Product review information: total number of reviews, average rating, as well as individual customer review information including time, user id, rating, total number of votes on the review, total number of helpfulness votes (how many people found the review to be helpful)


The first step we will perform is read, preprocess, and format this data for further analysis. 

The script PreprocessAmazonBooks.py  takes the “amazon-meta.txt” file as input, and performs the following steps:

•	Parse the amazon-meta.txt file

•	Preprocess the metadata for all ASINs, and write out the following fields into the amazonProducts Nested Dictionary (key = ASIN and value = MetaData Dictionary associated with ASIN):
o	Id: same as “Id” in amazon-meta.txt
o	ASIN: same as “ASIN” in amazon -meta.txt
o	Title: same as “title” in amazon-meta.txt
o	Categories: a transformed version of “categories” in amazon-meta.txt. Essentially, all categories associated with the ASIN are concatenated, and are then subject to the following Text Preprocessing steps: lowercase, stemming, remove digit/punctuation, remove stop words, retain only unique words. The resulting list of words is then placed into “Categories”.
o	Copurchased: a transformed version of “similar” in amazon-meta.txt. Essentially, the copurchased ASINs in the “similar” field are filtered down to only those ASINs that have metadata associated with it. The resulting list of ASINs is then placed into “Copurchased”.
o	SalesRank: same as “salesrank” in amazon-meta.txt
o	TotalReviews: same as total number of reviews under “reviews” in amazon-meta.txt
o	AvgRating: same as average rating under “reviews” in amazon-meta.txt

•	Filter amazonProducts Dictionary down to only Group=Book, and write filtered data to amazonBooks Dictionary

•	Use the co-purchase data in amazonBooks Dictionary to create the copurchaseGraph Structure as follows:
o	Nodes: the ASINs are Nodes in the Graph
o	Edges: an Edge exists between two Nodes (ASINs) if the two ASINs were co-purchased
o	Edge Weight (based on Category Similarity): since we are attempting to make book recommendations based on co-purchase information, it would be nice to have some measure of Similarity for each ASIN (Node) pair that was co-purchased (existence of Edge between the Nodes). We can then use the Similarity measure as the Edge Weight between the Node pair that was co-purchased. We can potentially create such a Similarity measure by using the “Categories” data, where the Similarity measure between any two ASINs that were co-purchased is calculated as follows:
Similarity = (Number of words that are common between Categories of connected Nodes)/
		(Total Number of words in both Categories of connected Nodes)
The Similarity ranges from 0 (most dissimilar) to 1 (most similar).

•	Add the following graph-related measures for each ASIN to the amazonBooks Dictionary:
o	DegreeCentrality: associated with each Node (ASIN)
o	ClusteringCoeff: associated with each Node (ASIN)

•	Write out the amazonBooks data to the amazon-books.txt file (all except copurchase data – because that data is now in the copurchase graph)

•	Write out the copurchaseGraph data to the amazon-books-copurchase.edgelist file



The next step is to use this transformed data to make Book Recommendations. 

•	Read amazon-books.txt data into the amazonBooks Dictionary

•	Read amazon-books-copurchase.edgelist into the copurchaseGraph Structure

•	We then assume a User has purchased a Book with ASIN=0805047905. The question then is, how do we make other Book Recommendations to this User, based on the Book copurchase data that we have? We could potentially take ALL books that were ever copurchased with this book, and recommend all of them. However, the Degree Centrality of Nodes in a Product Co-Purchase Network can typically be quite large. We should therefore come up with a better strategy. 

•	We examine the metadata associated with the Book that the User is looking to purchase (purchasedAsin =0805047905), including Title, SalesRank, TotalReviews, AvgRating, DegreeCentrality, and ClusteringCoefficient. We notice that this Book has a DegreeCentrality of 216 – which means 216 other Books were copurchased with this Book by other Customers. So yes, it would indeed make sense to come up with a better strategy of recommending copurchased Books.

Coding Steps described in the script performs following function:

•	[Step 1] Get the books that have been co-purchased with the purchasedAsin in the past. That is, get the depth-1 ego network of purchasedAsin from copurchaseGraph, and assign the resulting graph to purchasedAsinEgoGraph.

•	[Step 2] Filter down to the most similar books. That is, use the island method on purchasedAsinEgoGraph to only retain edges with threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph

•	[Step 3] Get the books that are still connected to the purchasedAsin by one hop (called the neighbors of the purchasedAsin) after the above clean-up, and assign the resulting list to purchasedAsinNeighbors.

•	[Step 4] Come up with a composite measure to make the Top Five book recommendations based on one or more of the following metrics associated with neighbors in purchasedAsinNeighbors: SalesRank, AvgRating, TotalReviews, DegreeCentrality, and ClusteringCoeff.

•	[Step 5] Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff) based on your composite measure.
