#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ---------------------------------------------------------------
# wxpasswd.py
#
# Copyright (c) 2019 sanderiana https://github.com/sanderiana
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# ---------------------------------------------------------------
# Icon made by Freepik from www.flaticon.com
# ---------------------------------------------------------------

import wx
import random
import sys
import hashlib
import os
import warnings
import argparse


class WxPassWindow(wx.Frame):
    APP_WIDTH = 90 * 3
    APP_HEIGHT = 90 * 3
    COLOUR_DIFF = -160

    def __init__(self, title, hash_type=None):
        self.button_dict = {}
        self.button_num = {}
        self.total_pass = ""
        self.back_colour = None
        self.fore_colour = None
        self.hash_type = hash_type
        self.InitializeComponents(title)

    def InitializeComponents(self, title):
        pos = self.GetWindowPos()
        wx.Frame.__init__(self, parent=None, title=title, pos=pos, size=(self.APP_WIDTH, self.APP_HEIGHT))
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseOver)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_CHAR,self.OnInputKey)
        self.SetBaseColour(self.GetBackgroundColour())
        self.SetForegroundColour(self.fore_colour)
        self.SetCanFocus(True)

        main_panel = wx.Panel(self)
        sizer = wx.GridBagSizer()
        main_panel.SetSizer(sizer)

        for idx in list(range(0, 9)):
            button = self.CreateButton(idx,main_panel)
            pos_y = idx // 3
            pos_x = idx % 3
            sizer.Add(button, (pos_y,pos_x), (1, 1), flag=wx.EXPAND)

        button = self.CreateButton(9, main_panel)
        sizer.Add(button, (3, 0), (1, 3), flag=wx.EXPAND)

        button_ok = wx.Button(main_panel, -1, "ok")
        button_ok.Bind(wx.EVT_BUTTON, self.OnCloseButton)
        button_ok.SetForegroundColour(self.fore_colour)
        button_ok.SetBackgroundColour(self.back_colour)
        button_ok.SetCanFocus(False)
        sizer.Add(button_ok, (4, 0), (1, 1), flag=wx.EXPAND)

        button_reset = wx.Button(main_panel, -1, "reset")
        button_reset.Bind(wx.EVT_BUTTON, self.OnResetButton)
        button_reset.SetForegroundColour(self.fore_colour)
        button_reset.SetBackgroundColour(self.back_colour)
        button_reset.SetCanFocus(False)
        sizer.Add(button_reset, (4, 1), (1, 1), flag=wx.EXPAND)

        button_reset = wx.Button(main_panel, -1, "cancel")
        button_reset.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        button_reset.SetForegroundColour(self.fore_colour)
        button_reset.SetBackgroundColour(self.back_colour)
        button_reset.SetCanFocus(False)
        sizer.Add(button_reset, (4, 2), (1, 1), flag=wx.EXPAND)

        self.ChangeButtonLabel()

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)

    def CreateButton(self, idx, main_panel):
        button = wx.Button(main_panel, -1)
        button.Bind(wx.EVT_BUTTON, self.OnClick)
        button.SetId(idx)
        button.SetForegroundColour(self.fore_colour)
        button.SetBackgroundColour(self.back_colour)
        button.SetCanFocus(False)
        self.button_dict[idx] = button
        return button

    def SetBaseColour(self, back_colour):
        back_list = list(back_colour.Get())
        fore = map(lambda colour: colour + self.COLOUR_DIFF, back_list)
        fore += [back_colour.Alpha()]

        self.fore_colour = wx.Colour(fore[0], fore[1], fore[2], fore[3])
        self.back_colour = back_colour

    def GetWindowPos(self):
        w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        x = w / 2
        y = h / 2

        x -= (self.APP_WIDTH / 2)
        y -= (self.APP_HEIGHT / 2)
        pos = (x, y)
        return pos

    def ChangeButtonLabel(self):
        label_list = list(range(0,10))
        random.shuffle(label_list)

        for idx, button in self.button_dict.items():
            new_value = label_list[idx]
            new_label = str(new_value)
            self.button_num[idx] = new_value
            button.SetLabelText(new_label)

    def ClearButtonLabel(self):
        for idx, button in self.button_dict.items():
            button.SetLabelText("")

    def ExitWindow(self):
        if self.hash_type == 'sha256':
            output = hashlib.sha256(self.total_pass).hexdigest()
        elif self.hash_type == 'md5':
            output = hashlib.md5(self.total_pass).hexdigest()
        else:
            output = self.total_pass

        sys.stdout.write(output)
        self.Close()

    # event ---------------------------------------------------------
    def OnInputKey(self, event):
        keycode = chr(event.GetKeyCode())
        self.total_pass += keycode

    def OnExitWindow(self, event):
        self.ExitWindow()

    def OnCancelButton(self, event):
        self.Close()

    def OnCloseButton(self, event):
        self.ExitWindow()

    def OnResetButton(self, event):
        dlg = wx.MessageDialog(None, 'Do you reset inputted passwd？', 'check',
           wx.YES_NO | wx.ICON_QUESTION)

        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.total_pass = ""

    def OnClick(self, event):
        button = event.GetEventObject()
        idx = button.GetId()
        label = str(self.button_num[idx]).encode('utf_8')
        self.total_pass += label

    def OnMouseOver(self, event):
        self.ClearButtonLabel()
        event.Skip()

    def OnMouseLeave(self, event):
        self.ChangeButtonLabel()
        event.Skip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='password input window')
    parser.add_argument('--title', default="input password", help='window title')
    parser.add_argument('--hash', default=None, choices=['sha256', 'md5'], help='encode type')
    args = parser.parse_args()

    app = wx.App()
    frame = WxPassWindow(title=args.title, hash_type=args.hash)
    app.SetTopWindow(frame)

    warnings.simplefilter("ignore")
    icon = wx.EmptyIcon()
    icon_file = os.path.dirname(__file__) + '/wxpasswd.png'
    icon_source = wx.Image(icon_file, wx.BITMAP_TYPE_PNG)
    icon.CopyFromBitmap(icon_source.ConvertToBitmap())
    frame.SetIcon(icon)

    # 処理の開始
    frame.Show()
    app.MainLoop()
