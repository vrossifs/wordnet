import re, pandas, time, Clustering, matplotlib.pyplot as pyplot
from scipy.cluster import hierarchy
from Komutatif import alt_gen

def read_input():
    file = open('datauji/Input.txt')
    return file.readlines()

def read_validasi():
    file = open('datauji/Validasi.txt')
    return file.readlines()

def read_dataset():
    file = open('output/output komutatif.txt')
    return file.readlines()

def read_hasil_clustering(file):
    file = open(file)
    return file.readlines()

def preprocessing(data):
    clear_right = []
    record = []
    kata = []

    #bersih char sebelah kanan
    for i in range(len(data)):
        data[i] = data[i].rstrip()
        if len(data[i]) > 1:
            clear_right.append(data[i])
    
    for i in range(len(clear_right)):
        string = clear_right[i]
        while i < len(clear_right) and clear_right[i][len(clear_right[i]) - 1] == ',':
            i += 1
            string += ' '+clear_right[i]
        record.append(string)

    #hapus karakter
    for i in range(0, len(record)):
        string = re.sub('\ |\'|\[|\]', '',record[i])
        string = string.split(',')
        kata.append(string)
    return kata

def merge_synset(data):
    merge = []
    for i in range(len(data)):
        hasil = []
        for j in data[i]:
            if j not in hasil:
                hasil.append(j)
        merge.append(hasil)
    return merge

if __name__ == '__main__':

    # read query input
    list_kata = []
    for x in read_input():
        list_kata.append(str(x).replace('\n',''))

    # # ----- start process 1

    # # memproses kata untuk menjadi synset
    # synset_dataset = []

    # for x in list_kata:
    #     ds = 'datauji/{}.json'
    #     synset_dataset.append(alt_gen(x, open(ds.format(x)))) # synset_dataset.append(alt_gen('aborsi', open('datauji/aborsi.json'))) dan seterusnya

    # # mencetak hasil synset pada file .txt
    # output_komutatif = open('output/output komutatif.txt', 'w+')
    # for k in synset_dataset:
        
    #     # penyesuaian format data uji
    #     hapuski2 = str(k).replace('[[','[')
    #     hapuska2 = hapuski2.replace(']]',']')
    #     hapuski3 = hapuska2.replace('[[','[')
    #     hapuska3 = hapuski3.replace(']]',']')
    #     hapussp = hapuska3.replace('],',']\n')
    #     synset = hapussp.replace(' [','[')

    #     output_synset = (synset)
    #     output_komutatif.write(str(output_synset) + '\n')
    # output_komutatif.close()

    # print()
    # print('-----------')
    # print()

    # print('output komutatif.txt has been created sucsessfully')

    # print()
    # print('-----------')
    # print()

    # # ----- finish process 1

    # -----

    # ----- start process 2

    synset_temp = []
    synset = []
    for x in preprocessing(read_dataset()):
        if len(x) > 1:
            for i in range(len(x)):
                for j in range(len(list_kata)):
                    if x[i] == list_kata[j]:
                        synset_temp.append(x)
        else:
            synset_temp.append(x)               
    
    for a in range(len(synset_temp)):
        for b in range(len(list_kata)):
            if list_kata[b] in synset_temp[a]:
                synset_temp[a].remove(list_kata[b])
                synset_temp[a].insert(0, list_kata[b])
                synset.append(synset_temp[a])

    merge_synset = merge_synset(synset)
    cluster = Clustering.agglomerative_clustering(merge_synset)
    distance_value = pandas.DataFrame(cluster[1])
    # ytdist = distance_value
    # Z = hierarchy.linkage(ytdist, 'complete')
    # pyplot.figure()
    # dendrogram = hierarchy.dendrogram(Z)
    # pyplot.show()

    #tampil distance value & matrix similarity synsets
    print("Distance Value: ")
    print(distance_value)
    print(pandas.DataFrame(cluster[0]))

    #hitung similarity terbesar
    similarity = Clustering.big_similarity(cluster[0])
    print("Maximum similarity :",similarity)
    distance, distance1, distance2 = Clustering.big_distance(cluster[1])
    print("Maximum distance value :",distance)
    print("Index Distance : ", distance1, distance2)

    #hitung nilai threshold
    koefisien = 0.1
    print("Koefisien : ",koefisien)
    threshold = distance*koefisien
    print( "Threshold value : ",threshold)

    print()
    print('-----------')
    print()

    # kandidat synsets yang memiliki kata yang sama
    synset_baru = Clustering.new_synsets(merge_synset, distance1, distance2)

    # merge synsets kata yang sama
    merged_synset = Clustering.merged_synsets(synset_baru)

    looping = 1
    while (distance >= threshold):

        #print('----------------------------------------------------------------------')
        datadistance1 = distance_value

        datadistance1 = datadistance1.drop([distance1, distance2])
        datadistance1 = datadistance1.drop([distance1, distance2], axis=1)

        merge_synset.pop(distance1)
        merge_synset.pop(distance2-1)
        merge_synset.append(merged_synset)

        #print("Jumlah Baru: ", len(merge_synset))
        cluster = Clustering.agglomerative_clustering(merge_synset)
        distance_value = pandas.DataFrame(cluster[1])
        #print(distance_value)

        similarity = Clustering.big_similarity(cluster[0])
        print("Maximum similarity:", round(similarity, 2))
        distance, distance1, distance2 = Clustering.big_distance(cluster[1])
        print("Maximum distance value: ", round(distance, 2))
        #print("Index Distance: ", distance1, distance2)

        if distance >= threshold:
            #print("Looping ", looping)
            synset_baru = Clustering.new_synsets(merge_synset, distance1, distance2)
            # print("Kandidat Merge Synsets: ", synset_baru)
            merged_synset = Clustering.merged_synsets(synset_baru)
            # print("Merged Synsets Baru: ", merged_synset)
            looping = looping + 1
    
    output_clustering = "output/output Koefisien_"+str(koefisien)+".txt"
    simpan_hasil = open(output_clustering, 'w')

    kata = "\n".join(str(x) for x in merge_synset)
    simpan_hasil.write(kata)
    simpan_hasil.close()

    # ----- finish process 2

    # -----

    # ----- start process 3

    print()
    print('-----------')
    print()

    print('file output clustering has been created successfully')

    print()
    print('-----------')
    print()
    
    hasil_clustering = preprocessing(read_hasil_clustering('output/output komutatif.txt'))
    hasil_validasi = preprocessing(read_validasi())

    synset_clustering = []
    synset_validasi = []
    for i in range(0, len(hasil_clustering)):
        for j in range(0, len(hasil_validasi)):
            tmp1 = hasil_clustering[i][0]
            tmp2 = hasil_validasi[j][0]

            if tmp1 == tmp2 :
                checked = 0
                for k in range(0, len(hasil_clustering[i])):
                    tmp3 = hasil_clustering[i][k]
                    if tmp3 in hasil_validasi[j]:
                        checked = checked + 1

                if checked == len(hasil_clustering[i]):
                    synset_clustering.append(hasil_clustering[i])
                    synset_validasi.append(hasil_validasi[j])

                if checked == len(hasil_validasi[j]):
                    synset_clustering.append(hasil_clustering[i])
                    synset_validasi.append(hasil_validasi[j])

    synsets = []            

    for i in range(0, len(synset_clustering)):
        if i % 2 == 0:
            synsets.append([synset_clustering[i], synset_validasi[i]])

    print('Synset yang sama antara Program - Validasi')
    for i in range(0, len(synset_clustering)):
        if i % 2 == 0:
            if synset_clustering[i] == synset_validasi[i]:
                print(synset_clustering[i],'---',synset_validasi[i])

    print()
    print('-----------')
    print()

    print('Synset yang tidak sama antara Program - Validasi')
    for i in range(0, len(synset_clustering)):
        if synset_clustering[i] != synset_validasi[i]:
            print(synset_clustering[i],'---',synset_validasi[i])

    print()
    print('-----------')
    print()

    kata_sama = len(synsets)
    data_validasi = len(hasil_validasi)
    data_program = len(hasil_clustering)

    # perhitungan performansi
    precission = (kata_sama / data_program) * 100
    recall = (kata_sama / data_validasi) * 100
    fmeasure = 2*((precission*recall)/(precission+recall))

    print("Looping: ", looping)
    print("Precission : (",kata_sama,"/",data_program,") x 100 =",round(precission, 2))
    print("Recall : (",kata_sama,"/",data_validasi,") x 100 =",round(recall, 2))
    print("F measure : ", round(fmeasure, 2))

    # ----- finish process 3