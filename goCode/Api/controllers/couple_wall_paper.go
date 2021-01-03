package controllers

import (
	entity2 "git.3717.cn/yusheng_api/models/entity"
	services2 "git.3717.cn/yusheng_api/services"
	"net/http"
)

func HandlerWallPaper(w http.ResponseWriter, r *http.Request) {
	checkModelStatus(w, r, "couple_wall")
	if r.Method == http.MethodPost {
		PostWallPaper(w, r)
	} else if r.Method == http.MethodGet {
		GetWallPaper(w, r)
	} else {
		response405(w, r)
	}
}

// PostWallPaper
func PostWallPaper(w http.ResponseWriter, r *http.Request) {
	user, _ := getTokenCouple(r)
	couple := user.Couple
	// 接收数据
	wallPaper := &entity2.WallPaper{}
	checkRequestBody(w, r, wallPaper)
	wallPaper.CoupleId = couple.Id
	// 开始增加/修改
	wallPaper, err := services2.UpdateWallPaper(wallPaper)
	response417ErrToast(w, r, err)
	// 返回
	response200DataToast(w, r, "db_update_success", struct {
		WallPaper *entity2.WallPaper `json:"wallPaper"`
	}{wallPaper})
}

// GetWallPaper
func GetWallPaper(w http.ResponseWriter, r *http.Request) {
	user, _ := getTokenCouple(r)
	couple := user.Couple
	//接受参数
	values := r.URL.Query()
	action := values.Get("action")
	//获取系统墙纸
	if action == "system" {
		systemWallPaper, err := services2.GetSystemWallPaper()
		response200ErrShow(w, r, err)
		// 返回
		response200Data(w, r, struct {
			SystemWallPaper []*entity2.SystemWallPaper `json:"systemWallPaper"`
		}{systemWallPaper})
	}
	// 获取bg
	wallPaper, err := services2.GetWallPaperByCouple(couple.Id)
	response200ErrShow(w, r, err)
	// 返回
	response200Data(w, r, struct {
		WallPaper *entity2.WallPaper `json:"wallPaper"`
	}{wallPaper})
}
