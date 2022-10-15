package vacancy

type Vacancy struct {
	Id          int
	SektaId     int
	Description string
	IsActive    bool
	Token       string
}

func (Vacancy) TableName() string {
	return "sekta_app_vacancy"
}
