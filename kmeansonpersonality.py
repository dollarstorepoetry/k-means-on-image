import sys
import random
import numpy as np
import pandas as pd

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

def average_difference(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("come on now")

    sum = 0
    for i in range(len(vec1)):
        sum += (vec1[i] - vec2[i]) if vec1[i] > vec2[i] else (vec2[i] - vec1[i])
    return sum/len(vec1)

def bigdista(vec1, vec2, choice=0):
    if choice == 0:
        return euclidean_distance(vec1, vec2)
    elif choice == 1:
        return average_difference(vec1, vec2)
    raise ValueError("what") 

def average(arr):
    if len(arr) < 1:
        raise ValueError("input is empty")
    
    sum = [0 for _ in range(len(arr[0]))]
    for vec in arr:
        for i in range(len(sum)):
            sum[i] += vec[i]
    for i in range(len(sum)):
        sum[i] /= len(arr)
    return sum

def clean_data(df, header):
    if (header in df.to_dict().keys()):
        df.drop(header, inplace=True, axis=1) 

# return an array containing the cluster center.
# TODO:order from greatest to least number of poitns assigned to a cluster cneter
def k_means(data, k=3, epsilon=0, max_iter=20, verbose=False):
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
        choice = random.choice(list(oops.keys()))
        cluster_centers.append(list(oops[choice].values()))
        oops.pop(choice)
    del oops  # get out of my memory! you shoddy implementation!

    # Continue until no cluster centers change. 
    k_means = dict()
    num_changes = epsilon+1
    iter = 0
    # if verbose:
        # print(f"Run {iter} (initial values)", flush=True)  
        # for center in cluster_centers:
            # print(f"\t{center}")

    woof = []
    for i in data.keys():
        if list(data[i].values()) in cluster_centers:
            woof.append(i)
    print(f"Initial seeds: {woof}")

    while (num_changes > epsilon and iter < max_iter):
        num_changes = 0

        # Assign data to its closest cluster center.
        # fun fact: this is where the MAJOR bulk of computation is.
        # they have algorithms for this but i am stubborn
        for point in data.keys():
            assigned_center = min(cluster_centers, key=lambda center: bigdista(data[point], center), default=-1) # woah
            # .get returns None if it's not in the dictionary
            if k_means.get(point) == None or k_means.get(point) != assigned_center:
                k_means[point] = assigned_center
                num_changes += 1
            

        # Reassign the cluster centers as the average of its assigned data points.
        for i in range(len(cluster_centers)):
            center = cluster_centers[i]
            assigned_points = []
            # filter out for only the points who have this center
            for point in k_means.keys():
                # feel like this SHOULD raise an error if it's not in the dictionary
                if k_means[point] == center:
                    assigned_points.append(data[point])
            # # bandaid on a tumor
            # if len(assigned_points) == 0:
            #     new_center = (-1,-1,-1)
            #     continue
            new_center = average(assigned_points)
            # reassign the points currently mapped to this center to be mapped to the new center.
            # this is so we can accurately track the number of points that change
            for point in k_means.keys():
                if k_means[point] == center:
                    k_means[point] = new_center
            cluster_centers[i] = new_center
        
        iter += 1

        if verbose:
            print(f"Run {iter}\n\tNum els changed: {num_changes}")  
            for center in cluster_centers:
                print(f"\t{center}")

    # post processing on k_means dict
    for key in k_means.keys():
        k_means[key] = cluster_centers.index(k_means[key])

    return k_means


def main():
    argc = len(sys.argv) # i'm so c-pilled
    if argc < 3:
        raise ValueError("Argument format: python k-means-on-personality.py [csv path] [k]")
        # epsilon = int(input(""))
    else:
        filename = sys.argv[1]
        k = int(sys.argv[2])

    df = pd.read_csv(filename)
    for header in {'category', 'category.1', 'Unnamed: 0', 'Unnamed: 0.1'}:
        clean_data(df, header)

    # df = df.to_dict()  # i cannot be bothered to learn pandas rn. respectfully
    # df.pop("category") # TODO: do more with this

    df = df.to_dict()

    km = k_means(data=df, k=k)

    km = pd.DataFrame(km, index=[0]).T
    
    print(km)

if __name__ == '__main__':
    main()    
    
