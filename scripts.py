from excelRead import *
from Labware import *
from Worklist import *
from smart_LH_functions import *

def Example():

    synthesis_sheet = getExcelSheet(path)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)

    # Open worklist
    WL = Worklist("worklist.txt")

    # Initialize labwares
    synthesis_plate = Labware("synthesis_plate", 8, 12)
    A_reservoir = Labware("A_reservoir",8,1)
    C_reservoir = Labware("C_reservoir",8,1)
    G_reservoir = Labware("G_reservoir",8,1)
    T_reservoir = Labware("T_reservoir",8,1)

    nucs_list=["A","C","G","T"]
    reservoir_list=[A_reservoir,C_reservoir,G_reservoir,T_reservoir]
    tips_labware="Tips_1000_1"
    tips_wells=[1,2,3,4]

    for nuc in range(4):
        print("Dispensing " + nucs_list[nuc])

        WL.tip_pickup_8channels("Tips_1000_1",[nuc+1],"10000000")

        for well in nucleo_arrays[nuc+1]:
            WL.aspirate_8channels("HighVolume_Water_DispenseJet_Empty",reservoir_list[nuc].name,[1],[50],"10000000")
            WL.dispense_8channels("HighVolume_Water_DispenseJet_Empty","synthesis_plate",[int2well(well,8,1)],[50],"10000000")

        WL.tip_eject_8channels("Tips_1000_1",[nuc+1],"10000000")
    # Close worklist
    WL.close()

def DNA_synthesis():

    synthesis_sheet = getExcelSheet(path)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)

    # Open worklist
    WL = Worklist("worklist.txt")

    # Initialize labwares
    synthesis_plate = Labware("FilterPlate", 8, 12)

    #Create_dispense_list
    vol_to_disp=400
    disp_list = {}
    nuc_name=["A","C","G","T"]
    for nuc in range(1,5):
        for well in nucleo_arrays[nuc]:
            disp_list[well]=[nuc_name[nuc-1],vol_to_disp]



    #RAD

    tip_source = [["Tips_1000_1", 1], ["Tips_1000_1", 2], ["Tips_1000_1", 3], ["Tips_1000_1", 4], ["Tips_1000_1", 5],
                  ["Tips_1000_1", 6], ["Tips_1000_1", 7], ["Tips_1000_1", 8]]

    tip_assignment = [["A", "PremixA", 1], ["A", "PremixA", 2], ["C", "PremixC", 1], ["C", "PremixC", 2],
                      ["G", "PremixG", 1], ["G", "PremixG", 2], ["T", "PremixT", 1], ["T", "PremixT", 2]]

    dispense_list = {1:["A",25],2:["C",50],3:["G",50],4:["T",50],5:["T",50],6:["A",50]}

    multi_buffer_8channels(WL, tip_source, tip_assignment, synthesis_plate, disp_list)

    # Close worklist
    WL.close()

def onTheFly_nucs_disp():

    synthesis_sheet = getExcelSheet(path)
    sequences = getSequences(synthesis_sheet)
    nucleo_arrays = splitSequences(sequences, 1)

    # Open worklist
    WL = Worklist("worklist.txt")

    # Initialize labwares
    synthesis_plate = Labware("FilterPlate", 8, 12)

    #Create_dispense_list
    vol_to_disp=25
    disp_list = {}
    nuc_name=["A","C","G","T"]
    for nuc in range(1,5):
        for well in nucleo_arrays[nuc]:
            disp_list[well]=[nuc_name[nuc-1],vol_to_disp]



    #RAD

    tip_boxes=["Tips_1000_1","Tips_1000_1"]
    tip_columns=[1,3]
    tip_assignment = [["A","A","C","C","G","G","T","T"],["M","M","N","N","O","O","P","P"]]
    nuc_assignment = {"A":"PremixA","C":"PremixC","G":"PremixG","T":"PremixT",
                      "M":"PremixM","N":"PremixN","O":"PremixO","P":"PremixP"}



    onTheFly_8channels(WL, tip_boxes, tip_columns, tip_assignment, nuc_assignment, synthesis_plate, disp_list)


    # Close worklist
    WL.close()