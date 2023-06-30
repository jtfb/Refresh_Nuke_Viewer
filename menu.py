import nuke
import KnobScripter
import refreshViewer

# def set_environment_variables():
#     key1 = 'CCC_PATH'
#     value1 = '[getenv CCC_PATH]'
#     key2 = 'LUT_PATH'
#     value2 = '[getenv LUT_PATH]'

#     nuke.knobDefault("OCIODisplay1.knob_" + key1, value1)
#     nuke.knobDefault("OCIODisplay1.knob_" + key2, value2)
    
#     nuke.knobDefault("Root.colorspace", "OCIODisplay1")

# set_environment_variables()

# menubar=nuke.menu("MenuType")
# menubar.addMenu("Viewer").addCommand("Refresh Viewer", "F4")



def toggle_monitor_output():
    active_viewer = nuke.activeViewer()
    if active_viewer:
        monitor_node = active_viewer.node().input(0)
        if monitor_node.Class() == 'Write':
            active_viewer.node().setInput(0, monitor_node.input(0))
        else:
            write_node = nuke.createNode('Write')
            write_node.setInput(0, active_viewer.node())
            active_viewer.node().setInput(0, write_node)

toggle_monitor_output()

nuke.menu("Nuke").addCommand("Viewer/Refresh", toggle_monitor_output, "F6", shortcutContext=2)