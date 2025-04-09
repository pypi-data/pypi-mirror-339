__author__ = "Chris"

# https://github.com/chriskiehl/Gooey/issues/826#issuecomment-1240180894
from rewx import widgets
from rewx.widgets import set_basic_props, dirname
from rewx.dispatch import update
import wx


@update.register(wx.Frame)
def frame(element, instance: wx.Frame):
    props = element["props"]
    set_basic_props(instance, props)
    if "title" in props:
        instance.SetTitle(props["title"])
    if "show" in props:
        instance.Show(props["show"])
    if "icon_uri" in props:
        pass  # No icons for now
    if "on_close" in props:
        instance.Bind(wx.EVT_CLOSE, props["on_close"])

    return instance


widgets.frame = frame
