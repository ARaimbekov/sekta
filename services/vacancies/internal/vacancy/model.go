package vacancy

type Vacancy struct {
	Id          int
	SektaId     int
	Description string
	IsActive    bool
	Token       string
	Sect        Sect `json:"location,omitempty" gorm:"foreignKey:SektaId;references:Id"`
}

func (Vacancy) TableName() string {
	return "sekta_app_vacancy"
}

type Sect struct {
	Id        int
	Sektaname string
}

func (Sect) TableName() string {
	return "sekta_app_sekta"
}
