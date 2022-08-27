package database

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

const (
	dbName = "database/db"
)

type Vacancy struct {
	Id       int
	Name     string
	IsActive bool
	Token    string
}

func NewDB() (db *sql.DB, err error) {
	log.Print("init db")

	db, err = sql.Open("sqlite3", dbName)
	if err != nil {
		return
	}

	var version string
	err = db.
		QueryRow("SELECT SQLITE_VERSION()").
		Scan(&version)

	if err != nil {
		return
	}

	return
}

func Migrate(db *sql.DB) (err error) {
	log.Print("migrate db")

	query := `
		create table if not exists vacancies(
			id integer primary key autoincrement,
			name var(255) not null,
			description var(1023) not null,
			is_active bool not null default false,
			token var(255) not null
		);`

	_, err = db.Exec(query)

	return
}
