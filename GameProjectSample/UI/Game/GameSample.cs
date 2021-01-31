using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.EventSystems;
using LitJson;
public class GameSample : UIView
{ 
    public void Awake()
    {
        base.Awake();
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
