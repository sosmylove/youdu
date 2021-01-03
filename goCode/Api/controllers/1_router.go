package controllers

import (
	"context"
	"fmt"
	utils2 "git.3717.cn/yusheng_api/libs/utils"
	entity2 "git.3717.cn/yusheng_api/models/entity"
	sentryhttp "github.com/getsentry/sentry-go/http"
	"io/ioutil"
	"net/http"
	"time"

	"strings"
)

const (
	// v2重开项目
	URL_V1 = "/v2"

	//signChallenge(签到挑战1314)
	URL_SIGN_CHALLENGE                 = URL_V1 + "/signChallenge"
	URL_SIGN_CALENDAR                  = URL_SIGN_CHALLENGE + "/calendar"      //签到日历
	URL_SIGN_CHALLENGE_FILL_CHECK_CARD = URL_SIGN_CHALLENGE + "/fillCheckCard" //补签卡

	//用户登录游戏
	URL_COUPLE_GAME = URL_V1 + "/coupleGame"
	// ios获取纪念日提示
	URL_NOTE_IOS_TIP = URL_V1 + "/souvenirIosTip"
	//时光轴页面分享
	URL_SHARE_TIME_AXIS = URL_V1 + "/shareTimeAxis"

	// common
	URL_API                  = URL_V1 + "/api"             // api
	URL_SMS                  = URL_V1 + "/sms"             // 短信
	URL_USER                 = URL_V1 + "/user"            // 用户
	URL_USER_LOGIN           = URL_USER + "/login"         // 登录
	URL_USER_GET_INVITE_CODE = URL_USER + "/getInviteCode" // 获取邀请码
	URL_ENTRY                = URL_V1 + "/entry"           // 进入
	URL_OSS                  = URL_V1 + "/oss"             // oss
	URL_GOODS_LIST           = URL_V1 + "/goods"           // 获取商品列表. 会员、金币

	// settings
	URL_SET                 = URL_V1 + "/set"
	URL_SET_VERSION         = URL_SET + "/version"         // 版本
	URL_SET_NOTICE          = URL_SET + "/notice"          // 公告
	URL_SET_SUGGEST         = URL_SET + "/suggest"         // 建议
	URL_SET_SUGGEST_COMMENT = URL_SET_SUGGEST + "/comment" // 评论
	URL_SET_SUGGEST_FOLLOW  = URL_SET_SUGGEST + "/follow"  // 关注
	// couple(我和TA)
	RUL_COUPLE               = URL_V1 + "/couple"            // 配对
	RUL_COUPLE_HOME          = RUL_COUPLE + "/home"          // 首页
	RUL_COUPLE_WALLPAPER     = RUL_COUPLE + "/wallPaper"     // 墙纸
	RUL_COUPLE_WALLPAPER_SET = RUL_COUPLE_WALLPAPER + "/set" // 墙纸设置
	RUL_COUPLE_PLACE         = RUL_COUPLE + "/place"         // 地址
	//RUL_COUPLE_WEATHER   = RUL_COUPLE + "/weather"   // 天气
	// note(小本本)
	URL_NOTE          = URL_V1 + "/note"
	URL_NOTE_HOME     = URL_NOTE + "/home"     // 首页
	URL_NOTE_LOCK     = URL_NOTE + "/lock"     // 密码锁
	URL_NOTE_TRENDS   = URL_NOTE + "/trends"   // 动态 + 统计
	URL_NOTE_SOUVENIR = URL_NOTE + "/souvenir" // 纪念日 + 愿望清单
	// v2.1新版本纪念日
	URL_NOTE_NEW_SOUVENIR = URL_NOTE + "/souvenirs" // 纪念日

	URL_NOTE_MENSES_INFO   = URL_NOTE + "/mensesInfo"    // 姨妈头信息
	URL_NOTE_MENSES_DAY    = URL_NOTE + "/mensesDay"     // 姨妈日信息
	URL_NOTE_MENSES        = URL_NOTE + "/menses"        // 姨妈 android<20
	URL_NOTE_MENSES2       = URL_NOTE + "/menses2"       // 姨妈 android>=20
	URL_NOTE_SHY           = URL_NOTE + "/shy"           // 羞羞
	URL_NOTE_SLEEP         = URL_NOTE + "/sleep"         // 睡眠
	URL_NOTE_AUDIO         = URL_NOTE + "/audio"         // 音频
	URL_NOTE_VIDEO         = URL_NOTE + "/video"         // 视频
	URL_NOTE_ALBUM         = URL_NOTE + "/album"         // 相册
	URL_NOTE_PICTURE       = URL_NOTE + "/picture"       // 照片
	URL_NOTE_WORD          = URL_NOTE + "/word"          // 留言
	URL_NOTE_WHISPER       = URL_NOTE + "/whisper"       // 耳语
	URL_NOTE_DIARY         = URL_NOTE + "/diary"         // 日记
	URL_NOTE_AWARD         = URL_NOTE + "/award"         // 打卡
	URL_NOTE_AWARD_RULE    = URL_NOTE_AWARD + "/rule"    // 约定
	URL_NOTE_DREAM         = URL_NOTE + "/dream"         // 梦境
	URL_NOTE_GIFT          = URL_NOTE + "/gift"          // 礼物
	URL_NOTE_FOOD          = URL_NOTE + "/food"          // 美食
	URL_NOTE_TRAVEL        = URL_NOTE + "/travel"        // 游记
	URL_NOTE_ANGRY         = URL_NOTE + "/angry"         // 生气
	URL_NOTE_PROMISE       = URL_NOTE + "/promise"       // 承诺
	URL_NOTE_PROMISE_BREAK = URL_NOTE_PROMISE + "/break" // 违规
	URL_NOTE_MOVIE         = URL_NOTE + "/movie"         // 电影
	//时光轴
	URL_NOTE_TIME_AXIS = URL_NOTE + "/timeAxis" // 时光轴
	// topic(恋爱吧)
	URL_TOPIC                     = URL_V1 + "/topic"
	URL_TOPIC_HOME                = URL_TOPIC + "/home"                // 首页
	URL_TOPIC_MESSAGE             = URL_TOPIC + "/message"             // 消息
	URL_TOPIC_POST                = URL_TOPIC + "/post"                // 帖子
	URL_TOPIC_POST_READ           = URL_TOPIC_POST + "/read"           // 阅读
	URL_TOPIC_POST_REPORT         = URL_TOPIC_POST + "/report"         // 举报
	URL_TOPIC_POST_POINT          = URL_TOPIC_POST + "/point"          // 点赞
	URL_TOPIC_POST_COLLECT        = URL_TOPIC_POST + "/collect"        // 收藏
	URL_TOPIC_POST_COMMENT        = URL_TOPIC_POST + "/comment"        // 评论
	URL_TOPIC_POST_COMMENT_REPORT = URL_TOPIC_POST_COMMENT + "/report" // 评论举报
	URL_TOPIC_POST_COMMENT_POINT  = URL_TOPIC_POST_COMMENT + "/point"  // 评论点赞
	// 我的页面(原步行街)
	URL_MY_PAGE = URL_V1 + "/myPage" // 我的页面
	// more(步行街)
	URL_MORE                        = URL_V1 + "/more"
	URL_MORE_HOME                   = URL_MORE + "/home"      // 首页
	URL_MORE_BROADCAST              = URL_MORE + "/broadcast" // 广播
	URL_MORE_BILL                   = URL_MORE + "/bill"      // 账单
	URL_MORE_VIP                    = URL_MORE + "/vip"       // 会员
	URL_MORE_COIN                   = URL_MORE + "/coin"      // 金币
	URL_MORE_SIGN                   = URL_MORE + "/sign"      // 签到
	URL_MORE_MATCH                  = URL_MORE + "/match"
	URL_MORE_MATCH_PERIOD           = URL_MORE_MATCH + "/period" // 比赛期数
	URL_MORE_MATCH_WORK             = URL_MORE_MATCH + "/work"   // 比赛作品
	URL_MORE_MATCH_REPORT           = URL_MORE_MATCH + "/report" // 比赛举报
	URL_MORE_MATCH_POINT            = URL_MORE_MATCH + "/point"  // 比赛点赞
	URL_MORE_MATCH_COIN             = URL_MORE_MATCH + "/coin"   // 比赛金币
	URL_MORE_FEATURE                = URL_MORE + "/feature"
	URL_MORE_FEATURE_WISH           = URL_MORE_FEATURE + "/wish"           // 许愿树
	URL_MORE_FEATURE_WISH_BLESSINGS = URL_MORE_FEATURE_WISH + "/blessings" // 愿望祝福
	URL_MORE_FEATURE_CARD           = URL_MORE_FEATURE + "/card"           // 明信卡
	URL_ACTIVITES_REWARD            = URL_MORE + "/activitesReward"        // 活动奖励
	URL_USER_MONEY_LOG              = URL_MORE + "/userMoneyLog"           // 获取用户金额流水
	CESHI                           = URL_V1 + "/ceshi"                    // 测试代码
)

// InitRoutes
func InitRoutes() {
	// 服务维护
	if !utils2.GetConfigBool("conf", "model.conf", "model", "servicing") {
		http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
			defer onRequestStop()
			response503(w, r)
		})
		return
	}
	// 路径错误
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		defer onRequestStop()
		Response404(w, r)
	})

	//用户登录游戏
	http.HandleFunc(URL_COUPLE_GAME, check(HandlerCoupleGame, true, false))
	//时光轴分享页面
	http.HandleFunc(URL_SHARE_TIME_AXIS, check(HandlerShareTimeAxis, false, false))

	//signChallenge
	http.HandleFunc(URL_SIGN_CALENDAR, check(HandlerSignCalendar, true, true))
	http.HandleFunc(URL_SIGN_CHALLENGE_FILL_CHECK_CARD, check(HandlerUserFillCheckCard, true, true))

	http.HandleFunc(URL_NOTE_IOS_TIP, check(HandlerIosTip, true, false))

	// common
	http.HandleFunc(URL_SMS, check(HandlerSms, false, false))
	http.HandleFunc(URL_USER, check(HandlerUser, false, false))
	http.HandleFunc(URL_USER_LOGIN, check(HandlerUserLogin, false, false))
	http.HandleFunc(URL_API, check(HandlerApi, true, false))
	http.HandleFunc(URL_ENTRY, check(HandlerEntry, true, false))
	http.HandleFunc(URL_OSS, check(HandlerOss, true, false))
	http.HandleFunc(URL_USER_GET_INVITE_CODE, check(HandlerUserInviteCode, true, true))
	http.HandleFunc(URL_GOODS_LIST, check(HandlerGoods, true, false))
	// settings
	http.HandleFunc(URL_SET_VERSION, check(HandlerVersion, true, false))
	http.HandleFunc(URL_SET_NOTICE, check(HandlerNotice, true, false))
	http.HandleFunc(URL_SET_SUGGEST, check(HandlerSuggest, true, false))
	http.HandleFunc(URL_SET_SUGGEST_COMMENT, check(HandlerSuggestComment, true, false))
	http.HandleFunc(URL_SET_SUGGEST_FOLLOW, check(HandlerSuggestFollow, true, false))
	// couple
	http.HandleFunc(RUL_COUPLE, check(HandlerCouple, true, false))
	http.HandleFunc(RUL_COUPLE_HOME, check(HandlerCoupleHome, true, false))
	http.HandleFunc(RUL_COUPLE_WALLPAPER, check(HandlerWallPaper, true, true))
	http.HandleFunc(RUL_COUPLE_WALLPAPER_SET, check(HandlerWallPaperSet, true, true))
	http.HandleFunc(RUL_COUPLE_PLACE, check(HandlerPlace, true, true))
	//http.HandleFunc(RUL_COUPLE_WEATHER, check(HandlerWeather, true, true))
	// note
	http.HandleFunc(URL_NOTE_TIME_AXIS, check(HandlerTimeAxis, true, true))
	http.HandleFunc(URL_NOTE_HOME, check(HandlerNoteHome, true, true))
	http.HandleFunc(URL_NOTE_LOCK, check(HandlerLock, true, true))
	http.HandleFunc(URL_NOTE_TRENDS, check(HandlerTrends, true, true))
	http.HandleFunc(URL_NOTE_SOUVENIR, check(HandlerSouvenir, true, true))
	http.HandleFunc(URL_NOTE_NEW_SOUVENIR, check(HandlerSouvenirs, true, true))
	http.HandleFunc(URL_NOTE_MENSES_INFO, check(HandlerMensesInfo, true, true))
	http.HandleFunc(URL_NOTE_MENSES, check(HandlerMenses, true, true))
	http.HandleFunc(URL_NOTE_MENSES2, check(HandlerMenses2, true, true))
	http.HandleFunc(URL_NOTE_MENSES_DAY, check(HandlerMensesDay, true, true))
	http.HandleFunc(URL_NOTE_SHY, check(HandlerShy, true, true))
	http.HandleFunc(URL_NOTE_SLEEP, check(HandlerSleep, true, true))
	http.HandleFunc(URL_NOTE_WORD, check(HandlerWord, true, true))
	http.HandleFunc(URL_NOTE_WHISPER, check(HandlerWhisper, true, true))
	http.HandleFunc(URL_NOTE_DIARY, check(HandlerDiary, true, true))
	http.HandleFunc(URL_NOTE_ALBUM, check(HandlerAlbum, true, true))
	http.HandleFunc(URL_NOTE_PICTURE, check(HandlerPicture, true, true))
	http.HandleFunc(URL_NOTE_AUDIO, check(HandlerAudio, true, true))
	http.HandleFunc(URL_NOTE_VIDEO, check(HandlerVideo, true, true))
	http.HandleFunc(URL_NOTE_FOOD, check(HandlerFood, true, true))
	http.HandleFunc(URL_NOTE_TRAVEL, check(HandlerTravel, true, true))
	http.HandleFunc(URL_NOTE_GIFT, check(HandlerGift, true, true))
	http.HandleFunc(URL_NOTE_PROMISE, check(HandlerPromise, true, true))
	http.HandleFunc(URL_NOTE_PROMISE_BREAK, check(HandlerPromiseBreak, true, true))
	http.HandleFunc(URL_NOTE_ANGRY, check(HandlerAngry, true, true))
	http.HandleFunc(URL_NOTE_DREAM, check(HandlerDream, true, true))
	http.HandleFunc(URL_NOTE_AWARD, check(HandlerAward, true, true))
	http.HandleFunc(URL_NOTE_AWARD_RULE, check(HandlerAwardRule, true, true))
	http.HandleFunc(URL_NOTE_MOVIE, check(HandlerMovie, true, true))

	// topic
	http.HandleFunc(URL_TOPIC_HOME, check(HandlerTopicHome, true, false))
	http.HandleFunc(URL_TOPIC_MESSAGE, check(HandlerTopicMessage, true, true))
	http.HandleFunc(URL_TOPIC_POST, check(HandlerPost, true, false))
	http.HandleFunc(URL_TOPIC_POST_READ, check(HandlerPostRead, true, false))
	http.HandleFunc(URL_TOPIC_POST_REPORT, check(HandlerPostReport, true, true))
	http.HandleFunc(URL_TOPIC_POST_POINT, check(HandlerPostPoint, true, true))
	http.HandleFunc(URL_TOPIC_POST_COLLECT, check(HandlerPostCollect, true, true))
	http.HandleFunc(URL_TOPIC_POST_COMMENT, check(HandlerPostComment, true, false))
	http.HandleFunc(URL_TOPIC_POST_COMMENT_REPORT, check(HandlerPostCommentReport, true, true))
	http.HandleFunc(URL_TOPIC_POST_COMMENT_POINT, check(HandlerPostCommentPoint, true, true))
	// myPage
	http.HandleFunc(URL_MY_PAGE, check(HandlerMyPage, true, false))
	// more
	http.HandleFunc(URL_MORE_HOME, check(HandlerMoreHome, true, false))
	http.HandleFunc(URL_MORE_BROADCAST, check(HandlerBroadcast, true, false))
	http.HandleFunc(URL_MORE_BILL, check(HandlerBill, true, true))
	http.HandleFunc(URL_MORE_VIP, check(HandlerVip, true, true))
	http.HandleFunc(URL_MORE_COIN, check(HandlerCoin, true, true))
	http.HandleFunc(URL_MORE_SIGN, check(HandlerSign, true, true))
	http.HandleFunc(URL_MORE_MATCH_PERIOD, check(HandlerMatchPeriod, true, false))
	http.HandleFunc(URL_MORE_MATCH_WORK, check(HandlerMatchWork, true, false))
	http.HandleFunc(URL_MORE_MATCH_REPORT, check(HandlerMatchReport, true, true))
	http.HandleFunc(URL_MORE_MATCH_POINT, check(HandlerMatchPoint, true, true))
	http.HandleFunc(URL_MORE_MATCH_COIN, check(HandlerMatchCoin, true, true))
	http.HandleFunc(URL_ACTIVITES_REWARD, check(HandlerActivitesReward, true, false))
	http.HandleFunc(URL_MORE_FEATURE_WISH, check(HandlerWishTree, true, false))
	http.HandleFunc(URL_MORE_FEATURE_WISH_BLESSINGS, check(HandleWishBlessings, true, false))
	http.HandleFunc(URL_USER_MONEY_LOG, check(HandlerUserMoneyLog, true, true))

	//线上测试代码
	http.HandleFunc(CESHI, check(HandleCeshi, false, false))
}

// check 打印日志的handler
func check(handler func(w http.ResponseWriter, r *http.Request), user bool, couple bool) func(w http.ResponseWriter, r *http.Request) {
	sentryHandler := sentryhttp.New(sentryhttp.Options{
		Repanic: true,
	})
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*") //允许访问所有域
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Add("Access-Control-Allow-Headers", "accessToken,appKey,User-Agent,DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type") //header的类型
		w.Header().Set("content-type", "application/json")
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}
		// 手动终止http
		defer onRequestStop()
		// 检查header
		checkRequestHeader(w, r)
		// api记录
		start := time.Now()
		var u *entity2.User
		defer func() {
			// 要看开关是否打开
			if !getModelStatus("api") {
				return
			}
			platform := strings.ToLower(strings.TrimSpace(r.Header.Get(HEAD_PARAMS_PLATFORM1)))
			if len(platform) <= 0 {
				platform = strings.ToLower(strings.TrimSpace(r.Header.Get(HEAD_PARAMS_PLATFORM2)))
			}
			language := strings.ToLower(strings.TrimSpace(r.Header.Get(HEAD_PARAMS_LANGUAGE1)))
			if len(language) <= 0 {
				language = strings.ToLower(strings.TrimSpace(r.Header.Get(HEAD_PARAMS_LANGUAGE2)))
			}
			// 构造request对象
			api := &entity2.Api{
				Platform: platform,
				Language: language,
				URI:      r.URL.Path,
				Method:   r.Method,
				Params:   r.URL.RawQuery,
				Body:     string(getRequestBody(r)),
				Result:   "",
				Duration: time.Since(start).Seconds(),
			}
			if u != nil {
				api.UserId = u.Id
			} else {
				api.UserId = 0
			}
			//services.AddApi(api) // 删除吧，太耗mysql资源了
		}()
		// 检查 + 传递user
		if user || couple {
			if couple {
				u = checkTokenCouple(w, r)
			} else if user {
				u = checkTokenUser(w, r)
			}
			ctx := context.WithValue(r.Context(), CONTEXT_KEY_USER, u)
			r = r.WithContext(ctx)
		}
		// 读取 + 传递body
		defer r.Body.Close()
		bytes, _ := ioutil.ReadAll(r.Body)
		ctx := context.WithValue(r.Context(), CONTEXT_KEY_BODY, bytes)
		r = r.WithContext(ctx)
		// 开始http
		handlerFunc := sentryHandler.Handle(http.HandlerFunc(handler))
		handlerFunc.ServeHTTP(w, r)
	})
}

// onRequestStop 手动终止http
func onRequestStop() {
	if rec := recover(); rec != nil {
		sprint := fmt.Sprintf("%v", rec)
		utils2.LogErr("异常终止router\n", sprint)
	}
}
