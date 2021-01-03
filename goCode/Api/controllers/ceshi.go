package controllers

import (
	utils2 "git.3717.cn/yusheng_api/libs/utils"
	"net/http"
	"time"
)

func HandleCeshi(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		GetCeshi(w, r)
	} else {
		response405(w, r)
	}
}

func GetCeshi(w http.ResponseWriter, r *http.Request) {
	sjc := time.Now().Unix()
	aaa := time.Unix(time.Now().Unix(), 0).Format("2006-01-02 15:04:05")
	utils2.LogInfo("测试借款国：：", aaa)
	utils2.LogInfo("测试时间戳结果：：", sjc)
}
