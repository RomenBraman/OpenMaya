import pymel.core as pm
import logging
import Renderer as Renderer

reload(Renderer)

log = logging.getLogger("mtapLogger")

#    parentForm = pm.setParent(query = True)
#    pm.setUITemplate( "attributeEditorTemplate", pushTemplate = True)
#    pm.scrollLayout( "MantraScrollLayout", horizontalScrollBarThickness = 0)
#    pm.columnLayout("MantraColumnLayout", adjustableColumn = True)
#
#    mantraAttributes.mantraGlobalsATList.createUi(mrg)
#    
#    pm.setUITemplate( "attributeEditorTemplate", popTemplate = True)
#    pm.formLayout(parentForm, edit = True, attachForm = [ ("MantraScrollLayout", "top", 0),
#                                                          ("MantraScrollLayout", "bottom", 0),
#                                                          ("MantraScrollLayout", "left", 0),
#                                                          ("MantraScrollLayout", "right", 0)
#                                                        ])


class AppleseedRenderer(Renderer.MayaToRenderer):
    theRendererInstance = None
    @staticmethod
    def theRenderer(arg = None):
        if not AppleseedRenderer.theRendererInstance:
            AppleseedRenderer.theRendererInstance = AppleseedRenderer( "Appleseed", "mtap_initialize")
        return AppleseedRenderer.theRendererInstance
    
    def __init__(self, rendererName, moduleName):
        Renderer.MayaToRenderer.__init__(self, rendererName, moduleName)
        self.rendererTabUiDict = {}
    
    def getEnumList(self, attr):
        return [(i, v) for i,v in enumerate(attr.getEnums().keys())]

    def updateTest(self, dummy = None):
        print "UpdateTest", dummy             
    def AppleseedRendererCreateTab(self):
        log.debug("AppleseedRendererCreateTab()")
        self.createGlobalsNode()
        parentForm = pm.setParent(query = True)
        pm.setUITemplate("attributeEditorTemplate", pushTemplate = True)
        scLo = self.rendererName + "ScrollLayout"
        with pm.scrollLayout(scLo, horizontalScrollBarThickness = 0):
            with pm.columnLayout(self.rendererName + "ColumnLayout", adjustableColumn = True):
                with pm.frameLayout(label="Sampling", collapsable = True, collapse=False):
                    ui = pm.checkBoxGrp(label="Adaptive Sampling:", value1 = False, cc = self.AppleseedRendererUpdateTab)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".adaptiveSampling", index = 2)
                    self.rendererTabUiDict['minSamples'] = pm.intFieldGrp(label="Samples min:", value1 = 2, numberOfFields = 1)
                    pm.connectControl(self.rendererTabUiDict['minSamples'], self.renderGlobalsNodeName + ".minSamples", index = 2 )
                    ui = pm.intFieldGrp(label="Samples max:", value1 = 16, numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".maxSamples", index = 2 )
                    self.rendererTabUiDict['maxError'] = pm.floatFieldGrp(label="Max Error:", value1 = 0.01, numberOfFields = 1)
                    pm.connectControl(self.rendererTabUiDict['maxError'], self.renderGlobalsNodeName + ".maxError", index = 2 )
                    pm.separator()
                    ui = pm.checkBoxGrp(label="Motionblur:", value1 = False)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".doMotionBlur", index = 2 )
                    ui = pm.checkBoxGrp(label="Depth Of Field:", value1 = False)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".doDof", index = 2 )
                    
                with pm.frameLayout(label="Output", collapsable = True, collapse=False):
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".imageFormat")
                    ui = pm.attrEnumOptionMenuGrp(label = "Image Format", at=self.renderGlobalsNodeName + ".imageFormat", ei = self.getEnumList(attr)) 
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".bitdepth")
                    ui = pm.attrEnumOptionMenuGrp(label = "Bit Depth", at=self.renderGlobalsNodeName + ".bitdepth", ei = self.getEnumList(attr)) 
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".colorSpace")
                    ui = pm.attrEnumOptionMenuGrp(label = "Color Space", at=self.renderGlobalsNodeName + ".colorSpace", ei = self.getEnumList(attr)) 
                    ui = pm.checkBoxGrp(label="Clamping:", value1 = False)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".clamping", index = 2 )
                    
                with pm.frameLayout(label="Filtering", collapsable = True, collapse=False):
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".filtertype")
                    ui = pm.attrEnumOptionMenuGrp(label = "Filter Type", at=self.renderGlobalsNodeName + ".filtertype", ei = self.getEnumList(attr)) 
                    ui = pm.intFieldGrp(label="Filter Size:", numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".filtersize", index = 2 )

                with pm.frameLayout(label="Lighting", collapsable = True, collapse=False):
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".lightingEngine")
                    ui = pm.attrEnumOptionMenuGrp(label = "Lighting Engine", at=self.renderGlobalsNodeName + ".lightingEngine", ei = self.getEnumList(attr)) 
                    ui = pm.intFieldGrp(label="Max Trace Depth:", value1 = 4, numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".maxTraceDepth", index = 2 )
                    ui = pm.checkBoxGrp(label="Caustics:", value1 = False)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".caustics", index = 2 )
                    with pm.frameLayout(label="Advanced Lighting", collapsable = True, collapse=True):
                        ui = pm.intFieldGrp(label="Diffuse Depth:", value1 = 4, numberOfFields = 1)
                        pm.connectControl(ui, self.renderGlobalsNodeName + ".diffuseDepth", index = 2 )
                        ui = pm.intFieldGrp(label="Glossy Depth:", value1 = 4, numberOfFields = 1)
                        pm.connectControl(ui, self.renderGlobalsNodeName + ".glossyDepth", index = 2 )
                        ui = pm.intFieldGrp(label="Direct Light Samples:", value1 = 4, numberOfFields = 1)
                        pm.connectControl(ui, self.renderGlobalsNodeName + ".directLightSamples", index = 2 )
                    with pm.frameLayout(label="Environment Lighting", collapsable = True, collapse=True):
                        attr = pm.Attribute(self.renderGlobalsNodeName + ".environmentType")
                        ui = pm.attrEnumOptionMenuGrp(label = "Environemnt Type", at=self.renderGlobalsNodeName + ".environmentType", ei = self.getEnumList(attr)) 
                        ui = pm.floatFieldGrp(label="Environemnt Intensity:", value1 = 1.0, numberOfFields = 1)
                        pm.connectControl(ui, self.renderGlobalsNodeName + ".environmentIntensity", index = 2 )
                        
                        ui = pm.attrColorSliderGrp(label = "Environment Color", at=self.renderGlobalsNodeName + ".environmentColor")
                        attr = pm.Attribute(self.renderGlobalsNodeName + ".environmentColor")
                        ui = pm.attrColorSliderGrp(label = "Gradient Horizon", at=self.renderGlobalsNodeName + ".gradientHorizon")
                        attr = pm.Attribute(self.renderGlobalsNodeName + ".gradientHorizon")
                        ui = pm.attrColorSliderGrp(label = "Gradient Zenit", at=self.renderGlobalsNodeName + ".gradientZenit")
                        attr = pm.Attribute(self.renderGlobalsNodeName + ".gradientZenit")

                    
                with pm.frameLayout(label="Renderer", collapsable = True, collapse=False):
                    ui = pm.intFieldGrp(label="Threads:", numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".threads", index = 2 )
                    ui = pm.intFieldGrp(label="Verbosity:", numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".rendererVerbosity", index = 2 )
                    ui = pm.intFieldGrp(label="Tile Size:", value1 = 32, numberOfFields = 1)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".tilesize", index = 2 )
                    
                    
        pm.setUITemplate("attributeEditorTemplate", popTemplate = True)
        pm.formLayout(parentForm, edit = True, attachForm = [ (scLo, "top", 0), (scLo, "bottom", 0), (scLo, "left", 0), (scLo, "right", 0) ])
        self.AppleseedRendererUpdateTab()

    def AppleseedRendererUpdateTab(self, dummy = None):
        log.debug("AppleseedRendererUpdateTab()")
        if self.renderGlobalsNode.adaptiveSampling.get():
            self.rendererTabUiDict['minSamples'].setEnable(True)
            self.rendererTabUiDict['maxError'].setEnable(True)
        else:
            self.rendererTabUiDict['minSamples'].setEnable(False)
            self.rendererTabUiDict['maxError'].setEnable(False)


    def AppleseedTranslatorCreateTab(self):
        log.debug("AppleseedTranslatorCreateTab()")
        self.createGlobalsNode()
        parentForm = pm.setParent(query = True)
        pm.setUITemplate("attributeEditorTemplate", pushTemplate = True)
        scLo = self.rendererName + "TrScrollLayout"
        
        with pm.scrollLayout(scLo, horizontalScrollBarThickness = 0):
            with pm.columnLayout(self.rendererName + "TrColumnLayout", adjustableColumn = True):
                with pm.frameLayout(label="Translator", collapsable = True, collapse=False):
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".translatorVerbosity")
                    ui = pm.attrEnumOptionMenuGrp(label = "Translator Verbosity", at=self.renderGlobalsNodeName + ".translatorVerbosity", ei = self.getEnumList(attr)) 
                    attr = pm.Attribute(self.renderGlobalsNodeName + ".assemblyExportType")
                    ui = pm.attrEnumOptionMenuGrp(label = "Assembly Export Type", at=self.renderGlobalsNodeName + ".assemblyExportType", ei = self.getEnumList(attr)) 
                with pm.frameLayout(label="Appleseed XML export", collapsable = True, collapse=False):
                    ui = pm.checkBoxGrp(label="Export scene XML file:", value1 = False)
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".exportXMLFile", index = 2 )
                    ui = pm.textFieldGrp(label="XMLFileName:", text = "")
                    pm.connectControl(ui, self.renderGlobalsNodeName + ".exportXMLFileName", index = 2 )
                    
        pm.setUITemplate("attributeEditorTemplate", popTemplate = True)
        pm.formLayout(parentForm, edit = True, attachForm = [ (scLo, "top", 0), (scLo, "bottom", 0), (scLo, "left", 0), (scLo, "right", 0) ])

    def AppleseedTranslatorUpdateTab(self):
        log.debug("AppleseedTranslatorUpdateTab()")

    def createImageFormats(self):
        self.imageFormats.append('exr')
        self.imageFormats.append('png')

    def registerNodeExtensions(self):
        """Register Appleseed specific node extensions. e.g. camera type, diaphram_blades and others
        """
        pm.addExtension(nodeType="camera", longName="mtap_cameraType", attributeType="enum", enumName="Pinhole:Thinlens", defaultValue = 0)
        pm.addExtension(nodeType="camera", longName="mtap_diaphragm_blades", attributeType="long", defaultValue = 0)
        pm.addExtension(nodeType="camera", longName="mtap_diaphragm_tilt_angle", attributeType="float", defaultValue = 0.0)
    
    def renderProcedure(self):
        log.debug("renderProcedure")
        self.createGlobalsNode()    
        self.preRenderProcedure()
        self.renderGlobalsNode.basePath.set(pm.workspace.path)
        self.renderGlobalsNode.imagePath.set(pm.workspace.path + pm.workspace.fileRules['images'])
        imageName = pm.sceneName().basename().replace(".ma", "").replace(".mb", "")
        # check for mayabatch name like sceneName_number 
        numberPart = imageName.split("__")[-1]
        try:
            number = int(numberPart)
            if number > 999:
                imageName = imageName.replace("__" + numberPart, "")
        except:
            pass
        self.renderGlobalsNode.imageName.set(imageName)        
        pm.mayatoappleseed()
        

def theRenderer():
    return AppleseedRenderer.theRenderer()
        
def initRenderer():
    try:
        log.debug("Init renderer Appleseed")
        theRenderer().registerRenderer()
    except:
        log.error("Init renderer Appleseed FAILED")
        
def unregister():
    theRenderer().unRegisterRenderer()
    log.debug("Unregister done")
