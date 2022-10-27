import enum


class CustomerStatus(enum.Enum):
	NEW = 'new'
	SUITABLE = 'suitable'
	NOT_SUITABLE = 'not_suitable'
	BLACK_LIST = 'black_list'
