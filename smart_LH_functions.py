from Labware import *
from small_functions import*

def multi_buffer_8channels(worklist, tip_source, tip_assignment, dest_labware:Labware, dispense_list):
    '''
    worklist = worklist handle
    tip_assignment = list of 8 3-tuple telling for each tip [buffer,labware,well] from which to aspirate
    tip_source = list of 8 2-tuple telling for each tip [labware,well] from which fetch and unfetch tips
    dest_labware = labware we want to dispense in
    dispense_list = dictionnary of well:[buffer,volume]
    '''


    MAX_TIP_VOLUME=900
    LIQUID_CLASS_ASPIRATE="HighVolume_Premix_DispenseJet_Part"
    LIQUID_CLASS_DISPENSE="HighVolume_Premix_DispenseJet_Part"

    aspirate_vols=[0,0,0,0,0,0,0,0]
    tips_to_fetch=[0,0,0,0,0,0,0,0]
    asp_disp_stack=[]
    disp_stack=[] # = list of [tip_to_use,well,volume]
    refill_need=0

    for col in range(dest_labware.nb_cols):
        first_well = col*dest_labware.nb_rows+1
        accepted_wells = [well for well in range(first_well,first_well+dest_labware.nb_rows)]

        #we keep going with that column until all wells have been treated
        while (any(well in accepted_wells for well in dispense_list.keys())):
            tips_positions = [first_well - 7, first_well - 6, first_well - 5, first_well - 4, first_well - 3,first_well - 2, first_well - 1, first_well]
            next_disp=[]
            best_next_disp = []
            #Find the best dispense
            while tips_positions[0]<=accepted_wells[-1]:
                potential_nextdisp=[]
                tips_positions_filtered = filter_tips_position(tips_positions,accepted_wells)
                #print(tips_positions_filtered)
                for tip in range(0,8):
                    well=tips_positions_filtered[tip]
                    if well>0 and well in dispense_list.keys() and dispense_list[well][0]==tip_assignment[tip][0]:
                        potential_nextdisp.append([tip,well,dispense_list[well][1]])

                if len(potential_nextdisp)>len(best_next_disp):
                    best_next_disp=potential_nextdisp
                tips_positions=[tip_position+1 for tip_position in tips_positions ]

            #Apply the best dispense if possible

            for disp in best_next_disp:
                if aspirate_vols[disp[0]]+disp[2]>MAX_TIP_VOLUME:
                    refill_need=1
                else:
                    aspirate_vols[disp[0]] += disp[2]
                    next_disp.append(disp)
                    tips_to_fetch[disp[0]]=1
                    del dispense_list[disp[1]]

            if next_disp!=[]:
                disp_stack.append(next_disp)

            if refill_need or len(dispense_list)==0:
                asp_disp_stack.append(['Asp',aspirate_vols])
                aspirate_vols=[0,0,0,0,0,0,0,0]
                for disp_step in disp_stack:
                    asp_disp_stack.append(['Disp',disp_step])
                disp_stack=[]
                refill_need=0

    print(asp_disp_stack)
    print(tips_to_fetch)
    tipmask_fetching=list2tipmask(tips_to_fetch)

    worklist.tip_pickup_8channels(filter_tipmask([tipsource[0] for tipsource in tip_source],tipmask_fetching),
                                  filter_tipmask([tipsource[1] for tipsource in tip_source],tipmask_fetching),
                                  tipmask_fetching)

    for asp_disp in asp_disp_stack:

        print(asp_disp)
        if asp_disp[0]=="Asp":
            worklist.aspirate_8channels(LIQUID_CLASS_ASPIRATE,
                                        [tip_ass[1] for tip_ass in tip_assignment],
                                        [tip_ass[2] for tip_ass in tip_assignment],
                                        asp_disp[1],
                                        list2tipmask(asp_disp[1]))
        if asp_disp[0] == "Disp":
            volumes_to_disp=[0,0,0,0,0,0,0,0]
            for disp in asp_disp[1]:
                volumes_to_disp[disp[0]]=disp[2]
            worklist.dispense_8channels(LIQUID_CLASS_DISPENSE,
                                        [dest_labware.name] * len(asp_disp[1]),
                                        int_list2well_list([disp[1] for disp in asp_disp[1]],dest_labware),
                                        volumes_to_disp,
                                        disp2tipmask(asp_disp[1]))

    worklist.tip_eject_8channels(filter_tipmask([tipsource[0] for tipsource in tip_source], tipmask_fetching),
                                  filter_tipmask([tipsource[1] for tipsource in tip_source], tipmask_fetching),
                                  tipmask_fetching)

def onTheFly_8channels(worklist,tip_boxes,tip_columns,tip_assignment, nuc_assignment, dest_labware ,disp_list):

    volume_to_disp = disp_list[1][1]
    MAX_TIP_VOLUME = 900
    LIQUID_CLASS_ASPIRATE = "HighVolume_Premix_DispenseJet_Part"
    LIQUID_CLASS_DISPENSE = "HighVolume_Premix_DispenseJet_Part"

    for nucleotide_stack in range(len(tip_assignment)):

        disp_list_nuc_stack=filter_disp_list_by_nuc(disp_list,tip_assignment[nucleotide_stack])
        tips_to_fetch= [0, 0, 0, 0, 0, 0, 0, 0]
        disp_stack=[]
        asp_disp_stack=[]

        while len(disp_list_nuc_stack.keys()) != 0:
            print(disp_list_nuc_stack)

            tip_volume = [0, 0, 0, 0, 0, 0, 0, 0]
            refill_needed = 0

            row_of_each_tip=[-5, -4 ,-3 ,-2 ,-1 ,0 ,1 ,2 ]

            for line_offset in range(7):
                if refill_needed:
                    break
                wells_to_disp = []
                for col in range(1,12+1):
                    if refill_needed:
                        break

                    for tip in range(8):

                        if row_of_each_tip[tip] + line_offset*2 < 1 or row_of_each_tip[tip] + line_offset*2 >8 :
                            continue
                        else:
                            well= (col-1)*8 + row_of_each_tip[tip] + line_offset*2

                        if well in disp_list_nuc_stack.keys() and disp_list_nuc_stack[well][0]==tip_assignment[nucleotide_stack][tip]:
                            vol_to_disp = disp_list_nuc_stack[well][1]
                            if tip_volume[tip]+vol_to_disp<=MAX_TIP_VOLUME:
                                wells_to_disp.append(well)
                                tip_volume[tip]+=vol_to_disp
                                disp_list_nuc_stack.pop(well,None)
                                tips_to_fetch[tip]=1
                            else:
                                refill_needed=1
                                break

                disp_stack.append([line_offset,wells_to_disp])

            asp_disp_stack.append(['Asp', tip_volume])
            for disp_step in disp_stack:
                asp_disp_stack.append(['Disp', disp_step])
            disp_stack = []


        if asp_disp_stack!=[]:

            print(asp_disp_stack)
            print(tips_to_fetch)
            tipmask_fetching = list2tipmask(tips_to_fetch)

            worklist.tip_pickup_8channels([tip_boxes[nucleotide_stack]]*tips_to_fetch.count(1),
                                          filter_tipmask([(tip_columns[nucleotide_stack]-1)*8 + row +1 for row in range(8)], tipmask_fetching),
                                          tipmask_fetching)

            for asp_disp in asp_disp_stack:

                print(asp_disp)
                if asp_disp[0] == "Asp":
                    worklist.aspirate_8channels(LIQUID_CLASS_ASPIRATE,
                                                [nuc_assignment[tip] for tip in tip_assignment[nucleotide_stack]],
                                                filter_tipmask([1,2,1,2,1,2,1,2],list2tipmask(asp_disp[1])),
                                                asp_disp[1],
                                                list2tipmask(asp_disp[1]))
                if asp_disp[0] == "Disp":
                    wells_to_disp=asp_disp[1][1]
                    tipmask= tipmask_from_line_offset(asp_disp[1][0])
                    worklist.dispense_onTheFly(LIQUID_CLASS_DISPENSE,
                                                [dest_labware.name] * len(wells_to_disp),
                                                int_list2well_list(wells_to_disp, dest_labware),
                                                vol_to_disp,
                                                tipmask)

            worklist.tip_eject_8channels([tip_boxes[nucleotide_stack]]*tips_to_fetch.count(1),
                                      filter_tipmask([(tip_columns[nucleotide_stack]-1)*8 + row +1 for row in range(8)], tipmask_fetching),
                                      tipmask_fetching)




if __name__ == "__main__":

    print('ok')