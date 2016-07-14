#!/bin/python3

import threading
import time
import subprocess
import curses

class VBox(threading.Thread):
    def __init__(self):
        self.vms = []
        self.stop = 0
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.set_vms()
            if self.stop == 1:
                break
            time.sleep(1)

    def stop_thread(self):
        self.stop = 1
        self.join()

    def set_vms(self):
        vms = []
        cmd = ['VBoxManage', 'list', 'vms']
        for i, item in enumerate(self.call_command(cmd)):
            vms_record = self.get_info(i, item)
            vms.append(vms_record)
        self.vms = []
        self.vms = vms

    def get_info(self, index, string):
        vms = {}
        vms['id'] = index + 1
        vms['name'] = string.split('"')[1]
        vms['uuid'] = string.split(' ')[-1]
        vms['os_type'] = self.vm_os_type(vms['uuid'])
        vms['memory'] = self.vm_memory(vms['uuid'])
        vms['status'] = self.vm_status(vms['uuid'])
        return vms

    def vm_status(self, uuid):
        cmd = ['VBoxManage', 'list', 'runningvms']
        for vm in self.call_command(cmd):
            if vm.find(uuid) >= 0:
                return 'RUNNING'
        return 'OFF'

    def vm_memory(self, uuid):
        memory = ""
        cmd = ['VBoxManage', 'showvminfo', uuid]
        for line in self.call_command(cmd):
            if line.find("Memory size:") >= 0:
                memory = line.split()[2]
        return memory
        
    def vm_os_type(self, uuid):
        os_type = ""
        cmd = ['VBoxManage', 'showvminfo', uuid]
        for line in self.call_command(cmd):
            if line.find("Guest OS:") >= 0:
                os_type = line.split()[2:]
        return " ".join(os_type)

    # output is send to /dev/null
    def run_command(self, cmd):
        with open('/dev/null', 'w') as null:
            with subprocess.Popen(cmd, stdout=null, stderr=null) as proc:
                proc.communicate()

    # this will return output
    def call_command(self, cmd):
        with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
            output = proc.communicate()[0].decode().split('\n')
        output.pop()
        return output

    def run_vm(self, index):
        cmd = ['VBoxManage', 'startvm', self.vms[index]['uuid'], '--type', 'headless']
        self.run_command(cmd)

    def stop_vm(self, index):
        cmd = ['VBoxManage', 'controlvm', self.vms[index]['uuid'], 'poweroff']
        self.run_command(cmd)
