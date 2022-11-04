package vacancy

import (
	"context"
	"errors"
	"log"
	"vacancies/internal/vacancy/protobuf"

	"gorm.io/gorm"
)

type Handler struct {
	protobuf.UnimplementedVacanciesServer
	service *Service
}

func NewHandler(db *gorm.DB) Handler {
	return Handler{
		service: &Service{
			storage: &Storage{
				db: db,
			},
		},
	}
}

func (h Handler) List(context.Context, *protobuf.ListRequest) (resp *protobuf.ListResponse, err error) {
	defer handleErr(&err)

	vs, err := h.service.List()
	if err != nil {
		return
	}

	resp = &protobuf.ListResponse{
		Vacancies: make([]*protobuf.Vacancy, 0, len(vs)),
	}

	for _, v := range vs {
		resp.Vacancies = append(resp.Vacancies, &protobuf.Vacancy{
			Id:          int32(v.Id),
			SectId:      int32(v.SektaId),
			Name:        v.Sect.Sektaname,
			Description: v.Description,
			IsActive:    v.IsActive,
		})
	}

	return
}

func (h Handler) Get(_ context.Context, req *protobuf.GetRequest) (vacancy *protobuf.Vacancy, err error) {
	defer handleErr(&err)

	dto := GetDTO{
		Id:   int(req.Id),
		Name: req.Name,
	}

	v, err := h.service.Get(&dto)
	if err != nil {
		return
	}

	vacancy = &protobuf.Vacancy{
		Id:          int32(v.Id),
		SectId:      int32(v.SektaId),
		Name:        v.Sect.Sektaname,
		Description: v.Description,
		IsActive:    v.IsActive,
		Token:       v.Token,
	}

	return
}

func (h Handler) Create(_ context.Context, req *protobuf.CreateRequest) (vacancy *protobuf.Vacancy, err error) {
	defer handleErr(&err)
	dto := CreateDTO{
		SectId:      int(req.SectId),
		Description: req.Description,
	}

	v, err := h.service.Create(&dto)
	if err != nil {
		return
	}

	vacancy = &protobuf.Vacancy{
		Id:          int32(v.Id),
		SectId:      int32(v.SektaId),
		Name:        v.Sect.Sektaname,
		Description: v.Description,
		IsActive:    v.IsActive,
		Token:       v.Token,
	}
	return
}

func (h Handler) Edit(_ context.Context, req *protobuf.Vacancy) (vacancy *protobuf.Vacancy, err error) {
	defer handleErr(&err)
	dto := EditDTO{
		Id:          int(req.Id),
		Description: req.Description,
		IsActive:    req.IsActive,
		Token:       req.Token,
	}

	v, err := h.service.Edit(&dto)
	if err != nil {
		return
	}

	vacancy = &protobuf.Vacancy{
		Id:          int32(v.Id),
		SectId:      int32(v.SektaId),
		Name:        v.Sect.Sektaname,
		Description: v.Description,
		IsActive:    v.IsActive,
		Token:       v.Token,
	}

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
	*err = ErrInternal
}
