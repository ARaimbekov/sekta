package vacancy

import (
	"errors"
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Storage struct {
	db *gorm.DB
}

func (s *Storage) List() (vs []Vacancy, err error) {

	err = s.db.
		Preload("Sect").
		Order("id desc").
		Limit(40).
		Find(&vs).Error

	return
}

func (s *Storage) Get(id int, name string, isOnlyActive bool) (v *Vacancy, err error) {

	var result struct {
		Vacancy
		Sektaname string
	}

	query := fmt.Sprintf(`
	select
		v.id,
		v.sekta_id,
		v.token,
		v.description,
		v.is_active,
		s.sektaname
	from sekta_app_vacancy as v
	inner join sekta_app_sekta as s on v.sekta_id = s.id
	where (v.id = %d or s.sektaname = '%s')`, id, name)

	if isOnlyActive {
		query = query + ` and is_active = true`
	}

	res := s.db.
		Raw(query).
		Scan(&result)

	if res.RowsAffected == 0 {
		err = ErrNotFound
	}

	v = &Vacancy{
		Id:          result.Id,
		SektaId:     result.SektaId,
		Description: result.Description,
		IsActive:    result.IsActive,
		Token:       result.Token,
		Sect: Sect{
			Id:        result.SektaId,
			Sektaname: result.Sektaname,
		},
	}
	return
}

func (s *Storage) Find(id int) (v *Vacancy, err error) {
	err = s.db.
		Where("sekta_id = ?", id).
		First(&v).Error

	if errors.Is(err, gorm.ErrRecordNotFound) {
		err = ErrNotFound
	}

	return
}

func (s *Storage) Create(dto *CreateDTO) (v *Vacancy, err error) {

	v = &Vacancy{
		SektaId:     dto.SectId,
		Description: dto.Description,
		IsActive:    false,
		Token:       uuid.New().String(),
	}

	err = s.db.
		Preload("Sect").
		Create(&v).Error

	if err != nil {
		err = ErrSectNotExist
		return
	}

	return
}

func (s *Storage) Edit(dto *EditDTO, v *Vacancy) (err error) {

	return s.db.
		Model(&Vacancy{}).
		Where("id = ?", dto.Id).
		Updates(map[string]any{
			"description": dto.Description,
			"is_active":   dto.IsActive,
		}).Error

}
