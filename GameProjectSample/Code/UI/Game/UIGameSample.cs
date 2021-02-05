using System.Collections;
using System.Collections.Generic;
using LitJson;
using UnityEngine; 
using UnityEngine.UI;
using System.IO;  
public class UIGameSample : UIGameBase//, IGameSampleDelegate
{ 
     GameSample GameSamplePrefab;
    public GameSample GameSample; 

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
                GameSamplePrefab = obj.GetComponent<GameSample>();
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
         
    }
    public override void LayOut()
    {
        base.LayOut();

    }
 


}
