import os
import sys

class UserInteractor():

    @staticmethod
    def check_if_file_exisits(file_path): #todo naming
        skip = None
        for_all = False
        if os.path.isfile(file_path):
            user_input = input(
                '\nThe file ' + file_path + ' already exists. \n'
                                          'Do you want to \n'
                                          ' [y] continue anyways\n'
                                          ' [c] continue anyways for all files\n'
                                          ' [n] skip this file\n'
                                          ' [s] skip all existing files\n'
                                          ' [x] chancel \n')
            if user_input == 'x':
                sys.exit()
            elif user_input == 'c':
                skip = False
                for_all = True
            elif user_input == 'n':
                skip = True
            elif user_input == 's':
                skip = True
                for_all = True
        return skip, for_all