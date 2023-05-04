from small_functions import *

def readExpID():
    path="C:\\Users\\Prototype\\PycharmProjects\\OligoPrintVacuum\\ExpID.txt"
    file=open(path,"r")
    number=file.readline()
    file.close()
    file=open(path,"w")
    file.write(str(int(number)+1))
    file.close()
    return number

class Worklist():

    def __init__(self, path):
        self.file=open(path,"w")
        self.write_line("Step name\targ1\targ2\targ3\targ4\targ5\n")

    def write_line(self,line):
        self.file.write(line)

    def close(self):
        self.file.close()

    def tip_pickup_8channels(self, labwares, wells, tipmask):
        '''
        :param labwares: list of labwares from which to pick-up
        :param wells: list of wells
        :param tipmask: serie of 1 and 0 corresponding to tipmask ex. 00111011
        :return:
        '''
        command_str="Tip_pickup_8channels\t" + list2str(labwares) + "\t" + list2str(wells) + "\t" + tipmask + "\t" + "0\n"
        self.write_line(command_str)

    def tip_eject_8channels(self, labwares, wells, tipmask):
        '''
        :param labwares: list of labwares to which eject tips
        :param wells: list of wells
        :param tipmask: serie of 1 and 0 corresponding to tipmask ex. 00111011
        :return:
        '''
        command_str="Tip_eject_8channels\t" + list2str(labwares) + "\t" + list2str(wells) + "\t" + tipmask + "\t" + "0\n"
        self.write_line(command_str)

    def aspirate_8channels(self, liquid_class, labwares, wells, volumes, tipmask):
        '''
        :param liquid_class: string corresponding to liquid class
        :param labware: list of labwares from which to aspirate
        :param wells: list of wells ex. [1,2,4,96]
        :param volumes: list of volumes, same size as the list of wells
        :param tipmask: serie of 1 and 0 corresponding to tipmask ex. 00111011
        :return:
        '''
        command_str = "Aspirate_8channels\t" + \
            liquid_class + "\t" + \
            list2str(labwares) + "\t" + \
            list2str(wells) + "\t" + \
            list2str(volumes) + "\t" +\
            tipmask +"\n"

        self.write_line(command_str)

    def dispense_8channels(self, liquid_class, labwares, wells, volumes, tipmask):
        '''
        :param liquid_class: string corresponding to liquid class
        :param labware: list of labwares to which dispense
        :param wells: list of wells ex. [1,2,4,96]
        :param volumes: list of volumes, same size as the list of wells
        :param tipmask: serie of 1 and 0 corresponding to tipmask ex. 00111011
        :return:
        '''
        command_str = "Dispense_8channels\t" + \
            liquid_class + "\t" + \
            list2str(labwares) + "\t" + \
            list2str(wells) + "\t" + \
            list2str(volumes) + "\t" +\
            tipmask +"\n"

        self.write_line(command_str)

    def dispense_onTheFly(self, liquid_class, labwares, wells, volume, tipmask):
        '''
        :param liquid_class: string corresponding to liquid class
        :param labware: list of labwares to which dispense
        :param wells: list of wells ex. [1,2,4,96]
        :param volumes: the volume to dispense
        :param tipmask: serie of 1 and 0 corresponding to tipmask ex. 00111011
        :return:
        '''
        command_str = "Dispense_OnTheFly\t" + \
            liquid_class + "\t" + \
            list2str(labwares) + "\t" + \
            list2str(wells) + "\t" + \
            str(volume) + "\t" +\
            tipmask +"\n"

        self.write_line(command_str)