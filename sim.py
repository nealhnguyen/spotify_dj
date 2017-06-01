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
   x = [0.6927300000000003, 0.17840999999999993, 112.34678, 0.13855849999999992, 0.6693300000000002, 0.4957969999999998]
   y = [0.627949152542, 0.177649152542, 122.952220339, 0.158078864407, 0.696559322034, 0.0]
   print cosine_similarity(x,y)

if __name__ == "__main__":
  main()
