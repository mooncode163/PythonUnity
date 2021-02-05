
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AppRes
{
    public const int GOLD_SHARE = 5;
    public const int GOLD_GUANKA = 3;
    public const int GOLD_COMMENT = 3;
    public const int GOLD_INIT_VALUE = 10;
    public const int GOLD_GUANKA_STEP = 4;
    //color
    //f88816 248,136,22
    static public Color colorTitle = new Color(248 / 255f, 136 / 255f, 22 / 255f);

    //audio 
    public const string AUDIO_BG = "AppCommon/Audio/Bg";
    public const string AUDIO_BTN_CLICK = "AppCommon/Audio/BtnClick";
    public const string AUDIO_WORD_OK = "AppCommon/Audio/word_ok";
    public const string AUDIO_WORD_FAIL = "AppCommon/Audio/word-failed";
    public const string AUDIO_LETTER_DRAG_1 = "AppCommon/Audio/letter-drag-1";
    public const string AUDIO_LETTER_DRAG_2 = "AppCommon/Audio/letter-drag-2";
    public const string AUDIO_LETTER_DRAG_3 = "AppCommon/Audio/letter-drag-3";
    public const string AUDIO_LETTER_DRAG_4 = "AppCommon/Audio/letter-drag-4";
    public const string AUDIO_SELECT = "AppCommon/Audio/select";
    public const string AUDIO_SUCCESS_1 = "AppCommon/Audio/success-1";
    public const string AUDIO_SUCCESS_2 = "AppCommon/Audio/success-2";
    public const string Audio_PopupOpen = "AppCommon/Audio/PopUp/PopupOpen";
    public const string Audio_PopupClose = "AppCommon/Audio/PopUp/PopupClose";

    //prefab  
    public const string PREFAB_SETTING = "AppCommon/Prefab/Setting/UISettingController";
    public const string PREFAB_MOREAPP_CELL_ITEM = "AppCommon/Prefab/MoreApp/UIMoreAppCellItem";
    public const string PREFAB_GUANKA_CELL_ITEM = "AppCommon/Prefab/Guanka/UIGuankaCellItem";
    public const string PREFAB_MathFormulationCellItem = "AppCommon/Prefab/MathFormulation/UIMathFormulationCellItem";
    public const string PREFAB_UITIPS = "AppCommon/Prefab/TipsBar/UITips";


    public const string PREFAB_UIHowToPlayController = "AppCommon/Prefab/HowToPlay/UIHowToPlayController";
    public const string PREFAB_UIKaZhuLeController = "AppCommon/Prefab/KaZhuLe/UIKaZhuLeController";
    //image
    public const string IMAGE_UIVIEWALERT_BG_BOARD = "App/UI/Setting/SettingCellBgBlue";
    static public Vector4 borderUIViewAlertBgBoard = new Vector4(18f, 18f, 18f, 18f);
    public const string IMAGE_UIVIEWALERT_BG_BTN = "App/UI/Setting/SettingCellBgOringe";
    static public Vector4 borderUIViewAlertBgBtn = new Vector4(18f, 18f, 18f, 18);

    public const string IMAGE_BtnMusicOn = "App/UI/Home/MusicButton";
    public const string IMAGE_BtnMusicOff = "App/UI/Home/MusicButtonGrey";

    public const string IMAGE_BtnSoundOn = "App/UI/Home/SoundButton";
    public const string IMAGE_BtnSoundOff = "App/UI/Home/SoundButtonGrey";

    public const string IMAGE_LOGO = "App/UI/Home/Logo";

    public const string IMAGE_GUANKA_ITEM_DOT0 = "App/UI/Guanka/dot0";
    public const string IMAGE_GUANKA_ITEM_DOT1 = "App/UI/Guanka/dot1";
    public const string IMAGE_GUANKA_CELL_BG = "App/UI/Guanka/guanka_cell_bg";
    public const string IMAGE_GUANKA_CELL_BG_LOCK = "App/UI/Guanka/guanka_cell_bg_lock";

    public const string IMAGE_ITEM_PIC_NORMAL = "App/UI/Game/GameBox/chip2";
    public const string IMAGE_ITEM_PIC_ANIMATION = "App/UI/Game/GameBox/chipgreen2";
    public const string IMAGE_ITEM_PIC_SEL = "App/UI/Game/GameBox/chiporange2";
    public const string IMAGE_ITEM_PIC_ERROR = "App/UI/Game/GameBox/chipred2";


    public const string IMAGE_MATHFORMULATION_DOT_HEAD = "App/UI/Game/FormulationBar/head";
    public const string IMAGE_MATHFORMULATION_DOT_NUM = "App/UI/Game/FormulationBar/dot_num";
    public const string IMAGE_MATHFORMULATION_DOT_MATH = "App/UI/Game/FormulationBar/dot_math";


    public const string IMAGE_CELL_BG_BLUE = "App/UI/Setting/SettingCellBgBlue";
    public const string IMAGE_CELL_BG_ORINGE = "App/UI/Setting/SettingCellBgOringe";
    public const string IMAGE_CELL_BG_YELLOW = "App/UI/Setting/SettingCellBgYellow";
    static public Vector4 borderCellSettingBg = new Vector4(18f, 18f, 18f, 18f);


    //bg
    public const string IMAGE_COMMON_BG = "App/UI/Bg/GuankaBg";
    public const string IMAGE_GAME_BG = "App/UI/Bg/GameBg";
    public const string IMAGE_PLACE_BG = "App/UI/Bg/PlaceBg";
    public const string IMAGE_GUANKA_BG = "App/UI/Bg/GuankaBg";
    public const string IMAGE_LEARN_BG = "App/UI/Bg/LearnBg";
    public const string IMAGE_SETTING_BG = "App/UI/Bg/SettingBg"; 

    public const string IMAGE_MOREAPP_BG = "App/UI/Bg/GuankaBg";

    public const string IMAGE_GUANKA_CELL_ITEM_BG_UNLOCK = "App/UI/Guanka/guanka_item_unlock";
    public const string IMAGE_GUANKA_CELL_ITEM_BG_LOCK = "App/UI/Guanka/guanka_item_lock";
    public const string IMAGE_GUANKA_CELL_ITEM_BG_PLAY = "App/UI/Guanka/guanka_item_playing";


}
