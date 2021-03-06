#ifndef mtkr_MAYA_SCENE_H
#define mtkr_MAYA_SCENE_H

#include <maya/MDagPathArray.h>
#include <fstream>
#include <map>

#include "mayaScene.h"
#include "mtkr_renderGlobals.h"
#include "mtkr_MayaObject.h"
#include "utilities/MiniMap.h"
#include "../kray/krayRenderer.h"

class mtkr_MayaScene : public MayaScene
{
public:
	mtkr_RenderGlobals *renderGlobals;
	MayaObject *defaultCamera; // needed for motionblur calculation
	
	//std::map<MayaObject *, MObject> mayaObjMObjMap;
	MiniMap<MObject, MayaObject *> mayaObjMObjMap;
	krayRender::KrayRenderer mtkr_renderer;

	virtual void transformUpdateCallback(MayaObject *);
	virtual void shapeUpdateCallback(MayaObject *);
	virtual bool translateShaders(int timeStep);
	virtual bool translateShapes(int timeStep);
	virtual bool doPreRenderJobs();
	virtual bool renderImage();
	virtual bool doPreFrameJobs();
	virtual bool doPostFrameJobs();
	virtual bool doPostRenderJobs();
	virtual MayaObject* mayaObjectCreator(MObject&);
	virtual MayaObject* mayaObjectCreator(MDagPath&);
	virtual void mayaObjectDeleter(MayaObject *);
	virtual void getRenderGlobals();
	virtual void stopRendering();
	virtual void updateInteraciveRenderScene(std::vector<MObject> mobjList);
	void mobjectListToMayaObjectList(std::vector<MObject>& mObjectList, std::vector<MayaObject *>& mtapObjectList);
	virtual bool postParseCallback();
	void makeMayaObjectMObjMap(); // fill with maya objects and dag nodes for later fast access
	mtkr_MayaObject *getMayaObjectFromMap(MObject& mobj);
	bool parseScene(ParseType ptype = NORMALPARSE);
	mtkr_MayaScene();
	mtkr_MayaScene(RenderType rtype);
	~mtkr_MayaScene();
};


#endif
