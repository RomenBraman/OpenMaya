import pymel.core as pm
import logging

log = logging.getLogger("ui")

class BaseTemplate(pm.ui.AETemplate):
    
    def addControl(self, control, label=None, **kwargs):
        pm.ui.AETemplate.addControl(self, control, label=label, **kwargs)
        
    def beginLayout(self, name, collapse=True):
        pm.ui.AETemplate.beginLayout(self, name, collapse=collapse)
        

class AECoatingBSDFTemplate(BaseTemplate):
    def __init__(self, nodeName):
        BaseTemplate.__init__(self,nodeName)
        log.debug("AECoatingBSDFTemplate")
        self.thisNode = None
        self.node = pm.PyNode(self.nodeName)
        pm.mel.AEswatchDisplay(nodeName)
        self.beginScrollLayout()
        self.buildBody(nodeName)
        self.addExtraControls("ExtraControls")
        self.endScrollLayout()
        
    def buildBody(self, nodeName):
        self.thisNode = pm.PyNode(nodeName)
        self.beginLayout("ShaderSettings" ,collapse=0)
        self.beginNoOptimize()
        #autoAddBegin
        self.addControl("normalMapping", label="NormalMapping")
        self.addControl("kappa", label="Kappa")
        self.addControl("bump", label="Bump")
        self.addControl("anisotropy", label="Anisotropy")
        self.addControl("reflectanceColor", label="Reflectance Color")
        self.addControl("ior", label="Ior")
        self.addControl("roughness", label="Roughness")
        self.addControl("microRoughnessHeight", label="MicroRoughnessHeight")
        self.addControl("coatingAbsorption", label="CoatingAbsorption")
        self.addControl("microRoughness", label="MicroRoughness")
        self.addControl("rotation", label="Rotation")
        self.addControl("thickness", label="Thickness")
        self.addControl("microRoughnessWidth", label="MicroRoughnessWidth")
        self.addSeparator()
        #autoAddEnd
        self.endNoOptimize()
        self.endLayout()
        