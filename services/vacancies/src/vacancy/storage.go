package vacancy

import (
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Storage struct {
	db *gorm.DB
}

func (s *Storage) List() (vs []Vacancy, err error) {

	err = s.db.
		Order("id desc").
		Limit(40).
		Find(&vs).Error

	return
}

func (s *Storage) Get(id int) (v *Vacancy, err error) {
	err = s.db.First(&v, id).Error

	if errors.Is(err, gorm.ErrRecordNotFound) {
		err = ErrNotFound
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

	err = s.db.Create(&v).Error

	if err != nil {
		err = ErrSectNotExist
		return
	}

	return
}

func (s *Storage) Edit(dto *EditDTO, v *Vacancy) (err error) {

	if dto.Description != "" {
		v.Description = dto.Description
	}

	v.IsActive = dto.IsActive

	err = s.db.Save(&v).Error
	if err != nil {
		return
	}

	return
}
