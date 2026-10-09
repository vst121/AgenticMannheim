
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.citizen_request import CitizenRequest, CitizenRequestStatus
from infrastructure.persistence.models.citizen_request import (
    CitizenRequestModel,
)


class CitizenRequestRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, request: CitizenRequest) -> CitizenRequest:
        model = CitizenRequestModel.from_domain(request)
        self._session.add(model)
        self._session.flush()
        return model.to_domain()

    def get_by_id(self, request_id: UUID) -> CitizenRequest | None:
        model = self._session.get(CitizenRequestModel, request_id)
        return model.to_domain() if model is not None else None

    def list_recent(
        self,
        limit: int = 50,
        status: CitizenRequestStatus | None = None,
    ) -> list[CitizenRequest]:
        if limit < 1:
            raise ValueError("limit must be greater than zero.")

        statement = select(CitizenRequestModel)

        if status is not None:
            statement = statement.where(
                CitizenRequestModel.status == status.value
            )

        statement = statement.order_by(
            CitizenRequestModel.created_at.desc(),
            CitizenRequestModel.id.desc(),
        ).limit(limit)

        models = self._session.scalars(statement).all()
        return [model.to_domain() for model in models]

    def update(self, request: CitizenRequest) -> CitizenRequest:
        model = self._session.get(CitizenRequestModel, request.id)

        if model is None:
            raise ValueError(
                f"Citizen request '{request.id}' was not found."
            )

        model.request_type = request.request_type.value
        model.description = request.description
        model.latitude = request.location.latitude
        model.longitude = request.location.longitude
        model.status = request.status.value
        model.created_at = request.created_at
        model.correlation_id = request.correlation_id

        self._session.flush()
        return model.to_domain()
