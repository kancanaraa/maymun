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
		jsonData, _ := ioutil.ReadAll(c.Request.Body)
		data := string(jsonData)
		split := strings.Split(data, ",")
		if len(split) == 6 {
			date := time.Time(split[0])
			coin := split[1]
			resolutionNo := split[2]
			resolution := split[3]
			signal := split[4]
			price := split[5]
			obj := &Sex{
				Date: date,
				Coin: coin,
				ResolutionNo: resolutionNo,
				Resolution: resolution,
				Signal: signal,
				Price: price,
			}
			if err = db.Create(&obj).Error; err != nil {
				c.Status(400)
			}
			c.JSON(200, obj)
		}	
		
	})

	app.GET("/bekiringotleri", func(c *gin.Context) {
		var gots []Sex
		result := db.Find(&gots)
		if result.Error != nil {
			c.JSON(400, result.Error)
		}
		c.JSON(200, gots)
	})

	app.Run(":80")
}
