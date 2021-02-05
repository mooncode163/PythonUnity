using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIHomeSample : UIHomeBase//, ISysImageLibDelegate
{
    public UIHomeSideBar uiHomeSideBar;

    public UIHomeCenterBar uiHomeCenterBar;
    void Awake()
    {

        base.Awake();
        // TextureUtil.UpdateRawImageTexture(imageBg, AppRes.IMAGE_HOME_BG, true);
        string appname = Common.GetAppNameDisplay();
        TextName.text = appname;

 
        LayOutSize ly = imageBgName.GetComponent<LayOutSize>();
        if (Device.isLandscape)
        {
            ly.ratioW = 0.6f;
            ly.ratioH = 0.8f;
        }
        else
        {
            ly.ratioW = 0.8f;
            ly.ratioH = 0.6f;
        }


    }

    // Use this for initialization
    void Start()
    {
        base.Start();
        LayOut();

        OnUIDidFinish(0.5f);
    }

    // Update is called once per frame
    void Update()
    {
        UpdateBase();
    }



    public override void LayOut()
    {
        base.LayOut();
        Vector2 sizeCanvas = this.frame.size;
        float x = 0, y = 0, w = 0, h = 0;
        uiHomeCenterBar.LayOut();
        base.LayOut();
    }

}
