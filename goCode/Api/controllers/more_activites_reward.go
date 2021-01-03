package controllers

import (
	services2 "git.3717.cn/yusheng_api/services"
	"net/http"
)

func HandlerActivitesReward(w http.ResponseWriter, r *http.Request) {
	checkModelStatus(w, r, "activity_reward_vip")
	if r.Method == http.MethodGet {
		GetActivitesReward(w, r)
	} else {
		response405(w, r)
	}
}

func GetActivitesReward(w http.ResponseWriter, r *http.Request) {
	page := 0
	list, err := services2.GetParticipateVipList(page)
	response200ErrShow(w, r, err)
	response200Data(w, r, struct {
		ActivitiesRewardList []interface{} `json:"activitiesRewardList"`
	}{list})
}
