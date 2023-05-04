import xlrd

path = r'hamilton_control.xlsx'



def getExcelSheet(path):
    wb = xlrd.open_workbook(path)
    synthesis_sheet = wb.sheet_by_name("Syntheses")
    return synthesis_sheet

def getSequences(synthesis_sheet):

    sequences=[]
    well=1
    for col in range(12):
        for row in range(8):
            value=synthesis_sheet.cell_value(7+row,1+col)
            if value!='':
                sequences.append((well,value))
            well+=1

    return sequences

def splitSequences(sequences,cycle):

    ended_wells = []
    A_wells=[]
    C_wells=[]
    G_wells=[]
    T_wells=[]
    M_wells=[]
    N_wells=[]

    nucleos=['A','C','G','T','M','N']
    nucleo_arrays=[ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells]

    for nucleo in range(1,6+1):
        for sample in range(len(sequences)):
            if (cycle<=len(sequences[sample][1]) and sequences[sample][1][cycle-1]==nucleos[nucleo-1]):
                nucleo_arrays[nucleo].append(sequences[sample][0])

    for sample in range(len(sequences)):
        if cycle > len(sequences[sample][1]):
            ended_wells.append(sequences[sample][0])

    return nucleo_arrays


def getUsedWells(sequences):
    #returns all the wels in the synthesis
    usedWells=[]
    for sample in sequences:
        usedWells.append(sample[0])
    return usedWells

def getActiveWells(sequences,cycle):
    #Return all the wells in the synthesis minus the finished ones
    usedWells=getUsedWells(sequences)
    ended_wells=splitSequences(sequences,cycle)[0]
    activeWells=[]

    for well in usedWells:
        if well not in ended_wells:
            activeWells.append(well)

    return activeWells

def findIndexes(eltToFind,synthesis_sheet):

    for row in range(synthesis_sheet.nrows):
        for col in range(synthesis_sheet.ncols):
            if synthesis_sheet.cell_value(row,col)==eltToFind:
                return (row,col)



if __name__ == "__main__":

    synthesis_sheet=getExcelSheet(path)
    sequences=getSequences(synthesis_sheet)
    nucleo_arrays=splitSequences(sequences,1)
    print(sequences)
    print(nucleo_arrays[0])
    print(nucleo_arrays[1])
    print(nucleo_arrays[2])
    print(nucleo_arrays[3])
    print(nucleo_arrays[4])
    #params=getParameters(synthesis_sheet)
    print(getUsedWells(sequences))
    print(getActiveWells(sequences,4))