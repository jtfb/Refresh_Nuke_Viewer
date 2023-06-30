import nuke


def update_viewers():
    active_viewer = nuke.activeViewer()
    if active_viewer:
        current_frame = nuke.frame()
        nuke.frame(current_frame + 1)
        nuke.frame(current_frame - 1)

# Add the "Refresh Active Viewer" command to the Viewer menu with the shortcut
nuke.menu("Nuke").addCommand("Viewer/Refresh Viewer", update_viewers, "F4", shortcutContext=2)