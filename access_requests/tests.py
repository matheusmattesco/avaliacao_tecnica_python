from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from access_requests.models import AccessRequest, DecisionHistory


class AccessRequestAPITestCase(APITestCase):

    #Teste para criar uma solicitação de acesso

    def test_create_access(self):
        payload = {
            "requester_name": "Usuario",
            "requester_email": "usuario@email.com",
            "system": "SAP",
            "profile": "Administrador",
            "justification": "Necessário para execução das atividades.",
        }

        response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["requester_email"],
            "usuario@email.com",
        )

        self.assertEqual(
            response.data["status"],
            AccessRequest.Status.PENDING,
        )

    #Teste para não permitir solicitações duplicadas pendentes

    def test_not_allow_duplicate(self):
        payload = {
            "requester_name": "Usuario 2",
            "requester_email": "usuario2@email.com",
            "system": "SAP",
            "profile": "Administrador",
            "justification": "Necessário para execução das atividades.",
        }

        first_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        second_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # Testes para aprovar solicitações de acesso

    def test_approve_pending_request(self):
        payload = {
            "requester_name": "Usuario 3",
            "requester_email": "usuario3@email.com",
            "system": "SAP",
            "profile": "Administrador",
            "justification": "Necessário para execução das atividades.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        response = self.client.post(
            f"/api/requests/{request_id}/approve/",
            {
                "decision_reason": "Acesso necessário para execução das atividades.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            AccessRequest.Status.APPROVED,
        )

        self.assertEqual(
            response.data["decision_reason"],
            "Acesso necessário para execução das atividades.",
        )

    # Testes para rejeitar solicitações de acesso

    def test_reject_pending_request(self):
        payload = {
            "requester_name": "Usuario 4",
            "requester_email": "usuario4@email.com",
            "system": "CRM",
            "profile": "Consulta",
            "justification": "Necessário para atendimento.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        response = self.client.post(
            f"/api/requests/{request_id}/reject/",
            {
                "decision_reason": "O perfil solicitado não é necessário.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            AccessRequest.Status.REJECTED,
        )

    # Testes para garantir que a decisão de aprovação exija uma razão
    
    def test_approve_requires_decision_reason(self):
        payload = {
            "requester_name": "Usuario 5",
            "requester_email": "usuario5@email.com",
            "system": "SAP",
            "profile": "Administrador",
            "justification": "Necessário para execução das atividades.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        response = self.client.post(
            f"/api/requests/{request_id}/approve/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # Testes para garantir que a decisão de rejeição exija uma razão    

    def test_reject_requires_decision_reason(self):
        payload = {
            "requester_name": "Usuario 6",
            "requester_email": "usuario6@email.com",
            "system": "CRM",
            "profile": "Consulta",
            "justification": "Necessário para atendimento.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        response = self.client.post(
            f"/api/requests/{request_id}/reject/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # Testes para garantir que solicitações já aprovadas não possam ser aprovadas ou rejeitadas novamente

    def test_should_not_approve_already_approved_request(self):
        payload = {
            "requester_name": "Usuario 7",
            "requester_email": "usuario7@email.com",
            "system": "SAP",
            "profile": "Administrador",
            "justification": "Necessário para execução das atividades.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        self.client.post(
            f"/api/requests/{request_id}/approve/",
            {
                "decision_reason": "Acesso necessário.",
            },
            format="json",
        )

        response = self.client.post(
            f"/api/requests/{request_id}/approve/",
            {
                "decision_reason": "Tentativa novamente.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # Testes para garantir que solicitações já rejeitadas não possam ser aprovadas ou rejeitadas novamente

    def test_should_not_reject_already_rejected_request(self):
        payload = {
            "requester_name": "Usuario 8",
            "requester_email": "usuario8@email.com",
            "system": "CRM",
            "profile": "Consulta",
            "justification": "Necessário para atendimento.",
        }

        create_response = self.client.post(
            "/api/requests/",
            payload,
            format="json",
        )

        request_id = create_response.data["id"]

        self.client.post(
            f"/api/requests/{request_id}/reject/",
            {
                "decision_reason": "Acesso não necessário.",
            },
            format="json",
        )

        response = self.client.post(
            f"/api/requests/{request_id}/reject/",
            {
                "decision_reason": "Tentativa novamente.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # Testes para garantir que o histórico de decisões seja criado corretamente ao aprovar uma solicitação

    def test_creates_history(self):
            payload = {
                "requester_name": "Matheus",
                "requester_email": "historico-aprovacao@email.com",
                "system": "SAP",
                "profile": "Administrador",
                "justification": "Necessário para execução das atividades.",
            }

            create_response = self.client.post(
                "/api/requests/",
                payload,
                format="json",
            )

            request_id = create_response.data["id"]

            decision_reason = "Acesso necessário para execução das atividades."

            response = self.client.post(
                f"/api/requests/{request_id}/approve/",
                {
                    "decision_reason": decision_reason,
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            history = DecisionHistory.objects.filter(
                access_request_id=request_id
            )

            self.assertEqual(history.count(), 1)

            self.assertEqual(
                history.first().action,
                DecisionHistory.Action.APPROVED,
            )

            self.assertEqual(
                history.first().reason,
                decision_reason,
            )
                    