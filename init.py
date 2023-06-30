import nuke
from marz_studio.utils.studio_info import studio_info


def add_format(name='', width=3840, height=2160, par=1.0):
    """
    Gets a format object for the current nuke session.   

    Args:
        name (str): The format's name. Can be empty string (default) to use the width height and pixel aspect ratio as the name.
        width (int): Horizontal dimension in pixels
        height (int): Vertical dimension in pixels
        par (float): Pixel Aspect Ratio. The width/height ratio of a pixel. 1 = spare pixels. >1 = anamorphic (squeezed) pixels.

    Returns:
        (nuke.format): The format object with the requested parameters. Creates it if necessary.
    """
    for nuke_format in nuke.formats():
        if nuke_format.width() == width and nuke_format.height() == height and nuke_format.pixelAspect == par:
            return nuke_format
    
    return nuke.addFormat(" {width} {height} {par} {name}".format(width=width, height=height, par=par, name=name))

class ViewerDefaultHandler:
    @classmethod
    def updateViewerDefault(self):
        """
        Update viewProcess to client look for shots and cg look for assets.   

        Args:

        Returns:
            update viewer's viewProcess
        """
        import nuke
        try:
            action_mode = os.environ.get('ACTION_MODE')
            project = os.environ['IC_PROJECT']
            seq     = os.environ['IC_SEQ_TYPE']
            shot    = os.environ['IC_CODE']
            info    = studio_info()
            idn     = info.get_code(project, seq, shot).get('id')

            ml_colorspace = info.sg.find_one(entity_type="Shot", filters=[["id", "is", idn], ['sg_status_list', 'is_not', 'na,cbb,park']], fields=["sg_ml_plate_colorspace"])["sg_ml_plate_colorspace"]
            
            nodes = [w for w in nuke.allNodes('Viewer')]

            if ml_colorspace == "ACES":
                nuke.knobDefault('Viewer.viewerProcess','Client Look ACES (MARZ)')
                for node in nodes:
                    node['viewerProcess'].setValue('Client Look ALEXA (MARZ)')
            elif ml_colorspace == "ALEXA_v3":
                nuke.knobDefault('Viewer.viewerProcess','Client Look ALEXA (MARZ)')
                for node in nodes:
                    node['viewerProcess'].setValue('Client Look ALEXA (MARZ)')
            elif ml_colorspace == "RED":
                nuke.knobDefault('Viewer.viewerProcess','Client Look RED (MARZ)')
                for node in nodes:
                    node['viewerProcess'].setValue('Client Look ALEXA (MARZ)')
            elif ml_colorspace == "SONYCine":
                nuke.knobDefault('Viewer.viewerProcess','Client Look SONYCine (MARZ)')
                for node in nodes:
                    node['viewerProcess'].setValue('CG Look (MARZ)')
            else:
                nuke.knobDefault('Viewer.viewerProcess','Lookdev Look (MARZ)')
                 
        except:
            pass

def setViewer():
    """
    Update viewProcess to client look for shots and cg look for assets.   

    Args:

    Returns:
        update viewer's viewProcess
    """
    action_mode = os.environ.get('ACTION_MODE')
    project = os.environ['IC_PROJECT']
    seq     = os.environ['IC_SEQ_TYPE']
    shot    = os.environ['IC_CODE']
    info    = studio_info()
    idn     = info.get_code(project, seq, shot).get('id')

    ml_colorspace = info.sg.find_one(entity_type="Shot", filters=[["id", "is", idn], ['sg_status_list', 'is_not', 'na,cbb,park']], fields=["sg_ml_plate_colorspace"])["sg_ml_plate_colorspace"]
    

    if ml_colorspace  == "ACES":
        nuke.thisNode()['viewerProcess'].setValue('Client Look ACES (ACES)')        
    elif ml_colorspace  == "ALEXA_v3":
        nuke.thisNode()['viewerProcess'].setValue('Client Look ALEXA (ACES)')
    elif ml_colorspace  == "Red":
        nuke.thisNode()['viewerProcess'].setValue('Client Look RED (ACES)')
    elif ml_colorspace  == "SONYCine":
        nuke.thisNode()['viewerProcess'].setValue('Client Look SONYCine (ACES)')
    else:
        nuke.thisNode()['viewerProcess'].setValue('Lookdev Look (ACES)')

# rename delivery resolution format here 
DELIVERY_FORMAT_NAME = 'maz_imaging_training Delivery Format'
# update the resolution here to match to delivery space
delivery_format = add_format(DELIVERY_FORMAT_NAME, 3532, 1766, 1.0)
nuke.knobDefault("Root.format", DELIVERY_FORMAT_NAME)

nuke.addOnScriptLoad(ViewerDefaultHandler.updateViewerDefault)
nuke.addOnUserCreate(setViewer, nodeClass='Viewer')

nuke.ViewerProcess.register("Colour Review Local", nuke.Node, ("Client_Display_Test", ""))