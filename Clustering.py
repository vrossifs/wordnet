import numpy as n

def agglomerative_clustering(data):
    distance_value = [[0 for col in range(len(data))] for row in range(len(data))]
    similarity = n.zeros((len(data), len(data)))
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            for k in range(0, len(data)):
                if data[i][j] in data[k]:
                    if i != k:
                        similarity[i][k] = similarity[i][k] + 1
                        #cari unique words dengan menjumlahkan kedua synstes & menguranginya dengan jumlah kata yg sama
                        unique_word = (len(data[i]) + len(data[k])) - similarity[i][k]
                        # print(unique_word)
                        #hitung distance value
                        distance_value[i][k] = similarity[i][k] / unique_word

    return similarity, distance_value

def big_similarity(data):
    value_similarity = 0
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if data[i][j] > value_similarity:
                value_similarity = data[i][j]
    return value_similarity

def big_distance(data):
    value_distance = 0
    distance_1 = 0
    distance_2 = 0
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if data[i][j] > value_distance:
                value_distance = data[i][j]
                distance_1 = i
                distance_2 = j
                if value_distance == 1:
                    break
    return value_distance, distance_1, distance_2

def new_synsets(data, distance1, distance2):
    synsets = []
    synsets.append(data[distance1])
    synsets.append(data[distance2])
    return synsets

def merged_synsets(data):
    if len(data)>1:
        merged = data[0]
        for i in range(1, len(data)):
            for j in range(0, len(data[i])):
                if data[i][j] not in merged:
                    merged.append(data[i][j])
    return merged