package vacancy

import (
	"errors"
)

type Service struct {
	storage *Storage
}

func (s *Service) List() (vs []Vacancy, err error) {

	vs, err = s.storage.List()
	if err != nil {
		return
	}

	for i, v := range vs {
		if !v.IsActive {
			vs[i].Token = ""
		}
	}
	return
}

func (s *Service) Get(dto *GetDTO) (v *Vacancy, err error) {
	v, err = s.storage.Get(dto.Id)
	if err != nil {
		return
	}

	if !v.IsActive {
		err = ErrNotFound
		return
	}

	return
}

func (s *Service) Create(dto *CreateDTO) (v *Vacancy, err error) {

	v, err = s.storage.Find(dto.SectId)

	if errors.Is(err, ErrNotFound) {
		err = nil
	}

	if err != nil {
		return
	}

	// if err == nil {
	// 	err = errors.New("already exist")
	// 	return
	// }

	// if !errors.Is(err, ErrNotFound) {
	// 	return
	// }

	v, err = s.storage.Create(dto)
	if err != nil {
		return
	}

	return
}

func (s *Service) Edit(dto *EditDTO) (v *Vacancy, err error) {

	v, err = s.storage.Get(dto.Id)
	if err != nil {
		return
	}

	if dto.Token != v.Token {
		ErrNotOwner = errors.New("not owner")
		// err = ErrNotOwner
		return
	}

	err = s.storage.Edit(dto, v)
	if err != nil {
		return
	}

	v, err = s.storage.Get(dto.Id)
	if err != nil {
		return
	}

	return
}
