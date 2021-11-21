package main
import (
	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"io/ioutil"
	"strings"
	"strconv"
    "gorm.io/gorm"
	"time"
)

type CoinInfo struct {
	Id uint `json:"id"`
	Date time.Time `json:"date"`
	Coin string `json:"coin"`
	ResolutionNo int `json:"resolutionNo"`
	Resolution string `json:"resolution"`
	Signal string `json:"signal"`
	Price string `json:"price"`
	Algorithm string `json:"algorithm"`
}

func main() {
	db, err := gorm.Open(sqlite.Open("coin.db"), &gorm.Config{})
	if err != nil {
		panic("db conn err")
	}
	db.AutoMigrate(&CoinInfo{})
	app := gin.Default()

	app.POST("/createCoinInfo", func(c *gin.Context) {
		jsonData, _ := ioutil.ReadAll(c.Request.Body)
		data := string(jsonData)
		split := strings.Split(data, ",")
		if len(split) == 7 {
			date,_ := time.Parse(time.RFC3339, split[0])
			coin := split[1]
			i, _ := strconv.Atoi(split[2])
			resolutionNo := i
			resolution := split[3]
			signal := split[4]
			price := split[5]
			algorithm := split[6]
			obj := &CoinInfo{
				Date: date,
				Coin: coin,
				ResolutionNo: resolutionNo,
				Resolution: resolution,
				Signal: signal,
				Price: price,
				Algorithm: algorithm,
			}
			if err = db.Create(&obj).Error; err != nil {
				c.Status(400)
			}
			c.JSON(200, obj)
		}	
		
	})

	app.GET("/getCoinInfos", func(c *gin.Context) {
		var gots []CoinInfo
		result := db.Find(&gots)
		if result.Error != nil {
			c.JSON(400, result.Error)
		}
		c.JSON(200, gots)
	})

	app.GET("/getCoinInfosTake/:take", func(c *gin.Context) {
		take := c.Param("take")
		var gots []CoinInfo
		result := db.Order("id desc").Limit(take).Find(&gots)
		if result.Error != nil {
			c.JSON(400, result.Error)
		}
		c.JSON(200, gots)
	})

	app.Run(":80")
}
