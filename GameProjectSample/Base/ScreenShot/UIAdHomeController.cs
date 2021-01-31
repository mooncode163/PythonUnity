using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class UIAdHomeController : UIShotBase
{
    public Image imageBg;
    public GameObject objGameBox;
    public GameObject objMath;
    public Image imageTitle;
    public Text textTitle;


    /// <summary>
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    void Awake()
    {
        string appname = Common.GetAppNameDisplay();
        textTitle.text = appname; 

    }
    /// <summary>
    /// Start is called on the frame when a script is enabled just before
    /// any of the Update methods is called the first time.
    /// </summary>
    void Start()
    {
        LayOut();
        OnUIDidFinish();
    }
    public override void LayOut()
    {
        base.LayOut();
        float x, y, w, h;

        Vector2 sizeCanvas = this.frame.size;
        {
            RectTransform rctran = imageBg.GetComponent<RectTransform>();
            float w_image = rctran.rect.width;
            float h_image = rctran.rect.height;
            float scalex = sizeCanvas.x / w_image;
            float scaley = sizeCanvas.y / h_image;
            float scale = Mathf.Max(scalex, scaley);
            imageBg.transform.localScale = new Vector3(scale, scale, 1.0f);

        }

        {
            x = -this.frame.width / 4;
            y = 0;
            RectTransform rctran = objGameBox.GetComponent<RectTransform>();
            rctran.anchoredPosition = new Vector2(x, y);
        }

        {
            x = this.frame.width / 4;
            RectTransform rctran = objMath.GetComponent<RectTransform>();
            y = rctran.rect.height;
            rctran.anchoredPosition = new Vector2(x, y);
        }

        {
            x = this.frame.width / 4;
            RectTransform rctran = imageTitle.GetComponent<RectTransform>();
            y = -rctran.rect.height;
            rctran.anchoredPosition = new Vector2(x, y);
        }


    }
}
