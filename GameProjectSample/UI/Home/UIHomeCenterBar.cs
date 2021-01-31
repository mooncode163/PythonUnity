using System.Collections;
using System.Collections.Generic;
using DG.Tweening;
using Moonma.IAP;
using Moonma.Share;
using UnityEngine;
using UnityEngine.UI;
using Moonma.SysImageLib;
public class UIHomeCenterBar : UIView
{

    public Button btnPlay;
    public Button btnLearn;
    public Button btnAdVideo;
    public Button btnAddLove;
    public Button btnPhoto;
    public Button btnCamera;
    public Button btnNetImage;
    void Awake()
    {


        if (btnAdVideo != null)
        {
            btnAdVideo.gameObject.SetActive(true);
            if ((Common.noad) || (!AppVersion.appCheckHasFinished))
            {
                btnAdVideo.gameObject.SetActive(false);
            }
            if (Common.isAndroid)
            {
                if (Config.main.channel == Source.GP)
                {
                    //GP市场不显示
                    btnAdVideo.gameObject.SetActive(false);
                }
            }
        }
        if (!AppVersion.appCheckHasFinished)
        {
            btnPhoto.gameObject.SetActive(false);
            btnCamera.gameObject.SetActive(false);
            btnNetImage.gameObject.SetActive(false);
        }





    }
    // Use this for initialization
    void Start()
    {
        LayOut();

    }



    public override void LayOut()
    {
        base.LayOut();

        Vector2 sizeCanvas = this.frame.size;
        float x = 0, y = 0, w = 0, h = 0;

        LayOutGrid lygrid = this.GetComponent<LayOutGrid>();
        if (Device.isLandscape)
        {
            lygrid.row = 1;
            lygrid.col = lygrid.GetChildCount(false);


        }
        else
        {
            int count = lygrid.GetChildCount(false);
            lygrid.col = 2;
            lygrid.row = count / lygrid.col;
            if (count % lygrid.col > 0)
            {
                lygrid.row++;
            }

        }
        // if (!AppVersion.appCheckHasFinished)
        // {
        //     lygrid.row = 2;

        //     lygrid.col = 2;
        // }


        lygrid.LayOut();

        RectTransform rctran = this.GetComponent<RectTransform>();
        w = rctran.rect.width;
        h = lygrid.row * 256;
        rctran.sizeDelta = new Vector2(w, h);

    }





    public void OnClickBtnPlay()
    {
        //AudioPlay.main.PlayAudioClip(audioClipBtn); 

        if (this.controller != null)
        {
            NaviViewController navi = this.controller.naviController;
            // navi.Push(LoginViewController.main);
        }
    }


    public void OnClickBtnLearn()
    {
        NaviViewController navi = this.controller.naviController;
        // navi.Push(LearnProgressViewController.main);

    }
    public void OnClickBtnAddLove()
    {
        if (this.controller != null)
        {
            NaviViewController navi = this.controller.naviController;
            // navi.Push(LoveViewController.main);
        }
    }

    public void OnClickBtnAdVideo()
    {
        AdKitCommon.main.ShowAdVideo();
    }

}
