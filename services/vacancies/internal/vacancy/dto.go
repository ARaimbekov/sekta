package vacancy

type CreateDTO struct {
	SectId      int
	Description string
}

type GetDTO struct {
	Id   int
	Name string
}

type EditDTO struct {
	Id          int
	Description string
	IsActive    bool
	Token       string
}
