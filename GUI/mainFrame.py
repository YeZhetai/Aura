import wx
import sys


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500, 300))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()

        menuStart = filemenu.Append(wx.ID_OPEN, '启动', '')
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, '关于', '')
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, '退出', '')

        menubar = wx.MenuBar()
        menubar.Append(filemenu, '文件')
        self.SetMenuBar(menubar)

        self.Show(True)
