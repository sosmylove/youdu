package controllers

import (
	entity2 "git.3717.cn/yusheng_api/models/entity"
	services2 "git.3717.cn/yusheng_api/services"
	"net/http"
	"strconv"
)

func HandlerPlace(w http.ResponseWriter, r *http.Request) {
	checkModelStatus(w, r, "couple_place")
	if r.Method == http.MethodPost {
		PostPlace(w, r)
	} else if r.Method == http.MethodGet {
		GetPlace(w, r)
	} else {
		response405(w, r)
	}
}

// PostPlace
func PostPlace(w http.ResponseWriter, r *http.Request) {
	user, _ := getTokenCouple(r)
	couple := user.Couple
	// 接受参数
	placeMe := &entity2.Place{}
	checkRequestBody(w, r, placeMe)
	// 我的地址
	placeMe, err := services2.AddPlace(user.Id, couple.Id, placeMe)
	response417ErrToast(w, r, err)
	// ta的地址
	taId := services2.GetTaId(user)
	placeTa, err := services2.GetPlaceLatestByUserCouple(taId, couple.Id)
	response417ErrToast(w, r, err)
	// weather 还是要给的 避免一个地方不动长时间不能刷新天气
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
		PlaceMe *entity2.Place `json:"placeMe"`
		PlaceTa *entity2.Place `json:"placeTa"`
		//WeatherTodayMe *services.WeatherToday `json:"weatherTodayMe"`
		//WeatherTodayTa *services.WeatherToday `json:"weatherTodayTa"`
	}{placeMe,
		placeTa,
		//weatherTodayMe,
		//weatherTodayTa
	})
}

// GetPlace
func GetPlace(w http.ResponseWriter, r *http.Request) {
	user, _ := getTokenCouple(r)
	couple := user.Couple
	// 参数
	values := r.URL.Query()
	list, _ := strconv.ParseBool(values.Get("list"))
	group, _ := strconv.ParseBool(values.Get("group"))
	if list {
		admin, _ := strconv.ParseBool(values.Get("admin"))
		page, _ := strconv.Atoi(values.Get("page"))
		//查询的时候获取这个要查询的用户字段. 前端不传默认查全部
		uid, _ := strconv.ParseInt(values.Get("uid"), 10, 64)
		var placeList []*entity2.Place
		var err error
		if admin && services2.IsAdminister(user) {
			//uid, _ := strconv.ParseInt(values.Get("uid"), 10, 64)
			placeList, err = services2.GetPlaceList(uid, page)
		} else {
			placeList, err = services2.GetPlaceListByCouple(couple, page, user.Id, uid)
		}
		response200ErrShow(w, r, err)
		// 返回
		response200Data(w, r, struct {
			PlaceList []*entity2.Place `json:"placeList"`
		}{placeList})
	} else if group {
		// admin检查
		if !services2.IsAdminister(user) {
			response200Toast(w, r, "")
		}
		start, _ := strconv.ParseInt(values.Get("start"), 10, 64)
		end, _ := strconv.ParseInt(values.Get("end"), 10, 64)
		filed := values.Get("filed")
		infoList := make([]*entity2.FiledInfo, 0)
		if filed == "country" {
			infoList, _ = services2.GetPlaceGroupCountryList(start, end)
		} else if filed == "province" {
			infoList, _ = services2.GetPlaceGroupProvinceList(start, end)
		} else if filed == "city" {
			infoList, _ = services2.GetPlaceGroupCityList(start, end)
		} else if filed == "district" {
			infoList, _ = services2.GetPlaceGroupDistrictList(start, end)
		}
		// 返回
		response200Data(w, r, struct {
			InfoList []*entity2.FiledInfo `json:"infoList"`
		}{infoList})
	} else {
		response405(w, r)
	}
}
