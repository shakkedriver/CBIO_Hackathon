import pandas as pd
import numpy as np
import random
#TODO parse just the erocarioties

import os

# def make_smaller_file(path):
#     new_file = open('new_input.txt', 'w')
#     new_file.write('##species_taxonomy_id	orthgroup_id	count\n')
#
#     lines = []
#     an = {}
#     counter = 0
#     with open(path) as f:
#         lines = f.readlines()[1:]
#         for line in lines:
#             splited = line.split('\t')
#             ammount = splited[2][:-2]
#             if ammount >= '10':
#                 new_file.write(line)
#                 if splited[0] not in an:
#                     an[splited[0]] = 1
#                     counter+=1
#                 else:
#                     an[splited[0]] += 1
#             if counter == 100:
#                 break

def all_animal_dic(path):
    lines = []
    an = {}
    with open(path) as f:
        lines = f.readlines()[1:]
        for line in lines:
            splited = line.split('\t')
            if splited[0] not in an:
                an[splited[0]] = {splited[1]:splited[2].replace('\n', '')}
            else:
                an[splited[0]][splited[1]] = splited[2].replace('\n', '')
        return an

def dic_random_input_file(an, iteration):
    animalslist = list(an.keys())
    chosen_animals = random.sample(animalslist,400)
    new_file = open('new_input'+str(iteration)+'.txt', 'w')
    new_file.write('##species_taxonomy_id	orthgroup_id	count\n')
    for animal in chosen_animals:
        for cog in an[animal].keys():
            new_file.write(animal+"\t"+cog+"\t"+an[animal][cog]+'\n')
    new_file.close()

def make_k_random_files(k):
    an = all_animal_dic('species.mappings.v11.5.txt')
    index_file = 1
    while index_file <= k:
        dic_random_input_file(an, index_file)
        index_file+=1

def main2():
    make_k_random_files(5)

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

def data_permutation_bonus(pre_abs_matrix):
    prev_mat = pre_abs_matrix.copy()

    for i in tqdm.tqdm(range(10**6)):
        ret_mat, flag = find_circle_and_replace(prev_mat)
        if flag:
            prev_mat = ret_mat

    return prev_mat

def find_circle_and_replace(prev_matrix):
    new_matrix = prev_matrix.copy()
    num_rows = prev_matrix.shape[0]
    num_cols = prev_matrix.shape[1]
    row_p_1 = random.randint(0, num_rows-1)
    col_p_1 = random.randint(0, num_cols-1)

    row_p_2 = random.randint(0, num_rows-1)
    col_p_2 = random.randint(0, num_cols-1)

    counter = 0
    while((row_p_1 == row_p_2) and (counter < 10)):
        row_p_2 = random.randint(0, num_rows-1)
        counter = counter + 1

    if row_p_1 == row_p_2:
        return (np.empty((1,1)),False)

    counter2 = 0
    counter2_flag = True
    while((col_p_1 == col_p_2) or (prev_matrix[row_p_1, col_p_1] != prev_matrix[row_p_2, col_p_2])):
        if counter2 >= 10:
            counter2_flag = False
            break

        col_p_2 = random.randint(0, num_cols-1)
        counter2 = counter2 + 1

    if not counter2_flag:
       return (np.empty((1, 1)), False)

    # here we know we have two edges to the circle
    circle_x = [row_p_1, col_p_1]
    circle_y = [row_p_2, col_p_2]

    circle_z = [row_p_1, col_p_2]
    circle_w = [row_p_2, col_p_1]

    if (prev_matrix[circle_z[0], circle_z[1]] == prev_matrix[circle_w[0], circle_w[1]]) and\
            (prev_matrix[circle_z[0], circle_z[1]] != (prev_matrix[circle_x[0], circle_x[1]])):
            # found good circle
            # 1 become 0, 0 become 1
            new_matrix[circle_x[0], circle_x[1]] = 1 - prev_matrix[circle_x[0], circle_x[1]]
            new_matrix[circle_y[0], circle_y[1]] = 1 - prev_matrix[circle_y[0], circle_y[1]]

            new_matrix[circle_z[0], circle_z[1]] = 1 - prev_matrix[circle_z[0], circle_z[1]]
            new_matrix[circle_w[0], circle_w[1]] = 1 - prev_matrix[circle_w[0], circle_w[1]]
            return (new_matrix, True)

    return (np.empty((1, 1)), False)



if __name__ == '__main__':
    main()
