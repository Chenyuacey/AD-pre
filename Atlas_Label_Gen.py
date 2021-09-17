import json
import os
import re

def Acronym(str):
    Str_list = str.split(' ')
    acronym = ''
    for words in Str_list:
        acronym += words[0]
    if len(acronym) == 1:
        acronym = acronym + words[1] + words[2]
    new_str = acronym
    #print(new_str)
    return new_str

def Safe_name(str):
    pattern = r'(.*),(.*)'
    if re.match(pattern,str):
        str_tmp = re.findall(pattern, str)
        new_str = str_tmp[0][0] + str_tmp[0][1]
        #print(new_str)
    else:
        new_str = str
    return new_str

def Json_Gen(label_source,label_save):
    Dict_format = ["acronym", "atlas_index_range","color_hex_triplet",\
              "failed_facet","graph_order","id","name","parent_structure_id",\
              "safe_name","st_level","structure_id_path","structure_name_facet",
              "label_color"]
    Dict = dict()
    with open(label_source,'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                pattern, pattern2= r'[0-9]\d*',r'"(.*)"'
                label,name= re.findall(pattern, line),re.findall(pattern2,line)
                #print(label,name)
                term = dict.fromkeys(Dict_format, None)
                id =  graph_order = label_color = int(label[0])
                R,G,B = hex(int(label[1])),hex(int(label[2])),hex(int(label[3]))
                color_hex_triplet = R[2:].zfill(2) + G[2:].zfill(2) + B[2:].zfill(2)
                term['graph_order'] = term['label_color'] = id
                term['id'] = id
                term['name'] = name[0]
                term['safe_name'] = Safe_name(name[0])
                term['acronym'] = Acronym(name[0])
                term['color_hex_triplet'] = color_hex_triplet
                term['failed_facet'], term['parent_structure_id'], term['st_level'], \
                term['structure_id_path'], term['structure_name_facet'] = None,None,None,None,None
                print(term)
                Dict[str(id)] = term
        print(Dict)
        with open(label_save,'a+') as f:
            json.dump(Dict,f,indent=4)



if __name__ == '__main__':
    Label_source = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_atlas_v2.label'
    Label_save = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\Structure_WHS_SD_rat_atlas_v2.json'
    Json_Gen(Label_source, Label_save)