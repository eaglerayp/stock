package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	mgo "gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"

	"github.com/tealeg/xlsx"
)

const (
	db = "stock"
)

func main() {

	searchDir := "data"

	fileList := []string{}
	err := filepath.Walk(searchDir, func(path string, f os.FileInfo, err error) error {
		if !f.IsDir() {
			fileList = append(fileList, path)
		}
		return nil
	})
	if err != nil {
		panic(err)
	}
	// TODO: connect mongodb

	dialInfo := mgo.DialInfo{
		Addrs:     []string{"127.0.0.1:20379"},
		FailFast:  true,
		Username:  "",
		Password:  "",
		PoolLimit: 1,
	}
	maxAttempts := 20
	var session *mgo.Session
	for attempts := 1; attempts <= maxAttempts; attempts++ {
		session, err = mgo.DialWithInfo(&dialInfo)
		if err == nil {
			break
		}
		time.Sleep(time.Duration(attempts) * time.Second)
	}
	if err != nil {
		panic("[mongo] no reachable server")
	}

	for _, file := range fileList {
		// read excel from data folder
		fmt.Println("File:", file)

		xlFile, err := xlsx.OpenFile(file)
		if err != nil {
			log.Println("open excel fail:", err)
			panic(err)
		}

		for _, sheet := range xlFile.Sheets {
			// rows end with data is null
			// read row 5 to get stock name, and labels

			labelRaw := sheet.Rows[4]
			cols := len(labelRaw.Cells)
			labels := make([]string, cols)
			stockName := labelRaw.Cells[0].String()
			col := session.DB(db).C(stockName)
			bulk := col.Bulk()
			bulk.Unordered()
			// TODO: add mgo collection
			fmt.Println("stock:", stockName)
			for i := 1; i < cols; i++ {
				labels[i] = labelRaw.Cells[i].String()
			}
			// fmt.Println("labels:", labels)
			rawsNum := len(sheet.Rows)
			if rawsNum > 1365 {
				rawsNum = 1365
			}
			for i := 5; i < rawsNum; i++ {
				raw := sheet.Rows[i]
				data := bson.M{}
				cols = len(raw.Cells)
				for j := 1; j < cols; j++ {
					// from cell 2 ~  n
					// try int, float, then string
					key := labels[j]
					ivalue, err := raw.Cells[j].Int()
					if err == nil {
						data[key] = ivalue
						continue
					}
					fvalue, err := raw.Cells[j].Float()
					if err == nil {
						data[key] = fvalue
						continue
					}
					svalue := raw.Cells[j].String()
					data[key] = svalue
				}
				// TODO:bulk insert
				bulk.Insert(data)
				// fmt.Println(data)
			}
			_, err = bulk.Run()
			if err != nil {
				log.Println("bulk insert error:", err)
			}
		}
		// save to mongodb
	}
	fmt.Println("end")
}
