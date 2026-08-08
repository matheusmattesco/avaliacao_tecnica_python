from django.db import models


class AccessRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDENTE", "Pendente"
        APPROVED = "APROVADO", "Aprovado"
        REJECTED = "REJEITADO", "Rejeitado"

    requester_name = models.CharField(max_length=150)
    requester_email = models.EmailField()
    system = models.CharField(max_length=150)
    profile = models.CharField(max_length=150)
    justification = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    decision_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      constraints = [
          models.UniqueConstraint(
              fields=[
                  "requester_email",
                  "system",
                  "profile",
              ],
              condition=models.Q(status="PENDENTE"),
              name="unique_pending_access_request",
          )
      ]