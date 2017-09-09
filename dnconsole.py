import os
import get_console_opt


class Dnconsole:
    def __init__(self, path: str):
        self.console = get_console_opt.get_console_output
        self.basic_command = os.path.join(path, 'dnconsole.exe')
        self.method = ['name', 'index']
        self.not_exist = "player don't exist!"
        if not os.path.isfile(self.basic_command):
            raise LookupError('Dnconsole not found.')

    def run(self, command: str):
        stdout, stderr = self.console(command)
        if stdout:
            if stdout == self.not_exist:
                raise IOError('player not exist!')
            else:
                return stdout
        elif stderr:
            raise IOError(stderr)

    def quit(self, method: str, n: str):
        """
        退出特定模擬器
        :param method: name or index
        :param n: name or index of emulator

        """
        if method in self.method:
            command = f'{self.basic_command} quit --{method} {str(n)}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def quitall(self):
        """
        退出所有模擬器
        :return:
        """
        command = f'{self.basic_command} quitall'
        self.run(command)

    def launch(self, method: str, n: str):
        """
        執行模擬器 N
        :param method:index | name
        :param n: n of index | n of name
        :return: None
        """
        if method in self.method:
            command = f'{self.basic_command} launch --{method} {str(n)}'
            self.run(command)

        else:
            raise TypeError('method wrong.')

    def reboot(self, method: str, n: str):
        """
        直接重啟模擬器
        :param method: index | name
        :param n: n of index | n of name
        :return: None
        """
        if method is self.method:
            command = f'{self.basic_command} reboot --{method} {n}'
            self.run(command)

        else:
            raise TypeError('method wrong.')

    def list(self) -> list:
        """
        取得模擬器名稱列表
        :return: list of name
        """
        command = f'{self.basic_command} list'
        opt = self.run(command)
        if opt:
            index = opt.split('\n')
            res = [x for x in index if len(x) > 0]
            return res

    def runninglist(self) -> list:
        """
        正在執行之模擬器名稱
        :return: list of name
        """
        command = f'{self.basic_command} runninglist'
        opt = self.run(command)

        if opt:
            index = opt.split('\n')
            res = [x for x in index if len(x)]
            return res

    def isrunning(self, method: str, n: str) -> bool:
        """
        返回模擬器是否執行中
        :param method: index | name
        :param n: n of index | n of name
        :return: bool
        """
        if method in self.method:
            command = f'{self.basic_command} isrunning --{method} {n}'
            opt = self.run(command)
            if opt:
                if opt == 'running':
                    return True
                elif opt == 'stop':
                    return False

    def list2(self) -> list:
        """
        返回list2 包含HWID 執行狀態
        :return: dict of res
        """
        command = f'{self.basic_command} list2'
        opt = self.run(command)
        temp = opt.split('\n')
        temp = [string.split(',') for string in temp if len(string) > 0]
        if temp:
            res = [{'index': index, 'name': name, 'Hwnd': Hwnd, 'Cwnd': Cwnd, 'android_running': android_running,
                    'P_PID': P_PID, "VBOX_PID": VBOX_PID} for index, name, Hwnd, Cwnd, android_running, P_PID, VBOX_PID
                   in temp]
            return res

    def add(self, n: str):
        """
        添加新模擬器
        :param n: name
        :return: None
        """
        command = f'{self.basic_command} add --name {n}'
        self.run(command)

    def copy(self, n: str, from_n: str):
        """
        複製模擬器從名稱到名稱
        :param n: name
        :param from_n: name of emulator to copy from
        :return: None
        """
        command = f'{self.basic_command} copy --name {n} --from {from_n}'
        self.run(command)

    def remove(self, method: str, n: str):
        """
        移除模擬器
        :param method:index | name
        :param n: n of index | n of name
        :return: None
        """
        if method in self.method:
            command = f'{self.basic_command} remove --{method} {n}'
            opt = self.run(command)
            if opt == "player don't exist!":
                raise IOError('player not exist!')
        else:
            raise TypeError('method wrong.')

    def rename(self, method: str, n: str, title: str):
        """
        重新命名模擬器
        :param method: index | name
        :param n: n of index | n of name
        :param title: new name of emulator
        :return: None
        """
        if method in self.method:
            command = f'{self.basic_command} rename --{method} {n} --title {title}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def modify(self, method: str, n: str, **kwargs):
        """
        修改模擬器設定
        :param method:
        :param n:
        :param kwargs:resolution , cpu , memory, manufacturer, model, pnumber, imei, imsi, simserail, androidid, mac, autorotate, lockwindow
        :return:
        """
        if method in self.method:
            if not kwargs:
                raise KeyError('must have kwargs to run.')
            command = f'{self.basic_command} modify --{method} {n}'
            temp_string = " "
            for key, value in kwargs.items():
                temp_string += f'--{key} {value}'
            command = command + temp_string
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def installapp(self, method: str, n: str, filename: str):
        """
        安裝app
        :param method: index | name
        :param n: n of index | n of name
        :param filename: target apk to install
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} installapp --{method} {n} --filename {filename}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def uninstallapp(self, method: str, n: str, apkname: str):
        """
        移除app
        :param method: index | name
        :param n: n of index | n of name
        :param apkname: name of apk
        :return: None
        """
        if method in self.method:
            command = f'{self.basic_command} uninstallapp --{method} {n} --packagename {apkname}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def runapp(self, method: str, n: str, apkname: str):
        """
        執行app
        :param method: index | name
        :param n: n of index | n of name
        :param apkname: name of apk in android
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} --runapp --{method} {n} --packagename {apkname}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def killapp(self, method: str, n: str, apkname: str):
        """
        強制終止指定app
        :param method: index | name
        :param n:  n of index | n of name
        :param apkname: name of apk in android
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} killapp --{method} {n} --packagename {apkname}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def locate(self, method: str, n: str, LLI: str):
        """
        指定模擬器GPS位置
        :param method: index | name
        :param n: n of index | n of  name
        :param LLI: lng , lat
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} locate --{method} {n} --LLI {LLI}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def adb(self, method: str, n: str, cmd: str):
        """
        對指定模擬器adb操作
        :param method: index | name
        :param n: n of index | n of name
        :param cmd: command in adb ex. shell screencap
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} adb --{method} {n} --command {cmd}'
            opt = self.run(command)
            if opt:
                return opt
        else:
            raise TypeError('method wrong.')

    def setprop(self, method: str, n: str, key: str, value: str):
        if method in self.method:
            command = f'{self.basic_command} setprop --{method} {n} --key {key} --value {value}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def getprop(self, method: str, n: str, key: str):
        if method in self.method:
            command = f'{self.basic_command} getprop --{method} {n} --key {key}'
            opt = self.run(command)
            if opt:
                return opt
        else:
            raise TypeError('method wrong.')

    def downcpu(self, method: str, n: str, rate: str):
        """
        降低模擬器VM cpu 使用率
        :param method: index | name
        :param n: n of index | n of name
        :param rate: 1~100
        :return: None
        """
        if method in self.method:
            command = f'{self.basic_command} downcpu --{method} {n} --rate {rate}'
            opt = self.run(command)
            if opt:
                return opt
        else:
            raise TypeError('method wrong.')

    def backup(self, method: str, n: str, tofilepath: str):
        """
        備份指定模擬器
        :param method: index | name
        :param n: n of index | n of name
        :param tofilepath: path of target file
        :return:
        """
        if method in self.method:
            command = f'{self.basic_command} backup --{method} {n} --file {tofilepath}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def restore(self, method: str, n: str, fromfilepath: str):
        """
        從映像恢復到指定模擬器
        :param method:index | name
        :param n: n of index | n of name
        :param fromfilepath: path of file
        :return:None
        """
        if method in self.method:
            command = f'{self.basic_command} restore --{method} {n} --file {fromfilepath}'
            self.run(command)
        else:
            raise TypeError('method wrong.')

    def action(self, method: str, n: str, key: str, value: str):
        """
        執行動態命令
        :param method: name | index
        :param n: n of name | n of index
        :param key: reboot|keyboard|locate|shake|input
        :param value: apkname | keyname:back/home/menu/volumeup/volumedown | lng,lnt | null | text
        :return:None
        """
        key_list = ['reboot', 'keyboard', 'locate', 'shake', 'input']
        if method in self.method and key in key_list:
            command = f'{self.basic_command} action --{method} {n} --key call.{key} --value {value}'
            self.run(command)
        else:
            raise TypeError('method wrong.')


if __name__ == "__main__":
    dn = Dnconsole('C:\ChangZhi2\dnplayer2\\')
    print(dn.isrunning('name', '1'))
    print(dn.list2())
