import logging
from datetime import datetime

ERROR_TERMINAL_INPUT = 'Error: unknown command'

class COLORS:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  ENDC = '\033[0m'

class Terminal:
    def __init__(self):
        logging.basicConfig(filename=f'log/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    def p_user(self, msg, username, user_id):
      print(COLORS.BOLD + f'[{datetime.now().replace(second=0, microsecond=0)}]' + COLORS.ENDC + COLORS.OKGREEN + f' USER {user_id} "{username}": "{msg}"' + COLORS.ENDC)
      logging.info(f'"USER" "{user_id}" "{username}" "{msg}"')

    def p_bot(self, msg, user_id):
        print(COLORS.BOLD + f'[{datetime.now().replace(second=0, microsecond=0)}]' + COLORS.ENDC + COLORS.OKBLUE + f' ASSISTANT {user_id}: "{msg}"' + COLORS.ENDC)
        logging.info(f'"ASSISTANT" "{user_id}" "{msg}"')

    def p_system(self, msg, user_id=None, input_mode=False):
        if input_mode == False:
            if user_id != None:
                print(COLORS.BOLD + f'[{datetime.now().replace(second=0, microsecond=0)}]' + COLORS.ENDC + f' SYSTEM {user_id}: "{msg}"')
                logging.info(f'"SYSTEM" "{user_id}" "{msg}"')
            else:
                print(COLORS.BOLD + f'[{datetime.now().replace(second=0, microsecond=0)}]' + COLORS.ENDC + f' SYSTEM: "{msg}"')
                logging.info(f'"SYSTEM" "{msg}"')
        else:
            logging.info(f'"SYSTEM(admin)" "{msg}"')

    def p_error(self, msg):
        print(COLORS.BOLD + f'[{datetime.now().replace(second=0, microsecond=0)}]' + COLORS.ENDC + COLORS.FAIL + f' ERROR: "{msg}"' + COLORS.ENDC)
        logging.info(f'"ERROR" "{msg}"')

    @staticmethod
    def run_admin_terminal(terminal, db):
      while True:
          command = input()
          terminal.p_system(command, None, True)
          command_splt = command.split()
          if command_splt[0] == "users":
              terminal.p_system(db.get_users())
          elif command_splt[0] == "history":
              if len(command_splt) == 2 and command_splt[1].isdigit():
                  terminal.p_system(db.get_history(int(command_splt[1])))
              else:
                  terminal.p_error(ERROR_TERMINAL_INPUT)
          elif command_splt[0] == "reset":
              if len(command_splt) == 2 and command_splt[1].isdigit():
                  db.delete_history(int(command_splt[1]))
                  terminal.p_system(f'User {command_splt[1]} history cleared.')
              else:
                  terminal.p_error(ERROR_TERMINAL_INPUT)
          else:
              terminal.p_error(ERROR_TERMINAL_INPUT)

