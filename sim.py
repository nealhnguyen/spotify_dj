from __future__ import division
from math import*
from decimal import Decimal
from scipy import spatial
from scipy.spatial.distance import cosine
import numpy as np
from itertools import izip
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

def cos_sim(vect_x, vect_y, vect_weight=None):
   if vect_weight != None:
      if len(vect_x) != len(vect_weight):
         print "len(x) and len(vector) don't match"
      if len(vect_y) != len(vect_weight):
         print "len(y) and len(vector) don't match"

      total_weight = sum(vect_weight)
      for i, weight in enumerate(vect_weight):
         vect_x[i] = (vect_x[i] * weight) / total_weight
         vect_y[i] = (vect_y[i] * weight) / total_weight

   return 1 - spatial.distance.cosine(vect_x, vect_y)

def main():
   x = [1,1,1]
   y = [2,2,1]
   z = [1,2,2]
   weighty = [1, 1, 2]
   weightz = [2, 1, 1]
   print x, y, z
   print y, z
   print"_____________________________"
   print cos_sim([1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1])
   print "x, y, weighty", cos_sim(x, y, weighty)
   print "x, z, weighty", cos_sim(x, z, weighty)
   print "x, y, weightz", cos_sim(x, y, weightz)
   print "x, z, weightz", cos_sim(x, z, weightz)

if __name__ == "__main__":
  main()
