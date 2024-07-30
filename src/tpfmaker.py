import numpy as np

class tpf_block:
    """
    tpfit の入力コード　INT1に関するモジュール
    """
    def __init__(self,cmd, list_code=[]):
        """
        INT1クラスのコンストラクタ
        Args:
            
        """
        self.__cmd = cmd
        self.__list_code = list_code

    @property
    def list_code(self):
        return self.__list_code
    
    @list_code.setter
    def list_code(self, value):
        self.__list_code = value

    @property
    def cmd(self):
        return self.__cmd
    
    @cmd.setter
    def cmd(self, value):
        self.__cmd = value
    
    def write_code(self,path_tpf):
        with open(path_tpf, 'w') as f:
            print(self.cmd)
            f.write(f'{self.cmd}\n')

            for code in self.list_code:
                for para in code:
                    f.write(f'{para} ')
                f.write('\n')
            f.write('END\n')
            print("end")