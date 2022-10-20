import unittest


class TestBasic(unittest.TestCase):
	"""Basic tests"""

	def test_basic(self):
		a = 1
		self.assertEqual(1, a)

	def test_basic_2(self):
		a = 1
		assert a == 1


# For tests in the future
# async def main():
# 	tasks_experiments = [
# 		('[1], None', TasksRequest([1], None)),
# 		('[2, 5], None', TasksRequest([2, 5], None)),
# 		('[], StatusTask.DRAFT.value', TasksRequest([], StatusTask.DRAFT.value)),
# 		('[3], StatusTask.DRAFT.value', TasksRequest([3], StatusTask.DRAFT.value)),
# 		('[3, 7, 9], StatusTask.DRAFT.value', TasksRequest([3, 7, 9], StatusTask.DRAFT.value)),
# 		('[], None', TasksRequest([], None)),
# 	]
#
# 	for task in tasks_experiments:
# 		results = await MongoRepositoryTask().findTaskByParameters(task[1])
# 		experiment = []
# 		for y in results:
# 			experiment.append((y.task_id, y.status))
# 		print((task[0], f'Result: {experiment}'))
#
#
# asyncio.run(main())
