package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

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
			for _, row := range sheet.Rows {
				for _, cell := range row.Cells {
					text := cell.String()
					fmt.Printf("%s\n", text)
				}
			}
		}
		// save to mongodb
	}
	fmt.Println("end")
}
