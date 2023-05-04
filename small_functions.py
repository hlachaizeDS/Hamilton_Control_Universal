from Labware import *

def filter_disp_list_by_nuc(disp_list,nucs):

    new_dict=dict()
    for (key,value) in disp_list.items():
        if value[0] in nucs:
            new_dict[key]=value

    return new_dict

def filter_tips_position(tips_positions,accepted_wells):

    tips_positions_filtered=[]
    for tip_position in tips_positions:
        if tip_position in accepted_wells:
            tips_positions_filtered.append(tip_position)
        else:
            tips_positions_filtered.append(0)

    return tips_positions_filtered

def list2str(list):
    string=""
    for item in list:
        string = string + str(item) + ";"

    return string[:-1]

def list2tipmask(list):
    # if an element of the list is != 0, puts 1
    tipmask=""
    for item in list:
        if int(item)>0 :
            tipmask += "1"
        else:
            tipmask += "0"

    return tipmask

def filter_tipmask(list,tipmask):
    # list is a list (of 8 elements)
    # tipmask is a 8 character string of 0 and 1
    # returns the elements of the list only if there's 1 in the tipmask for that position
    filtered_list=[]
    for id in range(len(list)):
        if tipmask[id]=="1":
            filtered_list.append(list[id])

    return filtered_list

def disp2tipmask(disp):
    list_tipmask=[0,0,0,0,0,0,0,0]

    for well_to_disp in disp:
        list_tipmask[well_to_disp[0]]=1

    return list2tipmask(list_tipmask)

def well_col(well,nb_rows,nb_cols):
    return (well-1) // nb_rows + 1

def well_row(well,nb_rows,nb_cols):
    return (well-1) % nb_rows + 1

def int2well(well,nb_rows,nb_cols):
    col=well_col(well,nb_rows,nb_cols)
    row=well_row(well,nb_rows,nb_cols)
    return chr(65+row-1) + str(col)

def int_list2well_list(int_list,labware:Labware):

    return [int2well(int_well,labware.nb_rows,labware.nb_cols) for int_well in int_list]

def tipmask_from_line_offset(line_offset):

    tipmask=""

    first_tip= 7 - (line_offset)*2
    last_tip = 14 - (line_offset)*2
    for tip in range(8):
        if tip+1 < first_tip or tip+1 > last_tip:
            tipmask+="0"
        else:
            tipmask+="1"
    return tipmask