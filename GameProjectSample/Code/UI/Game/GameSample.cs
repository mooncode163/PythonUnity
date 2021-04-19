using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.EventSystems;
using LitJson;
public class GameSample : UIView
{ 
    static private GameSample _main = null;
    public static GameSample main
    {
        get
        {
            if (_main == null)
            {

            }
            return _main;
        }

    }
    public void Awake()
    {
        base.Awake();
        _main = this;
        LoadPrefab(); 
    }
    // Use this for initialization
    public void Start()
    {
        base.Start(); 
        LayOut();
    }


    void LoadPrefab()
    {


    }

    public override void LayOut()
    {
        base.LayOut();
        float x, y, w, h;
    }
}
