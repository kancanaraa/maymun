package main
import ("github.com/gin-gonic/gin"
"gorm.io/driver/sqlite"

    "gorm.io/gorm"
"time")

type Sex struct {
	Date time.Time `json:"date"`
	Coin string `json:"coin"`
	ResolutionNo uint `json:"resolutionNo"`
	Resolution string `json:"resolution"`
	Signal string `json:"signal"`
	Price string `json:"price"`
}

func main() {
	db, err := gorm.Open(sqlite.Open("ovye.db"), &gorm.Config{})
	if err != nil {
		panic("db conn err")
	}
	db.AutoMigrate(&Sex{})
	app := gin.Default()

	app.POST("/bekiringotu", func(c *gin.Context) {
		var body Sex
		err := c.BindJSON(&body)
		if err != nil {
			c.JSON(400,err)
		}
		if err = db.Create(&body).Error; err != nil {
			c.Status(400)
		}
		c.JSON(200, body)
		
	})

	app.GET("/bekiringotleri", func(c *gin.Context) {
		c.JSON(200,"a")
	})

	app.Run(":80")
}
