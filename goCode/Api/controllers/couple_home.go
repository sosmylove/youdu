package controllers

import (
	entity2 "git.3717.cn/yusheng_api/models/entity"
	"git.3717.cn/yusheng_api/models/mysql"
	services2 "git.3717.cn/yusheng_api/services"
	"net/http"
)

func HandlerCoupleHome(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		GetCoupleHome(w, r)
	} else {
		response405(w, r)
	}
}

// GetCoupleHome
func GetCoupleHome(w http.ResponseWriter, r *http.Request) {
	// me
	me, _ := getTokenCouple(r)
	couple := me.Couple
	if couple == nil || couple.Id <= 0 {
		response200Data(w, r, struct {
			User *entity2.User `json:"user"`
		}{me})
	}
	// ta
	taId := services2.GetTaId(me)
	ta, _ := services2.GetUserById(taId)
	if ta != nil {
		ta.Password = ""
		ta.UserToken = ""
	}

	// togetherDay
	//togetherDay := services.GetCoupleTogetherDay(couple.Id)
	// wallPaper
	var wallPaper *entity2.WallPaper
	//查询情侣墙纸应用的哪一种类型
	var wallPaperSetType int
	var systemwallPaperContent string
	if getModelStatus("couple_wall") {
		wallPaperSetInfo, _ := mysql.GetSetInfoByCoupleId(couple.Id)
		if wallPaperSetInfo != nil {
			wallPaperSetType = wallPaperSetInfo.SetType
			//如果是系统推荐的强制 那么图片渲染出来
			if wallPaperSetType == 1 {
				systemwallPaperInfo, _ := mysql.GetSystemWallPaperById(wallPaperSetInfo.SystemWallPaperId)
				if systemwallPaperInfo == nil {
					wallPaperSetType = 0
				} else {
					systemwallPaperContent = systemwallPaperInfo.ContentImage
				}
			}
		}

		wallPaper, _ = services2.GetWallPaperByCouple(couple.Id)
	}
	// place
	//var placeMe, placeTa *entity.Place
	//if getModelStatus("couple_place") {
	//	placeMe, _ = services.GetPlaceLatestByUser(me.Id)
	//	placeTa, _ = services.GetPlaceLatestByUser(taId)
	//}
	// weather
	//var weatherTodayMe, weatherTodayTa *services.WeatherToday
	//if getModelStatus("couple_weather") {
	//	if placeMe != nil {
	//		weatherTodayMe, _ = services.GetWeatherToday(placeMe.Longitude, placeMe.Latitude)
	//	}
	//	if placeTa != nil {
	//		weatherTodayTa, _ = services.GetWeatherToday(placeTa.Longitude, placeTa.Latitude)
	//	}
	//}
	// 返回
	response200Data(w, r, struct {
		User *entity2.User `json:"user"`
		Ta   *entity2.User `json:"ta"`
		//TogetherDay int               `json:"togetherDay"`
		WallPaper              *entity2.WallPaper `json:"wallPaper"`
		WallPaperSetType       int                `json:"wallPaperSetType"`
		SystemwallPaperContent string             `json:"systemwallPaperContent"`
		//PlaceMe        *entity.Place          `json:"placeMe"`
		//PlaceTa        *entity.Place          `json:"placeTa"`
		//WeatherTodayMe *services.WeatherToday `json:"weatherTodayMe"`
		//WeatherTodayTa *services.WeatherToday `json:"weatherTodayTa"`
	}{
		me,
		ta,
		//togetherDay,
		wallPaper,
		wallPaperSetType,
		systemwallPaperContent,
		//placeMe,
		//placeTa,
		//weatherTodayMe,
		//weatherTodayTa,
	})
}
