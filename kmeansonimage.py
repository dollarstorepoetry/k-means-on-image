import sys
from PIL import Image
import random

# there are TOTALLY preexisting methods for all of these but i'm silly :p
def euclidean_distance(color1, color2):
    # finds the distance between two three-tuples.
    # naively doing euclidean distance for now
    if len(color1) != len(color2):
        raise ValueError("vectors need to be in the same space to have a distance.")
    
    # why import numpy for this
    sum = 0
    for i in range(len(color1)):
        sum += (color1[i] - color2[i]) ** 2
    sum **= 0.5
    return sum

def tuple_to_hex(color):
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}" 

def hex_to_tuple(color):
    hex1 = int(color[1:3], 16)
    hex2 = int(color[3:5], 16)
    hex3 = int(color[5:], 16)
    return (hex1, hex2, hex3)   

def oops1(arr):
    thing = []
    for i in arr:
        thing.append(tuple_to_hex(i))
    print(thing)

# i need this for an array of ints. this is fine
def minimum(arr):
    min = arr[0]
    for point in arr:
        if point < min:
            min = point
    return min

# i need THIS for an array of colors... not so simple!
def average(arr):
    # sum = 0
    # for i in arr:
    #     sum += i
    # return sum / len(arr)
    sum = [0 for _ in range(len(arr[0]))]
    for color in arr:
        for i in range(len(sum)):
            sum[i] += color[i]
    for i in range(len(sum)):
        sum[i] /= len(arr)
    return sum

# return an array containing the cluster center.
# TODO:order from greatest to least number of poitns assigned to a cluster cneter
def k_means(data, k=5, epsilon=5):
    # K-means algorithm:
    # Randomly assign k points in the data as cluster centers.
    # Then, assign data to its closest cluster center.
    # Reassign the cluster centers as the average of its assigned data points.
    # Continue until no cluster centers change. 

    # Randomly assign k points in the data as cluster centers.
    cluster_centers = []
    oops = data.copy()
    for i in range(k):
        choice = random.choice(oops)
        cluster_centers.append(choice)
        oops.remove(choice)

    # # Then, assign data to its closest cluster center.
    # k_means = dict()
    # for point in data:
    #     distances = dict()
    #     for center in cluster_centers:
    #         dist = euclidean_distance(point, center)
    #         distances[dist] = center
    #     min_dist = minimum(distances.keys())
    #     assigned_center = distances[min_dist]
    #     k_means[point] = assigned_center

    # # Reassign the cluster centers as the average of its assigned data points.
    # for i in range(len(cluster_centers)):
    #     center = cluster_centers[i]
    #     assigned_points = []
    #     for point in k_means.keys():
    #         if k_means[point] == center:
    #             assigned_points.append(point)
    #     cluster_centers[i] = average(assigned_points)

    # Continue until no cluster centers change. 
    num_changes = -1
    i = 0
    while (num_changes < epsilon):
        num_changes = 0

        # Assign data to its closest cluster center.
        k_means = dict()
        for point in data:
            distances = dict()
            for center in cluster_centers:
                dist = euclidean_distance(point, center)
                distances[dist] = center
            min_dist = minimum(list(distances.keys()))
            assigned_center = distances[min_dist]
            # .get returns None if it's not in the dictionary
            if k_means.get(point) != assigned_center:
                k_means[point] = assigned_center
                num_changes += 1

        # Reassign the cluster centers as the average of its assigned data points.
        for i in range(len(cluster_centers)):
            center = cluster_centers[i]
            assigned_points = []
            for point in k_means.keys():
                # feel like this SHOULD raise an error if it's not in the dictionary
                if k_means[point] == center:
                    assigned_points.append(point)
            cluster_centers[i] = average(assigned_points)
        
        print(f"Run {i}: {cluster_centers}")
        # oops1(cluster_centers)
        
        i += 1 # exclusively for debugging purposes

    for i in range(len(cluster_centers)):
        for j in range(3): # not generalizable but I DONT CARE!@!!
            cluster_centers[i][j] = round(cluster_centers[i][j])
    return cluster_centers


def main():
    argc = len(sys.argv) # i'm so c-pilled
    img = Image.open(sys.argv[1]).convert("RGB")
    pixels = list(img.getdata())
    km = k_means(data=pixels)
    for i in range(len(km)):
        km[i] = tuple_to_hex(km[i])
    
    outfilename = 'kmeansoutput.txt'
    with open(outfilename, 'w+') as f:
        for i in km:
            f.write(i)
            f.write('\n')
    print(f"output successfully written to {outfilename}")

if __name__ == '__main__':
    main()    
    
