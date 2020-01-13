import os
import sys


class Cli():

    @staticmethod
    def ask_for_exit(message):
        user_input = input(message + '\nDo you want to \n'
                                     ' [c] continue \n'
                                     ' [x] exit \n')
        if user_input == 'x':
            sys.exit()

    @staticmethod
    def skip_existing_files(file_path):
        skip = None
        for_all = False
        if os.path.isfile(file_path):
            user_input = input(
                '\nThe file %s already exists. \n'
                'Do you want to \n'
                ' [y] continue anyways\n'
                ' [c] continue anyways for all files\n'
                ' [n] skip this file\n'
                ' [s] skip all existing files\n'
                ' [x] exit \n' % (file_path))
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
