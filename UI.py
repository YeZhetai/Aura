import wx
import threading
import random
import aura
import time
import asyncio


class WorkerThread(threading.Thread):
    def __init__(self, thread_num=0):
        threading.Thread.__init__(self)
        self.thread_num = thread_num
        self.stopped = False

    def stop(self):
        self.stopped = True

    def run(self):
        subthread = threading.Thread()
        subthread.setDaemon(True)
        subthread.start()

        while not self.stopped:
            aura.main_process()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Aura')
        self.threads = []
        self.count = 0

        panel = wx.Panel(self)
        startBtn = wx.Button(panel, -1, 'START')
        stopBtn = wx.Button(panel, -1, 'STOP')
        self.log = wx.TextCtrl(panel, -1, '', style=wx.TE_MULTILINE)

        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(startBtn, 0, wx.RIGHT, 15)
        inner.Add(stopBtn, 0, wx.RIGHT, 15)
        main1 = wx.BoxSizer(wx.VERTICAL)
        main1.Add(inner, 0, wx.ALL, 5)
        main1.Add(self.log, 1, wx.EXPAND, 5)
        panel.SetSizer(main1)

        self.Bind(wx.EVT_BUTTON, self.on_start_button, startBtn)
        self.Bind(wx.EVT_BUTTON, self.on_stop_button, stopBtn)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)

    def on_start_button(self, evt):
        thread = WorkerThread()
        self.threads.append(thread)
        thread.start()
        msg = '正在运行'
        wx.CallAfter(self.log_message, msg)

    def on_stop_button(self, evt):
        self.stop_threads()

    def on_close_window(self, evt):
        self.stop_threads()
        self.Destroy()

    def stop_threads(self):
        while self.threads:
            thread = self.threads[0]
            thread.stop()
            self.threads.remove(thread)
            msg = 'exit'
            wx.CallAfter(self.log_message, msg)

    def log_message(self, msg):
        self.log.AppendText(msg)

    def thread_finished(self, thread):
        self.threads.remove(thread)


class App(wx.App):
    def OnInit(self):
        image = wx.Image('Aura.png', wx.BITMAP_TYPE_PNG)
        frame = MyFrame()

        frame.Show()
        self.SetTopWindow(frame)
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
