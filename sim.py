from __future__ import division
from scipy.spatial.distance import cosine
import numpy as np
import sys

def all_same_len(lists):
   lists = filter(None, lists)

   n = len(lists[0])
   if all(len(x) == n for x in lists):
      return True
   return False

def get_weighted_vectors(vect_x, vect_y, vect_weight):
   total_weight = sum(vect_weight)
   for i, weight in enumerate(vect_weight):
      vect_x[i] = (vect_x[i] * weight) / total_weight
      vect_y[i] = (vect_y[i] * weight) / total_weight

   return vect_x, vect_y

def cos_sim(vect_x, vect_y, vect_weight=None):
   if not all_same_len([vect_x, vect_y, vect_weight]):
      print "Lengths of all vectors not the same"
      sys.exit()

   if vect_weight != None:
      vect_x, vect_y = get_weighted_vectors(vect_x, vect_y, vect_weight)

   return 1 - cosine(vect_x, vect_y)

def test_cos_sim():
   x = [1,1,1]
   y = [2,2,1]
   z = [1,2,2]
   weighty = [1, 1, 2]
   weightz = [2, 1, 1]
   print x, y, z
   print y, z
   print cos_sim([1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1])
   print "x, y, weighty", cos_sim(x, y, weighty)
   print "x, z, weighty", cos_sim(x, z, weighty)
   print "x, y, weightz", cos_sim(x, y, weightz)
   print "x, z, weightz", cos_sim(x, z, weightz)
   x = [0.6927300000000003, 0.17840999999999993, 0.13855849999999992, 0.6693300000000002, 0.4957969999999998]
   y = [0.627949152542, 0.177649152542, 0.158078864407, 0.696559322034, 0.0]
   print cos_sim(x, y)

if __name__ == "__main__":
  test_cos_sim()
