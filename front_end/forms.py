from django import forms

from telegram.models.model_app_task import TaskDeliveryStatus


class TaskForm(forms.Form):
	task_id = forms.IntegerField()
	status = forms.ChoiceField(choices=(
		(1, TaskDeliveryStatus.DRAFT.name_status),
		(2, TaskDeliveryStatus.READY_FOR_DELIVERY.name_status),
		(3, TaskDeliveryStatus.PARTLY_COMPLETED.name_status),
		(4, TaskDeliveryStatus.COMPLETED.name_status),
		(5, TaskDeliveryStatus.ERROR.name_status),
	)
	)
