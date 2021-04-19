using System.Collections;
using System.Collections.Generic;
using LitJson;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
public class UIGameSample : UIGameBase//, IGameSampleDelegate
{
    GameSample gamePrefab;
    public GameSample game;

    static private UIGameSample _main = null;
    public static UIGameSample main
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
        LoadPrefab();
        _main = this;
    }
    // Use this for initialization
    public void Start()
    {
        base.Start();
        LayOut();
        UpdateGuankaLevel(LevelManager.main.gameLevel);
        Invoke("AutoReady", 1f);
    }

    public void AutoReady()
    {

    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetKeyUp(KeyCode.Escape))
        {
            OnClickBtnBack();
        }

    }

    void LoadPrefab()
    {


        {
            GameObject obj = PrefabCache.main.LoadByKey("GameSample");
            if (obj != null)
            {
                gamePrefab = obj.GetComponent<GameSample>();
            }

        }





    }

    void InitUI()
    {


        OnUIDidFinish();
    }


    public override void UpdateGuankaLevel(int level)
    {
        base.UpdateGuankaLevel(level);
        {
            game = (GameSample)GameObject.Instantiate(gamePrefab);
            AppSceneBase.main.AddObjToMainWorld(game.gameObject);
            game.transform.localPosition = new Vector3(0f, 0f, -1f);
            UIViewController.ClonePrefabRectTransform(gamePrefab.gameObject, game.gameObject);
        }


    }
    public override void LayOut()
    {
        base.LayOut();

    }



}
