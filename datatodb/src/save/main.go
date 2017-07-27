package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"gopkg.in/mgo.v2/bson"

	"github.com/tealeg/xlsx"
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
	for _, file := range fileList {
		// read excel from data folder
		fmt.Println(file)

		xlFile, err := xlsx.OpenFile(file)
		if err != nil {
			log.Println("open excel fail:", err)
			panic(err)
		}
		fmt.Println(len(xlFile.Sheets))
		for _, sheet := range xlFile.Sheets {
			// rows end with data is null
			// read row 5 to get stock name, and labels

			labelRaw := sheet.Rows[4]
			cols := len(labelRaw.Cells)
			labels := make([]string, cols)
			stockName := labelRaw.Cells[0].String()
			// TODO: add mgo collection
			fmt.Println("stock:", stockName)
			for i := 1; i < cols; i++ {
				labels[i] = labelRaw.Cells[i].String()
			}
			fmt.Println("labels:", labels)
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
				fmt.Println(data)
			}
		}
		// save to mongodb
	}
	fmt.Println("end")
}
