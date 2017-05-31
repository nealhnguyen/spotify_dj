from math import*
from decimal import Decimal
from scipy import spatial

from math import*
  
def jaccard_similarity(x,y):
   intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
   union_cardinality = len(set.union(*[set(x), set(y)]))
   return intersection_cardinality/float(union_cardinality)
  
#def cosine_similarity(x, y):
#   return 1 - spatial.distance.cosine(x, y)

def square_rooted(x):
   return round(sqrt(sum([a*a for a in x])),3)
  
def cosine_similarity(x,y):
   numerator = sum(a*b for a,b in zip(x,y))
   denominator = square_rooted(x)*square_rooted(y)
   return round(numerator/float(denominator),3)

def main():
   x = [0,3,4,5]
   y = [7,6,3,-1]
   print jaccard_similarity(x,y)
   print cosine_similarity(x,y)

if __name__ == "__main__":
  main()
