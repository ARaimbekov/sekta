package vacancy

import (
	"errors"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	ErrInternal     = status.Error(codes.Internal, "internal error")
	ErrNotFound     = errors.New("vacancy not found or not activated")
	ErrWrongToken   = errors.New("invalid token")
	ErrSectNotExist = errors.New("sect doesnt exist")
	ErrNotOwner     = errors.New("not owner")

	knownErrors = []error{
		ErrNotFound,
		ErrWrongToken,
		ErrSectNotExist,
		ErrNotOwner,
	}
)
