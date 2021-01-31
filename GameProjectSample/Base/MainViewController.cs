using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainViewController : NaviViewController
{
    static private MainViewController _main = null;
    public static MainViewController main
    {
        get
        {
            if (_main == null)
            {
                _main = new MainViewController();
                _main.Init();
            }
            return _main;
        }
    }

    void Init()
    {
        this.title = "Main";
        this.Push(HomeViewController.main);
    }

    public override void ViewDidLoad()
    {
        //必须先调用基类方法以便初始化
        base.ViewDidLoad();

        Debug.Log("MainViewController ViewDidLoad");
    }
    public override void ViewDidUnLoad()
    {
        //必须先调用基类方法
        base.ViewDidUnLoad();
    }

}
