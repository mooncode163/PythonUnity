using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;


public class UIIconController : UIShotBase
{
    public Image imageBg;
    public Image imageHD;
    public Image imageBoard;
    /// <summary>
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    void Awake()
    {
        imageHD.gameObject.SetActive(false);
        imageBoard.gameObject.SetActive(false);
    }
    void Start()
    {
        IconViewController iconctroller = (IconViewController)this.controller;
        if (iconctroller != null)
        {
            if (iconctroller.deviceInfo.isIconHd)
            {
                imageHD.gameObject.SetActive(true);
            }

        }
        LayOut();
        OnUIDidFinish();
    }
    public override void LayOut()
    {
        base.LayOut();
    }
}
