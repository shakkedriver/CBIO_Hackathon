import pandas as pd
import numpy as np

#TODO parse just the erocarioties



def make_smaller_file(path):
    new_file = open('new_input.txt', 'w')
    new_file.write('##species_taxonomy_id	orthgroup_id	count\n')

    lines = []
    an = {}
    counter = 0
    with open(path) as f:
        lines = f.readlines()[1:]
        for line in lines:
            splited = line.split('\t')
            ammount = splited[2][:-2]
            if ammount >= '10':
                new_file.write(line)
                if splited[0] not in an:
                    an[splited[0]] = 1
                    counter+=1
                else:
                    an[splited[0]] += 1
            if counter == 100:
                break


def txt_to_data(path):
    lines = []
    animals = []
    seq = []
    an = {}
    with open(path) as f:
        lines = f.readlines()[1:]
        for line in lines:
            splited = line.split('\t')
            animals.append(splited[0])
            seq.append(splited[1])
            if splited[0] not in an:
                an[splited[0]] = {splited[1] : splited[2].replace('\n', '')}
            else:
                an[splited[0]][splited[1]] = splited[2].replace('\n', '')
    return animals, seq, an

def make_DF(animals, seq):
    arr = np.array([animals, seq])
    return pd.DataFrame(arr.T, columns=['animal', 'COG_ID'])

def main():
    # make_smaller_file('species.mappings.v11.5.txt')
    animals, seq, an = txt_to_data('new_input.txt')
    DF = make_DF(animals, seq)
    animal_translate = {}
    counter = 0
    for key in an.keys():
        animal_translate[key] = counter
        counter +=1
    mat, gens_vec = from_df_to_matrix(DF, an, animal_translate)
    return mat, gens_vec
    print('hi')


def from_df_to_matrix(df, an, animal_translate):

    num_of_species = len(df.animal.unique())
    cogs_list = list(df.COG_ID.unique())
    num_cogs = len(cogs_list)
    animals_vec = np.zeros((num_of_species, num_cogs))
    animals_df = pd.DataFrame(animals_vec, columns=cogs_list)
    for curr_animal in an.keys():
        for cog in an[curr_animal].keys():
            animals_df.at[animal_translate[curr_animal],cog] = 1

    distance_matrix = np.zeros((num_of_species, num_of_species))
    gens_vec = []
    for row in range(num_of_species):
        vec1 = animals_df.iloc[row]
        for col in range(num_of_species):
            vec2 =animals_df.iloc[col]
            tal = distance_func(np.array(vec1), np.array(vec2))
            distance_matrix[row,col] = tal
        gens_vec.append( vec1)
    return distance_matrix, gens_vec



def distance_func(vec1, vec2):
    tal = np.where((vec1==1) & (vec2==1),1,0)
    return sum(tal)


if __name__ == '__main__':
    main()
    # tal = 'mpwrmv\n'
    # tal = tal.replace('\n', '')
    # print(tal)
    arr = [1, 4, 4, 6, 8, 9, 8]
    arr = list(set(arr))
    print('hi')