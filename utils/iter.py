def find(predicate,iter):
  return next( (x for x in iter if predicate(x) ), None )