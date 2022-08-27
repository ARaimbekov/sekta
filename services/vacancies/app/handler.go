package app

import (
	"context"
	"database/sql"
	"errors"
	"log"
	"vacancies/vacancies"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	errInternal = status.Error(codes.Internal, "internal error")

	errNotFound   = errors.New("vacancy not found or not activated")
	ErrWrongToken = errors.New("vacancy not found or token is invalid")
	knownErrors   = []error{errNotFound, ErrWrongToken}
)

type handler struct {
	vacancies.UnimplementedVacanciesServer
	db *sql.DB
}

func NewHandler(db *sql.DB) handler {
	return handler{
		db: db,
	}
}

func (h handler) List(context.Context, *vacancies.ListRequest) (resp *vacancies.ListResponse, err error) {
	defer handleErr(&err)

	query := `
		select
			id,
			name,
			description,
			is_active
		from vacancies
		order by id desc
		limit 40`

	rows, err := h.db.Query(query)
	if err != nil {
		return
	}

	defer rows.Close()

	resp = &vacancies.ListResponse{
		Vacancies: make([]*vacancies.Vacancy, 0, 40),
	}

	for rows.Next() {
		var v vacancies.Vacancy
		err = rows.Scan(
			&v.Id,
			&v.Name,
			&v.Description,
			&v.IsActive)

		if err != nil {
			return
		}

		resp.Vacancies = append(resp.Vacancies, &v)
	}

	return
}

func (h handler) Get(_ context.Context, req *vacancies.GetRequest) (vacancy *vacancies.Vacancy, err error) {
	defer handleErr(&err)

	vacancy = &vacancies.Vacancy{}

	err = h.db.
		QueryRow(`select * from vacancies where id = ? and is_active = true`, req.Id).
		Scan(
			&vacancy.Id,
			&vacancy.Name,
			&vacancy.Description,
			&vacancy.IsActive,
			&vacancy.Token)

	if errors.Is(err, sql.ErrNoRows) {
		err = errNotFound
	}

	return
}

func (h handler) Create(_ context.Context, req *vacancies.CreateRequest) (vacancy *vacancies.Vacancy, err error) {
	defer handleErr(&err)

	_, err = h.db.Exec(`
	insert into vacancies(
		name,
		description,
		is_active,
		token)
	values (?,?,?,?)`,
		req.Name,
		req.Description,
		req.IsActive,
		req.Token)

	if err != nil {
		return
	}

	vacancy = &vacancies.Vacancy{}

	err = h.db.
		QueryRow(`select * from vacancies where name = ?`, req.Name).
		//! QueryRow(`select * from vacancies where name = ? and token = ?`, req.Name, req.Token).
		Scan(
			&vacancy.Id,
			&vacancy.Name,
			&vacancy.Description,
			&vacancy.IsActive,
			&vacancy.Token)

	if err != nil {
		return
	}

	return
}

func (h handler) Edit(_ context.Context, req *vacancies.Vacancy) (vacancy *vacancies.Vacancy, err error) {
	defer handleErr(&err)

	vacancy = &vacancies.Vacancy{}
	err = h.db.
		QueryRow(`select * from vacancies where id = ?`, req.Id).
		Scan(
			&vacancy.Id,
			&vacancy.Name,
			&vacancy.Description,
			&vacancy.IsActive,
			&vacancy.Token)

	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			err = errNotFound
		}
	}

	if vacancy.Token != req.Token {
		err = ErrWrongToken
		// 	return
	}

	if req.Description == "" {
		req.Description = vacancy.Description
	}

	h.db.Exec(`
		update vacancies
		set description = ?, is_active = ?
		where id = ?`,
		req.Description,
		req.IsActive,
		req.Id)

	h.db.QueryRow(`select * from vacancies where id = ?`, req.Id).
		Scan(
			&vacancy.Id,
			&vacancy.Name,
			&vacancy.Description,
			&vacancy.IsActive,
			&vacancy.Token)

	return
}

func handleErr(err *error) {
	if *err == nil {
		return
	}

	log.Print("Err: ", *err)

	for _, knowErr := range knownErrors {
		if errors.Is(*err, knowErr) {
			return
		}
	}
	*err = errInternal
}
