
def multiply_feature_vectors(vector1, vector2):
    total = 0.0
    for name in vector1:
        total += vector1[name] * vector2[name]
    return total