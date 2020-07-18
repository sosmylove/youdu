package admin

import (
	"github.com/astaxie/beego/cache"
	"github.com/astaxie/beego/utils/captcha"
	"youdu/models"
)
var cpt *captcha.Captcha

func init(){
	store := cache.NewMemoryCache()
	cpt = captcha.NewWithFilter("/captcha/", store)
	// 调整验证码的尺寸像素
	cpt.ChallengeNums=4
	cpt.StdWidth = 100
	cpt.StdHeight = 40
}

type LoginController struct {
	BaseController // 继承这个结构体!
}

func (c *LoginController) Get() {
	c.TplName = "admin/login/login.html"
}

func (c *LoginController) DoLogin() {
	var flag = cpt.VerifyReq(c.Ctx.Request)
	if flag{
		// 2获取表单数据(用户名和密码)和数据库进行匹配！
		username := c.GetString("username")
		password := models.Md5(c.GetString("password"))//把获取的密码进行加密然后跟数据库匹对!

		// 3 和数据库匹配! 查询所有 返回的是一个切片
		info := []models.Manager{}
		// 4判断什么情况才让用户登录!  status=1证明是有这个权限在 ==0就是用户开除了!
		models.DB.Where("username=? AND password=? AND status=1",username,password).Find(&info)//把获取的数据的地址放进去
		

		if len(info)>0{
			c.SetSession("userinfo", info[0])
			c.Success("登录成功！","/")
		}else{
			c.Error("登录失败-用户名或者密码错误! 或者的账户已经被管理员限制登录了!!!", "/login")
		}
	}else{
		c.Error("验证码错误!", "/login")
	}
}

func (c *LoginController) LoginOut(){
	// 销毁session  就实现了退出登录!
	c.DelSession("userinfo")
	c.Success("退出登录成功!","/login")
}