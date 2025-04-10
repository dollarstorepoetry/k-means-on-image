import sys
from PIL import Image
import random
import numpy as np

def trollface(data, k):
    asdlkfijhyg = data.sort(reverse=True)
    return asdlkfijhyg[:k]

# there are TOTALLY preexisting methods for all of these but i'm silly :p
def euclidean_distance(vec1, vec2):
    # finds the distance between two three-tuples.
    # naively doing euclidean distance for now
    if len(vec1) != len(vec2):
        raise ValueError("vectors need to be in the same space to have a distance.")
    
    # why import numpy for this
    sum = 0
    for i in range(len(vec1)):
        sum += (vec1[i] - vec2[i]) ** 2
    sum **= 0.5
    return sum

def tuple_to_hex(color, roundy=True):
    if roundy:
        doink = []
        # for component in color:
        for feature in color: # gotta use the lingo
            doink.append(int(round(feature)))
    else:
        doink = color
    if len(doink) == 0:
        return "#what"
    else:
        return f"#{doink[0]:02x}{doink[1]:02x}{doink[2]:02x}" 

def hex_to_tuple(color):
    hex1 = int(color[1:3], 16)
    hex2 = int(color[3:5], 16)
    hex3 = int(color[5:], 16)
    return (hex1, hex2, hex3)   

# i need THIS for an array of colors... not so simple!
# except it actually is because you can just treat the colors as vectors in R3
def average(arr):
    # if len(arr) < 1:
    #     return arr # this is a bandaid on a MASSIVE tumor. i should probably fix this
    
    sum = [0 for _ in range(len(arr[0]))]
    for vec in arr:
        for i in range(len(sum)):
            sum[i] += vec[i]
    for i in range(len(sum)):
        sum[i] /= len(arr)
    return sum

# return an array containing the cluster center.
# TODO:order from greatest to least number of poitns assigned to a cluster cneter
def k_means(data, k=5, epsilon=0, max_iter=100, verbose=False):
    if k <= 0:
        raise ValueError("k must be greater than zero.")
    if epsilon < 0:
        # gonna piss off a lot of mathematicians with this
        raise ValueError("epsilon must be a natural number.")
    
    # K-means algorithm:
    # Randomly assign k points in the data as cluster centers.
    # Then, assign data to its closest cluster center.
    # Reassign the cluster centers as the average of its assigned data points.
    # Continue until no cluster centers change. 

    # Randomly assign k points in the data as cluster centers.
    cluster_centers = []
    oops = data.copy()
    for _ in range(k):
        choice = random.choice(oops)
        # print(type(choice))
        cluster_centers.append(choice)
        np.delete(oops, choice)
    del oops  # get out of my memory! you shoddy implementation!

    # Continue until no cluster centers change. 
    k_means = dict()
    num_changes = epsilon+1
    iter = 0
    if verbose:
        print(f"Run {iter} (initial values)", flush=True)  
        for center in cluster_centers:
            print(f"\t{tuple_to_hex(center)} {center}")

    while (num_changes > epsilon and iter < max_iter):
        num_changes = 0

        # Assign data to its closest cluster center.
        # fun fact: this is where the MAJOR bulk of computation is.
        # they have algorithms for this but i am stubborn
        for point in data:
            pt = tuple(point)
            assigned_center = min(cluster_centers, key=lambda center: euclidean_distance(point, center), default=-1) # woah
            # .get returns None if it's not in the dictionary
            if k_means.get(pt) is None or not np.array_equal(k_means.get(pt), assigned_center):
                k_means[pt] = assigned_center
                num_changes += 1
            

        # Reassign the cluster centers as the average of its assigned data points.
        for i in range(len(cluster_centers)):
            center = cluster_centers[i]
            assigned_points = []
            # filter out for only the points who have this center
            for point in k_means.keys():
                # feel like this SHOULD raise an error if it's not in the dictionary
                pt = tuple(point)
                if np.array_equal(k_means[pt], center):
                    assigned_points.append(point)
            # bandaid on a tumor
            if len(assigned_points) == 0:
                new_center = (-1,-1,-1)
                continue
            new_center = average(assigned_points)
            # reassign the points currently mapped to this center to be mapped to the new center.
            # this is so we can accurately track the number of points that change
            for point in k_means.keys():
                pt = tuple(point)
                if np.array_equal(k_means[pt], center):
                    k_means[pt] = new_center
            cluster_centers[i] = new_center
        
        iter += 1

        if verbose:
            print(f"Run {iter}\n\tNum els changed: {num_changes}")  
            for center in cluster_centers:
                print(f"\t{tuple_to_hex(center)} {center}")

    for i in range(len(cluster_centers)):
        for j in range(len(cluster_centers[i])):
            cluster_centers[i][j] = round(cluster_centers[i][j])
    return cluster_centers


def main():
    argc = len(sys.argv) # i'm so c-pilled
    if argc < 3:
        raise ValueError("Argument format: python kmeansonimage.py [image path] [k]")
        # epsilon = int(input(""))
    else:
        filename = sys.argv[1]
        k = int(sys.argv[2])
    # img = Image.open(filename).convert("RGB")
    img = Image.open(filename).resize((100,100)).convert("RGB") # wow!
    # lesson #1 in machine learning: 
    # if you can preserve the integrity of the data by doing so, 
    # reduce the size of the data whenever possible
    pixels = np.array(img.getdata())
    km = k_means(data=pixels, k=k, verbose=True)
    # km = trollface(data=pixels, k=k)
    for i in range(len(km)):
        km[i] = tuple_to_hex(km[i])
    
    outfilename = 'k-means-output.txt'
    with open(outfilename, 'w+') as f:
        for i in km:
            f.write(i)
            f.write('\n')
    print(f"output successfully written to {outfilename}")

if __name__ == '__main__':
    main()    
    
